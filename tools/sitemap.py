#!/usr/bin/env python3
"""Regenerate sitemap.xml from what's actually on disk.

Usage:
    python3 tools/sitemap.py

Standard library only, no venv needed — unlike og-image.py, this one runs
anywhere, including the cloud agents' sandbox.

Every directory containing an index.html becomes a URL, plus the site root.
404.html is excluded: a sitemap is a list of pages you want indexed, and the
error page is not one of them.

`lastmod` comes from git — the file's last commit date — rather than the
filesystem, so a fresh clone doesn't claim every page changed today.
"""

import pathlib
import subprocess
import sys

BASE = "https://mcmizzle.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent

# Rough priority: the front page, then app pages, then posts, then the rest.
# Search engines largely ignore this, but it costs nothing and documents intent.
PRIORITY = {"": "1.0", "blog": "0.9"}
DEFAULT_PRIORITY = "0.8"
POST_PRIORITY = "0.7"


def last_commit_date(path):
    """YYYY-MM-DD of the file's last commit, or None if git doesn't know it."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def main():
    pages = []
    for index in sorted(ROOT.rglob("index.html")):
        if ".git" in index.parts:
            continue
        rel = index.parent.relative_to(ROOT)
        slug = "" if str(rel) == "." else f"{rel}/"
        top = str(rel).split("/")[0] if slug else ""

        if top == "blog" and slug != "blog/":
            priority = POST_PRIORITY
        else:
            priority = PRIORITY.get(top, DEFAULT_PRIORITY)

        pages.append((f"{BASE}/{slug}", last_commit_date(index), priority))

    # Front page first, then everything else alphabetically — purely for a
    # readable diff when this file changes.
    pages.sort(key=lambda p: (p[0] != f"{BASE}/", p[0]))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, priority in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    out = ROOT / "sitemap.xml"
    out.write_text("\n".join(lines) + "\n")
    print(f"wrote sitemap.xml — {len(pages)} URLs")
    for loc, lastmod, _ in pages:
        print(f"  {lastmod or '(no git date)'}  {loc}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
