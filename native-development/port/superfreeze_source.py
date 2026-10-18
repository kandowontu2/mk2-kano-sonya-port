"""Own victim pose/palette instead of out-of-range offset and Jax ice proxy."""
OLD_STUN='\tmovi\tfrozen_stunned,a0\n\tcalla\tget_char_word\n\tmove\ta0,a7'
NEW_STUN='''	move *a8(ochar),a0,w
	cmpi 17,a0
	jreq ks_superfreeze_own_stun
	cmpi 18,a0
	jreq ks_superfreeze_own_stun
	movi	frozen_stunned,a0
	calla	get_char_word
	jruc ks_superfreeze_stun_ready
ks_superfreeze_own_stun
	clr a0
ks_superfreeze_stun_ready
	move	a0,a7'''
OLD_ICE='\tmove\t*a8(ochar),a9,w\n\tcmpi\tft_jax,a9\n\tjrls\trsupf5'
NEW_ICE='''	move	*a8(ochar),a9,w
	cmpi 17,a9
	jreq ks_superfreeze_own_ice
	cmpi 18,a9
	jreq ks_superfreeze_own_ice
	cmpi	ft_jax,a9
	jrls	rsupf5'''
OLD_LOOP='\nrsup9\tsleep\t40\nsuper_frozen'
NEW_LOOP='''
	jruc rsup9
ks_superfreeze_own_ice
	movi 028H,a9
	calla get_char_ani
	calla do_next_a9_frame
	callr ks_own_statue_palette
rsup9	sleep	40
super_frozen'''

OLD_LEGS='''	movi	FREEZE_P,a0
	calla	player_swpal
	move	*a8(ochar),a9,w
	sll	5,a9
	addi	frozen_legs,a9
	calla	do_next_a9_frame
	jauc	wait_forever'''
NEW_LEGS='''	move *a8(ochar),a0,w
	cmpi 17,a0
	jreq ks_shatter_own_legs
	cmpi 18,a0
	jreq ks_shatter_own_legs
	movi	FREEZE_P,a0
	calla	player_swpal
	move	*a8(ochar),a9,w
	sll	5,a9
	addi	frozen_legs,a9
	calla	do_next_a9_frame
	jauc	wait_forever
ks_shatter_own_legs
	movi 039H,a9
	calla get_char_ani
	movk 6,a14
	calla find_part_a14
	calla do_next_a9_frame
	callr ks_own_statue_palette
	jauc wait_forever
ks_own_statue_palette
	move *a8(ochar),a0,w
	cmpi 17,a0
	jrne ks_statue_sonya_palette
	movi ks_kano_statue_palette,a0
	jauc player_swpal
ks_statue_sonya_palette
	movi ks_sonya_statue_palette,a0
	jauc player_swpal'''

def integrate(text):
    for old,new in ((OLD_STUN,NEW_STUN),(OLD_ICE,NEW_ICE),(OLD_LOOP,NEW_LOOP),(OLD_LEGS,NEW_LEGS)):
        assert text.count(old)==1
        text=text.replace(old,new)
    return '\t.ref ks_kano_statue_palette,ks_sonya_statue_palette\n\t.def ks_superfreeze_own_ice,ks_shatter_own_legs\n'+text
