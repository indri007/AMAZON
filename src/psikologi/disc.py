"""src/psikologi/disc.py - Modul Asesmen Kepribadian DISC untuk HRD.

Mengukur 4 dimensi kepribadian di lingkungan kerja:
- Dominance (D): Berorientasi pada hasil, ketegasan, dan tantangan.
- Influence (I): Berorientasi pada orang, persuasi, antusiasme, dan relasi.
- Steadiness (S): Berorientasi pada stabilitas, kerja sama, ketekunan, dan loyalitas.
- Conscientiousness (C): Berorientasi pada akurasi, kualitas, logika, dan kepatuhan.
"""

from typing import Dict, List, Any


DISC_QUESTIONS = [
    {
        "id": 1,
        "options": {
            "D": "Tegas, cepat mengambil keputusan, dan berani mengambil risiko.",
            "I": "Antusias, ramah, dan mudah bergaul dengan orang baru.",
            "S": "Sabar, pendengar yang baik, dan menyukai ritme kerja yang stabil.",
            "C": "Teliti, analitis, dan mengutamakan ketepatan data/aturan.",
        },
    },
    {
        "id": 2,
        "options": {
            "D": "Fokus pada target hasil akhir (bottom line).",
            "I": "Fokus pada membangun relasi dan memotivasi tim.",
            "S": "Fokus pada menjaga keharmonisan dan mendukung rekan kerja.",
            "C": "Fokus pada standar kualitas tinggi dan keakuratan prosedur.",
        },
    },
    {
        "id": 3,
        "options": {
            "D": "Menyukai tantangan kompetitif dan kendali atas proyek.",
            "I": "Menyukai pengakuan sosial, presentasi, dan diskusi ide kreatif.",
            "S": "Menyukai konsistensi dan perubahan yang terencana bertahap.",
            "C": "Menyukai analisis mendalam berbasis fakta logis.",
        },
    },
    {
        "id": 4,
        "options": {
            "D": "Berbicara to-the-point dan langsung pada inti persoalan.",
            "I": "Ekspresif, persuasif, dan penuh energi positif.",
            "S": "Tenang, suportif, dan menghindari perdebatan frontal.",
            "C": "Sistematis, hati-hati, dan menyertakan bukti/fakta.",
        },
    },
    {
        "id": 5,
        "options": {
            "D": "Cepat bosan dengan rutinitas; ingin perubahan cepat.",
            "I": "Senang bekerja dalam tim besar dan suasana terbuka.",
            "S": "Setia, loyal, dan dapat diandalkan menyelesaikan tugas sampai tuntas.",
            "C": "Sangat terstruktur, disiplin jadwal, dan teliti memeriksa detail.",
        },
    },
    {
        "id": 6,
        "options": {
            "D": "Menghadapi konflik secara langsung dan berani bersikap.",
            "I": "Menyelesaikan konflik dengan humor, diplomasi, dan negosiasi santai.",
            "S": "Mencari jalan tengah demi menjaga ketenangan kelompok.",
            "C": "Menyelesaikan konflik berdasarkan aturan tertulis dan fakta objektif.",
        },
    },
]

PROFILES = {
    "D": {
        "title": "Dominance (The Driver / Pioneer)",
        "summary": "Karakter dominan, berorientasi hasil cepat, gigih, mandiri, dan berani menghadapi tantangan.",
        "strengths": ["Pengambilan keputusan cepat", "Visioner dan problem solver", "Berani memimpin di bawah krisis"],
        "weaknesses": ["Bisa terkesan tidak sabar atau mendikte", "Kurang peka terhadap perasaan orang lain", "Enggan berurusan dengan detail administratif"],
        "ideal_roles": ["Executive Leader", "Operations Manager", "Business Development", "Project Director"],
        "work_environment": "Lingkungan kompetitif, fleksibel, berorientasi target dengan otonomi tinggi.",
    },
    "I": {
        "title": "Influence (The Inspirer / Communicator)",
        "summary": "Karakter karismatik, persuasif, komunikatif, optimis, dan membangun jejaring dengan antusiasme tinggi.",
        "strengths": ["Kemampuan persuasi dan public speaking unggul", "Pembangun moral tim", "Kreatif dan inovatif"],
        "weaknesses": ["Kurang disiplin pada tindak lanjut detail", "Mudah terdistraksi", "Cenderung over-promising"],
        "ideal_roles": ["Public Relations", "Sales & Marketing", "Human Resource Engagement", "Creative Director"],
        "work_environment": "Lingkungan kolaboratif, dinamis, terbuka, dengan interaksi sosial yang intens.",
    },
    "S": {
        "title": "Steadiness (The Supporter / Anchor)",
        "summary": "Karakter tenang, setia, stabil, konsisten, berempati tinggi, dan menjadi perekat tim.",
        "strengths": ["Dapat dipercaya dan pendengar empati luar biasa", "Konsistensi eksekusi jangka panjang", "Menciptakan lingkungan kerja damai"],
        "weaknesses": ["Resisten terhadap perubahan mendadak", "Sulit menolak permintaan (sungkan)", "Kurang asertif dalam konflik"],
        "ideal_roles": ["Customer Service", "HR Administration", "Quality Assurance", "Counselor / General Affairs"],
        "work_environment": "Lingkungan yang aman, saling mendukung, dengan SOP yang jelas dan terencana.",
    },
    "C": {
        "title": "Conscientiousness (The Analyst / Thinker)",
        "summary": "Karakter analitis, presisi, berbasis data, sistematis, dan mengutamakan kualitas tanpa cela.",
        "strengths": ["Akurasi dan kepatuhan standar yang tinggi", "Analisis data dan mitigasi risiko mendalam", "Berpikir objektif dan metodis"],
        "weaknesses": ["Cenderung over-thinking (analisis kelumpuhan)", "Terlalu kritis pada diri sendiri dan orang lain", "Kaku pada peraturan"],
        "ideal_roles": ["Finance & Tax Specialist", "Compliance & Risk Auditor", "Data Scientist / Software Engineer", "Legal Officer"],
        "work_environment": "Lingkungan profesional, tertib, berstandar mutu tinggi dengan sedikit distraksi.",
    },
}


def calculate_disc_score(answers: List[str]) -> Dict[str, Any]:
    """Menghitung skor DISC dari daftar pilihan (D, I, S, C)."""
    counts = {"D": 0, "I": 0, "S": 0, "C": 0}
    for ans in answers:
        if ans in counts:
            counts[ans] += 1

    total = max(len(answers), 1)
    percentages = {k: round((v / total) * 100, 1) for k, v in counts.items()}

    # Tentukan tipe primer dan sekunder
    sorted_traits = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    primary = sorted_traits[0][0]
    secondary = sorted_traits[1][0] if sorted_traits[1][1] > 0 else primary

    profile_data = PROFILES[primary]

    return {
        "raw_counts": counts,
        "percentages": percentages,
        "primary_type": primary,
        "secondary_type": secondary,
        "title": profile_data["title"],
        "summary": profile_data["summary"],
        "strengths": profile_data["strengths"],
        "weaknesses": profile_data["weaknesses"],
        "ideal_roles": profile_data["ideal_roles"],
        "work_environment": profile_data["work_environment"],
    }
