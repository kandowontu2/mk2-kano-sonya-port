"""Own ROM-native announcer routes; original roster routes remain unchanged."""
def integrate(sound, selection, main):
    marker='\ntriple_end2\n'
    section=sound.split('\ntriple_sndtab2\n',1)[1].split(marker,1)[0]
    assert sum(line.lstrip().startswith('.word') for line in section.splitlines())==91
    entries='\n; MK2KS own name and win announcements, slots5b..5e.\n'
    for duration,call,label in ((72,2009,'Kano name'),(72,2012,'Sonya name'),
                                (122,2015,'Kano wins'),(122,2018,'Sonya wins')):
        entries+=f'\t.word\tsp_bossv1|{duration},0{call:04x}H\t; {label}\n'
    sound=sound.replace(marker,entries+marker)
    old='selsp3\taddi\t01cH,a10\n\tmove\ta10,a0\n\tcalla\ttriple_sound2'
    assert selection.count(old)==1
    new='selsp3\tcmpi\tft_kano,a10\n\tjreq\tks_sel_kano\n'
    new+='\tcmpi\tft_sonya,a10\n\tjreq\tks_sel_sonya\n'
    new+='\taddi\t01cH,a10\n\tmove\ta10,a0\n\tjruc\tks_sel_call\n'
    new+='ks_sel_kano\n\tmovi\t05bH,a0\n\tjruc\tks_sel_call\n'
    new+='ks_sel_sonya\n\tmovi\t05cH,a0\n'
    new+='ks_sel_call\n\tcalla\ttriple_sound2'
    selection=selection.replace(old,new)
    old='ks_sel_call\n\tcalla\ttriple_sound2\n\tsleep\t030H\n\tdie'
    assert selection.count(old)==1
    new='ks_sel_call\n\tcalla\ttriple_sound2\n'
    new+='\tcmpi\tft_kano,a10\n\tjreq\tks_sel_own_wait\n'
    new+='\tcmpi\tft_sonya,a10\n\tjreq\tks_sel_own_wait\n'
    new+='\tsleep\t030H\n\tdie\n'
    new+='ks_sel_own_wait\n\tsleep\t048H\n\tdie'
    selection=selection.replace(old,new)
    before,after=main.split('\nwinner_speech\n',1)
    table,rest=after.split('\nks_pf_kano_win\n',1)
    assert table.count('\t.word 0,0')==1
    table=table.replace('\t.word 0,0','\t.word 05dH,05eH ; own Kano/Sonya win announcements')
    main=before+'\nwinner_speech\n'+table+'\nks_pf_kano_win\n'+rest
    return sound,selection,main
