import streamlit as st
import requests
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Asisten HRD Virtual",
    page_icon="👥",
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
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .chat-bubble {
        border-radius: 24px;
        padding: 16px 20px;
        margin-bottom: 12px;
        box-shadow: 0 12px 28px rgba(16, 42, 67, 0.08);
        line-height: 1.75;
        max-width: 88%;
        word-wrap: break-word;
    }
    .user-bubble {
        background: #D0E2FF;
        color: #102A43;
        margin-left: auto;
        text-align: right;
    }
    .assistant-bubble {
        background: #FFFFFF;
        color: #102A43;
        margin-right: auto;
        text-align: left;
    }
    .sidebar-card {
        background: #E2E7EF;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .sidebar-title {
        color: #102A43;
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 12px;
    }
    .sidebar-text {
        color: #334E68;
        font-size: 14px;
        line-height: 1.8;
    }
    .header-card {
        background: #FFFFFF;
        border-radius: 26px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 18px 50px rgba(16, 42, 67, 0.08);
    }
    .header-title {
        font-size: 32px;
        font-weight: 700;
        color: #102A43;
        margin-bottom: 8px;
    }
    .header-subtitle {
        font-size: 16px;
        color: #334E68;
        line-height: 1.8;
    }
    .chat-area {
        background: #FFFFFF;
        border-radius: 30px;
        padding: 26px;
        box-shadow: 0 16px 40px rgba(16, 42, 67, 0.08);
    }
    .message-label {
        color: #334E68;
        font-size: 13px;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .stButton>button {
        border-radius: 999px;
        padding: 0.85rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        opacity: 0.95;
    }
    .stTextInput>div>div>input {
        border-radius: 999px;
        padding: 0.95rem 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Config ───────────────────────────────────────────────────────────────────
LANGFLOW_URL = st.secrets.get("LANGFLOW_URL", "http://localhost:7862")
FLOW_ID = st.secrets.get("FLOW_ID", "d8eedd75-92a7-47f0-974a-b74c0062ea23")
API_KEY = st.secrets.get("LANGFLOW_API_KEY", "")

LANGFLOW_API = f"{LANGFLOW_URL}/api/v1/run/{FLOW_ID}?stream=false"

# ── Helpers ───────────────────────────────────────────────────────────────────
def ask_langflow(question: str, session_id: str) -> str:
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
        resp = requests.post(LANGFLOW_API, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        outputs = data.get("outputs", [])
        if outputs:
            for out in outputs:
                for result in out.get("outputs", []):
                    msg = result.get("results", {}).get("message", {})
                    text = msg.get("text") or msg.get("data", {}).get("text", "")
                    if text:
                        return text
        return "Maaf, tidak ada respons dari sistem."
    except requests.exceptions.ConnectionError:
        return "❌ Tidak dapat terhubung ke Langflow. Pastikan Langflow sedang berjalan."
    except requests.exceptions.Timeout:
        return "❌ Waktu permintaan habis. Coba lagi beberapa saat."
    except Exception as e:
        return f"❌ Terjadi kesalahan: {str(e)}"


# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    import uuid
    st.session_state.session_id = str(uuid.uuid4())

# ── UI ────────────────────────────────────────────────────────────────────────
header_col, _ = st.columns([3, 1])
with header_col:
    st.markdown("<div class='header-card'>", unsafe_allow_html=True)
    st.markdown("<div class='header-title'>👥 Asisten HRD Virtual</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='header-subtitle'>Tanya seputar kebijakan perusahaan, cuti, gaji, training, KPI, dan rekrutmen.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

left_col, right_col = st.columns([1, 2], gap="large")

with left_col:
    st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>ℹ️ Tentang</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sidebar-text'>Asisten HRD Virtual membantu karyawan mendapatkan informasi seputar cuti, gaji, SOP, training, KPI, dan rekrutmen.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<hr style='border-color: #C7CAD0; margin: 18px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-title'>💡 Contoh pertanyaan</div>", unsafe_allow_html=True)

    examples = [
        "Berapa hari cuti tahunan saya?",
        "Bagaimana cara mengajukan training?",
        "Apa syarat promosi jabatan?",
        "Jelaskan proses performance appraisal",
        "Saya mau latihan wawancara HRD",
    ]

    for idx, ex in enumerate(examples):
        if st.button(ex, key=f"ex_{idx}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": ex})
            with st.spinner("Sedang memproses..."):
                response = ask_langflow(ex, st.session_state.session_id)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    st.markdown("<hr style='border-color: #C7CAD0; margin: 18px 0;'>", unsafe_allow_html=True)
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='chat-area'>", unsafe_allow_html=True)

    if not st.session_state.messages:
        with st.chat_message("assistant", avatar="👥"):
            st.markdown(
                """
                Halo! Saya **Asisten HRD Virtual** 👋
                
                Saya siap membantu menjawab pertanyaan Anda seputar:
                - Kebijakan perusahaan & SOP
                - Cuti, izin, dan absensi
                - Gaji, tunjangan, dan benefit
                - Training dan pengembangan karir
                - Performance appraisal & KPI
                - Proses rekrutmen dan promosi
                
                Atau jika Anda ingin **latihan wawancara**, ketik:
                > *"Saya mau latihan wawancara untuk posisi [nama posisi]"*
                
                Ada yang bisa saya bantu? 😊
                """,
                unsafe_allow_html=True,
            )

    for msg in st.session_state.messages:
        bubble_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "👥"):
            st.markdown(
                f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>",
                unsafe_allow_html=True,
            )

    if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(
                f"<div class='chat-bubble user-bubble'>{prompt}</div>",
                unsafe_allow_html=True,
            )

        with st.chat_message("assistant", avatar="👥"):
            with st.spinner("Sedang mencari jawaban..."):
                response = ask_langflow(prompt, st.session_state.session_id)
            st.markdown(
                f"<div class='chat-bubble assistant-bubble'>{response}</div>",
                unsafe_allow_html=True,
            )

        st.session_state.messages.append({"role": "assistant", "content": response})

    st.markdown("</div>", unsafe_allow_html=True)
