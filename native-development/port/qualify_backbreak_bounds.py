"""Check table bounds only. Missing back-break art intentionally rejects gameplay."""
import csv
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main/srcp'
old=source_tables((BASE/'mk2-rebuild-main/srcw/MKSLAM.ASM').read_text())['back_break_adjusts']
new=source_tables((BUILD/'MKSLAM.ASM').read_text())['back_break_adjusts']
oldvalues=[v for row in old['rows'] for v in row['values']]
newvalues=[v for row in new['rows'] for v in row['values']]
assert len(oldvalues)==34 and len(newvalues)==38 and newvalues[:34]==oldvalues
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(BUILD/'MK2P.MAP').read_text())}
lanes=[b''.join((BUILD/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in (0,1)]
program=bytearray(0x100000);program[::2]=lanes[0];program[1::2]=lanes[1]
offset=(symbols['back_break_adjusts']-0xff800000)//8
assert struct.unpack_from('<4h',program,offset+17*4)==(10,-75,10,-75)
def signed(value):
    value=int(value)
    return value-65536 if value>=32768 else value
for argument in sys.argv[1:]:
    folder=BASE/argument
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        assert hashlib.sha256(lanes[lane]).hexdigest().upper()==receipt['replacementChips'][chip]
    issue=json.loads((folder/'backbreak_missing.json').read_text())
    victim=18 if '--sonya' in receipt['testArguments'] else 17
    assert issue['tag']==63 and issue['actor']==victim and issue['attackerAction']==0x109
    rows=list(csv.DictReader((folder/'backbreak.csv').open()))
    last=rows[-1]
    assert int(last['p1char'])==11 and int(last['p2char'])==victim
    assert int(last['p2x'])-int(last['p1x'])==10
    assert signed(last['victimY'])-signed(last['ownerY'])==-75
    assert all(int(r['missing'])==0 for r in rows[:-1]) and int(last['missing'])==1
    result={'alignmentIndexBoundsVerified':True,'original17SlotsPreserved':True,
            'victimID':victim,'nativeBackbreakActivated':True,'relativeXY':[10,-75],
            'missingMain3fStillObserved':True,'backbreakGameplayVerified':False,'fullPortVerified':False}
    (folder/'backbreak_bounds_qualification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
