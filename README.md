# GroundedGeo: A Benchmark for Citation-Grounded Geographic QA

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
git clone https://github.com/nidhip1611/GroundedGeo.git
cd GroundedGeo
pip install -r requirements.txt
```

### Load Dataset
```python
import json

with open('data/groundedgeo_v1.0.json') as f:
    dataset = json.load(f)

queries = dataset['queries']
print(f"Loaded {len(queries)} queries")
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
| Naïve RAG | 100.0% | 100.0% | 72.7% | 0.0% | 11.1% |
| **Official-First** | 100.0% | 100.0% | 72.7% | 100.0% | **100.0%** |
| Freshness-Filter | 100.0% | 100.0% | 72.7% | 100.0% | 11.1% |
| Conflict-Aware | 100.0% | 100.0% | 72.7% | 100.0% | 88.9% |

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
├── results/
│   ├── final_results.json
│   ├── error_analysis.json
│   └── aggregate_metrics.json
├── paper/
│   ├── PAPER_DRAFT.md
│   ├── paper.tex
│   └── paper_tables.tex
├── requirements.txt
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## 📝 Citation
```bibtex
@misc{pandya2025groundedgeo,
  title={GroundedGeo: A Benchmark for Citation-Grounded Geographic QA},
  author={Pandya, Nidhi},
  year={2025},
  url={https://github.com/nidhip1611/GroundedGeo}
}
```

## 📜 License

- **Dataset**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Code**: [MIT License](LICENSE)

## 📧 Contact

- **Author**: Nidhi Pandya
- **Institution**: Pace University, Seidenberg School of Computer Science
