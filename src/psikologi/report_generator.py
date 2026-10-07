"""src/psikologi/report_generator.py - Generator Laporan Psikologi Terintegrasi.

Menghasilkan ringkasan laporan psikologi & assessment center kandidat untuk:
- Rekrutmen & Seleksi Karyawan Baru
- Talent Mapping & Suksesi Kepemimpinan
- Promosi Jabatan & Pelatihan Terarah
"""

from typing import Dict, Any
from datetime import datetime


def generate_candidate_assessment_report(
    candidate_name: str,
    target_position: str,
    disc_result: Dict[str, Any] = None,
    mbti_result: Dict[str, Any] = None,
    big_five_result: Dict[str, Any] = None,
    riasec_result: Dict[str, Any] = None,
    kraepelin_result: Dict[str, Any] = None,
    assessment_center_result: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Menyusun profil psikologi lengkap kandidat."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    overall_recommendation = "DIREKOMENDASIKAN"
    risk_factors = []

    # Cek konsistensi dan faktor risiko
    if kraepelin_result and "DIPERTIMBANGKAN" in kraepelin_result.get("hr_recommendation", ""):
        risk_factors.append("Ketahanan kerja dan stabilitas di bawah tekanan perlu pendampingan.")
        overall_recommendation = "DIPERTIMBANGKAN"

    report_markdown = f"""# 📑 LAPORAN HASIL ASESMEN PSIKOLOGI & ASSESSMENT CENTER

**Nama Kandidat:** {candidate_name}  
**Posisi yang Dituju:** {target_position}  
**Tanggal Asesmen:** {timestamp}  
**Status Rekomendasi:** **{overall_recommendation}**  

---

### 1. Profil Kepribadian & Gaya Kerja (DISC & MBTI)
"""
    if disc_result:
        report_markdown += f"- **DISC Profile:** {disc_result.get('title')} ({disc_result.get('primary_type')})\n"
        report_markdown += f"  - *Ringkasan:* {disc_result.get('summary')}\n"
        report_markdown += f"  - *Kekuatan Utama:* {', '.join(disc_result.get('strengths', []))}\n"

    if mbti_result:
        report_markdown += f"- **MBTI Type:** **{mbti_result.get('mbti_type')}** ({mbti_result.get('archetype')})\n"
        report_markdown += f"  - *Deskripsi:* {mbti_result.get('description')}\n"
        report_markdown += f"  - *Rekomendasi Peran:* {', '.join(mbti_result.get('recommended_careers', []))}\n"

    report_markdown += "\n### 2. Minat Karier & Kecocokan Tugas (Holland RIASEC)\n"
    if riasec_result:
        report_markdown += f"- **Holland Code:** **{riasec_result.get('holland_code')}**\n"
        report_markdown += f"- **Fokus Minat:** {riasec_result.get('primary_interest')} & {riasec_result.get('secondary_interest')}\n"
        report_markdown += f"- **Peran Ideal:** {', '.join(riasec_result.get('top_roles', []))}\n"

    report_markdown += "\n### 3. Ketahanan Mental & Daya Tahan Kerja (Kraepelin)\n"
    if kraepelin_result:
        metrics = kraepelin_result.get("metrics", {})
        panker = metrics.get("panker_kecepatan", {}).get("value", "-")
        tianker = metrics.get("tianker_ketelitian", {}).get("accuracy_pct", "-")
        hanker = metrics.get("hanker_daya_tahan", {}).get("status", "-")
        report_markdown += f"- **Kecepatan Kerja (Panker):** {panker} item/menit\n"
        report_markdown += f"- **Akurasi (Tianker):** {tianker}%\n"
        report_markdown += f"- **Kurva Daya Tahan (Hanker):** {hanker}\n"

    report_markdown += "\n### 4. Kompetensi Manajerial (Assessment Center)\n"
    if assessment_center_result:
        score = assessment_center_result.get("score_out_of_100", "-")
        lvl = assessment_center_result.get("assessment_level", "-")
        report_markdown += f"- **In-Basket Skor:** {score}/100 ({lvl})\n"

    report_markdown += f"\n---\n### 🎯 Kesimpulan & Rekomendasi HR:\n**{overall_recommendation}** untuk posisi {target_position}."
    if risk_factors:
        report_markdown += f"\n*Catatan Pengembangan:* {'; '.join(risk_factors)}"

    return {
        "candidate_name": candidate_name,
        "target_position": target_position,
        "assessment_timestamp": timestamp,
        "overall_recommendation": overall_recommendation,
        "risk_factors": risk_factors,
        "markdown_report": report_markdown,
    }
