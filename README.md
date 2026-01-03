# GroundedGeo: A Benchmark for Citation-Grounded Geographic QA

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18142378.svg)](https://doi.org/10.5281/zenodo.18142378)
[![Dataset on HuggingFace](https://img.shields.io/badge/🤗-Dataset-yellow)](https://huggingface.co/datasets/nidhipandya/GroundedGeo)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

**GroundedGeo** is a research-grade benchmark for evaluating RAG systems on location-based queries with **verifiable citations**, **freshness awareness**, and **conflict handling**.

## 🎯 Key Findings (Frozen Test Split)

> Naïve RAG reaches **79.2%** accuracy but fails on **conflicting sources** (**11.1% conflict-handled**).  
> Adding **official-source ranking** improves overall accuracy to **94.3%** and raises conflict handling to **100%**.

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
| **Boundary Adjacent** | 40 | County accuracy near borders | Locations near county/state lines |
| **Ambiguous Name** | 40 | Ask clarification | "Springfield" exists in many states |
| **Overlapping Jurisdiction** | 40 | Clarify authority type | Multiple jurisdictions apply |
| **Stale Fact** | 40 | Prefer fresh sources + "as of" | Hours/fees/policies change |
| **Conflicting Sources** | 40 | Detect & flag/resolve conflict | Official vs community disagree |

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/nidhip1611/GroundedGeo.git
cd GroundedGeo
pip install -r requirements.txt
```

### Load Dataset (JSON)
```python
import json

with open("data/groundedgeo_v1.0.json", "r") as f:
    dataset = json.load(f)

queries = dataset["queries"]
print("Loaded", len(queries), "queries")

dev = [q for q in queries if q["split"] == "dev"]
test = [q for q in queries if q["split"] == "test"]
```

### Using HuggingFace Datasets
```python
from datasets import load_dataset

ds = load_dataset("nidhip1611/groundedgeo", data_files="groundedgeo_v1.0.jsonl")
print(ds)
```

## 📈 Benchmark Results

### Overall Accuracy

| System | Dev | Test (Frozen) |
|--------|-----|---------------|
| Closed-Book LLM | 18.4% | 17.0% |
| Naïve RAG | 81.6% | 79.2% |
| **Official-First RAG** | **98.6%** | **94.3%** |
| Freshness-Filter RAG | 81.6% | 79.2% |
| Conflict-Aware RAG | 98.0% | 92.5% |

### Bucket-Specific Metrics (Test Split)

| System | Boundary Accuracy | Clarification Asked | Overlap Accuracy | Freshness Compliant | Conflict Handled |
|--------|-------------------|---------------------|------------------|---------------------|------------------|
| Closed-Book LLM | 25.0% | 45.5% | 0.0% | 0.0% | 11.1% |
| Naïve RAG | 100.0% | 100.0% | 72.7% | 0.0% | 11.1% |
| **Official-First RAG** | 100.0% | 100.0% | 72.7% | 100.0% | **100.0%** |
| Freshness-Filter RAG | 100.0% | 100.0% | 72.7% | 100.0% | 11.1% |
| Conflict-Aware RAG | 100.0% | 100.0% | 72.7% | 100.0% | 88.9% |

## 📁 Repository Structure
```
GroundedGeo/
├── data/
│   ├── groundedgeo_v1.0.json
│   ├── groundedgeo_v1.0.jsonl
│   └── groundedgeo_v1.0.csv
├── eval/
│   ├── harness.py
│   └── __init__.py
├── eval_results/
│   ├── final_results.json
│   ├── error_analysis.json
│   ├── aggregate_metrics.json
│   ├── PAPER_DRAFT.md
│   ├── paper.tex
│   └── paper_tables.tex
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
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

runner = EvalRunner(dataset_path="data/groundedgeo_v1.0.json")
print(f"Loaded {len(runner.queries)} queries")
```

## 📝 Citation
```bibtex
@misc{pandya2025groundedgeo,
  title={GroundedGeo: A Benchmark for Citation-Grounded Geographic QA},
  author={Pandya, Nidhi},
  year={2025},
  doi={10.5281/zenodo.18142378},
  url={https://github.com/nidhip1611/GroundedGeo}
}
```

## 📜 License

- **Dataset**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code**: [MIT License](LICENSE)

## 🙏 Acknowledgments

- US Census Bureau for TIGER/Line boundary data
- USGS for GNIS place name data
- State DMV and city government websites for civic information

## 📧 Contact

- **Author**: Nidhi Pandya
- **Email**: nidhipandya1606@gmail.com
- **Institution**: Pace University, Seidenberg School of Computer Science

---

## Related Projects

- [BoundaryBench](https://github.com/nidhip1611/BoundaryBench) — LLM geospatial boundary diagnosis
- [GroundedGeo](https://github.com/nidhip1611/GroundedGeo) — RAG citation grounding benchmark
- [NewsScope](https://github.com/nidhip1611/NewsScope) — Cross-domain news verification
