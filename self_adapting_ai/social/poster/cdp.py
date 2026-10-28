"""Attach to the user's logged-in Chrome-for-Testing over CDP (localhost:9222).
Rules: never more than 3 tabs open; every tab this code opens is closed in a finally block."""
from playwright.sync_api import sync_playwright

MAX_TABS = 3


def session(p):
    b = p.chromium.connect_over_cdp("http://localhost:9222", timeout=240000)
    return b, b.contexts[0]


def page_by_url(ctx, frag):
    for pg in ctx.pages:
        if frag in pg.url:
            return pg
    return None


def reuse_tab(ctx, frag, goto=None):
    """Reuse an existing tab whose URL contains frag; navigate it to goto. Opens a new one only when under the cap."""
    pg = page_by_url(ctx, frag)
    if pg is None:
        if len(ctx.pages) >= MAX_TABS:
            pg = ctx.pages[-1]           # reuse the last tab instead of opening a 4th
        else:
            pg = ctx.new_page()
    if goto:
        pg.goto(goto, wait_until="domcontentloaded")
    return pg
