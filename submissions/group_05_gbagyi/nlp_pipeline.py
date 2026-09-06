"""
Gbagyi NLP Pipeline - CSC 406 Group 05
======================================

Part 2: Normalization and custom tokenization (no NLTK, no SpaCy)
Part 3: Zipf's Law fitting
Part 4: Bigram language model with Laplace (Add-1) smoothing

The tokenizer output format is matched to tests/test_gbagyi_unseen.txt:
    shekwoi wa ye na nyi yi .
    gama shekwoi wa ye na nyi yi , har wa wo ɓi gba gmanyi ga .

Observed properties of the target format:
  - all lowercase
  - punctuation detached as its own token
  - the character ɓ (U+0253) is used
  - hyphenated words stay as ONE token: bui-bui, zaho-zahoyi
  - no digits
  - single space between tokens, one sentence per line
"""

import json
import math
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


# ----------------------------------------------------------------------
# PART 2: NORMALIZATION AND TOKENIZATION
# ----------------------------------------------------------------------

# Gbagyi-specific characters that must survive cleaning.
# ɓ U+0253, ɗ U+0257, ə U+0259, ʼ U+02BC (modifier apostrophe, as in ʼya)
GBAGYI_EXTRA_CHARS = "ɓɗəʼ"

# Punctuation that gets detached into standalone tokens
DETACHABLE_PUNCT = r"""[.,;:!?()\[\]{}"«»“”„…]"""

# Stop words. The Gbagyi entries below are the highest-frequency function
# words observed in the corpus. Translations should be confirmed by a
# native speaker before submission.
STOP_WORDS = [
    # Gbagyi function words (confirm translations with a native speaker)
    "wa", "nu", "yi", "n", "ɓa", "ge", "na", "ye", "wo", "ho",
    "ba", "ku", "lo", "shi", "zhin", "ntu", "ɓo", "ɓe", "a", "ma",
    "gna", "to", "ama", "sai", "har", "gama", "nya", "ɓi", "ga", "ta",
    # English fallbacks in case of code-mixing in scraped pages
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "for", "of", "with", "by", "from", "is", "are", "was", "were", "be",
]


def normalize_text(text):
    """
    Unicode-normalize and strip markup. Run this BEFORE anything else.

    NFC is applied first so that ɓ and any combining marks are represented
    consistently. Mixing NFC and NFD inflates vocabulary size and corrupts
    the perplexity comparison against the instructor's test file.
    """
    # 1. Unicode normalization (critical, do this first)
    text = unicodedata.normalize("NFC", text)

    # 2. Remove HTML / XML markup
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-zA-Z]+;", " ", text)
    text = re.sub(r"&#\d+;", " ", text)

    # 3. Strip control characters (\r, \t, \x00-\x1f) but keep newlines for now
    text = text.replace("\r", " ").replace("\t", " ")
    text = "".join(ch for ch in text
                   if ch == "\n" or unicodedata.category(ch)[0] != "C")

    # 4. Normalize quote variants down to the modifier apostrophe used in Gbagyi
    text = text.replace("\u2019", "\u02bc").replace("\u2018", "\u02bc")
    text = text.replace("'", "\u02bc")

    # 5. Collapse whitespace
    text = re.sub(r"[ ]+", " ", text)
    return text.strip()


def split_sentences(text):
    """
    Split normalized text into sentences on . ? ! followed by whitespace.
    Returns a list of sentence strings (terminator retained).
    """
    text = re.sub(r"\s+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]


def custom_tokenizer(text, remove_stopwords=False, keep_punctuation=True):
    """
    Tokenize Gbagyi text without any pre-trained English tokenizer.

    Args:
        text (str): input text (raw or normalized)
        remove_stopwords (bool): filter STOP_WORDS out.
            IMPORTANT: keep this False when building the training corpus.
            The instructor's test file is dense with function words, so a
            model trained on a stop-word-filtered corpus cannot score them
            and perplexity explodes.
        keep_punctuation (bool): emit punctuation as standalone tokens,
            matching the target format `... nyi yi .`

    Returns:
        str: space-separated tokens
    """
    text = normalize_text(text)

    # Lowercase. str.lower() leaves ɓ and ə untouched, which is what we want.
    text = text.lower()

    # Remove digits entirely (the target format contains none)
    text = re.sub(r"\d+", " ", text)

    # Detach punctuation into standalone tokens, or drop it
    if keep_punctuation:
        text = re.sub(r"(" + DETACHABLE_PUNCT + r")", r" \1 ", text)
    else:
        text = re.sub(DETACHABLE_PUNCT, " ", text)

    # Drop stray characters that are neither letters, the Gbagyi extras,
    # a hyphen, nor retained punctuation.
    allowed = set(GBAGYI_EXTRA_CHARS) | set("-")
    if keep_punctuation:
        allowed |= set(".,;:!?()[]{}\"")
    cleaned = []
    for ch in text:
        if ch.isspace() or ch.isalpha() or ch in allowed:
            cleaned.append(ch)
        else:
            cleaned.append(" ")
    text = "".join(cleaned)

    # Split on whitespace. Hyphens stay inside tokens (bui-bui stays whole).
    tokens = text.split()

    # Drop bare hyphens and empty artefacts
    tokens = [t for t in tokens if t and t != "-"]

    if remove_stopwords:
        stops = set(STOP_WORDS)
        tokens = [t for t in tokens if t not in stops]

    return " ".join(tokens)


def build_corpus(jsonl_path, output_path, min_tokens=3):
    """
    Read raw JSONL, produce the one-sentence-per-line processed corpus.

    Guarantees required by tests/autograder_eval.py:
      - no double spaces
      - no leading or trailing space
      - no tabs, no carriage returns

    Returns:
        dict: statistics about the produced corpus
    """
    jsonl_path = Path(jsonl_path)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    doc_count = 0

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            entry = json.loads(raw_line)
            doc_count += 1

            normalized = normalize_text(entry["raw_text"])
            for sentence in split_sentences(normalized):
                tokenized = custom_tokenizer(sentence, remove_stopwords=False)
                if len(tokenized.split()) >= min_tokens:
                    lines.append(tokenized)

    # Final safety pass against the autograder's format assertions
    safe_lines = []
    for line in lines:
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            safe_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(safe_lines) + "\n")

    all_tokens = " ".join(safe_lines).split()
    return {
        "documents": doc_count,
        "sentences": len(safe_lines),
        "total_tokens": len(all_tokens),
        "vocabulary_size": len(set(all_tokens)),
        "output_path": str(output_path),
    }


def validate_corpus_format(path):
    """Re-run the autograder's format checks locally. Returns list of problems."""
    problems = []
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            s = line.rstrip("\n")
            if not s:
                continue
            if any(not tok for tok in s.split(" ")):
                problems.append(f"line {n}: multiple consecutive spaces")
            if s.startswith(" "):
                problems.append(f"line {n}: leading space")
            if s.endswith(" "):
                problems.append(f"line {n}: trailing space")
            if "\t" in s:
                problems.append(f"line {n}: tab character")
            if "\r" in s:
                problems.append(f"line {n}: carriage return")
    return problems


# ----------------------------------------------------------------------
# PART 3: ZIPF'S LAW
# ----------------------------------------------------------------------

def fit_zipf_law(token_list, plot=True, trim_head=5, trim_tail_singletons=True,
                 save_path=None):
    """
    Fit log(f) = C - s * log(r) and return the Zipfian exponent s.

    The top few ranks and the singleton tail both deviate from the power law
    and drag the slope, so they are trimmed before regression.

    Args:
        token_list (list[str] | str): tokens, or a space-separated string
        plot (bool): draw the log-log plot
        trim_head (int): number of top ranks excluded from the fit
        trim_tail_singletons (bool): exclude frequency-1 words from the fit
        save_path (str | None): where to save the figure

    Returns:
        tuple: (s, r_squared, freq_counter)
    """
    import numpy as np

    if isinstance(token_list, str):
        token_list = token_list.split()

    freq = Counter(token_list)
    sorted_freqs = sorted(freq.values(), reverse=True)

    ranks = np.arange(1, len(sorted_freqs) + 1)
    freqs = np.array(sorted_freqs, dtype=float)

    # Build the fitting mask
    mask = np.ones(len(freqs), dtype=bool)
    if trim_head > 0:
        mask[:trim_head] = False
    if trim_tail_singletons:
        mask &= freqs > 1

    if mask.sum() < 10:
        mask = np.ones(len(freqs), dtype=bool)

    log_r = np.log10(ranks[mask])
    log_f = np.log10(freqs[mask])

    slope, intercept = np.polyfit(log_r, log_f, 1)
    s = -slope

    predicted = slope * log_r + intercept
    ss_res = float(np.sum((log_f - predicted) ** 2))
    ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
    r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    if plot:
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.rcParams["axes.grid"] = True

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.loglog(ranks, freqs, marker=".", linestyle="none",
                  markersize=4, alpha=0.6, label="Observed Gbagyi tokens")
        fit_line = 10 ** (intercept + slope * np.log10(ranks))
        ax.loglog(ranks, fit_line, linestyle="--", linewidth=2,
                  label=f"Fit: s = {s:.3f}, R2 = {r_squared:.3f}")
        ax.set_xlabel("Rank (log scale)")
        ax.set_ylabel("Frequency (log scale)")
        ax.set_title("Zipf's Law: Gbagyi Corpus (Group 05)")
        ax.legend()
        fig.tight_layout()
        if save_path:
            fig.savefig(save_path, dpi=150)
        plt.show()

    return s, r_squared, freq


# ----------------------------------------------------------------------
# PART 4: BIGRAM LANGUAGE MODEL
# ----------------------------------------------------------------------

class BigramModel:
    """
    Bigram language model with Laplace (Add-1) smoothing, built from scratch
    using dictionary frequency counts.

    Method signatures match the assignment template exactly:
        fit(corpus_file_path) -> int
        get_probability(w1, w2) -> float
        compute_perplexity(test_file_path) -> float

    Attributes:
        unigrams (dict): {token: count}
        bigrams (dict): {(w1, w2): count}
        vocab_size (int): number of unique tokens including <s> and </s>
    """

    START = "<s>"
    END = "</s>"

    def __init__(self):
        self.unigrams = defaultdict(int)
        self.bigrams = defaultdict(int)
        self.vocab_size = 0
        self.total_tokens = 0
        self.sentence_count = 0

    def _sentence_tokens(self, line):
        """Wrap a sentence with boundary markers."""
        tokens = line.strip().split()
        if not tokens:
            return []
        return [self.START] + tokens + [self.END]

    def fit(self, corpus_file_path):
        """
        Build unigram and bigram counts from a corpus file.

        Args:
            corpus_file_path (str): one sentence per line, space-separated tokens

        Returns:
            int: total number of bigram tokens observed
        """
        total_bigrams = 0
        with open(corpus_file_path, "r", encoding="utf-8") as f:
            for line in f:
                tokens = self._sentence_tokens(line)
                if not tokens:
                    continue
                self.sentence_count += 1

                for tok in tokens:
                    self.unigrams[tok] += 1
                    self.total_tokens += 1

                for i in range(len(tokens) - 1):
                    self.bigrams[(tokens[i], tokens[i + 1])] += 1
                    total_bigrams += 1

        self.vocab_size = len(self.unigrams)
        return total_bigrams

    def get_probability(self, w1, w2):
        """
        P(w2 | w1) with Laplace smoothing.

            P(w2|w1) = (count(w1, w2) + 1) / (count(w1) + V)

        An unseen context w1 yields count(w1) = 0, giving 1/V. That keeps the
        probability strictly positive so perplexity never becomes infinite.
        """
        if self.vocab_size == 0:
            raise ValueError("Model has not been fitted. Call fit() first.")
        bigram_count = self.bigrams.get((w1, w2), 0)
        unigram_count = self.unigrams.get(w1, 0)
        return (bigram_count + 1) / (unigram_count + self.vocab_size)

    def compute_perplexity(self, test_file_path):
        """
        Perplexity on a held-out file.

            PP = exp( -1/N * sum log P(w_i | w_{i-1}) )

        Computed in log space to avoid floating point underflow.
        """
        log_prob_sum = 0.0
        n_bigrams = 0

        with open(test_file_path, "r", encoding="utf-8") as f:
            for line in f:
                # Apply the same normalization the training corpus received,
                # so that Unicode form and casing match.
                line = normalize_text(line).lower()
                tokens = self._sentence_tokens(line)
                if len(tokens) < 2:
                    continue
                for i in range(len(tokens) - 1):
                    p = self.get_probability(tokens[i], tokens[i + 1])
                    log_prob_sum += math.log(p)
                    n_bigrams += 1

        if n_bigrams == 0:
            raise ValueError("No bigrams found in the test file.")

        return math.exp(-log_prob_sum / n_bigrams)

    def top_bigrams(self, n=10):
        """Return the n most frequent bigrams with their smoothed probabilities."""
        ranked = sorted(self.bigrams.items(), key=lambda kv: kv[1], reverse=True)
        return [
            (w1, w2, count, self.get_probability(w1, w2))
            for (w1, w2), count in ranked[:n]
        ]


class UnigramModel:
    """Unigram model with Laplace smoothing (Part 4 requires both models)."""

    def __init__(self):
        self.unigrams = defaultdict(int)
        self.total_tokens = 0
        self.vocab_size = 0

    def fit(self, corpus_file_path):
        with open(corpus_file_path, "r", encoding="utf-8") as f:
            for line in f:
                for tok in line.strip().split():
                    self.unigrams[tok] += 1
                    self.total_tokens += 1
        self.vocab_size = len(self.unigrams)
        return self.total_tokens

    def get_probability(self, word):
        return (self.unigrams.get(word, 0) + 1) / (self.total_tokens + self.vocab_size)

    def compute_perplexity(self, test_file_path):
        log_prob_sum = 0.0
        n = 0
        with open(test_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = normalize_text(line).lower()
                for tok in line.strip().split():
                    log_prob_sum += math.log(self.get_probability(tok))
                    n += 1
        if n == 0:
            raise ValueError("No tokens found in the test file.")
        return math.exp(-log_prob_sum / n)
