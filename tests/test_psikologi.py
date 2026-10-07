"""tests/test_psikologi.py - Unit test suite untuk modul asesmen psikologi & assessment center."""

import pytest
from src.psikologi import (
    calculate_disc_score,
    calculate_mbti_score,
    calculate_big_five_score,
    calculate_riasec_score,
    evaluate_kraepelin_performance,
    evaluate_papi_kostick,
    evaluate_in_basket_decisions,
    evaluate_bei_star_response,
    generate_candidate_assessment_report,
)


class TestPsikologiModules:
    def test_disc_dominant_profile(self):
        # Jawaban mayoritas D
        answers = ["D", "D", "D", "D", "I", "C"]
        result = calculate_disc_score(answers)
        assert result["primary_type"] == "D"
        assert result["raw_counts"]["D"] == 4
        assert "Dominance" in result["title"]
        assert len(result["ideal_roles"]) > 0

    def test_disc_conscientiousness_profile(self):
        answers = ["C", "C", "C", "C", "S", "D"]
        result = calculate_disc_score(answers)
        assert result["primary_type"] == "C"
        assert "Conscientiousness" in result["title"]

    def test_mbti_intj_scoring(self):
        # 1: I, 2: I, 3: N, 4: N, 5: T, 6: T, 7: J, 8: J
        answers = {1: "B", 2: "B", 3: "B", 4: "B", 5: "A", 6: "A", 7: "A", 8: "A"}
        result = calculate_mbti_score(answers)
        assert result["mbti_type"] == "INTJ"
        assert result["archetype"] == "The Architect / Mastermind"
        assert "Software Architect" in result["recommended_careers"]

    def test_big_five_ocean_scoring(self):
        responses = {1: 5, 2: 5, 3: 5, 4: 5, 5: 4, 6: 4, 7: 5, 8: 4, 9: 1, 10: 2}
        result = calculate_big_five_score(responses)
        traits = result["traits"]
        assert traits["O"]["level"] == "Tinggi"
        assert traits["C"]["level"] == "Tinggi"
        assert result["emotional_stability_score"] >= 70.0

    def test_riasec_holland_code(self):
        # Skor tinggi pada I (Investigative), S (Social), E (Enterprising)
        responses = {1: 2, 2: 5, 3: 2, 4: 5, 5: 5, 6: 2, 7: 1, 8: 5, 9: 2, 10: 5, 11: 4, 12: 2}
        result = calculate_riasec_score(responses)
        assert len(result["holland_code"]) == 3
        assert len(result["top_roles"]) >= 3

    def test_kraepelin_high_performance(self):
        columns = [
            {"attempted": 30, "correct": 29, "errors": 1},
            {"attempted": 32, "correct": 31, "errors": 1},
            {"attempted": 34, "correct": 33, "errors": 1},
            {"attempted": 35, "correct": 35, "errors": 0},
        ]
        result = evaluate_kraepelin_performance(columns)
        assert result["metrics"]["panker_kecepatan"]["value"] >= 30.0
        assert result["metrics"]["tianker_ketelitian"]["accuracy_pct"] >= 95.0
        assert "DIREKOMENDASIKAN" in result["hr_recommendation"]

    def test_papi_kostick_evaluation(self):
        scores = {"L": 8, "P": 7, "I": 8, "G": 7, "D": 6, "C": 7, "W": 6}
        result = evaluate_papi_kostick(scores)
        assert result["indices"]["leadership_potential"]["category"] == "Kuat"
        assert "Indeks Kepemimpinan" in result["hr_summary"]

    def test_in_basket_assessment(self):
        decisions = [
            {"memo_id": "MEMO-01", "priority": "High-Urgent", "action_notes": "Segera menghubungi tim bea cukai dan mengarahkan manajer produksi untuk skenario darurat."},
            {"memo_id": "MEMO-02", "priority": "High-Important", "action_notes": "Review langsung dengan seluruh tim supervisor untuk finalisasi KPI tepat waktu."},
        ]
        result = evaluate_in_basket_decisions(decisions)
        assert result["score_out_of_100"] > 0
        assert len(result["memo_feedbacks"]) == 2

    def test_bei_star_evaluation(self):
        answer = (
            "Pada waktu proyek sistem HR tahun lalu, tugas saya adalah memimpin integrasi data 500 karyawan. "
            "Saya melakukan restrukturisasi skema database dan membuat script validasi otomatis. "
            "Hasilnya proses migrasi berhasil tanpa kendala dan efisiensi waktu meningkat 40%."
        )
        result = evaluate_bei_star_response(answer, competency="Problem Solving")
        assert result["star_completeness_score"] == 100
        assert result["star_rating"] == "4/4 Elemen STAR Terpenuhi"

    def test_candidate_report_generation(self):
        disc = calculate_disc_score(["D", "D", "D", "D", "I", "C"])
        mbti = calculate_mbti_score({1: "B", 2: "B", 3: "B", 4: "B", 5: "A", 6: "A", 7: "A", 8: "A"})
        report = generate_candidate_assessment_report(
            candidate_name="Indri Anjar",
            target_position="HR Operations Lead",
            disc_result=disc,
            mbti_result=mbti,
        )
        assert report["candidate_name"] == "Indri Anjar"
        assert "LAPORAN HASIL ASESMEN PSIKOLOGI" in report["markdown_report"]
        assert report["overall_recommendation"] == "DIREKOMENDASIKAN"
