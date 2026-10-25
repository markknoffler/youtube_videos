"""Associative memory written at inference: pure Hebbian outer products vs the delta rule.
M stores (k_i -> v_i); recall = argmax over value codebook of M k_q.  Keys are correlated
(shared component) as real token keys are.  Writes hebb_vs_delta.json."""
import json, numpy as np
rng = np.random.default_rng(0)
d, NV, trials = 64, 64, 40
vals = rng.normal(size=(NV, d)); vals /= np.linalg.norm(vals, axis=1, keepdims=True)
def run(n_pairs, rule, corr=0.6, beta=1.0, sweeps=1):
    acc = []
    for _ in range(trials):
        common = rng.normal(size=d)
        K = corr * common + np.sqrt(1 - corr ** 2) * rng.normal(size=(n_pairs, d))
        K /= np.linalg.norm(K, axis=1, keepdims=True)
        vi = rng.integers(0, NV, n_pairs); V = vals[vi]
        M = np.zeros((d, d))
        for _ in range(sweeps):
            for k, v in zip(K, V):
                M += np.outer(v, k) if rule == "hebb" else beta * np.outer(v - M @ k, k)
        pred = (K @ M.T) @ vals.T
        acc.append((pred.argmax(1) == vi).mean())
    return float(np.mean(acc))
Ns = [2, 4, 8, 16, 24, 32, 48, 64]
out = {"n_pairs": Ns, "hebb": [run(n, "hebb") for n in Ns], "delta": [run(n, "delta") for n in Ns],
       "delta_3sweeps": [run(n, "delta", sweeps=3) for n in Ns], "d": d, "key_correlation": 0.6, "trials": trials}
json.dump(out, open("hebb_vs_delta.json", "w"), indent=1)
for k in ("hebb", "delta", "delta_3sweeps"): print(k, [round(x, 2) for x in out[k]])
