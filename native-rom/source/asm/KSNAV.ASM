; Native selector navigation. No key interception or emulated-state patches.
; Integration points: MKSEL new_cursor_position and is_move_legal.
; Callers must use the counted ks_*_sans tables, not the old fixed five words.
        .file "KSNAV.ASM"
        .def ks_cursor_destination,ks_move_legal
        .def ks_up_change,ks_down_change,ks_left_change,ks_right_change
        .def ks_up_sans,ks_down_sans,ks_left_sans,ks_right_sans
        .def ks_selection_xy,ks_menu_ids,ks_id_menu
        .text
; A1=current ID, A2=direction map. Returns A1=new ID, A3=dx, A4=dy.
; Preserve the original cursor process registers and player-number objects.
ks_cursor_destination
        mmtm sp,a0,a2,a5,a6
        cmpi 18,a1
        jrhi ks_nav_invalid
        move a1,a0
        sll 5,a0
        addi ks_selection_xy,a0
        move *a0+,a3,0
        move *a0,a4,0
        sll 4,a1
        add a2,a1
        move *a1,a1,0
        move a1,a0
        sll 5,a0
        addi ks_selection_xy,a0
        move *a0+,a5,0
        move *a0,a6,0
        sub a3,a5
        sub a4,a6
        move a5,a3
        move a6,a4
        mmfm sp,a0,a2,a5,a6
        rets
ks_nav_invalid
        clr a3
        clr a4
        mmfm sp,a0,a2,a5,a6
        rets
; A1=current ID, A2=counted sans table. Carry=allowed, no carry=blocked.
ks_move_legal
        mmtm sp,a0
        move *a2+,a0,0
ks_legal_loop
        move *a2+,a3,0
        cmp a1,a3
        jreq ks_legal_no
        dsjs a0,ks_legal_loop
        setc
        mmfm sp,a0
        rets
ks_legal_no
        clrc
        mmfm sp,a0
        rets
        .data
ks_selection_xy
        .word 143,24,83,24,203,24,143,174,203,99,83,174
        .word 143,99,263,174,83,99,263,24,203,174,263,99
        .word 0,0,0,0,0,0,0,0,0,0,23,24,323,24
ks_menu_ids
        .word 1,0,2,9,8,6,4,11,5,3,10,7,17,18
ks_id_menu
        .word 1,0,2,9,6,8,5,11,4,3,10,7,-1,-1,-1,-1,-1,12,13
ks_up_change
        .word 0,1,2,6,2,8,0,11,1,9,4,9,12,13,14,15,16,17,18
ks_down_change
        .word 6,8,4,3,10,5,3,7,5,11,10,7,12,13,14,15,16,8,11
ks_left_change
        .word 1,17,0,5,6,5,8,10,8,2,3,4,12,13,14,15,16,17,9
ks_right_change
        .word 2,0,9,10,11,3,4,7,6,18,7,11,12,13,14,15,16,1,18
; Count plus all self-neighbor IDs, including non-selectable boss/hidden slots.
ks_up_sans
        .word 11,0,1,2,9,12,13,14,15,16,17,18
ks_down_sans
        .word 9,3,5,7,10,12,13,14,15,16
ks_left_sans
        .word 8,5,8,12,13,14,15,16,17
ks_right_sans
        .word 8,7,11,12,13,14,15,16,18
