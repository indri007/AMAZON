# Helper to load a static QA/IR dataset for benchmarking
# Expected JSON format (list of dicts):
# [{"id": "q1", "question": "...", "gold_answers": ["..."], "gold_citations": ["doc1", "doc2"]}, ...]

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def load_queries(filename: str = "hrd_questions.json"):
    """Load queries from ``data/<filename>``.
    Returns a list of dictionaries with keys ``id``, ``question``, ``gold_answers``
    and ``gold_citations``.
    """
    file_path = DATA_DIR / filename
    if not file_path.is_file():
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
