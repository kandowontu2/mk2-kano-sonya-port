"""Finite process-context and cue retirement after physical Sonya Friendship."""
import csv
import hashlib
import json
from pathlib import Path
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
run=BASE/sys.argv[1]
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest().upper()
base=json.loads((run/'FINISHER_REJOIN_QUALIFICATION.json').read_text())
assert base['kind']=='friend' and base['currentFull26ROMBytesVerified']
assert base['freshCombatFields']==600 and base['ownIdentitiesPreserved']
for name,digest in base['evidenceSHA256'].items(): assert sha(Path(name))==digest
observer=PORT/'diagnostics/friend_lifecycle.lua'
assert observer.read_bytes() in (run/'autoboot.lua').read_bytes()
rows=list(csv.DictReader((run/'friend_lifecycle.csv').open()))
assert [int(row['frame']) for row in rows]==list(range(1,len(rows)+1))
active=[row for row in rows if row['death']=='7']
assert len(active)==176
assert sum(int(row['completionContexts']) for row in active)==128
assert any(row['danceContexts']=='1' for row in active)
first=int(active[0]['frame'])
completed=[row for row in rows if int(row['frame'])>first and row['death']=='65535']
assert completed and all(row['completionContexts']=='0' for row in completed)
selection=base['selectionFrame'];fresh=base['freshMatchFrame']
after=[row for row in rows if selection<=int(row['frame'])<fresh+600]
assert after and all(row['danceContexts']=='0' and row['completionContexts']=='0' for row in after)
fight=[row for row in rows if fresh<=int(row['frame'])<fresh+600]
assert len(fight)==600 and all(row['mode']=='2' for row in fight)
writes=list(csv.DictReader((run/'native_sound_writes.csv').open()))
cues=[]
for high,low in zip(writes,writes[1:]):
    command=((int(high['data'],16)&255)<<8)|(int(low['data'],16)&255)
    if 2036<=command<=2047: cues.append(int(high['frame']))
assert cues and not any(frame>=selection for frame in cues)
report=dict(scope='Observed Sonya dance-animation and completion contexts, not every possible process leak',
    run=run.name,side=base['performerSide'],completionContextFields=128,
    completionContextAbsentAfterNativeCompletion=True,
    danceContextAbsentFromSelectionThrough600FreshCombatFields=True,
    noChickenCommandsAfterSelection=True,lastChickenCommandFrame=max(cues),
    selectionFrame=selection,freshMatchFrame=fresh,
    hardwarePaletteColorComparisons=base['freshMatchPaletteColorComparisons'],
    audioTailVerified=False,allProcessLeaksExcluded=False,releaseReady=False)
paths=[run/'FINISHER_REJOIN_QUALIFICATION.json',run/'friend_lifecycle.csv',
       run/'native_sound_writes.csv',run/'autoboot.lua',observer,Path(__file__)]
paths += [BASE/'mk2-rebuild-main/srcp'/name for name in ('KSFRIEND.ASM','KSFRIEND.LST','MK2P.MAP','MAINEQU.ASM','MPROC.ASM')]
report['evidenceSHA256']={str(path):sha(path) for path in paths}
(run/'FRIEND_LIFECYCLE_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key!='evidenceSHA256'},indent=2))
