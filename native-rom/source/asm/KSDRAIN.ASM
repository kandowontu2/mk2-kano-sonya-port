; Native soul-drain lead-in DATA using own recoil/dizzy composites.
        .include mainequ.asm
        .data
        .ref ks_kano_pose_ff829040,ks_kano_pose_ff82a380
        .def ks_kano_drain_reaction
ks_kano_drain_reaction
        .long ani_adjustxy
        .word -048h,-013h
        .long ks_kano_pose_ff829040,0
        .long ani_adjustxy
        .word -10,26
        .long ks_kano_pose_ff82a380
        .long ani_adjustxy
        .word 19,-8
        .long ks_kano_pose_ff82a380
        .long ani_adjustxy
        .word 8,-20
        .long ks_kano_pose_ff82a380
        .long ani_adjustxy
        .word 0,0
        .long ks_kano_pose_ff82a380
        .long 0
        .ref ks_sonya_pose_ff836b60,ks_sonya_pose_ff83b680
        .def ks_sonya_drain_reaction
ks_sonya_drain_reaction
        .long ani_adjustxy
        .word -048h,-013h
        .long ks_sonya_pose_ff836b60,0
        .long ani_adjustxy
        .word -10,26
        .long ks_sonya_pose_ff83b680
        .long ani_adjustxy
        .word 19,-8
        .long ks_sonya_pose_ff83b680
        .long ani_adjustxy
        .word 8,-20
        .long ks_sonya_pose_ff83b680
        .long ani_adjustxy
        .word 0,0
        .long ks_sonya_pose_ff83b680
        .long 0
