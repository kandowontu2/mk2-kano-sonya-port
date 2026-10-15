"""Preserve real whole-round rejection; use exact stock XY clipping flags.

Five genuine launched-victim parts have bottom edge exactlyzero. Original
SUBXY/JRC/JRV keeps equality at the lower clip boundary; the old generic
rectangle test discarded it. Entire unchanged original gate/fault suite stays.
"""
import hashlib
import inspect
import json
from pathlib import Path
import qualify_native_selector_sonya_cpu_pressure_round_shadow as original

original_source=Path(original.__file__)
original_failure=original.OUT/'failure.json'
need=original.need
need(json.loads(original_failure.read_text())['error']==
     "ValueError('Every actual complete body part published iff on screen')",
     'Preserved executed full-round strict-rectangle rejection')
ops=original.ROOT/'mame-mkp/src/devices/cpu/tms34010/34010ops.hxx'
need(original.sha(ops)=='772F372A89CBDA2D7F8E59E51540350F17EFF175B0006EEA1C69BB033D2EDB12',
     'Entire actually compiled CPU operations source unchanged')
ops_source=ops.read_text()
for fragment in ('SET_N_LOG(a.x == b->x);','SET_C_LOG(a.y > b->y);',
                 'SET_Z_LOG(a.y == b->y);','SET_V_LOG(a.x > b->x);',
                 'j_xx_8(!C_FLAG() && !Z_FLAG());',
                 'j_xx_8((N_FLAG() && V_FLAG()) || (!N_FLAG() && !V_FLAG()));'):
    need(fragment in ops_source,'Whole source-native XY/JRHI/JRGE flag semantics: '+fragment)


def native_published(x,y,w,h,t):
    # FF8042B0 ADDXY A9,A2, then FF8042C0 SUBXY A14,A2.
    # SUBXY C=(clipLowY>bottom), V=(clipLowX>right); JRC/JRV reject.
    right,bottom=original.body.short(x+w),original.body.short(y+h)
    low=original.body.num(t,'clipLow');high=original.body.num(t,'clipHigh')
    lx,ly=original.body.short(low),original.body.short(low>>16)
    hx,hy=original.body.short(high),original.body.short(high>>16)
    if ly>bottom or lx>right:return False
    # FF804310 SUBXY A13,A2 sets N=(clipHighX==x), C=(clipHighY>y),
    # Z=(clipHighY==y), V=(clipHighX>x). JRHI then JRGE reject.
    n,c,z,v=(hx==x,hy>y,hy==y,hx>x)
    return not ((not c and not z) or (n==v))


def native_body(*args):
    return source_body(*args)


body_source=inspect.getsource(original.body.check_body)
before='shown=x+w>0 and y+h>0 and x<400 and y<254'
need(body_source.count(before)==1,'Only exact source-native clip decision boundary')
body_source=body_source.replace(before,'shown=native_published(x,y,w,h,t)',1)
body_scope=dict(vars(original.body),native_published=native_published)
exec(compile(body_source,__file__+'::whole_original_body_with_exact_XY_clip_flags','exec'),body_scope)
source_body=body_scope['check_body']
clip={'clipLow':'00000000','clipHigh':'00FE0190'}
for x,y,w,h,expected in ((10,-71,48,71,True),(10,-72,48,71,False),
    (-48,10,48,71,True),(-49,10,48,71,False),(400,10,48,71,True),
    (401,10,48,71,False),(10,254,48,71,True),(10,255,48,71,False)):
    need(native_published(x,y,w,h,clip)==expected,'Exact native signed XY boundary policy, including equality')

source=original_source.read_text()
for before,after in (
    ("OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_cpu_pressure_round_shadow_clip_checked'"),
    ('scope=dict(vars(body),state_gate=state_gate,context=context)',
     'scope=dict(vars(body),state_gate=state_gate,context=context,check_body=native_body)'),
    ("0xffa0dfc0:'JA     FF876650h'}",
     "0xffa0dfc0:'JA     FF876650h',0xff8042b0:'ADDXY  A9,A2',0xff8042c0:'SUBXY  A14,A2',"
     "0xff8042d0:'JRC    FF804570h',0xff8042e0:'JRV    FF804570h',"
     "0xff804310:'SUBXY  A13,A2',0xff804320:'JRHI   FF804570h',0xff804330:'JRGE   FF804570h'}"),
    ('Path(__file__),parent,Path(disasm.__file__),',
     'Path(__file__),original_source,original_failure,ops,parent,Path(disasm.__file__),'),
    ('originalBodyShadowFaultsRejected=faults,wholeRoundFaultsRejected=additional,inputHashes=pins,',
     'originalBodyShadowFaultsRejected=faults,wholeRoundFaultsRejected=additional,inputHashes=pins,'
     'originalStrictClipFailurePreserved=True,sourceNativeXYBoundaryChecks=8,')):
    need(source.count(before)==1,'Exact declared original whole-round checker boundary')
    source=source.replace(before,after,1)
exec(compile(source,str(original_source)+'::whole_original_case_exact_native_XY_clip_boundary','exec'))
