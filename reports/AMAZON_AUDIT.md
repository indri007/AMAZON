# AMAZON — Automated Audit Report

Generated: `2026-10-07T12:58:56.423051+00:00`

Repository: `https://github.com/indri007/AMAZON`

## Overall Score

**100.0/100**

## Audit Results

| Audit | Status | Detail |
|---|---|---|
| `repository_structure` | **PASS** | Expected AMAZON repository structure is present. |
| `git_repository` | **PASS** | Git repository detected. |
| `readme_architecture_claims` | **PASS** | README technology claims inspected. |
| `architecture_document` | **PASS** | Architecture document inspected. |
| `langflow` | **PASS** | Langflow JSON flow audit completed. |
| `streamlit` | **PASS** | Streamlit application detected. |
| `dependencies` | **PASS** | Dependency manifests detected. |
| `secret_leakage` | **PASS** | No obvious hard-coded credentials detected by heuristic scan. |
| `environment_security` | **PASS** | Environment configuration inspected. |
| `mcp` | **PASS** | MCP configuration detected. |
| `hrd_documents` | **PASS** | HRD document corpus inspected. |
| `persistence` | **PASS** | Persistence architecture indicators inspected. |
| `endpoints` | **PASS** | Public endpoint health checks completed. |
| `python_syntax` | **PASS** | Python syntax validation completed. |

## Evidence

### repository_structure
```json
[
  "README.md",
  "streamlit_app.py",
  "langflow",
  "hrd-docs",
  "src/assembly",
  "benchmarks",
  "docs",
  "tests"
]
```

### git_repository
```json
{
  "branch": "main",
  "commit": "8253955",
  "remote": "origin\thttps://github.com/indri007/AMAZON.git (fetch)\norigin\thttps://github.com/indri007/AMAZON.git (push)"
}
```

### readme_architecture_claims
```json
{
  "found": [
    "Langflow",
    "Streamlit",
    "Cloud Run",
    "IBM Bob",
    "MCP",
    "RAG"
  ],
  "missing": []
}
```

### architecture_document
```json
{
  "required_components": [
    "Streamlit",
    "Langflow",
    "Cloud Run",
    "MCP"
  ],
  "found": [
    "Streamlit",
    "Langflow",
    "Cloud Run",
    "MCP"
  ]
}
```

### langflow
```json
{
  "valid_flows": [
    "langflow/Vector Store RAG.json"
  ],
  "invalid_flows": []
}
```

### streamlit
```json
{
  "file": "/Users/jevin/HRD/langflow-bob/streamlit_app.py",
  "indicators": [
    "streamlit",
    "HTTP",
    "Langflow",
    "API"
  ]
}
```

### dependencies
```json
[
  {
    "file": "requirements.txt",
    "package": "streamlit"
  },
  {
    "file": "requirements.txt",
    "package": "requests"
  }
]
```

### secret_leakage
No additional evidence.

### environment_security
```json
{
  "env_files": [
    ".env.example",
    "remind_kas/.env.example",
    "Sistem-Informasi-Sekolah/.env.example",
    "Sistem-Informasi-Akademik-Sekolah-Laravel/.env.example",
    ".kilo/worktrees/petite-asparagus/.env.example"
  ],
  "gitignore_protection": true
}
```

### mcp
```json
[
  {
    "file": ".bob/mcp.json",
    "valid_json": true,
    "keys": [
      "mcpServers"
    ]
  }
]
```

### hrd_documents
```json
{
  "document_count": 185,
  "extensions": {
    ".zip": 2,
    "[no extension]": 1,
    ".md": 9,
    ".doc": 105,
    ".docx": 10,
    ".xls": 16,
    ".pptx": 6,
    ".xlsx": 21,
    ".pdf": 1,
    ".db": 3,
    ".ppt": 11
  }
}
```

### persistence
```json
[
  "persistent",
  "persistence",
  "volume",
  "cloud storage",
  "database",
  "vector store",
  "qdrant"
]
```

### endpoints
```json
[
  {
    "url": "https://indri007-langflow-bob.streamlit.app",
    "status_code": 303,
    "reachable": false
  },
  {
    "url": "https://langflow-192433070716.asia-southeast2.run.app/api/v1/mcp/project/a2a1a234-0b47-4007-a4e7-1d8fec7b3ebf/streamable\"",
    "status_code": 500,
    "reachable": false
  },
  {
    "url": "https://langflow-192433070716.asia-southeast2.run.app`",
    "reachable": false,
    "error": "<urlopen error [Errno 8] nodename nor servname provided, or not known>"
  },
  {
    "url": "https://langflow-bob-idewcrvkhn3lsxjcnw4pqn.streamlit.app",
    "status_code": 303,
    "reachable": false
  }
]
```

### python_syntax
```json
{
  "python_files_checked": 24,
  "failures": []
}
```

## Scientific/Production Interpretation

AMAZON is structurally strong and suitable for advanced validation. Remaining work should focus on empirical RAG quality and production verification.
