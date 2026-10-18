; Distinct native Sonya Death Orb: growth, travel, enclosure, burst and cleanup.
        .file "KSBUBBLE.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_sonya_bubble
        .ref ks_finish_sonya_kiss,ks_bubble_intro,ks_bubble_loop,ks_bubble_burst
        .ref ks_bubble_palette,ks_kiss_outro,get_proj_obj_m,disable_repell,kmo_proc
        .ref illegal_opcode
        .ref explode,exp_burst,bone_land,white_flash
        .text

ks_sonya_bubble
        movk 1,a0
        movk 2,a1
        calla init_death_blow
        movi 0220h,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_repell
        movk 4,a9
        calla get_char_ani2
        movk 3,a0
        jsrp mframew
        movi ks_bubble_intro,a9
        calla get_proj_obj_m
        movi -32,a0
        movi -16,a1
        move a10,a5
        calla adjust_xy_a5
        push a8
        move *a13(p_slave),a8,l
        movi ks_bubble_palette,a0
        calla swpal
        clr a0
        move a0,*a8(oxvel),l
        move a0,*a8(oyvel),l
; Multipart oslink is the dummy-process link (aliased with single-object
; gravity). Preserve it so kmo_proc can retire that process with the object.
        calla insobja8
        pull a8
        tsound 060h
        movi ks_bubble_intro,a0
        move a0,*a13(p_store3),l
        clr a0
        move a0,*a13(p_store1),w
ks_bubble_grow
        callr ks_bubble_draw
        sleep 3
        move *a13(p_store1),a0,w
        inc a0
        move a0,*a13(p_store1),w
        cmpi 7,a0
        jrlt ks_bubble_grow
        clr a0
        move a0,*a13(p_store1),w
        move a0,*a13(p_store2),w
        movi ks_bubble_loop,a0
        move a0,*a13(p_store3),l
        callr ks_bubble_draw
ks_bubble_travel
        jsrp ks_bubble_tick
        move *a13(p_slave),a10,l
        move *a13(p_otherguy),a11,l
        move *a10(oxpos),a0,w
        move *a11(oxpos),a1,w
        sub a1,a0
        abs a0
        cmpi 177,a0
        jrls ks_bubble_contact
        move *a13(p_store2),a0,w
        cmpi 256,a0
        jrlt ks_bubble_travel
; Finite visible-stage range should always contact before this bound.
        jauc illegal_opcode

ks_bubble_contact
; Use the native animation-point alignment and facing-aware raw pivot.
        push a8
        move *a13(p_slave),a0,l
        move *a13(p_otherguy),a8,l
        calla match_ani_points
        pull a8
        push a8
        move *a13(p_slave),a8,l
        movi -177,a0
        clr a1
        calla multi_adjust_xy
        pull a8
        movi ks_bubble_stumble,a7
        calla takeover_him
        movi 13,a0
        move a0,*a13(p_store4),w
        clr a0
        move a0,*a13(p_store1),w
ks_bubble_enclose
        callr ks_bubble_draw
        sleep 3
        callr ks_bubble_next_loop
        move *a13(p_store4),a0,w
        dec a0
        move a0,*a13(p_store4),w
        jrne ks_bubble_enclose
; Spawn native gore on the actual victim without the stock kiss routine's
; global off-screen deleter, which cannot classify our multipart raw pivot.
        movi ks_bubble_victim_pop,a7
        calla xfer_otherguy
        movi ks_bubble_burst,a0
        move a0,*a13(p_store3),l
        clr a0
        move a0,*a13(p_store1),w
ks_bubble_pop
        callr ks_bubble_draw
        sleep 4
        move *a13(p_store1),a0,w
        inc a0
        move a0,*a13(p_store1),w
        cmpi 3,a0
        jrlt ks_bubble_pop
; Retire both the multipart object/palette and its native dummy process.
        move *a13(p_slave),a2,l
        calla kmo_proc
        clr a0
        move a0,*a13(p_slave),l
        move a0,*a13(p_store1),w
ks_bubble_salute
        move *a13(p_store1),a0,w
        sll 5,a0
        addi ks_kiss_outro,a0
        move *a0,a0,l
        calla ani2
        sleep 4
        move *a13(p_store1),a0,w
        inc a0
        move a0,*a13(p_store1),w
        cmpi 8,a0
        jrlt ks_bubble_salute
        calla death_blow_complete
        jauc wait_forever

ks_bubble_tick
        sleep 1
        move *a13(p_slave),a10,l
        movi 020000h,a0
        move *a10(oflags),a1,w
        btst b_fliph,a1
        jreq ks_bubble_tick_right
        neg a0
ks_bubble_tick_right
        move *a10(oxval),a1,l
        add a0,a1
        move a1,*a10(oxval),l
        move *a13(p_store2),a0,w
        inc a0
        move a0,*a13(p_store2),w
        move a0,a1
        movk 3,a0
        modu a0,a1
        jrne ks_bubble_tick_draw
        callr ks_bubble_next_loop
ks_bubble_tick_draw
        callr ks_bubble_draw
        retp

ks_bubble_next_loop
        move *a13(p_store1),a0,w
        inc a0
        andi 3,a0
        move a0,*a13(p_store1),w
        rets

ks_bubble_draw
        move *a13(p_store1),a0,w
        sll 5,a0
        move *a13(p_store3),a1,l
        add a1,a0
        move *a0,a0,l
        push a8
        move *a13(p_slave),a8,l
        calla ani2
        pull a8
        rets

ks_bubble_stumble
        movi 0221h,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_all_buttons
        movi 023h,a9
        calla get_char_ani
        movk 4,a0
        jsrp mframew
        jauc wait_forever

ks_bubble_victim_pop
        movi 0222h,a0
        move a0,*a13(p_action),w
        tsound 0a4h
        jsrp white_flash
        move a8,a0
        calla set_inviso
        move a8,a11
        movi exp_burst,a6
        movi 04000h,a10
        movi bone_land,a0
        calla explode
        movi 000080008h,a11
        calla shake_a11
        jauc wait_forever
