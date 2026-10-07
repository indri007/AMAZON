"""src/psikologi/mbti.py - Modul Asesmen Kepribadian MBTI (16 Tipe Kepribadian) untuk HRD.

Mengukur 4 dimensi preferensi psikologis:
- E (Extraversion) vs I (Introversion)
- S (Sensing) vs N (Intuition)
- T (Thinking) vs F (Feeling)
- J (Judging) vs P (Perceiving)
"""

from typing import Dict, List, Any


MBTI_QUESTIONS = [
    # E vs I
    {"id": 1, "dim": "EI", "A": ("E", "Mendapatkan energi dari berinteraksi dan berdiskusi dengan banyak orang."), "B": ("I", "Mendapatkan energi dari waktu tenang untuk merenung dan fokus mandiri.")},
    {"id": 2, "dim": "EI", "A": ("E", "Cenderung berpikir sambil berbicara langsung dan spontan mengekspresikan ide."), "B": ("I", "Cenderung memikirkan matang-matang secara internal sebelum berbicara.")},
    # S vs N
    {"id": 3, "dim": "SN", "A": ("S", "Fokus pada data konkret, fakta nyata, dan pengalaman praktis saat ini."), "B": ("N", "Fokus pada gambaran besar, pola masa depan, dan kemungkinan-kemungkinan baru.")},
    {"id": 4, "dim": "SN", "A": ("S", "Menyukai instruksi kerja bertahap yang runtut dan realistis."), "B": ("N", "Menyukai inovasi konsep baru dan kebebasan bereksplorasi.")},
    # T vs F
    {"id": 5, "dim": "TF", "A": ("T", "Mengambil keputusan berdasarkan logika objektif, analisis data, dan prinsip keadilan."), "B": ("F", "Mengambil keputusan berdasarkan nilai empati, dampak terhadap manusia, dan harmoni.")},
    {"id": 6, "dim": "TF", "A": ("T", "Mengutamakan kebenaran kritis meskipun terasa kurang menyenangkan bagi orang lain."), "B": ("F", "Mengutamakan perasaan orang lain dan menjaga suasana tetap kondusif.")},
    # J vs P
    {"id": 7, "dim": "JP", "A": ("J", "Menyukai rencana kerja yang terjadwal rapi, target jelas, dan kepastian deadline."), "B": ("P", "Menyukai fleksibilitas, adaptif terhadap perubahan, dan opsi yang tetap terbuka.")},
    {"id": 8, "dim": "JP", "A": ("J", "Merasa puas setelah menyelesaikan daftar tugas (to-do list) lebih awal."), "B": ("P", "Bekerja paling produktif saat mendekati deadline dengan dorongan spontanitas.")},
]

MBTI_DESCRIPTIONS = {
    "INTJ": {"archetype": "The Architect / Mastermind", "desc": "Strategis, analitis mendalam, visioner, dan menuntut standar kesempurnaan tinggi.", "careers": ["Data Scientist", "Strategic Planner", "Software Architect", "R&D Director"]},
    "INTP": {"archetype": "The Logician / Thinker", "desc": "Inovatif, penasaran intelektual, suka menganalisis sistem rumit dan teori abstrak.", "careers": ["Systems Analyst", "Research Scientist", "Algorithm Developer", "Academician"]},
    "ENTJ": {"archetype": "The Commander / Leader", "desc": "Tegas, pengorganisasi andal, berorientasi hasil skala besar, dan pemimpin alami.", "careers": ["CEO / General Manager", "Management Consultant", "Operations Director", "Corporate Strategist"]},
    "ENTP": {"archetype": "The Debater / Innovator", "desc": "Cerdas berargumen, fleksibel, suka memecahkan masalah sulit dengan solusi out-of-the-box.", "careers": ["Venture Capitalist", "Product Manager", "Creative Strategist", "Business Innovator"]},
    "INFJ": {"archetype": "The Advocate / Counselor", "desc": "Idealis, intuitif, berintegritas tinggi, berorientasi menumbuhkan potensi manusia.", "careers": ["Organizational Psychologist", "HR Talent Development", "Coach & Mentor", "Ethics Officer"]},
    "INFP": {"archetype": "The Mediator / Idealist", "desc": "Empatik, penuh nilai kemanusiaan, kreatif, setia pada prinsip moral internal.", "careers": ["Content Creator", "Corporate Culture Specialist", "CSR Coordinator", "UX Researcher"]},
    "ENFJ": {"archetype": "The Protagonist / Mentor", "desc": "Karismatik, komunikator ulung, menginspirasi tim menuju visi bersama dengan empati.", "careers": ["HR Director", "Training & Development Lead", "Public Relations Head", "Team Facilitator"]},
    "ENFP": {"archetype": "The Campaigner / Inspirer", "desc": "Antusias, kaya ide baru, mudah berjejaring, energik membangun kolaborasi positif.", "careers": ["Brand Strategist", "Internal Communications", "Talent Acquisition Lead", "Creative Producer"]},
    "ISTJ": {"archetype": "The Inspector / Logistician", "desc": "Sangat bertanggung jawab, tertib, berpegang pada fakta, SOP, dan komitmen tugas.", "careers": ["Finance Controller", "Quality Assurance Manager", "Compliance Auditor", "Operations Lead"]},
    "ISFJ": {"archetype": "The Protector / Defender", "desc": "Teliti, hangat, setia, dapat diandalkan, dan selalu memastikan rekan kerja tertopang baik.", "careers": ["HR Operations", "Customer Support Manager", "Executive Assistant", "Office Manager"]},
    "ESTJ": {"archetype": "The Executive / Supervisor", "desc": "Praktis, tegas, terorganisir rapi, andal mengelola operasional dan menegakkan aturan.", "careers": ["Project Manager", "Factory Manager", "Legal & General Affairs", "Operations Supervisor"]},
    "ESFJ": {"archetype": "The Consul / Provider", "desc": "Ramah, suka melayani, menjaga harmoni sosial, dan memastikan kerja tim berjalan mulus.", "careers": ["Employee Relations Lead", "Corporate Event Manager", "Customer Experience Lead", "Account Manager"]},
    "ISTP": {"archetype": "The Virtuoso / Crafter", "desc": "Tenang, pengamat jeli, praktis, cepat menyelesaikan masalah teknis lapangan darurat.", "careers": ["DevOps Engineer", "Forensic Analyst", "Technical Specialist", "Maintenance Engineer"]},
    "ISFP": {"archetype": "The Adventurer / Artist", "desc": "Sensitif, fleksibel, ramah, mengutamakan estetika dan kenyamanan suasana kerja.", "careers": ["Graphic Designer", "UI/UX Designer", "Product Stylist", "Instructional Designer"]},
    "ESTP": {"archetype": "The Entrepreneur / Dynamo", "desc": "Berani mengambil risiko, pragmatis, tanggap krisis, dan cepat mengeksekusi peluang.", "careers": ["Sales Director", "Crisis Manager", "Field Operations Lead", "Startup Founder"]},
    "ESFP": {"archetype": "The Entertainer / Performer", "desc": "Spontan, antusias, membuat tempat kerja ceria dan aktif menggerakkan acara.", "careers": ["Talent Engagement Specialist", "Community Manager", "Customer Relations", "Corporate Host"]},
}


def calculate_mbti_score(user_answers: Dict[int, str]) -> Dict[str, Any]:
    """
    Menghitung tipe MBTI berdasarkan jawaban kuisioner.
    user_answers: dict mapping id pertanyaan ke 'A' atau 'B'.
    """
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}

    for q in MBTI_QUESTIONS:
        qid = q["id"]
        choice = user_answers.get(qid, "A")
        selected_code = q[choice][0]
        scores[selected_code] += 1

    # Tentukan huruf untuk setiap dikotomi
    e_or_i = "E" if scores["E"] >= scores["I"] else "I"
    s_or_n = "S" if scores["S"] >= scores["N"] else "N"
    t_or_f = "T" if scores["T"] >= scores["F"] else "F"
    j_or_p = "J" if scores["J"] >= scores["P"] else "P"

    mbti_type = f"{e_or_i}{s_or_n}{t_or_f}{j_or_p}"
    info = MBTI_DESCRIPTIONS.get(mbti_type, {
        "archetype": "Professional Profile",
        "desc": "Profil kepribadian adaptif.",
        "careers": ["General Professional"]
    })

    return {
        "mbti_type": mbti_type,
        "archetype": info["archetype"],
        "description": info["desc"],
        "recommended_careers": info["careers"],
        "dimension_scores": {
            "Extraversion vs Introversion": f"E: {scores['E']} | I: {scores['I']} -> {e_or_i}",
            "Sensing vs Intuition": f"S: {scores['S']} | N: {scores['N']} -> {s_or_n}",
            "Thinking vs Feeling": f"T: {scores['T']} | F: {scores['F']} -> {t_or_f}",
            "Judging vs Perceiving": f"J: {scores['J']} | P: {scores['P']} -> {j_or_p}",
        },
        "raw_scores": scores,
    }
