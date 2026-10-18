"""Own-ID common reaction lookup; never alias stored actions or weaken AI."""
ROUTES={17:{0x20b:'ks_counter_body',0x211:'ks_counter_projectile',0x117:'ks_counter_grab',
            0x216:'ks_counter_grab',0x217:'0',0x215:'0',0x218:'0',0x21b:'0',
            0x618:'ks_counter_recovery',0x61a:'ks_counter_recovery'},
        18:{0x207:'ks_counter_body',0x212:'ks_counter_projectile',0x219:'ks_counter_grab',
            0x21a:'0',0x214:'0',0x215:'0',0x218:'0',0x21b:'0',0x61b:'ks_counter_recovery'}}

CODE='''
; A1=actual opponent action. Carry=handled own action, A2=reaction (possibly0).
; No stored action/identity changes. Original fighters and ordinary own normals
; continue through the original tables exactly as before.
ks_own_counter_lookup
	push a0
	move *a13(p_otherguy),a0,l
	move *a0(ochar),a0,w
	cmpi 17,a0
	jrne ks_counter_check_sonya
	movi ks_kano_counter_rows,a2
	jruc ks_counter_scan
ks_counter_check_sonya
	cmpi 18,a0
	jrne ks_counter_not_owned
	movi ks_sonya_counter_rows,a2
ks_counter_scan
	move *a2+,a0,w
	cmpi 0,a0
	jreq ks_counter_not_owned
	cmp a0,a1
	jreq ks_counter_found
	addi 32,a2
	jruc ks_counter_scan
ks_counter_found
	move *a2,a2,l
; Preserve the original Jade projectile-immunity reaction exception.
	cmpi 0211h,a1
	jreq ks_counter_jade_check
	cmpi 0212h,a1
	jrne ks_counter_owned_done
ks_counter_jade_check
	move *a8(ochar),a0,w
	cmpi ft_jade,a0
	jrne ks_counter_owned_done
	clr a2
ks_counter_owned_done
	pull a0
	setc
	rets
ks_counter_not_owned
	pull a0
	clrc
	rets

ks_counter_projectile
; Count the real own action in the native history/difficulty policy.
	callr drone_get_his_action
	movk 3,a7
	callr react_jump_table
	.long duck_under_proj,pro_avoid_projectile

ks_counter_body
	callr drone_get_his_action
	movk 3,a7
	callr react_jump_table
	.long drone_block,drone_block

ks_counter_grab
	calla get_x_dist
	cmpi 0b0h,a3
	jrhi ks_counter_far
	callr drone_get_his_action
	movk 3,a7
	callr react_jump_table
	.long drone_duck,drone_duck_upcut
ks_counter_far
	jauc return_to_beware

ks_counter_recovery
	callr rtb_nail_sd
	callr sweep_if_u_can
	jauc return_to_beware
'''

def integrate(text):
    assert 'ks_own_counter_lookup' not in text
    marker='\n\tmove\ta1,a2\n\tsrl\t8,a2\n\tjrne\tbew5'
    assert text.count(marker)==1
    text=text.replace(marker,'''
	callr ks_own_counter_lookup
	jrnc ks_counter_original_lookup
	move a2,a1
	jruc ks_counter_dispatch_ready
ks_counter_original_lookup
'''+marker)
    marker='\tmove\t*a1,a1,l\n\tjreq\tbew8'
    assert text.count(marker)==1
    text=text.replace(marker,'\tmove\t*a1,a1,l\nks_counter_dispatch_ready\n\tmove a1,a1\n\tjreq\tbew8')
    rows=''
    for identity,name in ((17,'kano'),(18,'sonya')):
        rows+=f'\nks_{name}_counter_rows\n'
        for action,reaction in ROUTES[identity].items():
            rows+=f'\t.word 0{action:04x}h\n\t.long {reaction}\n'
        rows+='\t.word 0\n\t.long 0\n'
    marker='\n\t.end';assert text.count(marker)==1
    return '\t.def ks_own_counter_lookup\n'+text.replace(marker,'\n\t.text\n'+CODE+rows+marker)
