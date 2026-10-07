"""src/psikologi/kraepelin.py - Modul Simulasi Tes Kraepelin / Pauli untuk HRD.

Mengukur performa kerja dasar kandidat:
1. Kecepatan Kerja (Panker) - kuantitas output per satuan waktu
2. Ketelitian Kerja (Tianker) - tingkat kesalahan / error rate
3. Kestabilan Kerja (Stanker) - konsistensi ritme tanpa fluktuasi ekstrem
4. Ketahanan Kerja (Hanker) - daya tahan terhadap kejenuhan dan stres mental
"""

import math
from typing import List, Dict, Any


def evaluate_kraepelin_performance(columns_data: List[Dict[str, int]]) -> Dict[str, Any]:
    """
    Mengevaluasi hasil lembar kerja Kraepelin/Pauli.
    columns_data: List berisi dict per kolom:
      [
        {"attempted": 35, "correct": 34, "errors": 1},
        {"attempted": 38, "correct": 36, "errors": 2},
        ...
      ]
    """
    if not columns_data:
        return {"error": "Data kolom kosong"}

    total_attempted = sum(c.get("attempted", 0) for c in columns_data)
    total_correct = sum(c.get("correct", 0) for c in columns_data)
    total_errors = sum(c.get("errors", 0) for c in columns_data)
    n_cols = len(columns_data)

    # 1. Panker (Kecepatan Kerja): rata-rata output per kolom
    panker = round(total_attempted / n_cols, 2)

    # 2. Tianker (Ketelitian Kerja): persentase akurasi
    accuracy_pct = round((total_correct / max(total_attempted, 1)) * 100, 2)
    error_pct = round((total_errors / max(total_attempted, 1)) * 100, 2)

    # 3. Stanker (Kestabilan Kerja): deviasi standar output per kolom
    outputs = [c.get("attempted", 0) for c in columns_data]
    mean_out = sum(outputs) / len(outputs)
    variance = sum((x - mean_out) ** 2 for x in outputs) / len(outputs)
    stanker = round(math.sqrt(variance), 2)

    # 4. Hanker (Ketahanan Kerja / Tren kurva): membandingkan paruh akhir vs paruh awal
    half = n_cols // 2
    first_half = sum(outputs[:half]) / max(half, 1)
    second_half = sum(outputs[half:]) / max(n_cols - half, 1)
    trend_slope = round(second_half - first_half, 2)

    if trend_slope > 1.5:
        endurance_status = "Meningkat Positif (Motivasi tinggi seiring waktu)"
    elif trend_slope >= -1.5:
        endurance_status = "Stabil Konsisten (Daya tahan kerja prima)"
    else:
        endurance_status = "Menurun (Mengalami kelelahan mental / burnout cepat)"

    # Status Rekomendasi HR
    passed = (panker >= 25.0) and (accuracy_pct >= 90.0) and (stanker <= 6.0)

    return {
        "total_columns": n_cols,
        "total_attempted": total_attempted,
        "total_correct": total_correct,
        "total_errors": total_errors,
        "metrics": {
            "panker_kecepatan": {
                "value": panker,
                "benchmark": ">= 25 item/kolom",
                "status": "Baik" if panker >= 25 else "Perlu Ditingkatkan",
            },
            "tianker_ketelitian": {
                "accuracy_pct": accuracy_pct,
                "error_pct": error_pct,
                "benchmark": "Akurasi >= 90%",
                "status": "Teliti" if accuracy_pct >= 90 else "Tinggi Kesalahan",
            },
            "stanker_kestabilan": {
                "std_deviation": stanker,
                "benchmark": "<= 5.0 (makin kecil makin stabil)",
                "status": "Konsisten" if stanker <= 5.0 else "Fluktuatif",
            },
            "hanker_daya_tahan": {
                "slope": trend_slope,
                "status": endurance_status,
            },
        },
        "hr_recommendation": "DIREKOMENDASIKAN (Memenuhi Standar Daya Tahan Stres)" if passed else "DIPERTIMBANGKAN DENGAN CATATAN",
    }
