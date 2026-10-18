; Native Kano Eye Laser. Named body/beam events, actual victim and owned effect.
        .file "KSLASER.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_laser
        .ref ks_laser_phase0,ks_laser_phase1,ks_laser_phase2
        .ref ks_laser_beam_start,ks_laser_palette,ks_laser_victims
        .ref get_proj_obj_m,kmo_proc,disable_repell,illegal_opcode
        .text

ks_kano_laser
        movk 1,a0
        movk 2,a1
        calla init_death_blow
        movi 0223h,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_repell
        movk 4,a9
        calla get_char_ani2
        jsrp ks_laser_play
        movi ks_laser_victim,a7
        calla takeover_him
        movk 4,a0
        move a0,*a13(p_store1),w
        tsound 092h
ks_laser_sustain
        movi ks_laser_phase1,a9
        jsrp ks_laser_play
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_laser_sustain
        movi ks_laser_hidden,a7
        calla xfer_otherguy
        movi ks_laser_phase2,a9
        jsrp ks_laser_play
        move *a13(p_slave),a2,l
        calla kmo_proc
        clr a0
        move a0,*a13(p_slave),l
        calla death_blow_complete
        jauc victory_animation

; A9 event: long body/beam, word field delay/create flag. Zero delay terminates.
ks_laser_play
        move *a9+,a0,l
        move a0,*a13(p_store5),l
        move *a9+,a0,l
        move a0,*a13(p_store6),l
        move *a9+,a0,w
        jreq ks_laser_play_done
        move a0,*a13(p_store7),w
        move *a9+,a0,w
        jreq ks_laser_body
        push a9
        movi ks_laser_beam_start,a9
        calla get_proj_obj_m
        push a8
        move *a13(p_slave),a8,l
        movi ks_laser_palette,a0
        calla swpal
        calla insobja8
        pull a8
        pull a9
ks_laser_body
        move *a13(p_store5),a0,l
        jreq ks_laser_beam
        calla ani2
ks_laser_beam
        move *a13(p_store6),a0,l
        jreq ks_laser_delay
        move *a13(p_slave),a0,l
        calla match_ani_points
        push a8
        move *a13(p_slave),a8,l
        move *a13(p_store6),a0,l
        calla ani2
        pull a8
ks_laser_delay
        move *a13(p_store7),a0,w
        calla prcslp
        jruc ks_laser_play
ks_laser_play_done
        retp

ks_laser_victim
        movi 0224h,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_all_buttons
        move *a8(ochar),a0,w
        sll 5,a0
        addi ks_laser_victims,a0
        move *a0,a0,l
        jreq ks_laser_bad_victim
        calla ani2
; Retain this actor's native standing Y while lining up the horizontal beam.
        push a14
        move *a8(oyval),a14,l
        calla match_me_with_him
        calla flip_multi
        move a14,*a8(oyval),l
        pull a14
        movi -184,a0
        clr a1
        calla multi_adjust_xy
        calla rsnd_death_voice
        callr ks_laser_blood
        movk 5,a0
        move a0,*a13(p_store1),w
        movk 3,a0
        move a0,*a13(p_store2),w
ks_laser_small_shake
        jsrp ks_laser_shake
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_laser_small_shake
        callr ks_laser_blood
        movi 10,a0
        move a0,*a13(p_store1),w
        movk 5,a0
        move a0,*a13(p_store2),w
ks_laser_big_shake
        jsrp ks_laser_shake
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_laser_big_shake
        callr ks_laser_blood
ks_laser_last_shake
        jsrp ks_laser_shake
        jruc ks_laser_last_shake

ks_laser_shake
        move *a13(p_store2),a0,w
        move *a8(oypos),a1,w
        add a0,a1
        move a1,*a8(oypos),w
        sleep 3
        move *a13(p_store2),a0,w
        move *a8(oypos),a1,w
        sub a0,a1
        move a1,*a8(oypos),w
        sleep 3
        retp

ks_laser_blood
        movk 2,a0
        calla create_blood_proc
        rets

ks_laser_hidden
        movi 0225h,a0
        move a0,*a13(p_action),w
        calla stop_me
        move a8,a0
        calla set_inviso
        jauc wait_forever
ks_laser_bad_victim
        jauc illegal_opcode
