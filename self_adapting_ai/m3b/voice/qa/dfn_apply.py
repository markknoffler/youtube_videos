import sys, soundfile as sf, torch
from df.enhance import enhance, init_df
m, state, _ = init_df()
y, sr = sf.read(sys.argv[1], dtype="float32"); assert sr == state.sr(), sr
lim = float(sys.argv[3]) if len(sys.argv) > 3 else None
sf.write(sys.argv[2], enhance(m, state, torch.from_numpy(y)[None], atten_lim_db=lim)[0].numpy(), sr)
