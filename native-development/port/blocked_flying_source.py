"""Explicit added-ID block response without changing original lookup paths."""

OLD='\tmovi\tochar_block_superk,a0\n\tcalla\tget_char_word'
NEW='''ks_superk_block_pick
	move *a8(ochar),a0,w
	cmpi 17,a0
	jreq b_superk_lite
	cmpi 18,a0
	jreq b_superk_lite
	movi	ochar_block_superk,a0
	calla	get_char_word'''

def integrate(text):
    assert text.count(OLD)==1
    return '\t.def ks_superk_block_pick\n'+text.replace(OLD,NEW)
