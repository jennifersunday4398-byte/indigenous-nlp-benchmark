"""
Gbagyi Corpus Scraper - CSC 406 Group 05
=========================================

Scrapes the Gbagyi New Testament (Alkawali Woiwoyi, GAW, version 1621)
from bible.com and writes raw_data_group_05.jsonl.

Source: Biblica, Inc. Gbagyi New Testament (GAW), hosted on YouVersion.
URL pattern: https://www.bible.com/bible/1621/<BOOK>.<CHAPTER>.GAW

Output schema (validated against tests/autograder_eval.py):
    {"id": 1, "url": "...", "date_retrieved": "YYYY-MM-DD", "raw_text": "..."}

NOTE: 'id' MUST be an integer. The autograder asserts isinstance(entry['id'], int).

Usage:
    python scraper.py                  # full run, all 260 chapters
    python scraper.py --limit 10       # quick test on 10 chapters first
"""

import argparse
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

VERSION_ID = 1621
VERSION_CODE = "GAW"
BASE_URL = "https://www.bible.com/bible/{vid}/{book}.{chapter}.{code}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# New Testament book codes and chapter counts (YouVersion USFM codes)
NT_BOOKS = [
    ("MAT", 28), ("MRK", 16), ("LUK", 24), ("JHN", 21), ("ACT", 28),
    ("ROM", 16), ("1CO", 16), ("2CO", 13), ("GAL", 6), ("EPH", 6),
    ("PHP", 4), ("COL", 4), ("1TH", 5), ("2TH", 3), ("1TI", 6),
    ("2TI", 4), ("TIT", 3), ("PHM", 1), ("HEB", 13), ("JAS", 5),
    ("1PE", 5), ("2PE", 3), ("1JN", 5), ("2JN", 1), ("3JN", 1),
    ("JUD", 1), ("REV", 22),
]

# Chrome/UI strings that appear on the page but are not scripture
NOISE_MARKERS = (
    "Currently Selected", "YouVersion", "Bible App", "Copyright",
    "All rights reserved", "Learn More About", "Popular Bible Verses",
    "READER SETTINGS", "Next Chapter", "Previous Chapter", "Highlight",
    "Compare", "Share", "Sign up or sign in", "Get the app",
)


def build_chapter_urls(limit=None):
    """Return the list of chapter URLs to scrape."""
    urls = []
    for book, n_chapters in NT_BOOKS:
        for ch in range(1, n_chapters + 1):
            urls.append(BASE_URL.format(
                vid=VERSION_ID, book=book, chapter=ch, code=VERSION_CODE
            ))
    return urls[:limit] if limit else urls


def extract_verses_from_html(html):
    """
    Pull verse text out of a bible.com chapter page.

    Three strategies are attempted in order, because bible.com changes its
    CSS class hashes periodically and a single selector is brittle:
      1. CSS classes containing 'ChapterContent_verse'  (current markup)
      2. data-usfm attributes                            (older markup)
      3. Paragraph-level fallback with noise filtering    (last resort)

    Returns a list of verse strings.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Strategy 1: verse spans by class fragment
    verses = []
    for node in soup.find_all(
        attrs={"class": lambda c: c and "ChapterContent_verse" in " ".join(
            c if isinstance(c, list) else [c])}
    ):
        # Inside each verse, 'content' spans hold the actual words.
        # 'label' spans hold the verse number, which we do not want.
        content_spans = node.find_all(
            attrs={"class": lambda c: c and "ChapterContent_content" in " ".join(
                c if isinstance(c, list) else [c])}
        )
        if content_spans:
            text = " ".join(s.get_text(" ", strip=True) for s in content_spans)
        else:
            text = node.get_text(" ", strip=True)
        text = text.strip()
        if text:
            verses.append(text)

    if verses:
        return verses

    # Strategy 2: data-usfm attributes
    for node in soup.find_all(attrs={"data-usfm": True}):
        text = node.get_text(" ", strip=True)
        if text:
            verses.append(text)

    if verses:
        return verses

    # Strategy 3: fallback, take paragraph-ish blocks and filter UI noise
    for node in soup.find_all(["p", "div", "span"]):
        text = node.get_text(" ", strip=True)
        if len(text) < 25:
            continue
        if any(marker in text for marker in NOISE_MARKERS):
            continue
        if text not in verses:
            verses.append(text)

    return verses


def clean_verse(text):
    """Strip leading verse numbers, footnote markers and collapse whitespace."""
    # Leading verse number, e.g. "1Yesu Kristi..." or "23 Wo!"
    text = re.sub(r"^\s*\d+\s*", "", text)
    # Inline verse numbers glued to a following capital letter
    text = re.sub(r"(?<=[\.\?\!])\s*\d+(?=[A-ZƁ])", " ", text)
    # Footnote / cross-reference superscripts
    text = re.sub(r"[#\*]+", " ", text)
    # Collapse all whitespace
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def scrape_to_jsonl(url_list, output_path, delay=1.5, verbose=True):
    """
    Scrape text from a list of URLs and write JSON Lines.

    Args:
        url_list (list[str]): chapter URLs
        output_path (str): destination .jsonl path
        delay (float): seconds to wait between requests
        verbose (bool): print progress

    Returns:
        int: number of successfully written entries
    """
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    entry_id = 0
    failures = []

    with open(out, "w", encoding="utf-8") as f:
        for i, url in enumerate(url_list, 1):
            try:
                resp = requests.get(url, headers=HEADERS, timeout=25)
                resp.raise_for_status()
                resp.encoding = "utf-8"

                verses = extract_verses_from_html(resp.text)
                verses = [clean_verse(v) for v in verses]
                verses = [v for v in verses if len(v) > 10]

                if not verses:
                    failures.append((url, "no verses parsed"))
                    if verbose:
                        print(f"  [{i}/{len(url_list)}] EMPTY  {url}")
                    continue

                raw_text = " ".join(verses)
                entry_id += 1
                record = {
                    "id": entry_id,               # MUST be int
                    "url": url,
                    "date_retrieved": today,
                    "raw_text": raw_text,
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

                if verbose and i % 10 == 0:
                    print(f"  [{i}/{len(url_list)}] ok, {entry_id} entries so far")

            except requests.exceptions.RequestException as e:
                failures.append((url, str(e)))
                if verbose:
                    print(f"  [{i}/{len(url_list)}] FAIL   {url}  ({e})")
            except Exception as e:
                failures.append((url, f"unexpected: {e}"))
                if verbose:
                    print(f"  [{i}/{len(url_list)}] ERROR  {url}  ({e})")

            time.sleep(delay)

    if verbose:
        print(f"\nDone. {entry_id} entries written to {out}")
        print(f"Failures: {len(failures)}")
        for url, reason in failures[:10]:
            print(f"   {url} -> {reason}")

    return entry_id


def main():
    parser = argparse.ArgumentParser(description="Scrape Gbagyi NT to JSONL")
    parser.add_argument("--limit", type=int, default=None,
                        help="only scrape the first N chapters (use for testing)")
    parser.add_argument("--delay", type=float, default=1.5,
                        help="seconds between requests")
    parser.add_argument("--out", type=str,
                        default="data/gbagyi/raw/raw_data_group_05.jsonl")
    args = parser.parse_args()

    urls = build_chapter_urls(args.limit)
    print(f"Scraping {len(urls)} chapters from bible.com (GAW / Gbagyi NT)")
    print(f"Output: {args.out}\n")

    count = scrape_to_jsonl(urls, args.out, delay=args.delay)

    if count == 0:
        print("\nNOTHING WAS SCRAPED. The page markup may have changed.")
        print("Run a single URL manually to inspect:")
        print("  python -c \"import requests;print(requests.get("
              "'https://www.bible.com/bible/1621/MAT.1.GAW').text[:3000])\"")
        sys.exit(1)


if __name__ == "__main__":
    main()
