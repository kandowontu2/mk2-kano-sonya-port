; Authored impalement victim artwork and native two-part animation DATA.
        .include mainequ.asm
        .ref ks_kano_primary_palette
        .ref ks_sonya_primary_palette
        .data
        .def ks_im_kano_frame0,ks_im_kano_pose0
ks_im_kano_frame0
        .word 65,143,26,1
        .long 006ddd998h
        .word 06000h
        .long ks_kano_primary_palette
ks_im_kano_pose0
        .long ks_im_kano_frame0,0
        .def ks_im_kano_frame1,ks_im_kano_pose1
ks_im_kano_frame1
        .word 66,142,23,6
        .long 006deb378h
        .word 06000h
        .long ks_kano_primary_palette
ks_im_kano_pose1
        .long ks_im_kano_frame1,0
        .def ks_im_kano_frame2,ks_im_kano_pose2
ks_im_kano_frame2
        .word 60,128,21,-12
        .long 006df8f20h
        .word 06000h
        .long ks_kano_primary_palette
ks_im_kano_pose2
        .long ks_im_kano_frame2,0
        .def ks_kano_impaled
ks_kano_impaled
        .long ani_adjustxy,0010ffa0h,ks_im_kano_pose0
        .long ani_adjustxy,0ffe80000h,ks_im_kano_pose0
        .long ani_adjustxy,0ffe80000h,ks_im_kano_pose0
        .long ani_adjustxy,0ffe80010h,ks_im_kano_pose0,0
        .long ks_im_kano_pose0,ks_im_kano_pose1,ks_im_kano_pose2,ks_im_kano_pose1,ks_im_kano_pose0,ks_im_kano_pose1,ks_im_kano_pose2,0
        .def ks_im_sonya_frame0,ks_im_sonya_pose0
ks_im_sonya_frame0
        .word 74,143,31,1
        .long 006e04320h
        .word 06000h
        .long ks_sonya_primary_palette
ks_im_sonya_pose0
        .long ks_im_sonya_frame0,0
        .def ks_im_sonya_frame1,ks_im_sonya_pose1
ks_im_sonya_frame1
        .word 56,145,18,9
        .long 006e13b28h
        .word 06000h
        .long ks_sonya_primary_palette
ks_im_sonya_pose1
        .long ks_im_sonya_frame1,0
        .def ks_im_sonya_frame2,ks_im_sonya_pose2
ks_im_sonya_frame2
        .word 51,134,17,-6
        .long 006e1f978h
        .word 06000h
        .long ks_sonya_primary_palette
ks_im_sonya_pose2
        .long ks_im_sonya_frame2,0
        .def ks_sonya_impaled
ks_sonya_impaled
        .long ani_adjustxy,0010ffa0h,ks_im_sonya_pose0
        .long ani_adjustxy,0ffe80000h,ks_im_sonya_pose0
        .long ani_adjustxy,0ffe80000h,ks_im_sonya_pose0
        .long ani_adjustxy,0ffe80010h,ks_im_sonya_pose0,0
        .long ks_im_sonya_pose0,ks_im_sonya_pose1,ks_im_sonya_pose2,ks_im_sonya_pose1,ks_im_sonya_pose0,ks_im_sonya_pose1,ks_im_sonya_pose2,0
