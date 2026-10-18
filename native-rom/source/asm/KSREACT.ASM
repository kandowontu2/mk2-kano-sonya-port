; Own shared-reaction animation DATA, preserving native caller grammar.
        .file "KSREACT.ASM"
        .include mainequ.asm
        .def ks_kano_bike_victim,ks_sonya_bike_victim
        .def ks_kano_banged,ks_sonya_banged
        .def ks_kano_kintaro_thrown,ks_sonya_kintaro_thrown
        .ref ks_kano_pose_ff829940,ks_kano_pose_ff8299a0
        .ref ks_sonya_pose_ff837060,ks_sonya_pose_ff8370c0
        .ref ks_kano_pose_ff82aa60,ks_kano_pose_ff82aaa0
        .ref ks_kano_pose_ff82ab40,ks_kano_pose_ff82ab80
        .ref ks_sonya_pose_ff83adc0,ks_sonya_pose_ff83ae00
        .ref ks_sonya_pose_ff83aec0,ks_sonya_pose_ff83af20
        .ref ks_kano_pose_ff8294a0,ks_kano_pose_ff829500,ks_kano_pose_ff829560
        .ref ks_kano_pose_ff829620,ks_kano_pose_ff829680
        .ref ks_sonya_pose_ff836860,ks_sonya_pose_ff8368c0,ks_sonya_pose_ff836920
        .ref ks_sonya_pose_ff8369c0,ks_sonya_pose_ff836a00
        .data
; Native MKII a_bike_kicked is STUMBLE1..5 followed by ani_jump.
; These are the same actors' five own stumble poses used in their main23.
ks_kano_bike_victim
        .long ks_kano_pose_ff8294a0,ks_kano_pose_ff829500,ks_kano_pose_ff829560
        .long ks_kano_pose_ff829620,ks_kano_pose_ff829680
        .long ani_jump,ks_kano_bike_victim
ks_sonya_bike_victim
        .long ks_sonya_pose_ff836860,ks_sonya_pose_ff8368c0,ks_sonya_pose_ff836920
        .long ks_sonya_pose_ff8369c0,ks_sonya_pose_ff836a00
        .long ani_jump,ks_sonya_bike_victim
; Native a_banged = LKFLIPPED1..4,0. Use the same explicit own-pose
; mapping as the translated a_lk_fb_lk (main2b), without its throw XY
; commands, separators or landing phases. Native r_orb controls flight.
ks_kano_banged
        .long ks_kano_pose_ff82aa60,ks_kano_pose_ff82aaa0
        .long ks_kano_pose_ff82ab40,ks_kano_pose_ff82ab80,0
ks_sonya_banged
        .long ks_sonya_pose_ff83adc0,ks_sonya_pose_ff83ae00
        .long ks_sonya_pose_ff83aec0,ks_sonya_pose_ff83af20,0
; Native a_fb_goro, including every paired-coordinate adjustment. Pose
; mapping is the same STUMBLE1 / KNOCKDOWN5 / KNOCKDOWN6 used in main23/0f.
; Original MKBOSS goro_slam advances this script with double_mframew.
ks_kano_kintaro_thrown
        .long ani_adjustxy
        .word -060H,-020H
        .long ks_kano_pose_ff8294a0
        .long ani_adjustxy
        .word 010H,-070H
        .long ks_kano_pose_ff8299a0
        .long ani_adjustxy
        .word 020H,000H
        .long ks_kano_pose_ff8299a0
        .long ani_adjustxy
        .word 03aH,020H
        .long ks_kano_pose_ff829940
        .long ani_adjustxy
        .word 038H,010H
        .long ks_kano_pose_ff829940
        .long ani_adjustxy
        .word 000H,068H
        .long ks_kano_pose_ff8299a0,0
ks_sonya_kintaro_thrown
        .long ani_adjustxy
        .word -060H,-020H
        .long ks_sonya_pose_ff836860
        .long ani_adjustxy
        .word 010H,-070H
        .long ks_sonya_pose_ff8370c0
        .long ani_adjustxy
        .word 020H,000H
        .long ks_sonya_pose_ff8370c0
        .long ani_adjustxy
        .word 03aH,020H
        .long ks_sonya_pose_ff837060
        .long ani_adjustxy
        .word 038H,010H
        .long ks_sonya_pose_ff837060
        .long ani_adjustxy
        .word 000H,068H
        .long ks_sonya_pose_ff8370c0,0
