/*
 * test_angsuran_arm64.c
 * Implementasi & Pengujian Register Angsuran 16-Bit
 * Porting langsung dari angsuran_bitmask.asm ke ARM64 Assembly (Apple Silicon macOS)
 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define MASK_ANGSURAN   0x03FF
#define BIT_LUNAS_PENUH 0x8000
#define JUMLAH_ANGSURAN 10
#define NOMINAL         130000

// catat_angsuran: set bit N-1 (1..10) via ARM64 BFI / ORR
static inline uint16_t catat_angsuran(uint16_t reg, int n) {
    if (n < 1 || n > JUMLAH_ANGSURAN) return reg;
    uint32_t r = reg, shift = n - 1;
    uint32_t bitmask;
    __asm__ ("mov %w[m], #1 \n\t"
             "lsl %w[m], %w[m], %w[sh] \n\t"
             "orr %w[out], %w[in], %w[m]"
             : [out] "=r" (r), [m] "=&r" (bitmask)
             : [in] "r" (r), [sh] "r" (shift));
    return (uint16_t)r;
}

// hitung_bayar: popcount(reg & 0x03FF)
static inline int hitung_bayar(uint16_t reg) {
    return __builtin_popcount(reg & MASK_ANGSURAN);
}

// is_lunas: 1 bila (reg & 0x03FF) == 0x03FF
static inline int is_lunas(uint16_t reg) {
    uint32_t res;
    uint32_t val = reg & MASK_ANGSURAN;
    __asm__ ("cmp %w[v], %w[mask] \n\t"
             "cset %w[r], eq"
             : [r] "=r" (res)
             : [v] "r" (val), [mask] "r" (MASK_ANGSURAN)
             : "cc");
    return (int)res;
}

// tandai_lunas: nyalakan MSB (0x8000) bila lunas
static inline uint16_t tandai_lunas(uint16_t reg) {
    if (is_lunas(reg)) {
        return reg | BIT_LUNAS_PENUH;
    }
    return reg;
}

static inline int uang_masuk(uint16_t reg) {
    return hitung_bayar(reg) * NOMINAL;
}

static inline int sisa_tunggakan(uint16_t reg) {
    return (JUMLAH_ANGSURAN - hitung_bayar(reg)) * NOMINAL;
}

// perlu_pengingat: 1 bila bit K-1 masih 0
static inline int perlu_pengingat(uint16_t reg, int k) {
    int shift = k - 1;
    return ((reg >> shift) & 1) == 0;
}

static int fail_count = 0;

static void assert_val(int actual, int expected, const char* label) {
    if (actual == expected) {
        printf("  [LULUS] %s\n", label);
    } else {
        printf("  [GAGAL] %s (aktual=%d, harapan=%d)\n", label, actual, expected);
        fail_count++;
    }
}

static void cetak_laporan(uint16_t reg) {
    printf("  Kali bayar : %d\n", hitung_bayar(reg));
    printf("  Uang masuk : Rp%d\n", uang_masuk(reg));
    printf("  Sisa       : Rp%d\n", sisa_tunggakan(reg));
    printf("  Status     : %s\n", is_lunas(reg) ? "LUNAS" : "BELUM LUNAS");
}

int main(void) {
    printf("== UJI REGISTER ANGSURAN 16-BIT (ARM64 Apple Silicon) ==\n\n");

    // ---- Skenario A: Siswa bayar angsuran 1, 2, 3 ------------------------
    printf("[Skenario A] Siswa bayar angsuran 1, 2, 3\n");
    uint16_t reg_a = 0;
    reg_a = catat_angsuran(reg_a, 1);
    reg_a = catat_angsuran(reg_a, 2);
    reg_a = catat_angsuran(reg_a, 3);
    assert_val(reg_a, 0x0007, "register = 0x0007");

    cetak_laporan(reg_a);

    assert_val(hitung_bayar(reg_a), 3, "kali bayar = 3");
    assert_val(uang_masuk(reg_a), 390000, "uang masuk = 390000");
    assert_val(sisa_tunggakan(reg_a), 910000, "sisa = 910000");
    assert_val(is_lunas(reg_a), 0, "belum lunas (is_lunas = 0)");
    assert_val(perlu_pengingat(reg_a, 4), 1, "pengingat periode 4 menyala");

    // ---- Skenario B: Siswa bayar angsuran 1 s/d 10 -----------------------
    printf("\n[Skenario B] Siswa bayar angsuran 1 s/d 10\n");
    uint16_t reg_b = 0;
    for (int i = 1; i <= JUMLAH_ANGSURAN; i++) {
        reg_b = catat_angsuran(reg_b, i);
    }
    assert_val(reg_b, 0x03FF, "register = 0x03FF");

    reg_b = tandai_lunas(reg_b);
    assert_val(reg_b, 0x83FF, "setelah tandai_lunas register = 0x83FF");

    cetak_laporan(reg_b);

    assert_val(hitung_bayar(reg_b), 10, "kali bayar = 10");
    assert_val(uang_masuk(reg_b), 1300000, "uang masuk = 1300000");
    assert_val(sisa_tunggakan(reg_b), 0, "sisa = 0");
    assert_val(is_lunas(reg_b), 1, "lunas (is_lunas = 1)");
    assert_val(perlu_pengingat(reg_b, 4), 0, "pengingat periode 4 tidak menyala");

    // ---- Skenario C: Idempoten dan masukan tidak valid ------------------
    printf("\n[Skenario C] Pencatatan ganda dan angsuran tidak valid\n");
    uint16_t reg_c = 0x0007;
    reg_c = catat_angsuran(reg_c, 2); // catat ulang angsuran 2
    assert_val(reg_c, 0x0007, "catat angsuran 2 dua kali: register tetap 0x0007 (idempoten)");

    reg_c = catat_angsuran(reg_c, 11); // angsuran 11 tidak valid
    assert_val(reg_c, 0x0007, "angsuran ke-11 ditolak: register tidak berubah");

    printf("\n------------------------------------------------------------\n");
    if (fail_count == 0) {
        printf("SEMUA UJI LULUS (Exit Code 0)\n");
        return 0;
    } else {
        printf("ADA %d UJI GAGAL (Exit Code 1)\n", fail_count);
        return 1;
    }
}
