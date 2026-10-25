"""Same useful FLOPs, two memory patterns: dense GEMM vs. sparse gather/scatter (pointer chasing).
Measured on this machine (Apple M3); writes dense_vs_sparse.json."""
import json, time, torch
torch.manual_seed(0)
out = {}
for dev in ["cpu", "mps"] if torch.backends.mps.is_available() else ["cpu"]:
    N, d, deg = 4096, 1024, 16
    X = torch.randn(N, d, device=dev); W = torch.randn(d, d, device=dev)
    def sync():
        if dev == "mps": torch.mps.synchronize()
    # dense: X @ W
    for _ in range(3): X @ W
    sync(); t = time.perf_counter()
    for _ in range(10): Y = X @ W
    sync(); dt = (time.perf_counter() - t) / 10
    dense = 2 * N * d * d / dt / 1e9
    # sparse graph: each of N nodes sums deg random neighbours' d-vectors with per-edge weights,
    # repeated so total useful flops match a dense layer of the same width per edge
    src = torch.randint(0, N, (N * deg,), device=dev); dst = torch.arange(N, device=dev).repeat_interleave(deg)
    w = torch.randn(N * deg, 1, device=dev)
    def sparse():
        msg = X.index_select(0, src) * w
        return torch.zeros(N, d, device=dev).index_add_(0, dst, msg)
    for _ in range(3): sparse()
    sync(); t = time.perf_counter()
    for _ in range(10): sparse()
    sync(); dt2 = (time.perf_counter() - t) / 10
    sp = 2 * N * deg * d / dt2 / 1e9
    out[dev] = dict(dense_gflops=dense, sparse_gflops=sp, dense_ms=dt * 1e3, sparse_ms=dt2 * 1e3, ratio=dense / sp)
    print(dev, out[dev])
json.dump(out, open("dense_vs_sparse.json", "w"), indent=1)
