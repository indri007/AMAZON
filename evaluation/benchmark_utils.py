# evaluation/benchmark_utils.py
"""Utility functions for the AMAZON RAG benchmark.
These helpers support:
- Relative improvement percentages
- Confidence‑interval computation (95 % by default)
- Effect‑size (Cohen's d) for paired samples
"""

import numpy as np
import scipy.stats as st

def improvement_percent(baseline: float, amazon: float) -> float:
    """Return the relative improvement of *amazon* over *baseline* in percent.
    Formula: ((amazon - baseline) / baseline) * 100
    """
    if baseline == 0:
        return float('inf')
    return (amazon - baseline) / baseline * 100.0

def confidence_interval(data: np.ndarray, confidence: float = 0.95):
    """Return (mean, lower, upper) 95 % confidence interval for *data*.
    Uses Student's t‑distribution (appropriate for small sample sizes).
    """
    n = len(data)
    if n < 2:
        raise ValueError("Need at least two samples to compute CI")
    mean = np.mean(data)
    sem = st.sem(data)
    h = sem * st.t.ppf((1 + confidence) / 2.0, n - 1)
    return mean, mean - h, mean + h

def cohens_d(baseline: np.ndarray, amazon: np.ndarray) -> float:
    """Cohen's d for paired samples.
    Positive value means Amazon outperforms baseline.
    """
    diff = amazon - baseline
    return diff.mean() / diff.std(ddof=1)
