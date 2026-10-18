; Authored own Kano nut-punch sprite DATA.
        .include mainequ.asm
        .ref ks_kano_primary_palette
        .data
        .def ks_nut_kano_frame0,ks_nut_kano_pose0
ks_nut_kano_frame0
        .word 85,125,41,-6
        .long 006dc1c88h
        .word 06000h
        .long ks_kano_primary_palette
ks_nut_kano_pose0
        .long ks_nut_kano_frame0,0
        .def ks_nut_kano_frame1,ks_nut_kano_pose1
ks_nut_kano_frame1
        .word 82,102,40,-29
        .long 006dd1590h
        .word 06000h
        .long ks_kano_primary_palette
ks_nut_kano_pose1
        .long ks_nut_kano_frame1,0
        .def ks_kano_nutcrunched
ks_kano_nutcrunched
        .long ks_nut_kano_pose0,ks_nut_kano_pose1,0
        .long ks_nut_kano_pose0,0
