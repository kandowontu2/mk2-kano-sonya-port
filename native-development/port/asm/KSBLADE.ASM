; Kano Blade Swipe: own actor animation, native attached trail and victim state.
        .file "KSBLADE.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_blade,ks_blade_fx_step,ks_blade_hurt
        .ref ks_blade_animation,reaction_start_abc,airborn_hit_no_sound
        .text

ks_kano_blade
        movi 0117h,a1
        calla init_special_act
        tsound 0c8h
        movk 1,a9
        calla get_char_ani2
        movk 2,a0
        jsrp mframew
        movi ks_blade_attack,a0
        calla strike_check
        movi 0618h,a0
        move a0,*a13(p_action),w
        movk 4,a0
        jsrp mframew
        sleep 8
        movk 4,a0
        jsrp mframew
        calla delete_slave
        jauc reaction_exit

; Animation callback consumes the following single-image descriptor.
; Native parent p_slave owns its palette/object lifetime, including interruption.
ks_blade_fx_step
        move *a13(p_slave),a10,l
        jrne ks_blade_update
        push a8
        move *a9+,a5,l
        calla gso_dmawnz
        move a8,a10
        pull a8
        move a10,*a13(p_slave),l
        movi front_z+1,a0
        move a0,*a10(ozval),l
        push a10
        move a10,a0
        move a8,a1
        calla lineup_1pwm
        pull a10
        move a10,a0
        jauc insobj
ks_blade_update
        push a8
        move a10,a8
        calla frame_a9
        move a8,a10
        pull a8
        move a10,a0
        move a8,a1
        jauc lineup_1pwm

ks_blade_hurt
        movk 1,a0
        calla create_blood_proc
        tsound 044h
        movi airborn_hit_no_sound,a5
        movk 1,a6
        calla reaction_start_abc
        calla rsnd_wasted_voice
        movi act_reacting,a0
        move a0,*a13(p_action),w
        movi 023h,a9
        calla get_char_ani
        calla do_next_a9_frame
        movi 060000h,a0
        calla away_x_vel
        sleep 8
        movi 040000h,a0
        calla away_x_vel
        movk 4,a0
        jsrp mframew
        jauc reaction_exit

        .data
ks_blade_attack
        .word 109,20,75,67
        .word 01901h,01a03h
        .long 0
        .word sf_squeeze
