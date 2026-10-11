# Carl Martin Roofing — demo site (LOCAL ONLY)

Cold-pitch demo for **Carl Martin Roofing, LLC** · Roofing · Tampa, FL · (813) 977-0066 · roofinone@aol.com.
Real facts taken from carlmartinroofing.com (2026-10-10): family owned since 1972; re-roofing, maintenance, repair and roof-system installation across Tampa Bay; serves apartment complexes, HOAs, residential, commercial and public works; "we maintain our client's roofs year round"; phone (813) 977-0066; BBB badge; real testimonials from **Sabrina Piepenbring** and **John Mezzei** (their site names "Mike Martin" as the estimator). **Not deployed, not approved, never emailed.**

## Concept: "THE LEDGER"
The company's 54-year record rendered as a working job ledger. Every section opens as a ledger entry ("LEDGER ENTRY · 2026-10-07", "LEDGER NOTE · 01"); the live job in Seminole Heights is the ledger's latest line; the four-generation family timeline (1972→2026) is the page's spine and signature. The roof is sold as an **inspection, booked not dialled** — the hero's primary path is a 4-step inspection-booking stepper (service → ZIP → home size → callback time) with progress bar + per-field checkmarks; phone is secondary, direct `tel:` everywhere, no modal before dial.

## Art-direction triple
**heritage / plainspoken / steady** — judged every choice against it:
- *heritage*: ledger paper ground (#f6f1e6), ledger-cloth green (#1e4d33), Rokkitt slab display, the 1972→2026 numerals as hero architecture, mono entry numbers, then/now truck photos.
- *plainspoken*: 5th-grade headlines, read-aloud tested; prices printed on cards; FAQ answers with real ranges.
- *steady*: calm Mercury register on money moments (financing card, final CTA); one copper accent used ONLY on primary CTAs; 1px borders, zero shadows; film grain on the dark stat band.

## Broken convention
**No hero photograph.** The hero architecture is full-bleed ledger numerals ("1972 → 2026") behind the copy, and the one dominant visual is the live 4-step inspection stepper — not a photo, not a collage. (Siblings all lead with photography.)

## Signature elements
1. **The family ledger timeline** — 1972 (vintage truck photo, hand-painted lettering) → 1980s → 2004 (the four-hurricane season; ring-shank nails become the house standard) → 2026 (modern truck, "Mike runs the crews"). Ruled like a ledger, with an honesty note that the middle entries are illustrative.
2. **"This week in Seminole Heights"** — the live-job slot framed as the ledger's latest dated line: day-by-day frames (Oct 5–8), in-progress tear-off photo with hand-drawn marker annotation on the exposed decking, mono date-stamped caption.

## Motif
One motif: the **ledger double-rule with mono entry number** — every section eyebrow, the timeline's top rule, list bullets (◆), sticky call-bar icon treatment, and the favicon's ground. (Favicon glyph itself is a copper shingle mark on ledger green, per the standing favicon rule.) One decorative motif total.

## Distinctness vs the named siblings
- **cardinal-roofing** ("THE SHELL"): annotated roof cross-section + clickable layer explorer, HUD spec chips, cardinal-red accent, Barlow Condensed. Ours has no diagram, no HUD chips, no red — the system is the ledger, the accent is copper, the display face is a slab serif.
- **all-area-roofing** ("Built for Florida Storms"): full-bleed "STORM DAMAGE?" type over a storm-sky photo, safety-orange, Oswald, ZIP cost estimator. Ours has no hero photo, no giant pain word, no estimator — the conversion path is the stepper, the enemy is not storm chasers.
- **jrjb-roofing**: charcoal/terracotta. Ours is ledger green + paper + copper.
- Named enemy here is **"the disappearing warranty"** (the 10-year-warranty company that folds in three) — deliberately not storm chasers, which cardinal + all-area already used.

## Insider-ritual headline
"We walk the roof before we quote it. No satellite guesses." + the craft paragraph: six nails per shingle, ring-shank decking nails, peel-and-stick secondary water barrier — the 2004 standard, on every tear-off.

## Fonts (self-hosted, no runtime hotlinking)
Rokkitt variable (display + body, 100–900 axis in one woff2) + IBM Plex Mono 400/500 (utility: phones, prices, license, dates, chips) — latin woff2 in `fonts/`. Two families total.

## Images
6 original AI-generated WebP photos in `images/`: truck-1972, truck-2026, tearoff-progress (live job), before-damage, after-newroof, tech-portrait (Mike). `og-image.jpg` 1200×630 cropped from the hero. Full OG + Twitter Card tags with absolute URLs on the planned alias `https://carl-martin-roofing-demo-iodine-53s-projects.vercel.app/` (NOT deployed).

## Trade-literacy audit (all 6 photos inspected)
- truck-1972: PASS — 70s Ford, wooden ladder racks, hand-painted door lettering, Tampa ranch home.
- truck-2026: **FAIL → fixed** — first generation printed a wrong "561-478-9320" on the door (561 = Palm Beach, not Tampa). Edit attempt didn't take; regenerated fresh with "no phone number on the vehicle". Re-verified clean.
- tearoff-progress: PASS — tear-off shovels, staged GAF Timberline HDZ bundles, dump trailer, gloves, Spanish moss/oaks = Tampa.
- before-damage: PASS — curled tabs, exposed felt, cracked vent pipe boot, granule loss.
- after-newroof: PASS — straight courses, fitted ridge caps, fascia, new gutters.
- tech-portrait: PASS — "MIKE" name patch, plausible tool belt (hammer, pliers, tape, utility knives), ladder at eave.

## QA result (headless Chromium, 2026-10-10, `qa/qa.py`)
- Desktop 1440 + mobile 390: **zero console errors, zero page errors, zero horizontal overflow**, all 6 images load, all anchors resolve.
- Fonts load over HTTP (Rokkitt, IBM Plex Mono); CTA contrast **6.01:1** (white on #9e4c12).
- Animations: blur-to-sharp headlines + clip-wipe photos all complete with **no interaction in ≤3s** (3s backstop); `prefers-reduced-motion` disables them.
- JS-off: phone, all 4 services, from-prices, email, and the full stepper render in server HTML.
- Asks before first click: **2** (booking form + phone link) on both widths.
- CTA scroll depth: desktop 0.6vh; mobile form starts 0.81vh (Continue at 1.15vh — chip-tap auto-advance means step 1 rarely needs it).
- Stepper verified end-to-end: chip tap auto-advances (step 1→2, progress 50%, dot 1 ✓), ZIP validation nudges on bad input, final step composes the `mailto:roofinone@aol.com` handoff (navigation to mailto: attempted — verified).
- Callbar: hidden at top, slides up past hero, **hides over the booking form** (never covers the number/form) and at the final CTA. FAQ accordion, mobile nav, live Tampa clock + open chip all verified.
- Fixed before sign-off: (1) truck-2026 wrong phone (see audit); (2) `[hidden]` overridden by `.btn{display:inline-flex}` — Back button leaked onto step 1 → added `[hidden]{display:none!important}`; (3) mobile header overflow 35px from the loud header button → demoted to a quiet text link + 48px phone icon on mobile (one-loud-CTA-per-zone); (4) callbar covered the booking form → hides when #booking is in view; (5) wipe-reveal × lazy-load race left images blank (clipped images report intersection 0, so lazy never fired) → reveal observers now fire 25% before viewport; (6) hero numerals collided with the trust line → resized to 14vw inside the hero padding; (7) marker ellipse misplaced on the before photo → repositioned over the cracked vent boot; (8) mobile timeline 2-col scramble → single column; (9) no CTA between reviews and FAQ (friend-test Q5 exit point) → added "Join them — book the free inspection".

## Substitute QA (claude.ai critique parked — recorded 2026-10-10)
**Five-question friend test** (answered cold):
1. "I don't understand what I'm actually buying" — PASS: free inspection booking, named in the offer eyebrow + sub in the first viewport.
2. "Where is the price" — PASS: hero price line + from-prices on every card + repair-vs-replace matrix.
3. "This feels longer than it needs to be" — PASS with note: considered purchase ($8.5–15k) earns the full objection stack; every section answers one objection, nothing is filler; the one CTA-less stretch got a CTA added.
4. "Why should I trust this" — PASS: 54-year timeline, named enemy, real reviews from their own site, license line, meet-your-tech, receipt-style reviews; placeholder stats flagged on-page.
5. "I almost closed the tab here" — the reviews→FAQ stretch (no CTA) was the exit point → fixed with the "Join them" CTA; mobile callbar keeps Call + Book one tap away everywhere else.
**Blur pass** (hero, Gaussian 14): first fixation = H1 mass, second = the copper Continue button. Path clean — PASS.
**Read-aloud test**: all 13 headlines read clean at speaking pace, 5th-grade level — "Be the house that's ready for storm season." / "Beware the disappearing warranty." / "We walk the roof before we quote it. No satellite guesses." / "You'll know the crew lead before he knocks." / "This is what 'we'll get to it' becomes." / "Storm season comes every year. This year, be ready." — PASS, no rewrites.
**Redesign subtraction audit** (functional inventory: phone, form, services path, trust line, prices, email): all present — nothing subtracted for style. The header's loud button was demoted (not deleted) per the one-loud-CTA rule. PASS.

## Needs real data before a client could use it
- FL license number — `#CCC0000000` is a placeholder everywhere (footer, service-areas section).
- ★4.8 / 600+ reviews / 10-year workmanship warranty / stat-band figures — plausible, **unverified**; flagged on-page next to the stats.
- Testimonials: **John M. and Sabrina P. are real** (from carlmartinroofing.com); Tara W. and Luis G. are illustrative (one 4★ for believability) — flagged on-page.
- Timeline: 1972 founding, the 2004 hurricane season, and Mike Martin are real; the 1980s entry is illustrative — flagged on-page.
- Prices ($8,500–$15,000 replacement, $350–$900 repairs, $89/mo financing) are honest 2026 Tampa ranges from research, not their sheet.
- The tech portrait is an illustrative AI photo; "Mike Martin" the name is real (their testimonial).
- Forms compose a `mailto:` handoff — production needs a real form endpoint.

## Files
`index.html`, `styles.css`, `app.js`, `favicon.svg`, `og-image.jpg`, `images/`, `fonts/`, `qa/` (qa.py + results.json + screenshots).

**Local only.** Never deploy, never send.
