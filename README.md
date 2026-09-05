## Contributor : Abubakar Imran
## contributor : Usman Abdulsalam saba 

# Indigenous NLP Benchmark

A university-level low-resource Natural Language Processing assignment focusing on **Nupe** and **Gbagyi** language's

## Overview

This repository serves as a starter template for students learning fundamental NLP concepts through hands-on work with African low-resource languages. The assignment emphasizes:

- **Data Collection**: Web scraping and JSON Lines formatting
- **Tokenization**: Custom regex-based text processing with diacritic preservation
- **Linguistic Analysis**: Zipf's Law and frequency distributions
- **Language Modeling**: Bigram models with Laplace smoothing and perplexity evaluation

## Repository Structure

```
indigenous-nlp-benchmark/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .github/
│   └── workflows/
│       └── autograder.yml            # GitHub Actions CI/CD workflow
├── data/
│   ├── nupe/
│   │   ├── raw/                      # Raw scraped text data
│   │   └── processed/                # Cleaned and tokenized text
│   └── gbagyi/
│       ├── raw/                      # Raw scraped text data
│       └── processed/                # Cleaned and tokenized text
├── submissions/
│   └── group_01_nupe/
│       ├── HW1_assignment.ipynb      # Main assignment notebook
│       └── group_report.md           # Final analysis report
└── tests/
    ├── autograder_eval.py            # PyTest test suite
    ├── test_nupe_unseen.txt          # Unseen test data for evaluation
    └── test_gbagyi_unseen.txt        # Unseen test data for evaluation
```

## Assignment Overview

### Part 1: Data Collection
Implement a web scraper that collects text data from specified URLs and exports to JSON Line formats.

**Required Output Format** (`.jsonl`):
```json
{"id": 1, "url": "https://example.com", "date_retrieved": "2024-01-15", "raw_text": "..."}
{"id": 2, "url": "https://example.com", "date_retrieved": "2024-01-15", "raw_text": "..."}
```

### Part 2: Tokenization & Text Processing
Build a custom tokenizer that:
- Removes HTML markup
- Strips carriage returns and extra whitespace
- Preserves subdot diacritics (ẹ, ọ, ṇ, etc.) and tone marks
- Implements stop word filtering
- Returns tokens separated by single spaces

### Part 3: Zipf's Law Analysis
Analyze the token frequency distribution and determine if it follows Zipf's Law.

**Output**: Zipfian exponent `s` computed via log-log linear regression.

### Part 4: Bigram Language Model
Implement a bigram model from scratch with:
- Corpus fitting with unigram and bigram counting
- Probability computation with Laplace (Add-1) smoothing
- Perplexity evaluation on held-out test data

## Getting Started

### Prerequisites
- Python 3.10+
- pip or conda

### Installation

```bash
# Clone the repository
git clone https://github.com/abdullahikawu/indigenous-nlp-benchmark.git
cd indigenous-nlp-benchmark

# Install dependencies
pip install -r requirements.txt

# Start working on the assignment
jupyter notebook submissions/group_01_nupe/HW1_assignment.ipynb
```

## Autograding

This repository uses **GitHub Actions** for continuous autograding. When you push to a pull request targeting `main`, the following tests are automatically run:

1. **JSON Lines Schema Validation** - Ensures data files are properly formatted
2. **Processed Corpus Format** - Validates tokenization output
3. **Bigram Model Evaluation** - Tests model implementation and perplexity
4. **Git Collaboration Tracking** - Verifies multi-author contributions

View results in the **Checks** tab of your pull request.

## Assignment Deliverables

Students should complete and submit:

1. ✅ **Completed Jupyter Notebook** (`HW1_assignment.ipynb`) with all 4 parts implemented
2. ✅ **Raw Data** (`data/*/raw/*.jsonl`) with scraped contents
3. ✅ **Processed Corpus** (`data/*/processed/*.txt`) with tokenized text
4. ✅ **Group Report** (`group_report.md`) with analysis findings
5. ✅ **Git History** - Multiple commits from all team members

## Grading Rubric

| Component | Points | Criteria |
|-----------|--------|----------|
| Data Collection | 20% | Correctly formatted JSON with valid schema |
| Tokenization | 25% | Proper handling of diacritics and stop words |
| Zipf's Law Analysis | 20% | Accurate linear regression and interpretation |
| Bigram Model | 25% | Working implementation with correct perplexity |
| Report & Collaboration | 10% | Clear writing and multi-author commits |

## Resources
- **NLP Class Resource**: [Read/Watch NLP Tutorial esp NLP Fundamentals and N-Language Models](https://github.com/abdullahikawu/nlp-class)
- **Video Tutorial Code for this assignment**: [NLP Tutorial](https://www.youtube.com/watch?v=JdtuvnOhCZM)
- **Tutorial for this assignment**: [NLP Tutorial](https://github.com/abdullahikawu/nlp-class/blob/master/homework/HW1/assignment.ipynb)
- **About Nupe Language**: [Project Documentation](https://en.wikipedia.org/wiki/Nupe_language)
- **About Gbagyi Language**: [Project Documentation](https://en.wikipedia.org/wiki/Gbagyi_language)
- **Zipf's Law**: [Wikipedia](https://en.wikipedia.org/wiki/Zipf%27s_law)
- **Language Modeling**: [Speech and Language Processing (Jurafsky & Martin)](https://web.stanford.edu/~jurafsky/slp3/)

## Support & Questions

For issues or clarifications:
1. Ask in the class group
2. Consult the assignment notebook comments
3. Contact your Lecturer

##license

This repository is provided for educational purposes under the MIT License.

---

**Last Updated**: 25/08/2026
**Course Name**: CSC 406 - Artificial Intelligence
**Course Level**: Beginner to Intermediate NLP / Linguistics  
**Duration**: 1 week - Due September 1st 2026

## License
##Group 4 Member

-Abubakar Imran
