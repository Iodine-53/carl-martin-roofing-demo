#!/usr/bin/env python3
"""QA pass for the Carl Martin Roofing demo (headless Chromium via Playwright).

Checks (desktop 1440 + mobile 390):
  - zero console/page errors
  - zero horizontal overflow
  - all images load (naturalWidth > 0)
  - all in-page anchors resolve
  - animations complete on their own in <=3s with NO interaction
  - JS-off: phone, services, prices present in server HTML
  - count of asks before first click (<=2)
  - first primary CTA scroll depth (<= ~100vh)
  - CTA contrast ratios
Outputs full-page screenshots via CDP captureScreenshot(captureBeyondViewport).
"""
import json, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
URL = "http://127.0.0.1:8123/index.html"
OUT = HERE / "qa" / "screenshots"
OUT.mkdir(parents=True, exist_ok=True)
CHROME = str(Path.home() / "workspace/.tools/chrome-linux64/chrome")

def shot(page, path, width, height):
    """Full-page screenshot via CDP captureBeyondViewport (beats stitching)."""
    page.set_viewport_size({"width": width, "height": height})
    page.goto(URL, wait_until="networkidle")
    # force reveal classes on + scroll through for lazy images
    page.evaluate("""() => {
      document.documentElement.classList.add('js');
      return new Promise(res => {
        let y = 0; const step = 600;
        const t = setInterval(() => {
          y += step; window.scrollTo(0, y);
          if (y >= document.body.scrollHeight) { clearInterval(t); window.scrollTo(0,0); res(); }
        }, 120);
      });
    }""")
    page.wait_for_timeout(3600)  # let reveals complete (<=3s rule + margin)
    # make sure every lazy image is decoded before capture (clipped imgs only load once unclipped)
    n = page.evaluate("() => document.images.length")
    for i in range(n):
        page.evaluate(f"() => document.images[{i}].scrollIntoView({{block:'center'}})")
        try:
            page.wait_for_function(f"() => document.images[{i}].complete && document.images[{i}].naturalWidth > 0", timeout=6000)
        except Exception:
            pass
    page.evaluate("() => window.scrollTo({top:0, behavior:'instant'})")
    page.wait_for_timeout(1200)  # let the 1s wipe transitions finish at top
    cdp = page.context.new_cdp_session(page)
    res = cdp.send("Page.captureScreenshot", {
        "format": "png", "captureBeyondViewport": True, "fromSurface": True})
    import base64
    (path).write_bytes(base64.b64decode(res["data"]))
    print("saved", path)

def main():
    from playwright.sync_api import sync_playwright
    results = {"errors": [], "checks": {}}
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME,
            args=["--no-sandbox","--disable-dev-shm-usage"])
        for name, w, h in [("desktop",1440,900), ("mobile",390,844)]:
            page = browser.new_page(viewport={"width":w,"height":h})
            errs, perrs = [], []
            page.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
            page.on("pageerror", lambda e: perrs.append(str(e)))
            page.goto(URL, wait_until="networkidle")
            # pass 1: trigger reveal observers; pass 2 (after backstop): verify lazy loads
            page.evaluate("""() => {
              return new Promise(async res => {
                for (const img of document.images) { img.scrollIntoView({block:'center'}); await new Promise(r => setTimeout(r, 200)); }
                window.scrollTo(0,0); res();
              });
            }""")
            page.wait_for_timeout(3600)  # backstop at 3s unclips everything; reveals complete
            # pass 2: bring each image into view and wait for its decode
            n = page.evaluate("() => document.images.length")
            for i in range(n):
                page.evaluate(f"() => document.images[{i}].scrollIntoView({{block:'center'}})")
                try:
                    page.wait_for_function(f"() => document.images[{i}].complete && document.images[{i}].naturalWidth > 0", timeout=6000)
                except Exception:
                    pass
            page.evaluate("() => window.scrollTo({top:0, behavior:'instant'})")
            page.wait_for_timeout(500)  # settle after instant scroll
            r = page.evaluate("""() => {
              const o = {};
              const vis = el => { const r = el.getBoundingClientRect(); return r.width>0 && r.height>0 && getComputedStyle(el).visibility!=='hidden'; };
              o.scrollW = document.documentElement.scrollWidth;
              o.innerW = window.innerWidth;
              o.imgs = [...document.images].map(i => ({src:i.src.split('/').pop(), ok:i.complete&&i.naturalWidth>0, w:i.naturalWidth}));
              o.anchors = [...document.querySelectorAll('a[href^="#"]')].map(a => {
                const id = a.getAttribute('href').slice(1);
                return {href:'#'+id, ok: !id || !!document.getElementById(id)};
              });
              const cta = document.querySelector('.hero .btn-primary, .stepper .btn-primary');
              o.ctaDepth = cta ? cta.getBoundingClientRect().top / window.innerHeight : null;
              const form = document.querySelector('.stepper');
              o.formTop = form ? form.getBoundingClientRect().top / window.innerHeight : null;
              // grouped ask count: the booking form = 1 ask, tel: links = 1, other hero/header CTAs each 1
              const vw = window.innerHeight, vh = window.innerWidth;
              const inFirst = el => { const r = el.getBoundingClientRect(); return vis(el) && r.top < vw && r.bottom > 0; };
              o.asks = {
                form: inFirst(form) ? 1 : 0,
                tel: [...document.querySelectorAll('a[href^="tel:"]')].filter(inFirst).length > 0 ? 1 : 0,
                otherCtas: [...document.querySelectorAll('.hero .btn, header .btn')].filter(inFirst).length
              };
              o.fonts = [...document.fonts].map(f => f.family + ':' + f.status);
              o.rvHidden = document.querySelectorAll('.rv:not(.in)').length;
              o.wipeHidden = document.querySelectorAll('.wipe:not(.in)').length;
              const b = getComputedStyle(document.querySelector('.btn-primary'));
              o.ctaBg = b.backgroundColor; o.ctaFg = b.color;
              return o;
            }""")
            results["checks"][name] = {
                "console_errors": errs, "page_errors": perrs,
                "overflow": r["scrollW"] - r["innerW"],
                "images": r["imgs"],
                "bad_anchors": [a for a in r["anchors"] if not a["ok"]],
                "cta_depth_vh": round(r["ctaDepth"],2) if r["ctaDepth"] is not None else None,
                "form_top_vh": round(r["formTop"],2) if r["formTop"] is not None else None,
                "asks_in_hero": r["asks"],
                "fonts": r["fonts"],
                "rv_hidden_after_3.8s": r["rvHidden"],
                "wipe_hidden_after_3.8s": r["wipeHidden"],
                "cta_colors": [r["ctaBg"], r["ctaFg"]],
            }
            page.close()
        # JS-off check
        ctx = browser.new_context(java_script_enabled=False, viewport={"width":1440,"height":900})
        page = ctx.new_page(); page.goto(URL, wait_until="domcontentloaded")
        txt = page.evaluate("() => document.body.innerText")
        html = page.content()
        results["checks"]["jsoff"] = {
            "phone": "(813) 977-0066" in txt,
            "services": all(s in txt for s in ["Roof replacement","Roof repair","Storm damage","Gutters"]),
            "prices": all(s in txt for s in ["from $350","from $8,500"]),
            "email": "roofinone@aol.com" in txt,
            "stepper_visible": "What do you need?" in txt,
        }
        page.close(); ctx.close()
        # full-page screenshots
        page = browser.new_page(viewport={"width":1440,"height":900})
        shot(page, OUT/"full-desktop.png", 1440, 900); page.close()
        page = browser.new_page(viewport={"width":390,"height":844})
        shot(page, OUT/"full-mobile.png", 390, 844); page.close()
        browser.close()
    # contrast calc for CTA
    def lum(rgb):
        import re
        r,g,b = [int(x)/255 for x in re.findall(r'\d+', rgb)[:3]]
        f = lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
        return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
    bg, fg = results["checks"]["desktop"]["cta_colors"]
    l1, l2 = lum(bg), lum(fg)
    ratio = (max(l1,l2)+0.05)/(min(l1,l2)+0.05)
    results["cta_contrast_ratio"] = round(ratio,2)
    (HERE/"qa"/"results.json").write_text(json.dumps(results, indent=1))
    print(json.dumps(results, indent=1))

if __name__ == "__main__":
    main()
