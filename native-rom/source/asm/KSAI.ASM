; Own native CPU choices. No switch-history fabrication or character proxy.
        .file "KSAI.ASM"
        .include dispequ.asm
        .include sysequ.asm
        .include macros.hdr
        .include mainequ.asm
        .def ks_ai_kano_special,ks_ai_sonya_special
        .def ks_ai_kano_projectile,ks_ai_sonya_projectile
        .def ks_ai_kano_propell,ks_ai_sonya_air
        .ref ks_kano_ball,ks_kano_blade,ks_kano_choke,ks_kano_knife
        .ref ks_sonya_square,ks_sonya_bike,ks_sonya_leg,ks_sonya_ring
        .ref reset_proc_stack,get_x_dist,is_he_airborn,face_opponent
        .ref reaction_exit,existp
        .text

ks_ai_kano_special
        calla reset_proc_stack
        calla face_opponent
        calla get_x_dist
        cmpi 060h,a3
        jrhi ks_ai_kano_far
        move *a13(p_otherguy),a0,l
        move *a0(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_ai_blade
        cmpi ft_final_boss,a0
        jreq ks_ai_blade
        move @rand,a0,l
        jrn ks_ai_blade
        jauc ks_kano_choke
ks_ai_blade
        jauc ks_kano_blade
ks_ai_kano_far
        move @rand,a0,l
        jrn ks_ai_kano_projectile
ks_ai_kano_propell
        calla reset_proc_stack
        calla face_opponent
        jauc ks_kano_ball

ks_ai_sonya_special
        calla reset_proc_stack
        calla face_opponent
        calla is_he_airborn
        jrc ks_ai_sonya_air
        move *a13(p_otherguy),a0,l
        move *a0(ochar),a0,w
        cmpi ft_goro,a0
        jreq ks_ai_sonya_projectile
        cmpi ft_final_boss,a0
        jreq ks_ai_sonya_projectile
        calla get_x_dist
        cmpi 050h,a3
        jrhi ks_ai_sonya_mid
        jauc ks_sonya_leg
ks_ai_sonya_mid
        cmpi 070h,a3
        jrhi ks_ai_sonya_projectile
        jauc ks_sonya_bike
ks_ai_sonya_air
        calla reset_proc_stack
        calla face_opponent
        calla is_he_airborn
        jrnc ks_ai_sonya_projectile
        calla get_x_dist
        cmpi 0100h,a3
        jrhi ks_ai_sonya_projectile
        jauc ks_sonya_square

; Match the human route's one-live-projectile-per-owner predicate.
ks_ai_projectile_free
        movi pid_proj1,a0
        move *a8(oid),a1,w
        cmpi oid_p1,a1
        jreq ks_ai_projectile_pid
        movi pid_proj2,a0
ks_ai_projectile_pid
        movi -1,a1
        calla existp
        move a0,a0
        rets
ks_ai_kano_projectile
        calla reset_proc_stack
        calla face_opponent
        callr ks_ai_projectile_free
        jrne ks_ai_no_projectile
        jauc ks_kano_knife
ks_ai_sonya_projectile
        calla reset_proc_stack
        calla face_opponent
        callr ks_ai_projectile_free
        jrne ks_ai_no_projectile
        jauc ks_sonya_ring
ks_ai_no_projectile
        jauc reaction_exit
