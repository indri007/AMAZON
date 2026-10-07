# Metric thresholds for AMAZON RAG benchmark
# Values are the minimum acceptable performance levels.
# Used by evaluation scripts to assert that the system meets requirements.

METRIC_TARGETS = {
    "Recall@1": 0.70,
    "Recall@3": 0.85,
    "Recall@5": 0.90,
    "MRR@10": 0.75,
    "GroundedAnswerRate": 0.90,
    "HallucinationRate": 0.05,  # <= allowed, will be compared as max value
    "CitationAccuracy": 0.90,
    "P95LatencySec": 8.0,      # max latency in seconds
}
