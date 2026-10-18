; Shared native paired-pose stepping and live paired-victim boundary exception.
        .file "KSPAIR.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_pair_pose,ks_pair_mframew,ks_pair_boundary
        .text

; A9 = owner phase; p_store2 = victim record index; p_store3 = XY/pose records.
ks_pair_mframew
        move a0,-*a12,l
ks_pair_next
        calla do_next_a9_frame
        jreq ks_pair_done
        callr ks_pair_pose
        move *a12,a0,l
        calla prcslp
        jruc ks_pair_next
ks_pair_done
        pullp a0
        retp

ks_pair_pose
        mmtm sp,a8,a9,a10,a11
        movk 4,a0
        move a0,@f_norepell,w
        calla match_him_with_me_f
        move *a13(p_store2),a0,w
        sll 6,a0
        move *a13(p_store3),a2,l
        add a0,a2
        move *a2+,a0,w
        move *a2+,a1,w
        move *a2,a11,l
        move *a13(p_otherguy),a8,l
        calla multi_adjust_xy
        move a11,a0
        jrne ks_pair_own_pose
; Choke's original-roster records explicitly select this actor's high-hit pose 2.
; Added actors and all Leg Grab records always have named own composites.
        movi 010h,a9
        calla get_char_ani
        addi 32,a9
        move *a9,a0,l
ks_pair_own_pose
        calla ani2
        mmfm sp,a8,a9,a10,a11
        move *a13(p_store2),a0,w
        inc a0
        move a0,*a13(p_store2),w
        rets

; Display-side native boundary input A2 is a physical fighter object.
; Skip only X clamping while both actual owner/victim states and links agree.
; The original gravity path still runs; release/interruption restores bounds.
ks_pair_boundary
        mmtm sp,a0,a1,a3,a4,a5
        move @p1_obj,a3,l
        cmp a2,a3
        jrne ks_bound_p2
        move @p1_proc,a3,l
        jruc ks_bound_process
ks_bound_p2
        move @p2_obj,a3,l
        cmp a2,a3
        jrne ks_bound_no
        move @p2_proc,a3,l
ks_bound_process
        move a3,a3
        jreq ks_bound_no
        move *a3(p_action),a4,w
        cmpi 0226h,a4
        jreq ks_bound_throw
        cmpi 0224h,a4
        jreq ks_bound_laser
        cmpi 021bh,a4
        jreq ks_bound_leg
        cmpi 0215h,a4
        jreq ks_bound_bike
        cmpi 0218h,a4
        jrne ks_bound_no
        movi 0217h,a4
        movi 17,a5
        jruc ks_bound_owner
ks_bound_leg
        movi 021ah,a4
        movi 18,a5
        jruc ks_bound_owner
ks_bound_bike
        movi 0214h,a4
        movi 18,a5
        jruc ks_bound_owner
ks_bound_laser
        movi 0223h,a4
        movi 17,a5
        jruc ks_bound_owner
ks_bound_throw
        movi act_bodyslam,a4
        movi -1,a5
ks_bound_owner
        move *a3(p_otherproc),a0,l
        move a0,a0
        jreq ks_bound_no
        move *a0(p_action),a1,w
        cmp a4,a1
        jrne ks_bound_no
        move *a0(p_otherguy),a1,l
        cmp a2,a1
        jrne ks_bound_no
        move *a3(p_otherguy),a1,l
        move *a1(ochar),a1,w
        cmpi -1,a5
        jrne ks_bound_exact_id
        cmpi 17,a1
        jreq ks_bound_yes
        cmpi 18,a1
        jrne ks_bound_no
        jruc ks_bound_yes
ks_bound_exact_id
        cmp a5,a1
        jrne ks_bound_no
ks_bound_yes
        setc
        jruc ks_bound_return
ks_bound_no
        clrc
ks_bound_return
        mmfm sp,a0,a1,a3,a4,a5
        rets
