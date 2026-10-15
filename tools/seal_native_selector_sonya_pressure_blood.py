"""Exact new stock-effect metadata compression, whole source/native pins."""
import json
import subprocess
from pathlib import Path
import qualify_native_selector_sonya_pressure_blood_refs as proof
import seal_native_selector_knife_snapshot_storage as storage
import read_live_shang_drain_frames as census

ROOT,need,sha=proof.ROOT,proof.need,proof.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_blood_sealed.json'


def execute():
    need(not OUT.exists(),'Fresh immutable whole stock effect evidence/storage seal')
    report_path=proof.OUT/'report.json';report=json.loads(report_path.read_text())
    bound=proof.epoch.palette.original
    capture=bound.previous.original.capture;handle=capture.NATIVE_HANDLES[capture.KEY]
    host=next(r for r in census.census_hosts()if r['ProcessId']==38752)
    need(report['passed']and handle['process'].poll()==0 and report['actualNativeIdentity']==handle['identity']and
         host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766 and not census.identity.census(),
         'Same original45272 terminal handle and retained38752 live host, no substituted match')
    need(report['bloodFaultSuiteAccepted']and len(report['effectiveBloodFaultsRejected'])==22 and
         report['stockBlood']['nativeBloodPublications']==report['stockBlood']['actualNativeBloodDraws']==1089 and
         len(report['stockBlood']['actualBloodAllocationEpochs'])==17 and
         report['stockBlood']['nativeTaskSnapshots']==1800 and report['stockBlood']['wholeMainSlotsPerSnapshot']==168,
         'Whole finite source/projection/allocator/Main/drawing positives and22 faults accepted')
    pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every whole earlier source/current evidence pin intact')
    files={Path(__file__).resolve(),report_path.resolve()}
    for folder in (capture.BASE,capture.OUT,bound.previous.original.OUT,
                   bound.previous.OUT,bound.OUT,proof.epoch.palette.OUT,
                   proof.epoch.OUT,proof.OUT):
        at=folder.resolve();need(at.is_relative_to(ROOT.resolve())and at.is_dir(),'Exact new effect metadata subtree')
        files.update(p.resolve()for p in at.rglob('*')if p.is_file())
    for name in ('capture_native_selector_sonya_pressure_effects.py',
                 'qualify_native_selector_sonya_pressure_blood.py',
                 'qualify_native_selector_sonya_pressure_blood_slots.py',
                 'qualify_native_selector_sonya_pressure_blood_bound.py',
                 'qualify_native_selector_sonya_pressure_blood_palette.py',
                 'qualify_native_selector_sonya_pressure_blood_epoch.py',
                 'qualify_native_selector_sonya_pressure_blood_refs.py'):
        files.add((ROOT/'tools'/name).resolve())
    files.add(capture.LUA.resolve())
    folder=capture.RAM_CASES[capture.KEY][0]
    nvram=(folder/'nvram/mk2ks/nvram').resolve()
    mapping=ROOT/'diagnostic_native_selector_layers_long/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
    need(nvram.is_file()and nvram.stat().st_size()==16384 and
         'map(0x01400000, 0x0141ffff).rw(FUNC(midtunit_state::midtunit_cmos_r), FUNC(midtunit_state::midtunit_cmos_w)).share("nvram");'in mapping.read_text(),
         'Only exact normal16384-byte native CMOS metadata, bound to compiled memory map')
    entries=[]
    for p in sorted(files):
        need(p.is_relative_to(ROOT.resolve())and(p.suffix.lower()in('.py','.lua','.json','.gz','.log','.cfg')or p==nvram),
             'Only exact new metadata/source/trace files, no build/ROM/raw image/audio files')
        key=str(p);h=sha(p);need(key not in pins or pins[key]==h,'Never rewrite executed source or original failure');pins[key]=h
        old=dict(sha256=h,logicalBytes=p.stat().st_size,storedBefore=storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==h,'Every complete exact effect evidence file intact after LZX')
        entries.append(dict(path=key,**old,storedAfter=storage.stored(p)))
    need(storage.source.verify()['passed']and all(sha(p)==h for p,h in pins.items()),
         'All15 canonical/compiled-source sync, unchanged private/public endpoints and full pins')
    value=dict(report,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        originalTaskCountFailurePreserved=True,originalPaletteExclusionFailurePreserved=True,
        originalArtworkOnlyPaletteFailurePreserved=True,originalReferenceInputFaultPreserved=True,
        exactNewSmallFileCompression=entries,
        logicalBytes=sum(r['logicalBytes']for r in entries),storedBytes=sum(r['storedAfter']for r in entries),
        sourceSyncPassed=True,finalFiniteStockBloodSeal=True,
        wholeObjectiveStillActive=True,newNativeGamesThisEvidenceChain=1)
    OUT.write_text(json.dumps(value,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole final finite source/effects/storage receipt intact')
    return value
