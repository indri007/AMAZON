"""src/psikologi/assessment_center.py - Modul Simulasi & Evaluasi Assessment Center Manajerial.

Mengadopsi instrumen dari Tools 3 Assessment Center:
1. In-Basket Exercise (Prioritas Memo, Pengorganisasian, Delegasi)
2. Case Analysis (Studi Kasus Transformasi & Turnaround Perusahaan Blackberry Consumer Goods)
3. Behavioral Event Interview (BEI) STAR Evaluator
"""

from typing import List, Dict, Any


IN_BASKET_MEMOS = [
    {
        "id": "MEMO-01",
        "from": "Direktur Operasional",
        "subject": "Tuntutan Pengiriman Produk Tertahan di Pelabuhan",
        "content": "Kargo bahan baku utama tertahan di pelabuhan bea cukai karena kelengkapan izin impor. Pabrik terancam berhenti produksi dalam 24 jam jika bahan tidak tiba.",
        "correct_priority": "High-Urgent",
        "ideal_action": "Segera hubungi tim kepatuhan/legal untuk pengurusan diskresi, koordinasikan dengan manajer produksi untuk skenario jadwal darurat, dan laporkan status ke Direktur.",
        "competencies": ["Problem Solving", "Decisiveness", "Planning & Organizing"],
    },
    {
        "id": "MEMO-02",
        "from": "HR Manager",
        "subject": "Evaluasi Kinerja Semester & Nominasi Bonus Tim Anda",
        "content": "Format pengajuan KPI tim Anda belum diserahkan. Batas akhir pengisian adalah lusa pukul 17:00 WIB untuk pencairan bonus tepat waktu.",
        "correct_priority": "High-Important",
        "ideal_action": "Jadwalkan review 1-on-1 kilat dengan para supervisor untuk memverifikasi pencapaian target KPI sebelum batas waktu lusa.",
        "competencies": ["People Development", "Accountability"],
    },
    {
        "id": "MEMO-03",
        "from": "Supervisor Gudang (Doni)",
        "subject": "Konflik Antara Staf Shift Pagi dan Malam",
        "content": "Ada gesekan mengenai serah terima barang retur dan tuduhan selisih stok antara shift pagi dan malam. Suasana kerja memanas.",
        "correct_priority": "Medium-Important",
        "ideal_action": "Lakukan investigasi rekonsiliasi stok bersama audit internal, lalu gelar mediasi terstruktur dengan kedua supervisor shift.",
        "competencies": ["Conflict Management", "Leadership"],
    },
    {
        "id": "MEMO-04",
        "from": "Asosiasi Industri Consumer Goods",
        "subject": "Undangan Seminar Tren Pasar Tahun Depan",
        "content": "Undangan menghadiri seminar tahunan di Jakarta 3 minggu lagi mengenai strategi pemasaran digital.",
        "correct_priority": "Low",
        "ideal_action": "Delegasikan ke asisten atau staf pengembangan produk untuk hadir dan membuat resume laporan.",
        "competencies": ["Delegation", "Time Management"],
    },
]


CASE_ANALYSIS_BLACKBERRY = {
    "title": "Studi Kasus Penyehatan Organisasi Perusahaan Blackberry Consumer Goods",
    "background": (
        "Blackberry adalah perusahaan swasta di bidang consumer goods yang mengalami penurunan laba bersih dramatis "
        "sejak krisis moneter dan persaingan ketat. Laporan konsultan independen mengidentifikasi:\n"
        "1. Tumbuhnya 'raja-raja kecil' di tiap departemen (silo mentality), komunikasi lintas fungsi sangat lemah.\n"
        "2. Kultur birokratis lamban, lebih mementingkan prosedur daripada hasil dan keberanian mengambil risiko.\n"
        "3. Sistem bonus sama rata (tidak berbasis prestasi/KPI), memicu penurunan motivasi karyawan berbakat.\n"
        "4. Pelatihan hanya bersifat rutinitas tanpa evaluasi kebutuhan (TNA) dan tanpa tindak lanjut coaching.\n"
        "5. Redundansi karyawan pada bagian administrasi, sementara jalur karier (career path) tidak jelas.\n"
        "6. Churn karyawan berprestasi tinggi (talent attrition) dan produk dianggap tertinggal oleh konsumen."
    ),
    "task": (
        "Sebagai Ketua Tim Penyempurnaan Organisasi yang ditunjuk Managing Director, buat Cetak Biru (Blueprint) "
        "Rencana Aksi menyeluruh mencakup: Restrukturisasi Budaya, Sistem KPI & Kompensasi Berbasis Kinerja, "
        "Optimalisasi SDM & Jalur Karier, serta Akselerasi Inovasi Produk."
    ),
    "rubric": [
        {"aspect": "Identifikasi Akar Masalah (Root Cause)", "max_score": 25, "desc": "Mampu memetakan keterkaitan silo departemen, insentif non-KPI, dan disonansi inovasi."},
        {"aspect": "Solusi Strategis & KPI Alignment", "max_score": 25, "desc": "Merancang perombakan sistem appraisal berbasis KPI terukur dan meritokrasi bonus."},
        {"aspect": "Manajemen Perubahan & Budaya (Change Management)", "max_score": 25, "desc": "Langkah konkret meruntuhkan silo antar-departemen dan membangun budaya inovatif."},
        {"aspect": "Timeline & Rencana Implementasi Realistis", "max_score": 25, "desc": "Matriks rencana kerja (Action Plan) dengan tahapan jangka pendek, menengah, dan panjang."},
    ],
}


def evaluate_in_basket_decisions(user_decisions: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Mengevaluasi keputusan asese dalam simulasi In-Basket.
    user_decisions: List dict berisi {'memo_id': 'MEMO-01', 'priority': '...', 'action_notes': '...'}
    """
    score = 0
    feedback = []

    memos_dict = {m["id"]: m for m in IN_BASKET_MEMOS}
    for item in user_decisions:
        mid = item.get("memo_id")
        user_prio = item.get("priority", "")
        action = item.get("action_notes", "")

        memo = memos_dict.get(mid)
        if not memo:
            continue

        memo_score = 0
        if user_prio.lower() == memo["correct_priority"].lower():
            memo_score += 15
        else:
            memo_score += 5

        # Evaluasi kecukupan tindakan
        word_count = len(action.split())
        if word_count >= 15:
            memo_score += 10
        elif word_count >= 5:
            memo_score += 5

        score += memo_score
        feedback.append({
            "memo_id": mid,
            "subject": memo["subject"],
            "user_priority": user_prio,
            "ideal_priority": memo["correct_priority"],
            "score": memo_score,
            "ideal_action": memo["ideal_action"],
        })

    max_possible = len(IN_BASKET_MEMOS) * 25
    final_score = round((score / max_possible) * 100, 1)

    return {
        "score_out_of_100": final_score,
        "assessment_level": "Sangat Baik" if final_score >= 80 else ("Cukup" if final_score >= 60 else "Perlu Bimbingan"),
        "memo_feedbacks": feedback,
    }


def evaluate_bei_star_response(candidate_answer: str, competency: str) -> Dict[str, Any]:
    """
    Mengevaluasi jawaban wawancara berbasis Behavioral Event Interview (BEI) dengan metode STAR.
    """
    ans_lower = candidate_answer.lower()
    
    # Deteksi elemen STAR
    has_situation = any(k in ans_lower for k in ["ketika", "saat itu", "situasi", "kondisi", "pada waktu", "proyek"])
    has_task = any(k in ans_lower for k in ["tugas", "tanggung jawab", "tantangan", "target", "peran saya"])
    has_action = any(k in ans_lower for k in ["saya melakukan", "langkah", "inisiatif", "saya menghubungi", "menganalisis", "membuat"])
    has_result = any(k in ans_lower for k in ["hasilnya", "berhasil", "dampaknya", "meningkat", "selesai", "belajar bahwa"])

    elements = {
        "Situation (Konteks Latar Belakang)": has_situation,
        "Task (Tanggung Jawab Spesifik)": has_task,
        "Action (Tindakan Nyata yang Diambil)": has_action,
        "Result (Dampak Terukur & Pembelajaran)": has_result,
    }

    star_count = sum(1 for v in elements.values() if v)
    score = star_count * 25

    suggestions = []
    if not has_situation:
        suggestions.append("Perjelas konteks waktu, latar belakang, dan pihak yang terlibat.")
    if not has_task:
        suggestions.append("Tegaskan apa target atau tanggung jawab spesifik yang dibebankan kepada Anda.")
    if not has_action:
        suggestions.append("Gali lebih dalam tindakan konkret yang ANDA ambil, bukan hanya tindakan tim secara umum.")
    if not has_result:
        suggestions.append("Sertakan bukti keberhasilan terukur (angka, persentase) dan pelajaran yang dipetik.")

    return {
        "competency": competency,
        "star_completeness_score": score,
        "detected_elements": elements,
        "star_rating": f"{star_count}/4 Elemen STAR Terpenuhi",
        "recommendations": suggestions if suggestions else ["Jawaban terstruktur sangat baik dan memenuhi standar BEI profesional."],
    }
