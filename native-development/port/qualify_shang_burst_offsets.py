"""Before/after physical-input body-entry coordinate proof, not full visual QA."""
import csv
import json
import re
import zipfile
from pathlib import Path
from build_inflation_assets import sha
from current_graphics import verify_archive_sockets
from shang_burst_source import NEW
from inventory_character_tables import source_tables

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
SRC=BASE/'mk2-rebuild-main/srcp'
assert NEW in (SRC/'MKDEATH.ASM').read_text()
table=source_tables((SRC/'MKDEATH.ASM').read_text())['burst_distance_offset']
assert all(r['type']=='word' for r in table['rows'])
assert sum(len(r['values']) for r in table['rows'])==24
with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as original:
    key=next(n for n in original.namelist() if n.lower().endswith('/src/mkdeath.asm'))
    old=source_tables(original.read(key).decode('cp437'))['burst_distance_offset']
    assert [(r['type'],r['values']) for r in old['rows']]==[(r['type'],r['values']) for r in table['rows']]
symbols={n:int(a,16) for a,n in re.findall(r'\b([0-9a-fA-F]{8})\s+([A-Za-z_]\w*)',(SRC/'MK2P.MAP').read_text())}
lanes=[b''.join((SRC/f'rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC')) for lane in range(2)]
cases=[]
for actor,label,old_name,new_name in ((17,'kano','stock_shang_burst_kano271','stock_shang_offset_kano273'),
                                     (18,'sonya','stock_shang_burst_sonya272','stock_shang_offset_sonya274'),
                                     (17,'kano',None,'stock_shang_mirror_kano275'),
                                     (18,'sonya',None,'stock_shang_mirror_sonya276'),
                                     (1,'liu',None,'stock_shang_control_liu277'),
                                     (4,'kitana',None,'stock_shang_control_kitana278')):
    for before,name in (((True,old_name),(False,new_name)) if old_name else ((False,new_name),)):
        folder=BASE/name
        receipt=json.loads((folder/'execution.json').read_text())
        assert receipt['exitCode']==0 and not receipt['timedOut']
        assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
        assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
        observer=(folder/'autoboot.lua').read_text()
        assert ':write_u' not in observer and not re.search(r'\.value\s*=(?!=)',observer)
        assert sha((folder/'autoboot.lua').read_bytes())==receipt['controllerSHA256']
        with zipfile.ZipFile(folder/'roms/mk3.zip') as archive:
            verify_archive_sockets(archive)
            archive_lanes=[archive.read(chip) for chip in ('mk321u54.bin','mk321u63.bin')]
            if not before:assert archive_lanes==lanes
            else:assert [sha(v) for v in archive_lanes]==[
                'BF790FA54799DC404526D46A17875D3FECF7AFFC511F328C516B19B328531162',
                'C9FDD75F91DC53C92F012497C145B2827EC6D1D3FBCBCE590162123484D6F4E5']
        with (folder/'shangburst.csv').open() as stream:rows=list(csv.DictReader(stream))
        assert int(rows[-1]['frame'])==9000
        assert all(r['missing']=='0' for r in rows)
        side=1 if '--mirror' in receipt['testArguments'] else 2
        fight=[r for r in rows if r['mode']=='2' and r[f'p{3-side}char']=='6' and int(r[f'p{side}char'])==actor]
        assert len([b for a,b in zip(fight,fight[1:]) if int(a[f'p{side}hp'])>0 and b[f'p{side}hp']=='0'])==2
        active=[r for r in fight if r['death']=='2']
        if actor in (17,18):assert len(active)==228
        else:assert 200<=len(active)<=300
        bad=sum(int(r[f'p{3-side}y'])>512 for r in active)
        if before:assert bad>100
        else:
            assert bad==0
            assert all(int(r['pc'],16)!=symbols['illegal_opcode']+0x50 for r in rows)
        with (folder/'shangburst_victim.csv').open() as stream:victims=list(csv.DictReader(stream))
        assert victims[-1]['death']=='65535' and all(int(r['character'])==actor for r in victims)
        if not before and actor in (17,18):
            for phase in (0,5):
                assert any(int(r['shape'],16)==symbols[f'ks_inf_{label}_pose{phase}'] for r in victims)
            dx,dy=(95,16) if actor==17 else (88,13)
            lineups=[r for r in active
                     if int(r[f'p{3-side}y'])==int(r[f'p{side}y'])+dy
                     and abs(int(r[f'p{3-side}x'])-int(r[f'p{side}x']))==dx]
            assert lineups, 'No runtime application of the intended own offset'
        assert '[LUA ERROR]' not in (folder/'mame.log').read_text()
        if actor not in (17,18):
            own_shapes={v for k,v in symbols.items() if k.startswith('ks_inf_') and '_pose' in k}
            assert all(int(r['shape'],16) not in own_shapes for r in victims)
            assert any(int(r['flags'])&0x20 for r in victims)
        cases.append(dict(actor=actor,run=name,victimSide=side,beforeFix=before,naturalKOs=2,fields=9000,
            nativeFatalityFields=len(active),invalidAttackerYRows=bad,nativeCompletionObserved=True,
            traceSHA256=sha((folder/'shangburst.csv').read_bytes())))
report=dict(scope='Shang body-entry coordinate regression, both own sides and representative original controls',
    programLaneSHA256=[sha(v) for v in lanes],cases=cases,originalTwelveRowsPreserved=True,
    ownInflationAndPopPointersObserved=True,invalidCoordinateRegressionFixed=True,
    mirroredSidesVerified=all({c['victimSide'] for c in cases if not c['beforeFix'] and c['actor']==actor}=={1,2} for actor in (17,18)),
    representativeOriginalRuntimeControlsVerified={c['actor'] for c in cases if c['actor'] in (1,4)}=={1,4},
    allOriginalCharactersVerified=False,
    exactFaceEntryAlignmentAccepted=False,cleanRebuildCurrentLinkVerified=False,releaseReady=False)
(PORT/'SHANG_BURST_OFFSET_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
