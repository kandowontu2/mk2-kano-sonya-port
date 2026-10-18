; Sonya Down+LP+Block Leg Grab, own seven-pose entry and five-pose throw.
        .file "KSLEG.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_sonya_leg,ks_leg_wait
        .ref ks_leg_intro,ks_leg_pair,ks_leg_end,ks_leg_victims
        .ref ks_pair_pose,ks_pair_mframew,land_on_my_back,illegal_opcode
        .ref set_noflip,damage_to_me,rsnd_attack
ks_act_leg_seek .set 0219h
ks_act_leg_hold .set 021ah
ks_act_leg_victim .set 021bh
        .text

ks_sonya_leg
        movi ks_act_leg_seek,a1
        calla init_special_act
        calla rsnd_attack
        movk 2,a9
        calla get_char_ani2
        calla do_next_a9_frame
        sleep 3
        calla do_next_a9_frame
        sleep 3
        movk 1,a0
        jsrp mframew
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_leg_miss
        cmpi ft_final_boss,a0
        jreq ks_leg_miss
        movi ks_leg_attack,a0
        calla strike_check
        jrnc ks_leg_miss
        move b2,b2
        jrne ks_leg_blocked
        movi ks_leg_wait,a7
        calla takeover_him
        calla stop_me
        calla set_noflip
        movi ks_act_leg_hold,a0
        move a0,*a13(p_action),w
        move *a13(p_otherproc),a1,l
        movi ks_act_leg_victim,a0
        move a0,*a1(p_action),w
        calla rsnd_big_smack
        movi rsnd_react_voice,a0
        calla calla_for_him
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a0,w
        sll 5,a0
        addi ks_leg_victims,a0
        move *a0,a0,l
        jreq ks_leg_bad_victim
        move a0,*a13(p_store3),l
        clr a0
        move a0,*a13(p_store2),w
        movi ks_leg_pair,a9
        calla do_next_a9_frame
        calla ks_pair_pose
        movk 5,a0
        move a0,*a13(p_store1),w
ks_leg_squeeze
        movk 4,a0
        move a0,@f_norepell,w
        move *a13(p_otherguy),a10,l
        move *a10(oypos),a0,w
        addk 3,a0
        move a0,*a10(oypos),w
        sleep 3
        move *a13(p_otherguy),a10,l
        move *a10(oypos),a0,w
        subk 3,a0
        move a0,*a10(oypos),w
        sleep 3
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_leg_squeeze
        movk 4,a0
        jsrp ks_pair_mframew
        movi ks_leg_release,a7
        calla xfer_otherguy
        movi 061bh,a0
        move a0,*a13(p_action),w
        movi ks_leg_end,a9
        movk 5,a0
        jsrp mframew
        jauc reaction_exit

ks_leg_blocked
        movi 24,a0
        jruc ks_leg_recover
ks_leg_miss
        movi 16,a0
ks_leg_recover
        movi 061bh,a1
        move a1,*a13(p_action),w
        calla prcslp
        movi ks_leg_pair,a9
        movk 5,a0
        jsrp mframew
        movi ks_leg_end,a9
        movk 5,a0
        jsrp mframew
        jauc reaction_exit
ks_leg_bad_victim
        jauc illegal_opcode

ks_leg_wait
        calla disable_all_buttons
        calla stop_me
ks_leg_wait_next
        movk 4,a0
        move a0,@f_norepell,w
        sleep 1
        move *a13(p_otherproc),a0,l
        move *a0(p_action),a0,w
        cmpi ks_act_leg_hold,a0
        jreq ks_leg_wait_next
        jauc reaction_exit

ks_leg_release
        movi act_pit_fall,a0
        move a0,*a13(p_action),w
        calla face_opponent
        calla stop_me
        movi 00fh,a9
        calla do_first_a9_frame
        movi 35,a10
        clr b0
        calla damage_to_me
        movi 030000h,a0
        movi -060000h,a1
        movi 08000h,a2
        movk 4,a3
        jsrp flight
        jauc land_on_my_back

        .data
ks_leg_attack
        .word 115,34,72,77
        .word 01900h,0
        .long 0
        .word sf_duck
