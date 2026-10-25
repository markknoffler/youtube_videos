"""Same 90% sparsity, two layouts: unstructured (random synapses) vs 16x16 tile blocks.
Measures effective GFLOP/s of y = W x on this machine. Writes tile_sparsity.json."""
import json, time, torch
torch.manual_seed(0)
out = {}
for dev in ["cpu"]:
    n, b, keep, T = 2048, 64, 0.10, 16
    X = torch.randn(n, b, device=dev)
    sync = (lambda: torch.mps.synchronize()) if dev == "mps" else (lambda: None)
    def bench(f, reps=10):
        for _ in range(3): f()
        sync(); t = time.perf_counter()
        for _ in range(reps): f()
        sync(); return (time.perf_counter() - t) / reps
    useful = 2 * n * n * keep * b
    Wd = torch.randn(n, n, device=dev)
    dense = useful / keep / bench(lambda: Wd @ X) / 1e9
    nnz = int(n * n * keep)                                   # unstructured: COO gather-scatter
    r, c = torch.randint(0, n, (nnz,), device=dev), torch.randint(0, n, (nnz,), device=dev)
    w = torch.randn(nnz, 1, device=dev)
    uns = useful / bench(lambda: torch.zeros(n, b, device=dev).index_add_(0, r, X.index_select(0, c) * w)) / 1e9
    nt = n // T; nb = int(nt * nt * keep)                     # tile-sparse: dense 16x16 blocks, batched
    br, bc = torch.randint(0, nt, (nb,), device=dev), torch.randint(0, nt, (nb,), device=dev)
    Wt = torch.randn(nb, T, T, device=dev); Xt = X.view(nt, T, b)
    def tiles():
        return torch.zeros(nt, T, b, device=dev).index_add_(0, br, torch.bmm(Wt, Xt[bc]))
    til = useful / bench(tiles) / 1e9
    out[dev] = dict(dense_gflops=dense, unstructured_gflops=uns, tile16_gflops=til, sparsity=1 - keep)
    print(dev, {k: round(v, 1) for k, v in out[dev].items()})
json.dump(out, open("tile_sparsity.json", "w"), indent=1)
