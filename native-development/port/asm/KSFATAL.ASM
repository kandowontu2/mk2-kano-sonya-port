; Native Kano skeleton extraction. No donor opcodes or emulator hooks.
        .file "KSFATAL.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_extract
        .ref ks_extract_intro,ks_extract_body,ks_extract_skeleton,ks_extract_victims
        .ref ks_extract_kano_victim_palette,ks_finish_palette_ffccbf20
        .ref get_proj_obj_m,disable_repell,change_to_bloody_pal
        .text

ks_kano_extract
        movk 1,a0
        movk 1,a1
        calla init_death_blow
        movi 021ch,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_repell
        movi ks_extract_frozen,a7
        calla takeover_him
        move *a13(p_otherguy),a10,l
        move *a10(ochar),a0,w
        sll 5,a0
        addi ks_extract_victims,a0
        move *a0,a0,l
        move a0,*a13(p_store3),l
        movk 3,a9
        calla get_char_ani2
        movk 6,a0
        jsrp mframew
        movk 4,a0
        callr ks_extract_draw_body
        clr a0
        callr ks_extract_draw_victim
        sleep 59
        callr ks_extract_victim_palette
        movi ks_extract_skeleton,a9
        calla get_proj_obj_m
; The raw extracted composite uses Kano's origin, not match_ani_points offsets.
        move *a8(oxval),*a10(oxval),l
        move *a8(oyval),*a10(oyval),l
        move *a10(oflags),a0,w
        andni m_fliph,a0
        move *a8(oflags),a1,w
        andi m_fliph,a1
        or a1,a0
        move a0,*a10(oflags),w
        push a8
        move a10,a8
        movi ks_finish_palette_ffccbf20,a0
        calla swpal
        calla insobja8
        pull a8
        calla rsnd_big_smack
        movi rsnd_death_voice,a0
        calla calla_for_him
        clr a0
        move a0,*a13(p_store1),w
ks_extract_pull
        move *a13(p_store1),a0,w
        cmpi 2,a0
        jrge ks_extract_arm
        inc a0
        callr ks_extract_draw_victim
ks_extract_arm
        move *a13(p_store1),a0,w
        sll 4,a0
        addi ks_extract_arm_phases,a0
        move *a0,a0,w
        callr ks_extract_draw_body
        push a8
        move *a13(p_slave),a8,l
        move *a13(p_store1),a0,w
        sll 5,a0
        addi ks_extract_skeleton,a0
        move *a0,a0,l
        calla ani2
        pull a8
        sleep 8
        move *a13(p_store1),a0,w
        inc a0
        move a0,*a13(p_store1),w
        cmpi 6,a0
        jrlt ks_extract_pull
        sleep 28
        movk 3,a0
        move a0,*a13(p_store1),w
ks_extract_collapse
        move *a13(p_store1),a0,w
        callr ks_extract_draw_victim
        sleep 8
        move *a13(p_store1),a0,w
        inc a0
        move a0,*a13(p_store1),w
        cmpi 6,a0
        jrlt ks_extract_collapse
        sleep 48
        calla death_blow_complete
        jauc wait_forever

ks_extract_draw_body
        sll 5,a0
        addi ks_extract_body,a0
        move *a0,a0,l
        jauc ani2

ks_extract_draw_victim
        push a8
        sll 5,a0
        move *a13(p_store3),a1,l
        add a1,a0
        move *a0,a0,l
        move *a13(p_otherguy),a8,l
        calla ani2
        pull a8
        rets

ks_extract_victim_palette
        push a8
        move *a13(p_otherguy),a8,l
        move *a8(ochar),a0,w
        cmpi 17,a0
        jreq ks_extract_kano_palette
        cmpi 12,a0
        jrge ks_extract_pal_done
        calla change_to_bloody_pal
        jruc ks_extract_pal_done
ks_extract_kano_palette
        movi ks_extract_kano_victim_palette,a0
        calla swpal
ks_extract_pal_done
        pull a8
        rets

ks_extract_frozen
        movi 021dh,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_all_buttons
        jauc wait_forever

        .data
ks_extract_arm_phases
        .word 5,6,6,7,8,8
