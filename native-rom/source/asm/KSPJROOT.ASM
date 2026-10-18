; Own native main26/main27 typed roots. No executable binary arrays.
        .include mainequ.asm
        .ref ks_knife_palette,ks_ring_palette,ks_ring_charge_palette
        .data
        .ref ks_kano_pose_ff82f400
        .ref ks_kano_pose_ff82f460
        .ref ks_kano_pose_ff82f4c0
        .ref ks_kano_pose_ff82f520
        .ref ks_kano_pose_ff82f580
        .ref ks_kano_pose_ff82f5e0
        .ref ks_kano_pose_ff82f640
        .ref ks_kano_pose_ff82f6a0
        .def ks_kano_projectile_release
ks_kano_projectile_release
        .long ks_kano_pose_ff82f400
        .long ks_kano_pose_ff82f460
        .long ks_kano_pose_ff82f4c0
        .long ks_kano_pose_ff82f520
        .long ks_kano_pose_ff82f580
        .long ks_kano_pose_ff82f5e0
        .long ks_kano_pose_ff82f640
        .long ks_kano_pose_ff82f6a0
        .long 0
        .def ks_pe_kano_0
ks_pe_kano_0
        .word 9,19,12,-107
        .long 006444980h
        .word 06000h
        .long ks_knife_palette
        .def ks_pe_kano_1
ks_pe_kano_1
        .word 7,8,-33,-102
        .long 006444d88h
        .word 06000h
        .long ks_knife_palette
        .def ks_pp_kano_0
ks_pp_kano_0
        .long ks_pe_kano_0,ks_pe_kano_1,0
        .def ks_pe_kano_2
ks_pe_kano_2
        .word 47,48,13,-75
        .long 006444ed8h
        .word 06a80h
        .long ks_knife_palette
        .def ks_pp_kano_1
ks_pp_kano_1
        .long ks_pe_kano_2,0
        .def ks_pe_kano_3
ks_pe_kano_3
        .word 23,45,0,-18
        .long 006446258h
        .word 06080h
        .long ks_knife_palette
        .def ks_pe_kano_4
ks_pe_kano_4
        .word 48,18,14,-100
        .long 006447598h
        .word 06a80h
        .long ks_knife_palette
        .def ks_pp_kano_2
ks_pp_kano_2
        .long ks_pe_kano_3,ks_pe_kano_4,0
        .def ks_pe_kano_5
ks_pe_kano_5
        .word 60,25,30,13
        .long 006447b38h
        .word 06480h
        .long ks_knife_palette
        .def ks_pe_kano_6
ks_pe_kano_6
        .word 9,8,16,-109
        .long 0064493c8h
        .word 06000h
        .long ks_knife_palette
        .def ks_pe_kano_7
ks_pe_kano_7
        .word 3,3,-32,-102
        .long 006449578h
        .word 06000h
        .long ks_knife_palette
        .def ks_pp_kano_3
ks_pp_kano_3
        .long ks_pe_kano_5,ks_pe_kano_6,ks_pe_kano_7,0
        .def ks_pe_kano_8
ks_pe_kano_8
        .word 8,32,32,-1
        .long 0064495b0h
        .word 06000h
        .long ks_knife_palette
        .def ks_pe_kano_9
ks_pe_kano_9
        .word 13,27,-15,-3
        .long 006449bb0h
        .word 06080h
        .long ks_knife_palette
        .def ks_pp_kano_4
ks_pp_kano_4
        .long ks_pe_kano_8,ks_pe_kano_9,0
        .def ks_pe_kano_10
ks_pe_kano_10
        .word 6,5,13,-109
        .long 00644a2e0h
        .word 06000h
        .long ks_knife_palette
        .def ks_pe_kano_11
ks_pe_kano_11
        .word 56,33,-50,-7
        .long 00644a398h
        .word 06580h
        .long ks_knife_palette
        .def ks_pp_kano_5
ks_pp_kano_5
        .long ks_pe_kano_10,ks_pe_kano_11,0
        .def ks_pe_kano_12
ks_pe_kano_12
        .word 34,40,7,28
        .long 00644bd88h
        .word 06480h
        .long ks_knife_palette
        .def ks_pp_kano_6
ks_pp_kano_6
        .long ks_pe_kano_12,0
        .def ks_pe_kano_13
ks_pe_kano_13
        .word 45,26,10,21
        .long 00644ce30h
        .word 06580h
        .long ks_knife_palette
        .def ks_pp_kano_7
ks_pp_kano_7
        .long ks_pe_kano_13,0
        .def ks_pe_kano_14
ks_pe_kano_14
        .word 43,23,11,4
        .long 00644dd50h
        .word 06180h
        .long ks_knife_palette
        .def ks_pp_kano_8
ks_pp_kano_8
        .long ks_pe_kano_14,0
        .def ks_pe_kano_15
ks_pe_kano_15
        .word 35,41,9,9
        .long 00644eb80h
        .word 06580h
        .long ks_knife_palette
        .def ks_pp_kano_9
ks_pp_kano_9
        .long ks_pe_kano_15,0
        .def ks_pe_kano_16
ks_pe_kano_16
        .word 24,46,10,12
        .long 00644fc30h
        .word 06080h
        .long ks_knife_palette
        .def ks_pp_kano_10
ks_pp_kano_10
        .long ks_pe_kano_16,0
        .def ks_pe_kano_17
ks_pe_kano_17
        .word 34,40,27,10
        .long 006450cd0h
        .word 06180h
        .long ks_knife_palette
        .def ks_pp_kano_11
ks_pp_kano_11
        .long ks_pe_kano_17,0
        .def ks_pe_kano_18
ks_pe_kano_18
        .word 46,26,35,5
        .long 006451da0h
        .word 06580h
        .long ks_knife_palette
        .def ks_pp_kano_12
ks_pp_kano_12
        .long ks_pe_kano_18,0
        .def ks_pe_kano_19
ks_pe_kano_19
        .word 43,25,32,20
        .long 006452cf0h
        .word 06480h
        .long ks_knife_palette
        .def ks_pp_kano_13
ks_pp_kano_13
        .long ks_pe_kano_19,0
        .def ks_pe_kano_20
ks_pe_kano_20
        .word 34,41,26,32
        .long 006453bc0h
        .word 06180h
        .long ks_knife_palette
        .def ks_pp_kano_14
ks_pp_kano_14
        .long ks_pe_kano_20,0
        .def ks_pe_kano_21
ks_pe_kano_21
        .word 24,45,13,33
        .long 006454c08h
        .word 06080h
        .long ks_knife_palette
        .def ks_pp_kano_15
ks_pp_kano_15
        .long ks_pe_kano_21,0
        .def ks_kano_projectile_effect
ks_kano_projectile_effect
        .long ks_pp_kano_0
        .long ks_pp_kano_1
        .long ks_pp_kano_2
        .long ks_pp_kano_3
        .long ks_pp_kano_4
        .long ks_pp_kano_5
        .long 0
        .long ks_pp_kano_6
        .long ks_pp_kano_7
        .long ks_pp_kano_8
        .long ks_pp_kano_9
        .long ks_pp_kano_10
        .long ks_pp_kano_11
        .long ks_pp_kano_12
        .long ks_pp_kano_13
        .long ks_pp_kano_14
        .long ks_pp_kano_15
        .long 0
        .ref ks_sonya_pose_ff83dbe0
        .ref ks_sonya_pose_ff83dc40
        .ref ks_sonya_pose_ff83dca0
        .ref ks_sonya_pose_ff83dd00
        .ref ks_sonya_pose_ff83dec0
        .def ks_sonya_projectile_release
ks_sonya_projectile_release
        .long ani_calla,ks_ring_root_palette_on
        .long ks_sonya_pose_ff83dbe0
        .long ks_sonya_pose_ff83dc40
        .long ks_sonya_pose_ff83dca0
        .long ks_sonya_pose_ff83dd00
        .long ani_calla,player_normpal
        .long ks_sonya_pose_ff83dec0
        .long 0
        .def ks_pe_sonya_0
ks_pe_sonya_0
        .word 35,29,-73,-35
        .long 0068b4a38h
        .word 06080h
        .long ks_ring_palette
        .def ks_pp_sonya_0
ks_pp_sonya_0
        .long ks_pe_sonya_0,0
        .def ks_pe_sonya_1
ks_pe_sonya_1
        .word 36,29,-73,-35
        .long 0068b5d68h
        .word 06180h
        .long ks_ring_palette
        .def ks_pp_sonya_1
ks_pp_sonya_1
        .long ks_pe_sonya_1,0
        .def ks_pe_sonya_2
ks_pe_sonya_2
        .word 37,29,-72,-35
        .long 0068b7348h
        .word 06080h
        .long ks_ring_palette
        .def ks_pp_sonya_2
ks_pp_sonya_2
        .long ks_pe_sonya_2,0
        .def ks_pe_sonya_3
ks_pe_sonya_3
        .word 36,29,-73,-35
        .long 0068b8b78h
        .word 06480h
        .long ks_ring_palette
        .def ks_pp_sonya_3
ks_pp_sonya_3
        .long ks_pe_sonya_3,0
        .def ks_sonya_projectile_effect
ks_sonya_projectile_effect
        .long ks_pp_sonya_0
        .long ks_pp_sonya_1
        .long ks_pp_sonya_2
        .long ks_pp_sonya_3
        .long 0
        .long ks_pp_sonya_0
        .long ks_pp_sonya_1
        .long ks_pp_sonya_2
        .long ks_pp_sonya_3
        .long 0
        .text
ks_ring_root_palette_on
        movi ks_ring_charge_palette,a0
        jauc player_swpal
