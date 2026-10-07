"""src/psikologi/riasec.py - Modul Asesmen Minat Karier Holland RIASEC untuk HRD.

Mengukur 6 orientasi tipe kepribadian karier (Holland Codes):
- R: Realistic (Praktis, teknis operasional, konkret)
- I: Investigative (Riset analitis, pemecahan masalah kompleks, sains)
- A: Artistic (Kreativitas, desain, ekspresi bebas, orisinalitas)
- S: Social (Pelayanan, pembinaan SDM, kolaborasi, empati)
- E: Enterprising (Kepemimpinan bisnis, persuasi, negosiasi, pencapaian target)
- C: Conventional (Tertib administrasi, presisi data, kepatuhan regulasi)
"""

from typing import Dict, List, Any


RIASEC_QUESTIONS = [
    {"id": 1, "type": "R", "text": "Saya menyukai tugas perbaikan perangkat teknis atau pekerjaan operasional langsung di lapangan."},
    {"id": 2, "type": "I", "text": "Saya senang meneliti data, menganalisis akar masalah, dan menguji hipotesis ilmiah."},
    {"id": 3, "type": "A", "text": "Saya suka merancang konsep visual, menulis kreatif, atau menciptakan desain inovatif."},
    {"id": 4, "type": "S", "text": "Saya bersemangat mengajar, membimbing rekan kerja, dan membantu menyelesaikan problem antarpribadi."},
    {"id": 5, "type": "E", "text": "Saya menikmati negosiasi bisnis, memimpin proyek baru, dan meyakinkan klien/pemangku kepentingan."},
    {"id": 6, "type": "C", "text": "Saya sangat teliti menyusun laporan keuangan, memeriksa rekonsiliasi data, dan mengikuti SOP baku."},
    {"id": 7, "type": "R", "text": "Saya lebih suka bekerja dengan alat, mesin, atau benda fisik daripada konsep abstrak."},
    {"id": 8, "type": "I", "text": "Saya tertantang memecahkan teka-teki logika atau pola matematis yang sulit."},
    {"id": 9, "type": "A", "text": "Saya merasa terkekang jika harus mengikuti rutinitas kerja yang monoton dan kaku."},
    {"id": 10, "type": "S", "text": "Saya merasa puas ketika melihat orang lain berkembang berkat bimbingan yang saya berikan."},
    {"id": 11, "type": "E", "text": "Saya percaya diri mempresentasikan usulan bisnis di hadapan dewan direksi/investor."},
    {"id": 12, "type": "C", "text": "Saya menyukai penyimpanan arsip yang terstruktur, rapi, dan mudah ditelusuri ulang."},
]

CAREER_MAPPINGS = {
    "R": {"name": "Realistic", "roles": ["Site Operations Supervisor", "Facilities Engineer", "Logistics Operations Lead", "Hardware Support Specialist"]},
    "I": {"name": "Investigative", "roles": ["Data Analyst / BI Specialist", "Business Systems Analyst", "R&D Researcher", "Risk Modeler"]},
    "A": {"name": "Artistic", "roles": ["Creative Content Lead", "UI/UX Designer", "Brand Storyteller", "Instructional Media Designer"]},
    "S": {"name": "Social", "roles": ["HR Talent Development Specialist", "Employee Relations Lead", "Corporate Trainer", "Customer Success Lead"]},
    "E": {"name": "Enterprising", "roles": ["Account Executive / Sales Lead", "Product Manager", "Business Development Manager", "Operations Director"]},
    "C": {"name": "Conventional", "roles": ["Finance & Tax Officer", "Internal Compliance Auditor", "Payroll Specialist", "Database Administrator"]},
}


def calculate_riasec_score(responses: Dict[int, int]) -> Dict[str, Any]:
    """
    Menghitung skor RIASEC dan menghasilkan 3 Holland Codes teratas.
    responses: dict mapping id ke nilai skala minat (1: Kurang Minat s.d. 5: Sangat Minat).
    """
    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}

    for q in RIASEC_QUESTIONS:
        qid = q["id"]
        val = responses.get(qid, 3)
        scores[q["type"]] += val

    # Urutkan berdasarkan total skor
    sorted_codes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_3_code = "".join([code for code, _ in sorted_codes[:3]])

    recommended_roles = []
    for code, _ in sorted_codes[:3]:
        recommended_roles.extend(CAREER_MAPPINGS[code]["roles"])

    return {
        "raw_scores": scores,
        "holland_code": top_3_code,
        "primary_interest": CAREER_MAPPINGS[sorted_codes[0][0]]["name"],
        "secondary_interest": CAREER_MAPPINGS[sorted_codes[1][0]]["name"],
        "tertiary_interest": CAREER_MAPPINGS[sorted_codes[2][0]]["name"],
        "top_roles": recommended_roles[:6],
    }
