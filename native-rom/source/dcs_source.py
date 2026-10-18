"""Authored native TMS sound-priority entry for the own DCS playlist extension."""
def integrate(text):
    marker='\ntriple_end\n'
    assert text.count(marker)==1
    section=text.split('\ntriple_sndtab\n',1)[1].split(marker,1)[0]
    assert sum(line.lstrip().startswith('.word') for line in section.splitlines())==254
    entry='\n; MK2KS own native DCS Square launch: playlists2000/2001/2002.\n'
    entry+='\t.word\tsp_attkv1|59,07d0H\t; fe = Sonya Square launch\n'
    entry+='\t.word\tsp_attkv1|53,07d3H\t; ff = Sonya Bicycle launch\n'
    entry+='\t.word\tsp_bikeyl|86,07d6H\t; 100 = Sonya Bicycle paired cry\n'
    entry+='\t.word\tsp_attkv1|86,07e5H\t; 101 = Sonya kiss\n'
    entry+='\t.word\tsp_effect|234,07e8H\t; 102 = Sonya burn fire\n'
    entry+='\t.word\tsp_reacv1|168,07ebH\t; 103 = Sonya burn victim\n'
    entry+='\t.word\tsp_effect|40,07eeH\t; 104 = Kano Friendship bubble pop\n'
    entry+='\t.word\tsp_attkv1|72,07f1H\t; 105 = Kano Ball launch\n'
    for index,(hold,call) in enumerate(((16,2036),(23,2039),(20,2042),(18,2045))):
        entry+=f'\t.word\tsp_woosh1|{hold},0{call:04x}H\t; {262+index:x} = Sonya Friendship variant{index}\n'
    return text.replace(marker,entry+marker)
