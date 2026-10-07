"""
test_golden_dataset.py
Unit tests verifying golden dataset structure, integrity, and sample size for AMAZON RAG.
"""

import unittest
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

class TestGoldenDataset(unittest.TestCase):

    def setUp(self):
        self.base_path = ROOT / "benchmarks" / "golden_dataset.json"
        self.expanded_path = ROOT / "benchmarks" / "golden_dataset_expanded_110.json"

    def test_golden_dataset_base_exists_and_valid(self):
        self.assertTrue(self.base_path.exists(), f"File {self.base_path} must exist.")
        with open(self.base_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0, "Base golden dataset must not be empty.")

    def test_golden_dataset_required_fields(self):
        with open(self.base_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        for idx, item in enumerate(data):
            self.assertIn("question", item, f"Item {idx} missing 'question'")
            self.assertIn("ground_truth", item, f"Item {idx} missing 'ground_truth'")
            self.assertIn("category", item, f"Item {idx} missing 'category'")
            self.assertTrue(len(item["question"].strip()) > 5, f"Question at {idx} is too short")
            self.assertTrue(len(item["ground_truth"].strip()) > 5, f"Ground truth at {idx} is too short")

    def test_golden_dataset_expanded_sample_size(self):
        self.assertTrue(self.expanded_path.exists(), f"File {self.expanded_path} must exist.")
        with open(self.expanded_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertGreaterEqual(len(data), 100, "Expanded dataset must have at least N >= 100 samples.")

    def test_golden_dataset_diversity(self):
        with open(self.base_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        categories = set(item.get("category") for item in data)
        self.assertGreaterEqual(len(categories), 3, "Dataset should cover at least 3 distinct categories.")

if __name__ == "__main__":
    unittest.main()
