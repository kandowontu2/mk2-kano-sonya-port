; Own ROM-side projectile actions. Shared native allocator/process/collision lifetime.
        .file "KSPROJ.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_kano_knife,ks_sonya_ring
        .ref ks_knife_release,ks_knife_intro,ks_knife_flight,ks_knife_impact
        .ref ks_ring_charge,ks_ring_release,ks_ring_flight,ks_ring_impact
        .ref ks_knife_palette,ks_ring_palette,ks_ring_charge_palette
        .ref delete_proj_and_die,dead_projectile,proj_strike_check,tell_world_stk
        .text

ks_kano_knife
        movi 0211h,a1
        calla init_special_act
        movi 026h,a9
        calla get_char_ani
        calla do_next_a9_frame
        sleep 3
        push a9
        movi 027h,a9
        calla get_char_ani
        movi ks_knife_palette,a11
        movi ks_knife_child,a7
        callr ks_make_projectile
        pull a9
        movk 3,a0
        jsrp mframew
        sleep 1
        movi act_proj_sd,a0
        move a0,*a13(p_action),w
        sleep 24
        jauc reaction_exit

ks_sonya_ring
        movi 0212h,a1
        calla init_special_act
        movi 026h,a9
        calla get_char_ani
        movk 3,a0
        jsrp mframew
        movi 027h,a9
        calla get_char_ani
        movi ks_ring_palette,a11
        movi ks_ring_child,a7
        callr ks_make_projectile
        movi act_proj_sd,a0
        move a0,*a13(p_action),w
        sleep 35
        jauc reaction_exit

; No yield between object allocation, palette selection and insertion.
; A8 stays the true physical thrower until spawn_proj_proc transfers ownership.
ks_make_projectile
        mmtm sp,a7,a11
        calla get_proj_obj_m
        mmfm sp,a7,a11
        mmtm sp,a7,a8,a10
        move a10,a8
        move a11,a0
        calla swpal
        mmfm sp,a7,a8,a10
        push a7
        move a10,a0
        calla insobj
        pull a7
        calla spawn_proj_proc
        rets

ks_knife_child
        movi ks_knife_intro,a9
        movk 3,a0
        jsrp mframew
        movi 19,a0
        calla tell_world_stk
        movi 19,a0
        calla proj_strike_check
        jrc ks_knife_hit
        movi 080000h,a0
        calla set_proj_vel
        sleep 1
; Imported frames retain their original pivot: unlike the old converter,
; no -100/-72 frame rewrite exists. The raw flight origin is +88,+32.
        movi 80,a0
        movi 32,a1
        calla multi_adjust_xy
        movi ks_knife_flight,a9
        movk 1,a0
        calla init_anirate
ks_knife_travel
        calla next_anirate
        movi 19,a0
        calla tell_world_stk
        movi 19,a0
        calla proj_strike_check
        jrc ks_knife_hit
        sleep 1
        calla proj_onscreen_test
        jrc ks_knife_travel
        jauc delete_proj_and_die
ks_knife_hit
        calla dead_projectile
        calla stop_a8
        movk 6,a9
        calla get_char_ani2
        movk 3,a0
        jsrp mframew
        jauc delete_proj_and_die

ks_ring_child
; Actual release-origin hit core, not the travelling core stretched backward.
        movi 23,a0
        calla tell_world_stk
        movi 23,a0
        calla proj_strike_check
        jrc ks_ring_hit
        movi 080000h,a0
        calla set_proj_vel
        sleep 1
        movi ks_ring_flight,a9
        movk 3,a0
        calla init_anirate
ks_ring_travel
        calla next_anirate
        movi 19,a0
        calla tell_world_stk
        movi 19,a0
        calla proj_strike_check
        jrc ks_ring_hit
        sleep 1
        calla proj_onscreen_test
        jrc ks_ring_travel
        jauc delete_proj_and_die
ks_ring_hit
        calla dead_projectile
        calla stop_a8
        movk 6,a9
        calla get_char_ani2
        movk 3,a0
        jsrp mframew
        jauc delete_proj_and_die
