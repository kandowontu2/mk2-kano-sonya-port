"""Pin activated vertical-split failures, distinct from command-range failures."""
import csv
import json
import re
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
table=source_tables((SRC/'MKDEATH.ASM').read_text())['split_in_2_tab']
assert all(r['type']=='long' for r in table['rows'])
assert sum(len(r['values']) for r in table['rows'])==17
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
cases=[]
for actor,name,last in ((17,'stock_lao_split_range_kano295',5202),(18,'stock_lao_split_range_sonya296',5950)):
    folder=BASE/name
    receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    with (folder/'laosplit.csv').open() as stream:rows=list(csv.DictReader(stream))
    assert int(rows[-1]['frame'])==last<9000
    fight=[r for r in rows if r['mode']=='2' and r['p1char']=='0' and int(r['p2char'])==actor]
    assert len([b for a,b in zip(fight,fight[1:]) if int(a['p2hp'])>0 and b['p2hp']=='0'])==2
    active=[r for r in fight if r['death']=='1']
    assert len(active)==77
    distance=abs(int(active[0]['p2x'])-int(active[0]['p1x']))
    assert distance==113 and 96<=distance<=128
    with (folder/'laosplit_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
    assert victims and all(int(r['character'])==actor for r in victims)
    assert not any(r['death']=='65535' for r in victims)
    invalid_pc=[r for r in rows if not 0xff800000<=int(r['pc'],16)<=0xffffffff]
    if actor==18:assert invalid_pc
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=name,naturalKOs=2,activationDistance=distance,
        nativeFatalityFieldsObserved=77,lastTelemetryFrame=last,
        outsideProgramPCObservations=len(invalid_pc),completionObserved=False,
        mainTraceSHA256=sha((folder/'laosplit.csv').read_bytes()),behaviorPassed=False))
report=dict(scope='Kung Lao vertical-split missing own victim data reproduction',cases=cases,
    programLaneSHA256=[sha(v) for v in lanes],sourceTableEntries=17,requiredTrueIDCapacity=19,
    trials293And294DidNotActivateAndAreExcluded=True,
    originalNativeDistanceGateUnchanged=True,gameCodeChanged=False,
    bothOwnBodyHalvesRequired=True,lateRenderingDoesNotExplainCorruptState=True,
    verticalSplitCompatible=False,releaseReady=False)
(PORT/'LAO_SPLIT_FAILURE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
