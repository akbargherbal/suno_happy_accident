#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""watch_reply.py — read-only watcher for the AI Studio answer.

Connects over CDP (:9222), waits until generation stops (the `Stop` control
disappears), then saves the page text to a file. Clicks nothing, types nothing.
"""
import sys, time, datetime
from pathlib import Path
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
URL_KEY = "aistudio.google.com"
MAX_SECONDS = int(sys.argv[1]) if len(sys.argv) > 1 else 1200
OUT = Path(sys.argv[2] if len(sys.argv) > 2
           else "GEMINI/rounds/01_ab/response_raw.txt")

JS_TEXT = r"""() => {
  const main = document.querySelector('main') || document.body;
  return (main.innerText || '');
}"""

JS_RUNNING = r"""() => {
  const t = (document.body.innerText || '');
  const stop = [...document.querySelectorAll('button,mat-icon,span')]
      .some(e => (e.innerText || '').trim() === 'Stop');
  return stop || /\\bRunning\\.\\.\\.$/.test(t.trim().slice(-40));
}"""


def main():
    t0 = time.time()
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        pages = [pg for c in b.contexts for pg in c.pages]
        pg = next(x for x in pages if URL_KEY in x.url)
        # wait for generation to finish
        while time.time() - t0 < MAX_SECONDS:
            if not pg.evaluate(JS_RUNNING):
                break
            time.sleep(5)
        time.sleep(3)  # let the final render settle
        text = pg.evaluate(JS_TEXT)
        OUT.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.datetime.now().isoformat(timespec="seconds")
        OUT.write_text(f"# captured {stamp}  url={pg.url}\n"
                       f"# waited {time.time()-t0:.0f}s  chars={len(text)}\n\n{text}",
                       encoding="utf-8")
        print(f"saved {len(text)} chars -> {OUT}")
        b.close()


if __name__ == "__main__":
    main()
