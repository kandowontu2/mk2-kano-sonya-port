"""Native typed roster dispatch and input-type-aware Friendship checks."""
CHECKS='''
; Added actors keep native eligibility/transfer; Kano uses button history,
; Sonya uses direction history with a live Block ending.
	move *a8(ochar),a0,w
	cmpi ft_goro,a0
	jreq fsno
	cmpi ft_final_boss,a0
	jreq fsno
	cmpi 17,a0
	jreq ks_fs_kano
	cmpi 18,a0
	jrne ks_fs_original_history
	calla is_he_a_boss
	jrc fsno
	calla get_x_dist
	cmpi 0a0h,a3
	jrlo fsno
	movi f1b2,a0
	movi f2b2,a1
	calla button_mask
	jreq fsno
	movi f1b0|f1b1|f1b3|f1b4,a0
	movi f2b0|f2b1|f2b3|f2b4,a1
	calla button_mask
	jrne fsno
	jruc ks_fs_original_history
ks_fs_kano
	calla is_he_a_boss
	jrc fsno
	calla get_x_dist
	cmpi 0a0h,a3
	jrlo fsno
	movi f1b3,a0
	movi f2b3,a1
	calla button_mask
	jreq fsno
	movi f1b0|f1b1|f1b2|f1b4,a0
	movi f2b0|f2b1|f2b2|f2b4,a1
	calla button_mask
	jrne fsno
	movi ks_fs_kano_buttons,a11
	calla button_look_lr
	jrnc fsno
	jruc ks_fs_found
ks_fs_original_history
'''
COMMANDS='''
	.long 0,0,scom_nj_friend,scom_nj_friend,scom_fn_friend
	.long ks_fs_kano_buttons,ks_fs_sonya_directions
ks_fs_kano_buttons
	.word 050h
	.word sw_hi_kick,sw_block,sw_block,sw_lo_kick,0,0
ks_fs_sonya_directions
	.word 038h
	.word sw_down,sw_left,sw_right,sw_left,0,0
	.word sw_down,sw_right,sw_left,sw_right,0,0
'''

def integrate(text):
    def replace(old,new):
        nonlocal text
        assert text.count(old)==1,old
        text=text.replace(old,new)
    replace('\tmovi\tochar_friendship_combos,a0\n',CHECKS+'\tmovi\tochar_friendship_combos,a0\n')
    replace('\tpull\ta0\n\tmovi\tdo_friendship,a7','ks_fs_found\n\tpull\ta0\n\tmovi\tdo_friendship,a7')
    replace('\t.long\tscom_jx_friend\n','\t.long\tscom_jx_friend\n'+COMMANDS)
    replace('\t.long\tjx_friend\n','\t.long\tjx_friend\n\t.long sucide,sucide,nj_friend,nj_friend,fn1_friend\n\t.long ks_kano_friend,ks_sonya_friend\n')
    return '\t.ref ks_kano_friend,ks_sonya_friend,button_mask,button_look_lr\n'+text
