# GroundedGeo: A Benchmark for Citation-Grounded, Freshness-Aware, Conflict-Aware Geographic QA

## Abstract

Retrieval-augmented generation (RAG) systems are widely used for geographic and civic-information question answering, yet they often fail on real-world edge cases involving ambiguous place names, overlapping jurisdictions, time-sensitive facts, and conflicting sources. We introduce GroundedGeo, a research-grade benchmark of 200 evidence-grounded US geographic queries spanning five hard-case buckets (40 each): boundary-adjacent lookups, ambiguous place names, overlapping jurisdictions, stale facts, and conflicting sources. Each query includes curated evidence spans with source metadata to evaluate citation correctness, freshness compliance, and conflict handling.

We implement five baselines: a closed-book LLM, naïve RAG, official-first RAG, freshness-filter RAG, and conflict-aware RAG. On a frozen test split (53 queries), closed-book achieves 17.0% accuracy, naïve RAG 79.2%, official-first 94.3%, freshness-filter 79.2%, and conflict-aware 92.5%. Bucket-specific results show that naïve RAG fails on conflicting sources (11.1% conflict handled), while official-first and conflict-aware resolve conflicts (100% and 88.9%, respectively). We identify a key failure mode in overlapping jurisdiction queries, where models default to generic county/district templates rather than handling administrative exceptions. GroundedGeo provides a focused benchmark for building RAG systems that behave reliably under real civic and geographic constraints.

## 1. Introduction

Geographic and civic question answering is a common use case for retrieval-augmented generation (RAG) systems. Users ask questions like "What county is this address in?", "What are the DMV hours?", or "Who represents my district?" These queries appear simple but contain hidden complexity:

- **Ambiguous place names**: "Springfield" exists in 34 US states
- **Overlapping jurisdictions**: A single location may fall under federal, state, county, city, and special district authorities
- **Time-sensitive facts**: Office hours, fees, and policies change frequently
- **Conflicting sources**: Google Maps may show different hours than official .gov websites

Standard RAG evaluation focuses on answer accuracy, but this misses critical behavioral failures. A system that confidently returns "Springfield is in Illinois" when the user meant Massachusetts has failed, even if Illinois is a valid answer. A system that cites outdated hours without noting the retrieval date provides false confidence.

We introduce GroundedGeo, a benchmark designed to evaluate RAG systems on these behavioral dimensions:

1. **Citation correctness**: Are claims supported by cited evidence?
2. **Clarification behavior**: Does the system ask for disambiguation when needed?
3. **Freshness compliance**: Does the system include temporal grounding ("as of DATE")?
4. **Conflict handling**: Does the system flag source disagreements?

### Contributions

1. **Benchmark**: GroundedGeo v1.0 — 200 evidence-grounded queries across five hard-case buckets, with structured metadata (JSON/JSONL/CSV exports)

2. **Behavioral Metrics**: Bucket-specific evaluation: county accuracy, clarification asked, jurisdiction handling, freshness compliance, and conflict handled

3. **Baselines**: Five reference systems from closed-book to conflict-aware RAG

4. **Findings**: RAG achieves high accuracy on simple lookups but fails under conflict/freshness constraints; official ranking and conflict detection address this

5. **Diagnostics**: Qualitative examples and failure-mode analysis highlighting jurisdictional exceptions and scope-confusion conflicts

## 2. Dataset

### 2.1 Design Principles

GroundedGeo targets five hard-case buckets, each exposing a distinct failure mode:

| Bucket | Queries | Target Behavior | Example Query |
|--------|---------|-----------------|---------------|
| Boundary Adjacent | 40 | Citation accuracy near borders | "What county contains (40.7128, -74.0060)?" |
| Ambiguous Name | 40 | Ask clarification | "What county is Springfield in?" |
| Overlapping Jurisdiction | 40 | Clarify district type + stable facts | "What district is this location in?" |
| Stale Fact | 40 | Include "as of DATE" | "What are the DMV hours?" |
| Conflicting Sources | 40 | Flag conflict, prefer official | "What time does the museum open?" |

### 2.2 Query Schema

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
      "doc_id": "tiger_nyc_001",
      "url": "https://www.census.gov/geo/...",
      "source_type": "official",
      "passage_text": "TIGER/Line 2024: point intersects New York County...",
      "span_start": 0,
      "span_end": 45,
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

### 2.3 Evidence Sources

Evidence spans are drawn from:

- **Official sources**: US Census TIGER/Line, USGS GNIS, state DMV websites, city .gov sites
- **Community sources**: Simulated aggregator data (representing Google Maps, Yelp-style sources)

Each evidence span includes:
- `source_type`: official, community, encyclopedia, news
- `retrieved_date`: Frozen snapshot date (2025-12-15)
- `source_published_date`: When the source was last updated (where available)

### 2.4 Dataset Statistics

| Statistic | Value |
|-----------|-------|
| Total queries | 200 |
| Dev split | 147 |
| Test split | 53 |
| Queries with evidence | 200 (100%) |
| Multi-source queries | 85 |
| Refusal expected | 61 |

### 2.5 Bucket Invariants

We enforce consistency constraints:

- **Ambiguous Name**: `ambiguity_label=needs_clarification`, `refusal_expected=True`
- **Overlapping Jurisdiction**: `ambiguity_label=multi_valid`, `refusal_expected=False`
- **Stale Fact**: `freshness_requirement_days` is set (7-365 days depending on info type)
- **Conflicting Sources**: Includes both true conflicts (`conflict_label=conflicting_sources`) and false positives (`conflict_label=none`) to test precision

## 3. Baselines

We implement five systems with progressively more sophisticated evidence handling:

### 3.1 Closed-Book LLM

No evidence provided. Tests pure parametric knowledge. Expected to fail on boundary cases, stale facts, and conflicts.

### 3.2 Naïve RAG

Uses all provided evidence without ranking or filtering. Represents a standard production RAG setup. Expected to fail when sources conflict or information is stale.

### 3.3 Official-First RAG

Ranks evidence by source authority: official (.gov) > encyclopedia > community. When sources conflict, the official source is preferred. Does not explicitly flag conflicts.

### 3.4 Freshness-Filter RAG

Filters evidence based on `freshness_requirement_days`. Drops stale sources when fresh alternatives exist. Includes "as of DATE" in responses. Does not handle conflicts explicitly.

### 3.5 Conflict-Aware RAG

Detects contradictions between sources by comparing extracted values (hours, fees, phone numbers). When conflict is detected, flags it explicitly and prefers official sources. Combines freshness filtering with conflict detection.

| System | Evidence | Official Ranking | Freshness Filter | Conflict Detection |
|--------|----------|------------------|------------------|--------------------|
| Closed-Book | ❌ | ❌ | ❌ | ❌ |
| Naïve RAG | ✅ | ❌ | ❌ | ❌ |
| Official-First | ✅ | ✅ | ❌ | (implicit) |
| Freshness-Filter | ✅ | ✅ | ✅ | ❌ |
| Conflict-Aware | ✅ | ✅ | ✅ | ✅ |

## 4. Experiments

### 4.1 Setup

We evaluate all five systems on GroundedGeo v1.0 using a 147/53 dev/test split. Each query includes one or more evidence spans with URLs, source type, and temporal metadata. We report:

1. **Overall accuracy**: Answer correctness
2. **Bucket-specific behavioral metrics**:
   - Boundary Adjacent: County accuracy
   - Ambiguous Name: Clarification asked rate
   - Overlapping Jurisdiction: Accuracy (stable facts + type clarification)
   - Stale Fact: Freshness compliance (includes "as of" date)
   - Conflicting Sources: Conflict handled (flags disagreement or prefers official)

### 4.2 Overall Results

**Table 1: Overall Performance**

| System | Dev Accuracy | Test Accuracy |
|--------|-------------|---------------|
| Closed-Book LLM | 18.4% | 17.0% |
| Naïve RAG | 81.6% | 79.2% |
| Official-First RAG | 98.6% | 94.3% |
| Freshness-Filter RAG | 81.6% | 79.2% |
| Conflict-Aware RAG | 98.0% | 92.5% |

Closed-book performance is low (17.0%), reflecting the difficulty of answering jurisdictional and policy questions without evidence. RAG substantially improves accuracy: naïve RAG reaches 79.2%, but remains brittle under source disagreement. Official-first RAG achieves the best test accuracy (94.3%) by prioritizing authoritative sources, while conflict-aware RAG reaches 92.5%.

### 4.3 Bucket-Specific Results

**Table 2: Bucket-Specific Behavioral Metrics (Test Split)**

| System | Boundary Acc. | Clarif. Asked | Overlap Acc. | Freshness Compl. | Conflict Handled |
|--------|--------------|---------------|--------------|------------------|------------------|
| Closed-Book | 33.3% | 27.3% | 0.0% | 0.0% | 11.1% |
| Naïve RAG | 100.0% | 100.0% | 72.7% | 0.0% | 11.1% |
| Official-First | 100.0% | 100.0% | 72.7% | 100.0% | 100.0% |
| Freshness-Filter | 100.0% | 100.0% | 72.7% | 100.0% | 11.1% |
| Conflict-Aware | 100.0% | 100.0% | 72.7% | 100.0% | 88.9% |

**Key observations:**

1. **Boundary Adjacent**: All RAG systems achieve 100% accuracy when evidence is provided. Closed-book (33.3%) struggles without grounding.

2. **Ambiguous Name**: All RAG systems correctly ask for clarification (100%). Evidence helps models recognize when disambiguation is needed.

3. **Overlapping Jurisdiction**: All RAG systems achieve 72.7%, exposing a challenging failure mode where models default to generic templates.

4. **Stale Fact**: Systems with official ranking achieve 100% freshness compliance. Naïve RAG (0.0%) fails to include temporal grounding.

5. **Conflicting Sources**: The key differentiator. Naïve RAG collapses (11.1%) by picking the first source. Official-first resolves conflicts (100%) through implicit preference. Conflict-aware explicitly detects conflicts (88.9%).

### 4.4 Qualitative Examples

**Example 1: Ambiguous Name → Clarification**

Query: "What county is Springfield in?"

| System | Response |
|--------|----------|
| Naïve RAG | "Springfield is in Sangamon County, Illinois." |
| Official-First | "CLARIFICATION NEEDED: 'Springfield' has 34 GNIS matches. Which Springfield? Please specify state." |

**Example 2: Stale Fact → Freshness Compliance**

Query: "What are the hours of the Brooklyn DMV?"

| System | Response |
|--------|----------|
| Naïve RAG | "The DMV is open Monday-Friday 9 AM - 5 PM." |
| Freshness-Filter | "As of 2025-12-15: Brooklyn Atlantic Center DMV hours are Mon-Fri 8:00 AM - 5:00 PM. Verify at dmv.ny.gov." |

**Example 3: Conflicting Sources → Conflict Flagged**

Query: "What are the hours of the Oakland DMV?"

| System | Response |
|--------|----------|
| Naïve RAG | "The Oakland DMV is open 9 AM - 5 PM." |
| Conflict-Aware | "SOURCES CONFLICT: Official dmv.ca.gov says opens 8 AM (Wed 9 AM). Community source says 9 AM daily. Use official hours." |

## 5. Discussion

### 5.1 Failure Mode: Overlapping Jurisdiction Templates

The hardest bucket is overlapping jurisdiction (72.7% accuracy across all RAG systems). Error analysis reveals that models default to generic "county/district" templates even when evidence indicates exceptions:

- **Richmond, VA**: An independent city with no county. Models output "Richmond is in [County]" instead of recognizing the independent city status.
- **DC noise complaints**: Should route to DCRA or MPD, not a county agency. Models apply county-based templates inappropriately.

This suggests retrieval alone is insufficient. Models must learn to:
1. Detect exception cues ("independent city", "not in any county", "consolidated city-county")
2. Select the correct jurisdiction type based on user intent

### 5.2 Failure Mode: Scope Confusion in Conflicts

One conflict-aware miss (Getty Center) illustrates attribute scope confusion:
- Source A: "Admission is free"
- Source B: "$20 to visit" (referring to parking, not admission)

The conflict detector failed because the values have different implicit scopes. Fixing this requires:
1. Normalizing monetary patterns
2. Aligning extracted values to the same attribute
3. Detecting semantic opposites ("free" vs "$X") only when attributes match

### 5.3 Why Official-First Outperforms Conflict-Aware

Official-first RAG (94.3%) slightly outperforms conflict-aware (92.5%) because:

1. Official ranking implicitly resolves conflicts without requiring explicit detection
2. Conflict detection can miss subtle disagreements (scope confusion)
3. For GroundedGeo queries, official sources are reliably correct

However, conflict-aware provides better transparency by explicitly flagging disagreements, which may be preferred in high-stakes applications.

## 6. Limitations and Ethics

### 6.1 Scope

- **US-only**: GroundedGeo focuses on US administrative boundaries and civic services. International generalization requires additional benchmarks.
- **Snapshot date**: Evidence was collected as of 2025-12-15. Time-sensitive information may have changed.
- **Simulated baselines**: Our baselines simulate LLM behavior rather than calling production APIs. Real-world performance may differ.

### 6.2 Data Sources

- All geographic data is from public sources (US Census, USGS GNIS, official .gov websites)
- No personal or user-identifying information is included
- Community source passages are synthetic/paraphrased to avoid copyright issues

### 6.3 Intended Use

GroundedGeo is designed for:
- Evaluating RAG system behavior on edge cases
- Diagnosing citation, freshness, and conflict handling failures
- Benchmarking improvements to evidence ranking and aggregation

It is not intended for:
- Production deployment without human verification
- Legal or official determinations of jurisdiction
- Real-time civic information (always verify with official sources)

## 7. Conclusion

We introduced GroundedGeo, a benchmark of 200 evidence-grounded geographic queries designed to evaluate RAG system behavior under ambiguity, staleness, and source conflict. Our experiments show that standard RAG achieves 79.2% accuracy but fails on conflict handling (11.1%). Adding official-source ranking raises accuracy to 94.3% and conflict handling to 100%. We identify overlapping jurisdiction as a remaining challenge where models default to generic templates rather than handling administrative exceptions.

GroundedGeo provides a focused diagnostic tool for building RAG systems that behave reliably on civic and geographic queries. The dataset, evaluation code, and baseline implementations are available at [repository URL].

## References

[To be added based on related work]

---

## Appendix A: Dataset Files

| File | Description |
|------|-------------|
| `groundedgeo_v1.0.json` | Full dataset with metadata |
| `groundedgeo_v1.0.jsonl` | HuggingFace-compatible format |
| `groundedgeo_v1.0.csv` | Flattened for spreadsheet viewing |
| `groundedgeo_schema.json` | JSON Schema for validation |

## Appendix B: Reproducibility

- **Snapshot date**: 2025-12-15 (all evidence retrieval dates frozen)
- **Random seed**: 42-46 (deterministic train/test splits per bucket)
- **Dev/Test split**: 147/53 queries
- **Evaluation code**: Available in `eval/` directory

