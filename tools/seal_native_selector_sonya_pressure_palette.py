"""Exact new palette metadata compression, whole source and endpoint verification."""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_pressure_blood_all_owners as owners
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=owners.ROOT,owners.need,owners.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_palette_sealed.json'


def execute():
    need(not OUT.exists(), 'Fresh immutable palette/owner/storage seal')
    report_path=owners.OUT/'report.json';report=json.loads(report_path.read_text())
    capture=owners.arithmetic.previous.binding.capture
    handle=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts() if r['ProcessId']==38752)
    need(report['passed'] and handle['process'].poll()==0 and handle['identity']==report['actualNativeIdentity'] and
         host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and
         not census.identity.census(), 'Same original host and actual35924 terminal handle, no pending native job')
    arithmetic_path=owners.arithmetic.OUT/'report.json'
    arithmetic=json.loads(arithmetic_path.read_text())
    need(arithmetic['passed'] and len(arithmetic['effectiveFaultsRejected'])==23 and
         arithmetic['arithmetic']['nativeCacheStores']==4854 and
         arithmetic['arithmetic']['allNativeFIFOInputs']==112426 and
         report['stockBlood']['actualStockBloodOwnerEpochs']==32 and
         report['stockBlood']['publishedOwnerEpochs']==17 and
         report['stockBlood']['unpublishedOwnerEpochs']==15 and len(report['effectiveFaultsRejected'])==14,
         'Whole native cache arithmetic/FIFO and all published/unpublished blood owners qualified')
    pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()), 'Every whole earlier source/evidence pin intact')
    files={Path(__file__).resolve()}
    for folder in (capture.BASE,capture.OUT,owners.arithmetic.previous.binding.OUT,
                   owners.arithmetic.previous.OUT,owners.arithmetic.OUT,owners.OUT):
        at=folder.resolve();need(at.is_relative_to(ROOT.resolve()) and at.is_dir(), 'Exact newly created metadata subtree')
        files.update(p.resolve() for p in at.rglob('*') if p.is_file())
    for name in ('capture_native_selector_sonya_pressure_palette.py','bind_native_selector_sonya_pressure_palette.py',
                 'inspect_native_selector_sonya_pressure_palette.py','qualify_native_selector_sonya_pressure_palette.py',
                 'qualify_native_selector_sonya_pressure_palette_router.py',
                 'qualify_native_selector_sonya_pressure_blood_all_owners.py'):
        files.add((ROOT/'tools'/name).resolve())
    files.add(capture.LUA.resolve())
    nvram=(capture.RAM_CASES[capture.KEY][0]/'nvram/mk2ks/nvram').resolve()
    mapping=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    need(nvram.is_file() and nvram.stat().st_size==16384 and
         'map(0x01400000, 0x0141ffff).rw(FUNC(midtunit_state::midtunit_cmos_r), FUNC(midtunit_state::midtunit_cmos_w)).share("nvram");' in mapping.read_text(),
         'Only exact normal native CMOS metadata bound to actual compiled map')
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve()) and
             (p.suffix.lower() in ('.py','.lua','.json','.gz','.log','.cfg') or p==nvram),
             'Exact metadata/source files only, no build/ROM/raw media/ZIP')
        key=str(p);h=sha(p);need(key not in pins or pins[key]==h, 'No executed source or original failure rewritten');pins[key]=h
        old=dict(sha256=h,logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',key],capture_output=True)
        need(call.returncode==0 and sha(p)==h, 'Every entire evidence file unchanged after exact LZX')
        entries.append(dict(path=key,**old,storedAfter=storage.stored(p)))
    sync=storage.source.verify()
    need(sync['passed'] and all(sha(p)==h for p,h in pins.items()), 'All15 compiled-source sync, fixed endpoints and whole evidence pins')
    value=dict(report,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        wholeNativePaletteArithmetic=arithmetic['arithmetic'],nativeCacheFaultsRejected=23,
        actualBloodOwnerFaultsRejected=14,all32StockBloodOwnersAccepted=True,
        wholeOriginalHistoryRGBandAudioIdentical=True,
        originalArrayComparisonFailurePreserved=True,originalAllStockEntryAssumptionFailurePreserved=True,
        exactNewSmallFileCompression=entries,sourceSyncPassed=True,
        logicalBytes=sum(r['logicalBytes'] for r in entries),storedBytes=sum(r['storedAfter'] for r in entries),
        wholeObjectiveStillActive=True,newNativeGamesThisEvidenceChain=1,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.write_text(json.dumps(value,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h, 'Whole final finite palette/owner/storage receipt intact')
    return value
