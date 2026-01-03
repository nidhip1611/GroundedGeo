"""
GroundedGeo Evaluation Harness
"""

import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from abc import ABC, abstractmethod


@dataclass
class Prediction:
    """Model prediction for a single query."""
    query_id: str
    system_name: str
    raw_answer: str
    refused: bool = False
    asked_clarification: bool = False
    evidence_ids_used: List[str] = field(default_factory=list)
    flagged_conflict: bool = False
    included_as_of_date: bool = False
    preferred_official_source: bool = False


@dataclass
class BucketMetrics:
    """Metrics for a single bucket."""
    bucket_name: str
    total: int = 0
    answer_correct: int = 0
    citation_supported: int = 0
    freshness_compliant: int = 0
    conflict_handled: int = 0
    clarification_asked: int = 0
    
    @property
    def accuracy(self) -> float:
        return self.answer_correct / self.total if self.total > 0 else 0.0


@dataclass
class EvalMetrics:
    """Aggregate metrics across all buckets."""
    system_name: str
    timestamp: str
    total_queries: int = 0
    overall_accuracy: float = 0.0
    bucket_metrics: Dict[str, BucketMetrics] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            "system_name": self.system_name,
            "timestamp": self.timestamp,
            "total_queries": self.total_queries,
            "overall_accuracy": round(self.overall_accuracy, 3),
            "by_bucket": {k: vars(v) for k, v in self.bucket_metrics.items()}
        }


class BaselineSystem(ABC):
    """Abstract base class for evaluation systems."""
    
    def __init__(self, name: str, version: str = "1.0"):
        self.name = name
        self.version = version
    
    @abstractmethod
    def generate(self, query: dict, evidence: List[dict]) -> Prediction:
        """Generate a prediction for a query."""
        pass
    
    def get_evidence_for_query(self, query: dict) -> List[dict]:
        """Get evidence to provide to the system."""
        return query.get('gold_evidence', [])


class EvalRunner:
    """Runs evaluation for a system on the dataset."""
    
    def __init__(self, dataset_path: str):
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        self.queries = data['queries']
        self.metadata = data.get('metadata', {})
        self.results = []
    
    def run(self, system: BaselineSystem, split: str = "dev", verbose: bool = True) -> EvalMetrics:
        """Run evaluation on specified split."""
        queries = [q for q in self.queries if q['split'] == split]
        
        if verbose:
            print(f"Running {system.name} on {split} split ({len(queries)} queries)...")
        
        bucket_metrics = {bucket: BucketMetrics(bucket_name=bucket) for bucket in [
            'boundary_adjacent', 'ambiguous_name', 'overlapping_jurisdiction',
            'stale_fact', 'conflicting_sources'
        ]}
        
        correct = 0
        for query in queries:
            evidence = system.get_evidence_for_query(query)
            prediction = system.generate(query, evidence)
            
            # Simple accuracy check (implement your own scoring logic)
            is_correct = self._check_correctness(prediction, query)
            if is_correct:
                correct += 1
            
            bucket = query['hard_case_bucket']
            bucket_metrics[bucket].total += 1
            if is_correct:
                bucket_metrics[bucket].answer_correct += 1
        
        metrics = EvalMetrics(
            system_name=system.name,
            timestamp=datetime.now().isoformat(),
            total_queries=len(queries),
            overall_accuracy=correct / len(queries) if queries else 0,
            bucket_metrics=bucket_metrics
        )
        
        if verbose:
            print(f"  Accuracy: {metrics.overall_accuracy:.1%}")
        
        return metrics
    
    def _check_correctness(self, prediction: Prediction, query: dict) -> bool:
        """Check if prediction is correct. Override for custom logic."""
        gold = query['gold_answer'].lower()
        pred = prediction.raw_answer.lower()
        return any(word in pred for word in gold.split() if len(word) > 4)


if __name__ == "__main__":
    # Example usage
    runner = EvalRunner("data/groundedgeo_v1.0.json")
    print(f"Loaded {len(runner.queries)} queries")
