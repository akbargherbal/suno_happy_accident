#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""studio.py — drive Google AI Studio through the user's Chrome on :9222.

Safety contract
---------------
* Only elements inside the chat area and the right-hand run-settings panel are used.
* Nothing is ever clicked in: API key, billing, upgrade/unlock, reset-settings.
* STAGE-1 RULE (AGENTS §6): the agent never presses Run. `send` is disabled and
  explains why. Use `prepare`: it fills the system prompt, attaches the files and
  writes the message, then stops.

Usage
-----
  python3 GEMINI/studio.py state
  python3 GEMINI/studio.py newchat
  python3 GEMINI/studio.py clean
  python3 GEMINI/studio.py sys-show
  python3 GEMINI/studio.py sys-set GEMINI/system_prompt.txt
  python3 GEMINI/studio.py sys-clear
  python3 GEMINI/studio.py attach FILE
  python3 GEMINI/studio.py attachments
  python3 GEMINI/studio.py detach
  python3 GEMINI/studio.py draft FILE
  python3 GEMINI/studio.py prepare --files A.mp3[,B.mp3] --system F --message F
  python3 GEMINI/studio.py last [CHARS]
  python3 GEMINI/studio.py dump [CHARS]
"""
import argparse, sys, time, re
from pathlib import Path
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9222"
URL_KEY = "aistudio.google.com"

SEL_PROMPT = 'textarea[aria-label="Enter a prompt"]'
SEL_ATTACH = '[aria-label="Insert images, videos, audio, or files"]'
SEL_TOOLS = '[aria-label="Open tools menu"]'
SEL_RUN = 'button.ctrl-enter-submits'
SEL_SYS_BTN = 'button:has-text("System instructions")'
SEL_SYS_BOX = 'textarea[aria-label="System instructions"]'


class Studio:
    def __init__(self, p):
        self.b = p.chromium.connect_over_cdp(CDP)
        pages = [pg for c in self.b.contexts for pg in c.pages]
        self.pg = next(x for x in pages if URL_KEY in x.url)
        self.pg.bring_to_front()
        time.sleep(0.2)

    # ---------- primitives ----------
    def overlays(self):
        return self.pg.evaluate(
            "() => document.querySelectorAll('.cdk-overlay-container > *').length")

    def clean(self, n=3):
        for _ in range(n):
            if self.overlays() == 0:
                return True
            self.pg.keyboard.press("Escape")
            time.sleep(0.5)
        return self.overlays() == 0

    def overlay_text(self, limit=400):
        txt = self.pg.evaluate(
            "() => [...document.querySelectorAll('.cdk-overlay-container > *')]"
            ".map(e => (e.innerText || '').trim()).join('\\n---\\n')")
        return (txt or "")[:limit]

    def close(self):
        try:
            self.b.close()
        except Exception:
            pass

    # ---------- commands ----------
    def newchat(self):
        """Navigate the AI Studio tab to a fresh chat (old one stays in History)."""
        self.pg.goto("https://aistudio.google.com/prompts/new_chat")
        self.pg.wait_for_load_state("domcontentloaded")
        time.sleep(2.0)
        print("navigated:", self.pg.url)

    def state(self):
        print("url        :", self.pg.url)
        print("overlays   :", self.overlays(), "(0 = nothing open)")
        print("prompt box :", self.pg.locator(SEL_PROMPT).count())
        print("run button :", self.pg.locator(SEL_RUN).count())
        try:
            v = self.pg.locator(SEL_SYS_BOX).first.input_value()
        except Exception:
            v = None
        print("system     :", (v.splitlines()[0][:70] + f"  [{len(v)} chars]") if v else "(closed; open to read)")
        print("draft len  :", len(self.pg.locator(SEL_PROMPT).first.input_value()))

    def sys_show(self):
        self.pg.locator(SEL_SYS_BTN).first.click()
        time.sleep(0.8)
        v = self.pg.locator(SEL_SYS_BOX).first.input_value()
        print(v)
        self.clean()

    def sys_set(self, path):
        text = Path(path).read_text(encoding="utf-8").strip("\n")
        self.pg.locator(SEL_SYS_BTN).first.click()
        time.sleep(0.8)
        self.pg.locator(SEL_SYS_BOX).first.fill(text)
        time.sleep(0.6)
        got = self.pg.locator(SEL_SYS_BOX).first.input_value()
        print(f"system instructions set: {len(got)} chars, match={got == text}")
        self.clean()

    def sys_clear(self):
        self.pg.locator(SEL_SYS_BTN).first.click()
        time.sleep(0.8)
        self.pg.locator(SEL_SYS_BOX).first.fill("")
        time.sleep(0.4)
        print("system instructions cleared; closing")
        self.clean()

    def attach(self, path):
        p = Path(path).resolve()
        if not p.exists():
            raise SystemExit(f"no such file: {p}")
        self.clean()
        with self.pg.expect_file_chooser() as info:
            self.pg.locator(SEL_ATTACH).first.click()
            time.sleep(0.7)
            self.pg.get_by_text("Upload files", exact=False).first.click()
        chooser = info.value
        chooser.set_files(str(p))
        time.sleep(1.5)
        print("attached:", p.name, f"({p.stat().st_size/1e6:.1f} MB)")
        self.attachments()

    def attachments(self):
        js = r"""() => {
          const box = [...document.querySelectorAll('*')].find(e =>
             e.querySelector && e.querySelector('textarea[aria-label="Enter a prompt"]'));
          if (!box) return [];
          const names = new Set();
          box.querySelectorAll('*').forEach(e => {
            const t = (e.innerText || '').trim();
            if (t && t.length < 120 && /\.(mp3|wav|m4a|flac|ogg|pdf|txt)$/i.test(t)) names.add(t);
          });
          return [...names];
        }"""
        names = self.pg.evaluate(js)
        print("attachments:", names if names else "none detected")

    def detach(self):
        btns = self.pg.locator('[aria-label*="Remove"], [aria-label*="remove"]')
        n = btns.count()
        print("remove buttons:", n, "(selector is best-effort)")
        for i in range(n):
            try:
                btns.nth(i).click()
                time.sleep(0.3)
            except Exception:
                pass
        self.attachments()

    def draft(self, path):
        text = Path(path).read_text(encoding="utf-8")
        self.pg.locator(SEL_PROMPT).first.fill(text)
        time.sleep(0.4)
        got = self.pg.locator(SEL_PROMPT).first.input_value()
        print(f"draft written: {len(got)} chars (NOT sent)")

    def send(self, yes):
        raise SystemExit(
            "disabled by the stage-1 rule (AGENTS §6): the owner presses Run.\n"
            "Use `prepare` to leave everything ready, then send it yourself.")

    def prepare(self, files, system, message):
        """Fill the system prompt and the message; list the files for the owner to attach."""
        self.clean()
        if system:
            self.sys_set(system)
        if message:
            self.draft(message)
        print("\n--- ready state ---")
        self.state()
        if files:
            print("\nارفعها بنفسك (زر الإرفاق ← Upload files، أو اسحبها):")
            for f in files:
                p = Path(f).resolve()
                print(f"    {p}   ({p.stat().st_size/1e6:.1f} MB)" if p.exists() else f"    MISSING: {f}")
        self.attachments()
        print("\nREADY. Nothing has been attached or sent by the agent. Attach, then press Run yourself.")

    def last(self, chars=1200):
        js = r"""(n) => {
          const main = document.querySelector('main') || document.body;
          const t = (main.innerText || '').trim();
          return t.slice(-n);
        }"""
        return self.pg.evaluate(js, int(chars))

    def dump(self, chars=3000):
        print(self.pg.evaluate("(n)=>document.body.innerText.slice(0,n)", int(chars)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["state", "newchat", "clean", "sys-show", "sys-set", "sys-clear",
                                    "attach", "attachments", "detach", "draft", "prepare",
                                    "send", "last", "dump"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--files", help="comma-separated file paths to attach")
    ap.add_argument("--system", help="path to the system instructions text")
    ap.add_argument("--message", help="path to the message text")
    a = ap.parse_args()

    with sync_playwright() as p:
        s = Studio(p)
        try:
            if a.cmd == "state":       s.state()
            elif a.cmd == "newchat":   s.newchat()
            elif a.cmd == "clean":     print("clean:", s.clean())
            elif a.cmd == "sys-show":  s.sys_show()
            elif a.cmd == "sys-set":   s.sys_set(a.arg)
            elif a.cmd == "sys-clear": s.sys_clear()
            elif a.cmd == "attach":    s.attach(a.arg)
            elif a.cmd == "attachments": s.attachments()
            elif a.cmd == "detach":    s.detach()
            elif a.cmd == "draft":     s.draft(a.arg)
            elif a.cmd == "prepare":   s.prepare((a.files or "").split(",") if a.files else [],
                                                 a.system, a.message)
            elif a.cmd == "send":      s.send(a.yes)
            elif a.cmd == "last":      print(s.last(a.arg or 1200))
            elif a.cmd == "dump":      s.dump(a.arg or 3000)
        finally:
            s.close()


if __name__ == "__main__":
    main()
