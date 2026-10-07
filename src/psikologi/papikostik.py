"""src/psikologi/papikostik.py - Modul Asesmen Kepribadian PAPI Kostick untuk HRD.

Mengukur 20 aspek kepribadian kerja dalam 7 bidang utama:
1. Work Direction (Arah Kerja): N (Finish task), G (Hard worker), A (Need to achieve)
2. Leadership (Kepemimpinan): L (Leadership role), P (Need to control), I (Decision making)
3. Activity (Aktivitas Kerja): T (Pace), V (Vigorous type)
4. Social Nature (Relasi Sosial): X (Need to be noticed), S (Social extension), B (Belong to groups), O (Closeness)
5. Work Style (Gaya Kerja): R (Theoretical), D (Interest in details), C (Organized type)
6. Temperament (Temperamen): Z (Need for change), E (Emotional restraint), K (Forceful)
7. Followership (Kepatuhan): F (Need to support authority), W (Need for rules/supervision)
"""

from typing import Dict, List, Any


PAPI_DIMENSIONS = {
    "G": ("Peran Pekerja Keras", "Kegigihan dan dedikasi dalam mencurahkan energi kerja."),
    "L": ("Peran Kepemimpinan", "Kecenderungan untuk memegang kendali dan mengarahkan orang lain."),
    "I": ("Pengambilan Keputusan", "Kecepatan dan keberanian dalam membuat keputusan mandiri."),
    "T": ("Tempo Kerja", "Kecepatan dan dinamika dalam menyelesaikan tugas harian."),
    "V": ("Vitalitas / Energi", "Stamina fisik dan ketahanan beraktivitas intensif."),
    "S": ("Hubungan Sosial", "Kenyamanan dalam membangun relasi hangat dengan rekan kerja."),
    "R": ("Tipe Teoretis / Konseptual", "Kecenderungan berpikir analitis sebelum bertindak."),
    "D": ("Perhatian pada Detail", "Ketelitian dalam memeriksa akurasi dokumen dan angka."),
    "C": ("Keteraturan Kerja", "Sistematika, keteraturan meja kerja, dan kedisiplinan metode."),
    "E": ("Pengendalian Emosi", "Ketenangan dalam menghadapi tekanan dan provokasi."),
    "N": ("Kebutuhan Menyelesaikan Tugas", "Dorongan kuat untuk menuntaskan pekerjaan sampai tuntas."),
    "A": ("Kebutuhan Berprestasi", "Dorongan untuk mencapai target yang menantang (Need for Achievement)."),
    "P": ("Kebutuhan Mengontrol", "Keinginan untuk memimpin dan memegang otoritas penuh."),
    "X": ("Kebutuhan Diperhatikan", "Keinginan mendapatkan apresiasi dan pengakuan publik."),
    "B": ("Kebutuhan Berkelompok", "Keinginan menjadi bagian dari kelompok kerja yang solid."),
    "O": ("Kebutuhan Kedekatan", "Keinginan menjalin persahabatan akrab di tempat kerja."),
    "Z": ("Kebutuhan Perubahan", "Kebutuhan akan variasi tugas dan keengganan pada rutinitas."),
    "K": ("Sikap Agresif / Asertif", "Ketegasan dalam mempertahankan pendapat."),
    "F": ("Kebutuhan Mendukung Atasan", "Loyalitas dan kepatuhan pada figur otoritas perusahaan."),
    "W": ("Kebutuhan Aturan / Pengawasan", "Kenyamanan bekerja dengan petunjuk pelaksanaan dan SOP baku."),
}


def evaluate_papi_kostick(raw_scores: Dict[str, int]) -> Dict[str, Any]:
    """
    Mengevaluasi skor mentah PAPI Kostick (skala 0 - 9 per dimensi).
    """
    profile = {}
    for code, (label, desc) in PAPI_DIMENSIONS.items():
        score = raw_scores.get(code, 5)
        level = "Tinggi" if score >= 7 else ("Sedang" if score >= 4 else "Rendah")
        profile[code] = {
            "dimension": label,
            "description": desc,
            "score": score,
            "level": level,
        }

    # Analisis Indeks Kepemimpinan (L + P + I)
    leadership_idx = round((raw_scores.get("L", 5) + raw_scores.get("P", 5) + raw_scores.get("I", 5)) / 3.0, 1)
    
    # Analisis Indeks Ketelitian & Kepatuhan (D + C + W)
    compliance_idx = round((raw_scores.get("D", 5) + raw_scores.get("C", 5) + raw_scores.get("W", 5)) / 3.0, 1)

    return {
        "dimensions": profile,
        "indices": {
            "leadership_potential": {
                "score": leadership_idx,
                "category": "Kuat" if leadership_idx >= 6.5 else "Moderat",
            },
            "detail_and_compliance": {
                "score": compliance_idx,
                "category": "Sangat Teliti" if compliance_idx >= 6.5 else "Adaptif",
            },
        },
        "hr_summary": f"Indeks Kepemimpinan: {leadership_idx}/9 | Indeks Kepatuhan & Ketelitian: {compliance_idx}/9.",
    }
