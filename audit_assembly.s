	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 15, 0	sdk_version 15, 5
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #144
	stp	x28, x27, [sp, #48]             ; 16-byte Folded Spill
	stp	x26, x25, [sp, #64]             ; 16-byte Folded Spill
	stp	x24, x23, [sp, #80]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #96]             ; 16-byte Folded Spill
	stp	x20, x19, [sp, #112]            ; 16-byte Folded Spill
	stp	x29, x30, [sp, #128]            ; 16-byte Folded Spill
	add	x29, sp, #128
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	.cfi_offset w27, -88
	.cfi_offset w28, -96
Lloh0:
	adrp	x0, l_str.33@PAGE
Lloh1:
	add	x0, x0, l_str.33@PAGEOFF
	bl	_puts
Lloh2:
	adrp	x0, l_str.28@PAGE
Lloh3:
	add	x0, x0, l_str.28@PAGEOFF
	bl	_puts
Lloh4:
	adrp	x0, l_str.29@PAGE
Lloh5:
	add	x0, x0, l_str.29@PAGEOFF
	bl	_puts
	mov	w8, #255                        ; =0xff
	; InlineAsm Start
	mov	w0, w8
	tst	w0, #0x1
	cset	w23, ne
	tst	w0, #0x2
	cset	w22, ne
	tst	w0, #0x4
	cset	w28, ne
	tst	w0, #0x8
	cset	w27, ne
	tst	w0, #0x10
	cset	w26, ne
	tst	w0, #0x20
	cset	w25, ne
	tst	w0, #0x40
	cset	w11, ne
	tst	w0, #0x80
	cset	w10, ne
	cmp	w0, #255
	cset	w9, eq

	; InlineAsm End
	stp	w11, w10, [sp, #32]             ; 8-byte Folded Spill
	str	x9, [sp, #40]                   ; 8-byte Folded Spill
	str	x8, [sp]
Lloh6:
	adrp	x0, l_.str.3@PAGE
Lloh7:
	add	x0, x0, l_.str.3@PAGEOFF
	bl	_printf
	mov	w24, #1                         ; =0x1
	str	x24, [sp]
Lloh8:
	adrp	x20, l_.str.4@PAGE
Lloh9:
	add	x20, x20, l_.str.4@PAGEOFF
	mov	x0, x20
	bl	_printf
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
	mov	w0, #32                         ; =0x20
	bl	_putchar
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
	str	x24, [sp]
	mov	x0, x20
	bl	_printf
Lloh10:
	adrp	x0, l_str.30@PAGE
Lloh11:
	add	x0, x0, l_str.30@PAGEOFF
	bl	_puts
Lloh12:
	adrp	x8, l_.str.10@PAGE
Lloh13:
	add	x8, x8, l_.str.10@PAGEOFF
Lloh14:
	adrp	x9, l_.str.9@PAGE
Lloh15:
	add	x9, x9, l_.str.9@PAGEOFF
Lloh16:
	adrp	x10, l_.str.8@PAGE
Lloh17:
	add	x10, x10, l_.str.8@PAGEOFF
	stp	x9, x8, [sp, #8]
	str	x10, [sp]
Lloh18:
	adrp	x0, l_.str.7@PAGE
Lloh19:
	add	x0, x0, l_.str.7@PAGEOFF
	bl	_printf
Lloh20:
	adrp	x0, l_str.32@PAGE
Lloh21:
	add	x0, x0, l_str.32@PAGEOFF
	bl	_puts
Lloh22:
	adrp	x19, l_.str.13@PAGE
Lloh23:
	add	x19, x19, l_.str.13@PAGEOFF
Lloh24:
	adrp	x20, l_.str.14@PAGE
Lloh25:
	add	x20, x20, l_.str.14@PAGEOFF
	cmp	w23, #0
	csel	x8, x20, x19, eq
Lloh26:
	adrp	x9, l_.str.20@PAGE
Lloh27:
	add	x9, x9, l_.str.20@PAGEOFF
	stp	xzr, x8, [sp, #8]
	str	x9, [sp]
Lloh28:
	adrp	x21, l_.str.12@PAGE
Lloh29:
	add	x21, x21, l_.str.12@PAGEOFF
	mov	x0, x21
	bl	_printf
	add	w23, w22, w23
	cmp	w22, #0
	csel	x8, x20, x19, eq
	stp	x24, x8, [sp, #8]
Lloh30:
	adrp	x8, l_.str.21@PAGE
Lloh31:
	add	x8, x8, l_.str.21@PAGEOFF
	str	x8, [sp]
	mov	x0, x21
	bl	_printf
	cmp	w28, #0
	csel	x10, x20, x19, eq
	mov	w8, #2                          ; =0x2
Lloh32:
	adrp	x9, l_.str.22@PAGE
Lloh33:
	add	x9, x9, l_.str.22@PAGEOFF
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
	mov	x0, x21
	bl	_printf
	add	w8, w27, w28
	add	w22, w8, w23
	cmp	w27, #0
	csel	x10, x20, x19, eq
	mov	w8, #3                          ; =0x3
Lloh34:
	adrp	x9, l_.str.23@PAGE
Lloh35:
	add	x9, x9, l_.str.23@PAGEOFF
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
	mov	x0, x21
	bl	_printf
	cmp	w26, #0
	csel	x10, x20, x19, eq
	mov	w8, #4                          ; =0x4
Lloh36:
	adrp	x9, l_.str.24@PAGE
Lloh37:
	add	x9, x9, l_.str.24@PAGEOFF
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
	mov	x0, x21
	bl	_printf
	add	w23, w25, w26
	cmp	w25, #0
	csel	x10, x20, x19, eq
	mov	w8, #5                          ; =0x5
Lloh38:
	adrp	x9, l_.str.25@PAGE
Lloh39:
	add	x9, x9, l_.str.25@PAGEOFF
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
	mov	x0, x21
	bl	_printf
	ldr	w9, [sp, #32]                   ; 4-byte Folded Reload
	add	w8, w9, w23
	add	w22, w8, w22
	cmp	w9, #0
	csel	x10, x20, x19, eq
	mov	w8, #6                          ; =0x6
Lloh40:
	adrp	x9, l_.str.26@PAGE
Lloh41:
	add	x9, x9, l_.str.26@PAGEOFF
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
	mov	x0, x21
	bl	_printf
	ldr	w8, [sp, #36]                   ; 4-byte Folded Reload
	add	w22, w8, w22
	cmp	w8, #0
	csel	x10, x20, x19, eq
	mov	w8, #7                          ; =0x7
Lloh42:
	adrp	x9, l_.str.27@PAGE
Lloh43:
	add	x9, x9, l_.str.27@PAGEOFF
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
	mov	x0, x21
	bl	_printf
Lloh44:
	adrp	x0, l_str.32@PAGE
Lloh45:
	add	x0, x0, l_str.32@PAGEOFF
	bl	_puts
	ldr	x19, [sp, #40]                  ; 8-byte Folded Reload
	str	x19, [sp]
Lloh46:
	adrp	x0, l_.str.15@PAGE
Lloh47:
	add	x0, x0, l_.str.15@PAGEOFF
	bl	_printf
	str	x22, [sp]
Lloh48:
	adrp	x0, l_.str.16@PAGE
Lloh49:
	add	x0, x0, l_.str.16@PAGEOFF
	bl	_printf
	cmp	w19, #0
	cset	w20, eq
Lloh50:
	adrp	x8, l_.str.18@PAGE
Lloh51:
	add	x8, x8, l_.str.18@PAGEOFF
Lloh52:
	adrp	x9, l_.str.19@PAGE
Lloh53:
	add	x9, x9, l_.str.19@PAGEOFF
	csel	x8, x9, x8, eq
	str	x8, [sp]
Lloh54:
	adrp	x0, l_.str.17@PAGE
Lloh55:
	add	x0, x0, l_.str.17@PAGEOFF
	bl	_printf
Lloh56:
	adrp	x0, l_str.33@PAGE
Lloh57:
	add	x0, x0, l_str.33@PAGEOFF
	bl	_puts
	mov	x0, x20
	ldp	x29, x30, [sp, #128]            ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #112]            ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #96]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #80]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #64]             ; 16-byte Folded Reload
	ldp	x28, x27, [sp, #48]             ; 16-byte Folded Reload
	add	sp, sp, #144
	ret
	.loh AdrpAdd	Lloh56, Lloh57
	.loh AdrpAdd	Lloh54, Lloh55
	.loh AdrpAdd	Lloh52, Lloh53
	.loh AdrpAdd	Lloh50, Lloh51
	.loh AdrpAdd	Lloh48, Lloh49
	.loh AdrpAdd	Lloh46, Lloh47
	.loh AdrpAdd	Lloh44, Lloh45
	.loh AdrpAdd	Lloh42, Lloh43
	.loh AdrpAdd	Lloh40, Lloh41
	.loh AdrpAdd	Lloh38, Lloh39
	.loh AdrpAdd	Lloh36, Lloh37
	.loh AdrpAdd	Lloh34, Lloh35
	.loh AdrpAdd	Lloh32, Lloh33
	.loh AdrpAdd	Lloh30, Lloh31
	.loh AdrpAdd	Lloh28, Lloh29
	.loh AdrpAdd	Lloh26, Lloh27
	.loh AdrpAdd	Lloh24, Lloh25
	.loh AdrpAdd	Lloh22, Lloh23
	.loh AdrpAdd	Lloh20, Lloh21
	.loh AdrpAdd	Lloh18, Lloh19
	.loh AdrpAdd	Lloh16, Lloh17
	.loh AdrpAdd	Lloh14, Lloh15
	.loh AdrpAdd	Lloh12, Lloh13
	.loh AdrpAdd	Lloh10, Lloh11
	.loh AdrpAdd	Lloh8, Lloh9
	.loh AdrpAdd	Lloh6, Lloh7
	.loh AdrpAdd	Lloh4, Lloh5
	.loh AdrpAdd	Lloh2, Lloh3
	.loh AdrpAdd	Lloh0, Lloh1
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str.3:                               ; @.str.3
	.asciz	"ARM64 Register w0 Value : 0x%02X (Biner: "

l_.str.4:                               ; @.str.4
	.asciz	"%d"

l_.str.7:                               ; @.str.7
	.asciz	"%-58s | %-12s | %s\n"

l_.str.8:                               ; @.str.8
	.asciz	"Indikator Kriteria Jurnal Q1"

l_.str.9:                               ; @.str.9
	.asciz	"ASM Instruksi"

l_.str.10:                              ; @.str.10
	.asciz	"Status Bit"

l_.str.12:                              ; @.str.12
	.asciz	"%-58s | TST w0, #(1<<%d) | %s\n"

l_.str.13:                              ; @.str.13
	.asciz	"\342\234\205 Bit 1 (PASS)"

l_.str.14:                              ; @.str.14
	.asciz	"\342\235\214 Bit 0 (FAIL)"

l_.str.15:                              ; @.str.15
	.asciz	"Hasil Hardware Flags       : CMP w0, #0xFF -> Zero Flag Z = %d (EQ)\n"

l_.str.16:                              ; @.str.16
	.asciz	"Akumulasi Bit Aktif        : %u / 8 Bit (100.0%%)\n"

l_.str.17:                              ; @.str.17
	.asciz	"Status Kesiapan Q1         : %s\n"

l_.str.18:                              ; @.str.18
	.asciz	"ALL CLEAR (0xFF READY)"

l_.str.19:                              ; @.str.19
	.asciz	"DEFECTIVE BIT DETECTED"

l_.str.20:                              ; @.str.20
	.asciz	"Bit 0: Large Golden Dataset (N >= 100)"

l_.str.21:                              ; @.str.21
	.asciz	"Bit 1: Inter-Rater Reliability (Cohen's Kappa >= 0.80)"

l_.str.22:                              ; @.str.22
	.asciz	"Bit 2: Ablation Study Matrix (Multi-Agent > Baseline)"

l_.str.23:                              ; @.str.23
	.asciz	"Bit 3: RAGAS Benchmark (Faithfulness >= 0.85)"

l_.str.24:                              ; @.str.24
	.asciz	"Bit 4: Privacy & PII Guardrail (Zero Leak)"

l_.str.25:                              ; @.str.25
	.asciz	"Bit 5: Statistical Rigor (Paired t-test p < 0.05)"

l_.str.26:                              ; @.str.26
	.asciz	"Bit 6: Human User Study (SUS Score >= 75.0)"

l_.str.27:                              ; @.str.27
	.asciz	"Bit 7: Environment Reproducibility (Dockerfile & Seeds)"

l_str.28:                               ; @str.28
	.asciz	"\342\232\231\357\270\217  AUDIT HARDWARE REGISTER (ARM64 ASSEMBLY EXECUTION)"

l_str.29:                               ; @str.29
	.asciz	"======================================================================\n"

l_str.30:                               ; @str.30
	.asciz	"b)\n"

l_str.32:                               ; @str.32
	.asciz	"--------------------------------------------------------------------------------------"

l_str.33:                               ; @str.33
	.asciz	"======================================================================"

.subsections_via_symbols
