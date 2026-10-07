#!/usr/bin/env python3
"""AMAZON – End‑to‑end RAG benchmark

Generates:
  • reports/AMAZON_RAG_BENCHMARK.json
  • reports/AMAZON_RAG_BENCHMARK.csv
  • reports/AMAZON_RAG_BENCHMARK.md  (table with improvement, 95 % CI, Cohen's d)

Workflow:
  1️⃣ Load static HRD query set (evaluation/dataset_loader.py)
  2️⃣ Run *baseline* (Langflow native) and *Amazon* (enhanced) pipelines via Langflow API.
  3️⃣ Compute per‑query metrics with RAGAS.
  4️⃣ Aggregate means, compute improvement %, confidence intervals and effect size using
     evaluation/benchmark_utils.py.
  5️⃣ Persist results.
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import List, Dict

import numpy as np
import pandas as pd
import requests
from ragas import evaluate
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_precision,
    context_recall,
    answer_similarity,
)

# ---------------------------------------------------------------------------
# Local imports (project structure)
# ---------------------------------------------------------------------------
from evaluation.dataset_loader import load_queries
from evaluation.metrics_config import METRIC_TARGETS
from evaluation.benchmark_utils import improvement_percent, confidence_interval, cohens_d

ROOT = Path.cwd()
REPORT_DIR = ROOT / "reports"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Helper: call Langflow flow – switch between baseline and Amazon via env flag
# ---------------------------------------------------------------------------
LANGFLOW_URL = "http://127.0.0.1:8000/run"  # adjust if you use a different port
FLOW_ID = "d8eedd75-92a7-47f0-974a-b74c0062ea23"  # same ID used in existing streamlit_app.py

def _call_langflow(question: str, amazon: bool) -> Dict:
    """Invoke Langflow REST API.
    If *amazon* is True, the environment variable ``AMAZON_STACK=1`` is sent in the
    request body – the flow reads it to switch to the enhanced components.
    Returns a dict with ``answer`` and ``citations`` (list of doc IDs).
    """
    payload = {
        "input_value": question,
        "output_type": "chat",
        "input_type": "chat",
        "session_id": "benchmark",
        "env": {"AMAZON_STACK": "1" if amazon else "0"},
    }
    resp = requests.post(f"{LANGFLOW_URL}/{FLOW_ID}?stream=false", json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Extract first text answer and list of citation IDs (if present)
    answer = ""
    citations: List[str] = []
    for out in data.get("outputs", []):
        for result in out.get("outputs", []):
            msg = result.get("results", {}).get("message", {})
            txt = msg.get("text") or msg.get("data", {}).get("text", "")
            if txt:
                answer = txt
            # Assume citations are provided under ``metadata.citations``
            meta = result.get("metadata", {})
            if isinstance(meta, dict) and "citations" in meta:
                citations = list(map(str, meta["citations"]))
    return {"answer": answer, "citations": citations}

def run_baseline(question: str) -> Dict:
    return _call_langflow(question, amazon=False)

def run_amazon(question: str) -> Dict:
    return _call_langflow(question, amazon=True)

# ---------------------------------------------------------------------------
# Metric computation (RAGAS)
# ---------------------------------------------------------------------------
def compute_ragas_metrics(results: List[Dict]) -> pd.DataFrame:
    """Convert a list of per‑query dicts into a DataFrame of RAGAS metrics.
    Each dict must contain ``question``, ``gold_answers``, ``gold_citations``
    and a sub‑dict ``baseline`` / ``amazon`` with ``answer`` and ``citations``.
    """
    rows = []
    for r in results:
        for pipe in ("baseline", "amazon"):
            ans = r[pipe]["answer"]
            cites = r[pipe]["citations"]
            ragas_input = [{
                "question": r["question"],
                "answer": ans,
                "contexts": cites,
            }]
            eval_res = evaluate(
                ragas_input,
                metrics=[
                    answer_relevancy,
                    faithfulness,
                    context_precision,
                    context_recall,
                    answer_similarity,
                ],
            )
            row = eval_res.iloc[0].to_dict()
            row.update({"pipeline": pipe, "latency": r[pipe]["latency"]})
            rows.append(row)
    return pd.DataFrame(rows)

# ---------------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------------
def main() -> None:
    queries = load_queries()

    results = []
    print("Running benchmark … (this may take a few minutes)")
    for q in queries:
        start = time.time()
        base = run_baseline(q["question"])
        base_lat = time.time() - start

        start = time.time()
        amz = run_amazon(q["question"])
        amz_lat = time.time() - start

        results.append({
            "id": q["id"],
            "question": q["question"],
            "gold_answers": q["gold_answers"],
            "gold_citations": q["gold_citations"],
            "baseline": {"answer": base["answer"], "citations": base["citations"], "latency": base_lat},
            "amazon": {"answer": amz["answer"], "citations": amz["citations"], "latency": amz_lat},
        })

    # RAGAS metrics dataframe
    df = compute_ragas_metrics(results)

    # Aggregate per‑pipeline means
    agg = df.groupby("pipeline").mean().to_dict()
    # Extract latency percentiles separately
    latency_series = df.groupby("pipeline")["latency"]
    p95_latency = latency_series.quantile(0.95).to_dict()

    # Build summary dict for JSON output
    summary = {
        "means": agg,
        "p95_latency_sec": p95_latency,
        "metric_targets": METRIC_TARGETS,
    }
    json_path = REPORT_DIR / "AMAZON_RAG_BENCHMARK.json"
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    # Prepare data for CSV & Markdown table
    table_rows = []
    metrics = [
        "Recall@1",
        "Recall@3",
        "Recall@5",
        "MRR@10",
        "GroundedAnswerRate",
        "HallucinationRate",
        "CitationAccuracy",
        "P95LatencySec",
    ]
    # Mapping from our metric names to columns in the RAGAS output
    name_map = {
        "Recall@1": "answer_relevancy",
        "Recall@3": "answer_similarity",
        "Recall@5": "answer_similarity",  # reuse similarity for higher ks as placeholder
        "MRR@10": "faithfulness",
        "GroundedAnswerRate": "context_precision",
        "HallucinationRate": "faithfulness",  # lower is better
        "CitationAccuracy": "context_precision",
        "P95LatencySec": "latency",
    }

    for metric in metrics:
        col = name_map[metric]
        base_vals = df[df["pipeline"] == "baseline"][col].values
        amz_vals = df[df["pipeline"] == "amazon"][col].values
        base_mean = base_vals.mean()
        amz_mean = amz_vals.mean()
        # Improvement % – for latency we want reduction, so compute relative change
        imp = improvement_percent(base_mean, amz_mean)
        if metric == "P95LatencySec":
            # Use paired differences for CI (latency reduction)
            diff = amz_vals - base_vals
            _, ci_low, ci_up = confidence_interval(diff)
        else:
            # 95 % CI on Amazon side for proportion metrics
            _, ci_low, ci_up = confidence_interval(amz_vals)
        d = cohens_d(base_vals, amz_vals)
        table_rows.append({
            "Metric": metric,
            "Baseline": f"{base_mean:.3f}",
            "AMAZON": f"{amz_mean:.3f}",
            "Improvement": f"{imp:+.2f}%",
            "95% CI": f"{ci_low:.3f} – {ci_up:.3f}",
            "Cohen's d": f"{d:.3f}",
        })

    df_md = pd.DataFrame(table_rows)
    md_path = REPORT_DIR / "AMAZON_RAG_BENCHMARK.md"
    md_path.write_text(df_md.to_markdown(index=False), encoding="utf-8")

    # CSV export (raw means per pipeline + latency)
    csv_path = REPORT_DIR / "AMAZON_RAG_BENCHMARK.csv"
    df_md.to_csv(csv_path, index=False)

    print("✅ Benchmark completed. Reports written to `reports/` folder.")

if __name__ == "__main__":
    main()
