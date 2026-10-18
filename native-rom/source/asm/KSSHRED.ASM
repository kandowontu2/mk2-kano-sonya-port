; Own blade-fury victim DATA, exact native shake/loop controls.
        .include mainequ.asm
        .data
        .ref ks_kano_pose_ff8294a0
        .ref ks_kano_pose_ff829500
        .ref ks_kano_pose_ff829560
        .def ks_kano_shredded

ks_kano_shredded
	.long	ani_adjustxy
	.word	6,6
	.long	ks_kano_pose_ff8294a0

	.long	ani_adjustxy
	.word	-6,-6
	.long	ks_kano_pose_ff829500

	.long	ani_adjustxy
	.word	6,6
	.long	ks_kano_pose_ff829560

	.long	ani_adjustxy
	.word	-6,-6
	.long	ks_kano_pose_ff829500

	.long	ani_jump,ks_kano_shredded

        .ref ks_sonya_pose_ff836860
        .ref ks_sonya_pose_ff8368c0
        .ref ks_sonya_pose_ff836920
        .def ks_sonya_shredded

ks_sonya_shredded
	.long	ani_adjustxy
	.word	6,6
	.long	ks_sonya_pose_ff836860

	.long	ani_adjustxy
	.word	-6,-6
	.long	ks_sonya_pose_ff8368c0

	.long	ani_adjustxy
	.word	6,6
	.long	ks_sonya_pose_ff836920

	.long	ani_adjustxy
	.word	-6,-6
	.long	ks_sonya_pose_ff8368c0

	.long	ani_jump,ks_sonya_shredded

