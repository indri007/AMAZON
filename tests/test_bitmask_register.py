"""
test_bitmask_register.py
Unit tests for 16-bit installment register bitmask operations in Python & Assembly logic.
"""

import unittest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "assembly"))

from angsuran_bitmask import (
    SiswaAngsuranBit,
    TARGET_LUNAS_MASK,
    NOMINAL_PER_ANGSURAN,
    TOTAL_TARGET,
    FLAG_IS_LUNAS
)

class TestBitmaskRegister(unittest.TestCase):

    def setUp(self):
        self.siswa = SiswaAngsuranBit(id_siswa=1, nama="Ahmad", no_wa="081234567890")

    def test_initial_register_state(self):
        self.assertEqual(self.siswa.reg, 0x0000)
        self.assertEqual(self.siswa.hitung_angsuran_masuk(), 0)
        self.assertEqual(self.siswa.total_bayar(), 0)
        self.assertEqual(self.siswa.sisa_tunggakan(), TOTAL_TARGET)
        self.assertFalse(self.siswa.status_lunas())

    def test_single_payment(self):
        self.siswa.bayar_angsuran(1) # bit 0
        self.assertEqual(self.siswa.reg, 0x0001)
        self.assertEqual(self.siswa.hitung_angsuran_masuk(), 1)
        self.assertEqual(self.siswa.total_bayar(), NOMINAL_PER_ANGSURAN)
        self.assertEqual(self.siswa.sisa_tunggakan(), TOTAL_TARGET - NOMINAL_PER_ANGSURAN)
        self.assertFalse(self.siswa.status_lunas())

    def test_partial_payments(self):
        # Bayar angsuran 1, 3, 5
        self.siswa.bayar_angsuran(1)
        self.siswa.bayar_angsuran(3)
        self.siswa.bayar_angsuran(5)
        expected_mask = (1 << 0) | (1 << 2) | (1 << 4) # 1 + 4 + 16 = 21 (0x0015)
        self.assertEqual(self.siswa.reg & TARGET_LUNAS_MASK, expected_mask)
        self.assertEqual(self.siswa.hitung_angsuran_masuk(), 3)
        self.assertEqual(self.siswa.total_bayar(), 3 * NOMINAL_PER_ANGSURAN)

    def test_full_payment_lunas_status(self):
        # Bayar 10x angsuran
        for i in range(1, 11):
            self.siswa.bayar_angsuran(i)
        
        self.assertTrue(self.siswa.status_lunas())
        self.assertEqual(self.siswa.hitung_angsuran_masuk(), 10)
        self.assertEqual(self.siswa.total_bayar(), TOTAL_TARGET)
        self.assertEqual(self.siswa.sisa_tunggakan(), 0)
        # 10 bit lower harus menyala (0x03FF) dan bit 15 menyala (FLAG_IS_LUNAS = 0x8000)
        self.assertEqual(self.siswa.reg & TARGET_LUNAS_MASK, TARGET_LUNAS_MASK)
        self.assertTrue(bool(self.siswa.reg & FLAG_IS_LUNAS))

    def test_invalid_installment_index(self):
        with self.assertRaises(AssertionError):
            self.siswa.bayar_angsuran(0)
        with self.assertRaises(AssertionError):
            self.siswa.bayar_angsuran(11)

if __name__ == "__main__":
    unittest.main()
