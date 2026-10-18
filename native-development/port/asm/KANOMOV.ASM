; Kano ROM-side moves. TI GSPA source; all engine calls are linker symbols.
; Own roll script, native held-LK command route and ROM-resident DCS cue.
        .file "KANOMOV.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_ball
        .def ks_ball_animation
        .ref init_special_act,set_noflip,towards_x_vel,get_char_ani
        .ref init_anirate,prcslp,strike_check,next_anirate,stop_me
        .ref ground_player,reaction_exit,away_x_vel,flight_call
        .ref do_land_animation,get_x_dist
        .ref ks_kano_pose_ff828c40,ks_kano_pose_ff828c80
        .ref ks_kano_pose_ff828cc0,ks_kano_pose_ff828d00
        .ref ks_kano_pose_ff828d40,ks_kano_pose_ff828d80
        .ref ks_kano_pose_ff828dc0
        .text

; Entry from native held-LK release gate (>50h ticks).
ks_kano_ball
        movi 020bh,a1
        calla init_special_act
        tsound 0105h
        calla set_noflip
        movi 0a0000h,a0
        calla towards_x_vel
        move *a8(oypos),a1,w
        addk 16,a1
        move a1,*a8(oypos),w
        callr ks_ball_roll
        movk 4,a0
        move a0,@f_norepell,w
        movk 3,a0
        calla init_anirate
        movi 01ah,a11
ks_ball_flight
        movk 3,a0
        move a0,@f_norepell,w
        sleep 1
        cmpi 014h,a11
        jrhi ks_ball_startup
        movi ks_ball_attack,a0
        calla strike_check
        jrc ks_ball_contact
ks_ball_startup
        calla next_anirate
        dec a11
        jrne ks_ball_flight
        calla stop_me
        calla ground_player
        jauc reaction_exit
ks_ball_contact
        movi act_dive_sd,a0
        move a0,*a13(p_action),w
        callr ks_ball_roll
        movi 050000h,a0
        move b2,b2
        jreq ks_ball_recoil
        movi 010000h,a0
ks_ball_recoil
        calla away_x_vel
        move a0,*a8(oxvel),l
        movi dont_touch,a0
        movi -080000h,a1
        movi 06000h,a2
        movk 2,a3
        movi dont_touch,a9
        movi ks_ball_repel,a6
        jsrp flight_call
        jsrp do_land_animation
        jauc reaction_exit
ks_ball_roll
        clr a9
        jauc get_char_ani2
ks_ball_repel
        mmtm sp,a1,a2,a3,a4,a5,a8,a9,a10
        calla get_x_dist
        cmpi 0130h,a3
        jrlo ks_ball_repel_near
        mmfm sp,a1,a2,a3,a4,a5,a8,a9,a10
        movk 3,a0
        rets
ks_ball_repel_near
        mmfm sp,a1,a2,a3,a4,a5,a8,a9,a10
        movk 3,a0
        move a0,@f_norepell,w
        rets
        .data
; Seven tucked rotation poses; independent of ordinary forward-flip roots.
ks_ball_animation
        .long ks_kano_pose_ff828c40,ks_kano_pose_ff828c80
        .long ks_kano_pose_ff828cc0,ks_kano_pose_ff828d00
        .long ks_kano_pose_ff828d40,ks_kano_pose_ff828d80
        .long ks_kano_pose_ff828dc0
        .long ani_jump,ks_ball_animation
ks_ball_attack
        .word 57,8,72,31
        .word 01417h,01805h
        .long 0
        .word 1
