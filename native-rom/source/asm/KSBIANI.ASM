; Own bicycle body scripts, original compressed art and native control tokens.
        .include mainequ.asm
        .ref ks_bike_push
        .ref ks_sonya_pose_ff83ea40
        .ref ks_sonya_pose_ff83ea80
        .ref ks_sonya_pose_ff83eae0
        .ref ks_sonya_pose_ff83eb40
        .ref ks_sonya_pose_ff83eb80
        .ref ks_sonya_pose_ff83ebc0
        .ref ks_sonya_pose_ff83ec00
        .ref ks_sonya_pose_ff83ec40
        .ref ks_sonya_pose_ff83ec80
        .def ks_bike_intro,ks_bike_cycle,ks_bike_end
        .data
ks_bike_intro
        .long ani_calla,ks_bike_push
        .long ani_adjustxy
        .word 5,10
        .long ks_sonya_pose_ff83ea40
        .long ani_calla,ks_bike_push
        .long ani_adjustxy
        .word 5,10
        .long ks_sonya_pose_ff83ea80
        .long ani_calla,ks_bike_push
        .long ani_adjustxy
        .word 5,10
        .long ks_sonya_pose_ff83eae0
        .long 0
ks_bike_cycle
        .long ks_sonya_pose_ff83eb40
        .long ks_sonya_pose_ff83eb80
        .long ks_sonya_pose_ff83ebc0
        .long ks_sonya_pose_ff83ec00
        .long ks_sonya_pose_ff83ec40
        .long ks_sonya_pose_ff83ec80
        .long ks_sonya_pose_ff83ec40
        .long ks_sonya_pose_ff83ec00
        .long ks_sonya_pose_ff83ebc0
        .long ks_sonya_pose_ff83eb80
        .long ani_jump,ks_bike_cycle
ks_bike_end
        .long ks_sonya_pose_ff83eae0
        .long ks_sonya_pose_ff83ea80
        .long ks_sonya_pose_ff83ea40
        .long 0
