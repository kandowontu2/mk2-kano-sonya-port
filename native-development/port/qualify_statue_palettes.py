"""Compiled statue data, unchanged ordinary tint, and real palette transitions."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
from statue_palettes import build

PORT=Path(__file__).resolve().parent;SRC=PORT.parent/'baseline/mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
block,records=build()
assert (PORT/'generated_frozen/KSICEPAL.ASM').read_bytes().endswith(block)
assert (SRC/'KSICEPAL.ASM').read_bytes()==(PORT/'generated_frozen/KSICEPAL.ASM').read_bytes()
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
proof=json.loads((PORT/'SHATTER_VICTIM_QUALIFICATION.json').read_text())
assert proof['nativeShatterCompletionVerified'] and proof['programLaneSHA256']==[sha(data) for data in lanes]
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
program=bytearray(1048576);program[::2]=lanes[0];program[1::2]=lanes[1]
read_palette=lambda name:struct.unpack_from('<66H',program,(symbols[name]-0xff800000)//8)
for actor in ('kano','sonya'):
    statue=read_palette(f'ks_{actor}_statue_palette')
    assert statue[:2]==(65,0)
    assert all((color&31)==31 and (color>>5&31)>=24 and (color>>10&31)>=8 for color in statue[2:])
    # Recompute the original ordinary ice/lightning formula independently.
    primary=read_palette(f'ks_{actor}_primary_palette')
    expected=[65]
    for color in primary[1:]:
        if color==0:expected.append(0);continue
        luma=((color>>10&31)*3+(color>>5&31)*6+(color&31))//10
        expected.append(((luma*20//31)<<10)|((luma*27//31)<<5)|(8+luma*23//31))
    assert read_palette(f'ks_{actor}_frozen_palette')==tuple(expected)
cases=[]
for case in proof['cases']:
    folder=PORT.parent/'baseline'/case['run']
    rows=list(csv.DictReader((folder/'superfreeze_victim.csv').open()))
    frozen=[row for row in rows if row['action']=='1558']
    final=frozen[-50:]
    assert len({row['palette'] for row in final})==1
    statue_selector=final[0]['palette']
    assert statue_selector!=rows[0]['palette']
    assert len({row['palette'] for row in frozen[:56]})==2
    assert statue_selector not in {row['palette'] for row in frozen[:56]}
    legs=[row for row in rows if row['shape']==case['ownLegs']]
    assert legs and all(row['palette']==statue_selector for row in legs)
    cases.append(dict(actor=case['actor'],run=case['run'],side=case['victimSide'],
        distinctStatuePaletteObserved=True,ownLegsUseSameStatuePalette=True))
regressions=[]
for filename,key in (('FROZEN_VICTIM_QUALIFICATION.json','frozenVictimBehaviorVerified'),
                     ('LIGHTNING_VICTIM_QUALIFICATION.json','lightningVictimBehaviorVerified')):
    path=PORT/filename
    record=json.loads(path.read_text())
    assert record['programLaneSHA256']==proof['programLaneSHA256']
    assert record[key] and record['mirroredSidesVerified']
    assert {(case['actor'],case['victimSide']) for case in record['cases']}=={(17,1),(17,2),(18,1),(18,2)}
    regressions.append(dict(report=filename,reportSHA256=sha(path.read_bytes()),cases=record['cases']))
report=dict(scope='Separate own-index statue palettes and physical freeze/shatter transitions',cases=cases,
    actors=records,programLaneSHA256=[sha(data) for data in lanes],
    compiledStatuePalettesVerified=True,ordinaryFrozenPaletteBytesUnchanged=True,
    nativeShatterCompletionVerified=True,mirroredSidesVerified=True,
    capturedCyanWhiteTreatmentReviewed=True,pixelPerfectCrystallineArtworkAccepted=False,
    ordinaryFreezeLightningRuntimeRegressionVerified=True,regressionReports=regressions,
    releaseReady=False,fullPortVerified=False)
(PORT/'STATUE_PALETTE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
