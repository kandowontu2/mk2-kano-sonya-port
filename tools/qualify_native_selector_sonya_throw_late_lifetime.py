"""Distinguish true-character writes from three neutral bound-address writes.

The original tap remains attached through reset/retirement. All138 callbacks
remain checked, but three zero-pose/id0/zero-body callbacks do not become
claims of a live native17/18 character. Preserve the original rejection.
"""
from pathlib import Path
import qualify_native_selector_sonya_throw_late_checkpoint as previous

ROOT=previous.ROOT
SOURCE=Path(previous.__file__)
FAILURE=previous.OUT/'failure.json'


def neutral_body_context(r,guest):
    expected={(2433,1):0xff83ff50,(2433,2):0xff83ff50,(3412,2):0xffa2ec30}
    key=(int(r['frame']),int(r['slot']))
    if key not in expected:return False
    pc=expected[key]
    if int(r['pc'],16)!=pc:return False
    previous.need(r['id']=='0' and r['pose']=='00000000' and
        r['before']==r['after']==r['data']==r['body']=='0000' and r['mask']=='FFFF',
        'Only exact original reset/retired zero-pose neutral target callbacks')
    stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    lo,hi=(pc-64-0xff800000)//8,(pc+16-0xff800000)//8
    previous.need(guest[lo:hi]==stock[lo:hi],
        'Whole original native neutral reset/retired target instruction context')
    previous.need((int(r['op0'],16),int(r['op1'],16))==previous.struct.unpack_from('<2H',guest,(pc-32-0xff800000)//8),
        'Actual captured native neutral callback instruction words')
    return True


source=SOURCE.read_text()
changes=[
    ("OUT=ROOT/'audit_native_selector_sonya_throw_late_checkpoint_checked'",
     "OUT=ROOT/'audit_native_selector_sonya_throw_late_lifetime_checked'"),
    ("int(r['at'],16)==a+0x160 and int(r['id'])==(18 if s==1 else 17) and mask==65535 and",
     "int(r['at'],16)==a+0x160 and (int(r['id'])==(18 if s==1 else 17) or neutral_body_context(r,guest)) and mask==65535 and"),
    ("    hides=[r for r in body if r['frame']=='3028' and r['slot']=='1']",
     "    neutral=[r for r in body if r['id']=='0'];need(len(neutral)==3,'Exactly three original neutral-address callbacks, no blanket id0 acceptance')\n    a,m=owners[1]\n    hides=[r for r in body if r['frame']=='3028' and r['slot']=='1']"),
    ("actualHideStore=hide,actualMultipartSkipTests=len(skips),actualSkipFrames=80,",
     "actualHideStore=hide,trueCharacterBodyWrites=len(body)-len(neutral),neutralBoundAddressCallbacks=neutral,actualMultipartSkipTests=len(skips),actualSkipFrames=80,"),
    ("for path in (Path(__file__),Path(capture.__file__),capture.LUA,GEOMETRY,AUDIO,VIEWS,capture.OUT/'report.json',",
     "for path in (Path(__file__),SOURCE,FAILURE,Path(capture.__file__),capture.LUA,GEOMETRY,AUDIO,VIEWS,capture.OUT/'report.json',")]
for before,after in changes:
    previous.need(source.count(before)==1,'Only exact original lifetime/publication context change')
    source=source.replace(before,after,1)
scope=dict(vars(previous),__file__=__file__,SOURCE=SOURCE,FAILURE=FAILURE,neutral_body_context=neutral_body_context)
exec(compile(source,__file__+'::all_actual_callbacks_exact_native_lifetime_context','exec'),scope)
OUT=scope['OUT']
execute=scope['execute']
safe_execute=scope['safe_execute']
