# TF-IDF-IR-Eval

Evaluate TF-IDF IR performance across CISI, Cranfield, MED, and NPL datasets.

---

## Overview

This project implements a **TF-IDF (Term Frequency–Inverse Document Frequency)** based information retrieval system to evaluate performance across four benchmark datasets:

- **CISI**
- **Cranfield**
- **MED (Medline)**
- **NPL**

The system:

- Converts raw dataset files into structured CSVs.
- Computes TF-IDF vectors with **60 different configurations**.
- Retrieves and ranks relevant documents using vector similarity.
- Evaluates performance with **Precision@10, Recall, and Mean Average Precision (MAP)**.
- Identifies **best weighting combinations** per dataset and overall.

---

## Methodology

The TF-IDF weighting scheme in this project uses three main components:

- **TF (Term Frequency)**: raw or transformed frequency of a term in a document.
- **IDF (Inverse Document Frequency)**: rarity of the term across the collection.
- **Normalization**: adjusts for document length and scale differences.

Final weight = `TF × IDF`, with normalization applied.

### Supported Weighting Functions

**Term Frequency (TF):**

- `natural`: raw counts
- `augmented`: normalized by max frequency
- `boolean`: binary presence (0/1)
- `log_avg`: log of average frequency
- `logarithmic`: log-scaled frequency

**Inverse Document Frequency (IDF):**

- `standard`: log(N/df)
- `probabilistic`: log((N–df)/df)
- `none`: constant 1

**Normalization:**

- `none`
- `cosine`
- `pivoted`
- `byte`

**Total combinations:** 5 TF × 3 IDF × 4 Norm = **60 configs**

---

## Implementation Details

### 1. Data Preprocessing

- Raw `.ALL`, `.QRY`, `.REL` files are parsed and converted into CSV (`docs.csv`, `queries.csv`, `qrels.csv`).
- Parsing functions extract:
  - **Docs:** `DocID, Title, Author, Source, Text`
  - **Queries:** `QueryID, Text`
  - **Qrels:** `QueryID, DocID, Relevance`

> During conversion, irrelevant metadata and inconsistent formatting are removed.

### 2. Tokenization & Text Processing

- Lowercasing
- Tokenization with NLTK
- Stopword removal
- Lemmatization (WordNet)
- Conversion into **dictionary + bag-of-words**

### 3. TF/IDF/Normalization Functions

- Implemented as modular Python functions.
- Applied to both documents and queries.
- Output: weighted, normalized TF-IDF vectors.

### 4. Similarity & Ranking

- Similarity measured using **dot product** (compatible with cosine and other norms).
- Top-10 documents retrieved for each query.

### 5. Evaluation Metrics

- **Precision@10**
- **Recall**
- **Mean Average Precision (MAP)**

### 6. Parallel Execution

- Heavy computations across 60 configs × 4 datasets parallelized with `joblib.Parallel`.

### 7. Results Aggregation

- All results saved to `results/tfidf_results_gensim.csv`.
- Best config selected **per dataset** and **overall**.

---

## Results Summary

**Best TF-IDF configurations (based on MAP):**

| Dataset | TF          | IDF           | Norm    | MAP    | Precision@10 | Recall |
| ------- | ----------- | ------------- | ------- | ------ | ------------ | ------ |
| MED     | logarithmic | standard      | cosine  | 0.2641 | 0.6500       | 0.3196 |
| CISI    | logarithmic | standard      | cosine  | 0.0594 | 0.2063       | 0.0819 |
| Cran    | boolean     | standard      | pivoted | 0.0026 | 0.0080       | 0.0061 |
| NPL     | augmented   | standard      | pivoted | 0.1327 | 0.3172       | 0.1924 |
| Overall | logarithmic | probabilistic | pivoted | 0.1083 | -            | -      |

👉 Full metrics table available in: `results/tfidf_results_gensim.csv`

**Key Finding:**  
Logarithmic TF consistently performed best across datasets, especially when combined with **standard or probabilistic IDF** and **cosine/pivoted normalization**.

## Requirements

Also download required **NLTK data** (handled in notebook):

- `punkt`
- `stopwords`
- `wordnet`

---

## Usage

### 1. Process Raw Data

Place dataset files under:

```
data/raw/{CISI, cran, MED, NPL}/
```

Run conversion scripts:

```bash
python src/data_processing/Datasets2csv.py   # For CISI, Cran, MED
python src/data_processing/npl2csv.py        # For NPL
```

Outputs are stored in:

```
data/processed/
```

---

### 2. Run TF-IDF Analysis

Launch the Jupyter notebook:

```bash
jupyter notebook src/analysis/TD_IDF.ipynb
```

The notebook will:

- Load CSV files
- Build vocabulary
- Compute TF-IDF for 60 configurations
- Perform retrieval & evaluation
- Save results

---

### 3. View Results

- Results CSV: `results/tfidf_results_gensim.csv`
- Notebook: includes detailed outputs & visualizations

---

## File Structure

```
TF-IDF-IR-Eval/
├── README.md              # This file
├── src/
│   ├── data_processing/
│   │   ├── Datasets2csv.py
│   │   └── npl2csv.py
│   └── analysis/
│       └── TD_IDF.ipynb
├── data/
│   ├── raw/               # Original datasets
│   └── processed/         # CSVs
└── tfidf_results_gensim.csv # Output metrics
```
