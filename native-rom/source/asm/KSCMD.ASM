; Native MKII switch-process entries, with true identity and ownership checks.
        .file "KSCMD.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_lk_release,ks_sonya_high_punch
        .def ks_kano_high_punch,ks_sonya_low_punch
        .ref ks_kano_ball,ks_sonya_square
        .ref ks_kano_knife,ks_sonya_ring
        .ref ks_kano_blade
        .def ks_sonya_high_kick
        .ref ks_sonya_bike
        .def ks_kano_low_punch
        .ref ks_kano_choke
        .def ks_sonya_block
        .def ks_kano_high_kick
        .ref ks_kano_extract,fatality_xfer_close
        .ref ks_sonya_flame_kiss,fatality_xfer
        .ref ks_sonya_bubble
        .ref ks_kano_laser,button_look_lr
        .ref ks_sonya_leg,button_mask,do_switches_match
        .ref get_tsl,combo_look_lr,restricted_xfer,sucide,is_he_airborn
        .ref l_lk
        .text

        .def ks_baby_kick
; Native no-punch eligibility and command history remain in bb_check.
ks_baby_kick
        move *a8(ochar),a0,w
        cmpi 17,a0
        jrne ks_baby_check
        movi f1b0|f1b1|f1b2|f1b3,a0
        movi f2b0|f2b1|f2b2|f2b3,a1
        movi ks_kano_stage_command,a11
        calla combo_look_lr
        jrnc ks_baby_check
        movi f1b0|f1b1|f1b2|f1b3,a0
        movi f2b0|f2b1|f2b2|f2b3,a1
        movi ks_kano_stage_command,a11
        jauc check_dtp
ks_baby_check
        move @winner_status,a0,w
        cmpi 3,a0
        jrne ks_command_reject
        calla is_he_a_boss
        jrc ks_command_reject
        calla get_x_dist
        cmpi 0a0h,a3
        jrlo ks_command_reject
        calla bb_check
        jauc sucide
ks_kano_high_kick
        move *a8(ochar),a0,w
        cmpi 17,a0
        jrne ks_command_reject
        move @winner_status,a0,w
        cmpi 3,a0
        jrne ks_command_reject
        move *a13(p_otherguy),a0,l
        move *a0(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_command_reject
        cmpi ft_final_boss,a0
        jreq ks_command_reject
        movi f1b0|f1b1|f1b2|f1b4,a0
        movi f2b0|f2b1|f2b2|f2b4,a1
        calla button_mask
        jrne ks_command_reject
        calla fs_check
        movi ks_laser_command,a11
        calla button_look_lr
        jrnc ks_kano_extract_check
        calla get_x_dist
        cmpi 128,a3
        jrlo ks_command_reject
        cmpi 288,a3
        jrhi ks_command_reject
        movi ks_kano_laser,a7
        jauc fatality_xfer
ks_kano_extract_check
        movi f1b0|f1b1|f1b2|f1b4,a0
        movi f2b0|f2b1|f2b2|f2b4,a1
        movi ks_extract_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
        movi ks_kano_extract,a7
        movi 070h,a1
        jauc fatality_xfer_close

ks_kano_low_punch
        move *a8(ochar),a0,w
        cmpi 17,a0
        jrne ks_command_reject
        movi f1b0|f1b2|f1b3|f1b4,a0
        movi f2b0|f2b2|f2b3|f2b4,a1
        movi ks_ring_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
        movi ks_kano_choke,a7
        jauc restricted_xfer

ks_sonya_high_kick
        move *a8(ochar),a0,w
        cmpi 18,a0
        jrne ks_command_reject
        move @winner_status,a0,w
        cmpi 3,a0
        jreq ks_sonya_bubble_check
        movi f1b0|f1b1|f1b2|f1b4,a0
        movi f2b0|f2b1|f2b2|f2b4,a1
        movi ks_bike_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
        movi ks_sonya_bike,a7
        jauc restricted_xfer

ks_sonya_bubble_check
        move *a13(p_otherguy),a0,l
        move *a0(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_command_reject
        cmpi ft_final_boss,a0
        jreq ks_command_reject
        movi f1b2,a0
        movi f2b2,a1
        calla button_mask
        jreq ks_command_reject
        movi f1b0|f1b1|f1b4,a0
        movi f2b0|f2b1|f2b4,a1
        movi ks_bubble_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
; Latest Block press must predate the oldest direction, and Block is still down.
        movi l_block,a0
        calla get_tsl
        cmp a10,a1
        jrlo ks_command_reject
        calla get_x_dist
        cmpi 160,a3
        jrlo ks_command_reject
        movi ks_sonya_bubble,a7
        jauc fatality_xfer

ks_kano_high_punch
        move *a8(ochar),a0,w
        cmpi 17,a0
        jrne ks_command_reject
        movi f1b1|f1b2|f1b3|f1b4,a0
        movi f2b1|f2b2|f2b3|f2b4,a1
        movi ks_blade_command,a11
        calla combo_look_lr
        jrnc ks_kano_knife_check
        movi ks_kano_blade,a7
        jauc restricted_xfer
ks_kano_knife_check
        movi f1b1|f1b2|f1b3|f1b4,a0
        movi f2b1|f2b2|f2b3|f2b4,a1
        movi ks_knife_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
        callr ks_projectile_free
        jrne ks_command_reject
        movi ks_kano_knife,a7
        jauc restricted_xfer

ks_sonya_low_punch
        move *a8(ochar),a0,w
        cmpi 18,a0
        jrne ks_command_reject
        move @winner_status,a0,w
        cmpi 3,a0
        jreq ks_sonya_kiss_check
        callr ks_leg_chord
        jrnc ks_sonya_ring_check
        movi ks_sonya_leg,a7
        jauc restricted_xfer

ks_sonya_kiss_check
        move *a13(p_otherguy),a0,l
        move *a0(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_command_reject
        cmpi ft_final_boss,a0
        jreq ks_command_reject
        movi f1b0|f1b2|f1b3|f1b4,a0
        movi f2b0|f2b2|f2b3|f2b4,a1
        movi ks_kiss_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
        movi ks_sonya_flame_kiss,a7
        jauc fatality_xfer
ks_sonya_ring_check
        movi f1b0|f1b2|f1b3|f1b4,a0
        movi f2b0|f2b2|f2b3|f2b4,a1
        movi ks_ring_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
        callr ks_projectile_free
        jrne ks_command_reject
        movi ks_sonya_ring,a7
        jauc restricted_xfer

; One live projectile per physical player, including through morph ownership.
ks_sonya_block
        move *a8(ochar),a0,w
        cmpi 18,a0
        jrne ks_command_reject
        move @winner_status,a0,w
        cmpi 3,a0
        jreq ks_sonya_friend_check
        callr ks_leg_chord
        jrnc ks_command_reject
        movi ks_sonya_leg,a7
        jauc restricted_xfer

; Native shared friendship dispatcher validates the own ending button/history.
ks_sonya_friend_check
        calla fs_check
        jauc sucide

; Accept either button order, but require live LP, Down and primary/redundant Block.
        .def ks_leg_chord
ks_leg_chord
        movi f1b0|f1b3|f1b4,a0
        movi f2b0|f2b3|f2b4,a1
        calla button_mask
        jrne ks_leg_chord_no
        movi f1b1,a0
        movi f2b1,a1
        calla button_mask
        jreq ks_leg_chord_no
        movi f1b2,a0
        movi f2b2,a1
        calla button_mask
        jrne ks_leg_chord_down
        .if wunit
; Wolf button_mask already normalizes both physical Block inputs.
        jruc ks_leg_chord_no
        .else
        move @switch2,a2,l
        not a2
        move @p1_obj,a0,l
        cmp a8,a0
        jrne ks_leg_chord_p2
        btst 2,a2
        jreq ks_leg_chord_no
        jruc ks_leg_chord_down
ks_leg_chord_p2
        btst 6,a2
        jreq ks_leg_chord_no
        .endif
ks_leg_chord_down
        movi ks_leg_down,a0
        calla do_switches_match
        jrnc ks_leg_chord_no
        setc
        rets
ks_leg_chord_no
        clrc
        rets

ks_projectile_free
        movi pid_proj1,a0
        move *a8(oid),a1,w
        cmpi oid_p1,a1
        jreq ks_projectile_pid
        movi pid_proj2,a0
ks_projectile_pid
        movi -1,a1
        calla existp
        move a0,a0
        rets

; Own identity is checked explicitly; no substitution with Liu Kang.
ks_kano_lk_release
        move *a8(ochar),a0,w
        cmpi 17,a0
        jrne ks_command_reject
        movi l_lk,a0
        calla get_tsl
        cmpi 050h,a1
        jrls ks_command_reject
        movi ks_kano_ball,a7
        jauc restricted_xfer

ks_sonya_high_punch
        move *a8(ochar),a0,w
        cmpi 18,a0
        jrne ks_command_reject
        move @winner_status,a0,w
        cmpi 3,a0
        jreq ks_sonya_stage_check
        movi f1b1|f1b2|f1b3|f1b4,a0
        movi f2b1|f2b2|f2b3|f2b4,a1
        movi ks_square_command,a11
        calla combo_look_lr
        jrnc ks_command_reject
; The switch process is not the fighter process. Use the owner only for
; the predicate, then restore it before restricted_xfer performs ownership,
; grounded-state, health and busy checks through the real process fields.
        push a13
        move *a13(p_store4),a13,l
        calla is_he_airborn
        pull a13
        jrnc ks_command_reject
        movi ks_sonya_square,a7
        jauc restricted_xfer
        .ref check_dtp
ks_sonya_stage_check
        movi f1b1|f1b2|f1b3|f1b4,a0
        movi f2b1|f2b2|f2b3|f2b4,a1
        movi ks_sonya_stage_command,a11
        jauc check_dtp
ks_command_reject
        jauc sucide
        .data
ks_laser_command
        .word 050h
        .word sw_hi_kick,sw_block,sw_block,sw_lo_punch,0,0
ks_bubble_command
        .word 038h
        .word sw_down,sw_left,sw_up,sw_up,0,0
        .word sw_down,sw_right,sw_up,sw_up,0,0
ks_kiss_command
        .word 038h
        .word sw_down,sw_down,sw_right,sw_left,0,0
        .word sw_down,sw_down,sw_left,sw_right,0,0
ks_extract_command
        .word 038h
        .word sw_right,sw_down,sw_left,0,0,0
        .word sw_left,sw_down,sw_right,0,0,0
ks_leg_down
        .long 2,0200h
ks_bike_command
        .word 024h
        .word sw_down,sw_left,sw_left,0,0,0
        .word sw_down,sw_right,sw_right,0,0,0
ks_blade_command
        .word 024h
        .word sw_right,sw_down,0,0,0,0
        .word sw_left,sw_down,0,0,0,0
ks_knife_command
        .word 024h
        .word sw_left,sw_down,0,0,0,0
        .word sw_right,sw_down,0,0,0,0
ks_ring_command
        .word 024h
        .word sw_right,sw_down,0,0,0,0
        .word sw_left,sw_down,0,0,0,0
ks_square_command
        .word 024h
        .word sw_left,sw_right,0,0,0,0
        .word sw_right,sw_left,0,0,0,0
ks_kano_stage_command
        .word 050h
        .word sw_left,sw_up,sw_up,0,0,0
        .word sw_right,sw_up,sw_up,0,0,0
ks_sonya_stage_command
        .word 038h
        .word sw_down,sw_right,sw_right,0,0,0
        .word sw_down,sw_left,sw_left,0,0,0
