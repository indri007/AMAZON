import streamlit as st
import requests
import json
import re
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AMAZON — Asisten HRD Virtual & Multi-Agent RAG",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        color-scheme: light;
    }
    .stApp {
        background: #F8FAFC;
    }
    .header-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-radius: 24px;
        padding: 26px 32px;
        margin-bottom: 20px;
        color: #FFFFFF;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .header-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 8px;
        background: linear-gradient(to right, #38BDF8, #818CF8, #34D399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .header-subtitle {
        font-size: 15px;
        color: #94A3B8;
        line-height: 1.6;
    }
    .badge-chip {
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-family: monospace;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 10px;
    }
    .badge-cyan { background: rgba(56, 189, 248, 0.15); color: #38BDF8; border: 1px solid rgba(56, 189, 248, 0.3); }
    .badge-emerald { background: rgba(52, 211, 153, 0.15); color: #34D399; border: 1px solid rgba(52, 211, 153, 0.3); }
    .badge-purple { background: rgba(168, 85, 247, 0.15); color: #C084FC; border: 1px solid rgba(168, 85, 247, 0.3); }

    .sidebar-card {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(16, 42, 67, 0.05);
        border: 1px solid #E2E8F0;
    }
    .sidebar-title {
        color: #0F172A;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .chat-area {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 12px 36px rgba(16, 42, 67, 0.06);
        border: 1px solid #E2E8F0;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        font-family: monospace;
    }
    .status-online { background: #DCFCE7; color: #166534; border: 1px solid #86EFAC; }
    .status-offline { background: #FEF3C7; color: #92400E; border: 1px solid #FCD34D; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Config ───────────────────────────────────────────────────────────────────
DEFAULT_LANGFLOW_URL = st.secrets.get("LANGFLOW_URL", "https://langflow-192433070716.asia-southeast2.run.app")
FLOW_ID = st.secrets.get("FLOW_ID", "d8eedd75-92a7-47f0-974a-b74c0062ea23")
API_KEY = st.secrets.get("LANGFLOW_API_KEY", "")

# ── Local Knowledge Base Loader (Fallback) ───────────────────────────────────
@st.cache_data
def load_local_faq():
    faq_path = Path(__file__).resolve().parent / "hrd-docs" / "faq_hrd.md"
    if not faq_path.exists():
        return []
    content = faq_path.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"\n\*\*Q:\s*", content)
    for b in blocks[1:]:
        parts = re.split(r"\n\s*A:\s*", b, maxsplit=1)
        if len(parts) == 2:
            q = parts[0].strip().rstrip("*?")
            a = parts[1].strip()
            entries.append((q, a))
    return entries

FAQ_ENTRIES = load_local_faq()

def search_local_faq(question: str) -> str | None:
    q_lower = question.lower()
    
    # 1. Exact or keyword matching
    for q, a in FAQ_ENTRIES:
        keywords = [w for w in re.findall(r"\w+", q.lower()) if len(w) > 3]
        match_count = sum(1 for kw in keywords if kw in q_lower)
        if match_count >= 2 or q.lower() in q_lower:
            return f"**Pertanyaan Terkait:** {q}?\n\n{a}"

    # 2. General Intent Fallback
    if any(k in q_lower for k in ["cuti", "libur", "izin"]):
        for q, a in FAQ_ENTRIES:
            if "cuti tahunan" in q.lower():
                return f"**Kebijakan Cuti:**\n\n{a}"
    elif any(k in q_lower for k in ["training", "pelatihan", "kursus"]):
        for q, a in FAQ_ENTRIES:
            if "training" in q.lower():
                return f"**Kebijakan Training:**\n\n{a}"
    elif any(k in q_lower for k in ["kpi", "appraisal", "kinerja"]):
        for q, a in FAQ_ENTRIES:
            if "kpi" in q.lower():
                return f"**Kebijakan Kinerja & KPI:**\n\n{a}"
    elif any(k in q_lower for k in ["gaji", "salary", "upah", "benefit"]):
        for q, a in FAQ_ENTRIES:
            if "gaji" in q.lower():
                return f"**Kebijakan Gaji & Kompensasi:**\n\n{a}"
    elif any(k in q_lower for k in ["promosi", "jabatan", "karir"]):
        for q, a in FAQ_ENTRIES:
            if "promosi" in q.lower():
                return f"**Syarat & Ketentuan Promosi:**\n\n{a}"
    elif "wawancara" in q_lower or "interview" in q_lower:
        return (
            "**Simulasi Wawancara Competency-Based Interview (CBI):**\n\n"
            "Halo! Silakan ceritakan pengalaman kerja Anda menggunakan teknik **STAR**:\n"
            "- **S (Situation)**: Jelaskan situasi atau proyek yang pernah Anda hadapi.\n"
            "- **T (Task)**: Apa tanggung jawab spesifik Anda saat itu?\n"
            "- **A (Action)**: Langkah konkret apa yang Anda ambil untuk menyelesaikan tantangan tersebut?\n"
            "- **R (Result)**: Apa hasil terukur atau pelajaran yang Anda dapatkan?"
        )
    return None

# ── Health Check ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=20)
def check_langflow_health(url: str):
    try:
        r = requests.get(url, timeout=3)
        return r.status_code == 200, r.status_code
    except Exception:
        return False, 0

# ── Ask Langflow or Fallback ─────────────────────────────────────────────────
def ask_assistant(question: str, session_id: str, active_url: str) -> str:
    langflow_api = f"{active_url.rstrip('/')}/api/v1/run/{FLOW_ID}?stream=false"
    headers = {"Content-Type": "application/json"}
    if API_KEY:
        headers["x-api-key"] = API_KEY

    payload = {
        "input_value": question,
        "output_type": "chat",
        "input_type": "chat",
        "session_id": session_id,
    }

    try:
        resp = requests.post(langflow_api, json=payload, headers=headers, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            outputs = data.get("outputs", [])
            for out in outputs:
                for result in out.get("outputs", []):
                    msg = result.get("results", {}).get("message", {})
                    text = msg.get("text") or msg.get("data", {}).get("text", "")
                    if text:
                        return text
    except Exception:
        pass

    # Intelligent Knowledge Fallback
    local_answer = search_local_faq(question)
    if local_answer:
        return (
            f"{local_answer}\n\n"
            f"---\n"
            f"*💡 Mode Pengetahuan Lokal: Disajikan dari Basis Pengetahuan SOP & FAQ HRD resmi.*"
        )

    return (
        "Maaf, pertanyaan Anda belum dapat diproses oleh model saat ini. "
        "Silakan ajukan pertanyaan seputar cuti tahunan, pelatihan, KPI, struktur gaji, atau latihan wawancara CBI."
    )

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# ── UI Header ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class='header-card'>
        <div class='header-title'>AMAZON — Asisten HRD Virtual & Multi-Agent RAG</div>
        <div class='header-subtitle'>
            Platform Orkestrasi Multi-Agen Cerdas & Retrieval-Augmented Generation untuk Kebijakan SDM, SOP Perusahaan, dan Simulasi Kompetensi.
        </div>
        <div>
            <span class='badge-chip badge-cyan'>Multi-Agent RAG</span>
            <span class='badge-chip badge-emerald'>Audit 100/100</span>
            <span class='badge-chip badge-purple'>ARM64 0x03FF Bitmask</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1, 2], gap="large")

with left_col:
    # Service Connectivity Card
    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>⚡ Status Layanan</div>", unsafe_allow_html=True)
    
    is_live, code = check_langflow_health(DEFAULT_LANGFLOW_URL)
    if is_live:
        st.markdown(
            "<div class='status-pill status-online'>🟢 Langflow Online (Cloud Run)</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='status-pill status-offline'>🟠 Langflow Standby (Auto-Fallback Aktif)</div>",
            unsafe_allow_html=True
        )
        st.caption("Jawaban tetap responsif menggunakan basis pengetahuan internal SOP & FAQ HRD.")
    
    st.markdown("<hr style='border-color: #E2E8F0; margin: 16px 0;'>", unsafe_allow_html=True)
    
    # 3D Showcase Link
    st.markdown("<div class='sidebar-title'>🌌 3D Orchestration</div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 13px; color: #64748B;'>Eksplorasi visualisasi 3D WebGL Multi-Agent Network, chip ARM64 bitmask, dan HUD telemetri:</p>", unsafe_allow_html=True)
    st.link_button("🚀 Buka 3D Architecture Showcase", "https://github.com/indri007/AMAZON/blob/main/showcase/index.html", use_container_width=True)

    st.markdown("<hr style='border-color: #E2E8F0; margin: 16px 0;'>", unsafe_allow_html=True)

    # Prompt Examples
    st.markdown("<div class='sidebar-title'>💡 Contoh Pertanyaan</div>", unsafe_allow_html=True)
    examples = [
        "Berapa hari cuti tahunan saya?",
        "Bagaimana cara mengajukan training?",
        "Apa syarat promosi jabatan?",
        "Jelaskan proses performance appraisal dan KPI",
        "Saya mau latihan wawancara HRD",
    ]

    for idx, ex in enumerate(examples):
        if st.button(ex, key=f"ex_{idx}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": ex})
            with st.spinner("Menganalisis pertanyaan..."):
                response = ask_assistant(ex, st.session_state.session_id, DEFAULT_LANGFLOW_URL)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    st.markdown("<hr style='border-color: #E2E8F0; margin: 16px 0;'>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='chat-area'>", unsafe_allow_html=True)

    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(
                """
                Halo! Saya **Asisten HRD Virtual — AMAZON Multi-Agent RAG** 👋
                
                Saya siap membantu menjawab pertanyaan Anda seputar:
                - 📋 **Kebijakan Perusahaan & SOP SDM**
                - 🏖️ **Cuti, Izin, dan Prosedur Sakit**
                - 💵 **Gaji, Tunjangan, dan Salary Grading**
                - 📚 **Training & Matriks Pengembangan Karyawan**
                - 🎯 **Performance Appraisal & Katalog KPI**
                - 🎙️ **Simulasi Latihan Wawancara Competency-Based Interview (STAR)**
                
                Ketik pertanyaan Anda di bawah atau pilih salah satu contoh di panel kiri!
                """
            )

    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    st.markdown("</div>", unsafe_allow_html=True)

    if prompt := st.chat_input("Ketik pertanyaan Anda seputar HRD atau latihan wawancara di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Memproses respon..."):
                response = ask_assistant(prompt, st.session_state.session_id, DEFAULT_LANGFLOW_URL)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
