; Authored head image DATA, no imported executable words.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
        .def ks_hd_kano_frame0
ks_hd_kano_frame0
        .word 22,27,11,13
        .long 006cdadd8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_hd_kano_frame1
ks_hd_kano_frame1
        .word 25,22,12,11
        .long 006cdbbc8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_hd_kano_frame2
ks_hd_kano_frame2
        .word 25,24,12,12
        .long 006cdc8b0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_hd_kano_frame3
ks_hd_kano_frame3
        .word 22,26,11,13
        .long 006cdd6c0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_hd_kano_frame4
ks_hd_kano_frame4
        .word 25,25,12,12
        .long 006cde428h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_hd_kano_frame5
ks_hd_kano_frame5
        .word 25,22,12,11
        .long 006cdf2d0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_hd_kano_frame6
ks_hd_kano_frame6
        .word 25,25,12,12
        .long 006cdffb8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_kano_head
ks_kano_head
        .long ks_hd_kano_frame0
        .long ks_hd_kano_frame1
        .long ks_hd_kano_frame2
        .long ks_hd_kano_frame3
        .long ks_hd_kano_frame4
        .long ks_hd_kano_frame5
        .long ks_hd_kano_frame6
        .long ani_jump,ks_kano_head
        .def ks_hd_sonya_frame0
ks_hd_sonya_frame0
        .word 26,27,13,13
        .long 006ce0e60h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_hd_sonya_frame1
ks_hd_sonya_frame1
        .word 26,25,13,12
        .long 006ce1ed8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_hd_sonya_frame2
ks_hd_sonya_frame2
        .word 28,30,14,15
        .long 006ce2e18h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_hd_sonya_frame3
ks_hd_sonya_frame3
        .word 26,27,13,13
        .long 006ce41c8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_hd_sonya_frame4
ks_hd_sonya_frame4
        .word 27,30,13,15
        .long 006ce5240h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_hd_sonya_frame5
ks_hd_sonya_frame5
        .word 25,23,12,11
        .long 006ce6540h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_hd_sonya_frame6
ks_hd_sonya_frame6
        .word 26,31,13,15
        .long 006ce72c0h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_sonya_head
ks_sonya_head
        .long ks_hd_sonya_frame0
        .long ks_hd_sonya_frame1
        .long ks_hd_sonya_frame2
        .long ks_hd_sonya_frame3
        .long ks_hd_sonya_frame4
        .long ks_hd_sonya_frame5
        .long ks_hd_sonya_frame6
        .long ani_jump,ks_sonya_head
