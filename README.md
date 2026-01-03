# GroundedGeo: A Benchmark for Citation-Grounded Geographic QA

[![Dataset on HuggingFace](https://img.shields.io/badge/🤗-Dataset-yellow)](https://huggingface.co/datasets/YOUR_USERNAME/groundedgeo)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![arXiv](https://img.shields.io/badge/arXiv-2501.XXXXX-b31b1b.svg)](https://arxiv.org/abs/2501.XXXXX)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**GroundedGeo** is a research-grade benchmark for evaluating RAG systems on location-based queries with verifiable citations, freshness awareness, and conflict detection.

## 🎯 Key Findings

> Standard RAG achieves **79.2%** accuracy but fails on conflict handling (**11.1%**). Adding official-source ranking raises accuracy to **94.3%** and conflict handling to **100%**.

## 📊 Dataset Overview

| Statistic | Value |
|-----------|-------|
| Total queries | 200 |
| Dev / Test split | 147 / 53 |
| Hard-case buckets | 5 (40 each) |
| Multi-source queries | 85 |
| Queries with evidence | 200 (100%) |

### Five Hard-Case Buckets

| Bucket | Count | Target Behavior | Challenge |
|--------|-------|-----------------|-----------|
| **Boundary Adjacent** | 40 | Citation accuracy | Locations near county/state lines |
| **Ambiguous Name** | 40 | Ask clarification | "Springfield" exists in 34 states |
| **Overlapping Jurisdiction** | 40 | Clarify district type | Multiple authorities apply |
| **Stale Fact** | 40 | Include "as of" date | DMV hours, fees change |
| **Conflicting Sources** | 40 | Flag conflict | Official vs community disagree |

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/YOUR_USERNAME/groundedgeo.git
cd groundedgeo
pip install -r requirements.txt
```

### Load Dataset
```python
import json

# Load full dataset
with open('data/groundedgeo_v1.0.json') as f:
    dataset = json.load(f)

queries = dataset['queries']
print(f"Loaded {len(queries)} queries")

# Filter by bucket
boundary_queries = [q for q in queries if q['hard_case_bucket'] == 'boundary_adjacent']

# Filter by split
dev_queries = [q for q in queries if q['split'] == 'dev']
test_queries = [q for q in queries if q['split'] == 'test']
```

### Using HuggingFace Datasets
```python
from datasets import load_dataset

dataset = load_dataset("YOUR_USERNAME/groundedgeo")
print(dataset)
```

## 📈 Benchmark Results

### Overall Accuracy

| System | Dev | Test |
|--------|-----|------|
| Closed-Book LLM | 18.4% | 17.0% |
| Naïve RAG | 81.6% | 79.2% |
| **Official-First RAG** | **98.6%** | **94.3%** |
| Freshness-Filter RAG | 81.6% | 79.2% |
| Conflict-Aware RAG | 98.0% | 92.5% |

### Bucket-Specific Metrics (Test Split)

| System | Boundary | Clarif. | Overlap | Fresh. | Conflict |
|--------|----------|---------|---------|--------|----------|
| Closed-Book | 25.0% | 45.5% | 0.0% | 0.0% | 11.1% |
| Naïve RAG | 100% | 100% | 72.7% | 0.0% | 11.1% |
| **Official-First** | 100% | 100% | 72.7% | 100% | **100%** |
| Freshness-Filter | 100% | 100% | 72.7% | 100% | 11.1% |
| Conflict-Aware | 100% | 100% | 72.7% | 100% | 88.9% |

## 📁 Repository Structure
```
groundedgeo/
├── data/
│   ├── groundedgeo_v1.0.json      # Full dataset with metadata
│   ├── groundedgeo_v1.0.jsonl     # HuggingFace format
│   └── groundedgeo_v1.0.csv       # Spreadsheet view
├── eval/
│   ├── harness.py                 # Evaluation harness
│   ├── baselines.py               # 5 baseline implementations
│   └── metrics.py                 # Scoring functions
├── results/
│   ├── final_results.json         # Frozen test results
│   └── predictions/               # Per-system outputs
├── paper/
│   ├── paper.tex                  # LaTeX source
│   └── figures/                   # Paper figures
├── notebooks/
│   └── GroundedGeo_Phase2.ipynb   # Dataset creation notebook
├── requirements.txt
├── LICENSE
└── README.md
```

## 🔬 Query Schema

Each query contains:
```json
{
  "query_id": "gg_boundary_0001",
  "query_text": "What county contains (40.7128, -74.0060)?",
  "query_type": "boundary",
  "gold_answer": "New York County, New York",
  "hard_case_bucket": "boundary_adjacent",
  "split": "dev",
  "gold_evidence": [
    {
      "doc_id": "tiger_36061",
      "url": "https://www.census.gov/geo/...",
      "source_type": "official",
      "passage_text": "TIGER/Line 2024: point intersects New York County...",
      "span_start": 42,
      "span_end": 65,
      "retrieved_date": "2025-12-15",
      "source_published_date": "2024-01-01"
    }
  ],
  "ambiguity_label": "unambiguous",
  "conflict_label": "none",
  "freshness_requirement_days": null,
  "refusal_expected": false
}
```

## 🏃 Running Evaluation
```python
from eval.harness import EvalRunner
from eval.baselines import OfficialFirstRAG

# Initialize
runner = EvalRunner(dataset_path='data/groundedgeo_v1.0.json')
system = OfficialFirstRAG()

# Run on dev split
metrics = runner.run(system, split='dev')
print(f"Accuracy: {metrics.overall_accuracy:.1%}")

# Run on test split (frozen)
test_metrics = runner.run(system, split='test')
print(f"Test Accuracy: {test_metrics.overall_accuracy:.1%}")
```

## 📝 Citation
```bibtex
@article{groundedgeo2025,
  title={GroundedGeo: A Benchmark for Citation-Grounded, Freshness-Aware, Conflict-Aware Geographic QA},
  author={Pandya, Nidhi},
  journal={arXiv preprint arXiv:2501.XXXXX},
  year={2025}
}
```

## 📜 License

- **Dataset**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code**: [MIT License](LICENSE)

## 🙏 Acknowledgments

- US Census Bureau for TIGER/Line boundary data
- USGS for GNIS place name data
- Various state DMV and city government websites for civic information

## 📧 Contact

- **Author**: Nidhi Pandya
- **Email**: [your.email@example.com]
- **Institution**: Pace University, Seidenberg School of Computer Science

---

**Part of the Grounded AI Research Agenda:**
- [BoundaryBench](https://github.com/YOUR_USERNAME/boundarybench) - LLM geospatial boundary diagnosis
- [GroundedGeo](https://github.com/YOUR_USERNAME/groundedgeo) - RAG citation grounding benchmark
- [NewsScope](https://github.com/YOUR_USERNAME/newsscope) - Cross-domain news verification
