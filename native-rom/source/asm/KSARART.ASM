; Own arm-rip victim and detached-arm DATA. Staged, not active gameplay.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
        .def ks_ar_kano_body_frame0
ks_ar_kano_body_frame0
        .word 97,131,34,0
        .long 006e299a8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_body_pose0
ks_ar_kano_body_pose0
        .long ks_ar_kano_body_frame0,0
        .def ks_ar_kano_body_frame1
ks_ar_kano_body_frame1
        .word 70,131,34,0
        .long 006e3c380h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_body_pose1
ks_ar_kano_body_pose1
        .long ks_ar_kano_body_frame1,0
        .def ks_ar_kano_body_frame2
ks_ar_kano_body_frame2
        .word 66,123,33,-8
        .long 006e49a70h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_body_pose2
ks_ar_kano_body_pose2
        .long ks_ar_kano_body_frame2,0
        .def ks_ar_kano_body_frame3
ks_ar_kano_body_frame3
        .word 71,111,37,-20
        .long 006e558b8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_body_pose3
ks_ar_kano_body_pose3
        .long ks_ar_kano_body_frame3,0
        .def ks_ar_kano_body_frame4
ks_ar_kano_body_frame4
        .word 65,60,36,-71
        .long 006e61170h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_body_pose4
ks_ar_kano_body_pose4
        .long ks_ar_kano_body_frame4,0
        .def ks_ar_sonya_body_frame0
ks_ar_sonya_body_frame0
        .word 96,132,35,0
        .long 006e66cd8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_body_pose0
ks_ar_sonya_body_pose0
        .long ks_ar_sonya_body_frame0,0
        .def ks_ar_sonya_body_frame1
ks_ar_sonya_body_frame1
        .word 71,132,35,0
        .long 006e795d8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_body_pose1
ks_ar_sonya_body_pose1
        .long ks_ar_sonya_body_frame1,0
        .def ks_ar_sonya_body_frame2
ks_ar_sonya_body_frame2
        .word 71,125,60,-7
        .long 006e87180h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_body_pose2
ks_ar_sonya_body_pose2
        .long ks_ar_sonya_body_frame2,0
        .def ks_ar_sonya_body_frame3
ks_ar_sonya_body_frame3
        .word 76,114,35,-18
        .long 006e94188h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_body_pose3
ks_ar_sonya_body_pose3
        .long ks_ar_sonya_body_frame3,0
        .def ks_ar_sonya_body_frame4
ks_ar_sonya_body_frame4
        .word 71,70,40,-62
        .long 006ea0c98h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_body_pose4
ks_ar_sonya_body_pose4
        .long ks_ar_sonya_body_frame4,0
        .def ks_ar_kano_arm_frame0
ks_ar_kano_arm_frame0
        .word 57,15,-31,-101
        .long 006ea8118h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_arm_frame1
ks_ar_kano_arm_frame1
        .word 56,22,2,-106
        .long 006ea9528h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_arm_frame2
ks_ar_kano_arm_frame2
        .word 57,33,50,-72
        .long 006eab208h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_arm_frame3
ks_ar_kano_arm_frame3
        .word 52,35,79,-79
        .long 006eade20h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_kano_arm_frame4
ks_ar_kano_arm_frame4
        .word 40,32,89,-113
        .long 006eb08c8h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_ar_sonya_arm_frame0
ks_ar_sonya_arm_frame0
        .word 53,12,-31,-101
        .long 006eb26c8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_arm_frame1
ks_ar_sonya_arm_frame1
        .word 55,20,3,-108
        .long 006eb35b0h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_arm_frame2
ks_ar_sonya_arm_frame2
        .word 54,27,52,-66
        .long 006eb4f78h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_arm_frame3
ks_ar_sonya_arm_frame3
        .word 49,30,81,-84
        .long 006eb71a8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_ar_sonya_arm_frame4
ks_ar_sonya_arm_frame4
        .word 39,30,92,-115
        .long 006eb9420h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_kano_arms_ripped
ks_kano_arms_ripped
        .long ks_ar_kano_body_pose0
        .long ks_ar_kano_body_pose1
        .long ks_ar_kano_body_pose2
        .long ks_ar_kano_body_pose3
        .long ks_ar_kano_body_pose4
        .long 0
        .def ks_kano_arm_fly
ks_kano_arm_fly
        .long ks_ar_kano_arm_frame0
        .long ks_ar_kano_arm_frame1
        .long ks_ar_kano_arm_frame2
        .long ks_ar_kano_arm_frame3
        .long ks_ar_kano_arm_frame4
        .long 0
        .def ks_sonya_arms_ripped
ks_sonya_arms_ripped
        .long ks_ar_sonya_body_pose0
        .long ks_ar_sonya_body_pose1
        .long ks_ar_sonya_body_pose2
        .long ks_ar_sonya_body_pose3
        .long ks_ar_sonya_body_pose4
        .long 0
        .def ks_sonya_arm_fly
ks_sonya_arm_fly
        .long ks_ar_sonya_arm_frame0
        .long ks_ar_sonya_arm_frame1
        .long ks_ar_sonya_arm_frame2
        .long ks_ar_sonya_arm_frame3
        .long ks_ar_sonya_arm_frame4
        .long 0
