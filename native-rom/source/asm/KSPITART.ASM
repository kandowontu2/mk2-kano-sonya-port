; Recovered authored dedicated Pit sprite DATA only, no old executable payload.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
ks_pit_kano_frame0
        .word 122,132,60,-1
        .long 006ba98d8h
        .word 06000h
        .long ks_kano_primary_palette
ks_pit_kano_pose0
        .long ks_pit_kano_frame0,0
ks_pit_kano_frame1
        .word 116,128,60,-3
        .long 006bc1248h
        .word 06000h
        .long ks_kano_primary_palette
ks_pit_kano_pose1
        .long ks_pit_kano_frame1,0
ks_pit_kano_frame2
        .word 112,136,51,7
        .long 006bd6e48h
        .word 06000h
        .long ks_kano_primary_palette
ks_pit_kano_pose2
        .long ks_pit_kano_frame2,0
ks_pit_kano_frame3
        .word 120,134,46,5
        .long 006bed348h
        .word 06000h
        .long ks_kano_primary_palette
ks_pit_kano_pose3
        .long ks_pit_kano_frame3,0
ks_pit_kano_frame4
        .word 110,125,41,-2
        .long 006c04c28h
        .word 06000h
        .long ks_kano_primary_palette
ks_pit_kano_pose4
        .long ks_pit_kano_frame4,0
ks_pit_kano_frame5
        .word 139,131,65,0
        .long 006c18e70h
        .word 06000h
        .long ks_kano_primary_palette
ks_pit_kano_pose5
        .long ks_pit_kano_frame5,0
        .def ks_pit_kano_sequence
ks_pit_kano_sequence
        .long ks_pit_kano_pose0
        .long ks_pit_kano_pose1
        .long ks_pit_kano_pose2
        .long ks_pit_kano_pose3
        .long ks_pit_kano_pose4
        .long ani_jump,ks_pit_kano_sequence,0
        .long ks_pit_kano_pose5,0
ks_pit_sonya_frame0
        .word 112,130,55,-1
        .long 006c33938h
        .word 06000h
        .long ks_sonya_primary_palette
ks_pit_sonya_pose0
        .long ks_pit_sonya_frame0,0
ks_pit_sonya_frame1
        .word 97,118,50,-3
        .long 006c48e78h
        .word 06000h
        .long ks_sonya_primary_palette
ks_pit_sonya_pose1
        .long ks_pit_sonya_frame1,0
ks_pit_sonya_frame2
        .word 100,130,45,7
        .long 006c59ac0h
        .word 06000h
        .long ks_sonya_primary_palette
ks_pit_sonya_pose2
        .long ks_pit_sonya_frame2,0
ks_pit_sonya_frame3
        .word 95,123,33,5
        .long 006c6cb70h
        .word 06000h
        .long ks_sonya_primary_palette
ks_pit_sonya_pose3
        .long ks_pit_sonya_frame3,0
ks_pit_sonya_frame4
        .word 93,124,32,-2
        .long 006c7dd50h
        .word 06000h
        .long ks_sonya_primary_palette
ks_pit_sonya_pose4
        .long ks_pit_sonya_frame4,0
ks_pit_sonya_frame5
        .word 112,131,52,0
        .long 006c8eb98h
        .word 06000h
        .long ks_sonya_primary_palette
ks_pit_sonya_pose5
        .long ks_pit_sonya_frame5,0
        .def ks_pit_sonya_sequence
ks_pit_sonya_sequence
        .long ks_pit_sonya_pose0
        .long ks_pit_sonya_pose1
        .long ks_pit_sonya_pose2
        .long ks_pit_sonya_pose3
        .long ks_pit_sonya_pose4
        .long ani_jump,ks_pit_sonya_sequence,0
        .long ks_pit_sonya_pose5,0
