"""Current repaired guest, whole earned Tomb state and all 19 sound channels.

Reuse the entire existing physical campaign and source-clock audio models.
Source-only preparation boots nothing and makes no runtime acceptance claim.
Full mixed PCM/DAC/ROM stay in RAM; exact native identity is recorded at birth.
"""
import argparse
import code
import gzip
import hashlib
import inspect
import json
import re
import time
import traceback
from pathlib import Path
from types import SimpleNamespace

import capture_native_paired_stumble_campaign as repaired
import qualify_native_paired_stumble_table as repair_source
import run_current_cross_tomb_audio_v5838 as previous
import verify_current_cross_tomb_audio_v5842 as verification
import native_process_census_v6647 as census

ROOT,need,sha=repaired.ROOT,repaired.need,repaired.sha
SOURCE=ROOT/'audit_native_cross_tomb_19_audio_source'
LUA='mk2ks_native_cross_tomb_19_audio.lua'
RAM={}
CONTROLLERS=(LUA,'mk2ks_current_cross_tomb_provenance_v5834.lua',
 'mk2ks_current_cross_tomb_driver_v5833.lua','mk2ks_current_stage_ram_driver_v3594.lua',
 'mk2ks_current_stage_provenance_v3595.lua',previous.OBSERVER)
once=previous.once


def context():
    metadata=json.loads((ROOT/repaired.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    return SimpleNamespace(ROOT=ROOT,NAME=repaired.NAME,EXE_SHA=metadata['executable_sha256'],
        GUEST_SHA=metadata['expected_guest_sha256'],PAYLOAD_SHA=metadata['payload_sha256'],__file__=__file__)


def voice_models(current):
    body=once(inspect.getsource(previous.branches.original_voice.qualify_scream),
        "own=17 if fighter=='kano' else 18","own=18 if fighter=='kano' else 17")
    body=once(body,"'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA))
    scope=dict(vars(previous.branches.original_voice))
    exec(compile(body,__file__+'::whole_original_cross_victim_voice','exec'),scope)
    exec(compile(inspect.getsource(previous.branches.original_voice.faults),
        __file__+'::whole_original_voice_faults','exec'),scope)
    scope['qualify_scream'].source=body
    return scope['qualify_scream'],scope['faults']


def branch_models(current):
    scope=dict(vars(previous.branches),voice_models=lambda:voice_models(current))
    exec(compile(inspect.getsource(previous.branches.voice_proof),
        __file__+'::whole_current_voice_proof','exec'),scope)
    return SimpleNamespace(**scope)


def channel_models():
    body=inspect.getsource(verification.dropped.channel_gate)
    body=once(body,'len(precise)==14*len(pcm)','len(precise)==19*len(pcm)')
    body=once(body,'range(14)','range(19)')
    scope=dict(vars(verification.dropped),observed=verification.observed)
    exec(compile(body,__file__+'::whole_precise_channel_gate_expanded_to19','exec'),scope)
    channel=scope['channel_gate'];channel.source=body
    gates=[]
    for original in (verification.held_gate,verification.drop_gate):
        body=once(original.source,'len(channels)==len(pairs)==14*1100','len(channels)==len(pairs)==19*1100')
        body=once(body,'range(14)','range(19)')
        scope=dict(original.__globals__,channel_gate=channel)
        exec(compile(body,__file__+'::whole_cross_audio_gate_expanded_to19','exec'),scope)
        scope['gate'].source=body;gates.append(scope['gate'])
    return channel,gates


def collector(current):
    original,_=previous.collector()
    body=original.source
    for before,after in (
        ('audit_v5841_current_cross_tomb_winner_mix_','audit_native_cross_tomb_19_audio_'),
        (previous.LUA,LUA),(previous.current.EXE_SHA,current.EXE_SHA),
        (previous.current.PAYLOAD_SHA,current.PAYLOAD_SHA),
        ("'-samplepath',str(ROOT/'samples')","'-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples')"),
        ("'-samples'if enabled else'-nosamples'","'-samples'if enabled else'-nosamples','-wavwrite','NUL'"),
        ("    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}",
         "    files.update(ROOT/p for p in CONTROLLERS)\n    files.add(Path(census.__file__))\n    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}"),
        ("        (folder/'process.json').write_text(",
         """        actual=None
        for _ in range(100):
            actual=next((item for item in census.census() if item['ProcessId']==process.pid),None)
            if actual or process.poll()is not None:break
            time.sleep(.02)
        need(actual and actual['ParentProcessId']==os.getpid() and
             Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),
             'Actual current native birth/path/parent/command identity')
        (folder/'native_identity.json').write_text(json.dumps(actual,indent=2)+'\\n')
        (folder/'process.json').write_text("""),
    ):
        body=once(body,before,after)
    scope=dict(original.__globals__,__file__=__file__,NAME=current.NAME,current=current,
        source=SimpleNamespace(OUT=SOURCE),CONTROLLERS=CONTROLLERS,census=census)
    exec(compile(body,__file__+'::whole_existing_cold_cross_Tomb_collector_current19','exec'),scope)
    fn=scope['capture'];fn.source=body
    return fn


def source_guard():
    current=context();build_path=ROOT/current.NAME/'build-info.json'
    build=json.loads(build_path.read_text(encoding='utf-8-sig'))
    guard=json.loads(repaired.GUARD.read_text())
    repair_source.source_contract()
    need(guard['passed']and guard['sourceOnlyAccepted']and guard['initializedGuestByteDelta']==79 and
         current.GUEST_SHA==guard['proposedGuestSHA256']and
         all(sha(p)==h for p,h in guard['inputHashes'].items())and
         all(sha(p)==h for p,h in build['input_hashes'].items())and
         sha(ROOT/current.NAME/'mkport_candidate.exe')==current.EXE_SHA and
         sha(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata')==current.PAYLOAD_SHA,
         'Entire immutable compiled repaired source, payload and initialized guest context')
    for name in ('midtunit.cpp','midtunit.h','midtunit_m.cpp'):
        need((ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway'/name).read_bytes()==
             (repair_source.STAGE/name).read_bytes(),'Entire actual compiled source matches the qualified repair')
    observer=(ROOT/previous.OBSERVER).read_text()
    need(observer.count('for n=0,13 do')==observer.count('for channel=0,13 do')==2,
         'Exactly four whole legacy observer loops expand; no audio-window or source-clock edits')
    for name in CONTROLLERS:
        text=(ROOT/name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',text),
             'Every whole transitive controller remains physical-input/passive-observation only')
    wrapper=(ROOT/LUA).read_text()
    need(wrapper.count("source:gsub(")==2 and wrapper.count('assert(count==2)')==2 and
         "dofile('mk2ks_current_cross_tomb_provenance_v5834.lua')" in wrapper and
         'emu.time()>=890' in wrapper,'Same full earned campaign and original failure-only deadline')
    fn=collector(current);channel,gates=channel_models();voice,_=voice_models(current)
    need(fn.__globals__['NAME']==current.NAME and fn.__globals__['current']is current and
         "'-str','900'" in fn.source and "'-nocheat'" in fn.source and
         "'-noautoframeskip','-frameskip','0'" in fn.source,
         'Whole actual host compiles with current candidate, original deadline and native flags')
    paths=[Path(__file__),Path(repaired.__file__),Path(repair_source.__file__),Path(previous.__file__),
        Path(verification.__file__),Path(census.__file__),build_path,repaired.GUARD,
        ROOT/current.NAME/'mkport_candidate.exe',ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata',
        *[ROOT/p for p in CONTROLLERS]]
    report=dict(passed=True,sourceOnlyAccepted=True,wholePythonHostCompiled=True,
        actualNativeLuaParserAccepted=False,nativeGameplayAccepted=False,nativeAudioAccepted=False,
        candidate=current.NAME,guestSHA256=current.GUEST_SHA,executableSHA256=current.EXE_SHA,
        totalSampleChannels=19,entireLegacyObserverRetainedExceptFourChannelBounds=True,
        allEarnedStateBranchVoicePacketDACROMAndWaveformModelsRetained=True,
        transportSourceSHA256=hashlib.sha256(fn.source.encode()).hexdigest().upper(),
        channelGateSHA256=hashlib.sha256(channel.source.encode()).hexdigest().upper(),
        wholeAudioGateSHA256=[hashlib.sha256(g.source.encode()).hexdigest().upper()for g in gates],
        wholeVoiceGateSHA256=hashlib.sha256(voice.source.encode()).hexdigest().upper(),
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],
        inputHashes={str(p.resolve()):sha(p)for p in paths},
        newBuilds=0,newNativeBoots=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        publicPlayableChanged=False,fullPortAcceptance=False,goalStatus='active')
    need(len(report['originalNaturalIntegrationRequirements'])==14 and
         len(report['originalRemainingWorkGroups'])==6,'Whole natural-integration objective retained')
    if SOURCE.exists():need(json.loads((SOURCE/'report.json').read_text())==report,'Immutable source preparation unchanged')
    else:
        SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run(fighter,side):
    need(not census.census(),'Do not launch over or replace an existing native campaign')
    source_guard();current=context()
    leaf=f'audit_native_cross_tomb_19_audio_{fighter}_p{side}'
    scope=dict(vars(repaired),__file__=__file__,INIT=ROOT/(leaf+'_initializer'),
        OLD_INIT=ROOT/(leaf+'_previous_initializer'))
    exec(compile(inspect.getsource(repaired.expectation),__file__+'::whole_repaired_source_initializer','exec'),scope)
    guest,gfx,build,_=scope['expectation']()
    captured=collector(current)(fighter,side,True,guest)
    folder,headers,pcm,dac_chunks,dac_headers,rom_headers,buffers,expected=captured
    RAM.update(captured=captured,guest=guest,gfx=gfx,build=build,folder=folder)
    with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
    need((folder/'stderr.log').read_text()==''and 'MK2_TOMB_SOURCE_HOST_DEADLINE'not in text,
         'Actual complete native earned scene terminal, not a deadline success')
    state=previous.state;branches=branch_models(current);model=previous.model
    native=state.check_log(text,fighter,side,1,guest=guest)
    state_faults=state.actual_faults(text,fighter,side,guest)
    phase=branches.branch(text,guest,fighter,side)
    branch_faults=branches.faults(text,guest,fighter,side)
    voice,voice_faults=branches.voice_proof(text,guest,fighter,side,phase)
    gate,fault=model.dac_models(len(headers))
    dac,dac_faults=gate(dac_chunks,dac_headers,headers),fault(dac_chunks,dac_headers,headers)
    mix_pins={};waveform=model.predict_mix(dac_chunks,dac_headers,pcm,text,fighter,mix_pins)
    need(waveform['passed']and waveform['actualMixedRawPCMByteFaultSuiteAccepted'],
         'Every current mixed PCM sample source-clock exact; no fitting or trimming')
    rg,rf=model.rom_models(expected)
    live=dict(passed=True,nativeEarnedTombState=native,pcmHeaders=headers,dacHeaders=dac_headers,
        soundROMHeaders=rom_headers,actualNativeDACSourceProof=dac,actualDACFaultsRejected=dac_faults,
        actualWholeSoundROMProof=[rg(bytes(buffers[p]),p)for p in ('startup','terminal')],
        actualSoundROMFaultsRejected=[f for p in ('startup','terminal')for f in rf(bytes(buffers[p]),p)],
        waveform=waveform,samplesEnabled=True,importedWinnerMixedWaveformAccepted=True,
        sourceQualifiedNativeBranch=phase,sourceQualifiedNativeRandomBranch=phase,
        actualMixedRawPCMByteFaultSuiteAccepted=True)
    _,gates=channel_models();meta=json.loads((folder/'result.json').read_text())
    positive=gates[bool(phase['nativeDrop'])](text,meta,live,fighter,side,guest,
        (ROOT/'mk2/mk2-maincpu.bin').read_bytes(),expected)
    records=verification.inventory(text)
    terminal=records.get('MK2_CROSS_TOMB_AUDIO_TERMINAL',[])
    pool=records.get('MK2_CROSS_TOMB_AUDIO_POOL',[])
    need(len(terminal)==19 and {int(r['channel'])for r in terminal}==set(range(19))and
         all(r['sample']=='4294967295'and r['writes']=='0'and r['assistance']=='none'for r in terminal)and
         len(pool)==1 and pool[0]['actor']==pool[0]['main']=='00000000'and
         pool[0]['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0',
         'All19 channels and every added priority/owner slot actually retired at native scene terminal')
    report=dict(live,currentCrossTomb19ChannelFiniteAudioAccepted=True,accepted=positive,
        actualEarnedStateFaultsRejected=state_faults,actualBranchFaultsRejected=branch_faults,
        actualLateVictimVoice=voice,actualLateVictimVoiceFaultsRejected=voice_faults,
        mixedWaveformSourceInputHashes=mix_pins,candidate=current.NAME,guestSHA256=current.GUEST_SHA,
        nativeTerminalChannels=terminal,nativeTerminalOwnerPool=pool,
        fullStageArtAccepted=False,allStageFinishersAccepted=False,fullPortAcceptance=False,
        goalStatus='active',newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
    RAM['report']=report
    (folder/'current_19_audio_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteCrossTomb19ChannelAudio=True,
        fighter=fighter,physicalSlot=side,stereoFrames=len(pcm),fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true')
    parser.add_argument('--fighter',choices=('kano','sonya'));parser.add_argument('--side',type=int,choices=(1,2))
    args=parser.parse_args()
    if args.source_only:
        proof=source_guard()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,totalSampleChannels=19,
            wholePythonHostCompiled=True,newNativeBoots=0,nativeAudioAccepted=False)),flush=True)
    else:
        need(args.fighter and args.side,'Actual fighter and physical slot required')
        try:run(args.fighter,args.side)
        except Exception as error:
            folder=RAM.get('folder',ROOT/f'audit_native_cross_tomb_19_audio_{args.fighter}_p{args.side}_samples')
            failure=folder/'current_19_audio_failure.json'
            if folder.exists()and not failure.exists():
                failure.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                    fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual earned Tomb trial; all original raw audio retained only in RAM.',local=dict(RAM=RAM))
