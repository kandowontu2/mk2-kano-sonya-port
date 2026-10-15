"""Preserve5467 preflight; source-bind later qualified rolling-head correction.

Original900 whole art encoding plus original1014 whole head-order/new-diagonal
recipe rebuilt in RAM. Actual current death header/descriptors/pixels must
equal that intended result; no obsolete media restore or game-state writes.
"""
import inspect, json, struct, textwrap
from pathlib import Path
import current_reptile_victims_ram_v5467 as original
import verify_rolling_heads_v1014 as rolling

ROOT, need, sha = original.ROOT, original.need, original.sha
FAILED = ROOT / 'audit_v5469_current_reptile_victims_progress/progress.json'
SOURCE = ROOT / 'diagnostic_v978_owned_torso_invariant_blood/roms/mk2ks/mk2ks.mdata'


def corrected_art(guest,payload,pins):
    failed=json.loads(FAILED.read_text())
    need(not failed['passed']and failed['error']=="ValueError('Entire current descriptor independently source-PNG/donor-palette encoded')"and
         not failed['completedCases'], 'Preserved preboot old-head-order reference failure, no native capture rerun')
    source=SOURCE.read_bytes()
    need(sha(SOURCE)=='2679C041539C99F917CE1A9AAADAE455859A20DA5F5CC8AF9FB6013DB6A79F79',
         'Original immutable before-rolling-head asset source; not an old runtime replay')
    source_guest=bytearray(guest)
    source_guest[0xfaa00:0xfaa00+560]=source[0x160400:0x160400+560]
    original.independent_art(bytes(source_guest),source,pins)
    recipe=inspect.getsource(rolling.verify_payload)
    first="    artwork=ROOT/'art_native_rolling_heads_v998/sonya-diagonals-135-225-315.png'"
    last="    assert bytes(wanted)==payload,'Whole payload differs from independently reconstructed intention'"
    need(recipe.count(first)==recipe.count(last)==1,'Entire original1014 source-image head-order/diagonal recipe boundaries')
    body=textwrap.dedent(recipe[recipe.index(first):recipe.index(last)])
    function='def rebuild(source):\n'+textwrap.indent(body,'    ')+'    return bytes(wanted)\n'
    scope=dict(rolling.__dict__)
    exec(compile(function,__file__+'.whole_original1014_rolling_head_source_recipe','exec'),scope)
    expected=scope['rebuild'](source)
    need(payload[0x160000:0x180000]==expected[0x160000:0x180000],
         'Entire current native-death allocation exactly equals original source-PNG art plus qualified original1014 head-order/diagonals')
    need(guest[0xfaa00:0xfaa00+560]==expected[0x160400:0x160400+560],
         'Every actual current compiled native-death descriptor agrees with independently corrected source art')
    count=struct.unpack_from('<I',expected,0x160008)[0]
    need(49228<count<0x1c000,'Actual expanded corrected native head pixel allocation')
    reference=dict(fighters={},pixel_bytes=count,entireOriginal1014SourceRecipeSHA256=original.digest(function.encode()),
      original900All28FramesSourceEncoded=True,currentCorrectedDeathAllocationSourceExact=True)
    for fighter_index,fighter in enumerate(('kano','sonya')):
        frames=[]
        for index in range(14):
            w,h,xo,yo,graphic,command,palette,pad=struct.unpack_from('<4hIHIH',expected,0x160400+(fighter_index*14+index)*20)
            need(command==0x6000 and not pad and palette==(0xfffed000,0xfffed800)[fighter_index],
                 'Complete corrected own body/head descriptor grammar and palette')
            frames.append(dict(kind='body'if index<7 else'head',pose=index%7,size=[w,h],graphics=f'{graphic:08X}',
              descriptor=f'{0xff800000+(0xfaa00+(fighter_index*14+index)*20)*8:08X}'))
        reference['fighters'][fighter]=dict(frames=frames)
    for p in(SOURCE,FAILED,Path(original.__file__).resolve(),Path(rolling.__file__).resolve(),
             ROOT/'art_native_rolling_heads_v998/sonya-diagonals-135-225-315.png',ROOT/'mk2ks_current_reptile_ram_v5467.lua'):
        pins[str(p)]=sha(p)
    return reference,expected[0x164000:0x164000+count]


source=Path(original.__file__).read_text()
changes={
 "audit_v5468_current_reptile_victims_ram":"audit_v5471_current_reptile_victims_ram",
 "audit_v5469_current_reptile_victims_progress":"audit_v5472_current_reptile_victims_progress",
 "LUA = ROOT / 'mk2ks_current_reptile_ram_v5467.lua'":"LUA = ROOT / 'mk2ks_current_reptile_ram_v5470.lua'",
 'reference,expected_gfx=independent_art(guest,payload,pins)':'reference,expected_gfx=corrected_art(guest,payload,pins)',
 '    edits = {':"    edits = {\n      'payload[assets.PIXELS:assets.PIXELS+49228]':'payload[assets.PIXELS:assets.PIXELS+len(actual_gfx)]',",
 'independent selected source-PNG native encoding inRAM and84 effective actual record faults':
 'independent selected original900/1014 corrected head/body source-PNG native encoding inRAM and84 effective actual record faults',
}
for before,after in changes.items():
    need(source.count(before)==1,'Exact current corrected-art transport/reference adaptation: '+before)
    source=source.replace(before,after)
exec(compile(source,__file__+'.entire5467_current_original1014_corrected_art_reference','exec'),globals())
