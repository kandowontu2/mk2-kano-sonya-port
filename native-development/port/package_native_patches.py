"""Produce a DEVELOPMENT-only native IPS/source snapshot, never ROM archives."""
import difflib
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import zipfile
from current_graphics import graphics_metadata,graphics_directory
from ips_codec import create_patch,apply_patch
from patch_native_roms import read_chip,build

PORT=Path(__file__).resolve().parent
ROOT=PORT.parents[1]
BASE=PORT.parent/'baseline'
BUILD=BASE/'mk2-rebuild-main'
OUT=PORT/'development_patches'
PACKAGE=OUT/'MK2KS_NATIVE_DEVELOPMENT'
sha=lambda data:hashlib.sha256(data).hexdigest().upper()

README='''MKII KANO / SONYA - NATIVE ROM DEVELOPMENT CANDIDATE
NOT A FINISHED RELEASE. Do not confuse this with the withdrawn custom-driver build.

This contains classic per-chip IPS patches, hash checks, readable authored ASM,
native-source diffs and patching scripts. It contains NO complete ROM archive,
custom MAME executable, driver patch, host samples or proprietary compiler.

REQUIRES
  Your own MKII ROM archive and MK3 revision2.1 ROM archive matching the per-chip
  SHA256 hashes in PATCH_MANIFEST.json. ZIP container hashes/names need not match;
  chip bytes and internal filenames must. Python3.10+ (standard library only for
  patching). Unmodified stock MAME: tested with Windows x64 MAME0.289.

PATCH ON WINDOWS
  Extract this package to its own writable folder. Do not run inside the ZIP.
  From Command Prompt:
    PATCH.cmd "C:\\path\\mk2.zip" "C:\\path\\mk3.zip"
  Or on any OS:
    python patch_native_roms.py --mk2 /path/mk2.zip --mk3 /path/mk3.zip --output roms/mk3.zip
  All chips/patches/results are checked before output creation. Existing output
  is never overwritten. Original input archives are never modified.

PLAY
  PLAY.cmd "C:\\path\\to\\stock\\mame.exe"
  Or put your stock mame.exe beside PLAY.cmd, then double-click PLAY.cmd.
  Command on any platform:
    mame mk3 -rompath ./roms
  This native Wolf build uses MAME's existing mk3 hardware/socket definition.
  It is MKII game code, not MK3 gameplay. Run from this isolated folder so this
  candidate does not replace your normal MK3 ROM set or configuration.
  Stock MAME reports checksum warnings because patched ROM hashes differ from
  retail MK3. Those are expected; no emulator hash/driver spoofing is supplied.

WHAT THE PATCHER DOES
  Program: two compiled native TMS34010 lanes, assembled from proper ASM.
  Graphics: maps twelve original MKII chips to the Wolf sockets, then applies
  eight IPS patches for the added native graphics bank. No runtime DMA hacks.
  Sound: four IPS patches produce the current native Wolf DCS ROM images.
  Source program/sound/added-graphics bases come from your MK3 archive; unchanged
  original graphics come from your MKII archive. Never patch the ZIP file itself.
  Manual application: for each manifest operation=ips, extract its source chip,
  apply the named IPS, check targetSHA256 and rename to target. For operation=copy,
  copy the named chip without editing it. ZIP exactly those26 target entries.

SOURCE SNAPSHOT
  source/asm: current authored/generated own ASM modules actually linked.
  source/native_source.patch: byte-preserving8-bit diffs against the supplied
  mk2-rebuild source's src files (a/src/... -> b/src/...). Normalize CRLF line
  endings to LF without character-set conversion before applying with git apply.
  No complete proprietary source tree is included.
  source/PBUILD.BAT and source/MK2NEWW.CMD document the current native build route.
  The proprietary rebuild input, TI tools and original ROMs are not included.
  Independent program, sound and added-graphics rebuilds match the tested ROM
  bytes. This snapshot alone is not a standalone rebuild kit: it still requires
  the original proprietary inputs/tools, which are not redistributed here.

MOVELIST
  MOVELIST_NATIVE.txt includes Kano/Sonya specials, fatalities, stage finishers,
  Friendships, Babalities and the two added Shang Tsung morph commands.

KNOWN OPEN GATES
  This2219 candidate fixes detached-leg grounding in native MKDEATH ASM at four
  consumers, applying only to true IDs17/18. Twelve current Cage/Scorpion/Sub-Zero
  victim cases and an independent130-object byte-identical clean rebuild pass.
  No shared artwork, normal-body pivot, driver or game-balance change is used.
  Current2219 finite checks cover all eight specials, four lethal finishers,
  Friendship/Babality eligibility, stage finishers and transformed specials/
  lethal finishers on both player sides, including tested fresh-match recovery.
  Earned lethal victim coverage now passes112 cases: all four added fatalities,
  all14 selectable victims, both player sides, including same-character matches.
  Independent exact-coverage/hash audits verify native completion and600 fresh
  combat fields with hardware palette restoration for every case. This does
  not certify every interruption, edge, CPU behaviour or audio overlap.
  Normal/proximity contact checks cover136 finite cases:17 actual actions,
  both added characters/player sides, hit and appropriate block, native damage
  and recovery. These do not certify arbitrary ranges, victims or every frame.
  Own ingestion, arm-rip, inflation/burst, split and Raiden-head reactions have
  current runtime checks and separately documented sampled visual reviews.
  Representative original Liu/Kitana controls pass; remaining original-roster/
  Goro/edge coverage is not inferred. Older broad6AE0 evidence remains historical
  unless a current2219 check is explicitly identified here.
  All six native ladder maps now include Kano and Sonya as real opponents,
  without replacing an original fighter. Linked roster/geometry/secret/boss
  tables and the initial portrait pan are checked. One earned Sonya route
  reaches and defeats both added opponents; all six maps are not runtime-tested.
  Current2219 native/control cue checks,41 independent isolated chicken-tail
  windows and a three-track native mix comparison pass. These are finite sound
  checks, not exact full-scene audio-sync/every-overlap acceptance. Nonlethal
  lifecycle and fresh-match recovery checks also pass on the current build.
  Kano/Sonya have source-linked two-page own-photo endings and a native cast
  pair. An earned current2219 Sonya route displays her two pages, the added cast pair,
  sampled native credits and attract return. Named pixel checks support
  observed page stability, not every-field or full audiovisual acceptance.
  Kano's earned ending remains unverified.
  Finite stock-MAME checks cover all eight specials and four lethal finishers
  while Shang is morphed into Kano/Sonya, on both player sides. This does not
  certify every victim, interruption, edge or audio path. Native punch-history
  restrictions still apply to transformed nonlethals; see the movelist.
  Native own-ID CPU reaction and boss projectile classification fixes are
  included. On current2219 Sonya naturally clears both bosses and her ending.
  Kano has earned matches against all14 human opponents across paid continues,
  but his boss match clear/earned ending remain unverified. This is not full-port
  completion. No test controller edits AI, difficulty, health, damage or results.
  Remaining campaign and broad opponent/edge/interruption/AI verification;
  remaining native audio and final visual acceptance; final release validation.
  Existing finite tests are not a claim that all gameplay is complete.
  This package is for development/testing only, not the final GitHub release.
'''

def write_package_zip(destination,files):
    """Replace only after a complete sibling candidate has passed ZIP checks."""
    candidate=destination.with_name(destination.stem+'.candidate.zip')
    assert not candidate.exists(),'Inspect an unfinished ZIP candidate before retrying'
    with zipfile.ZipFile(candidate,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
        for name,data in sorted(files.items()):
            entry=zipfile.ZipInfo('MK2KS_NATIVE_DEVELOPMENT/'+name,date_time=(2026,1,1,0,0,0))
            entry.compress_type=zipfile.ZIP_DEFLATED;archive.writestr(entry,data)
    with zipfile.ZipFile(candidate) as archive:
        assert archive.testzip() is None
        assert not any(name.lower().endswith(('.exe','.bin','.rom','.u2','.u3','.u4','.u5')) for name in archive.namelist())
        assert all(archive.read('MK2KS_NATIVE_DEVELOPMENT/'+name)==data for name,data in files.items())
    candidate.replace(destination)

def main():
    runtime_args=[arg.split('=',1)[1] for arg in sys.argv[1:] if arg.startswith('--runtime-run=')]
    assert len(runtime_args)==1,'Pass exactly one --runtime-run=NAME for the current tested ROM'
    runtime_name=runtime_args[0]
    assert runtime_name and Path(runtime_name).name==runtime_name and '/' not in runtime_name and '\\' not in runtime_name
    if OUT.exists():
        assert '--refresh-generated' in sys.argv, 'Never overwrite a generated patch candidate implicitly'
        previous=json.loads((OUT/'PACKAGING_VERIFICATION.json').read_text())
        assert sha((OUT/'MK2KS_NATIVE_DEVELOPMENT_IPS.zip').read_bytes())==previous['SHA256']
        pins=json.loads((PACKAGE/'FILES.json').read_text())
        assert all(sha((PACKAGE/name).read_bytes())==digest for name,digest in pins.items()), 'Generated candidate was edited'
    graphics=graphics_metadata()
    targets={}
    sources={}
    for lane,chip in enumerate(('mk321u54.bin','mk321u63.bin')):
        targets[chip]=b''.join((BUILD/f'srcp/rom/P12{part}.{lane}').read_bytes() for part in ('F8','FC'))
        sources[chip]=('mk3',chip)
    with zipfile.ZipFile(ROOT/'roms/mk2.zip') as mk2:
        for bank,(first,second) in enumerate(((14,19),(16,20),(17,22))):
            for lane,(letter,socket) in enumerate((('ug',first),('uj',first),('ug',second),('uj',second))):
                source=f'l1_mortal_kombat_ii_game_rom_{letter}{socket}.{letter}{socket}'
                chip=f'l1_mortal_kombat_3_u{133-bank*4-lane}_game_rom.u{133-bank*4-lane}'
                targets[chip]=read_chip(mk2,source);sources[chip]=('mk2',source)
    for chip in range(114,122):
        name=f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}'
        targets[name]=(graphics_directory()/name).read_bytes()
        assert sha(targets[name])==graphics['sockets'][name]
        sources[name]=('mk3',name)
    for chip in range(2,6):
        name=f'l1_mortal_kombat_3_u{chip}_music_spch.u{chip}'
        targets[name]=(BUILD/f'soundp/U{chip}.ROM').read_bytes();sources[name]=('mk3',name)
    assert len(targets)==26
    receipt=json.loads((BASE/runtime_name/'execution.json').read_text())
    assert receipt['exitCode']==0 and not receipt['timedOut'] and not receipt['customDriver'] and not receipt['gameMemoryWrites']
    assert receipt['replacementChips']=={name:sha(data) for name,data in targets.items()}
    rebuilt=json.loads((PORT/'REBUILT_ROM_SET_QUALIFICATION.json').read_text())
    assert rebuilt['allRebuiltROMBytesMatchRuntimeInput']
    assert rebuilt['chipSHA256']=={name:sha(data) for name,data in targets.items()},'Current clean rebuild proof required'
    program_bytes=bytearray(1048576)
    program_bytes[0::2]=targets['mk321u54.bin']
    program_bytes[1::2]=targets['mk321u63.bin']
    for name in ('ENDING_LINK_QUALIFICATION.json','CAST_LINK_QUALIFICATION.json','LADDER_LINK_QUALIFICATION.json'):
        linked=json.loads((PORT/name).read_text())
        assert linked['programSHA256']==sha(program_bytes),'Current linked-record proof required: '+name
        if name=='LADDER_LINK_QUALIFICATION.json':
            assert linked['linkedROMTablesVerified']
    # Independent older generic IPS decoder, not old game/driver payload code.
    spec=importlib.util.spec_from_file_location('reference_ips',ROOT/'tools/ips_apply.py')
    reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
    files={};records=[]
    with zipfile.ZipFile(ROOT/'roms/mk2.zip') as mk2,zipfile.ZipFile(ROOT/'mk3.zip') as mk3:
        archives={'mk2':mk2,'mk3':mk3}
        for name,target in sorted(targets.items()):
            source_archive,source_name=sources[name]
            source=read_chip(archives[source_archive],source_name)
            record=dict(target=name,sourceArchive=source_archive,source=source_name,
                sourceBytes=len(source),sourceSHA256=sha(source),targetBytes=len(target),targetSHA256=sha(target))
            if source==target: record['operation']='copy'
            else:
                assert len(source)==len(target)
                delta=create_patch(source,target)
                assert apply_patch(source,delta)==target
                assert bytes(reference.apply_ips(source,delta))==target
                relative='patches/'+name+'.ips';files[relative]=delta
                record.update(operation='ips',patch=relative,patchBytes=len(delta),patchSHA256=sha(delta))
            records.append(record)
    manifest=dict(format='MK2KS-NATIVE-IPS-1',developmentOnly=True,releaseReady=False,
        fullPortVerified=False,stockDriver='mk3',stockMAMEVersion='0.289',
        testedEmulatorSHA256=receipt['emulatorSHA256'],customDriver=False,
        provenanceReceipt=runtime_name+'/execution.json',chips=records)
    files['PATCH_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    files['README_PATCHING.txt']=README.encode('ascii')
    files['MOVELIST_NATIVE.txt']=(PORT/'MOVELIST_NATIVE.txt').read_bytes()
    for name in ('ips_codec.py','patch_native_roms.py','test_ips_codec.py'):
        files[name]=(PORT/name).read_bytes()
    files['PATCH.cmd']=b'@echo off\r\ncd /d "%~dp0"\r\nif "%~2"=="" (echo Usage: PATCH.cmd "path\\mk2.zip" "path\\mk3.zip"& pause& exit /b 1)\r\npy -3 patch_native_roms.py --mk2 "%~1" --mk3 "%~2" --output "%~dp0roms\\mk3.zip"\r\nif errorlevel 1 (echo PATCH FAILED& pause& exit /b 1)\r\necho DEVELOPMENT ROM SET CREATED\r\npause\r\n'
    files['PLAY.cmd']=b'@echo off\r\ncd /d "%~dp0"\r\nset "MK2KS_MAME=%~1"\r\nif not defined MK2KS_MAME set "MK2KS_MAME=%~dp0mame.exe"\r\nif not exist "%MK2KS_MAME%" (echo Supply a stock MAME executable path.& pause& exit /b 1)\r\nif not exist "%~dp0roms\\mk3.zip" (echo Run PATCH.cmd first.& pause& exit /b 1)\r\n"%MK2KS_MAME%" mk3 -rompath "%~dp0roms" -cfg_directory "%~dp0config\\cfg" -nvram_directory "%~dp0config\\nvram" -snapshot_directory "%~dp0config\\snap"\r\n'
    for path in sorted((BUILD/'srcp').glob('*.ASM')):
        if path.name.startswith(('KS','KANO','SONYA')): files['source/asm/'+path.name]=path.read_bytes()
    files['source/PBUILD.BAT']=(BUILD/'PBUILD.BAT').read_bytes()
    files['source/MK2NEWW.CMD']=(BUILD/'srcp/MK2NEWW.CMD').read_bytes()
    files['source/deadpool_source.py']=(PORT/'deadpool_source.py').read_bytes()
    files['source/special_root_contract.py']=(PORT/'special_root_contract.py').read_bytes()
    for name in ('ending_source.py','dcs_source.py','extend_dcs_kano_ball.py','current_sound.py',
                 'extend_dcs_chicken.py','prepare_chicken_pcm.py',
                 'boss_category_source.py','cpu_action_source.py','build_ending_art.py',
                 'native_roster.py','qualify_ending_link.py','qualify_cast_link.py',
                 'ladder_source.py','test_ladder_source.py','qualify_ladder_link.py',
                 'leg_ground_source.py','test_leg_ground_source.py','DETACHED_LEGS_2219_CURRENT.md'):
        files['source/'+name]=(PORT/name).read_bytes()
    for name in ('decode_native_picture.py','build_native_ending_reference.py','upgrade_ksui_previews.py'):
        files['source/reference_tools/'+name]=(ROOT/'tools'/name).read_bytes()
    files['source/ENDING_ART.json']=(PORT/'generated_ending/ENDING_ART.json').read_bytes()
    files['source/ENDING_LINK_QUALIFICATION.json']=(PORT/'ENDING_LINK_QUALIFICATION.json').read_bytes()
    files['source/CAST_LINK_QUALIFICATION.json']=(PORT/'CAST_LINK_QUALIFICATION.json').read_bytes()
    files['source/ENDING_ART_STAGE.md']=(PORT/'ENDING_ART_STAGE.md').read_bytes()
    files['source/NATIVE_CAST_INTEGRATION.md']=(PORT/'NATIVE_CAST_INTEGRATION.md').read_bytes()
    files['source/NATIVE_LADDER_ROSTER.md']=(PORT/'NATIVE_LADDER_ROSTER.md').read_bytes()
    guide=(PORT/'NATIVE_SOURCE_GUIDE.md').read_bytes()
    assert sha(program_bytes).encode('ascii') in guide, 'Source guide names a stale program build'
    files['source/NATIVE_SOURCE_GUIDE.md']=guide
    for name in ('qualify_common_table_link.py','COMMON_TABLE_LINK_QUALIFICATION.json'):
        files['source/'+name]=(PORT/name).read_bytes()
    for name in ('CLAPPED_LINEUPS_CURRENT.md','qualify_clap_runtime.py','test_clapped_lineups.py'):
        files['source/'+name]=(PORT/name).read_bytes()
    files['source/LADDER_LINK_QUALIFICATION.json']=(PORT/'LADDER_LINK_QUALIFICATION.json').read_bytes()
    diffs=[]
    with zipfile.ZipFile('C:/Users/kando/Downloads/mk2-rebuild-main.zip') as archive:
        for entry in archive.namelist():
            if not entry.startswith('mk2-rebuild-main/src/') or entry.count('/')!=2: continue
            name=Path(entry).name;path=BUILD/'srcp'/name
            if not path.is_file() or path.suffix.upper() not in ('.ASM','.HDR','.CMD'): continue
            before=archive.read(entry).decode('latin-1').replace('\r\n','\n').rstrip('\n')+'\n'
            after=path.read_bytes().decode('latin-1').replace('\r\n','\n').rstrip('\n')+'\n'
            if before!=after:
                diffs.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),
                    fromfile='a/src/'+name,tofile='b/src/'+name))
    assert diffs
    files['source/native_source.patch']=''.join(diffs).encode('latin-1')
    files['FILES.json']=(json.dumps({name:sha(data) for name,data in sorted(files.items())},indent=2)+'\n').encode()
    for name,data in files.items():
        path=PACKAGE/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    roundtrip_path=OUT/'roundtrip/roms/mk3.zip'
    if roundtrip_path.exists():
        assert '--refresh-generated' in sys.argv
        assert sha(roundtrip_path.read_bytes())==previous['roundtrip']['SHA256'],'Modified old generated roundtrip archive'
        candidate_path=roundtrip_path.with_name('mk3-candidate.zip')
        assert not candidate_path.exists(),'Inspect a previous unfinished candidate before retrying'
        patched=build(ROOT/'roms/mk2.zip',ROOT/'mk3.zip',PACKAGE,candidate_path)
        with zipfile.ZipFile(candidate_path) as archive:
            assert set(archive.namelist())==set(targets)
            assert all(archive.read(name)==data for name,data in targets.items())
        candidate_path.replace(roundtrip_path)
        patched['output']=str(roundtrip_path)
    else:
        patched=build(ROOT/'roms/mk2.zip',ROOT/'mk3.zip',PACKAGE,roundtrip_path)
    with zipfile.ZipFile(OUT/'roundtrip/roms/mk3.zip') as archive:
        assert set(archive.namelist())==set(targets)
        assert all(archive.read(name)==data for name,data in targets.items())
    destination=OUT/'MK2KS_NATIVE_DEVELOPMENT_IPS.zip'
    write_package_zip(destination,files)
    result=dict(package=str(destination),bytes=destination.stat().st_size,SHA256=sha(destination.read_bytes()),
        chipCount=26,ipsPatches=sum(r['operation']=='ips' for r in records),
        copiedMK2Graphics=sum(r['operation']=='copy' for r in records),
        ownASMModules=sum(n.startswith('source/asm/') for n in files),
        twoIndependentDecodersVerified=True,fullArchiveRoundtripVerified=True,
        roundtrip=patched,releaseReady=False,fullPortVerified=False)
    (OUT/'PACKAGING_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
