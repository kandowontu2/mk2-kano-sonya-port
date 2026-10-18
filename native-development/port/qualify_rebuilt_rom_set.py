"""Compare all26 independently rebuilt/copied chips to an actual stock-MAME run."""
import hashlib
import json
from pathlib import Path
import zipfile
import sys

PORT=Path(__file__).resolve().parent
BASE=PORT.parent/'baseline'
CLEAN=BASE/'clean_program'
ROOT=PORT.parents[1]
sha=lambda b:hashlib.sha256(b).hexdigest().upper()
program=json.loads((PORT/'CLEAN_PROGRAM_QUALIFICATION.json').read_text())
sound=json.loads((PORT/'CLEAN_SOUND_QUALIFICATION.json').read_text())
prior_graphics=json.loads((PORT/'OWN_VICTIM_GRAPHICS_REBUILD.json').read_text())
assert prior_graphics['priorReportSHA256']==sha((PORT/'FINAL_GRAPHICS_REBUILD.json').read_bytes())
split_graphics=json.loads((PORT/'SPLIT_GRAPHICS_REBUILD.json').read_text())
assert split_graphics['priorReportSHA256']==sha((PORT/'OWN_VICTIM_GRAPHICS_REBUILD.json').read_bytes())
graphics=json.loads((PORT/'MORPH_GRAPHICS_REBUILD.json').read_text())
assert graphics['priorReportSHA256']==sha((PORT/'SPLIT_GRAPHICS_REBUILD.json').read_bytes())
assert program['cleanProgramRebuildByteIdentical'] and sound['cleanSoundRebuildByteIdentical']
assert graphics['independentAddedBankChainVerified']
ending_graphics=json.loads((PORT/'ENDING_ART_REBUILD_QUALIFICATION.json').read_text())
assert ending_graphics['priorReportSHA256']==sha((PORT/'MORPH_GRAPHICS_REBUILD.json').read_bytes())
assert ending_graphics['independentAddedBankChainVerified']
chips={}
for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
    parts=[]
    for part in ('F8','FC'):
        name=f'P12{part}.{lane}';data=(CLEAN/'srcp/rom'/name).read_bytes()
        assert sha(data)==next(item['SHA256'] for item in program['programROMs'] if item['file']==name)
        parts.append(data)
    chips[chip]=b''.join(parts)
for i in range(2,6):
    name=f'U{i}.ROM';data=(CLEAN/'soundp'/name).read_bytes()
    assert sha(data)==next(item['SHA256'] for item in sound['soundROMs'] if item['file']==name)
    chips[f'l1_mortal_kombat_3_u{i}_music_spch.u{i}']=data
prefix=(CLEAN/'graphics_chain'/graphics['finalPackedRelativePath']).read_bytes()
assert sha(prefix)==graphics['finalAddedBankSHA256']
packed=(CLEAN/'graphics_chain'/ending_graphics['finalPackedRelativePath']).read_bytes()
assert packed.startswith(prefix) and sha(packed)==ending_graphics['finalAddedBankSHA256']
region=packed+bytes(0x600000-len(packed))
for bank,size in ((0,0x100000),(1,0x80000)):
    for lane in range(4):
        chip=121-bank*4-lane;start=bank*0x400000+lane
        chips[f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}']=region[start:start+size*4:4]
with zipfile.ZipFile(ROOT/'roms/mk2.zip') as mk2:
    for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
        for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
            data=mk2.read(f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}')
            assert len(data)==1048576
            chip=133-bank*4-lane
            chips[f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}']=data
assert len(chips)==26
assert len(sys.argv)<=2
run_name=sys.argv[1] if len(sys.argv)==2 else 'stock_wolf_game358'
assert Path(run_name).name==run_name
run=BASE/run_name
receipt=json.loads((run/'execution.json').read_text())
assert receipt['exitCode']==0 and not receipt['timedOut']
assert not receipt['customDriver'] and not receipt['gameMemoryWrites']
assert receipt['emulatorSHA256']=='AF6966108D9B52C22465C6D50F4E5D50CC371B50F2D27DC443935F287AAD37A3'
assert set(chips)==set(receipt['replacementChips'])
with zipfile.ZipFile(run/'roms/mk3.zip') as archive:
    # Input archive also retains nested alternate-revision chips. Stock mk3
    # uses these26 root entries, not those unrelated clone subdirectories.
    assert {name for name in archive.namelist() if '/' not in name}==set(chips)
    unused_clone_entries=[name for name in archive.namelist() if '/' in name]
    assert all(name.startswith(('mk3r20/','mk3r10/','mk3p40/')) for name in unused_clone_entries)
    for name,data in chips.items():
        assert sha(data)==receipt['replacementChips'][name]
        assert data==archive.read(name),name
report=dict(scope='All26 rebuilt/copied native ROM chips compared to actual stock-MAME test input',
    runtimeReference=run_name,chipsVerified=26,
    programCleanRebuildByteIdentical=True,soundCleanRebuildByteIdentical=True,
    addedGraphicsChainRebuiltByteIdentical=True,originalMK2GraphicsSocketsCopiedUnchanged=12,
    allRebuiltROMBytesMatchRuntimeInput=True,
    unusedNestedAlternateRevisionEntries=unused_clone_entries,
    chipSHA256={name:sha(data) for name,data in chips.items()},
    fullGameplayAcceptance=False,sourceAssetLicenseReviewComplete=False,releaseReady=False)
(PORT/'REBUILT_ROM_SET_QUALIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:value for key,value in report.items() if key!='chipSHA256'},indent=2))
