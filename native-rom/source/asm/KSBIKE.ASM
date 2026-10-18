; Sonya B,B,D+HK Bicycle Kick. Native seek/block/paired/release states.
        .file "KSBIKE.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_sonya_bike,ks_bike_wait,ks_bike_push
        .ref ks_bike_intro,ks_bike_cycle,ks_bike_end,land_on_my_back
        .ref set_noflip
ks_act_bike_pair .set 0214h
ks_act_bike_victim .set 0215h
        .text

ks_sonya_bike
        movi act_bike,a1
        calla init_special_act
        tsound 0ffh
        movk 1,a9
        calla get_char_ani2
        movk 2,a0
        jsrp mframew
        movi ks_bike_cycle,a9
        movk 4,a0
        calla init_anirate
        movi 040000h,a0
        calla towards_x_vel
        move a0,*a8(oxvel),l
        movi -020000h,a0
        move a0,*a8(oyvel),l
        movi -0c000h,a0
        move a0,*a8(ograv),l
ks_bike_seek
        sleep 1
        callr ks_bike_push
        move *a13(p_otherproc),a0,l
        move *a0(p_action),a1,w
        cmpi act_duck,a1
        jreq ks_bike_seek_next
        cmpi act_blocklo,a1
        jreq ks_bike_seek_next
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_bike_seek_next
        cmpi ft_final_boss,a0
        jreq ks_bike_seek_next
        movi ks_bike_attack,a0
        calla strike_check
        jrc ks_bike_contact
ks_bike_seek_next
        calla next_anirate
        calla distance_from_ground
        cmpi 0c0h,a0
        jrlt ks_bike_seek
; Miss: keep the forward arc, add native gravity and land normally.
        movi 0611h,a0
        move a0,*a13(p_action),w
        movi dont_touch,a0
        movi dont_touch,a1
        movi 0a000h,a2
        movk 4,a3
        movi ks_bike_push,a6
        jsrp flight_call
        jsrp do_land_animation
        jauc reaction_exit

ks_bike_contact
        move b2,b2
        jrne ks_bike_blocked
        tsound 0100h
        movi ks_bike_wait,a7
        calla takeover_him
        movi ks_act_bike_pair,a0
        move a0,*a13(p_action),w
        move *a13(p_otherproc),a1,l
        movi ks_act_bike_victim,a0
        move a0,*a1(p_action),w
        calla set_noflip
        mmtm sp,a9,a10,a11
        movi 00030030h,a11
        calla shake_a11
        mmfm sp,a9,a10,a11
; Keep a separate native victim cursor; no substitute actor ID or body.
        mmtm sp,a8,a9
        move *a13(p_otherguy),a8,l
        movi 023h,a9
        calla get_char_ani
        move a9,*a13(p_store3),l
        move a9,*a13(p_store4),l
        mmfm sp,a8,a9
        calla stop_him
        calla stop_me
        movk 4,a0
        calla init_anirate
        movk 1,a0
        move a0,*a13(p_store2),w
        movi 030000h,a0
        move a0,*a13(p_store6),l
        movi -030000h,a0
        move a0,*a13(p_store5),l
        callr ks_bike_velocity
        movi 32,a0
        move a0,*a13(p_store1),w
ks_bike_lift
        sleep 1
        callr ks_bike_tick
        calla distance_from_ground
        cmpi 0e0h,a0
        jrge ks_bike_float_start
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_bike_lift
ks_bike_float_start
        movi 010000h,a0
        move a0,*a13(p_store6),l
        movi 08000h,a0
        move a0,*a13(p_store5),l
        callr ks_bike_velocity
        movi 16,a0
        move a0,*a13(p_store1),w
ks_bike_float
        sleep 1
        callr ks_bike_tick
        move *a13(p_store1),a0,w
        dec a0
        move a0,*a13(p_store1),w
        jrne ks_bike_float
        movi pid_shaker,a0
        calla dallprc
        movi ks_bike_release,a7
        calla xfer_otherguy
        movi 0611h,a0
        move a0,*a13(p_action),w
        calla stop_me
        movi ks_bike_end,a9
        movk 4,a0
        jsrp mframew
        movk 6,a9
        calla find_ani_part2
        calla do_next_a9_frame
        clr a0
        movi 020000h,a1
        movi 08000h,a2
        movi never_ani,a3
        jsrp flight
        jsrp do_land_animation
        jauc reaction_exit

ks_bike_blocked
        movi 0611h,a0
        move a0,*a13(p_action),w
        calla stop_me
        clr a0
        movi -060000h,a1
        movi 08000h,a2
        movk 4,a3
        jsrp flight
        jsrp do_land_animation
        jauc reaction_exit

ks_bike_push
        movk 3,a0
        move a0,@f_norepell,w
        rets

ks_bike_tick
        callr ks_bike_push
        move *a13(p_store2),a0,w
        dec a0
        jrne ks_bike_no_impact
        mmtm sp,a9,a10,a11
        calla rsnd_big_smack
        mmfm sp,a9,a10,a11
        movk 7,a0
ks_bike_no_impact
        move a0,*a13(p_store2),w
        calla match_him_with_me_f
        movi -48,a0
        movi -32,a1
        calla adjust_him_xy
        callr ks_bike_velocity
        calla next_anirate
        move *a13(p_anicount),a0,w
        cmpi 4,a0
        jrne ks_bike_tick_done
        move *a13(p_otherguy),a10,l
        move *a13(p_store3),a11,l
        calla do_next_a11_for_a10
        jrne ks_bike_victim_store
        move *a13(p_store4),a11,l
        calla do_next_a11_for_a10
ks_bike_victim_store
        move a11,*a13(p_store3),l
ks_bike_tick_done
        rets

ks_bike_velocity
; Both actual velocities and native player requests must change at phase
; transitions, even when the normal close-body publication path is suppressed.
        move *a13(p_store6),a0,l
        calla towards_x_vel
        move a0,*a8(oxvel),l
        move *a13(p_otherguy),a10,l
        move a0,*a10(oxvel),l
        push a8
        move a10,a8
        calla set_x_vel
        pull a8
        move *a13(p_otherguy),a10,l
        move *a13(p_store5),a0,l
        move a0,*a8(oyvel),l
        move a0,*a10(oyvel),l
        clr a0
        move a0,*a8(ograv),l
        move a0,*a10(ograv),l
        rets

ks_bike_wait
        calla disable_all_buttons
ks_bike_wait_next
        sleep 1
        move *a13(p_otherproc),a0,l
        move *a0(p_action),a0,w
        cmpi ks_act_bike_pair,a0
        jreq ks_bike_wait_next
ks_bike_release
        movi act_pit_fall,a0
        move a0,*a13(p_action),w
        calla stop_me
        movi 00fh,a9
        movi 040000h,a0
        movi -060000h,a1
        movi 0a000h,a2
        movk 5,a3
        jsrp flight
        jauc land_on_my_back

        .data
ks_bike_attack
        .word 54,3,57,53
        .word 01a01h,01603h
        .long 0
        .word sf_squeeze
