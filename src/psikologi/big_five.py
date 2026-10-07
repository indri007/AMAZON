"""src/psikologi/big_five.py - Modul Asesmen Big Five (OCEAN) untuk HRD.

Mengukur 5 dimensi kepribadian universal menurut psikologi modern:
- O: Openness (Keterbukaan terhadap ide & pengalaman baru)
- C: Conscientiousness (Kehati-hatian, keteraturan & kedisiplinan kerja)
- E: Extraversion (Orientasi energi sosial & asertivitas)
- A: Agreeableness (Keramahan, kerja sama tim & empati)
- N: Neuroticism (Sensitivitas emosional & respon terhadap stres)
"""

from typing import Dict, List, Any


BIG_FIVE_QUESTIONS = [
    # Openness
    {"id": 1, "trait": "O", "text": "Saya memiliki imajinasi aktif dan selalu antusias mencoba pendekatan/teknologi baru."},
    {"id": 2, "trait": "O", "text": "Saya menikmati diskusi konsep abstrak dan eksplorasi ide-ide filosofis/kreatif."},
    # Conscientiousness
    {"id": 3, "trait": "C", "text": "Saya selalu menepati janji, teliti mengerjakan tugas, dan terorganisir rapi."},
    {"id": 4, "trait": "C", "text": "Saya bekerja dengan rencana jelas dan jarang menunda-nunda pekerjaan sampai batas waktu."},
    # Extraversion
    {"id": 5, "trait": "E", "text": "Saya merasa penuh energi saat berada di tengah kerumunan dan memimpin pembicaraan."},
    {"id": 6, "trait": "E", "text": "Saya mudah memulai percakapan dengan orang asing dan mengekspresikan pendapat saya."},
    # Agreeableness
    {"id": 7, "trait": "A", "text": "Saya cenderung percaya pada itikad baik rekan kerja dan berusaha membantu orang lain."},
    {"id": 8, "trait": "A", "text": "Saya lebih memilih berkompromi demi keharmonisan tim daripada memaksakan kehendak sendiri."},
    # Neuroticism (Inverse / Emotional Stability)
    {"id": 9, "trait": "N", "text": "Saya mudah merasa cemas atau tertekan saat menghadapi perubahan target mendadak."},
    {"id": 10, "trait": "N", "text": "Suasana hati saya sering berfluktuasi ketika menghadapi beban kerja yang tinggi."},
]


def calculate_big_five_score(responses: Dict[int, int]) -> Dict[str, Any]:
    """
    Menghitung skor Big Five (OCEAN).
    responses: dict mapping id pertanyaan ke nilai Likert (1: Sangat Tidak Setuju s.d. 5: Sangat Setuju).
    """
    trait_scores = {"O": [], "C": [], "E": [], "A": [], "N": []}

    for q in BIG_FIVE_QUESTIONS:
        qid = q["id"]
        val = responses.get(qid, 3)
        trait_scores[q["trait"]].append(val)

    results = {}
    trait_labels = {
        "O": ("Openness to Experience", "Inovasi & Daya Adaptasi Konseptual"),
        "C": ("Conscientiousness", "Integritas Kerja, Ketelitian & Disiplin"),
        "E": ("Extraversion", "Komunikasi & Kepemimpinan Sosial"),
        "A": ("Agreeableness", "Kolaborasi Tim & Kepekaan Antarpribadi"),
        "N": ("Neuroticism", "Tingkat Kerentanan terhadap Tekanan Stres"),
    }

    for code, scores in trait_scores.items():
        avg = sum(scores) / len(scores) if scores else 3.0
        pct = round((avg / 5.0) * 100, 1)

        level = "Tinggi" if avg >= 3.8 else ("Sedang" if avg >= 2.6 else "Rendah")
        label, desc = trait_labels[code]

        results[code] = {
            "name": label,
            "focus": desc,
            "average_score": round(avg, 2),
            "percentage": pct,
            "level": level,
        }

    # Hitung Emotional Stability (100 - Neuroticism %)
    stability_pct = round(100.0 - results["N"]["percentage"], 1)

    return {
        "traits": results,
        "emotional_stability_score": stability_pct,
        "hr_summary": (
            f"Kandidat memiliki Conscientiousness {results['C']['level']} ({results['C']['percentage']}%) "
            f"dan Agreeableness {results['A']['level']} ({results['A']['percentage']}%). "
            f"Tingkat ketahanan stres (Emotional Stability): {stability_pct}%."
        ),
    }
