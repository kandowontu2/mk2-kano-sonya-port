; Own blade scripts; compressed graphics already reside in native ROM sockets.
        .include mainequ.asm
        .ref ks_blade_fx_step,ks_knife_palette
        .ref ks_kano_pose_ff82fc40
        .ref ks_kano_pose_ff82fca0
        .ref ks_kano_pose_ff82fd00
        .ref ks_kano_pose_ff82fd60
        .ref ks_kano_pose_ff82fdc0
        .ref ks_kano_pose_ff82fe20
        .ref ks_kano_pose_ff82fe80
        .ref ks_kano_pose_ff82fee0
        .ref ks_kano_pose_ff82ff40
        .ref ks_kano_pose_ff82ffa0
        .def ks_blade_animation
        .data
ks_blade_animation
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_0
        .long ks_kano_pose_ff82fc40
        .long ani_adjustx
        .word 8
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_1
        .long ks_kano_pose_ff82fca0
        .long ani_adjustx
        .word 8
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_2
        .long ks_kano_pose_ff82fd00
        .long ani_adjustx
        .word 8
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_3
        .long ks_kano_pose_ff82fd60
        .long ani_adjustx
        .word 11
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_4
        .long ks_kano_pose_ff82fdc0
        .long 0
        .long ani_adjustx
        .word 11
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_5
        .long ks_kano_pose_ff82fe20
        .long ani_adjustx
        .word 11
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_6
        .long ks_kano_pose_ff82fe80
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_7
        .long ks_kano_pose_ff82fee0
        .long 0
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_8
        .long ks_kano_pose_ff82ff40
        .long ani_calla,ks_blade_fx_step,ks_blade_fx_9
        .long ks_kano_pose_ff82ffa0
        .long 0
ks_blade_fx_0
        .word 7,15,21,-110
        .long 0064b4568h
        .word 06000h
        .long ks_knife_palette
ks_blade_fx_1
        .word 21,19,15,-101
        .long 0064b47e0h
        .word 06080h
        .long ks_knife_palette
ks_blade_fx_2
        .word 18,24,15,-98
        .long 0064b4e78h
        .word 06080h
        .long ks_knife_palette
ks_blade_fx_3
        .word 60,15,-17,-102
        .long 0064b54d8h
        .word 06580h
        .long ks_knife_palette
ks_blade_fx_4
        .word 40,54,-70,-41
        .long 0064b64a8h
        .word 06180h
        .long ks_knife_palette
ks_blade_fx_5
        .word 47,36,-68,12
        .long 0064b8628h
        .word 06180h
        .long ks_knife_palette
ks_blade_fx_6
        .word 37,45,-30,60
        .long 0064ba2d8h
        .word 06080h
        .long ks_knife_palette
ks_blade_fx_7
        .word 44,33,40,50
        .long 0064bc048h
        .word 06180h
        .long ks_knife_palette
ks_blade_fx_8
        .word 12,47,37,23
        .long 0064bd7b8h
        .word 06080h
        .long ks_knife_palette
ks_blade_fx_9
        .word 21,23,24,-42
        .long 0064be448h
        .word 06080h
        .long ks_knife_palette
