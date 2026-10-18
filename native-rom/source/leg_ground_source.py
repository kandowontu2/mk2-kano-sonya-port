"""Ground own detached legs without changing shared art or original actors."""
OWN_LEG_EXTENT=141  # PGM opaque last row93 +1 - signed yOffset(-47).
SPAWN='\tcalla\tmatch_ani_points\n\tpull\ta8\n\n\tcalla\tinsobja8'
SHATTER='\tcalla do_next_a9_frame\n\tcallr ks_own_statue_palette\n\tjauc wait_forever\nks_own_statue_palette'
PALETTE='ks_statue_sonya_palette\n\tmovi ks_sonya_statue_palette,a0\n\tjauc player_swpal'
HELPER='''
; Only the own detached-leg consumers call this helper. Their art has an
; opaque lower extent of141 from the animation pivot; preserve every other ID.
ks_ground_own_legs
	push a0
	move *a8(ochar),a0,w
	cmpi 17,a0
	jreq ks_ground_own_legs_apply
	cmpi 18,a0
	jrne ks_ground_own_legs_done
ks_ground_own_legs_apply
	move @ground_y,a0,w
	subi 08dH,a0
	move a0,*a8(oypos),w
ks_ground_own_legs_done
	pull a0
	rets
'''

def integrate(text):
    assert 'ks_ground_own_legs' not in text,'Already integrated'
    assert text.count(SPAWN)==3,'Expected Goro, Scorpion and Cage leg insertions'
    assert text.count(SHATTER)==text.count(PALETTE)==1,'Expected own shatter/palette branches'
    text=text.replace(SPAWN,SPAWN.replace('\n\n\tcalla\tinsobja8','\n\tcallr ks_ground_own_legs\n\n\tcalla\tinsobja8'))
    text=text.replace(SHATTER,SHATTER.replace('\n\tcallr ks_own_statue_palette','\n\tcallr ks_ground_own_legs\n\tcallr ks_own_statue_palette'))
    return '\t.def ks_ground_own_legs\n'+text.replace(PALETTE,PALETTE+'\n'+HELPER)
