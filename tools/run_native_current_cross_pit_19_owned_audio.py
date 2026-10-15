"""Current Pit19 full audio plus direct movie/voice/queue/RNG observations.

Complete original runtime and29 audio faults retained. The extracted fault
function now receives its folder; no reporting-tail extraction or alias edits.
Added observations are not owner/priority acceptance until qualified.
"""
import argparse
import code
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_current_cross_pit_19_audio as original
import qualify_native_current_cross_pit_19_audio_context as folder_context

ROOT, need, sha, once = original.ROOT, original.need, original.sha, original.once
SOURCE = ROOT/'audit_native_current_cross_pit_19_owned_audio_source'
PREFIX = 'audit_native_current_cross_pit_19_owned_audio_'
LUA = 'mk2ks_native_cross_pit_19_owned_audio.lua'
RAM = {}


def functions():
    scope = folder_context.functions()
    fn = scope['collector']
    body = once(fn.source,original.PREFIX,PREFIX)
    body = once(body,original.LUA,LUA)
    namespace = dict(fn.__globals__,__file__=__file__,source=SimpleNamespace(OUT=SOURCE,__file__=__file__),
                     CONTROLLERS=fn.__globals__['CONTROLLERS']+(LUA,'mk2ks_current_subzero_pit_audio_v5941.lua',
                                    'mk2ks_current_pit_queue_rng_v5954.lua'),SOURCE_PINS={})
    exec(compile(body,__file__+'::whole_current19_collector_additive_owned_observer','exec'),namespace)
    scope['collector']=namespace['capture'];scope['collector'].source=body
    need(tuple(inspect.signature(scope['check_faults']).parameters)[-1]=='folder',
         'Entire29-fault function has its real capture-folder argument')
    return scope


def preflight(scope,fighter,side):
    # Original whole current compiled/transitive observer/manifest proof remains
    # exactly frozen. Its preflight boots nothing and creates no baseline case.
    original.preflight(original.functions(),fighter,side)
    pins=dict(json.loads((original.SOURCE/'report.json').read_text())['inputHashes'])
    owner=(ROOT/'mk2ks_current_subzero_pit_audio_v5941.lua').read_text()
    owner=owner[owner.index('\ndo\n')+1:]
    owner=once(owner,'local frame,origin,cine=0,nil,nil',
        "local frame,origin,cine=0,nil,nil\nlocal victim_id=assert(({kano=18,sonya=17})[os.getenv('MK2KS_STAGE_WINNER')])")
    owner=once(owner,'p:read_u16(a+0x1f0)==8','p:read_u16(a+0x1f0)==victim_id')
    owner=once(owner,'owner140=%08X id=8 body','owner140=%08X id=%d body')
    owner=once(owner,'cpu.A0.value,a,m,p:read_u32(m+0x140),p:read_u16(a+0x160)',
        'cpu.A0.value,a,m,p:read_u32(m+0x140),p:read_u16(a+0x1f0),p:read_u16(a+0x160)')
    rng=(ROOT/'mk2ks_current_pit_queue_rng_v5954.lua').read_text()
    rng=rng[rng.index('\ndo\n')+1:]
    expected="-- Whole current Pit19 audio, plus passive native movie/voice/queue/RNG ownership.\ndofile('mk2ks_native_cross_pit_19_audio.lua')\n"+owner+'\n'+rng+'\n'
    actual=(ROOT/LUA).read_text()
    need(actual.startswith(expected),'Entire original movie and queue/RNG observers retained; only actual opposite-victim ID metadata changes')
    routes=actual[len(expected):]
    need(routes.count('MK2_PIT_OWNER_ROUTE')==1 and
         'ownerC0=%08X owner140=%08X owner290=%08X' in routes and
         "ipairs({0xffa11fd0,0xffa12070,0xffa12220,0xffa122d0,0xffa123b0,0xffa123d0,0xffa12430,0xffa12530})"in routes and
         'cpu.PC.value~=at+16'in routes and 'frame>origin+1100'in routes and
         'p:read_u32(m+0xc0)'in routes and 'p:read_u32(m+0x140)'in routes and 'p:read_u32(m+0x290)'in routes and
         'p:read_u32(cpu.SP.value)'in routes,'Direct saved native actor/Main namespaces, caller and full original audio window')
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(',actual),
         'Entire additional companion contains only passive state reads')
    prior_path=ROOT/'audit_native_current_cross_pit_19_audio_kano_p1_samples/current_19_audio_ram_retirement.json'
    prior=json.loads(prior_path.read_text())
    need(prior['passed'] and prior['originalStereoFrames']==965760 and
         prior['originalCaptureRAMDictionaryCleared'] and all(sha(p)==h for p,h in prior['inputHashes'].items()),
         'Original current KanoP1 finite19 waveform and full retirement intact, never repeated as this broader case')
    for p,h in prior['inputHashes'].items():
        need(p not in pins or pins[p]==h,'Consistent current sources')
        pins[p]=h
    for p in(Path(__file__),Path(original.__file__),Path(folder_context.__file__),ROOT/LUA,
              ROOT/'mk2ks_current_subzero_pit_audio_v5941.lua',ROOT/'mk2ks_current_pit_queue_rng_v5954.lua',
              original.SOURCE/'report.json',prior_path):
        pins[str(p.resolve())]=sha(p)
    fn=scope['collector'];fn.__globals__['SOURCE_PINS']=pins
    original_proof=json.loads((original.SOURCE/'report.json').read_text())
    proof=dict(passed=True,sourceOnlyAccepted=True,candidate=scope['current'].NAME,
               guestSHA256=scope['current'].GUEST_SHA,totalSampleChannels=19,
               entirePreviousAudioAnd29FaultAlgorithmsRetained=True,passiveOwnedObserversSourceBound=True,
               actualNativeOwnedAudioAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,fullPortAcceptance=False,
               inputHashes=pins,transportSourceSHA256=original.hashlib.sha256(fn.source.encode()).hexdigest().upper(),
               originalNaturalIntegrationRequirements=original_proof['originalNaturalIntegrationRequirements'],
               originalRemainingWorkGroups=original_proof['originalRemainingWorkGroups'],
               newNativeBoots=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active')
    need(all(sha(p)==h for p,h in pins.items()),'Whole source/prior/native/failure bytes unchanged before boot')
    if SOURCE.exists():need(json.loads((SOURCE/'report.json').read_text())==proof,'Immutable additive source proof')
    else:SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    body=fn.source[:fn.source.index('    folder.mkdir();')]+'    return len(files),pins\n'
    namespace=dict(fn.__globals__)
    exec(compile(body,__file__+'::whole_actual_owned_case_input_manifest','exec'),namespace)
    count,actual_pins=namespace['capture'](fighter,side,True,None)
    need(count>100 and all(sha(p)==h for p,h in actual_pins.items()),'Whole requested current owned-Pit manifest before boot')
    print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,fighter=fighter,side=side,actualManifestFiles=count,
                         totalSampleChannels=19,addedOwnedObserversAcceptedAtRuntime=False,newNativeBoots=0)),flush=True)
    return proof


def run(scope,fighter,side):
    body=inspect.getsource(original.run)
    before="accepted=scope['check_faults'](text,meta,live,fighter,side,guest,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),expected)"
    body=once(body,before,before[:-1]+',folder)')
    body=once(body,"    RAM['report']=report",
        "    report.update(passiveCinematicOwnershipAndQueueRNGCaptured=True,actualAddedOwnedObserverQualificationAccepted=False)\n"
        "    RAM['report']=report")
    namespace=dict(vars(original),__file__=__file__,PREFIX=PREFIX,SOURCE=SOURCE,LUA=LUA,RAM=RAM,preflight=preflight)
    exec(compile(body,__file__+'::whole_original_initialized_native19_runtime_with_capture_folder','exec'),namespace)
    return namespace['run'](scope,fighter,side)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true')
    parser.add_argument('--fighter',choices=('kano','sonya'),required=True);parser.add_argument('--side',type=int,choices=(1,2),required=True)
    args=parser.parse_args()
    try:
        scope=functions()
        if args.source_only:preflight(scope,args.fighter,args.side)
        else:run(scope,args.fighter,args.side)
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active')
        folder=RAM.get('folder',ROOT/f'{PREFIX}{args.fighter}_p{args.side}_samples')
        if not folder.exists():folder=ROOT/'audit_native_current_cross_pit_19_owned_audio_preflight_failure'
        if not folder.exists():folder.mkdir()
        path=folder/'current_19_audio_failure.json'
        if not path.exists():path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure),flush=True)
        if args.source_only:raise SystemExit(1)
    if not args.source_only:
        code.interact(banner='Same current owned-Pit capture; full sound remains only in RAM.',local=dict(RAM=RAM))
