; Native Sonya Friendship action; original own art, no donor callback execution.
        .file "KSFRIEND.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_sonya_friend
        .def ks_kano_friend
        .ref ks_friend_kano_body,ks_friend_kano_bubbles
        .ref ks_friend_palette_ffcdf710,get_proj_obj_m,kmo_proc
        .ref ks_friend_pose_ff9d2610,ks_friend_pose_ff9d2650
        .ref ks_friend_pose_ff9d2690,ks_friend_pose_ff9d26d0
        .ref ks_friend_pose_ff9d2710,ks_friend_pose_ff9d2750,ks_friend_pose_ff9d2790
        .ref friendship_start,friendship_end,ks_friend_sonya_intro
        .ref ks_friend_pose_ff9d2f70,ks_friend_pose_ff9d2ff0
        .ref ks_friend_pose_ff9d3070,ks_friend_pose_ff9d30f0
        .ref ks_friend_pose_ff9d2ef0,ks_friend_pose_ff9d2e50
        .ref ks_friend_pose_ff9d2db0,ks_friend_pose_ff9d2d10
        .text

; Non-sleeping original 1..4 selection, through MKII's native effect allocator.
ks_chicken_sound
        mmtm sp,a0,a1,a2,a3,a4,a5,a6
        movk 4,a0
        calla randu
        dec a0
        addi 0106h,a0
        calla triple_sound
        mmfm sp,a0,a1,a2,a3,a4,a5,a6
        rets
ks_kano_friend
        movi 0227h,a1
        calla init_special_act
        calla stop_me
        jsrp friendship_start
        movk 5,a9
        calla get_char_ani2
        movk 5,a0
        jsrp mframew
        movi ks_friend_kano_bubbles,a9
        calla get_proj_obj_m
        push a8
        move *a13(p_slave),a8,l
        movi ks_friend_palette_ffcdf710,a0
        calla swpal
        calla insobja8
        pull a8
        movi ks_gum_frames,a9
ks_gum_next
        move *a9+,a0,l
        jreq ks_gum_done
        push a9
        move a0,*a13(p_store5),l
        cmpi ks_friend_pose_ff9d2750,a0
        jrne ks_gum_no_pop
        tsound 0104h
ks_gum_no_pop
        move *a13(p_slave),a0,l
        calla match_ani_points
        push a8
        move *a13(p_slave),a8,l
        move *a13(p_store5),a0,l
        calla ani2
        pull a8
        pull a9
        sleep 5
        jruc ks_gum_next
ks_gum_done
        move *a13(p_slave),a2,l
        calla kmo_proc
        clr a0
        move a0,*a13(p_slave),l
        calla friendship_end
        jauc wait_forever
ks_sonya_friend
        movi 0226h,a1
        calla init_special_act
        calla stop_me
        jsrp friendship_start
; Native MKII dramatic pause is 48 fields. Original scene's asynchronous
; completion delay is 128; retain a cooperative owner rather than host timers.
        create pid_fx,ks_friend_complete
        movk 5,a9
        calla get_char_ani2
        movk 5,a0
        jsrp mframew
ks_chicken_loop
        movi ks_chicken_frames,a9
        movk 3,a0
        jsrp mframew
        jruc ks_chicken_loop
ks_friend_complete
        sleep 080h
        calla friendship_end
        die
        .data
ks_gum_frames
        .long ks_friend_pose_ff9d2610,ks_friend_pose_ff9d2650
        .long ks_friend_pose_ff9d2690,ks_friend_pose_ff9d26d0
        .long ks_friend_pose_ff9d2710,ks_friend_pose_ff9d2710
        .long ks_friend_pose_ff9d2710,ks_friend_pose_ff9d2710
        .long ks_friend_pose_ff9d2710,ks_friend_pose_ff9d2750
        .long ks_friend_pose_ff9d2790,0
ks_chicken_frames
        .long ks_friend_pose_ff9d2f70,ks_friend_pose_ff9d2ff0
        .long ani_calla,ks_chicken_sound
        .long ks_friend_pose_ff9d3070,ks_friend_pose_ff9d30f0
        .long ani_calla,ks_chicken_sound
        .long ks_friend_pose_ff9d3070,ks_friend_pose_ff9d2ff0
        .long ani_calla,ks_chicken_sound
        .long ks_friend_pose_ff9d2f70,ks_friend_pose_ff9d2ef0
        .long ks_friend_pose_ff9d2e50,ks_friend_pose_ff9d2db0
        .long ks_friend_pose_ff9d2d10,ks_friend_pose_ff9d2db0
        .long ks_friend_pose_ff9d2e50,ks_friend_pose_ff9d2ef0,0
