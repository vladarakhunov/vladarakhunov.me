# House rules for vladarakhunov.me

Vlada Rakhunov's executive personal site. Static HTML on GitHub Pages, custom domain `vladarakhunov.me`. Built with Claude.

## How we work (one-person team)
1. **Ask before changing anything.** Reply with a one-line plan; wait for a "go" before editing or pushing.
2. Push small, finished changes straight to `main`. Use a branch + PR only for big redesigns.
3. Run `python3 scripts/check_site.py` before every push. It must pass. The same check runs on GitHub after each push.
4. **Every visible change gets a changelog line** in `changelog.html`: one sentence, a fun emoji bullet, newest first, under that day's date heading.
5. Confirm back what changed in a few lines — no step-by-step recap.

## Commits
- Author as Vlada: `Vlada Rakhunov <356782017+vladarakhunov@users.noreply.github.com>` (keeps her personal email private).
- End every message with a `Co-Authored-By: Claude …` trailer so GitHub shows "Vlada and Claude".
- Subject line in plain English describing the outcome, not the mechanics.

## Content rules
- Never invent titles, dates, metrics, testimonials or client details. Unconfirmed facts stay as `[verify]` placeholders.
- The Diageo / The Bar figures are **draft** until Vlada approves them; keep the "DRAFT" badge until then.
- Voice: warm, confident, human. Hiring readers first: who she is → where she helps → evidence.

## Design (Tartan Heritage)
- Colors: ground `#F3EEE3`, ink `#1A2238`, navy `#1F2D4F`, gold `#C9A24A`, section tints `#E3E8DF` / `#E7EBF3` / `#F3E8CC`.
- Type: Playfair Display (headings), Libre Franklin (body and spaced small caps).
- Tartan pattern is pure CSS (`repeating-linear-gradient`); no image files for it.
- No motion on the page. Keep text contrast at 4.5:1 or better; every image needs alt text.

## Files
- `index.html` — the whole site (single page, inline styles).
- `changelog.html` — what's new.
- `images/` — optimized photos (resize to ≤ 640 px, JPEG quality ~85).
- `CNAME` — must contain exactly `vladarakhunov.me`.
- `scripts/check_site.py` — pre-publish checks (no dependencies).
- `.nojekyll` — serve files as-is, skip Jekyll.
