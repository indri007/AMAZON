"""
test_evaluation_metrics.py
Unit tests verifying metrics configuration and statistical helper functions.
"""

import unittest
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from evaluation.metrics_config import METRIC_TARGETS
from evaluation.benchmark_utils import improvement_percent, confidence_interval, cohens_d

class TestEvaluationMetrics(unittest.TestCase):

    def test_metrics_targets_structure(self):
        self.assertIsInstance(METRIC_TARGETS, dict)
        self.assertIn("Recall@1", METRIC_TARGETS)
        self.assertIn("MRR@10", METRIC_TARGETS)
        self.assertIn("GroundedAnswerRate", METRIC_TARGETS)
        self.assertIn("HallucinationRate", METRIC_TARGETS)
        for metric, target in METRIC_TARGETS.items():
            self.assertGreaterEqual(target, 0.0, f"Target for {metric} must be non-negative")

    def test_improvement_percent_calculation(self):
        # 0.5 to 0.75 is +50%
        imp = improvement_percent(0.5, 0.75)
        self.assertAlmostEqual(imp, 50.0, places=2)

        # Baseline 0 should return float('inf')
        imp_zero = improvement_percent(0.0, 0.8)
        self.assertEqual(imp_zero, float('inf'))

    def test_confidence_interval_bounds(self):
        sample = np.array([0.8, 0.82, 0.85, 0.81, 0.84, 0.83, 0.86, 0.82])
        mean_val, low, high = confidence_interval(sample, confidence=0.95)
        self.assertAlmostEqual(mean_val, float(np.mean(sample)), places=4)
        self.assertLessEqual(low, mean_val)
        self.assertGreaterEqual(high, mean_val)

    def test_cohens_d_effect_size(self):
        baseline = np.array([0.6, 0.62, 0.59, 0.61, 0.63])
        amazon = np.array([0.8, 0.85, 0.82, 0.83, 0.84])
        d = cohens_d(baseline, amazon)
        # Amazon is clearly higher than baseline -> d should be positive and large
        self.assertGreater(d, 1.0, "Effect size d should be large (> 1.0)")

if __name__ == "__main__":
    unittest.main()
