"""Pin real arm-rip crashes and all known short victim-data dependencies."""
import csv
import hashlib
import json
from pathlib import Path
import re
import zipfile
from inventory_character_tables import source_tables
from current_graphics import verify_archive_sockets

PORT=Path(__file__).resolve().parent;BASE=PORT.parent/'baseline';SRC=BASE/'mk2-rebuild-main/srcp'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
dependencies=[]
for file,label,expected in (('MKDEATH.ASM','arm_ripped_adjust',16),('MKDEATH.ASM','ochar_flyin_arms',12),
                            ('MKDIE.ASM','ochar_arm_ripped_ani',16),('MKBLOOD.ASM','arm_flow_lineups',16),
                            ('MKBLOOD.ASM','left_gush_lineups',12),('MKBLOOD.ASM','right_gush_lineups',12)):
    path=SRC/file;table=source_tables(path.read_text())[label]
    bits=sum({'word':16,'long':32,'byte':8}[row['type']]*len(row['values']) for row in table['rows'])
    assert bits==expected*32
    dependencies.append(dict(file=file,label=label,sourceSHA256=sha(path.read_bytes()),
        entries=bits//32,requiredTrueIDCapacity=19,ownEntriesAbsent=True))
cases=[]
for actor,run in ((17,'stock_arms_kano215'),(18,'stock_arms_sonya216')):
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--arms-victim' in receipt['testArguments']
    observer=(folder/'autoboot.lua').read_text()
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert "if m.devices[':maincpu'].state['PC'].value==recovery then" in observer
    assert "io.open(kind..'_fault.txt','w')" in observer
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'arms.csv').open()))
    fight=[row for row in rows if row['mode']=='2' and row['p1char']=='11' and int(row['p2char'])==actor]
    kos=[row for previous,row in zip(fight,fight[1:]) if int(previous['p2hp'])>0 and row['p2hp']=='0']
    assert len(kos)==2
    assert int(rows[-1]['frame'])<9000 and fight[-1]['death']=='2'
    fault=folder/'arms_fault.txt';assert fault.exists() and 'SP=' in fault.read_text()
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,naturalKOs=2,terminalFrame=int(rows[-1]['frame']),
        nativeArmRipInitiated=True,illegalRecoveryFaultDump=True,faultSHA256=sha(fault.read_bytes()),
        allTraceMissingMarkersZero=all(row['missing']=='0' for row in rows),behaviorPassed=False))
report=dict(scope='Physical Jax arm-rip crash reproduction, not a fix or passing test',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],shortVictimDataDependencies=dependencies,
    missingMarkerDidNotDetectCrash=True,properOwnArmlessBodyAndDetachedArmAssetsRequired=True,
    allDependenciesEnumerated=False,gameCodeChanged=False,armRipCompatible=False,
    releaseReady=False,fullPortVerified=False)
(PORT/'ARM_RIP_FAILURE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
