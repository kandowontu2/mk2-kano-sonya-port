"""Checked native source additions for Shang's two new target identities."""
MORPH_ROWS='''
	.long dummy,dummy,dummy
	.long ks_st_to_kano,ks_st_to_sonya
; Authored intermediate frames; native cadence and final stance retained.
ks_st_to_kano
	.long STSTANCE1
	.long ani_calla,ks_morph_kano_pal
	.long ks_mo_kano_pose0,ks_mo_kano_pose1,ks_mo_kano_pose2
	.long ani_nosleep,ks_kano_pose_ff8246a0,0
ks_st_to_sonya
	.long STSTANCE1
	.long ani_calla,ks_morph_sonya_pal
	.long ks_mo_sonya_pose0,ks_mo_sonya_pose1,ks_mo_sonya_pose2
	.long ani_nosleep,ks_sonya_pose_ff8325a0,0
'''

MORPH_ENTRY_HELPERS='''
; Own entry images use the target baseline while OCHAR is still Shang.
; Reverse morph already uses the target anchor and does not call these.
ks_morph_kano_pal
	callr morph_swpal
	movi 131,a1
	jruc ks_morph_entry_ground
ks_morph_sonya_pal
	callr morph_swpal
	movi 132,a1
ks_morph_entry_ground
	move @ground_y,a0,w
	sub a1,a0
	move a0,*a8(oypos),w
	rets
'''

def add_morph_art(text):
    marker='\n\tdummy\n' if '\n\tdummy\n' in text else '\ndummy\n'
    assert text.count(marker)==1
    refs='\t.ref ks_kano_pose_ff8246a0,ks_kano_pose_ff824700,ks_kano_pose_ff8247c0\n\t.ref ks_sonya_pose_ff8325a0,ks_sonya_pose_ff832600,ks_sonya_pose_ff832660\n'
    refs+='\t.ref ks_mo_kano_pose0,ks_mo_kano_pose1,ks_mo_kano_pose2\n\t.ref ks_mo_sonya_pose0,ks_mo_sonya_pose1,ks_mo_sonya_pose2\n'
    assert text.count('\nmorph_swpal\n')==1
    text=text.replace('\nmorph_swpal\n',MORPH_ENTRY_HELPERS+'\nmorph_swpal\n')
    return refs+text.replace(marker,MORPH_ROWS+marker)

def add_morphs(text):
    changes={
        'st_block\n': 'st_block\n\tcalla ks_leg_chord\n\tjrnc ks_st_block_original\n\tmovi do_st_2_sonya,a7\n\tjruc restricted_xfer\nks_st_block_original\n',
        'st_lo_punch\n': 'st_lo_punch\n\tcalla ks_leg_chord\n\tjrnc ks_st_lp_original\n\tmovi do_st_2_sonya,a7\n\tjruc restricted_xfer\nks_st_lp_original\n',
        'stlk2\n': 'stlk2\n\tmovi f1b0|f1b1|f1b2|f1b3,a0\n\tmovi f2b0|f2b1|f2b2|f2b3,a1\n\tmovi ks_scom_st_kano,a11\n\tcallr combo_look_lr\n\tjrnc ks_st_lk_original\n\tmovi do_st_2_kano,a7\n\tjruc restricted_xfer\nks_st_lk_original\n',
        'do_st_2_hh\n': 'do_st_2_kano\n\tmovi 17,a9\n\tjruc shang_morph\ndo_st_2_sonya\n\tmovi 18,a9\n\tjruc shang_morph\ndo_st_2_hh\n',
    }
    for old,new in changes.items():
        old='\n'+old;new='\n'+new
        assert text.count(old)==1,old
        text=text.replace(old,new)
    marker='\ndo_st_2_kano\n'
    table='\n\t.ref ks_leg_chord\nks_scom_st_kano\n\t.word 030H\n\t.word sw_left,sw_down,sw_left,0,0,0\n\t.word sw_right,sw_down,sw_right,0,0,0\n'
    assert text.count(marker)==1
    return text.replace(marker,table+'do_st_2_kano\n')
