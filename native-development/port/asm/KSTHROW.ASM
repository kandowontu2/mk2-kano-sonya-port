; Own ordinary throws. Entered by native toss eligibility, not switch cheats.
        .file "KSTHROW.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_throw,ks_sonya_throw
        .ref ks_throw_kano_victims,ks_throw_sonya_victims
        .ref ks_kano_throw_phase0,ks_kano_throw_phase1,ks_kano_throw_phase2
        .ref ks_sonya_throw_phase0,ks_sonya_throw_phase1,ks_sonya_throw_phase2
        .ref ks_pair_mframew,ks_pair_pose,land_on_my_back,clear_inviso,delete_slave
        .ref rsnd_grab_voice,rsnd_throw_voice,rsnd_ground,illegal_opcode
ks_act_thrown .set 0226h
        .text
ks_kano_throw
        calla init_special
        movi ks_throw_kano_victims,a0
        callr ks_throw_setup
        movi ks_kano_throw_phase0,a9
        jsrp ks_throw_grab_phase
        calla rsnd_throw_voice
        movi ks_kano_throw_phase1,a9
        movk 4,a0
        jsrp ks_pair_mframew
        movi ks_throw_release,a7
        calla xfer_otherguy
        calla flip_multi
        movi ks_kano_throw_phase2,a9
        movk 4,a0
        jsrp mframew
        calla face_opponent
        retp
ks_sonya_throw
        calla init_special
        movi ks_throw_sonya_victims,a0
        callr ks_throw_setup
        movi ks_sonya_throw_phase0,a9
        jsrp ks_throw_grab_phase
        calla rsnd_throw_voice
        movi ks_sonya_throw_phase1,a9
        movk 4,a0
        jsrp ks_pair_mframew
        movi ks_throw_release,a7
        calla xfer_otherguy
        movi ks_sonya_throw_phase2,a9
        movk 4,a0
        jsrp mframew
        movi 012h,a9
        calla get_char_ani
        movk 4,a0
        jsrp mframew
        calla ground_player
        calla face_opponent
        retp

; Position the victim on the first actual grab pose, not an unrelated stance
; pivot. The first paired record is still consumed by throw phase1 afterward.
ks_throw_grab_phase
        calla do_next_a9_frame
        calla ks_pair_pose
        clr a0
        move a0,*a13(p_store2),w
        sleep 4
        movk 4,a0
        jauc mframew

; A0 = owner-specific19-entry victim descriptor matrix.
ks_throw_setup
        move a0,*a13(p_store4),l
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a1,w
        sll 5,a1
        add a1,a0
        move *a0,a0,l
        jreq ks_throw_bad_victim
        move a0,*a13(p_store4),l
        move *a13(p_otherguy),a0,l
        calla clear_inviso
        calla delete_slave
        calla stop_me
        calla stop_him
        calla set_noflip
        movi ks_throw_wait,a7
        calla takeover_him
        movi act_bodyslam,a0
        move a0,*a13(p_action),w
        move *a13(p_otherproc),a1,l
        movi ks_act_thrown,a0
        move a0,*a1(p_action),w
        move *a13(p_store4),a2,l
        move *a2+,a11,l
        move *a2+,a0,l
        move a0,*a13(p_store3),l
        move *a2,a0,l
        move a0,*a1(p_store1),l
        clr a0
        move a0,*a13(p_store2),w
        calla match_him_with_me_f
        push a8
        move *a13(p_otherguy),a8,l
        move a11,a0
        calla ani2
        pull a8
        calla rsnd_grab_voice
        rets
ks_throw_bad_victim
        jauc illegal_opcode
ks_throw_wait
        calla disable_all_buttons
        calla stop_me
ks_throw_wait_next
        movk 4,a0
        move a0,@f_norepell,w
        sleep 1
        move *a13(p_otherproc),a0,l
        move *a0(p_action),a0,w
        cmpi act_bodyslam,a0
        jreq ks_throw_wait_next
        jauc reaction_exit
ks_throw_release
        movi act_pit_fall,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla face_opponent
        move *a13(p_store1),a9,l
        movi 060000h,a0
        movi -030000h,a1
        movi 08000h,a2
        movk 4,a3
        clr a6
        jsrp flight
        movi 34,a10
        clr b0
        calla damage_to_me
        jauc land_on_my_back
