"""Own split lookup and asymmetric secondary-half script, native timing intact."""
from arm_rip_source import lookup

LOOKUP_OLD,LOOKUP_NEW=lookup('split_in_2_tab','get_char_long','ks_kano_split','ks_sonya_split','split')
LOOKUP_NATIVE=LOOKUP_OLD.replace(',a0\n',',a0\t\n')
LOOKUP_NEW=LOOKUP_NEW.replace(LOOKUP_OLD,LOOKUP_NATIVE)
SECOND_OLD='\tmmfm\tsp,a8,a9\n\tmove\ta9,a11\n\n;\tcreate\tpid_blood,split_blood2'
SECOND_NEW='''\tmmfm\tsp,a8,a9
\tmove\ta9,a11
\tmove *a8(ochar),a0,w
\tcmpi 17,a0
\tjreq ks_sp_other_k
\tcmpi 18,a0
\tjrne ks_sp_other_ready
\tmovi ks_sonya_split_other,a11
\tjruc ks_sp_other_ready
ks_sp_other_k
\tmovi ks_kano_split_other,a11
ks_sp_other_ready

;\tcreate\tpid_blood,split_blood2'''


def integrate(text):
    assert text.count(LOOKUP_NATIVE)==1 and text.count(SECOND_OLD)==1
    text=text.replace(LOOKUP_NATIVE,LOOKUP_NEW).replace(SECOND_OLD,SECOND_NEW)
    assert text.count('\nr_split_in_2\n')==1
    return text.replace('\nr_split_in_2\n',
        '\n\t.ref ks_kano_split,ks_sonya_split,ks_kano_split_other,ks_sonya_split_other\nr_split_in_2\n')
