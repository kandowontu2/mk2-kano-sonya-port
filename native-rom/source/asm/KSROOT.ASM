; DEVELOPMENT roster roots. Missing-state markers are NOT move implementations.
        .ref ks_square_animation
        .ref ks_sonya_walk_forward
        .ref ks_sonya_walk_backward
        .ref ks_sonya_vertical_jump
        .ref ks_sonya_torso_ripped
        .ref ks_sonya_throw_phase0
        .ref ks_sonya_swipe_torso
        .ref ks_sonya_stance
        .ref ks_sonya_shredded
        .ref ks_sonya_projectile_release
        .ref ks_sonya_projectile_effect
        .ref ks_sonya_main_35
        .ref ks_sonya_main_34
        .ref ks_sonya_main_33
        .ref ks_sonya_main_32
        .ref ks_sonya_main_31
        .ref ks_sonya_main_30
        .ref ks_sonya_main_2f
        .ref ks_sonya_main_2e
        .ref ks_sonya_main_2d
        .ref ks_sonya_main_2c
        .ref ks_sonya_main_2b
        .ref ks_sonya_main_2a
        .ref ks_sonya_main_29
        .ref ks_sonya_main_28
        .ref ks_sonya_main_23
        .ref ks_sonya_main_22
        .ref ks_sonya_main_21
        .ref ks_sonya_main_20
        .ref ks_sonya_main_1f
        .ref ks_sonya_main_1e
        .ref ks_sonya_main_1d
        .ref ks_sonya_main_1c
        .ref ks_sonya_main_1b
        .ref ks_sonya_main_1a
        .ref ks_sonya_main_19
        .ref ks_sonya_main_18
        .ref ks_sonya_main_17
        .ref ks_sonya_main_16
        .ref ks_sonya_main_15
        .ref ks_sonya_main_14
        .ref ks_sonya_main_13
        .ref ks_sonya_main_12
        .ref ks_sonya_main_11
        .ref ks_sonya_main_10
        .ref ks_sonya_main_0f
        .ref ks_sonya_main_0e
        .ref ks_sonya_main_0d
        .ref ks_sonya_main_0c
        .ref ks_sonya_main_0b
        .ref ks_sonya_main_0a
        .ref ks_sonya_main_09
        .ref ks_sonya_main_04
        .ref ks_sonya_main_02
        .ref ks_sonya_kintaro_thrown
        .ref ks_sonya_impaled
        .ref ks_sonya_head
        .ref ks_sonya_forward_flip
        .ref ks_sonya_drain_reaction
        .ref ks_sonya_decapfall
        .ref ks_sonya_crouch
        .ref ks_sonya_bike_victim
        .ref ks_sonya_banged
        .ref ks_sonya_backward_flip
        .ref ks_sonya_back_broke
        .ref ks_ring_impact
        .ref ks_leg_intro
        .ref ks_laser_phase0
        .ref ks_knife_impact
        .ref ks_kano_walk_forward
        .ref ks_kano_walk_backward
        .ref ks_kano_vertical_jump
        .ref ks_kano_torso_ripped
        .ref ks_kano_throw_phase0
        .ref ks_kano_swipe_torso
        .ref ks_kano_stance
        .ref ks_kano_shredded
        .ref ks_kano_projectile_release
        .ref ks_kano_projectile_effect
        .ref ks_kano_nutcrunched
        .ref ks_kano_main_35
        .ref ks_kano_main_34
        .ref ks_kano_main_33
        .ref ks_kano_main_32
        .ref ks_kano_main_31
        .ref ks_kano_main_30
        .ref ks_kano_main_2f
        .ref ks_kano_main_2e
        .ref ks_kano_main_2d
        .ref ks_kano_main_2c
        .ref ks_kano_main_2b
        .ref ks_kano_main_2a
        .ref ks_kano_main_29
        .ref ks_kano_main_28
        .ref ks_kano_main_23
        .ref ks_kano_main_22
        .ref ks_kano_main_21
        .ref ks_kano_main_20
        .ref ks_kano_main_1f
        .ref ks_kano_main_1e
        .ref ks_kano_main_1d
        .ref ks_kano_main_1c
        .ref ks_kano_main_1b
        .ref ks_kano_main_1a
        .ref ks_kano_main_19
        .ref ks_kano_main_18
        .ref ks_kano_main_17
        .ref ks_kano_main_16
        .ref ks_kano_main_15
        .ref ks_kano_main_14
        .ref ks_kano_main_13
        .ref ks_kano_main_12
        .ref ks_kano_main_11
        .ref ks_kano_main_10
        .ref ks_kano_main_0f
        .ref ks_kano_main_0e
        .ref ks_kano_main_0d
        .ref ks_kano_main_0c
        .ref ks_kano_main_0b
        .ref ks_kano_main_0a
        .ref ks_kano_main_09
        .ref ks_kano_main_04
        .ref ks_kano_main_02
        .ref ks_kano_kintaro_thrown
        .ref ks_kano_impaled
        .ref ks_kano_head
        .ref ks_kano_forward_flip
        .ref ks_kano_drain_reaction
        .ref ks_kano_decapfall
        .ref ks_kano_crouch
        .ref ks_kano_bike_victim
        .ref ks_kano_banged
        .ref ks_kano_backward_flip
        .ref ks_kano_back_broke
        .ref ks_friend_sonya_intro
        .ref ks_friend_kano_body
        .ref ks_finish_sonya_kiss
        .ref ks_extract_intro
        .ref ks_choke_intro
        .ref ks_blade_animation
        .ref ks_bike_intro
        .ref ks_ball_animation
        .include dispequ.asm
        .include sysequ.asm
        .include mainequ.asm
        .def ks_missing_animation_count,ks_missing_animation_tag,ks_missing_animation_actor
        .bss ks_missing_animation_count,32
        .bss ks_missing_animation_tag,16
        .bss ks_missing_animation_actor,16
        .data
        .def ks_kano_anitab1,ks_kano_anitab2
ks_kano_anitab1
        .long ks_kano_stance ; main 00
        .long ks_kano_walk_forward ; main 01
        .long ks_kano_main_02 ; main 02
        .long ks_kano_walk_backward ; main 03
        .long ks_kano_main_04 ; main 04
        .long ks_kano_crouch ; main 05
        .long ks_kano_vertical_jump ; main 06
        .long ks_kano_forward_flip ; main 07
        .long ks_kano_backward_flip ; main 08
        .long ks_kano_main_09 ; main 09
        .long ks_kano_main_0a ; main 0a
        .long ks_kano_main_0b ; main 0b
        .long ks_kano_main_0c ; main 0c
        .long ks_kano_main_0d ; main 0d
        .long ks_kano_main_0e ; main 0e
        .long ks_kano_main_0f ; main 0f
        .long ks_kano_main_10 ; main 10
        .long ks_kano_main_11 ; main 11
        .long ks_kano_main_12 ; main 12
        .long ks_kano_main_13 ; main 13
        .long ks_kano_main_14 ; main 14
        .long ks_kano_main_15 ; main 15
        .long ks_kano_main_16 ; main 16
        .long ks_kano_main_17 ; main 17
        .long ks_kano_main_18 ; main 18
        .long ks_kano_main_19 ; main 19
        .long ks_kano_main_1a ; main 1a
        .long ks_kano_main_1b ; main 1b
        .long ks_kano_main_1c ; main 1c
        .long ks_kano_main_1d ; main 1d
        .long ks_kano_main_1e ; main 1e
        .long ks_kano_main_1f ; main 1f
        .long ks_kano_main_20 ; main 20
        .long ks_kano_main_21 ; main 21
        .long ks_kano_main_22 ; main 22
        .long ks_kano_main_23 ; main 23
        .long ks_kano_throw_phase0 ; main 24
        .long ks_kano_shredded ; main 25
        .long ks_kano_projectile_release ; main 26
        .long ks_kano_projectile_effect ; main 27
        .long ks_kano_main_28 ; main 28
        .long ks_kano_main_29 ; main 29
        .long ks_kano_main_2a ; main 2a
        .long ks_kano_main_2b ; main 2b
        .long ks_kano_main_2c ; main 2c
        .long ks_kano_main_2d ; main 2d
        .long ks_kano_main_2e ; main 2e
        .long ks_kano_main_2f ; main 2f
        .long ks_kano_main_30 ; main 30
        .long ks_kano_main_31 ; main 31
        .long ks_kano_main_32 ; main 32
        .long ks_kano_main_33 ; main 33
        .long ks_kano_main_34 ; main 34
        .long ks_kano_main_35 ; main 35
        .long ks_kano_nutcrunched ; main 36
        .long ks_kano_bike_victim ; main 37
        .long ks_kano_drain_reaction ; main 38
        .long ks_kano_torso_ripped ; main 39
        .long ks_kano_banged ; main 3a
        .long ks_kano_impaled ; main 3b
        .long ks_kano_decapfall ; main 3c
        .long ks_kano_head ; main 3d
        .long ks_kano_kintaro_thrown ; main 3e
        .long ks_kano_back_broke ; main 3f
        .long ks_kano_stance ; main 40
        .long ks_kano_swipe_torso ; main 41
ks_kano_anitab2
        .long ks_ball_animation ; own special 00: travelling_special
        .long ks_blade_animation ; own special 01: strike_special
        .long ks_choke_intro ; own special 02: grab_special
        .long ks_extract_intro ; own special 03: fatality_one
        .long ks_laser_phase0 ; own special 04: fatality_two
        .long ks_friend_kano_body ; own special 05: friendship_intro
        .long ks_knife_impact ; own special 06: projectile_impact
        .def ks_sonya_anitab1,ks_sonya_anitab2
ks_sonya_anitab1
        .long ks_sonya_stance ; main 00
        .long ks_sonya_walk_forward ; main 01
        .long ks_sonya_main_02 ; main 02
        .long ks_sonya_walk_backward ; main 03
        .long ks_sonya_main_04 ; main 04
        .long ks_sonya_crouch ; main 05
        .long ks_sonya_vertical_jump ; main 06
        .long ks_sonya_forward_flip ; main 07
        .long ks_sonya_backward_flip ; main 08
        .long ks_sonya_main_09 ; main 09
        .long ks_sonya_main_0a ; main 0a
        .long ks_sonya_main_0b ; main 0b
        .long ks_sonya_main_0c ; main 0c
        .long ks_sonya_main_0d ; main 0d
        .long ks_sonya_main_0e ; main 0e
        .long ks_sonya_main_0f ; main 0f
        .long ks_sonya_main_10 ; main 10
        .long ks_sonya_main_11 ; main 11
        .long ks_sonya_main_12 ; main 12
        .long ks_sonya_main_13 ; main 13
        .long ks_sonya_main_14 ; main 14
        .long ks_sonya_main_15 ; main 15
        .long ks_sonya_main_16 ; main 16
        .long ks_sonya_main_17 ; main 17
        .long ks_sonya_main_18 ; main 18
        .long ks_sonya_main_19 ; main 19
        .long ks_sonya_main_1a ; main 1a
        .long ks_sonya_main_1b ; main 1b
        .long ks_sonya_main_1c ; main 1c
        .long ks_sonya_main_1d ; main 1d
        .long ks_sonya_main_1e ; main 1e
        .long ks_sonya_main_1f ; main 1f
        .long ks_sonya_main_20 ; main 20
        .long ks_sonya_main_21 ; main 21
        .long ks_sonya_main_22 ; main 22
        .long ks_sonya_main_23 ; main 23
        .long ks_sonya_throw_phase0 ; main 24
        .long ks_sonya_shredded ; main 25
        .long ks_sonya_projectile_release ; main 26
        .long ks_sonya_projectile_effect ; main 27
        .long ks_sonya_main_28 ; main 28
        .long ks_sonya_main_29 ; main 29
        .long ks_sonya_main_2a ; main 2a
        .long ks_sonya_main_2b ; main 2b
        .long ks_sonya_main_2c ; main 2c
        .long ks_sonya_main_2d ; main 2d
        .long ks_sonya_main_2e ; main 2e
        .long ks_sonya_main_2f ; main 2f
        .long ks_sonya_main_30 ; main 30
        .long ks_sonya_main_31 ; main 31
        .long ks_sonya_main_32 ; main 32
        .long ks_sonya_main_33 ; main 33
        .long ks_sonya_main_34 ; main 34
        .long ks_sonya_main_35 ; main 35
        .long ks_sonya_bike_victim ; main 36
        .long ks_sonya_bike_victim ; main 37
        .long ks_sonya_drain_reaction ; main 38
        .long ks_sonya_torso_ripped ; main 39
        .long ks_sonya_banged ; main 3a
        .long ks_sonya_impaled ; main 3b
        .long ks_sonya_decapfall ; main 3c
        .long ks_sonya_head ; main 3d
        .long ks_sonya_kintaro_thrown ; main 3e
        .long ks_sonya_back_broke ; main 3f
        .long ks_sonya_stance ; main 40
        .long ks_sonya_swipe_torso ; main 41
ks_sonya_anitab2
        .long ks_square_animation ; own special 00: travelling_special
        .long ks_bike_intro ; own special 01: strike_special
        .long ks_leg_intro ; own special 02: grab_special
        .long ks_finish_sonya_kiss ; own special 03: fatality_one
        .long ks_finish_sonya_kiss ; own special 04: fatality_two
        .long ks_friend_sonya_intro ; own special 05: friendship_intro
        .long ks_ring_impact ; own special 06: projectile_impact
        .text
ks_missing_animation_mark
        move a0,@ks_missing_animation_tag,w
        move *a8(ochar),a0,w
        move a0,@ks_missing_animation_actor,w
        move @ks_missing_animation_count,a0,l
        addk 1,a0
        move a0,@ks_missing_animation_count,l
        rets
