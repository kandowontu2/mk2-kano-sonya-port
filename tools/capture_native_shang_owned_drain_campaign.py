"""Replay the ENTIRE original failed physical campaign on actual drain repair.

No proxy, forced fatality/outcome, state writes, dropped preceding opponents,
modified control strategy, ROM copies, saved RGB/audio, or public promotion.
All initialized high/owned/new-GFX bytes checked in this actual cold game.
The native handle, decoded frames and original chronology remain held in RAM.
"""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace

import capture_native_sonya_shang_cache_cause as previous
import verify_native_shang_drain_startup as initial
import verify_native_shang_drain_startup_successor as corrected

ROOT = previous.ROOT
need, sha = previous.need, previous.sha
NAME = corrected.NAME
OUT = ROOT / 'audit_native_shang_owned_drain_campaign'
SOURCE = ROOT / 'audit_native_shang_owned_drain_campaign_source'
INIT = ROOT / 'audit_native_shang_owned_drain_campaign_initializer'
LUA = 'mk2ks_native_shang_owned_drain_campaign.lua'
CONTROLLERS = list(dict.fromkeys((LUA, 'mk2ks_native_shang_drain_startup.lua', *previous.CONTROLLERS)))
RAM = {}


def once(source, before, after):
    need(source.count(before) == 1, 'One exact original whole-host boundary: ' + before[:100])
    return source.replace(before, after, 1)


def expectation():
    need(not INIT.exists(), 'Fresh independently initialized whole source model')
    INIT.mkdir()
    wanted = initial.expected(INIT)
    physical = (ROOT / NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    wanted['owned'], _ = corrected.expected_owned(physical)
    build = json.loads((ROOT / NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    startup = json.loads((ROOT / 'audit_native_shang_drain_startup_successor/report.json').read_text())
    need({k:corrected.digest(v) for k,v in wanted.items()} == startup['actualWindowHashes'] and
         corrected.digest(wanted['high']) == build['expected_guest_sha256'] and
         sha(ROOT / NAME / 'mkport_candidate.exe') == build['executable_sha256'],
         'Independent full program/owned/reserved-graphics model equals accepted startup and actual build')
    provider = SimpleNamespace(ROOT=ROOT, NAME=NAME, EXE_SHA=build['executable_sha256'],
        GUEST_SHA=corrected.digest(wanted['high']), PAYLOAD_SHA=build['payload_sha256'],
        expected=lambda:wanted['high'], expected_windows=lambda:wanted,
        expected_gfx=lambda:wanted['graphics'], __file__=__file__)
    (INIT / 'report.json').write_text(json.dumps(dict(passed=True, sourceOnlyAccepted=True,
        expectedWindowHashes={k:corrected.digest(v) for k,v in wanted.items()},
        metadataOwnedModelCorrectionRequired=True, priorExistingOwnedByteDelta=43, newOwnedByteDelta=24,
        totalOwnedInitializationByteDelta=67, nativeGameplayAccepted=False, fullPortAcceptance=False), indent=2)+'\n')
    return wanted, build, provider


def functions(provider):
    scope, host = previous.functions(provider)
    host = once(host, "name.startswith('shang_victim_provenance_') or name.startswith('ending_page')",
                "name.startswith('shang_shrink_') or name.startswith('shang_victim_provenance_') or name.startswith('ending_page')")
    # Parse all chunks in RAM, persist ONLY digest/count receipts. The original
    # full high-window export remains an additional independent comparison.
    prefix = '''    if line.startswith('MK2_DRAIN_STARTUP '):
     f=dict(re.findall(r'(\\w+)=([^\\s]+)',line));raw=bytes.fromhex(f.pop('hex'))
     kind=f['kind'];offset=int(f['offset']);count=int(f['bytes']);start=int(f['start'],16)
     need(kind in window_buffers and f['writes']=='0' and f['assistance']=='none' and
      start==window_starts[kind] and count==len(raw) and 0<count<=4096 and offset==len(window_buffers[kind]),
      'Every actual initialized window chunk bounded and contiguous')
     window_buffers[kind].extend(raw)
    elif line.startswith('MK2_DRAIN_STARTUP_COMPLETE '):
     need(not window_proof and line.strip()=='MK2_DRAIN_STARTUP_COMPLETE writes=0 assistance=none' and
      {k:bytes(v) for k,v in window_buffers.items()}==native.expected_windows(),
      'Every actual HIGH/OWNED/new-GFX byte equals independent complete initialized model')
     window_proof=dict(passed=True,actualWindowHashes={k:hashlib.sha256(v).hexdigest().upper()for k,v in window_buffers.items()},
      actualWindowBytes={k:len(v)for k,v in window_buffers.items()},gameWrites=0,physicalInputs=0,rawExportsPersisted=False,
      metadataOwnedModelCorrectionRequired=True,nativeGameplayAccepted=False,fullPortAcceptance=False)
     (OUT/'initialized_windows_proof.json').write_text(json.dumps(window_proof,indent=2)+'\\n')
     log.write('MK2_DRAIN_STARTUP_COMPLETE_DIGEST '+json.dumps(window_proof)+'\\n')
     print('All actual initialized windows qualified: '+json.dumps(window_proof['actualWindowHashes']),flush=True)
     window_buffers.clear()
    elif line.startswith('MK2_CAMPAIGN_GUEST_RAM '):'''
    host = once(host, "    if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):", prefix)
    host = once(host, ' started=time.time()',
                " window_buffers={k:bytearray()for k in ('high','owned','graphics')};window_starts=dict(high=0,owned=0,graphics=0x1fb0000);window_proof=None\n started=time.time()")
    host = once(host,
        "  need(identity and identity['ParentProcessId']==os.getpid() and identity['createdUnix']>=started-1,'Actual known native child creation identity')",
        "  need(identity and identity['ParentProcessId']==os.getpid() and identity['createdUnix']>=started-1 and Path(identity['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve() and identity['CommandLine']==subprocess.list2cmdline(command),'Actual original PID/birth/path/parent/full command')\n  RAM_HANDLE.update(process=process,identity=identity,command=command)")
    host = once(host, "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_'))",
                "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_','MK2_SHANG_OWNED_DRAIN_ROUTE','MK2_SONYA_SHANG_CACHE_CAUSE_RESULT'))")
    host = once(host, " metadata=qualify_payload_metadata_warning(errors,guestproof)",
                " need(window_proof and not window_buffers,'Actual complete initialized windows observed in THIS game')\n metadata=qualify_payload_metadata_warning(errors,guestproof)")
    host = once(host, 'return dict(result=result,images=images,text=chronology,guest=guest,rawImages=raw_images)',
                'return dict(result=result,images=images,text=chronology,guest=guest,rawImages=raw_images,initializedWindows=window_proof)')
    scope.update(__file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS, RAM_HANDLE=RAM)
    exec(compile(host, __file__+'::whole_original_physical_campaign_plus_full_windows_and_routes', 'exec'), scope)
    return scope, host


def source_guard():
    need(not OUT.exists() and not SOURCE.exists() and not INIT.exists() and
         not initial.identity.census() and not (ROOT / 'mame-mkp/build/mingw-gcc').exists(),
         'Fresh required replay only after original startup host/native/cache terminal')
    paths = [previous.SOURCE/'report.json', ROOT/'audit_native_shang_drain_startup_successor/report.json',
             ROOT/'audit_native_shang_drain_build_source/report.json',
             ROOT/'audit_native_shang_actual_cache_cause_checked/report.json',
             ROOT/'audit_native_shang_cause_preceding_campaign_checked/report.json',
             ROOT/'audit_native_sonya_shang_actual_cause_retirement/report.json']
    old, startup, build_guard, cause, prefix, retirement = [json.loads(p.read_text()) for p in paths]
    need(all(r['passed'] for r in (old,startup,build_guard,cause,prefix,retirement)) and
         startup['actualNativeInitializedWindowsAccepted'] and not startup['nativeGameplayRepairAccepted'] and
         prefix['accepted']['completedOpponents']==13 and prefix['accepted']['completeOriginalRows']==1009959 and
         not cause['nativeRepairAccepted'] and len(old['originalNaturalIntegrationRequirements'])==14 and
         len(old['originalRemainingWorkGroups'])==6,
         'Accepted startup/source, exact real failed cause and whole prior thirteen earned opponents; full scope retained')
    pins = {}
    for proof in (old,startup,build_guard,cause,prefix,retirement):
        need(not proof['fullPortAcceptance'], 'No earlier finite evidence is whole-port acceptance')
        for p,h in proof['inputHashes'].items():
            need(sha(p)==h and (p not in pins or pins[p]==h), 'Every immutable transitive input: '+p)
            pins[p]=h
    for name in CONTROLLERS:
        text=(ROOT/name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data',text),
             'All actual loaded sources physical-input/passive-read only: '+name)
    wrapper=(ROOT/LUA).read_text()
    need(wrapper.count("source:gsub('0xff9d7770','0xffd88000')")==1 and 'assert(count==3' in wrapper and
         wrapper.count('install_read_tap')==1 and ':set_value(' not in wrapper and
         ':clear_value(' not in wrapper and 'machine:exit' not in wrapper,
         'Exact passive relocated-table observations/helper taps; no changed buttons or exits')
    meta_path=ROOT/NAME/'build-info.json';meta=json.loads(meta_path.read_text(encoding='utf-8-sig'))
    provider=SimpleNamespace(GUEST_SHA=meta['expected_guest_sha256'],EXE_SHA=meta['executable_sha256'],PAYLOAD_SHA=meta['payload_sha256'])
    _, host=functions(provider)
    need("MK2KS_TEST_FIGHTER='sonya',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'" in host and "'-str','18100'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and 'len(images)<=64' in host,
         'Original entire tower/ending/fresh join, physical strategy, limits and bounded RAM capture')
    for p in (Path(__file__).resolve(),Path(previous.__file__),Path(initial.__file__),Path(corrected.__file__),
              meta_path,*paths,*(ROOT/n for n in CONTROLLERS)):
        pins[str(p.resolve())]=sha(p)
    report=dict(passed=True,sourceOnlyAccepted=True,currentCandidate=NAME,
        unchangedWholeOriginalPhysicalInputs=True,allThirteenEarlierOpponentsRetained=True,
        originalObservationDeadlineSeconds=18000,originalNativeLimitSeconds=18100,
        fullHighOwnedNewGraphicsComparisonRequired=True,maximumRetainedNativeRasters=64,
        wholeGeneratedHostSHA256=corrected.digest(host.encode()),inputHashes=pins,
        originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=old['originalRemainingWorkGroups'],
        nativeGameplayAccepted=False,fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,
        artAccepted=False,audioAccepted=False,fullPortAcceptance=False,newBuilds=0,newROMCopies=0,
        newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    guard=source_guard()
    wanted,build,provider=expectation()
    scope,host=functions(provider)
    need(corrected.digest(host.encode())==guard['wholeGeneratedHostSHA256'], 'Exact qualified entire host')
    RAM.update(scope=scope,wanted=wanted,build=build,executedHost=host,guard=guard)
    captured=scope['capture']()
    RAM['capture']=captured
    return captured


if __name__=='__main__':
    try:
        captured=run()
    except Exception as error:
        folder=OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active')
        if folder.exists():
            path=folder/'current_capture_failure.json';need(not path.exists(),'Preserve original successor failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Same full original physical campaign on owned Shang repair; original native handle and evidence held in RAM.',local=dict(RAM=RAM))
