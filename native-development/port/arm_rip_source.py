"""Own-ID arm-rip dispatch; original table contents and paths stay intact."""

def lookup(table,helper,kano,sonya,tag,other=False):
    old=f'\tmovi\t{table},a0\n\tcalla\t{helper}'
    char=('\tmove *a13(p_otherguy),a0,l\n\tmove *a0(ochar),a0,w' if other else '\tmove *a8(ochar),a0,w')
    new=f'''{char}
	cmpi 17,a0
	jreq ks_ar_{tag}_k
	cmpi 18,a0
	jreq ks_ar_{tag}_s
{old}
	jruc ks_ar_{tag}_ready
ks_ar_{tag}_k
	movi {kano},a0
	jruc ks_ar_{tag}_ready
ks_ar_{tag}_s
	movi {sonya},a0
ks_ar_{tag}_ready'''
    return old,new

DEATH=(lookup('ochar_arm_ripped_ani','get_char_long','ks_kano_arms_ripped','ks_sonya_arms_ripped','pose'),
       lookup('arm_ripped_adjust','get_char_long','00008ff70H','00007ff70H','line'),
       lookup('ochar_flyin_arms','get_his_char_long','ks_kano_arm_fly','ks_sonya_arm_fly','fly',True))
BLOOD=(lookup('arm_flow_lineups','get_char_long','00018001aH','000180018H','drip'),)
GUSH_OLD='gush_lineup\n\tcalla\tget_char_long'
GUSH_NEW='''gush_lineup
	push a2
	move a0,a2
	move *a8(ochar),a0,w
	cmpi 17,a0
	jreq ks_ar_own_gush
	cmpi 18,a0
	jreq ks_ar_own_gush
	move a2,a0
	calla get_char_long
	jruc ks_ar_gush_ready
ks_ar_own_gush
	cmpi 17,a0
	jrne ks_ar_sonya_gush
	cmpi right_gush_lineups,a2
	jreq ks_ar_k_right_gush
	movi 000510000H,a0
	jruc ks_ar_gush_ready
ks_ar_k_right_gush
	movi 0005bffd9H,a0
	jruc ks_ar_gush_ready
ks_ar_sonya_gush
	cmpi right_gush_lineups,a2
	jreq ks_ar_right_gush
	movi 00052fffeH,a0
	jruc ks_ar_gush_ready
ks_ar_right_gush
	movi 00057ffddH,a0
ks_ar_gush_ready
	pull a2'''

def integrate(text,file):
    replacements=DEATH if file=='MKDEATH.ASM' else BLOOD+((GUSH_OLD,GUSH_NEW),)
    for old,new in replacements:
        assert text.count(old)==1,(file,old)
        text=text.replace(old,new)
    if file=='MKDEATH.ASM':text='\t.ref ks_kano_arms_ripped,ks_sonya_arms_ripped,ks_kano_arm_fly,ks_sonya_arm_fly\n'+text
    else:text='\t.def GUSHER1\n'+text
    return text
