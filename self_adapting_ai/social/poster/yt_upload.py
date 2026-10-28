"""Upload shorts one at a time in ONE existing Studio tab (no extra tabs). usage: yt_upload.py slug [slug ...]"""
import sys, json, time; sys.path.insert(0, ".")
from cdp import *
D = "/Users/samreedhbhuyan/Desktop/Win_C/youtube_videos/self_adapting_ai/shorts"
copy = {c["slug"]: c for c in json.load(open(f"{D}/shorts_copy2.json"))}


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


def upload(pg, slug):
    c = copy[slug]
    pg.goto("https://studio.youtube.com", wait_until="domcontentloaded"); pg.wait_for_timeout(6000)
    pg.get_by_role("button", name="Create").first.click(); pg.wait_for_timeout(1000)
    pg.get_by_text("Upload videos", exact=True).first.click(); pg.wait_for_timeout(2500)
    with pg.expect_file_chooser() as fc:
        pg.get_by_role("button", name="Select files").click()
    fc.value.set_files(f"{D}/out2/{slug}.mp4"); pg.wait_for_timeout(9000)
    t = pg.locator("#title-textarea #textbox"); t.click(); pg.keyboard.press("Meta+a"); pg.keyboard.insert_text(c["yt_title"])
    d = pg.locator("#description-textarea #textbox"); d.click(); pg.keyboard.press("Meta+a"); pg.keyboard.insert_text(c["yt_description"])
    pg.locator("[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first.click(); pg.wait_for_timeout(800)
    for _ in range(3):
        pg.locator("#next-button").first.click(); pg.wait_for_timeout(2500)
    pg.locator("tp-yt-paper-radio-button[name='PUBLIC']").first.click(); pg.wait_for_timeout(800)
    t0 = time.time()
    while time.time() - t0 < 900:
        if "Checks complete" in pg.locator("ytcp-uploads-dialog").inner_text(): break
        pg.wait_for_timeout(8000)
    pg.locator("#done-button").first.click(); pg.wait_for_timeout(7000)
    ok = "Video published" in pg.locator("body").inner_text()
    log("DONE" if ok else "UNCONFIRMED", slug)
    return ok


with sync_playwright() as p:
    b, ctx = session(p)
    pg = reuse_tab(ctx, "studio.youtube.com")
    for slug in sys.argv[1:]:
        try:
            upload(pg, slug)
        except Exception as e:
            log("FAIL", slug, str(e)[:150])
        finally:
            try: pg.goto("https://studio.youtube.com", wait_until="domcontentloaded")   # drop any leftover dialog
            except Exception: pass
            log("tabs:", len(ctx.pages))
    log("ALLDONE")
