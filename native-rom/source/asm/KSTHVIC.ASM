; Authored throw victim descriptors. Original-roster XY needs visual QA.
        .include mainequ.asm
        .data
        .ref JCFLIPPED1
        .ref JCFLIPPED2
        .ref JCFLIPPED3
        .ref JCFLIPPED4
        .ref JCKNOCKDOWN1
        .ref JXFLIPPED1
        .ref JXFLIPPED2
        .ref JXFLIPPED3
        .ref JXFLIPPED4
        .ref JXKNOCKDOWN1
        .ref KTGETFLIPPED2
        .ref KTGETFLIPPED3
        .ref KTGETFLIPPED4
        .ref KTKNOCKDOWN1
        .ref KTSTUMBLE1
        .ref LKFLIPPED1
        .ref LKFLIPPED2
        .ref LKFLIPPED3
        .ref LKFLIPPED4
        .ref LKKNOCKDOWN1
        .ref NJFLIPPED1
        .ref NJFLIPPED2
        .ref NJFLIPPED3
        .ref NJFLIPPED4
        .ref NJKNOCKDOWN1
        .ref RNFLIPPED1
        .ref RNFLIPPED2
        .ref RNFLIPPED3
        .ref RNFLIPPED4
        .ref RNKNOCKDOWN1
        .ref STFLIPPED2
        .ref STFLIPPED3
        .ref STFLIPPED4
        .ref STKNOCKDOWN1
        .ref STSTUMBLE4
        .ref TMFLIPPED1
        .ref TMFLIPPED2
        .ref TMFLIPPED4
        .ref TMKNOCKDOWN1
        .ref TMSTUMBLE4
        .ref UGFLIPPED1
        .ref UGFLIPPED2
        .ref UGFLIPPED3
        .ref UGFLIPPED4
        .ref UGKNOCKDOWN1
        .ref ks_kano_pose_ff82aa60
        .ref ks_sonya_pose_ff83adc0
        .ref ks_th_kano_v_kano
        .ref ks_th_kano_v_kano_flight
        .ref ks_th_kano_v_sonya
        .ref ks_th_kano_v_sonya_flight
        .ref ks_th_sonya_v_kano
        .ref ks_th_sonya_v_kano_flight
        .ref ks_th_sonya_v_sonya
        .ref ks_th_sonya_v_sonya_flight
        .def ks_throw_kano_victims
ks_throw_kano_victims
        .long ks_tv_kano_0
        .long ks_tv_kano_1
        .long ks_tv_kano_2
        .long ks_tv_kano_3
        .long ks_tv_kano_4
        .long ks_tv_kano_5
        .long ks_tv_kano_6
        .long ks_tv_kano_7
        .long ks_tv_kano_8
        .long ks_tv_kano_9
        .long ks_tv_kano_10
        .long ks_tv_kano_11
        .long 0
        .long 0
        .long ks_tv_kano_14
        .long ks_tv_kano_15
        .long ks_tv_kano_16
        .long ks_tv_kano_17
        .long ks_tv_kano_18
ks_tv_kano_0
        .long TMSTUMBLE4,ks_tp_kano_0,ks_tf_kano_0
ks_tp_kano_0
        .word -57,-16
        .long TMSTUMBLE4
        .word -35,-54
        .long TMFLIPPED1
        .word 66,-71
        .long TMFLIPPED2
ks_tf_kano_0
        .long TMFLIPPED2,TMFLIPPED4,0
ks_tv_kano_1
        .long LKFLIPPED1,ks_tp_kano_1,ks_tf_kano_1
ks_tp_kano_1
        .word -57,-16
        .long LKFLIPPED1
        .word -35,-54
        .long LKFLIPPED2
        .word 66,-71
        .long LKFLIPPED3
ks_tf_kano_1
        .long LKFLIPPED3,LKFLIPPED4,0
ks_tv_kano_2
        .long JCFLIPPED1,ks_tp_kano_2,ks_tf_kano_2
ks_tp_kano_2
        .word -57,-16
        .long JCFLIPPED1
        .word -35,-54
        .long JCFLIPPED2
        .word 66,-71
        .long JCFLIPPED3
ks_tf_kano_2
        .long JCFLIPPED3,JCFLIPPED4,0
ks_tv_kano_3
        .long UGFLIPPED1,ks_tp_kano_3,ks_tf_kano_3
ks_tp_kano_3
        .word -57,-16
        .long UGFLIPPED1
        .word -35,-54
        .long UGFLIPPED2
        .word 66,-71
        .long UGFLIPPED3
ks_tf_kano_3
        .long UGFLIPPED3,UGFLIPPED4,0
ks_tv_kano_4
        .long KTSTUMBLE1,ks_tp_kano_4,ks_tf_kano_4
ks_tp_kano_4
        .word -57,-16
        .long KTSTUMBLE1
        .word -35,-54
        .long KTGETFLIPPED2
        .word 66,-71
        .long KTGETFLIPPED3
ks_tf_kano_4
        .long KTGETFLIPPED3,KTGETFLIPPED4,0
ks_tv_kano_5
        .long KTSTUMBLE1,ks_tp_kano_5,ks_tf_kano_5
ks_tp_kano_5
        .word -57,-16
        .long KTSTUMBLE1
        .word -35,-54
        .long KTGETFLIPPED2
        .word 66,-71
        .long KTGETFLIPPED3
ks_tf_kano_5
        .long KTGETFLIPPED3,KTGETFLIPPED4,0
ks_tv_kano_6
        .long STSTUMBLE4,ks_tp_kano_6,ks_tf_kano_6
ks_tp_kano_6
        .word -57,-16
        .long STSTUMBLE4
        .word -35,-54
        .long STFLIPPED2
        .word 66,-71
        .long STFLIPPED3
ks_tf_kano_6
        .long STFLIPPED3,STFLIPPED4,0
ks_tv_kano_7
        .long RNFLIPPED1,ks_tp_kano_7,ks_tf_kano_7
ks_tp_kano_7
        .word -57,-16
        .long RNFLIPPED1
        .word -35,-54
        .long RNFLIPPED2
        .word 66,-71
        .long RNFLIPPED3
ks_tf_kano_7
        .long RNFLIPPED3,RNFLIPPED4,0
ks_tv_kano_8
        .long NJFLIPPED1,ks_tp_kano_8,ks_tf_kano_8
ks_tp_kano_8
        .word -57,-16
        .long NJFLIPPED1
        .word -35,-54
        .long NJFLIPPED2
        .word 66,-71
        .long NJFLIPPED3
ks_tf_kano_8
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_kano_9
        .long NJFLIPPED1,ks_tp_kano_9,ks_tf_kano_9
ks_tp_kano_9
        .word -57,-16
        .long NJFLIPPED1
        .word -35,-54
        .long NJFLIPPED2
        .word 66,-71
        .long NJFLIPPED3
ks_tf_kano_9
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_kano_10
        .long NJFLIPPED1,ks_tp_kano_10,ks_tf_kano_10
ks_tp_kano_10
        .word -57,-16
        .long NJFLIPPED1
        .word -35,-54
        .long NJFLIPPED2
        .word 66,-71
        .long NJFLIPPED3
ks_tf_kano_10
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_kano_11
        .long JXFLIPPED1,ks_tp_kano_11,ks_tf_kano_11
ks_tp_kano_11
        .word -57,-16
        .long JXFLIPPED1
        .word -35,-54
        .long JXFLIPPED2
        .word 66,-71
        .long JXFLIPPED3
ks_tf_kano_11
        .long JXFLIPPED3,JXFLIPPED4,0
ks_tv_kano_14
        .long NJFLIPPED1,ks_tp_kano_14,ks_tf_kano_14
ks_tp_kano_14
        .word -57,-16
        .long NJFLIPPED1
        .word -35,-54
        .long NJFLIPPED2
        .word 66,-71
        .long NJFLIPPED3
ks_tf_kano_14
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_kano_15
        .long NJFLIPPED1,ks_tp_kano_15,ks_tf_kano_15
ks_tp_kano_15
        .word -57,-16
        .long NJFLIPPED1
        .word -35,-54
        .long NJFLIPPED2
        .word 66,-71
        .long NJFLIPPED3
ks_tf_kano_15
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_kano_16
        .long KTSTUMBLE1,ks_tp_kano_16,ks_tf_kano_16
ks_tp_kano_16
        .word -57,-16
        .long KTSTUMBLE1
        .word -35,-54
        .long KTGETFLIPPED2
        .word 66,-71
        .long KTGETFLIPPED3
ks_tf_kano_16
        .long KTGETFLIPPED3,KTGETFLIPPED4,0
ks_tv_kano_17
        .long ks_kano_pose_ff82aa60,ks_th_kano_v_kano,ks_th_kano_v_kano_flight
ks_tv_kano_18
        .long ks_sonya_pose_ff83adc0,ks_th_kano_v_sonya,ks_th_kano_v_sonya_flight
        .def ks_throw_sonya_victims
ks_throw_sonya_victims
        .long ks_tv_sonya_0
        .long ks_tv_sonya_1
        .long ks_tv_sonya_2
        .long ks_tv_sonya_3
        .long ks_tv_sonya_4
        .long ks_tv_sonya_5
        .long ks_tv_sonya_6
        .long ks_tv_sonya_7
        .long ks_tv_sonya_8
        .long ks_tv_sonya_9
        .long ks_tv_sonya_10
        .long ks_tv_sonya_11
        .long 0
        .long 0
        .long ks_tv_sonya_14
        .long ks_tv_sonya_15
        .long ks_tv_sonya_16
        .long ks_tv_sonya_17
        .long ks_tv_sonya_18
ks_tv_sonya_0
        .long TMSTUMBLE4,ks_tp_sonya_0,ks_tf_sonya_0
ks_tp_sonya_0
        .word -36,0
        .long TMSTUMBLE4
        .word -22,1
        .long TMFLIPPED1
        .word 30,-26
        .long TMFLIPPED2
        .word 93,-31
        .long TMFLIPPED4
        .word 129,-35
        .long TMFLIPPED4
ks_tf_sonya_0
        .long TMFLIPPED2,TMFLIPPED4,0
ks_tv_sonya_1
        .long LKFLIPPED1,ks_tp_sonya_1,ks_tf_sonya_1
ks_tp_sonya_1
        .word -36,0
        .long LKFLIPPED1
        .word -22,1
        .long LKFLIPPED2
        .word 30,-26
        .long LKFLIPPED3
        .word 93,-31
        .long LKFLIPPED4
        .word 129,-35
        .long LKFLIPPED4
ks_tf_sonya_1
        .long LKFLIPPED3,LKFLIPPED4,0
ks_tv_sonya_2
        .long JCFLIPPED1,ks_tp_sonya_2,ks_tf_sonya_2
ks_tp_sonya_2
        .word -36,0
        .long JCFLIPPED1
        .word -22,1
        .long JCFLIPPED2
        .word 30,-26
        .long JCFLIPPED3
        .word 93,-31
        .long JCFLIPPED4
        .word 129,-35
        .long JCFLIPPED4
ks_tf_sonya_2
        .long JCFLIPPED3,JCFLIPPED4,0
ks_tv_sonya_3
        .long UGFLIPPED1,ks_tp_sonya_3,ks_tf_sonya_3
ks_tp_sonya_3
        .word -36,0
        .long UGFLIPPED1
        .word -22,1
        .long UGFLIPPED2
        .word 30,-26
        .long UGFLIPPED3
        .word 93,-31
        .long UGFLIPPED4
        .word 129,-35
        .long UGFLIPPED4
ks_tf_sonya_3
        .long UGFLIPPED3,UGFLIPPED4,0
ks_tv_sonya_4
        .long KTSTUMBLE1,ks_tp_sonya_4,ks_tf_sonya_4
ks_tp_sonya_4
        .word -36,0
        .long KTSTUMBLE1
        .word -22,1
        .long KTGETFLIPPED2
        .word 30,-26
        .long KTGETFLIPPED3
        .word 93,-31
        .long KTGETFLIPPED4
        .word 129,-35
        .long KTGETFLIPPED4
ks_tf_sonya_4
        .long KTGETFLIPPED3,KTGETFLIPPED4,0
ks_tv_sonya_5
        .long KTSTUMBLE1,ks_tp_sonya_5,ks_tf_sonya_5
ks_tp_sonya_5
        .word -36,0
        .long KTSTUMBLE1
        .word -22,1
        .long KTGETFLIPPED2
        .word 30,-26
        .long KTGETFLIPPED3
        .word 93,-31
        .long KTGETFLIPPED4
        .word 129,-35
        .long KTGETFLIPPED4
ks_tf_sonya_5
        .long KTGETFLIPPED3,KTGETFLIPPED4,0
ks_tv_sonya_6
        .long STSTUMBLE4,ks_tp_sonya_6,ks_tf_sonya_6
ks_tp_sonya_6
        .word -36,0
        .long STSTUMBLE4
        .word -22,1
        .long STFLIPPED2
        .word 30,-26
        .long STFLIPPED3
        .word 93,-31
        .long STFLIPPED4
        .word 129,-35
        .long STFLIPPED4
ks_tf_sonya_6
        .long STFLIPPED3,STFLIPPED4,0
ks_tv_sonya_7
        .long RNFLIPPED1,ks_tp_sonya_7,ks_tf_sonya_7
ks_tp_sonya_7
        .word -36,0
        .long RNFLIPPED1
        .word -22,1
        .long RNFLIPPED2
        .word 30,-26
        .long RNFLIPPED3
        .word 93,-31
        .long RNFLIPPED4
        .word 129,-35
        .long RNFLIPPED4
ks_tf_sonya_7
        .long RNFLIPPED3,RNFLIPPED4,0
ks_tv_sonya_8
        .long NJFLIPPED1,ks_tp_sonya_8,ks_tf_sonya_8
ks_tp_sonya_8
        .word -36,0
        .long NJFLIPPED1
        .word -22,1
        .long NJFLIPPED2
        .word 30,-26
        .long NJFLIPPED3
        .word 93,-31
        .long NJFLIPPED4
        .word 129,-35
        .long NJFLIPPED4
ks_tf_sonya_8
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_sonya_9
        .long NJFLIPPED1,ks_tp_sonya_9,ks_tf_sonya_9
ks_tp_sonya_9
        .word -36,0
        .long NJFLIPPED1
        .word -22,1
        .long NJFLIPPED2
        .word 30,-26
        .long NJFLIPPED3
        .word 93,-31
        .long NJFLIPPED4
        .word 129,-35
        .long NJFLIPPED4
ks_tf_sonya_9
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_sonya_10
        .long NJFLIPPED1,ks_tp_sonya_10,ks_tf_sonya_10
ks_tp_sonya_10
        .word -36,0
        .long NJFLIPPED1
        .word -22,1
        .long NJFLIPPED2
        .word 30,-26
        .long NJFLIPPED3
        .word 93,-31
        .long NJFLIPPED4
        .word 129,-35
        .long NJFLIPPED4
ks_tf_sonya_10
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_sonya_11
        .long JXFLIPPED1,ks_tp_sonya_11,ks_tf_sonya_11
ks_tp_sonya_11
        .word -36,0
        .long JXFLIPPED1
        .word -22,1
        .long JXFLIPPED2
        .word 30,-26
        .long JXFLIPPED3
        .word 93,-31
        .long JXFLIPPED4
        .word 129,-35
        .long JXFLIPPED4
ks_tf_sonya_11
        .long JXFLIPPED3,JXFLIPPED4,0
ks_tv_sonya_14
        .long NJFLIPPED1,ks_tp_sonya_14,ks_tf_sonya_14
ks_tp_sonya_14
        .word -36,0
        .long NJFLIPPED1
        .word -22,1
        .long NJFLIPPED2
        .word 30,-26
        .long NJFLIPPED3
        .word 93,-31
        .long NJFLIPPED4
        .word 129,-35
        .long NJFLIPPED4
ks_tf_sonya_14
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_sonya_15
        .long NJFLIPPED1,ks_tp_sonya_15,ks_tf_sonya_15
ks_tp_sonya_15
        .word -36,0
        .long NJFLIPPED1
        .word -22,1
        .long NJFLIPPED2
        .word 30,-26
        .long NJFLIPPED3
        .word 93,-31
        .long NJFLIPPED4
        .word 129,-35
        .long NJFLIPPED4
ks_tf_sonya_15
        .long NJFLIPPED3,NJFLIPPED4,0
ks_tv_sonya_16
        .long KTSTUMBLE1,ks_tp_sonya_16,ks_tf_sonya_16
ks_tp_sonya_16
        .word -36,0
        .long KTSTUMBLE1
        .word -22,1
        .long KTGETFLIPPED2
        .word 30,-26
        .long KTGETFLIPPED3
        .word 93,-31
        .long KTGETFLIPPED4
        .word 129,-35
        .long KTGETFLIPPED4
ks_tf_sonya_16
        .long KTGETFLIPPED3,KTGETFLIPPED4,0
ks_tv_sonya_17
        .long ks_kano_pose_ff82aa60,ks_th_sonya_v_kano,ks_th_sonya_v_kano_flight
ks_tv_sonya_18
        .long ks_sonya_pose_ff83adc0,ks_th_sonya_v_sonya,ks_th_sonya_v_sonya_flight
