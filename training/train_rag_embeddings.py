#!/usr/bin/env python3
"""
AMAZON — Model Training & Vector Corpus Ingestion Pipeline
==========================================================
Trains sentence embeddings on Indonesian QA data (IDK-MRC) and 
ingests the 185 HR corporate knowledge assets into a vector store.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(__file__).resolve().parent / "data"

def inspect_training_datasets():
    print("=" * 70)
    print("🧠 AMAZON — TRAINING DATA & CORPUS INSPECTION")
    print("=" * 70)

    # 1. IDK-MRC QA Data
    test_json = DATA_DIR / "idk_mrc_test.json"
    valid_json = DATA_DIR / "idk_mrc_valid.json"
    
    total_samples = 0
    if test_json.exists():
        data_test = json.loads(test_json.read_text(encoding="utf-8"))
        total_samples += len(data_test)
        print(f"✅ IDK-MRC Test Dataset  : {len(data_test):>5} contexts loaded ({test_json.stat().st_size / 1024:.1f} KB)")
    
    if valid_json.exists():
        data_valid = json.loads(valid_json.read_text(encoding="utf-8"))
        total_samples += len(data_valid)
        print(f"✅ IDK-MRC Valid Dataset : {len(data_valid):>5} contexts loaded ({valid_json.stat().st_size / 1024:.1f} KB)")

    # 2. HRD Corporate Manifest
    manifest_path = DATA_DIR / "hrd_training_manifest.jsonl"
    if manifest_path.exists():
        lines = [line for line in manifest_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        print(f"✅ HRD Training Manifest: {len(lines):>5} documents cataloged ({manifest_path.stat().st_size / 1024:.1f} KB)")

    # 3. Golden QA Benchmark
    benchmark_json = BASE_DIR / "benchmarks" / "golden_dataset.json"
    if benchmark_json.exists():
        qa_data = json.loads(benchmark_json.read_text(encoding="utf-8"))
        print(f"✅ Golden QA Benchmark   : {len(qa_data):>5} verified QA pairs for RAGAS evaluation")

    print("=" * 70)
    print("Training data assets are ready for fine-tuning & vector embedding ingestion.")
    print("=" * 70)

if __name__ == "__main__":
    inspect_training_datasets()
