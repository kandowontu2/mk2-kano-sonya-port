; Native Sonya flame kiss: own performer, single-object orb and victim burn.
        .file "KSKISS.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_sonya_flame_kiss
        .ref ks_finish_sonya_kiss,ks_kiss_orb_frames,ks_kiss_orb_palette
        .ref ks_kiss_burn,ks_kiss_outro,ks_kiss_outro_counts
        .ref ks_finish_palette_ffccc130,disable_repell
        .text

ks_sonya_flame_kiss
        movk 1,a0
        movk 1,a1
        calla init_death_blow
        movi 021eh,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_repell
        movi ks_kiss_frozen,a7
        calla takeover_him
        movk 3,a9
        calla get_char_ani2
        movk 5,a0
        jsrp mframew
        callr ks_kiss_create
        tsound 0101h
        movi 060000h,a0
        movi -08000h,a1
        move *a8(oflags),a2,w
        btst b_fliph,a2
        jreq ks_kiss_velocity
        neg a0
        neg a1
ks_kiss_velocity
        move a0,*a13(p_store4),l
        move a1,*a13(p_store6),l
        clr a0
        move a0,*a13(p_store5),l
        move a0,*a13(p_store1),w
        movk 5,a0
        move a0,*a13(p_store2),w
ks_kiss_launch
        jsrp ks_kiss_tick
        callr ks_kiss_count
        jrne ks_kiss_launch
        movi -070000h,a0
        move a0,*a13(p_store5),l
ks_kiss_ascent
        jsrp ks_kiss_tick
        move *a13(p_store4),a0,l
        move *a13(p_store6),a1,l
        add a1,a0
        move a0,*a13(p_store4),l
        move *a13(p_store5),a0,l
        addi 04000h,a0
        move a0,*a13(p_store5),l
        jrn ks_kiss_ascent
        movi 10,a0
        move a0,*a13(p_store2),w
ks_kiss_turn
        jsrp ks_kiss_tick
        move *a13(p_store4),a0,l
        move *a13(p_store6),a1,l
        sub a1,a0
        move a0,*a13(p_store4),l
        move *a13(p_store5),a0,l
        addi 08000h,a0
        move a0,*a13(p_store5),l
        callr ks_kiss_count
        jrne ks_kiss_turn
; Signed fixed-point endpoint velocities: actual opponent X, stage floor - 88.
        move *a13(p_slave),a10,l
        move *a13(p_otherguy),a11,l
        move *a11(oxpos),a0,w
        move *a10(oxpos),a1,w
        sub a1,a0
        sll 16,a0
        sra 4,a0
        move a0,*a13(p_store4),l
        move @ground_y,a0,w
        subi 88,a0
        move *a10(oypos),a1,w
        sub a1,a0
        sll 16,a0
        sra 4,a0
        move a0,*a13(p_store5),l
        movi 16,a0
        move a0,*a13(p_store2),w
ks_kiss_home
        jsrp ks_kiss_tick
        callr ks_kiss_count
        jrne ks_kiss_home
; Let the final contact point reach the renderer before replacing the victim.
        sleep 1
        calla delete_slave
        tsound 0102h
        tsound 0103h
        push a8
        move *a13(p_otherguy),a8,l
        movi ks_finish_palette_ffccc130,a0
        calla swpal
        pull a8
        clr a0
        move a0,*a13(p_store8),w
        callr ks_kiss_burn_draw
; The first flash is only a torso. Grounding that frame moves the later full
; skeleton below the stage; retain the actual victim's standing origin instead.
        movi 18,a0
        move a0,*a13(p_store2),w
ks_kiss_burn_early
        jsrp ks_kiss_burn_step
        callr ks_kiss_count
        jrne ks_kiss_burn_early
        clr a0
        move a0,*a13(p_store7),w
ks_kiss_salute
        move *a13(p_store7),a0,w
        sll 5,a0
        addi ks_kiss_outro,a0
        move *a0,a0,l
        calla ani2
        move *a13(p_store7),a0,w
        sll 4,a0
        addi ks_kiss_outro_counts,a0
        move *a0,a0,w
        move a0,*a13(p_store2),w
ks_kiss_salute_fire
        jsrp ks_kiss_burn_step
        callr ks_kiss_count
        jrne ks_kiss_salute_fire
        move *a13(p_store7),a0,w
        inc a0
        move a0,*a13(p_store7),w
        cmpi 8,a0
        jrlt ks_kiss_salute
        calla death_blow_complete
        jauc wait_forever

ks_kiss_count
        move *a13(p_store2),a0,w
        dec a0
        move a0,*a13(p_store2),w
        rets

ks_kiss_create
        push a8
        move @ks_kiss_orb_frames,a5,l
        calla gso_dmawnz
        move a8,a10
        pull a8
        move a10,*a13(p_slave),l
        clr a0
        move a0,*a10(oxvel),l
        move a0,*a10(oyvel),l
        move a0,*a10(ograv),l
        move *a8(oxval),a0,l
        move *a8(oflags),a1,w
        btst b_fliph,a1
        jrne ks_kiss_create_left
        addi 01e0000h,a0
        jruc ks_kiss_create_x
ks_kiss_create_left
        subi 03c0000h,a0
ks_kiss_create_x
        move a0,*a10(oxval),l
        move *a8(oyval),a0,l
        addi 0180000h,a0
        move a0,*a10(oyval),l
        move *a10(oflags),a0,w
        andni m_fliph,a0
        andi m_fliph,a1
        or a1,a0
        move a0,*a10(oflags),w
        movi front_z+1,a0
        move a0,*a10(ozval),l
        movi 0713h,a0
        move a0,*a10(oid),w
        move a10,a0
        jauc insobj

ks_kiss_tick
        sleep 1
        move *a13(p_slave),a10,l
        move *a13(p_store4),a0,l
        move *a10(oxval),a1,l
        add a0,a1
        move a1,*a10(oxval),l
        move *a13(p_store5),a0,l
        move *a10(oyval),a1,l
        add a0,a1
        move a1,*a10(oyval),l
        move *a13(p_store1),a0,w
        inc a0
        move a0,*a13(p_store1),w
        cmpi 42,a0
        jrhi ks_kiss_home_frame
        movk 6,a1
        move a0,a3
        divu a1,a3
        move a3,a0
        jruc ks_kiss_draw_orb
ks_kiss_home_frame
        subi 43,a0
        movk 3,a1
        move a0,a3
        divu a1,a3
        move a3,a0
ks_kiss_draw_orb
        sll 5,a0
        addi ks_kiss_orb_frames,a0
        move *a0,a5,l
        move a5,*a10(oimg),l
        move a5,*a10(oshape),l
        move *a5(isag),*a10(osag),l
        move *a5(isize),*a10(osize),l
        move *a10(oflags),a1,w
        andi m_fliph,a1
        move *a5(icontrol),a0,w
        ori dmago|m_wrnonz,a0
        or a1,a0
        move a0,*a10(oflags),w
        retp

ks_kiss_burn_draw
        move *a13(p_store8),a0,w
        sll 5,a0
        addi ks_kiss_burn,a0
        move *a0,a0,l
        push a8
        move *a13(p_otherguy),a8,l
        calla ani2
        pull a8
        rets

ks_kiss_burn_step
        callr ks_kiss_burn_draw
        sleep 4
        move *a13(p_store8),a0,w
        inc a0
        move a0,*a13(p_store8),w
        retp

ks_kiss_frozen
        movi 021fh,a0
        move a0,*a13(p_action),w
        calla stop_me
        calla disable_all_buttons
        jauc wait_forever
