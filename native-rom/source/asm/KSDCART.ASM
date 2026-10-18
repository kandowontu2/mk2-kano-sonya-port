; Authored head image DATA, no imported executable words.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
        .def ks_dc_kano_frame0
ks_dc_kano_frame0
        .word 47,110,14,-21
        .long 006ce85a8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose0
ks_dc_kano_pose0
        .long ks_dc_kano_frame0,0
        .def ks_dc_kano_frame1
ks_dc_kano_frame1
        .word 46,103,20,-28
        .long 006cefed8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose1
ks_dc_kano_pose1
        .long ks_dc_kano_frame1,0
        .def ks_dc_kano_frame2
ks_dc_kano_frame2
        .word 49,84,14,-47
        .long 006cf6de8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose2
ks_dc_kano_pose2
        .long ks_dc_kano_frame2,0
        .def ks_dc_kano_frame3
ks_dc_kano_frame3
        .word 53,73,13,-58
        .long 006cfce60h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose3
ks_dc_kano_pose3
        .long ks_dc_kano_frame3,0
        .def ks_dc_kano_frame4
ks_dc_kano_frame4
        .word 76,54,15,-77
        .long 006d02910h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose4
ks_dc_kano_pose4
        .long ks_dc_kano_frame4,0
        .def ks_dc_kano_frame5
ks_dc_kano_frame5
        .word 103,45,10,-86
        .long 006d08940h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose5
ks_dc_kano_pose5
        .long ks_dc_kano_frame5,0
        .def ks_dc_kano_frame6
ks_dc_kano_frame6
        .word 130,21,15,-110
        .long 006d0f5e8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_dc_kano_pose6
ks_dc_kano_pose6
        .long ks_dc_kano_frame6,0
        .def ks_kano_decapfall
ks_kano_decapfall
        .long ks_dc_kano_pose0
        .long ks_dc_kano_pose1
        .long ks_dc_kano_pose2
        .long 0
        .long ks_dc_kano_pose3
        .long ks_dc_kano_pose2
        .long ks_dc_kano_pose3
        .long ks_dc_kano_pose2
        .long ks_dc_kano_pose3
        .long ks_dc_kano_pose2
        .long 0
        .long ks_dc_kano_pose3
        .long ks_dc_kano_pose4
        .long ks_dc_kano_pose5
        .long ks_dc_kano_pose6
        .long 0
        .def ks_dc_sonya_frame0
ks_dc_sonya_frame0
        .word 48,105,14,-27
        .long 006d135e8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose0
ks_dc_sonya_pose0
        .long ks_dc_sonya_frame0,0
        .def ks_dc_sonya_frame1
ks_dc_sonya_frame1
        .word 45,104,20,-28
        .long 006d1ac08h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose1
ks_dc_sonya_pose1
        .long ks_dc_sonya_frame1,0
        .def ks_dc_sonya_frame2
ks_dc_sonya_frame2
        .word 38,83,14,-49
        .long 006d219b8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose2
ks_dc_sonya_pose2
        .long ks_dc_sonya_frame2,0
        .def ks_dc_sonya_frame3
ks_dc_sonya_frame3
        .word 42,64,13,-68
        .long 006d263a8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose3
ks_dc_sonya_pose3
        .long ks_dc_sonya_frame3,0
        .def ks_dc_sonya_frame4
ks_dc_sonya_frame4
        .word 65,49,15,-83
        .long 006d2a2a8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose4
ks_dc_sonya_pose4
        .long ks_dc_sonya_frame4,0
        .def ks_dc_sonya_frame5
ks_dc_sonya_frame5
        .word 115,48,10,-84
        .long 006d2ed50h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose5
ks_dc_sonya_pose5
        .long ks_dc_sonya_frame5,0
        .def ks_dc_sonya_frame6
ks_dc_sonya_frame6
        .word 125,25,15,-107
        .long 006d36eb0h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_dc_sonya_pose6
ks_dc_sonya_pose6
        .long ks_dc_sonya_frame6,0
        .def ks_sonya_decapfall
ks_sonya_decapfall
        .long ks_dc_sonya_pose0
        .long ks_dc_sonya_pose1
        .long ks_dc_sonya_pose2
        .long 0
        .long ks_dc_sonya_pose3
        .long ks_dc_sonya_pose2
        .long ks_dc_sonya_pose3
        .long ks_dc_sonya_pose2
        .long ks_dc_sonya_pose3
        .long ks_dc_sonya_pose2
        .long 0
        .long ks_dc_sonya_pose3
        .long ks_dc_sonya_pose4
        .long ks_dc_sonya_pose5
        .long ks_dc_sonya_pose6
        .long 0
