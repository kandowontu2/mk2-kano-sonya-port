; Own throw ART phases and explicit paired-victim XY records.
; Not executable donor code. Not a complete throw action.
        .include mainequ.asm
        .data
        .ref ks_kano_pose_ff8298e0
        .ref ks_kano_pose_ff829940
        .ref ks_kano_pose_ff82a7c0
        .ref ks_kano_pose_ff82a820
        .ref ks_kano_pose_ff82a880
        .ref ks_kano_pose_ff82a8e0
        .ref ks_kano_pose_ff82a940
        .ref ks_kano_pose_ff82a9a0
        .ref ks_kano_pose_ff82aa00
        .ref ks_kano_pose_ff82aa60
        .ref ks_kano_pose_ff82aaa0
        .ref ks_kano_pose_ff82aae0
        .ref ks_kano_pose_ff82ab40
        .ref ks_kano_pose_ff82ab80
        .ref ks_sonya_pose_ff837000
        .ref ks_sonya_pose_ff837060
        .ref ks_sonya_pose_ff837540
        .ref ks_sonya_pose_ff8375a0
        .ref ks_sonya_pose_ff837600
        .ref ks_sonya_pose_ff837660
        .ref ks_sonya_pose_ff8376c0
        .ref ks_sonya_pose_ff837700
        .ref ks_sonya_pose_ff83adc0
        .ref ks_sonya_pose_ff83ae00
        .ref ks_sonya_pose_ff83ae60
        .ref ks_sonya_pose_ff83aec0
        .ref ks_sonya_pose_ff83af20
        .def ks_kano_throw_phase0
ks_kano_throw_phase0
        .long ks_kano_pose_ff82a7c0,ks_kano_pose_ff82a820,0
        .def ks_kano_throw_phase1
ks_kano_throw_phase1
        .long ks_kano_pose_ff82a880,ks_kano_pose_ff82a8e0,ks_kano_pose_ff82a940,0
        .def ks_kano_throw_phase2
ks_kano_throw_phase2
        .long ks_kano_pose_ff82a9a0,ks_kano_pose_ff82aa00,0
        .def ks_th_kano_v_kano,ks_th_kano_v_kano_flight
ks_th_kano_v_kano
        .word -57,-16
        .long ks_kano_pose_ff82aa60
        .word -35,-54
        .long ks_kano_pose_ff82aaa0
        .word 66,-71
        .long ks_kano_pose_ff82aae0
ks_th_kano_v_kano_flight
        .long ks_kano_pose_ff82ab40,ks_kano_pose_ff82ab80,ks_kano_pose_ff8298e0,ks_kano_pose_ff829940,0
        .def ks_th_sonya_v_kano,ks_th_sonya_v_kano_flight
ks_th_sonya_v_kano
        .word -36,0
        .long ks_kano_pose_ff82aa60
        .word -22,1
        .long ks_kano_pose_ff82aaa0
        .word 30,-26
        .long ks_kano_pose_ff82aae0
        .word 93,-31
        .long ks_kano_pose_ff82ab40
        .word 129,-35
        .long ks_kano_pose_ff82ab40
ks_th_sonya_v_kano_flight
        .long ks_kano_pose_ff82ab80,ks_kano_pose_ff8298e0,ks_kano_pose_ff829940,0
        .def ks_sonya_throw_phase0
ks_sonya_throw_phase0
        .long ks_sonya_pose_ff837540,0
        .def ks_sonya_throw_phase1
ks_sonya_throw_phase1
        .long ks_sonya_pose_ff8375a0,ks_sonya_pose_ff837600,ks_sonya_pose_ff837660,ks_sonya_pose_ff8376c0,ks_sonya_pose_ff837700,0
        .def ks_sonya_throw_phase2
ks_sonya_throw_phase2
        .long ks_sonya_pose_ff8376c0,ks_sonya_pose_ff837660,0
        .def ks_th_kano_v_sonya,ks_th_kano_v_sonya_flight
ks_th_kano_v_sonya
        .word -49,-21
        .long ks_sonya_pose_ff83adc0
        .word -12,-55
        .long ks_sonya_pose_ff83ae00
        .word 81,-55
        .long ks_sonya_pose_ff83ae60
ks_th_kano_v_sonya_flight
        .long ks_sonya_pose_ff83aec0,ks_sonya_pose_ff83af20,ks_sonya_pose_ff837000,ks_sonya_pose_ff837060,0
        .def ks_th_sonya_v_sonya,ks_th_sonya_v_sonya_flight
ks_th_sonya_v_sonya
        .word -38,0
        .long ks_sonya_pose_ff83adc0
        .word -5,-3
        .long ks_sonya_pose_ff83ae00
        .word 44,-26
        .long ks_sonya_pose_ff83ae60
        .word 110,-33
        .long ks_sonya_pose_ff83aec0
        .word 184,-38
        .long ks_sonya_pose_ff83aec0
ks_th_sonya_v_sonya_flight
        .long ks_sonya_pose_ff83af20,ks_sonya_pose_ff837000,ks_sonya_pose_ff837060,0
