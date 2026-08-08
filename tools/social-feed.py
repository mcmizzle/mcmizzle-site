#!/usr/bin/env python3
"""Generate blog/social.xml — the LinkedIn copy, as a feed a scheduler can read.

Usage:
    python3 tools/social-feed.py

Standard library only, so this runs anywhere including the agents' sandbox.

## Why this exists

Pointing a scheduler at the ordinary blog feed gets you a queued post
containing the title and a link, which is exactly the botlike output that
`AUTOMATION.md` argues against. This feed carries the hand-written LinkedIn
copy from `SOCIAL.md` in each item's `<description>`, so the thing waiting in
the queue is the copy that was actually reviewed.

The queue is the second approval gate. Nothing here posts anything: it
publishes text a scheduler can pick up, and a human still taps approve.

## Parsing contract

`SOCIAL.md` is the source of truth and this reader is deliberately strict, so
that a malformed section fails loudly rather than publishing something odd:

    ## <post title>
    `<post url>`
    ### LinkedIn
    ```
    <copy>
    ```

Every post section needs the URL on its own line in backticks, and a
`### LinkedIn` block. Forum-reply blocks are ignored — those get posted by
hand into a specific thread and make no sense in a scheduler.

## Dates

Each item's `pubDate` is the post's real publication date, read out of
`blog/feed.xml` and matched on URL. It must not be "when this file was last
generated": every new post rewrites `SOCIAL.md`, and if that re-dated every
item, a consumer that decides what is new by date would re-queue the entire
back catalogue. Zapier dedupes on `<guid>` and would probably survive that,
but "probably" is a poor guarantee when the failure mode is a queue full of
duplicate posts to someone's professional network.

## Already-posted items

Nothing is removed once published. Schedulers dedupe on `<guid>`, which is
the post URL and therefore stable, so an item is queued once no matter how
long it stays in the feed. Deleting old items would risk re-queueing them if
a scheduler ever reset its state.
"""

import pathlib
import re
import sys
import xml.dom.minidom as minidom

BASE = "https://mcmizzle.com"
ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "blog" / "SOCIAL.md"
OUT = ROOT / "blog" / "social.xml"


def blog_pubdates():
    """{post url: RFC-822 pubDate} from blog/feed.xml.

    The blog feed is the authority on when a post was published, so the two
    feeds can never disagree about a date.
    """
    feed = ROOT / "blog" / "feed.xml"
    if not feed.exists():
        return {}
    dom = minidom.parse(str(feed))
    dates = {}
    for item in dom.getElementsByTagName("item"):
        try:
            link = item.getElementsByTagName("link")[0].firstChild.data.strip()
            pub = item.getElementsByTagName("pubDate")[0].firstChild.data.strip()
        except (IndexError, AttributeError):
            continue
        dates[link.rstrip("/") + "/"] = pub
    return dates


def parse(md):
    """Yield (title, url, copy) per post section that has LinkedIn copy."""
    # Split on level-2 headings, keeping the heading text.
    sections = re.split(r"^## (.+)$", md, flags=re.M)[1:]
    for title, body in zip(sections[0::2], sections[1::2]):
        url_match = re.search(r"^`(https://[^`]+)`\s*$", body, flags=re.M)
        if not url_match:
            continue

        # The fenced block under "### LinkedIn", up to the next heading.
        li = re.search(
            r"^### LinkedIn\s*\n(.*?)(?=^## |\Z)", body, flags=re.M | re.S
        )
        if not li:
            continue
        block = re.search(r"^```\n(.*?)^```", li.group(1), flags=re.M | re.S)
        if not block:
            sys.exit(f"'{title}' has a ### LinkedIn heading but no fenced block")

        copy = block.group(1).strip()
        if not copy:
            sys.exit(f"'{title}' has an empty LinkedIn block")
        yield title.strip(), url_match.group(1).strip(), copy


def main():
    if not SOURCE.exists():
        sys.exit(f"{SOURCE} not found")

    items = list(parse(SOURCE.read_text()))
    if not items:
        sys.exit("no LinkedIn copy found in SOCIAL.md — refusing to write an empty feed")

    dates = blog_pubdates()
    missing = [u for _, u, _ in items if u.rstrip("/") + "/" not in dates]
    if missing:
        sys.exit(
            "no pubDate in blog/feed.xml for:\n  "
            + "\n  ".join(missing)
            + "\nAdd the post's feed item first — the two feeds must agree on dates."
        )

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
        'xmlns:content="http://purl.org/rss/1.0/modules/content/">',
        "  <channel>",
        "    <title>McMizzle — social copy</title>",
        f"    <link>{BASE}/blog/</link>",
        "    <description>Hand-written LinkedIn copy for each post, for a "
        "scheduler to queue. Generated from blog/SOCIAL.md; not intended for "
        "human readers.</description>",
        "    <language>en-us</language>",
        f'    <atom:link href="{BASE}/blog/social.xml" rel="self" '
        'type="application/rss+xml"/>',
    ]

    for title, url, copy in items:
        lines += [
            "    <item>",
            f"      <title><![CDATA[{title}]]></title>",
            f"      <link>{url}</link>",
            f'      <guid isPermaLink="true">{url}</guid>',
            f'      <pubDate>{dates[url.rstrip("/") + "/"]}</pubDate>',
            # The copy lives in both fields because schedulers disagree about
            # which one they read. CDATA keeps the paragraph breaks intact —
            # LinkedIn honours them and the copy is written expecting them.
            f"      <description><![CDATA[{copy}]]></description>",
            f"      <content:encoded><![CDATA[{copy}]]></content:encoded>",
            "    </item>",
        ]

    lines += ["  </channel>", "</rss>"]
    OUT.write_text("\n".join(lines) + "\n")

    print(f"wrote {OUT.relative_to(ROOT)} — {len(items)} item(s)")
    for title, url, copy in items:
        words = len(copy.split())
        print(f"  {dates[url.rstrip('/') + '/'][:16]}  {words:4d} words  {title[:44]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
