"""angsuran_bitmask.py - Solusi Arsitektur Bahasa Bit (16-Bit Bitmask)
Pencatatan Angsuran 10x Rp130.000 (Total Rp1.300.000) per Siswa.
"""

from typing import Dict, List, Any

# Bitmask target lunas 10 angsuran: 0b0000_0011_1111_1111 (0x03FF = 1023 desimal)
TARGET_LUNAS_MASK = 0x03FF
NOMINAL_PER_ANGSURAN = 130_000
TOTAL_TARGET = 1_300_000

# Flag tambahan (Bit 10 - 15)
FLAG_OVERDUE = 1 << 10        # Bit 10: Ada tunggakan lewat jatuh tempo
FLAG_REMINDER_SENT = 1 << 11  # Bit 11: Pengingat sudah terkirim
FLAG_SUBSIDI = 1 << 12        # Bit 12: Bantuan keringanan siswa
FLAG_IS_LUNAS = 1 << 15       # Bit 15: Status Lunas Penuh

class SiswaAngsuranBit:
    def __init__(self, id_siswa: int, nama: str, no_wa: str, register_awal: int = 0x0000):
        self.id_siswa = id_siswa
        self.nama = nama
        self.no_wa = no_wa
        self.reg = register_awal

    def bayar_angsuran(self, cicilan_ke: int):
        """Set bit cicilan ke-N menjadi 1 (Bitwise OR)."""
        assert 1 <= cicilan_ke <= 10, "Angsuran harus antara 1 sampai 10"
        self.reg |= (1 << (cicilan_ke - 1))
        # Jika semua 10 bit menyala, set bit lunas
        if (self.reg & TARGET_LUNAS_MASK) == TARGET_LUNAS_MASK:
            self.reg |= FLAG_IS_LUNAS

    def hitung_angsuran_masuk(self) -> int:
        """Menghitung jumlah bit 1 pada 10 bit pertama (Population Count)."""
        mask_cicilan = self.reg & TARGET_LUNAS_MASK
        return bin(mask_cicilan).count("1")

    def total_bayar(self) -> int:
        return self.hitung_angsuran_masuk() * NOMINAL_PER_ANGSURAN

    def sisa_tunggakan(self) -> int:
        return TOTAL_TARGET - self.total_bayar()

    def status_lunas(self) -> bool:
        return bool(self.reg & FLAG_IS_LUNAS) or ((self.reg & TARGET_LUNAS_MASK) == TARGET_LUNAS_MASK)

    def generate_wa_reminder(self, periode_berjalan: int) -> str:
        """Buat pesan jika bit periode_berjalan masih 0."""
        bit_pos = 1 << (periode_berjalan - 1)
        if not (self.reg & bit_pos):
            self.reg |= FLAG_REMINDER_SENT
            return (f"Yth. Wali dari {self.nama}, angsuran ke-{periode_berjalan} "
                    f"(Rp{NOMINAL_PER_ANGSURAN:,}) belum tercatat. "
                    f"Sisa tunggakan: Rp{self.sisa_tunggakan():,}. Terima kasih.")
        return ""

    def dump_register(self) -> str:
        """Tampilkan visual biner 16-bit."""
        b_str = f"{self.reg:016b}"
        return f"{b_str[:4]} {b_str[4:8]} {b_str[8:12]} {b_str[12:]}b (0x{self.reg:04X})"

def demo():
    print("=" * 70)
    print("⚙️  DEMO SISTEM PENCATATAN ANGSURAN 16-BIT BITMASK")
    print("=" * 70)

    siswa1 = SiswaAngsuranBit(101, "Ahmad Faiz", "08123456789")
    siswa2 = SiswaAngsuranBit(102, "Siti Nurhaliza", "08129876543")

    # Ahmad bayar angsuran 1, 2, 3
    siswa1.bayar_angsuran(1)
    siswa1.bayar_angsuran(2)
    siswa1.bayar_angsuran(3)

    # Siti bayar lunas semua (1 s/d 10)
    for i in range(1, 11):
        siswa2.bayar_angsuran(i)

    for s in [siswa1, siswa2]:
        print(f"Nama Siswa      : {s.nama}")
        print(f"Register Biner  : {s.dump_register()}")
        print(f"Angsuran Masuk  : {s.hitung_angsuran_masuk()} / 10 kali")
        print(f"Total Uang Masuk: Rp{s.total_bayar():,}")
        print(f"Sisa Tunggakan  : Rp{s.sisa_tunggakan():,}")
        print(f"Status Akhir    : {'LUNAS' if s.status_lunas() else 'BELUM LUNAS'}")
        reminder = s.generate_wa_reminder(periode_berjalan=4)
        if reminder:
            print(f"Pesan Pengingat : \"{reminder}\"")
        print("-" * 70)

if __name__ == "__main__":
    demo()
