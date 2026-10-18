"""Native own ending dispatch and two-page photos; original tables untouched."""

def winner(text):
    assert 'ks_end_name_ready' not in text
    marker='msg_rise\n\tmove\ta1,*a13(p_store1),w\n'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'''	cmpi 17,a0
	jrne ks_end_not_kano
	movi ks_end_kano,a0
	jruc ks_end_name_ready
ks_end_not_kano
	cmpi 18,a0
	jrne ks_end_old_name
	movi ks_end_sonya,a0
	jruc ks_end_name_ready
ks_end_old_name
''')
    marker='\taddi\tend_winner_text,a0\n\tmove\t*a0,a0,l\n'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'ks_end_name_ready\n')
    marker='\nend_winner_text\n'
    assert text.count(marker)==1
    return text.replace(marker,'''
ks_end_kano .string "KANO WINS",0
	.even
ks_end_sonya .string "SONYA WINS",0
	.even
'''+marker)

def story(text):
    assert 'ks_story_show' not in text
    marker='\nshow_a0_ending\n'
    assert text.count(marker)==1
    text=text.replace(marker,marker+'''	cmpi 17,a0
	jrne ks_story_not_kano
	movi ks_story_kano,a8
	jruc ks_story_show
ks_story_not_kano
	cmpi 18,a0
	jrne ks_story_original
	movi ks_story_sonya,a8
	jruc ks_story_show
ks_story_original
''')
    marker='\nend_text_1\n'
    assert text.count(marker)==1
    own='''
; Ordinary image objects and text, with no added compressed-picture decoder.
        .ref ks_end_kano_picture1,ks_end_kano_picture2
        .ref ks_end_sonya_picture1,ks_end_sonya_picture2
        .ref dlists_bogus
ks_story_show
ks_story_page
	pushp a8
	calla murder_myoinit_score
	calla clr_scrn
	; oinit clears dlists: restore native object-list rendering for this page.
	movi dlists_bogus,a0
	move a0,@dlists,l
	; Native static-story path: one fixed page, no autoerase or page flipping.
	calla page_0_setup_no_init
	pullp a11
	move *a11+,a5,l
	move *a11+,a4,l
	pushp a11
	pushp a4
	calla gso_dmawnz_ns
	pullp a4
	calla set_xy_coordinates
	calla insobj2a8
	pullp a11
	move *a11+,a8,l
	pushp a11
	jsrp lm_printf
	calla display_on
	sleep 4
	calla display_off
	calla sync_wait_dma_q
	calla grab_screen
	calla display_on
	sleep 040H*12
	pullp a8
	move *a8,a0,l
	jrne ks_story_page
	calla murder_myoinit_score
	calla clr_scrn
	retp

ks_story_kano
	.long ks_end_kano_picture1,0029001eH,ks_story_kano_text1
	.long ks_end_kano_picture2,0019003cH,ks_story_kano_text2
	.long 0
ks_story_sonya
	.long ks_end_sonya_picture1,0029001eH,ks_story_sonya_text1
	.long ks_end_sonya_picture2,0019003cH,ks_story_sonya_text2
	.long 0
ks_story_kano_text1
	mess_mac rd11font,2,0bdH,012H,bpal_white*010000H,strlnrmos_scr,0
	.string "KANO\\n\\n"
	.string "WITH SHAO KAHN\\n"
	.string "DEFEATED, KANO\\n"
	.string "ESCAPES THE CHAINS\\n"
	.string "THAT HELD HIM\\n"
	.string "IN OUTWORLD.",0
	.even
ks_story_kano_text2
	mess_mac rd11font,2,01cH,0a5H,bpal_white*010000H,strlnrmos_scr,0
	.string "HIS FREEDOM IS NO VICTORY FOR EARTH.\\n"
	.string "THE BLACK DRAGON WILL RISE AGAIN.",0
	.even
ks_story_sonya_text1
	mess_mac rd11font,2,0bdH,012H,bpal_white*010000H,strlnrmos_scr,0
	.string "SONYA\\n\\n"
	.string "FREE OF SHAO KAHN'S\\n"
	.string "CHAINS, SONYA\\n"
	.string "RETURNS TO EARTH\\n"
	.string "WITH HER MISSION\\n"
	.string "UNFINISHED.",0
	.even
ks_story_sonya_text2
	mess_mac rd11font,2,01cH,0a5H,bpal_white*010000H,strlnrmos_scr,0
	.string "KANO HAS ESCAPED ONCE MORE.\\n"
	.string "SHE WILL NOT REST UNTIL THE BLACK DRAGON\\n"
	.string "FALLS.",0
	.even
'''
    return text.replace(marker,own+marker)

def cast(text):
    """Append one ordinary cast pair; preserve the six original pair records."""
    assert 'ks_cast_kano' not in text
    start=text.index('\ncast_table\n')
    stop=text.index('\npf_left_bow\n',start)
    body=text[start:stop]
    marker='\t.word\t0\n'
    assert body.count(marker)==1
    body=body.replace(marker,'''; Own roster pair follows the original six cast pairs.
\t.word 17,070H
\t.word 18,0120H
\t.long ks_cast_kano
\t.long ks_cast_sonya

'''+marker)
    text=text[:start]+body+text[stop:]
    marker='\ncast_table\n'
    credits='''
; Performers verified against the original donor program cast strings.
ks_cast_kano .string "RICHARD DIVIZIO\\nAS\\nKANO",0
\t.even
ks_cast_sonya .string "KERRI HOSKINS\\nAS\\nSONYA",0
\t.even
'''
    return text.replace(marker,credits+marker)
