"""Classify own projectile launches for original boss category dispatch only."""
HELPER='''
; Return action category in A1; preserve original action stored in the process.
; Only matching true identities can reinterpret the two own launch tags.
ks_boss_category
	push a0
	cmpi 0211h,a1
	jrne ks_boss_ring_category
	move *a13(p_otherguy),a0,l
	move *a0(ochar),a0,w
	cmpi 17,a0
	jrne ks_boss_old_category
	clr a1
	jruc ks_boss_category_done
ks_boss_ring_category
	cmpi 0212h,a1
	jrne ks_boss_old_category
	move *a13(p_otherguy),a0,l
	move *a0(ochar),a0,w
	cmpi 18,a0
	jrne ks_boss_old_category
	clr a1
	jruc ks_boss_category_done
ks_boss_old_category
	srl 8,a1
ks_boss_category_done
	pull a0
	rets
'''

def integrate(text):
    assert 'ks_boss_category' not in text
    old='\tsrl\t8,a1\t\t\t\t; just use the catagory part'
    assert text.count(old)==2
    text=text.replace(old,'\tcallr ks_boss_category\t\t; native own-projectile classification')
    marker='\n\t.end';assert text.count(marker)==1
    return '\t.def ks_boss_category\n'+text.replace(marker,'\n\t.text\n'+HELPER+marker)

def category(identity,action):
    """Specification oracle, not an emulation of the assembled helper."""
    return 0 if (identity,action) in ((17,0x211),(18,0x212)) else action>>8
