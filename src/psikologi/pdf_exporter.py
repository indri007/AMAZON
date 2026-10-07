"""src/psikologi/pdf_exporter.py - Generator Laporan PDF Resmi Asesmen Psikologi & Assessment Center HRD."""

import io
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_assessment_pdf_report(
    candidate_name: str,
    target_position: str,
    disc_result: Optional[Dict[str, Any]] = None,
    mbti_result: Optional[Dict[str, Any]] = None,
    riasec_result: Optional[Dict[str, Any]] = None,
    kraepelin_result: Optional[Dict[str, Any]] = None,
    in_basket_result: Optional[Dict[str, Any]] = None,
) -> bytes:
    """Menghasilkan berkas PDF laporan psikotes dan assessment center formal dalam bentuk bytes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    c_primary = colors.HexColor("#0F172A")
    c_secondary = colors.HexColor("#1E293B")
    c_accent = colors.HexColor("#0284C7")
    c_slate = colors.HexColor("#475569")
    c_emerald = colors.HexColor("#059669")

    style_company = ParagraphStyle(
        "CompanyHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=c_primary,
        alignment=1,  # Center
    )
    style_sub_company = ParagraphStyle(
        "CompanySubHeader",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=c_slate,
        alignment=1,
    )
    style_doc_title = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=c_accent,
        alignment=1,
        spaceAfter=6,
    )
    style_section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=c_secondary,
        spaceBefore=8,
        spaceAfter=4,
    )
    style_body = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#1E293B"),
    )
    style_body_bold = ParagraphStyle(
        "BodyDarkBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11.5,
        textColor=c_primary,
    )
    style_badge = ParagraphStyle(
        "BadgeText",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.white,
        alignment=1,
    )

    story = []

    # 1. HEADER KOP SURAT
    story.append(Paragraph("PT AMAZON NUSANTARA TEKNOLOGI", style_company))
    story.append(Paragraph("DIVISI TALENT ACQUISITION & ORGANIZATIONAL DEVELOPMENT", style_company))
    story.append(Paragraph("Gedung Cyber Tower Lt. 18, Jakarta Selatan | Telp: (021) 7892-0000 | Email: hrd@amazon-corp.id", style_sub_company))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=8))

    story.append(Paragraph("LAPORAN RESMI ASESMEN PSIKOLOGI & ASSESSMENT CENTER", style_doc_title))

    # 2. METADATA KANDIDAT TABLE
    tgl_now = datetime.now().strftime("%d %B %Y - %H:%M WIB")
    doc_num = f"AMAZON/HR-PSY/{datetime.now().strftime('%Y%m')}/{abs(hash(candidate_name)) % 10000:04d}"

    meta_data = [
        [
            Paragraph("<b>Nama Kandidat:</b>", style_body), Paragraph(candidate_name or "-", style_body_bold),
            Paragraph("<b>Nomor Dokumen:</b>", style_body), Paragraph(doc_num, style_body),
        ],
        [
            Paragraph("<b>Posisi Target:</b>", style_body), Paragraph(target_position or "-", style_body_bold),
            Paragraph("<b>Tanggal Asesmen:</b>", style_body), Paragraph(tgl_now, style_body),
        ],
    ]
    meta_table = Table(meta_data, colWidths=[90, 170, 95, 165])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # 3. BAGIAN I: PROFIL KEPRIBADIAN (DISC & MBTI)
    story.append(Paragraph("I. HASIL ASESMEN KEPRIBADIAN & GAYA KERJA", style_section_heading))

    table_p_data = [
        [Paragraph("<b>Instrumen</b>", style_body_bold), Paragraph("<b>Hasil / Klasifikasi</b>", style_body_bold), Paragraph("<b>Interpretasi & Implikasi Kerja</b>", style_body_bold)]
    ]

    if disc_result:
        pcts = disc_result.get("percentages", {})
        disc_summary = (
            f"<b>Distribusi:</b> D: {pcts.get('D', 0)}% | I: {pcts.get('I', 0)}% | S: {pcts.get('S', 0)}% | C: {pcts.get('C', 0)}%<br/>"
            f"<b>Kekuatan:</b> {', '.join(disc_result.get('strengths', [])[:2])}<br/>"
            f"<b>Peran Ideal:</b> {', '.join(disc_result.get('ideal_roles', [])[:2])}"
        )
        table_p_data.append([
            Paragraph("<b>DISC Assessment</b>", style_body_bold),
            Paragraph(f"<b>{disc_result.get('title', '-')}</b>", style_body_bold),
            Paragraph(disc_summary, style_body),
        ])

    if mbti_result:
        mbti_summary = (
            f"<b>Archetype:</b> {mbti_result.get('archetype', '-')}<br/>"
            f"<b>Karakteristik:</b> {mbti_result.get('description', '-')}<br/>"
            f"<b>Karier Rekomendasi:</b> {', '.join(mbti_result.get('recommended_careers', [])[:3])}"
        )
        table_p_data.append([
            Paragraph("<b>MBTI (16 Types)</b>", style_body_bold),
            Paragraph(f"<b>Tipe: {mbti_result.get('mbti_type', '-')}</b>", style_body_bold),
            Paragraph(mbti_summary, style_body),
        ])

    if not disc_result and not mbti_result:
        table_p_data.append([
            Paragraph("-", style_body), Paragraph("Belum Diujikan", style_body), Paragraph("Data kuesioner kepribadian belum terisi.", style_body)
        ])

    table_p = Table(table_p_data, colWidths=[100, 150, 270])
    table_p.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table_p)
    story.append(Spacer(1, 8))

    # 4. BAGIAN II: MINAT KARIER & KETAHANAN KERJA (RIASEC & KRAEPELIN)
    story.append(Paragraph("II. MINAT JABATAN & DAYA TAHAN STRES KERJA", style_section_heading))

    table_jk_data = [
        [Paragraph("<b>Instrumen</b>", style_body_bold), Paragraph("<b>Metrik / Skor</b>", style_body_bold), Paragraph("<b>Analisis Rekomendasi HR</b>", style_body_bold)]
    ]

    if riasec_result:
        riasec_text = (
            f"Fokus Minat: <b>{riasec_result.get('primary_interest')}</b> & <b>{riasec_result.get('secondary_interest')}</b><br/>"
            f"Kecocokan Posisi: {', '.join(riasec_result.get('top_roles', [])[:3])}"
        )
        table_jk_data.append([
            Paragraph("<b>Holland RIASEC</b>", style_body_bold),
            Paragraph(f"<b>Code: {riasec_result.get('holland_code', '-')}</b>", style_body_bold),
            Paragraph(riasec_text, style_body),
        ])

    if kraepelin_result:
        m = kraepelin_result.get("metrics", {})
        panker = m.get("panker_kecepatan", {}).get("value", "-")
        tianker = m.get("tianker_ketelitian", {}).get("accuracy_pct", "-")
        hanker = m.get("hanker_daya_tahan", {}).get("status", "-")
        k_text = (
            f"Kecepatan: <b>{panker}</b> itm/mnt | Akurasi: <b>{tianker}%</b><br/>"
            f"Daya Tahan: {hanker}<br/>"
            f"Status Rekomendasi: <b>{kraepelin_result.get('hr_recommendation', '-')}</b>"
        )
        table_jk_data.append([
            Paragraph("<b>Kraepelin / Pauli</b>", style_body_bold),
            Paragraph(f"<b>Akurasi: {tianker}%</b>", style_body_bold),
            Paragraph(k_text, style_body),
        ])

    if not riasec_result and not kraepelin_result:
        table_jk_data.append([
            Paragraph("-", style_body), Paragraph("Belum Diujikan", style_body), Paragraph("Data tes kerja belum terisi.", style_body)
        ])

    table_jk = Table(table_jk_data, colWidths=[100, 150, 270])
    table_jk.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(table_jk)
    story.append(Spacer(1, 8))

    # 5. BAGIAN III: SIMULASI ASSESSMENT CENTER (IN-BASKET)
    if in_basket_result:
        story.append(Paragraph("III. SIMULASI ASSESSMENT CENTER (IN-BASKET DECISIONS)", style_section_heading))
        ib_score = in_basket_result.get("score_out_of_100", 0)
        ib_level = in_basket_result.get("assessment_level", "-")

        ib_data = [
            [Paragraph("<b>Skor Keseluruhan:</b>", style_body_bold), Paragraph(f"<b>{ib_score} / 100 ({ib_level})</b>", style_body_bold)]
        ]
        for fb in in_basket_result.get("memo_feedbacks", [])[:3]:
            ib_data.append([
                Paragraph(f"<b>{fb.get('memo_id')}</b>", style_body),
                Paragraph(f"{fb.get('subject')}<br/>Pilihan: <code>{fb.get('user_priority')}</code> (Ideal: <b>{fb.get('ideal_priority')}</b>) - {fb.get('ideal_action')}", style_body),
            ])

        table_ib = Table(ib_data, colWidths=[120, 400])
        table_ib.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FEF3C7")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(table_ib)
        story.append(Spacer(1, 8))

    # 6. KESIMPULAN & REKOMENDASI PANEL ASESOR HRD
    story.append(Paragraph("IV. KESIMPULAN & REKOMENDASI AKHIR HRD", style_section_heading))

    is_rec = True
    if kraepelin_result and "DIPERTIMBANGKAN" in kraepelin_result.get("hr_recommendation", ""):
        is_rec = False
    if in_basket_result and in_basket_result.get("score_out_of_100", 100) < 60:
        is_rec = False

    status_str = "DIREKOMENDASIKAN (RECOMMENDED)" if is_rec else "DIPERTIMBANGKAN DENGAN CATATAN (CONSIDERED)"
    bg_color = c_emerald if is_rec else colors.HexColor("#D97706")

    badge_data = [[Paragraph(f"<b>STATUS: {status_str}</b>", style_badge)]]
    badge_table = Table(badge_data, colWidths=[520])
    badge_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(badge_table)
    story.append(Spacer(1, 8))

    notes = [
        f"1. Berdasarkan profil asesmen terpadu, kandidat menunjukkan kesesuaian kompetensi untuk posisi <b>{target_position}</b>.",
        "2. Gaya kerja dan preferensi komunikasi kandidat mendukung integrasi tim lintas fungsi secara efektif.",
        "3. Rekomendasi Program Pembinaan: Lanjutkan penajaman kompetensi melalui program On-the-Job Training dan mentoring 90 hari pertama.",
    ]
    for n in notes:
        story.append(Paragraph(n, style_body))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 14))

    # 7. TANDA TANGAN ASESOR
    sign_data = [
        [
            Paragraph("Diverifikasi Oleh:<br/><b>Tim Psikometri & Asesor HRD</b>", style_body),
            Paragraph("Mengetahui & Menyetujui:<br/><b>Head of Human Capital Development</b>", style_body),
        ],
        [
            Paragraph("<br/><br/><u>Dra. Indri Anjar Kartika Sari, M.Psi., Psikolog</u><br/>Lead Certified Assessor", style_body),
            Paragraph("<br/><br/><u>Director of Human Resources</u><br/>PT AMAZON Nusantara Teknologi", style_body),
        ],
    ]
    sign_table = Table(sign_data, colWidths=[260, 260])
    sign_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    story.append(sign_table)

    doc.build(story)
    return buffer.getvalue()
