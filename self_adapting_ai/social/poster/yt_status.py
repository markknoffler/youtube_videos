import sys; sys.path.insert(0, ".")
from cdp import *
with sync_playwright() as p:
    b, ctx = session(p)
    pg = reuse_tab(ctx, "studio.youtube.com", "https://studio.youtube.com/channel/UCc62FDX2tPIwh0Wq9C-HKaw/videos/short")
    pg.wait_for_timeout(8000)
    t = pg.locator("ytcp-video-list-cell-video #video-title").all_inner_texts()
    print(len(t)); [print(x) for x in t]
    print("tabs:", len(ctx.pages))
