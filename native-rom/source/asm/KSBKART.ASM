; Authored back-break sprite DATA. No imported executable words.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
        .def ks_bk_kano_pose0
ks_bk_kano_frame0
        .word 89,59,28,-30
        .long 006ca4378h
        .word 06000h
        .long ks_kano_primary_palette
ks_bk_kano_pose0
        .long ks_bk_kano_frame0,0
        .def ks_bk_kano_pose1
ks_bk_kano_frame1
        .word 121,59,46,-40
        .long 006cabe90h
        .word 06000h
        .long ks_kano_primary_palette
ks_bk_kano_pose1
        .long ks_bk_kano_frame1,0
        .def ks_bk_kano_pose2
ks_bk_kano_frame2
        .word 125,60,50,-64
        .long 006cb65e8h
        .word 06000h
        .long ks_kano_primary_palette
ks_bk_kano_pose2
        .long ks_bk_kano_frame2,0
        .def ks_kano_back_broke
ks_kano_back_broke
        .long ks_bk_kano_pose0,ani_adjustxy
        .word 0,10
        .long ks_bk_kano_pose0,ani_adjustxy
        .word 0,48
        .long ks_bk_kano_pose0,ks_bk_kano_pose1,ks_bk_kano_pose2,0
        .long ks_bk_kano_pose1,ks_bk_kano_pose0,0
        .def ks_bk_sonya_pose0
ks_bk_sonya_frame0
        .word 80,56,28,-30
        .long 006cc15b0h
        .word 06000h
        .long ks_sonya_primary_palette
ks_bk_sonya_pose0
        .long ks_bk_sonya_frame0,0
        .def ks_bk_sonya_pose1
ks_bk_sonya_frame1
        .word 116,50,46,-40
        .long 006cc7eb0h
        .word 06000h
        .long ks_sonya_primary_palette
ks_bk_sonya_pose1
        .long ks_bk_sonya_frame1,0
        .def ks_bk_sonya_pose2
ks_bk_sonya_frame2
        .word 123,58,50,-64
        .long 006cd06a0h
        .word 06000h
        .long ks_sonya_primary_palette
ks_bk_sonya_pose2
        .long ks_bk_sonya_frame2,0
        .def ks_sonya_back_broke
ks_sonya_back_broke
        .long ks_bk_sonya_pose0,ani_adjustxy
        .word 0,10
        .long ks_bk_sonya_pose0,ani_adjustxy
        .word 0,48
        .long ks_bk_sonya_pose0,ks_bk_sonya_pose1,ks_bk_sonya_pose2,0
        .long ks_bk_sonya_pose1,ks_bk_sonya_pose0,0
