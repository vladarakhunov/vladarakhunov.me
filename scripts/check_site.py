#!/usr/bin/env python3
"""Pre-publish checks for vladarakhunov.me. Standard library only.

Run before pushing:  python3 scripts/check_site.py
Exits non-zero if anything would ship broken.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "vladarakhunov.me"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SVG_SELF = {"path", "circle", "rect", "line", "polyline", "polygon", "ellipse", "use", "stop"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.links = [], [], set(), []
        self.has = {"title": False, "viewport": False, "description": False, "lang": False}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html" and a.get("lang"):
            self.has["lang"] = True
        if tag == "title":
            self.has["title"] = True
        if tag == "meta" and a.get("name") == "viewport":
            self.has["viewport"] = True
        if tag == "meta" and a.get("name") == "description" and a.get("content"):
            self.has["description"] = True
        if "id" in a:
            if a["id"] in self.ids:
                self.errors.append(f"duplicate id '{a['id']}'")
            self.ids.add(a["id"])
        if tag == "img" and not (a.get("alt") or "").strip():
            self.errors.append(f"<img src='{a.get('src')}'> is missing alt text")
        for attr in ("href", "src"):
            if attr in a and tag not in ("textpath",):
                self.links.append((tag, a[attr]))
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack or self.stack[-1][0] != tag:
            opened = self.stack[-1] if self.stack else ("nothing", 0)
            self.errors.append(f"line {self.getpos()[0]}: </{tag}> closes <{opened[0]}> opened on line {opened[1]}")
            return
        self.stack.pop()


def check_page(path: Path) -> list[str]:
    p = Page()
    p.feed(path.read_text(encoding="utf-8"))
    errs = list(p.errors)
    errs += [f"<{t}> opened on line {ln} is never closed" for t, ln in p.stack]
    errs += [f"missing {k}" for k, ok in p.has.items() if not ok]
    for tag, url in p.links:
        if re.match(r"^(https?:|mailto:|tel:|data:)", url):
            continue
        if url.startswith("#"):
            if url != "#" and url[1:] not in p.ids and tag == "a":
                errs.append(f"link to {url} but no element has that id")
            continue
        target = (ROOT / url.lstrip("/").split("#")[0].split("?")[0]) if url.startswith("/") else (path.parent / url.split("#")[0])
        if target.is_dir():
            target = target / "index.html"
        if not target.exists():
            errs.append(f"{tag} points to '{url}', which isn't in the repo")
    return errs


def main() -> int:
    problems = []
    pages = sorted(ROOT.glob("*.html"))
    for page in pages:
        problems += [f"{page.name}: {e}" for e in check_page(page)]
    cname = (ROOT / "CNAME").read_text().strip() if (ROOT / "CNAME").exists() else ""
    if cname != DOMAIN:
        problems.append(f"CNAME should contain '{DOMAIN}' (found '{cname}') or the custom domain breaks")
    sitemap = (ROOT / "sitemap.xml").read_text() if (ROOT / "sitemap.xml").exists() else ""
    for loc in re.findall(r"<loc>https://" + re.escape(DOMAIN) + r"/([^<]*)</loc>", sitemap):
        if not (ROOT / (loc or "index.html")).exists():
            problems.append(f"sitemap.xml lists '/{loc}', which doesn't exist")
    if problems:
        print("✗ Site checks failed:\n  - " + "\n  - ".join(problems))
        return 1
    print(f"✓ {len(pages)} pages checked: HTML structure, alt text, internal links, metadata, CNAME, sitemap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
