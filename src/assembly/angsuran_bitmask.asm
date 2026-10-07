; ============================================================================
; angsuran_bitmask.asm  --  Register Status 16-Bit untuk Angsuran 10x Rp130.000
; Target : Linux x86-64, NASM, tanpa libc (hanya syscall write/exit)
;
; Rakit  : nasm -f elf64 angsuran_bitmask.asm -o angsuran_bitmask.o
; Tautkan: ld angsuran_bitmask.o -o angsuran_bitmask
; Jalan  : ./angsuran_bitmask ; echo $?     (exit code 0 = semua uji lulus)
;
; Tata letak register siswa (uint16, 2 byte per siswa):
;   bit 0..9  : angsuran ke-1 .. ke-10  (0 = belum, 1 = sudah)
;   bit 10    : lewat jatuh tempo
;   bit 11    : pengingat terkirim
;   bit 12    : keringanan / subsidi
;   bit 15    : lunas penuh (MSB, 0x8000)
; Lunas = (reg & 0x03FF) == 0x03FF
;
; Konvensi pemanggilan (sederhana, mirip System V):
;   argumen : edi = reg, esi = nomor angsuran / periode K (1..10)
;   hasil   : eax
;   rusak   : rax, rcx, rdx, rsi, rdi, r11 (rbx dan r12 disimpan bila dipakai)
; ============================================================================

bits 64
default rel

%define MASK_ANGSURAN   0x03FF
%define BIT_LUNAS_PENUH 0x8000
%define JUMLAH_ANGSURAN 10
%define NOMINAL         130000          ; Rp130.000 per angsuran

; ---------------------------------------------------------------- data ------
%macro STR 2                            ; STR nama, "isi",10
%1:     db %2
%1_len  equ $ - %1
%endmacro

%macro TULIS 2                          ; TULIS nama_string, panjang
        mov     eax, 1                  ; sys_write
        mov     edi, 1                  ; stdout
        lea     rsi, [%1]
        mov     edx, %2
        syscall
%endmacro

; ASSERT harapan, nama_pesan : bandingkan eax (aktual) dengan harapan
%macro ASSERT 2
        cmp     eax, %1
        je      %%ok
        inc     r13d                    ; hitung kegagalan
        TULIS   s_gagal, s_gagal_len
        jmp     %%cetak
%%ok:
        TULIS   s_lulus, s_lulus_len
%%cetak:
        TULIS   %2, %2_len
%endmacro

section .rodata
STR s_judul,  {"== UJI REGISTER ANGSURAN 16-BIT (NASM x86-64) ==",10}
STR s_skA,    {10,"[Skenario A] Siswa bayar angsuran 1, 2, 3",10}
STR s_skB,    {10,"[Skenario B] Siswa bayar angsuran 1 s/d 10",10}
STR s_skC,    {10,"[Skenario C] Pencatatan ganda dan angsuran tidak valid",10}
STR s_kb,     {"  Kali bayar : "}
STR s_um,     {"  Uang masuk : Rp"}
STR s_sisa,   {"  Sisa       : Rp"}
STR s_status, {"  Status     : "}
STR s_lunas_t,{"LUNAS",10}
STR s_belum_t,{"BELUM LUNAS",10}
STR s_nl,     {10}
STR s_lulus,  {"  [LULUS] "}
STR s_gagal,  {"  [GAGAL] "}
STR t_a_reg,  {"register = 0x0007",10}
STR t_a_kb,   {"kali bayar = 3",10}
STR t_a_um,   {"uang masuk = 390000",10}
STR t_a_sisa, {"sisa = 910000",10}
STR t_a_lns,  {"belum lunas (is_lunas = 0)",10}
STR t_a_rem,  {"pengingat periode 4 menyala",10}
STR t_b_reg,  {"register = 0x03FF",10}
STR t_b_msb,  {"setelah tandai_lunas register = 0x83FF",10}
STR t_b_kb,   {"kali bayar = 10",10}
STR t_b_um,   {"uang masuk = 1300000",10}
STR t_b_sisa, {"sisa = 0",10}
STR t_b_lns,  {"lunas (is_lunas = 1)",10}
STR t_b_rem,  {"pengingat periode 4 tidak menyala",10}
STR t_c_dup,  {"catat angsuran 2 dua kali: register tetap 0x0007 (idempoten)",10}
STR t_c_inv,  {"angsuran ke-11 ditolak: register tidak berubah",10}
STR s_ok,     {10,"SEMUA UJI LULUS",10}
STR s_fail,   {10,"ADA UJI GAGAL",10}

; ---------------------------------------------------------------- kode ------
section .text
global _start

; catat_angsuran: edi = reg, esi = N (1..10) -> eax = reg | (1 << (N-1))
; N di luar 1..10 diabaikan (reg dikembalikan apa adanya).
catat_angsuran:
        mov     eax, edi
        cmp     esi, 1
        jb      .selesai
        cmp     esi, JUMLAH_ANGSURAN
        ja      .selesai
        dec     esi
        bts     eax, esi                ; set bit N-1
.selesai:
        movzx   eax, ax                 ; jaga tetap 16-bit
        ret

; hitung_bayar: edi = reg -> eax = popcount(reg & 0x03FF)
hitung_bayar:
        and     edi, MASK_ANGSURAN
        popcnt  eax, edi
        ret

; is_lunas: edi = reg -> eax = 1 bila (reg & 0x03FF) == 0x03FF, selain itu 0
is_lunas:
        and     edi, MASK_ANGSURAN
        xor     eax, eax
        cmp     edi, MASK_ANGSURAN
        sete    al
        ret

; tandai_lunas: edi = reg -> eax = reg dengan MSB (0x8000) menyala bila lunas
tandai_lunas:
        push    rdi
        call    is_lunas
        pop     rdi
        mov     edx, edi
        or      edx, BIT_LUNAS_PENUH
        test    eax, eax
        cmovnz  edi, edx
        movzx   eax, di
        ret

; uang_masuk: edi = reg -> eax = kali_bayar * 130000
uang_masuk:
        call    hitung_bayar
        imul    eax, eax, NOMINAL
        ret

; sisa_tunggakan: edi = reg -> eax = (10 - kali_bayar) * 130000
sisa_tunggakan:
        call    hitung_bayar
        mov     edx, JUMLAH_ANGSURAN
        sub     edx, eax
        imul    eax, edx, NOMINAL
        ret

; perlu_pengingat: edi = reg, esi = K (1..10) -> eax = 1 bila bit K-1 masih 0
perlu_pengingat:
        dec     esi
        xor     eax, eax
        bt      edi, esi
        setnc   al
        ret

; cetak_angka: edi = bilangan tak bertanda -> tulis desimal ke stdout
cetak_angka:
        push    rbx
        sub     rsp, 32
        mov     eax, edi
        lea     rsi, [rsp + 31]
        mov     ebx, 10
        xor     ecx, ecx
.bagi:
        xor     edx, edx
        div     ebx
        add     dl, '0'
        mov     [rsi], dl
        dec     rsi
        inc     ecx
        test    eax, eax
        jnz     .bagi
        inc     rsi                     ; rsi -> digit pertama
        mov     edx, ecx                ; panjang
        mov     eax, 1
        mov     edi, 1
        syscall
        add     rsp, 32
        pop     rbx
        ret

; cetak_laporan: edi = reg -> tulis ringkasan kali bayar, uang masuk, sisa, status
cetak_laporan:
        push    r12
        mov     r12d, edi

        TULIS   s_kb, s_kb_len
        mov     edi, r12d
        call    hitung_bayar
        mov     edi, eax
        call    cetak_angka
        TULIS   s_nl, s_nl_len

        TULIS   s_um, s_um_len
        mov     edi, r12d
        call    uang_masuk
        mov     edi, eax
        call    cetak_angka
        TULIS   s_nl, s_nl_len

        TULIS   s_sisa, s_sisa_len
        mov     edi, r12d
        call    sisa_tunggakan
        mov     edi, eax
        call    cetak_angka
        TULIS   s_nl, s_nl_len

        TULIS   s_status, s_status_len
        mov     edi, r12d
        call    is_lunas
        test    eax, eax
        jz      .belum
        TULIS   s_lunas_t, s_lunas_t_len
        jmp     .selesai
.belum:
        TULIS   s_belum_t, s_belum_t_len
.selesai:
        pop     r12
        ret

; ------------------------------------------------------------ program uji ---
_start:
        xor     r13d, r13d              ; r13d = jumlah uji gagal
        TULIS   s_judul, s_judul_len

        ; ---- Skenario A: bayar angsuran 1, 2, 3 -----------------------------
        TULIS   s_skA, s_skA_len
        xor     edi, edi
        mov     esi, 1
        call    catat_angsuran
        mov     edi, eax
        mov     esi, 2
        call    catat_angsuran
        mov     edi, eax
        mov     esi, 3
        call    catat_angsuran
        mov     r12d, eax               ; r12d = register siswa A
        ASSERT  0x0007, t_a_reg

        mov     edi, r12d
        call    cetak_laporan

        mov     edi, r12d
        call    hitung_bayar
        ASSERT  3, t_a_kb
        mov     edi, r12d
        call    uang_masuk
        ASSERT  390000, t_a_um
        mov     edi, r12d
        call    sisa_tunggakan
        ASSERT  910000, t_a_sisa
        mov     edi, r12d
        call    is_lunas
        ASSERT  0, t_a_lns
        mov     edi, r12d
        mov     esi, 4
        call    perlu_pengingat
        ASSERT  1, t_a_rem

        ; ---- Skenario B: bayar angsuran 1 s/d 10 ---------------------------
        TULIS   s_skB, s_skB_len
        xor     r12d, r12d              ; reg awal = 0
        mov     r14d, 1                 ; N = 1
.loop_b:
        mov     edi, r12d
        mov     esi, r14d
        call    catat_angsuran
        mov     r12d, eax
        inc     r14d
        cmp     r14d, JUMLAH_ANGSURAN
        jbe     .loop_b
        mov     eax, r12d
        ASSERT  0x03FF, t_b_reg

        mov     edi, r12d
        call    tandai_lunas
        mov     r12d, eax
        ASSERT  0x83FF, t_b_msb

        mov     edi, r12d
        call    cetak_laporan

        mov     edi, r12d
        call    hitung_bayar
        ASSERT  10, t_b_kb
        mov     edi, r12d
        call    uang_masuk
        ASSERT  1300000, t_b_um
        mov     edi, r12d
        call    sisa_tunggakan
        ASSERT  0, t_b_sisa
        mov     edi, r12d
        call    is_lunas
        ASSERT  1, t_b_lns
        mov     edi, r12d
        mov     esi, 4
        call    perlu_pengingat
        ASSERT  0, t_b_rem

        ; ---- Skenario C: idempoten dan masukan tidak valid -----------------
        TULIS   s_skC, s_skC_len
        mov     edi, 0x0007
        mov     esi, 2                  ; angsuran 2 sudah tercatat
        call    catat_angsuran
        ASSERT  0x0007, t_c_dup
        mov     edi, 0x0007
        mov     esi, 11                 ; angsuran ke-11 tidak ada
        call    catat_angsuran
        ASSERT  0x0007, t_c_inv

        ; ---- Ringkasan dan keluar ------------------------------------------
        test    r13d, r13d
        jnz     .ada_gagal
        TULIS   s_ok, s_ok_len
        xor     edi, edi                ; exit code 0
        jmp     .keluar
.ada_gagal:
        TULIS   s_fail, s_fail_len
        mov     edi, 1                  ; exit code 1
.keluar:
        mov     eax, 60                 ; sys_exit
        syscall
