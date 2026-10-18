"""Pin malformed native kiss reactions; completion alone is not acceptance."""
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
for file,label,stride,count in (('MKDEATH.ASM','kissed_coor_adj',16,12),('MKDIE.ASM','inflate_animations',32,16),
                                ('MKDIE.ASM','inflate_palettes',32,12),('MKDIE.ASM','pop_palettes',32,12)):
    path=SRC/file;table=source_tables(path.read_text())[label]
    bits=sum({'word':16,'long':32,'byte':8}[row['type']]*len(row['values']) for row in table['rows'])
    assert bits==stride*count
    dependencies.append(dict(file=file,label=label,entries=count,requiredTrueIDCapacity=19,
        ownEntriesMissing=True,sourceSHA256=sha(path.read_bytes())))
cases=[]
for actor,run,screenshot in ((17,'stock_kitana_kiss_kano245','kitana_kiss_05693.png'),
                             (18,'stock_kitana_kiss_sonya246','kitana_kiss_05681.png')):
    folder=BASE/run;receipt=json.loads((folder/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut']
    assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
    assert '--kitana-kiss-victim' in receipt['testArguments']
    observer=(folder/'autoboot.lua').read_text()
    assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
    assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
    with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
        for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):assert archive.read(chip)==lanes[lane]
        verify_archive_sockets(archive)
    rows=list(csv.DictReader((folder/'kitana_kiss.csv').open()))
    assert int(rows[-1]['frame'])==9000
    fight=[row for row in rows if row['mode']=='2' and row['p1char']=='4' and int(row['p2char'])==actor]
    kos=[row for previous,row in zip(fight,fight[1:]) if int(previous['p2hp'])>0 and row['p2hp']=='0']
    assert len(kos)==2
    victims=list(csv.DictReader((folder/'kitana_kiss_victim.csv').open()))
    assert victims and all(int(row['character'])==actor for row in victims)
    active=[row for row in victims if row['death']=='2'];done=[row for row in victims if row['death']=='65535']
    assert len(active)==308 and len(done)==1
    capture=folder/'snap'/screenshot;assert capture.exists()
    assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
    cases.append(dict(actor=actor,run=run,naturalKOs=2,nativeFatalityFields=308,
        nativeCompletionObserved=True,observedPaletteSelectors=sorted({int(row['palette']) for row in active}),
        capturedCorruptColorsAndBadPositionVisuallyReviewed=True,captureSHA256=sha(capture.read_bytes()),
        properOwnInflationArtVerified=False,behaviorPassed=False))
report=dict(scope='Native Kitana kiss malformed-reaction reproduction, not a passing fatality',cases=cases,
    programLaneSHA256=[sha(data) for data in lanes],shortVictimDataDependencies=dependencies,
    completionFlagDoesNotProveCompatibility=True,properOwnInflationAndBurstDataRequired=True,
    gameCodeChanged=False,kitanaKissCompatible=False,releaseReady=False,fullPortVerified=False)
(PORT/'KITANA_KISS_FAILURE_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
