# GroundedGeo Results

## Main Results

We evaluate 5 baseline systems on GroundedGeo's dev split (147 queries) and test split (53 queries).

### Overall Performance

| System | Dev Accuracy | Test Accuracy |
|--------|-------------|---------------|
| Closed-Book LLM | 22.4% | 15.1% |
| Naive RAG | 81.6% | 79.2% |
| Official-First RAG | **98.6%** | **94.3%** |
| Freshness-Filter RAG | 81.6% | 79.2% |
| Conflict-Aware RAG | 98.0% | 92.5% |

**Key finding**: Standard RAG achieves ~80% accuracy but fails on the conflict bucket (11% test). Adding official-source ranking or conflict detection raises overall accuracy to 92-94%.

### Bucket-Specific Behavior (Test Split)

| System | Boundary Acc. | Clarif. Asked | Overlap Acc. | Freshness Compl. | Conflict Handled |
|--------|--------------|---------------|--------------|------------------|------------------|
| Closed-Book | 33.3% | 27.3% | 0.0% | 0.0% | 11.1% |
| Naive RAG | 100% | 100% | 72.7% | 0.0% | 11.1% |
| Official-First | 100% | 100% | 72.7% | 100% | **100%** |
| Freshness-Filter | 100% | 100% | 72.7% | 100% | 11.1% |
| Conflict-Aware | 100% | 100% | 72.7% | 100% | 88.9% |

**Behavioral insights**:
- **Clarification**: All RAG systems properly ask for clarification on ambiguous names (100%)
- **Freshness**: Freshness-aware systems include "as of" dates (100% compliance)
- **Conflict handling**: Only Official-First (100%) and Conflict-Aware (88.9%) properly handle source conflicts

## Ablation Analysis

Each behavioral module fixes its targeted bucket:

| Module Added | Stale Fact Compliance | Conflict Handled |
|--------------|----------------------|------------------|
| Naive RAG (baseline) | 0.0% | 11.1% |
| + Freshness Filter | **100%** | 11.1% |
| + Official Ranking | 100% | **100%** |
| + Conflict Detection | 100% | 88.9% |

## Failure Mode Analysis

### Overlapping Jurisdiction (72.7% accuracy)

Even with official-first retrieval, models struggle with administrative exceptions (e.g., independent cities, DC agency routing) and fall back to generic "county/district" templates.

**Examples**:
- Richmond, VA is an independent city with no county, but models output "Richmond is in [County]"
- DC noise complaints route to DCRA or MPD, not a county sheriff

**Fix direction**: Jurisdiction exception layer detecting phrases like "independent city", "consolidated city-county".

### Conflict Detection Miss (1 test error)

The Getty Center query reveals scope confusion: official source says "admission free" while review says "$20" (referring to parking). The conflict detector missed this because values have different implicit scopes.

**Fix direction**: Normalize monetary patterns and detect semantic opposites ("free" vs "$X" for same attribute type).

## Qualitative Examples

### Example 1: Ambiguous Name → Clarification

**Query**: "What county is Springfield in?"

| System | Response |
|--------|----------|
| Naive RAG | "Springfield is in Sangamon County, Illinois." |
| Official-First | "CLARIFICATION NEEDED: 'Springfield' has 34 GNIS matches. Which Springfield? Please specify state." |

### Example 2: Stale Fact → Freshness Compliance

**Query**: "What are the hours of the Brooklyn DMV?"

| System | Response |
|--------|----------|
| Naive RAG | "The DMV is open Monday-Friday 9 AM - 5 PM." |
| Freshness-Filter | "As of 2025-12-15: Brooklyn Atlantic Center DMV hours are Mon-Fri 8:00 AM - 5:00 PM. Verify at dmv.ny.gov." |

### Example 3: Conflicting Sources → Conflict Flagged

**Query**: "What are the hours of the Oakland DMV?"

| System | Response |
|--------|----------|
| Naive RAG | "The Oakland DMV is open 9 AM - 5 PM." |
| Conflict-Aware | "SOURCES CONFLICT: Official dmv.ca.gov says opens 8 AM (Wed 9 AM). Community source says 9 AM daily. Use official hours." |

## Summary

GroundedGeo reveals that standard RAG systems achieve high accuracy on simple lookups but fail on edge cases requiring source comparison. Adding source ranking (official-first) or explicit conflict detection raises conflict-bucket accuracy from 11% to 89-100%, with consistent gains across dev and test splits.
