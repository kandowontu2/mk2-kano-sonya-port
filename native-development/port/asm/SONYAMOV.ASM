; Sonya ROM-side moves. TI GSPA source, not embedded opcode arrays.
; Own square-wave pose script, routed through native F,B+HP command.
; Native priority-table FE routes launch to own DCS playlists2000/2001/2002.
        .file "SONYAMOV.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_sonya_square
        .def ks_square_animation
        .ref init_special_act,find_ani_last_frame,do_next_a9_frame
        .ref distance_off_ground,get_char_ani,init_anirate,towards_x_vel
        .ref next_anirate,strike_check,pose_a9,stop_me,face_opponent
        .ref flight,do_land_animation,reaction_exit,away_x_vel
        .ref ks_sonya_pose_ff836160,ks_sonya_pose_ff8361a0
        .ref ks_sonya_pose_ff840880
        .text

; Entry: normal native special-action transfer; A8 actor, A13 process.
; Caller must enforce F,B+HP command and airborne-opponent prerequisite.
ks_sonya_square
        movi 0207h,a1
        calla init_special_act
        tsound 0feh
        movk 6,a9
        calla find_ani_last_frame
        calla do_next_a9_frame
        movi -0c0000h,a0
        move a0,*a8(oyvel),l
ks_square_rise
        sleep 1
        calla distance_off_ground
        cmpi 060h,a0
        jrlo ks_square_rise
        clr a0
        move a0,*a8(oyvel),l
        clr a9
        calla get_char_ani2
        movk 3,a0
        calla init_anirate
        movi 0a0000h,a0
        calla towards_x_vel
        movi 01ah,a11
ks_square_flight
        sleep 1
        calla next_anirate
        movi ks_square_attack,a0
        calla strike_check
        jrc ks_square_contact
        dec a11
        jrne ks_square_flight
ks_square_recover
        movk 6,a9
        calla pose_a9
        calla stop_me
        calla face_opponent
        clr a0
        movi 020000h,a1
        movi 08000h,a2
        movi never_ani,a3
        movi dont_touch,a9
        jsrp flight
        jsrp do_land_animation
        jauc reaction_exit
ks_square_contact
        calla stop_me
        movi ks_square_contact_pose,a9
        calla do_next_a9_frame
        sleep 10
        movi 020000h,a0
        calla away_x_vel
        jruc ks_square_recover
        .data
; Native MKII control tokens, own imported square-wave art, no ordinary slot reuse.
ks_square_animation
        .long ks_sonya_pose_ff836160,ks_sonya_pose_ff8361a0
ks_square_contact_pose
        .long ks_sonya_pose_ff840880
        .long ani_jump,ks_square_contact_pose
ks_square_attack
        .word 70,15,58,52
        .word 01417h,01b08h
        .long 0
        .word 1
