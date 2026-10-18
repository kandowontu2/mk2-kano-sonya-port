"""Checked true-ID native baby victim image table extension."""
def add_baby_images(text):
    marker='\nSZBABE\t.word'
    assert text.count(marker)==1
    rows='\n; Bosses cannot be babality victims; retain explicit empty boss rows.\n\t.long 0,0,SZBABE,SCBABE,KTBABE,ks_kano_baby,ks_sonya_baby\n'
    return '\t.ref ks_kano_baby,ks_sonya_baby\n'+text.replace(marker,rows+marker)

COMBOS='''
	.long 0,0,scom_nj_baby,scom_nj_baby,scom_fn_baby
	.long ks_kano_baby_combo,ks_sonya_baby_combo
ks_kano_baby_combo
	.word 038H
	.word sw_down,sw_down,sw_right,sw_right,0,0
	.word sw_down,sw_down,sw_left,sw_left,0,0
ks_sonya_baby_combo
	.word 038H
	.word sw_right,sw_down,sw_down,0,0,0
	.word sw_left,sw_down,sw_down,0,0,0
'''

def add_baby_commands(text):
    marker='\n\t.long\tscom_jx_baby\n'
    assert text.count(marker)==1
    return text.replace(marker,marker+COMBOS)
