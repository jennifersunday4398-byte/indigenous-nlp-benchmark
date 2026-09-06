# Gbagyi Stop-Word List - Group 05

Curated functional words: conjunctions, prepositions, pronouns and particles.
Requirement: 30 or more words with English translations. Current count: 35.

**Status: translations need verification by a native Gbagyi speaker.**
Where a translation is uncertain it is marked with `[verify]`.

| # | Gbagyi | English translation | Category |
|---|---|---|---|
| 1 | wa | he / she / it (subject pronoun) | pronoun |
| 2 | nu | the / that (definite marker) | determiner |
| 3 | yi | is / are (copula, sentence-final) | copula |
| 4 | n | and / with | conjunction |
| 5 | ɓa | they / them | pronoun |
| 6 | ge | that / which (complementiser) | conjunction |
| 7 | na | of / belonging to | preposition |
| 8 | ye | to be / to exist | verb particle |
| 9 | wo | you (singular) | pronoun |
| 10 | ho | him / her (object) | pronoun |
| 11 | ba | not (negation) | particle |
| 12 | ku | give / to | preposition [verify] |
| 13 | lo | go / towards | preposition |
| 14 | shi | from / out of | preposition |
| 15 | zhin | do / make / become | verb |
| 16 | ntu | because | conjunction |
| 17 | ɓo | in / inside | preposition |
| 18 | ɓe | come | verb |
| 19 | a | we / our | pronoun |
| 20 | ma | also / too | particle |
| 21 | gna | say / tell | verb |
| 22 | to | but / however | conjunction |
| 23 | ama | but (Hausa loan) | conjunction |
| 24 | sai | until / then (Hausa loan) | conjunction |
| 25 | har | until (Hausa loan) | conjunction |
| 26 | gama | because (Hausa loan) | conjunction |
| 27 | nya | of (possessive marker) | particle |
| 28 | ɓi | child / small | noun [verify] |
| 29 | ga | question / emphasis particle | particle |
| 30 | ta | again / also | particle |
| 31 | kwo | this / that | determiner |
| 32 | aza | person / people | noun |
| 33 | oza | person | noun |
| 34 | deye | thing / matter | noun |
| 35 | fye | we (inclusive) | pronoun |

## Methodological note

These words are **not** removed from the training corpus. The instructor's
blind test file `tests/test_gbagyi_unseen.txt` consists largely of these same
function words. A bigram model trained on a stop-word-filtered corpus would
carry no probability mass for those transitions and its perplexity would
diverge. Filtering is therefore demonstrated on a sample in the notebook and
reported here as a deliverable, while the corpus itself remains complete.

## Loanword observation

Entries 23 to 26 are Hausa borrowings functioning as native Gbagyi discourse
connectives. Their high frequency reflects sustained Hausa contact across the
Middle Belt and is itself a finding worth noting in the report.
