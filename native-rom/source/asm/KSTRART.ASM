; Authored native multipart torso DATA, no executable words.
        .include mainequ.asm
        .data
        .ref ks_kano_primary_palette
        .ref ks_kano_pose_ff829040
        .def ks_tr_kano_frame0_0
ks_tr_kano_frame0_0
        .word 33,76,13,10
        .long 006d6d8a0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame0_1
ks_tr_kano_frame0_1
        .word 33,76,-20,10
        .long 006d71368h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose0
ks_tr_kano_pose0
        .long ks_tr_kano_frame0_0,ks_tr_kano_frame0_1,0
        .def ks_tr_kano_frame1_0
ks_tr_kano_frame1_0
        .word 25,69,20,3
        .long 006d74e30h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame1_1
ks_tr_kano_frame1_1
        .word 26,69,-5,3
        .long 006d776a0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame1_2
ks_tr_kano_frame1_2
        .word 26,69,-31,3
        .long 006d7a0b0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose1
ks_tr_kano_pose1
        .long ks_tr_kano_frame1_0,ks_tr_kano_frame1_1,ks_tr_kano_frame1_2,0
        .def ks_tr_kano_frame2_0
ks_tr_kano_frame2_0
        .word 44,86,15,14
        .long 006d7cac0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose2
ks_tr_kano_pose2
        .long ks_tr_kano_frame2_0,0
        .def ks_tr_kano_frame3_0
ks_tr_kano_frame3_0
        .word 42,65,28,-2
        .long 006d82370h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame3_1
ks_tr_kano_frame3_1
        .word 42,65,-14,-2
        .long 006d86370h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose3
ks_tr_kano_pose3
        .long ks_tr_kano_frame3_0,ks_tr_kano_frame3_1,0
        .def ks_tr_kano_frame4_0
ks_tr_kano_frame4_0
        .word 34,73,14,-7
        .long 006d8a370h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame4_1
ks_tr_kano_frame4_1
        .word 35,73,-20,-7
        .long 006d8dda0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose4
ks_tr_kano_pose4
        .long ks_tr_kano_frame4_0,ks_tr_kano_frame4_1,0
        .def ks_tr_kano_frame5_0
ks_tr_kano_frame5_0
        .word 46,42,18,-9
        .long 006d91988h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame5_1
ks_tr_kano_frame5_1
        .word 46,42,-28,-9
        .long 006d946d0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose5
ks_tr_kano_pose5
        .long ks_tr_kano_frame5_0,ks_tr_kano_frame5_1,0
        .def ks_tr_kano_frame6_0
ks_tr_kano_frame6_0
        .word 17,94,14,-47
        .long 006d97418h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_frame6_1
ks_tr_kano_frame6_1
        .word 17,94,-3,-47
        .long 006d99990h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_tr_kano_pose6
ks_tr_kano_pose6
        .long ks_tr_kano_frame6_0,ks_tr_kano_frame6_1,0
        .def ks_kano_torso_ripped

ks_kano_torso_ripped
	.long	ani_adjustxy
	.word	-04aH,004H
	.long	ks_kano_pose_ff829040
	.long	0

	.long	ani_calla,change_to_bloody_pal	; switch to bloody pal
	.long	ks_tr_kano_pose0

	.long	ani_adjustxy
	.word	028H,-020H
	.long	ks_tr_kano_pose1
	.long	0

	.long	ani_adjustxy
	.word	000H,008H
	.long	ks_tr_kano_pose1
	.long	0

	.long	ani_adjustxy
	.word	030H,020H
	.long	ks_tr_kano_pose2

	.long	ani_adjustxy
	.word	030H,040H
	.long	ks_tr_kano_pose3
	.long	0

	.long	ks_tr_kano_pose5
	.long	ks_tr_kano_pose5
;	.long	LKRIPTORSO7
	.long	0
*
* standing legz
*
	.long	ks_tr_kano_pose6			; legz
	.long	0


        .def ks_sw_kano_frame5_0
ks_sw_kano_frame5_0
        .word 46,42,18,-25
        .long 006d91988h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_sw_kano_frame5_1
ks_sw_kano_frame5_1
        .word 46,42,-28,-25
        .long 006d946d0h
        .word 06000h
        .long ks_kano_primary_palette
        .def ks_sw_kano_pose5
ks_sw_kano_pose5
        .long ks_sw_kano_frame5_0,ks_sw_kano_frame5_1,0
        .def ks_kano_swipe_torso

ks_kano_swipe_torso
	.long	ks_tr_kano_pose0
	.long	ks_tr_kano_pose1
	.long	ks_tr_kano_pose2
	.long	ks_tr_kano_pose3
	.long	ks_tr_kano_pose4
	.long	ks_sw_kano_pose5
	.long	0



        .ref ks_sonya_primary_palette
        .ref ks_sonya_pose_ff836b60
        .def ks_tr_sonya_frame0_0
ks_tr_sonya_frame0_0
        .word 26,76,6,10
        .long 006d9bf08h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame0_1
ks_tr_sonya_frame0_1
        .word 27,76,-20,10
        .long 006d9ed58h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose0
ks_tr_sonya_pose0
        .long ks_tr_sonya_frame0_0,ks_tr_sonya_frame0_1,0
        .def ks_tr_sonya_frame1_0
ks_tr_sonya_frame1_0
        .word 22,63,14,-3
        .long 006da1d70h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame1_1
ks_tr_sonya_frame1_1
        .word 22,63,-8,-3
        .long 006da3df0h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame1_2
ks_tr_sonya_frame1_2
        .word 23,63,-30,-3
        .long 006da5e70h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose1
ks_tr_sonya_pose1
        .long ks_tr_sonya_frame1_0,ks_tr_sonya_frame1_1,ks_tr_sonya_frame1_2,0
        .def ks_tr_sonya_frame2_0
ks_tr_sonya_frame2_0
        .word 45,80,16,8
        .long 006da8068h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose2
ks_tr_sonya_pose2
        .long ks_tr_sonya_frame2_0,0
        .def ks_tr_sonya_frame3_0
ks_tr_sonya_frame3_0
        .word 35,57,21,-10
        .long 006dad4c8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame3_1
ks_tr_sonya_frame3_1
        .word 36,57,-14,-10
        .long 006db0390h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose3
ks_tr_sonya_pose3
        .long ks_tr_sonya_frame3_0,ks_tr_sonya_frame3_1,0
        .def ks_tr_sonya_frame4_0
ks_tr_sonya_frame4_0
        .word 29,70,10,-10
        .long 006db33a8h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame4_1
ks_tr_sonya_frame4_1
        .word 30,70,-19,-10
        .long 006db6340h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose4
ks_tr_sonya_pose4
        .long ks_tr_sonya_frame4_0,ks_tr_sonya_frame4_1,0
        .def ks_tr_sonya_frame5_0
ks_tr_sonya_frame5_0
        .word 40,38,12,-14
        .long 006db9478h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame5_1
ks_tr_sonya_frame5_1
        .word 41,38,-28,-14
        .long 006dbb818h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose5
ks_tr_sonya_pose5
        .long ks_tr_sonya_frame5_0,ks_tr_sonya_frame5_1,0
        .def ks_tr_sonya_frame6_0
ks_tr_sonya_frame6_0
        .word 14,94,12,-47
        .long 006dbdca0h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_frame6_1
ks_tr_sonya_frame6_1
        .word 15,94,-2,-47
        .long 006dbfb78h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_tr_sonya_pose6
ks_tr_sonya_pose6
        .long ks_tr_sonya_frame6_0,ks_tr_sonya_frame6_1,0
        .def ks_sonya_torso_ripped

ks_sonya_torso_ripped
	.long	ani_adjustxy
	.word	-04aH,004H
	.long	ks_sonya_pose_ff836b60
	.long	0

	.long	ani_calla,change_to_bloody_pal	; switch to bloody pal
	.long	ks_tr_sonya_pose0

	.long	ani_adjustxy
	.word	028H,-020H
	.long	ks_tr_sonya_pose1
	.long	0

	.long	ani_adjustxy
	.word	000H,008H
	.long	ks_tr_sonya_pose1
	.long	0

	.long	ani_adjustxy
	.word	030H,020H
	.long	ks_tr_sonya_pose2

	.long	ani_adjustxy
	.word	030H,040H
	.long	ks_tr_sonya_pose3
	.long	0

	.long	ks_tr_sonya_pose5
	.long	ks_tr_sonya_pose5
;	.long	LKRIPTORSO7
	.long	0
*
* standing legz
*
	.long	ks_tr_sonya_pose6			; legz
	.long	0


        .def ks_sw_sonya_frame5_0
ks_sw_sonya_frame5_0
        .word 40,38,12,-30
        .long 006db9478h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_sw_sonya_frame5_1
ks_sw_sonya_frame5_1
        .word 41,38,-28,-30
        .long 006dbb818h
        .word 06000h
        .long ks_sonya_primary_palette
        .def ks_sw_sonya_pose5
ks_sw_sonya_pose5
        .long ks_sw_sonya_frame5_0,ks_sw_sonya_frame5_1,0
        .def ks_sonya_swipe_torso

ks_sonya_swipe_torso
	.long	ks_tr_sonya_pose0
	.long	ks_tr_sonya_pose1
	.long	ks_tr_sonya_pose2
	.long	ks_tr_sonya_pose3
	.long	ks_tr_sonya_pose4
	.long	ks_sw_sonya_pose5
	.long	0



