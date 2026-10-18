"""Preserve explicitly timed-out campaign evidence, never produce a full pass."""
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from campaign_rounds import split_rounds,native_round_wins,completed_native_matches
from native_roster import verified_names

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
assert len(sys.argv)==2 and Path(sys.argv[1]).name==sys.argv[1]
folder=BASE/sys.argv[1]
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
receipt=json.loads((folder/'execution.json').read_text())
assert receipt['timedOut'] and receipt['exitCode'] is None
assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
frozen=(folder/'autoboot.lua').read_bytes()
assert sha(frozen)==receipt['controllerSHA256']
assert b':write_u' not in frozen and not re.search(rb'\.value\s*=(?!=)',frozen)
rebuilt=json.loads((PORT/'REBUILT_ROM_SET_QUALIFICATION.json').read_text())
assert rebuilt['allRebuiltROMBytesMatchRuntimeInput']
assert receipt['replacementChips']==rebuilt['chipSHA256']
with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
    for name,digest in receipt['replacementChips'].items():assert sha(archive.read(name))==digest,name
raw=list(csv.DictReader((folder/'campaign.csv').open()))
incomplete=[index for index,row in enumerate(raw) if any(value is None for value in row.values())]
assert incomplete in ([],[len(raw)-1]),'Only an interrupted final CSV row may be incomplete'
rows=raw[:-1] if incomplete else raw
assert rows and max(int(row['missing']) for row in rows)==0
assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
target=18 if '--sonya' in receipt['testArguments'] else 17
fight=[row for row in rows if row['mode']=='2']
assert fight and all(int(row['p1char'])==target and int(row['p1selected'])==target for row in fight)
symbols={name:int(address,16) for address,name in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',
    (BASE/'mk2-rebuild-main/srcp/MK2P.MAP').read_text())}
assert not any(int(row['pc'],16)==symbols['illegal_opcode']+0x50 for row in rows)
rounds=split_rounds(fight)
wins=native_round_wins(rows,rounds)
matches=completed_native_matches(wins)
advanced=[match for match in matches if any(int(row['map'])>match['map'] for row in rows)]
names=verified_names(include_nonselectable=True)
for match in advanced:match['opponentName']=names.get(match['opponent'],'UNKNOWN')
events=list(csv.DictReader((folder/'campaign_continues.csv').open()))
report=dict(scope='Timed-out partial observation, not a completed test',
    timedOut=True,completedTest=False,fullCampaignVerified=False,fullPortVerified=False,releaseReady=False,
    lastCompleteFrame=int(rows[-1]['frame']),incompleteFinalRowsExcluded=len(incomplete),
    lastMode=int(rows[-1]['mode']),maxMapPosition=max(int(row['map']) for row in rows),
    verifiedCurrentROMChips=26,actor=target,nativeWinningRounds=wins,
    naturallyDefeatedAndAdvanced=advanced,
    paidBuyinsObserved=sum(event['phase']=='buyin' for event in events),
    paidContinuedCombatsStarted=sum(event['phase']=='combat' for event in events),
    missingMarkersInRecordedRows=0,recoveryPCObservedInRecordedRows=False,
    hostWallLimitSeconds=receipt.get('wallTimeoutSeconds'),
    traceSHA256=sha((folder/'campaign.csv').read_bytes()),controllerSHA256=sha(frozen))
(folder/'CAMPAIGN_PARTIAL_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key not in ('nativeWinningRounds',)},indent=2))
