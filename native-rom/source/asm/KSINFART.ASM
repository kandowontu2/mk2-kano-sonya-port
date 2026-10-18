; Own inflation DATA: staged only, NOT runtime qualified.
        .include mainequ.asm
        .ref ks_kano_primary_palette,ks_sonya_primary_palette
        .data
        .def ks_inf_kano_img0,ks_inf_kano_pose0
ks_inf_kano_img0
        .word 86,131,43,0
        .long 006ebaf90h
        .word 06000h
        .long ks_kano_primary_palette
ks_inf_kano_pose0
        .long ks_inf_kano_img0,0
        .def ks_inf_kano_img1,ks_inf_kano_pose1
ks_inf_kano_img1
        .word 84,131,39,0
        .long 006ecb7a0h
        .word 06000h
        .long ks_kano_primary_palette
ks_inf_kano_pose1
        .long ks_inf_kano_img1,0
        .def ks_inf_kano_img2,ks_inf_kano_pose2
ks_inf_kano_img2
        .word 91,131,46,0
        .long 006edb988h
        .word 06000h
        .long ks_kano_primary_palette
ks_inf_kano_pose2
        .long ks_inf_kano_img2,0
        .def ks_inf_kano_img3,ks_inf_kano_pose3
ks_inf_kano_img3
        .word 97,131,50,0
        .long 006eed0f0h
        .word 06000h
        .long ks_kano_primary_palette
ks_inf_kano_pose3
        .long ks_inf_kano_img3,0
        .def ks_inf_kano_img4,ks_inf_kano_pose4
ks_inf_kano_img4
        .word 100,131,52,0
        .long 006effac8h
        .word 06000h
        .long ks_kano_primary_palette
ks_inf_kano_pose4
        .long ks_inf_kano_img4,0
        .def ks_inf_kano_img5,ks_inf_kano_pose5
ks_inf_kano_img5
        .word 100,131,52,0
        .long 006f12dd0h
        .word 06000h
        .long ks_kano_primary_palette
ks_inf_kano_pose5
        .long ks_inf_kano_img5,0
        .def ks_kano_inflated
ks_kano_inflated
        .long ks_inf_kano_pose0
        .long ks_inf_kano_pose1
        .long ks_inf_kano_pose2
        .long ks_inf_kano_pose3
        .long ks_inf_kano_pose4
        .long 0
        .long ks_inf_kano_pose5
        .long 0
        .def ks_inf_sonya_img0,ks_inf_sonya_pose0
ks_inf_sonya_img0
        .word 78,132,37,0
        .long 006f260d8h
        .word 06000h
        .long ks_sonya_primary_palette
ks_inf_sonya_pose0
        .long ks_inf_sonya_img0,0
        .def ks_inf_sonya_img1,ks_inf_sonya_pose1
ks_inf_sonya_img1
        .word 81,132,39,0
        .long 006f35228h
        .word 06000h
        .long ks_sonya_primary_palette
ks_inf_sonya_pose1
        .long ks_inf_sonya_img1,0
        .def ks_inf_sonya_img2,ks_inf_sonya_pose2
ks_inf_sonya_img2
        .word 90,132,45,0
        .long 006f44cc0h
        .word 06000h
        .long ks_sonya_primary_palette
ks_inf_sonya_pose2
        .long ks_inf_sonya_img2,0
        .def ks_inf_sonya_img3,ks_inf_sonya_pose3
ks_inf_sonya_img3
        .word 92,132,47,0
        .long 006f56330h
        .word 06000h
        .long ks_sonya_primary_palette
ks_inf_sonya_pose3
        .long ks_inf_sonya_img3,0
        .def ks_inf_sonya_img4,ks_inf_sonya_pose4
ks_inf_sonya_img4
        .word 90,132,46,0
        .long 006f67fd0h
        .word 06000h
        .long ks_sonya_primary_palette
ks_inf_sonya_pose4
        .long ks_inf_sonya_img4,0
        .def ks_inf_sonya_img5,ks_inf_sonya_pose5
ks_inf_sonya_img5
        .word 90,132,45,0
        .long 006f79640h
        .word 06000h
        .long ks_sonya_primary_palette
ks_inf_sonya_pose5
        .long ks_inf_sonya_img5,0
        .def ks_sonya_inflated
ks_sonya_inflated
        .long ks_inf_sonya_pose0
        .long ks_inf_sonya_pose1
        .long ks_inf_sonya_pose2
        .long ks_inf_sonya_pose3
        .long ks_inf_sonya_pose4
        .long 0
        .long ks_inf_sonya_pose5
        .long 0
