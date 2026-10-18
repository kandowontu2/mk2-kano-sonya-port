; Kano D,F+LP Choke: six-field catch, own paired lift, four native damage pulses.
        .file "KSCHOKE.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_choke,ks_choke_wait
        .ref ks_choke_intro,ks_choke_lift,ks_choke_cycle,ks_choke_end
        .ref ks_choke_victims,land_on_my_back,set_noflip,illegal_opcode
        .ref ks_pair_pose,ks_pair_mframew
ks_act_choke_seek .set 0216h
ks_act_choke_hold .set 0217h
ks_act_choke_victim .set 0218h
        .text

ks_kano_choke
        movi ks_act_choke_seek,a1
        calla init_special_act
        movk 2,a9
        calla get_char_ani2
        movk 3,a0
        jsrp mframew
        movk 6,a0
        move a0,*a13(p_store1),w
ks_choke_check
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_choke_no_contact
        cmpi ft_final_boss,a0
        jreq ks_choke_no_contact
        movi ks_choke_attack,a0
        calla strike_check
        jrc ks_choke_contact
ks_choke_no_contact
        sleep 1
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_choke_check
ks_choke_miss
        sleep 10
        movi ks_choke_end,a9
        movk 5,a0
        jsrp mframew
        jauc reaction_exit

ks_choke_contact
        move b2,b2
        jrne ks_choke_miss
        movi ks_choke_wait,a7
        calla takeover_him
        calla stop_me
        calla set_noflip
        movi ks_act_choke_hold,a0
        move a0,*a13(p_action),w
        move *a13(p_otherproc),a1,l
        movi ks_act_choke_victim,a0
        move a0,*a1(p_action),w
        movi rsnd_react_voice,a0
        calla calla_for_him
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a0,w
        sll 5,a0
        addi ks_choke_victims,a0
        move *a0,a0,l
        jreq ks_choke_bad_victim
        move a0,*a13(p_store3),l
        clr a0
        move a0,*a13(p_store2),w
        movi ks_choke_lift,a9
        movk 5,a0
        jsrp ks_pair_mframew
        movk 4,a0
        move a0,*a13(p_store1),w
ks_choke_squeeze
        movk 3,a0
        move a0,*a13(p_store2),w
        movi ks_choke_cycle,a9
        movk 3,a0
        jsrp ks_pair_mframew
        mmtm sp,a9,a10,a11
        movk 8,a0
        calla damage_to_him
        mmfm sp,a9,a10,a11
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_choke_squeeze
; Preserve the final held pose until the native release flight's first field.
        movk 3,a0
        move a0,*a13(p_store2),w
        move a0,*a13(p_store1),w
        movi ks_choke_cycle,a9
ks_choke_final_poses
        calla do_next_a9_frame
        calla ks_pair_pose
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jreq ks_choke_release_now
        sleep 3
        jruc ks_choke_final_poses
ks_choke_release_now
        movi ks_choke_release,a7
        calla xfer_otherguy
        movi 061ah,a0
        move a0,*a13(p_action),w
        sleep 8
        movi ks_choke_end,a9
        movk 2,a0
        jsrp mframew
        jauc reaction_exit

ks_choke_bad_victim
        jauc illegal_opcode

ks_choke_wait
        calla disable_all_buttons
        calla stop_me
ks_choke_wait_next
        movk 4,a0
        move a0,@f_norepell,w
        sleep 2
        move *a13(p_otherproc),a0,l
        move *a0(p_action),a0,w
        cmpi ks_act_choke_hold,a0
        jreq ks_choke_wait_next
        jauc reaction_exit

ks_choke_release
        movi act_pit_fall,a0
        move a0,*a13(p_action),w
        calla stop_me
        movi 00fh,a9
        movi 040000h,a0
        movi -040000h,a1
        movi 08000h,a2
        movk 5,a3
        jsrp flight
        jauc land_on_my_back

        .data
ks_choke_attack
        .word 101,32,63,17
        .word 01a00h,0
        .long 0
        .word sf_squeeze
