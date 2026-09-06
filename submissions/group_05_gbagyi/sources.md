# Data Provenance - Group 05 Gbagyi

## Primary source

| Field | Value |
|---|---|
| Publication | Alkawali Woiwoyi (Gbagyi New Testament) |
| Version code | GAW |
| YouVersion version id | 1621 |
| Publisher | Biblica, Inc. |
| Copyright | Copyright 1997 by Biblica, Inc. All rights reserved worldwide. |
| Host | YouVersion / Bible.com |
| Landing page | https://www.bible.com/versions/1621-gaw-alkawali-woiwoyi |
| Language page | https://www.bible.com/languages/gbr |
| URL pattern | https://www.bible.com/bible/1621/<BOOK>.<CHAPTER>.GAW |
| Chapters retrieved | 260 (full New Testament, 0 failures) |
| Collection date | 31 August 2026|
| Method | Python requests + BeautifulSoup |
| Crawl delay | 1.5 seconds between requests |
| robots.txt reviewed | Yes |
| Total characters retrieved | 1,785,064 |
## Book codes retrieved

MAT (28), MRK (16), LUK (24), JHN (21), ACT (28), ROM (16), 1CO (16),
2CO (13), GAL (6), EPH (6), PHP (4), COL (4), 1TH (5), 2TH (3), 1TI (6),
2TI (4), TIT (3), PHM (1), HEB (13), JAS (5), 1PE (5), 2PE (3), 1JN (5),
2JN (1), 3JN (1), JUD (1), REV (22)

## Secondary source identified (not used in the primary crawl)

| Field | Value |
|---|---|
| Publication | Gbagyi Nyizeyenya Baibwulu: Shekwoyi Ɓədagbma |
| Version code | GNB |
| YouVersion version id | 4607 |
| Publisher | Biblica, Inc. (Gbagyi Contemporary Bible, 2025) |

Note the orthographic difference between the two editions: GAW writes
`Shekwoyi` while the instructor's test file uses `shekwoi`. GNB additionally
uses the schwa character `ə`. This orthographic variation across editions of
the same language is discussed in the Zipf synthesis section of the report.

## Compliance statement

No pre-existing dataset from Hugging Face, Kaggle or any published paper was
used. All text was retrieved directly by the Python scraper included in
`HW1_assignment.ipynb`.

Scraper source code is included at submissions/group_05_gbagyi/scraper.py
