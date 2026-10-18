; Authored head image DATA, no imported executable words.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
        .def ks_dr_kano_frame0
ks_dr_kano_frame0
        .word 45,125,-2,5
        .long 006d3b7f0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dr_kano_pose0
ks_dr_kano_pose0
        .long ks_dr_kano_frame0,0
        .def ks_dr_kano_frame1
ks_dr_kano_frame1
        .word 47,119,-2,3
        .long 006d43bc8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dr_kano_pose1
ks_dr_kano_pose1
        .long ks_dr_kano_frame1,0
        .def ks_dr_kano_frame2
ks_dr_kano_frame2
        .word 49,113,-3,1
        .long 006d4bee0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dr_kano_pose2
ks_dr_kano_pose2
        .long ks_dr_kano_frame2,0
        .def ks_kano_drain_shrink
ks_kano_drain_shrink
        .long ks_dr_kano_pose0
        .long ks_dr_kano_pose1
        .long ks_dr_kano_pose2
        .long 0
        .long ks_dr_kano_pose1
        .long ks_dr_kano_pose0
        .long ks_dr_kano_pose1
        .long ks_dr_kano_pose2
        .long 0
        .def ks_dr_sonya_frame0
ks_dr_sonya_frame0
        .word 51,125,-2,5
        .long 006d540a8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dr_sonya_pose0
ks_dr_sonya_pose0
        .long ks_dr_sonya_frame0,0
        .def ks_dr_sonya_frame1
ks_dr_sonya_frame1
        .word 49,119,-2,3
        .long 006d5d618h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dr_sonya_pose1
ks_dr_sonya_pose1
        .long ks_dr_sonya_frame1,0
        .def ks_dr_sonya_frame2
ks_dr_sonya_frame2
        .word 46,113,-3,1
        .long 006d65ec8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dr_sonya_pose2
ks_dr_sonya_pose2
        .long ks_dr_sonya_frame2,0
        .def ks_sonya_drain_shrink
ks_sonya_drain_shrink
        .long ks_dr_sonya_pose0
        .long ks_dr_sonya_pose1
        .long ks_dr_sonya_pose2
        .long 0
        .long ks_dr_sonya_pose1
        .long ks_dr_sonya_pose0
        .long ks_dr_sonya_pose1
        .long ks_dr_sonya_pose2
        .long 0
