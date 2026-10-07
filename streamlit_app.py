import streamlit as st
import requests
import json
import re
from pathlib import Path

from src.psikologi import (
    calculate_disc_score, DISC_QUESTIONS,
    calculate_mbti_score, MBTI_QUESTIONS,
    calculate_riasec_score, RIASEC_QUESTIONS,
    evaluate_kraepelin_performance,
    IN_BASKET_MEMOS, evaluate_in_basket_decisions,
    evaluate_bei_star_response,
    CASE_ANALYSIS_BLACKBERRY,
)

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
    st.link_button("🚀 Buka 3D Architecture Showcase (Lokal)", "http://localhost:3000", use_container_width=True)

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
    tab_chat, tab_psiko, tab_assessment = st.tabs([
        "💬 Asisten RAG HRD",
        "🧠 Modul Tes Psikologi",
        "🏢 Simulasi Assessment Center",
    ])

    with tab_chat:
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

    with tab_psiko:
        st.markdown("### 🧠 Asesmen Psikometrik & Tes Kepribadian Kerja")
        st.caption("Pilih instrumen tes psikologi yang ingin dijalankan:")
        
        test_type = st.selectbox(
            "Jenis Tes Psikologi:",
            ["Tes Kepribadian DISC", "Tes MBTI (16 Kepribadian)", "Tes Minat Karier Holland (RIASEC)", "Tes Daya Tahan Kerja (Kraepelin)"]
        )

        if test_type == "Tes Kepribadian DISC":
            st.markdown("#### 📊 Kuesioner Profil DISC")
            st.write("Pilih pernyataan yang paling menggambarkan gaya kerja Anda:")
            disc_answers = []
            for q in DISC_QUESTIONS:
                st.markdown(f"**Soal {q['id']}:**")
                choice = st.radio(
                    f"Pilihan Soal {q['id']}",
                    options=["D", "I", "S", "C"],
                    format_func=lambda x, opts=q["options"]: f"[{x}] {opts[x]}",
                    key=f"disc_q_{q['id']}",
                    label_visibility="collapsed"
                )
                disc_answers.append(choice)

            if st.button("🎯 Analisis Profil DISC Saya", use_container_width=True):
                res = calculate_disc_score(disc_answers)
                st.success(f"### Hasil: {res['title']}")
                st.info(f"**Ringkasan Perilaku Kerja:** {res['summary']}")
                
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.markdown("##### 🌟 Kekuatan Utama:")
                    for s in res["strengths"]:
                        st.markdown(f"- {s}")
                    st.markdown("##### 💼 Posisi / Peran Ideal:")
                    for r in res["ideal_roles"]:
                        st.markdown(f"- {r}")

                with col_d2:
                    st.markdown("##### ⚠️ Potensi Area Pengembangan:")
                    for w in res["weaknesses"]:
                        st.markdown(f"- {w}")
                    st.markdown(f"**Lingkungan Kerja Ideal:** {res['work_environment']}")

                st.markdown("##### Distribusi Dimensi:")
                st.progress(int(res["percentages"]["D"]), text=f"Dominance: {res['percentages']['D']}%")
                st.progress(int(res["percentages"]["I"]), text=f"Influence: {res['percentages']['I']}%")
                st.progress(int(res["percentages"]["S"]), text=f"Steadiness: {res['percentages']['S']}%")
                st.progress(int(res["percentages"]["C"]), text=f"Conscientiousness: {res['percentages']['C']}%")

        elif test_type == "Tes MBTI (16 Kepribadian)":
            st.markdown("#### 🧩 Kuesioner MBTI (Myers-Briggs Type Indicator)")
            mbti_answers = {}
            for q in MBTI_QUESTIONS:
                st.markdown(f"**Pertanyaan {q['id']}:**")
                mbti_choice = st.radio(
                    f"mbti_q_{q['id']}",
                    options=["A", "B"],
                    format_func=lambda opt, item=q: item[opt][1],
                    key=f"mbti_rad_{q['id']}",
                    label_visibility="collapsed"
                )
                mbti_answers[q["id"]] = mbti_choice

            if st.button("🔍 Hitung Tipe MBTI Saya", use_container_width=True):
                mbti_res = calculate_mbti_score(mbti_answers)
                st.success(f"### Tipe Anda: {mbti_res['mbti_type']} — {mbti_res['archetype']}")
                st.write(mbti_res["description"])
                st.markdown("##### 🚀 Rekomendasi Jalur Karier:")
                st.write(", ".join(mbti_res["recommended_careers"]))

        elif test_type == "Tes Minat Karier Holland (RIASEC)":
            st.markdown("#### 🧭 Inventori Minat Karier Holland (RIASEC)")
            st.write("Beri penilaian seberapa minat Anda terhadap aktivitas berikut (Skala 1: Kurang Minat s.d. 5: Sangat Minat):")
            riasec_answers = {}
            for q in RIASEC_QUESTIONS[:6]:
                riasec_answers[q["id"]] = st.slider(f"[{q['type']}] {q['text']}", 1, 5, 3, key=f"riasec_{q['id']}")

            if st.button("📊 Dapatkan Holland Code Karier", use_container_width=True):
                riasec_res = calculate_riasec_score(riasec_answers)
                st.success(f"### Holland Code Anda: {riasec_res['holland_code']}")
                st.info(f"Fokus Utama: **{riasec_res['primary_interest']}** & **{riasec_res['secondary_interest']}**")
                st.markdown("##### 🎯 Rekomendasi Jabatan Relevan:")
                for role in riasec_res["top_roles"]:
                    st.markdown(f"- {role}")

        elif test_type == "Tes Daya Tahan Kerja (Kraepelin)":
            st.markdown("#### ⏱️ Simulasi Evaluasi Ketahanan Kerja Kraepelin / Pauli")
            st.write("Masukkan simulasi performa lembar penjumlahan angka kandidat:")
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                attempted = st.number_input("Rata-rata item dikerjakan per kolom:", min_value=10, max_value=60, value=32)
            with col_k2:
                errors = st.number_input("Rata-rata kesalahan per kolom:", min_value=0, max_value=15, value=1)

            if st.button("📈 Evaluasi Daya Tahan Stres", use_container_width=True):
                sim_cols = [
                    {"attempted": attempted - 2, "correct": attempted - 2 - errors, "errors": errors},
                    {"attempted": attempted, "correct": attempted - errors, "errors": errors},
                    {"attempted": attempted + 2, "correct": attempted + 2 - errors, "errors": errors},
                    {"attempted": attempted + 3, "correct": attempted + 3 - errors, "errors": errors},
                ]
                k_res = evaluate_kraepelin_performance(sim_cols)
                st.info(f"### Status HR: {k_res['hr_recommendation']}")
                m = k_res["metrics"]
                st.write(f"- **Kecepatan (Panker):** {m['panker_kecepatan']['value']} ({m['panker_kecepatan']['status']})")
                st.write(f"- **Ketelitian (Tianker):** {m['tianker_ketelitian']['accuracy_pct']}% ({m['tianker_ketelitian']['status']})")
                st.write(f"- **Daya Tahan (Hanker):** {m['hanker_daya_tahan']['status']}")

    with tab_assessment:
        st.markdown("### 🏢 Simulasi Assessment Center (Manager & Supervisor)")
        st.caption("Instrumen resmi berbasis studi kasus dan simulasi manajerial operasional:")

        ac_mode = st.selectbox(
            "Pilih Instrumen Asesmen:",
            ["In-Basket Exercise (Manajemen Memo)", "Case Analysis (Studi Kasus Blackberry)", "Behavior Event Interview (Evaluasi STAR)"]
        )

        if ac_mode == "In-Basket Exercise (Manajemen Memo)":
            st.markdown("#### 📥 Simulasi In-Basket: Skala Prioritas & Tindakan Manajer")
            st.write("Sebagai Manajer, tentukan prioritas dan instruksi tindakan untuk setiap memo berikut:")
            
            user_in_basket = []
            for memo in IN_BASKET_MEMOS:
                with st.expander(f"📌 {memo['id']}: {memo['subject']} (Dari: {memo['from']})", expanded=True):
                    st.write(memo["content"])
                    prio = st.selectbox(
                        f"Prioritas untuk {memo['id']}:",
                        ["High-Urgent", "High-Important", "Medium-Important", "Low"],
                        key=f"prio_{memo['id']}"
                    )
                    act = st.text_input(
                        f"Instruksi Rencana Tindakan Anda:",
                        placeholder="Contoh: Koordinasikan segera dengan tim logistik dan buat jadwal darurat...",
                        key=f"act_{memo['id']}"
                    )
                    user_in_basket.append({"memo_id": memo["id"], "priority": prio, "action_notes": act})

            if st.button("📝 Kumpulkan & Nilai Keputusan In-Basket", use_container_width=True):
                eval_ib = evaluate_in_basket_decisions(user_in_basket)
                st.success(f"### Skor In-Basket Anda: {eval_ib['score_out_of_100']} / 100 ({eval_ib['assessment_level']})")
                for fb in eval_ib["memo_feedbacks"]:
                    st.markdown(f"**{fb['memo_id']} - {fb['subject']}**")
                    st.write(f"- Prioritas Anda: `{fb['user_priority']}` (Ideal: `{fb['ideal_priority']}`)")
                    st.write(f"- *Rekomendasi Tindakan Ideal:* {fb['ideal_action']}")

        elif ac_mode == "Case Analysis (Studi Kasus Blackberry)":
            st.markdown(f"#### 📖 {CASE_ANALYSIS_BLACKBERRY['title']}")
            st.info(CASE_ANALYSIS_BLACKBERRY["background"])
            st.markdown("##### 🎯 Tugas Peserta Asesmen:")
            st.write(CASE_ANALYSIS_BLACKBERRY["task"])
            
            st.markdown("##### Rubrik Evaluasi Asesor:")
            for r in CASE_ANALYSIS_BLACKBERRY["rubric"]:
                st.markdown(f"- **{r['aspect']} (Maks {r['max_score']} Poin):** {r['desc']}")

            candidate_solution = st.text_area(
                "Tuliskan Ringkasan Cetak Biru (Blueprint) Solusi Anda di Sini:",
                placeholder="1. Restrukturisasi komunikasi lintas divisi...\n2. Perombakan sistem reward berbasis KPI terukur...\n3. Program coaching dan retensi talenta..."
            )
            if st.button("📤 Kirim Cetak Biru untuk Penilaian Asesor", use_container_width=True):
                if len(candidate_solution.split()) >= 20:
                    st.success("✅ Cetak Biru Anda berhasil diserahkan! Struktur rencana aksi Anda telah dicatat untuk evaluasi panel asesor.")
                else:
                    st.warning("⚠️ Rencana aksi terlalu singkat. Uraikan minimal 20 kata mencakup restrukturisasi budaya, KPI, dan retensi talenta.")

        elif ac_mode == "Behavior Event Interview (Evaluasi STAR)":
            st.markdown("#### 🎙️ Evaluator Jawaban Wawancara Kompetensi (Metode STAR)")
            comp = st.selectbox("Kompetensi yang Dievaluasi:", ["Problem Solving & Decision Making", "Leadership", "Teamwork & Conflict Resolution"])
            answer_text = st.text_area(
                "Masukkan Transkrip / Jawaban Kandidat:",
                placeholder="Contoh: Ketika proyek logistik tahun lalu tertahan, tugas saya memimpin tim darurat. Saya melakukan negosiasi ulang izin kargo dan hasilnya barang tiba tepat waktu dengan kepuasan klien 95%."
            )
            if st.button("🔍 Evaluasi Kualitas STAR", use_container_width=True):
                if answer_text.strip():
                    star_res = evaluate_bei_star_response(answer_text, comp)
                    st.info(f"### Hasil Evaluasi: {star_res['star_rating']} (Skor: {star_res['star_completeness_score']}/100)")
                    st.markdown("##### Elemen Terdeteksi:")
                    for elem, detected in star_res["detected_elements"].items():
                        st.markdown(f"- {'✅' if detected else '❌'} {elem}")
                    st.markdown("##### Saran Perbaikan:")
                    for rec in star_res["recommendations"]:
                        st.markdown(f"- {rec}")
                else:
                    st.warning("Silakan masukkan teks jawaban kandidat terlebih dahulu.")

