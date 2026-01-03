# GroundedGeo Dataset v1.0.0

**A benchmark dataset for evaluating RAG systems on location-based queries with verifiable citations.**

## Overview

GroundedGeo contains 200 queries across 5 hard-case buckets designed to test:

1. **Citation correctness** - Can the system cite sources that actually support its claims?
2. **Freshness awareness** - Does the system prefer recent sources for time-sensitive info?
3. **Appropriate refusal** - Does the system ask for clarification when queries are ambiguous?
4. **Conflict detection** - Can the system identify when sources disagree?

## Dataset Statistics

| Bucket | Count | Description |
|--------|-------|-------------|
| boundary_adjacent | 40 | Locations near administrative boundaries |
| ambiguous_name | 40 | Place names that exist in multiple locations |
| overlapping_jurisdiction | 40 | Multiple jurisdictions apply |
| stale_fact | 40 | Time-sensitive information |
| conflicting_sources | 40 | Sources provide contradictory information |

### Split Distribution

- **Dev set**: 147 queries (for tuning thresholds)
- **Test set**: 53 queries (hold-out evaluation)

### Evidence Coverage

- Single evidence source: 115 queries
- Multiple evidence sources: 85 queries

### Refusal Expectations

- Refusal expected (should ask clarification): 61
- Answer expected: 139

## Files

| File | Description |
|------|-------------|
| `groundedgeo_v1.0.json` | Full dataset with metadata |
| `groundedgeo_v1.0.jsonl` | HuggingFace compatible format |
| `groundedgeo_v1.0.csv` | Flattened for spreadsheet viewing |
| `groundedgeo_stats.json` | Detailed statistics |
| `groundedgeo_schema.json` | JSON Schema for validation |

## Key Features

### Claim-Level Verification
Each query includes `gold_claims` - atomic facts that can be individually verified against evidence.

### Span-Level Citations
Evidence includes `span_start` and `span_end` offsets pointing to the exact text that supports each claim.

### Freshness Metadata
Evidence includes `retrieved_date`, `source_published_date` for temporal evaluation.

### Refusal Expectations
`refusal_expected` indicates whether the system should ask for clarification rather than guessing.

## Usage
```python
import json

# Load full dataset
with open('groundedgeo_v1.0.json') as f:
    dataset = json.load(f)
    
queries = dataset['queries']
print(f"Loaded {len(queries)} queries")

# Filter by bucket
boundary_queries = [q for q in queries if q['hard_case_bucket'] == 'boundary_adjacent']

# Filter by split
dev_queries = [q for q in queries if q['split'] == 'dev']
test_queries = [q for q in queries if q['split'] == 'test']
```

## Research Context

GroundedGeo is part of a research agenda on grounded AI systems:

- **BoundaryBench** - Diagnosed LLM failures on geospatial boundaries (13,000 points)
- **GroundedGeo** - Builds verifiable RAG evaluation for location queries (200 queries)
- **NewsScope** - Extends grounding/verification to news domain

## Snapshot Date

All evidence was collected as of **2025-12-15**. Time-sensitive queries should be evaluated against this date.

## License

CC-BY-4.0

## Citation
```bibtex
@dataset{groundedgeo2025,
  title={GroundedGeo: A Benchmark for Citation-Grounded Location Queries},
  author={Niki},
  year={2025},
  version={1.0.0}
}
```

---
Created: 2026-01-02

## Evaluation Summary

### Final Results (Test Split)

| System | Accuracy | Key Behavior |
|--------|----------|--------------|
| Closed-Book LLM | 15.1% | No grounding (0% citations) |
| Naive RAG | 79.2% | Fails on conflicts (11%) |
| **Official-First RAG** | **94.3%** | Best overall |
| Freshness-Filter RAG | 79.2% | 100% freshness compliance |
| Conflict-Aware RAG | 92.5% | 89% conflict handling |

### Key Takeaway

> "GroundedGeo reveals that standard RAG systems achieve ~80% accuracy on simple lookups but fail on edge cases requiring source comparison. Adding official-source ranking raises accuracy to 94%."

### Behavioral Metrics

- **Boundary Adjacent**: All RAG systems achieve 100% county accuracy
- **Ambiguous Name**: All RAG systems ask clarification (100%)  
- **Overlapping Jurisdiction**: 72.7% - administrative exceptions remain challenging
- **Stale Fact**: Freshness-aware systems achieve 100% compliance
- **Conflicting Sources**: Official-First achieves 100%, Conflict-Aware 89%

### Files
```
GroundedGeo/
├── groundedgeo_v1.0.json          # Full dataset
├── groundedgeo_v1.0.jsonl         # HuggingFace format
├── groundedgeo_v1.0.csv           # Spreadsheet view
├── README.md                      # Documentation
└── eval_results/
    ├── final_results.json         # Dev + Test metrics
    ├── paper_tables.tex           # LaTeX for paper
    ├── RESULTS_SECTION.md         # Paper results draft
    ├── error_analysis.json        # Failure analysis
    └── *_predictions.jsonl        # Per-system outputs
```
