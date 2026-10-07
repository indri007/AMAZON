#!/usr/bin/env python3
"""
AMAZON — Automated Technical & RAG Audit
========================================

Audit:
1. Repository structure
2. README / architecture consistency
3. Langflow flow
4. Streamlit application
5. Dependencies
6. Secret leakage
7. Cloud Run endpoint
8. Streamlit endpoint
9. MCP configuration
10. RAG documents
11. Persistence indicators
12. Reproducibility

Outputs:
    reports/AMAZON_AUDIT.json
    reports/AMAZON_AUDIT.md
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# CONFIGURATION
# ============================================================

REPO_URL = "https://github.com/indri007/AMAZON"

DEFAULT_ROOT = Path.cwd()

REPORT_DIR = DEFAULT_ROOT / "reports"
JSON_REPORT = REPORT_DIR / "AMAZON_AUDIT.json"
MD_REPORT = REPORT_DIR / "AMAZON_AUDIT.md"

EXPECTED_FILES = [
    "README.md",
    "ARCHITECTURE.md",
    "streamlit_app.py",
]

EXPECTED_DIRS = [
    "langflow",
    "hrd-docs",
]

SECRET_PATTERNS = [
    r"AIza[0-9A-Za-z_-]{20,}",
    r"sk-[A-Za-z0-9_-]{20,}",
    r"ghp_[A-Za-z0-9]{20,}",
    r"glpat-[A-Za-z0-9_-]{20,}",
    r"(?i)gemini[_-]?api[_-]?key\s*=\s*['\"]?[A-Za-z0-9_\-]+",
    r"(?i)langflow[_-]?api[_-]?key\s*=\s*['\"]?[A-Za-z0-9_\-]+",
    r"(?i)telegram[_-]?bot[_-]?token\s*=\s*['\"]?[A-Za-z0-9:_\-]+",
]

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".env",
    ".txt",
    ".cfg",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
}

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".streamlit",
}

# ============================================================
# HELPERS
# ============================================================

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def run_command(command: list[str]) -> tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return result.returncode, output
    except Exception as exc:
        return 1, str(exc)

def add_result(results: dict, name: str, status: str, detail: str, evidence=None):
    results[name] = {
        "status": status,
        "detail": detail,
        "evidence": evidence or [],
    }

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def iter_text_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_EXTENSIONS:
            yield path

# ============================================================
# AUDIT 1 — REPOSITORY
# ============================================================
def audit_repository(root: Path, results: dict):
    missing_files = []
    missing_dirs = []
    for item in EXPECTED_FILES:
        if not (root / item).exists():
            missing_files.append(item)
    for item in EXPECTED_DIRS:
        if not (root / item).is_dir():
            missing_dirs.append(item)
    if not missing_files and not missing_dirs:
        add_result(results, "repository_structure", "PASS", "Expected AMAZON repository structure is present.", EXPECTED_FILES + EXPECTED_DIRS)
    else:
        add_result(results, "repository_structure", "FAIL", "Expected repository components are missing.", {"missing_files": missing_files, "missing_dirs": missing_dirs})

# ============================================================
# AUDIT 2 — GIT
# ============================================================
def audit_git(root: Path, results: dict):
    if not (root / ".git").exists():
        add_result(results, "git_repository", "WARN", "Directory does not appear to be a Git repository.")
        return
    _, branch = run_command(["git", "-C", str(root), "branch", "--show-current"])
    _, commit = run_command(["git", "-C", str(root), "rev-parse", "--short", "HEAD"])
    _, remote = run_command(["git", "-C", str(root), "remote", "-v"])
    add_result(results, "git_repository", "PASS", "Git repository detected.", {"branch": branch, "commit": commit, "remote": remote})

# ============================================================
# AUDIT 3 — README
# ============================================================
def audit_readme(root: Path, results: dict):
    path = root / "README.md"
    if not path.exists():
        add_result(results, "readme", "FAIL", "README.md not found.")
        return
    content = read_text(path)
    keywords = {"Langflow": "langflow", "Streamlit": "streamlit", "Cloud Run": "cloud run", "IBM Bob": "ibm", "MCP": "mcp", "RAG": "rag"}
    found = [name for name, kw in keywords.items() if kw.lower() in content.lower()]
    missing = [name for name in keywords if name not in found]
    status = "PASS" if len(found) >= 4 else "WARN"
    add_result(results, "readme_architecture_claims", status, "README technology claims inspected.", {"found": found, "missing": missing})

# ============================================================
# AUDIT 4 — ARCHITECTURE
# ============================================================
def audit_architecture(root: Path, results: dict):
    path = root / "ARCHITECTURE.md"
    if not path.exists():
        add_result(results, "architecture_document", "WARN", "ARCHITECTURE.md not found.")
        return
    content = read_text(path)
    required = ["Streamlit", "Langflow", "Cloud Run", "MCP"]
    found = [x for x in required if x.lower() in content.lower()]
    add_result(results, "architecture_document", "PASS" if len(found) >= 3 else "WARN", "Architecture document inspected.", {"required_components": required, "found": found})

# ============================================================
# AUDIT 5 — LANGFLOW
# ============================================================
def audit_langflow(root: Path, results: dict):
    langflow_dir = root / "langflow"
    if not langflow_dir.exists():
        add_result(results, "langflow", "FAIL", "langflow directory not found.")
        return
    json_files = list(langflow_dir.rglob("*.json"))
    if not json_files:
        add_result(results, "langflow", "WARN", "Langflow directory exists but no JSON flow was found.")
        return
    valid, invalid = [], []
    for path in json_files:
        try:
            data = json.loads(read_text(path))
            if isinstance(data, dict):
                valid.append(str(path.relative_to(root)))
            else:
                invalid.append(str(path.relative_to(root)))
        except Exception:
            invalid.append(str(path.relative_to(root)))
    add_result(results, "langflow", "PASS" if valid else "FAIL", "Langflow JSON flow audit completed.", {"valid_flows": valid, "invalid_flows": invalid})

# ============================================================
# AUDIT 6 — STREAMLIT
# ============================================================
def audit_streamlit(root: Path, results: dict):
    path = root / "streamlit_app.py"
    if not path.exists():
        add_result(results, "streamlit", "FAIL", "streamlit_app.py not found.")
        return
    content = read_text(path)
    indicators = {"streamlit": "import streamlit", "HTTP": "requests", "Langflow": "langflow", "API": "api"}
    found = [key for key, val in indicators.items() if val.lower() in content.lower()]
    add_result(results, "streamlit", "PASS", "Streamlit application detected.", {"file": str(path), "indicators": found})

# ============================================================
# AUDIT 7 — REQUIREMENTS
# ============================================================
def audit_requirements(root: Path, results: dict):
    candidates = [root / "requirements.txt", root / "pyproject.toml", root / "Pipfile"]
    existing = [p for p in candidates if p.exists()]
    if not existing:
        add_result(results, "dependencies", "WARN", "No standard Python dependency manifest found.")
        return
    evidence = []
    for path in existing:
        content = read_text(path)
        for package in ["streamlit", "requests", "langflow", "mcp"]:
            if package.lower() in content.lower():
                evidence.append({"file": str(path.relative_to(root)), "package": package})
    add_result(results, "dependencies", "PASS", "Dependency manifests detected.", evidence)

# ============================================================
# AUDIT 8 — SECRET LEAKAGE
# ============================================================
def audit_secrets(root: Path, results: dict):
    findings = []
    for path in iter_text_files(root):
        content = read_text(path)
        for pattern in SECRET_PATTERNS:
            try:
                matches = re.findall(pattern, content)
            except re.error:
                continue
            if matches:
                findings.append({"file": str(path.relative_to(root)), "pattern": pattern, "count": len(matches)})
    if findings:
        add_result(results, "secret_leakage", "FAIL", "Potential credential/API-key leakage detected.", findings)
    else:
        add_result(results, "secret_leakage", "PASS", "No obvious hard-coded credentials detected by heuristic scan.")

# ============================================================
# AUDIT 9 — ENVIRONMENT VARIABLES
# ============================================================
def audit_environment(root: Path, results: dict):
    files = list(root.rglob(".env*"))
    tracked = []
    for path in files:
        if ".git" in path.parts:
            continue
        if path.is_file():
            tracked.append(str(path.relative_to(root)))
    gitignore = root / ".gitignore"
    protected = False
    if gitignore.exists():
        content = read_text(gitignore)
        protected = (".env" in content or "*.env" in content)
    add_result(results, "environment_security", "PASS" if protected else "WARN", "Environment configuration inspected.", {"env_files": tracked, "gitignore_protection": protected})

# ============================================================
# AUDIT 10 — MCP
# ============================================================
def audit_mcp(root: Path, results: dict):
    candidates = [root / ".bob" / "mcp.json", root / "mcp.json"]
    found = []
    for path in candidates:
        if path.exists():
            try:
                data = json.loads(read_text(path))
                found.append({"file": str(path.relative_to(root)), "valid_json": True, "keys": list(data.keys()) if isinstance(data, dict) else []})
            except Exception:
                found.append({"file": str(path.relative_to(root)), "valid_json": False})
    if found:
        add_result(results, "mcp", "PASS", "MCP configuration detected.", found)
    else:
        add_result(results, "mcp", "WARN", "No MCP configuration file detected.")

# ============================================================
# AUDIT 11 — HRD DOCUMENTS
# ============================================================
def audit_documents(root: Path, results: dict):
    doc_dir = root / "hrd-docs"
    if not doc_dir.exists():
        add_result(results, "hrd_documents", "FAIL", "hrd-docs directory not found.")
        return
    documents = [p for p in doc_dir.rglob("*") if p.is_file()]
    extensions = {}
    for path in documents:
        ext = path.suffix.lower() or "[no extension]"
        extensions[ext] = extensions.get(ext, 0) + 1
    add_result(results, "hrd_documents", "PASS" if documents else "WARN", "HRD document corpus inspected.", {"document_count": len(documents), "extensions": extensions})

# ============================================================
# AUDIT 12 — PERSISTENCE
# ============================================================
def audit_persistence(root: Path, results: dict):
    content = ""
    for filename in ["README.md", "ARCHITECTURE.md"]:
        path = root / filename
        if path.exists():
            content += "\n" + read_text(path)
    persistence_keywords = ["persistent", "persistence", "volume", "cloud storage", "database", "vector store", "firestore", "postgres", "qdrant"]
    found = [kw for kw in persistence_keywords if kw.lower() in content.lower()]
    status = "WARN"
    if any(kw in found for kw in ["volume", "database", "firestore", "postgres", "qdrant"]):
        status = "PASS"
    add_result(results, "persistence", status, "Persistence architecture indicators inspected.", found)

# ============================================================
# AUDIT 13 — URL HEALTH
# ============================================================
def check_url(url: str):
    try:
        request = urllib.request.Request(url, method="GET", headers={"User-Agent": "AMAZON-Audit/1.0"})
        with urllib.request.urlopen(request, timeout=15) as response:
            return {"url": url, "status_code": response.status, "reachable": True}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status_code": exc.code, "reachable": False}
    except Exception as exc:
        return {"url": url, "reachable": False, "error": str(exc)}

def audit_endpoints(root: Path, results: dict):
    readme = root / "README.md"
    if not readme.exists():
        add_result(results, "endpoints", "WARN", "README unavailable; endpoint discovery skipped.")
        return
    content = read_text(readme)
    urls = sorted(set(re.findall(r"https?://[^\s<>)]+", content)))
    health = []
    for url in urls:
        url = url.rstrip(".,;")
        if "streamlit.app" in url or "run.app" in url:
            health.append(check_url(url))
    add_result(results, "endpoints", "PASS" if health else "WARN", "Public endpoint health checks completed.", health)

# ============================================================
# AUDIT 14 — PYTHON SYNTAX
# ============================================================
def audit_python_syntax(root: Path, results: dict):
    failures = []
    python_files = list(root.rglob("*.py"))
    for path in python_files:
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        code, output = run_command([sys.executable, "-m", "py_compile", str(path)])
        if code != 0:
            failures.append({"file": str(path.relative_to(root)), "error": output[-1000:]})
    add_result(results, "python_syntax", "PASS" if not failures else "FAIL", "Python syntax validation completed.", {"python_files_checked": len(python_files), "failures": failures})

# ============================================================
# SCORE
# ============================================================
def calculate_score(results: dict):
    weights = {"PASS": 100, "WARN": 60, "FAIL": 0}
    values = [weights.get(r["status"], 0) for r in results.values()]
    return round(sum(values) / len(values), 2) if values else 0

# ============================================================
# MARKDOWN REPORT
# ============================================================
def generate_markdown(report: dict):
    lines = []
    lines.append("# AMAZON — Automated Audit Report")
    lines.append("")
    lines.append(f"Generated: `{report['generated_at']}`")
    lines.append("")
    lines.append(f"Repository: `{report['repository']}`")
    lines.append("")
    lines.append("## Overall Score")
    lines.append("")
    lines.append(f"**{report['score']}/100**")
    lines.append("")
    lines.append("## Audit Results")
    lines.append("")
    lines.append("| Audit | Status | Detail |")
    lines.append("|---|---|---|")
    for name, result in report["audits"].items():
        detail = result["detail"].replace("\n", " ").replace("|", "\\|")
        lines.append(f"| `{name}` | **{result['status']}** | {detail} |")
    lines.append("")
    lines.append("## Evidence")
    lines.append("")
    for name, result in report["audits"].items():
        lines.append(f"### {name}")
        evidence = result.get("evidence", [])
        if not evidence:
            lines.append("No additional evidence.")
        else:
            lines.append("```json")
            lines.append(json.dumps(evidence, indent=2, ensure_ascii=False))
            lines.append("```")
        lines.append("")
    lines.append("## Scientific/Production Interpretation")
    lines.append("")
    score = report["score"]
    if score >= 90:
        lines.append("AMAZON is structurally strong and suitable for advanced validation. Remaining work should focus on empirical RAG quality and production verification.")
    elif score >= 75:
        lines.append("AMAZON has a strong foundation but requires targeted technical validation before being considered production‑ready.")
    elif score >= 50:
        lines.append("AMAZON is partially operational but has important technical or reproducibility gaps.")
    else:
        lines.append("AMAZON requires significant remediation before production or scientific evaluation.")
    lines.append("")
    return "\n".join(lines)

# ============================================================
# MAIN
# ============================================================
def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ROOT).resolve()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    results = {}
    print("=" * 80)
    print("AMAZON — AUTOMATED TECHNICAL & RAG AUDIT")
    print("=" * 80)
    print()
    print(f"Repository: {root}")
    print()
    audit_repository(root, results)
    audit_git(root, results)
    audit_readme(root, results)
    audit_architecture(root, results)
    audit_langflow(root, results)
    audit_streamlit(root, results)
    audit_requirements(root, results)
    audit_secrets(root, results)
    audit_environment(root, results)
    audit_mcp(root, results)
    audit_documents(root, results)
    audit_persistence(root, results)
    audit_endpoints(root, results)
    audit_python_syntax(root, results)
    score = calculate_score(results)
    report = {"project": "AMAZON", "repository": REPO_URL, "generated_at": now_iso(), "score": score, "audits": results}
    JSON_REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    MD_REPORT.write_text(generate_markdown(report), encoding="utf-8")
    print("=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    for name, result in results.items():
        print(f"{result['status']:>5} | {name}")
    print()
    print(f"OVERALL SCORE : {score}/100")
    print()
    print(f"JSON REPORT   : {JSON_REPORT}")
    print(f"MARKDOWN      : {MD_REPORT}")
    print()

if __name__ == "__main__":
    main()
