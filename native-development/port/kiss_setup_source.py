"""Own dizzy wait offsets; preserve the original shared kiss setup path."""
OLD = '\tcalla\tget_his_char_word\n\tadd\ta0,a9 '
NEW = '''\tpush a1
\tmove *a13(p_otherguy),a1,l
\tmove *a1(ochar),a1,w
\tcmpi 17,a1
\tjreq ks_kiss_own_stop
\tcmpi 18,a1
\tjreq ks_kiss_own_stop
\tpull a1
\tcalla\tget_his_char_word
\tjruc ks_kiss_stop_ready
ks_kiss_own_stop
\tpull a1
\tmovi 32*5,a0 ; own seven-pose dizzy loop, after fifth pose
ks_kiss_stop_ready
\tadd\ta0,a9 '''


def integrate(text):
    assert text.count(OLD) == 1, 'Unexpected shared dizzy_wait source'
    return text.replace(OLD, NEW)
