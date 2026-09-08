#!/usr/bin/env python3
"""Check the docs site has no dead internal links.

A broken anchor on a docs page is invisible until someone clicks it, and there
is no build step here to catch it. This is the build step.

Run: python3 scripts/test_docs_links.py
"""

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

pages = {p.name: p.read_text() for p in DOCS.glob("*.html")}
problems = []

for name, text in sorted(pages.items()):
    ids = set(re.findall(r'\bid="([^"]+)"', text))

    for href in re.findall(r'href="([^"]+)"', text):
        if href.startswith(("http://", "https://", "mailto:")):
            continue

        target, _, fragment = href.partition("#")

        # "" is this page. "./" is the directory index, which is a different
        # page unless you happen to be on it.
        if target == "":
            page, page_ids = name, ids
        elif target == "./":
            page, page_ids = "index.html", set(
                re.findall(r'\bid="([^"]+)"', pages["index.html"]))
        else:
            if target not in pages:
                if not (DOCS / target).exists():
                    problems.append("{}: link to missing {}".format(name, target))
                continue
            page, page_ids = target, set(re.findall(r'\bid="([^"]+)"', pages[target]))

        if fragment and fragment not in page_ids:
            problems.append("{}: #{} does not exist in {}".format(name, fragment, page))

    for src in re.findall(r'(?:src|href)="((?:css|js)/[^"]+)"', text):
        if not (DOCS / src).exists():
            problems.append("{}: missing asset {}".format(name, src))

if problems:
    print("{} problem(s):".format(len(problems)))
    for problem in problems:
        print("  - {}".format(problem))
    sys.exit(1)

print("{} page(s), every internal link and anchor resolves: {}".format(
    len(pages), ", ".join(sorted(pages))))
