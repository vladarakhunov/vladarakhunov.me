# vladarakhunov.me

Personal site of **Vlada Rakhunov** — Digital Product & Business Executive.
Designed and built with [Claude](https://claude.ai). Hosted on GitHub Pages.

**Live:** https://vladarakhunov.me · **What's new:** [changelog](https://vladarakhunov.me/changelog.html)

## What's here

| Path | What it is |
|---|---|
| `index.html` | The site — a single page |
| `changelog.html` | One-line notes on every change |
| `images/` | Optimized photos |
| `CNAME` | Custom domain for GitHub Pages |
| `scripts/check_site.py` | Pre-publish checks |
| `.github/workflows/site-checks.yml` | Runs those checks on GitHub after every push |
| `CLAUDE.md` | House rules: workflow, content, design |

No build step and no dependencies — what's in the repo is what's served.

## Preview locally

```sh
python3 -m http.server 8000
# open http://localhost:8000
```

## Before publishing

```sh
python3 scripts/check_site.py
```

Checks HTML structure, image alt text, internal links, page metadata, the `CNAME` file and the sitemap.

## Deploy

Push to `main`. GitHub Pages publishes in about a minute. The domain's DNS (Squarespace) points four `A` records to GitHub Pages and `www` to `vladarakhunov.github.io`.
