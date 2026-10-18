"""Native Wolf graphics-bank reads for the original MKII floor-shadow walker.

Wolf CPU graphics window/bank register verified in stock MAME0.289:
src/mame/williams/midwunit.cpp and midtunit_v.cpp. No emulator modifications.
"""
OLD='shad7\tmove\t*a10+,a8,w\t; grab a BYTE !!'
NEW='''shad7
\t.if wunit
; A10 includes MKII's02000000h CPU-read bias. Wolf uses8MiB CPU banks.
; Preserve DMA helper registers and every original system-control bit.
\tmmtm\tsp,a0,a1,a2
\tsetf\t16,0,0
\tmove\t@sysctrl,a2,w
\tmove\ta10,a0
\tsubi\t02000000h,a0
\tmove\ta0,a1
\tsrl\t26,a1
\tandi\t3,a1
\tsll\t8,a1
\tmove\ta2,a8
\tandni\t0300h,a8
\tor\ta1,a8
\tmove\ta8,@sysctrl,w
\tandi\t03ffffffh,a0
\taddi\t02000000h,a0
\tsetf\t8,0,0
\tmove\t*a0,a8,w
\tsetf\t16,0,0
\tmove\ta2,@sysctrl,w
\tsetf\t8,0,0
\taddk\t8,a10
\tmmfm\tsp,a0,a1,a2
\t.else
\tmove\t*a10+,a8,w\t; original T-unit byte read
\t.endif'''

def integrate(text):
    assert text.count(OLD)==1
    text=text.replace(OLD,NEW)
    old='\tdsjs\tb3,shad7'
    assert text.count(old)==1
    return text.replace(old,'\t.if wunit\n\tdsj\tb3,shad7\n\t.else\n'+old+'\n\t.endif')
