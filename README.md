# AMAZON — Autonomous Multi-Agent Zero-Shot Orchestration & RAG Benchmark

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://indri007-langflow-bob.streamlit.app)
[![Tests](https://img.shields.io/badge/Unit%20Tests-16%20Passed-success.svg)](file:///Users/jevin/HRD/langflow-bob/tests)
[![Score](https://img.shields.io/badge/Technical%20Audit-100%2F100-brightgreen.svg)](file:///Users/jevin/HRD/langflow-bob/reports/AMAZON_AUDIT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](file:///Users/jevin/HRD/langflow-bob/LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Enterprise-grade **Autonomous Multi-Agent Zero-Shot Orchestration** and **Retrieval-Augmented Generation (RAG) Benchmark** platform. AMAZON integrates Langflow vector workflows, Google Cloud Run microservices, and IBM Bob via the Model Context Protocol (MCP) — backed by an ARM64 low-level bitmask engine, a 185-document HR knowledge base, and an empirical RAGAS / Q1 publication benchmark suite.

---

## 📌 Executive Summary

**AMAZON** bridges high-level agentic LLM orchestration with low-level execution speed and scientific validation:
1. **Multi-Agent RAG Orchestration**: A 6-agent cooperative architecture (Router, Query Reformulation, Retrieval Grounding, CS Responder, HRD Interviewer, and Evaluator) built on Langflow and deployed to Google Cloud Run.
2. **Standardized Protocol (MCP)**: Seamless inter-agent tool invocation via Model Context Protocol (`mcp-proxy` Streamable HTTP) connecting IBM Bob to backend vector stores.
3. **Low-Level Bitmask Engine**: High-performance ARM64 assembly (`src/assembly/angsuran_bitmask.asm`) tracking 10-period installment registers (`0x03FF`) with zero runtime allocation overhead.
4. **Empirical Benchmark Suite**: Publication-grade evaluation suite (`benchmarks/q1_benchmark_suite.py`) testing across $N=110$ golden QA samples with paired t-tests, 95% bootstrap confidence intervals, and Cohen's $d$ effect sizes.
5. **Interactive Frontend**: Production Streamlit application connected to cloud endpoints with fallback recovery.

---

## 🔗 Live Links & Endpoints

| Resource | Target / URL | Status |
|---|---|---|
| **3D Architecture Showcase (Interactive UI/UX)** | [`showcase/index.html`](file:///Users/jevin/HRD/langflow-bob/showcase/index.html) | Ready (WebGL / Three.js) |
| **Streamlit App (Interactive Web UI)** | [indri007-langflow-bob.streamlit.app](https://indri007-langflow-bob.streamlit.app) | Production |
| **Langflow Microservice (Cloud Run)** | `https://langflow-192433070716.asia-southeast2.run.app` | Active (`asia-southeast2`) |
| **GitHub Repository** | [github.com/indri007/AMAZON](https://github.com/indri007/AMAZON) | Main Branch |
| **System Architecture Spec** | [`docs/ARCHITECTURE.md`](file:///Users/jevin/HRD/langflow-bob/docs/ARCHITECTURE.md) | Technical Specification |
| **Entity Relationship Model** | [`docs/ERD.md`](file:///Users/jevin/HRD/langflow-bob/docs/ERD.md) | Schema & Data Dictionary |
| **Persistence & Scaling Plan** | [`docs/PERSISTENCE_PLAN.md`](file:///Users/jevin/HRD/langflow-bob/docs/PERSISTENCE_PLAN.md) | Chroma & Cloud SQL |
| **Research References** | [`docs/papers/ReceiptSense_2406.04493.pdf`](file:///Users/jevin/HRD/langflow-bob/docs/papers/ReceiptSense_2406.04493.pdf) | Academic Base |

---

## 🗂️ Clean Repository Structure

```
AMAZON/
├── benchmarks/                         # Multi-Agent RAG evaluation & audit suite
│   ├── golden_dataset.json             # Canonical QA ground-truth (N=110)
│   ├── golden_dataset_expanded_110.json# Expanded test corpus
│   ├── q1_benchmark_suite.py           # Statistical validation (t-test, CI, Cohen's d)
│   ├── ragas_eval.py                   # RAGAS metric pipeline (faithfulness, precision)
│   ├── amazon_audit.py                 # Automated 14-point technical & structural audit
│   └── q1_publication_report.json      # Published benchmark findings
├── src/
│   └── assembly/                       # Low-level ARM64 assembly & register bitmask
│       ├── angsuran_bitmask.asm        # ARM64 assembly 16-bit installment tracker
│       ├── audit_assembly.c            # C test harness & bitwise verification
│       ├── audit_assembly.s            # Compiled assembly listing
│       ├── check_solve_assembly.c      # Assembly validator
│       ├── test_angsuran_arm64.c       # ARM64 test runner
│       └── angsuran_bitmask.py         # Native bitmask Python implementation
├── hrd-docs/                           # Corporate knowledge corpus (185 documents)
│   ├── tools_hrd/                      # Structured tools: SOP, KPI, Salary Grade, etc.
│   │   ├── Tools 1 - SOP HRD/
│   │   ├── Tools 2 - Kamus Kompetensi/
│   │   ├── Tools 3 - Pedoman Perilaku/
│   │   ├── Tools 4 - Job Description/
│   │   ├── Tools 5 - Training Plan dan Modul Training/
│   │   ├── Tools 6 - Competency-based Interview/
│   │   ├── Tools 7 - Salary Grade/
│   │   ├── Tools 8 - Katalog KPI/
│   │   ├── Tools 9 - Program Strategis HR/
│   │   └── Tools 10 - Employee Retention/
│   ├── faq_hrd.md                      # Canonical HR FAQ knowledge base
│   └── prompts/                        # System prompts for 6 specialized agents
├── langflow/
│   └── Vector Store RAG.json           # Declarative Langflow multi-agent flow
├── docs/                               # Engineering documentation & papers
│   ├── ARCHITECTURE.md                 # Full architectural specification
│   ├── ERD.md                          # Entity relationship diagram
│   ├── PERSISTENCE_PLAN.md             # Vector store persistence strategy
│   ├── design.md / rules.md / schema.md# Architectural decisions & conventions
│   └── papers/                         # Research literature (ReceiptSense)
├── tests/                              # Automated unit test suite (16 tests)
│   ├── test_golden_dataset.py          # Ground-truth schema & diversity validation
│   ├── test_bitmask_register.py        # ARM64 bitmask register verification
│   ├── test_langflow_integration.py    # Langflow node & edge integrity
│   └── test_evaluation_metrics.py      # Statistical evaluation mathematics
├── reports/                            # Generated audit & benchmark reports
│   ├── AMAZON_AUDIT.json               # Structured audit output
│   └── AMAZON_AUDIT.md                 # Markdown audit report
├── showcase/                           # Standalone 3D WebGL Multi-Agent Showcase
│   └── index.html                      # Three.js 3D Orchestration UI/UX
├── .bob/
│   ├── mcp.json                        # MCP server definitions
│   └── mcp.json.example                # MCP template configuration
├── server.py                           # Cloud Run HTTP & Telemetry Server
├── angsuran_bitmask.py                 # Backward-compatibility re-export wrapper
├── streamlit_app.py                    # Streamlit interactive application
├── Dockerfile                          # Cloud Run container definition (Port 8080)
├── requirements.txt                    # Project dependencies
└── README.md                           # Documentation root
```

---

## 🏗️ System Architecture

```
                               ┌────────────────────────────────┐
                               │       User / Evaluator         │
                               └───────┬────────────────┬───────┘
                                       │                │
                        HTTP Streamlit │                │ MCP Protocol
                                       ▼                ▼
                     ┌───────────────────┐    ┌───────────────────┐
                     │  Streamlit Cloud  │    │      IBM Bob      │
                     │  Interactive UI   │    │   (MCP Client)    │
                     └─────────┬─────────┘    └─────────┬─────────┘
                               │                        │ uvx mcp-proxy@0.9.0
                               │ POST /api/v1/run/...   │ Streamable HTTP
                               └───────────┬────────────┘
                                           ▼
                 ┌──────────────────────────────────────────────────┐
                 │       Langflow Microservice (Cloud Run)          │
                 │        asia-southeast2, Gemini 2.0 Flash         │
                 └─────────────────────────┬────────────────────────┘
                                           │
         ┌─────────────────────────────────┴─────────────────────────────────┐
         ▼                                 ▼                                 ▼
┌───────────────────┐             ┌───────────────────┐             ┌───────────────────┐
│ Agent 1: Router   │             │ Agent 2: Query    │             │ Agent 3: Grounding│
│ Intent triage     │ ──────────► │ Reformulation     │ ──────────► │ Vector retrieval  │
└───────────────────┘             └───────────────────┘             └─────────┬─────────┘
                                                                              │
         ┌────────────────────────────────────────────────────────────────────┘
         ▼                                 ▼
┌───────────────────┐             ┌───────────────────┐
│ Agent 4 / 5:      │             │ Agent 6: Evaluator│
│ Response Gen      │ ──────────► │ Hallucination     │
│ (CS / HRD)        │             │ Verification      │
└───────────────────┘             └───────────────────┘
```

---

## ⚙️ Core Modules

### 1. Multi-Agent RAG Pipeline
- **Router Agent**: Analyzes incoming query semantics, classifying queries into HR Policy, SOP Guidelines, Installment Financials, or General Inquiry.
- **Query Reformulator**: Expands user prompts into dense semantic query terms tailored for embedding lookup.
- **Retrieval Grounding**: Queries 3072-dimensional vector spaces generated by `gemini-embedding-2`.
- **Evaluator Agent**: Performs real-time groundedness checks to prevent hallucinated answers before returning text to users.

### 2. ARM64 16-Bit Register Bitmask Engine
- **Hardware Register**: 16-bit unsigned integer (`uint16_t`).
- **Installment Tracking**: Tracks 10 discrete installments (Bits 0–9).
- **Settlement Mask (`0x03FF`)**: $2^{10} - 1 = 1023$, representing complete loan settlement (*Lunas*).
- **Zero-Allocation**: Can be executed via compiled native ARM64 assembly or Python ctypes binding.

### 3. Empirical Q1 Benchmark Suite
- **Dataset**: $N=110$ high-quality human-verified QA pairs covering all 10 HR tools and policies.
- **Statistical Significance**: Paired Student's t-test and Wilcoxon signed-rank test.
- **Effect Size**: Cohen's $d$ calculation.
- **Confidence Intervals**: 95% bootstrap confidence bounds across:
  - Context Precision: $\ge 0.85$ (AMAZON target: $0.92$)
  - Context Recall: $\ge 0.85$ (AMAZON target: $0.89$)
  - Faithfulness: $\ge 0.90$ (AMAZON target: $0.94$)
  - Answer Relevancy: $\ge 0.88$ (AMAZON target: $0.93$)

---

## 🧪 Testing & Verification

AMAZON includes a comprehensive unit testing suite in `tests/` covering dataset schema, ARM64 register mathematics, Langflow flow integrity, and statistical metrics.

### Run Unit Tests
```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

**Output:**
```
test_full_payment_lunas_status (test_bitmask_register.TestBitmaskRegister.test_full_payment_lunas_status) ... ok
test_initial_register_state (test_bitmask_register.TestBitmaskRegister.test_initial_register_state) ... ok
test_invalid_installment_index (test_bitmask_register.TestBitmaskRegister.test_invalid_installment_index) ... ok
test_partial_payments (test_bitmask_register.TestBitmaskRegister.test_partial_payments) ... ok
test_single_payment (test_bitmask_register.TestBitmaskRegister.test_single_payment) ... ok
test_cohens_d_effect_size (test_evaluation_metrics.TestEvaluationMetrics.test_cohens_d_effect_size) ... ok
test_confidence_interval_bounds (test_evaluation_metrics.TestEvaluationMetrics.test_confidence_interval_bounds) ... ok
test_improvement_percent_calculation (test_evaluation_metrics.TestEvaluationMetrics.test_improvement_percent_calculation) ... ok
test_metrics_targets_structure (test_evaluation_metrics.TestEvaluationMetrics.test_metrics_targets_structure) ... ok
test_golden_dataset_base_exists_and_valid (test_golden_dataset.TestGoldenDataset.test_golden_dataset_base_exists_and_valid) ... ok
test_golden_dataset_diversity (test_golden_dataset.TestGoldenDataset.test_golden_dataset_diversity) ... ok
test_golden_dataset_expanded_sample_size (test_golden_dataset.TestGoldenDataset.test_golden_dataset_expanded_sample_size) ... ok
test_golden_dataset_required_fields (test_golden_dataset.TestGoldenDataset.test_golden_dataset_required_fields) ... ok
test_flow_contains_data_nodes (test_langflow_integration.TestLangflowIntegration.test_flow_contains_data_nodes) ... ok
test_flow_contains_rag_components (test_langflow_integration.TestLangflowIntegration.test_flow_contains_rag_components) ... ok
test_flow_file_exists_and_valid_json (test_langflow_integration.TestLangflowIntegration.test_flow_file_exists_and_valid_json) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.005s

OK
```

### Run 14-Point Automated Audit
```bash
python3 benchmarks/amazon_audit.py
```

Generates detailed audit logs and scoring summary in `reports/AMAZON_AUDIT.md` and `reports/AMAZON_AUDIT.json`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`
- Optional: `uv` / `uvx` for MCP proxy execution

### Running the Benchmark Suite
```bash
python3 benchmarks/q1_benchmark_suite.py
```

### Running 3D Architecture Showcase Locally
```bash
python3 server.py
# Buka di browser: http://localhost:8080 (atau buka langsung file showcase/index.html)
```

### Deploy ke Google Cloud Run (via Cloud Shell)
Jalankan langkah ini langsung di terminal **Google Cloud Shell** (`g25067020011@cloudshell:~$`):

```bash
# 1. Cek & pilih project Google Cloud Anda
gcloud projects list
gcloud config set project [PROJECT_ID_ANDA]

# 2. Clone repository AMAZON & masuk ke direktori
git clone https://github.com/indri007/AMAZON.git
cd AMAZON

# 3. Deploy langsung ke Cloud Run
gcloud run deploy amazon-showcase \
  --source . \
  --region asia-southeast2 \
  --allow-unauthenticated \
  --port 8080
```

### Running Streamlit Locally
```bash
streamlit run streamlit_app.py
```

### IBM Bob MCP Integration
Add the following to `.bob/mcp.json`:
```json
{
  "mcpServers": {
    "lf-cloudrun": {
      "command": "uvx",
      "args": [
        "mcp-proxy@0.9.0",
        "--transport",
        "streamablehttp",
        "--header",
        "x-api-key:<LANGFLOW_API_KEY_CLOUDRUN>",
        "https://langflow-192433070716.asia-southeast2.run.app/api/v1/mcp/project/a2a1a234-0b47-4007-a4e7-1d8fec7b3ebf/streamable"
      ]
    }
  }
}
```

---

## 📄 License

This project is licensed under the MIT License — see the [`LICENSE`](file:///Users/jevin/HRD/langflow-bob/LICENSE) file for details.
