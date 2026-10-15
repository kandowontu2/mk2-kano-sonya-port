"""Bind the existing typed Friendship palette-release hook before native reset.

Preserve the rejected blanket stock-entry assertion. The current game already
routes FF83F060 through its narrow owned-bubble palette release, restores all
registers/status, replays the stolen prefix, then returns to original FF83F0A0.
Actual full free-pool membership remains independently observed, not inferred.
"""
import struct
from pathlib import Path
import qualify_native_selector_sonya_death_raw_pool as failed

ROOT=failed.ROOT
SOURCE=Path(failed.__file__)
FAILURE=failed.OUT/'failure.json'


def hook_gate(guest):
    def words(at,values):
        data=struct.pack('<'+'H'*len(values),*values)
        offset=(at-0xff800000)//8
        failed.need(guest[offset:offset+len(data)]==data,'Exact existing typed owned-palette reset hook, including all native register/status restoration')
    words(0xff83f060,(0xc080,0x3000,0xfffe,0x0300))
    # Independently transcribed from canonical midtunit_m.cpp emitter6408..6449:
    # save ST/A0-A14; traverse actual render list; filter only owned bubble
    # pose-range/palette; native release; restore; stolen prefix; stock reset.
    words(0xfffe3000,(0x01e0,0x098f,0xfffe,0x07a8,0xd480,0x0105,0x4d08,0xca80,0x3370,0xfffe,
        0xb702,0x01d0,0x0b62,0xd9ef,0x0162,0xc480,0x3330,0xfffe,0x0b62,0xd86f,0x0162,0xc780,0x3330,0xfffe,
        0xb500,0x0140,0x0b80,0xff00,0xffff,0x4c01,0x24c1,0x0b21,0xbb30,0x0105,0x8620,
        0x0b60,0xd7ff,0x0100,0xcb80,0x3330,0xfffe,0xb420,0x0020,0xc680,0x3330,0xfffe,
        0xb500,0x0140,0x0d5f,0xd580,0xff80,0x8708,0xc080,0x3060,0xfffe,
        0x09af,0x7fff,0x01c0,0x5600,0x0580,0x19f0,0x0106,0xc080,0xf0a0,0xff83))


source=SOURCE.read_text()
changes=[
 ("OUT=ROOT/'audit_native_selector_sonya_death_raw_pool_checked'","OUT=ROOT/'audit_native_selector_sonya_death_raw_pool_owned_reset_checked'"),
 ("    previous.source_gate(guest)","    previous.source_gate(guest)\n    hook_gate(guest)"),
 ("((0xff83f060,0xff83f210),(0xff8090b0,0xff809270))","((0xff83f0a0,0xff83f210),(0xff8090b0,0xff809270))"),
 ("((enter,0xff83f060,0x5600),(done,0xff83f200,0x0960))","((enter,0xff83f060,0xc080),(done,0xff83f200,0x0960))"),
 ("for p in (Path(__file__),previous.OUT/'report.json'","for p in (Path(__file__),SOURCE,FAILURE,previous.OUT/'report.json'")]
for before,after in changes:
    failed.need(source.count(before)==1,'Only exact typed native reset-source binding changes')
    source=source.replace(before,after,1)
scope=dict(vars(failed),__file__=__file__,SOURCE=SOURCE,FAILURE=FAILURE,hook_gate=hook_gate)
exec(compile(source,__file__+'::actual_existing_palette_hook_then_original_reset','exec'),scope)
OUT,gate,execute,safe_execute=(scope[k] for k in ('OUT','gate','execute','safe_execute'))
