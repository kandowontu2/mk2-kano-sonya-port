"""Native board-specific Dead Pool held-button read, no emulator alteration."""
OLD = '\tmove\t@switch2,a3,l\n\tnot\ta3\n\tmove\t*a8(oid),a0,w\n\tcmpi\toid_p1,a0\n\tjreq\tucut1\n'
NEW = '''\t.if wunit
* Wolf LP/LK are bits16/17 (P1),20/21 (P2) of the main input longword.
\tmove\t@switch,a3,l
\tnot\ta3
\tsrl\t16,a3
\t.else
\tmove\t@switch2,a3,l
\tnot\ta3
\t.endif
\tmove\t*a8(oid),a0,w
\tcmpi\toid_p1,a0
\tjreq\tucut1
'''

def integrate(text):
    assert text.count(OLD)==1, 'Unexpected native Dead Pool input gate'
    return text.replace(OLD,NEW)

WAIT_OLD='\tmovi\t088H,a2\n\tmove\ta2,*a0(pa11),l\t\t; yes, wait a little longer'
WAIT_NEW='''\t.if wunit
* Current Wolf baseline's flight plus hidden80-field wait outlives136 fields.
* Keep a bounded allowance; the native skeleton phase still declares completion.
\tmovi\t0100H,a2
\t.else
\tmovi\t088H,a2
\t.endif
\tmove\ta2,*a0(pa11),l\t\t; yes, wait a little longer'''

def integrate_wait(text):
    assert text.count(WAIT_OLD)==1, 'Unexpected native Dead Pool master wait'
    return text.replace(WAIT_OLD,WAIT_NEW)
