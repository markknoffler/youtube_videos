"""Post reels one at a time in ONE existing Instagram tab. usage: ig_upload.py slug [slug ...]"""
import sys, json, time; sys.path.insert(0, ".")
from cdp import *
D = "/Users/samreedhbhuyan/Desktop/Win_C/youtube_videos/self_adapting_ai/shorts"
copy = {c["slug"]: c for c in json.load(open(f"{D}/shorts_copy2.json"))}
FULL = "https://youtu.be/2tdrON7G6PU"


def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)


with sync_playwright() as p:
    b, ctx = session(p)
    pg = reuse_tab(ctx, "instagram.com")
    for slug in sys.argv[1:]:
        cap = copy[slug]["ig_caption"].replace("(link in bio)", f"\n{FULL}")
        try:
            pg.goto("https://www.instagram.com/", wait_until="domcontentloaded"); pg.wait_for_timeout(4000)
            pg.get_by_role("link", name="New post").first.click(timeout=10000); pg.wait_for_timeout(1500)
            with pg.expect_file_chooser() as fc:
                pg.get_by_role("button", name="Select from computer").click()
            fc.value.set_files(f"{D}/out2/{slug}.mp4"); pg.wait_for_timeout(7000)
            try: pg.get_by_role("button", name="OK").click(timeout=3000); pg.wait_for_timeout(1500)
            except Exception: pass
            for _ in range(2):
                pg.get_by_role("button", name="Next").first.click(timeout=10000); pg.wait_for_timeout(2500)
            box = pg.locator("div[role=dialog] [contenteditable=true], div[role=dialog] textarea").first
            box.click(); pg.keyboard.insert_text(cap); pg.wait_for_timeout(1000)
            pg.get_by_role("button", name="Share").first.click(timeout=8000)
            ok = False
            for _ in range(30):
                pg.wait_for_timeout(5000)
                t = pg.locator("div[role=dialog]").last.inner_text()[:80] if pg.locator("div[role=dialog]").count() else ""
                if "shared" in t.lower(): ok = True; break
            log("REEL", slug, "shared" if ok else "UNCONFIRMED")
        except Exception as e:
            log("FAIL", slug, str(e)[:150])
        finally:
            try: pg.goto("https://www.instagram.com/", wait_until="domcontentloaded")
            except Exception: pass
            log("tabs:", len(ctx.pages))
        pg.wait_for_timeout(90000)
    log("ALLDONE")
