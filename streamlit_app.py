import streamlit as st
import requests
import json

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Asisten HRD Virtual",
    page_icon="👥",
    layout="centered",
)

# ── Config ────────────────────────────────────────────────────────────────────
LANGFLOW_URL = st.secrets.get("LANGFLOW_URL", "http://localhost:7862")
FLOW_ID      = st.secrets.get("FLOW_ID", "d8eedd75-92a7-47f0-974a-b74c0062ea23")
API_KEY      = st.secrets.get("LANGFLOW_API_KEY", "")

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
        # Ambil output teks dari response Langflow
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
st.title("👥 Asisten HRD Virtual")
st.caption("Tanya seputar kebijakan perusahaan, cuti, gaji, training, KPI, dan rekrutmen.")

st.divider()

# Sidebar info
with st.sidebar:
    st.header("ℹ️ Tentang")
    st.markdown("""
    **Asisten HRD Virtual** membantu karyawan mendapatkan informasi seputar:
    
    - 📅 Cuti & Izin
    - 💰 Gaji & Benefit
    - 📋 SOP & Kebijakan
    - 🎓 Training & Pengembangan
    - 📊 KPI & Performance
    - 🔼 Promosi & Karir
    - 🤝 Rekrutmen & Onboarding
    """)
    
    st.divider()
    
    st.markdown("**💡 Contoh pertanyaan:**")
    
    examples = [
        "Berapa hari cuti tahunan saya?",
        "Bagaimana cara mengajukan training?",
        "Apa syarat promosi jabatan?",
        "Jelaskan proses performance appraisal",
        "Saya mau latihan wawancara HRD",
    ]
    
    for ex in examples:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": ex})
            with st.spinner("Sedang memproses..."):
                response = ask_langflow(ex, st.session_state.session_id)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.divider()
    
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "👥"):
        st.markdown(msg["content"])

# Welcome message jika belum ada chat
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="👥"):
        st.markdown("""
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
        """)

# Chat input
if prompt := st.chat_input("Ketik pertanyaan Anda di sini..."):
    # Tampilkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)

    # Proses dan tampilkan respons
    with st.chat_message("assistant", avatar="👥"):
        with st.spinner("Sedang mencari jawaban..."):
            response = ask_langflow(prompt, st.session_state.session_id)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
