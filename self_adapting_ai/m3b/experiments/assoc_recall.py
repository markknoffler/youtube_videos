"""In-context associative recall: tiny Transformer vs self-organizing Hebbian rewiring net.

Task: [k1 v1 k2 v2 ... kP vP  q] -> value bound to q.  Measured on this machine (Apple M3).
Outputs results.json with per-epoch accuracy, loss and effective rank, plus the final
singular-value spectra of both models' query representations.
"""
import json, math, os, time
import numpy as np, torch, torch.nn as nn, torch.nn.functional as F

torch.manual_seed(0); np.random.seed(0)
DEV = "mps" if torch.backends.mps.is_available() else "cpu"
P, NK, NV, D = int(os.environ.get("PAIRS", 64)), 96, 13, 64     # 64 pairs -> 129 tokens
EPOCHS, STEPS, B = int(os.environ.get("EPOCHS", 100)), 40, 128
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"results_p{P}{os.environ.get('TAG', '')}.json")

def batch(n):
    keys = torch.stack([torch.randperm(NK)[:P] for _ in range(n)])
    vals = torch.randint(0, NV, (n, P))
    qi = torch.randint(0, P, (n,))
    seq = torch.empty(n, 2 * P + 1, dtype=torch.long)
    seq[:, 0:-1:2], seq[:, 1:-1:2] = keys, vals + NK
    seq[:, -1] = keys[torch.arange(n), qi]
    return seq.to(DEV), vals[torch.arange(n), qi].to(DEV)

def eff_rank(h):
    s = torch.linalg.svdvals(h.float().cpu() - h.float().cpu().mean(0))
    p = s / s.sum()
    return float(torch.exp(-(p * torch.log(p + 1e-12)).sum())), (s / s[0]).tolist()

class Transformer(nn.Module):
    def __init__(s, layers=2, heads=4):
        super().__init__()
        s.emb, s.pos = nn.Embedding(NK + NV, D), nn.Embedding(2 * P + 1, D)
        L = nn.TransformerEncoderLayer(D, heads, 4 * D, dropout=0.0, batch_first=True, norm_first=True)
        s.enc, s.out = nn.TransformerEncoder(L, layers), nn.Linear(D, NV)
        s.register_buffer("mask", torch.triu(torch.full((2 * P + 1,) * 2, float("-inf")), 1))
    def forward(s, x):
        h = s.enc(s.emb(x) + s.pos.weight[None], mask=s.mask)[:, -1]
        return s.out(h), h

class SelfOrganizing(nn.Module):
    """Recurrent net whose recurrent synapses learn only by local Oja/Hebbian updates,
    with lateral competition and top-k structural pruning + random sprouting.
    Readout is trained by the local delta rule (no backprop through time)."""
    def __init__(s, H=D, k=16):
        super().__init__()
        s.H, s.k = H, k
        s.emb = torch.randn(NK + NV, H, device=DEV) / math.sqrt(H)
        s.Win = torch.randn(H, H, device=DEV) / math.sqrt(H)                       # plastic input synapses
        s.W = torch.randn(H, H, device=DEV) * 0.3 / math.sqrt(H)
        s.mask = (torch.rand(H, H, device=DEV) < 0.25).float()
        s.R = torch.zeros(H, NV, device=DEV)
    def run(s, x):
        h = torch.zeros(x.shape[0], s.H, device=DEV); traj = []
        for t in range(x.shape[1]):
            h = torch.tanh(s.emb[x[:, t]] @ s.Win + h @ (s.W * s.mask)); traj.append(h)
        return h, torch.stack(traj, 1)
    def forward(s, x):
        h, _ = s.run(x); return h @ s.R, h
    @torch.no_grad()
    def plasticity(s, x, y, eta=2e-3 * float(os.environ.get('ETA', 1)), lr=0.05):
        h, traj = s.run(x)
        pre, post = traj[:, :-1].reshape(-1, s.H), traj[:, 1:].reshape(-1, s.H)
        xin = s.emb[x.reshape(-1)]; yin = xin @ s.Win
        s.Win += eta * 5 * (xin.T @ yin - s.Win * (yin * yin).sum(0)) / len(xin)  # per-neuron Oja on inputs
        yy = post.T @ post / len(post)
        s.W += eta * (pre.T @ post / len(pre) - s.W @ yy)                        # Oja: x y^T - W y y^T
        s.W -= eta * 0.5 * (s.W.mean(1, keepdim=True))                            # lateral competition
        thr = (s.W * s.mask).abs().flatten().kthvalue(int(s.H * s.H * (1 - s.k / s.H)) or 1).values
        s.mask = ((s.W.abs() >= thr) | (torch.rand_like(s.mask) < 0.01)).float()  # prune top-k, sprout
        err = F.one_hot(y, NV).float() - torch.softmax(h @ s.R, -1)
        s.R += lr * h.T @ err / len(h)                                           # delta-rule readout

def evaluate(m, n=1024):
    with torch.no_grad():
        x, y = batch(n); logits, h = m(x)
        return float((logits.argmax(-1) == y).float().mean()), float(F.cross_entropy(logits, y)), h

tf, so = Transformer().to(DEV), SelfOrganizing()
opt = torch.optim.AdamW(tf.parameters(), 3e-4 * 3, weight_decay=0.01)
log = {"config": dict(pairs=P, tokens=2 * P + 1, keys=NK, values=NV, d=D, epochs=EPOCHS,
                      steps_per_epoch=STEPS, batch=B, device=DEV, chance=1 / NV,
                      tf_params=sum(p.numel() for p in tf.parameters())),
       "epochs": []}
t0 = time.time()
for ep in range(1, EPOCHS + 1):
    for _ in range(STEPS):
        x, y = batch(B)
        if not os.environ.get("SO_ONLY"):
            loss = F.cross_entropy(tf(x)[0], y); opt.zero_grad(); loss.backward(); opt.step()
        so.plasticity(*batch(B))
    a1, l1, h1 = evaluate(tf); a2, l2, h2 = evaluate(so)
    r1, s1 = eff_rank(h1); r2, s2 = eff_rank(h2)
    log["epochs"].append(dict(epoch=ep, tf_acc=a1, tf_loss=l1, tf_rank=r1, so_acc=a2, so_loss=l2, so_rank=r2,
                              so_edges=int(so.mask.sum())))
    print(f"ep {ep:3d} tf {a1:.3f} r{r1:5.2f} | so {a2:.3f} r{r2:5.2f} | {time.time()-t0:.0f}s", flush=True)
log["tf_spectrum"], log["so_spectrum"] = s1, s2
log["seconds"] = time.time() - t0
json.dump(log, open(OUT, "w"), indent=1)
