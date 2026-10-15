"""Current whole guest / seven earned matches / full native Pit 19-channel mix.

Retain the complete canonical RAM collector, Pit-specific 5785 window/packet/
DAC/ROM/waveform gate and all 29 actual faults; extend only passive bounds.
Voice/cue/priority ownership and later visible clearing are separate open gates.
"""
import argparse
import code
import gzip
import hashlib
import inspect
import json
import re
import textwrap
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_cross_tomb_19_audio_manifest_checked as prepared
import verify_current_cross_pit_winner_mix_v5898 as pit
import native_process_census_v6647 as census

ROOT, need, sha = prepared.ROOT, prepared.need, prepared.sha
once = prepared.original.once
SOURCE = ROOT / 'audit_native_current_cross_pit_19_audio_source'
PREFIX = 'audit_native_current_cross_pit_19_audio_'
LUA = 'mk2ks_native_cross_pit_19_audio.lua'
RAM = {}


def functions():
    parent = prepared.functions()
    current = parent['context']()
    namespace = dict(vars(pit.observed), current=current, model=pit.host.model,
                     state=pit.host.state, runtime=SimpleNamespace(state=pit.host.state))
    observed = SimpleNamespace(**namespace)
    channel_body = inspect.getsource(pit.original.channel_gate)
    channel_body = once(channel_body, 'len(precise)==14*len(pcm)', 'len(precise)==19*len(pcm)')
    channel_body = once(channel_body, 'range(14)', 'range(19)')
    scope = dict(pit.channel_gate.__globals__, observed=observed)
    exec(compile(channel_body, __file__+'::whole_precise_19channel_gate', 'exec'), scope)
    gate_body = once(pit.gate.source, 'len(channels)==len(pairs)==14*1100', 'len(channels)==len(pairs)==19*1100')
    gate_body = once(gate_body, 'range(14)', 'range(19)')
    gates = dict(pit.gate.__globals__, observed=observed, channel_gate=scope['channel_gate'])
    exec(compile(gate_body, __file__+'::whole_Pit_window_19channel_gate', 'exec'), gates)
    gate = gates['gate']
    start = pit.run.source.index('   positive=gate(')
    stop = pit.run.source.index('   need(not any(p.suffix', start)
    faults_body = 'def check_faults(text,meta,live,fighter,side,guest,stock,expected):\n'
    faults_body += textwrap.indent(textwrap.dedent(pit.run.source[start:stop]), '    ')
    faults_body += '    return positive\n'
    fault_scope = dict(pit.run.__globals__, observed=observed, gate=gate)
    exec(compile(faults_body, __file__+'::whole_original_29_Pit_audio_faults', 'exec'), fault_scope)
    old = parent['collector'](current)
    body = once(old.source, prepared.PREFIX, PREFIX)
    body = once(body, prepared.original.LUA, LUA)
    body = once(body, "MK2KS_STAGE_ARENA='1'", "MK2KS_STAGE_ARENA='6'")
    body = once(body, '    files.update(ROOT/p for p in CONTROLLERS)',
                '    files.update(ROOT/p for p in CONTROLLERS)\n'
                '    files.update(Path(p)for p in SOURCE_PINS)')
    collector_scope = dict(old.__globals__, __file__=__file__, source=SimpleNamespace(OUT=SOURCE, __file__=__file__),
                           state=pit.host.state, OBSERVER=LUA,
                           CONTROLLERS=parent['CONTROLLERS']+(LUA,), SOURCE_PINS={})
    exec(compile(body, __file__+'::whole_current_native_Pit_19_RAM_collector', 'exec'), collector_scope)
    fn = collector_scope['capture']
    fn.source = body
    return dict(parent=parent, current=current, gate=gate, channel=scope['channel_gate'],
                check_faults=fault_scope['check_faults'], collector=fn, channel_body=channel_body,
                gate_body=gate_body, faults_body=faults_body)


def preflight(scope, fighter, side):
    qualified = scope['parent']['source_guard']()
    need(qualified['passed'] and qualified['sourceOnlyAccepted'], 'Entire current compiled guest and source guard')
    need(not census.census(), 'No overlapping or replaced native campaign')
    old_lua = (ROOT/prepared.original.LUA).read_text()
    insertion = """local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'",
 "0xff8bdde0,0xff8bddef,'actual native Pit audio origin'")
replace('at~=0xff8bdfe0','at~=0xff8bdde0')
"""
    expected = once(old_lua, 'opposite-character Tomb', 'opposite-character Pit')
    expected = once(expected, "assert(load(source,'@complete5779_cross_tomb_all19_channels'", insertion+"assert(load(source,'@complete5779_cross_tomb_all19_channels'")
    need((ROOT/LUA).read_text() == expected, 'Entire already qualified19 observer retained except two exact Pit origin literals')
    observer = (ROOT/prepared.original.previous.OBSERVER).read_text()
    observer = observer.replace('for n=0,13 do', 'for n=0,18 do').replace('for channel=0,13 do', 'for channel=0,18 do')
    observer = once(observer, "0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'",
                    "0xff8bdde0,0xff8bddef,'actual native Pit audio origin'")
    observer = once(observer, 'at~=0xff8bdfe0', 'at~=0xff8bdde0')
    need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|snapshot\(|force_update|flush\(', observer),
         'Entire actual DAC/ROM/PCM/19channel observer is passive')
    pins = dict(qualified['inputHashes'])
    for relative in ('audit_native_current_cross_pit_render_matrix_checked/report.json',
                     'audit_native_cross_tomb_19_audio_matrix_checked/report.json',
                     'audit_v5899_current_cross_pit_winner_mix_checked/report.json'):
        path = ROOT/relative
        proof = json.loads(path.read_text())
        need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()), 'Frozen actual predecessor proof '+relative)
        for p,h in proof['inputHashes'].items():
            need(p not in pins or pins[p]==h, 'Consistent original source pins')
            pins[p]=h
        pins[str(path)] = sha(path)
    for path in (Path(__file__).resolve(), ROOT/LUA, Path(pit.__file__).resolve(),
                 Path(pit.host.state.__file__).resolve(), prepared.SOURCE/'report.json'):
        pins[str(path)] = sha(path)
    old_folder = ROOT/'audit_v5897_current_cross_pit_winner_mix_kano_p1_samples'
    with gzip.open(old_folder/'run.log.gz','rt') as reader:
        old_text = reader.read()
    old_live = json.loads((old_folder/'audio_live_source_model.json').read_text())
    records = pit.inventory(old_text)
    need(pit.channel_gate(records,old_live['pcmHeaders'],old_live,'kano')['passed'], 'Original14-channel Pit receipt valid only at original scope')
    try:
        scope['channel'](records,old_live['pcmHeaders'],old_live,'kano')
    except ValueError as error:
        need(str(error).startswith('All14 precise states'), 'Old14 capture rejects for missing five actual channels')
    else:
        raise ValueError('Historical14-channel Pit admitted as current19 observation')
    fn=scope['collector']
    fn.__globals__['SOURCE_PINS']=pins
    proof=dict(passed=True, sourceOnlyAccepted=True, candidate=scope['current'].NAME,
               guestSHA256=scope['current'].GUEST_SHA, totalSampleChannels=19,
               actualPitWaveformAccepted=False, cinematicVictimAudioOwnershipAccepted=False,
               allNativePitCuePriorityAndRNGAccepted=False, fullPortAcceptance=False,
               originalNaturalIntegrationRequirements=qualified['originalNaturalIntegrationRequirements'],
               originalRemainingWorkGroups=qualified['originalRemainingWorkGroups'],
               inputHashes=pins, transportSourceSHA256=hashlib.sha256(fn.source.encode()).hexdigest().upper(),
               wholeChannelGateSHA256=hashlib.sha256(scope['channel_body'].encode()).hexdigest().upper(),
               wholePitGateSHA256=hashlib.sha256(scope['gate_body'].encode()).hexdigest().upper(),
               whole29FaultBodySHA256=hashlib.sha256(scope['faults_body'].encode()).hexdigest().upper(),
               newNativeBoots=0, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
               publicPlayableChanged=False, goalStatus='active')
    need(len(proof['originalNaturalIntegrationRequirements'])==14 and len(proof['originalRemainingWorkGroups'])==6, 'Full objective unchanged')
    if SOURCE.exists():
        need(json.loads((SOURCE/'report.json').read_text())==proof, 'Immutable source-only proof')
    else:
        SOURCE.mkdir(); (SOURCE/'report.json').write_text(json.dumps(proof,indent=2)+'\n')
    prefix=fn.source[:fn.source.index('    folder.mkdir();')]+'    return len(files),pins\n'
    namespace=dict(fn.__globals__)
    exec(compile(prefix,__file__+'::whole_actual_requested_case_manifest','exec'),namespace)
    count,actual_pins=namespace['capture'](fighter,side,True,None)
    need(count>100 and all(sha(p)==h for p,h in actual_pins.items()), 'Entire requested current Pit input manifest before boot')
    print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,fighter=fighter,side=side,
                         actualManifestFiles=count,totalSampleChannels=19,newNativeBoots=0)),flush=True)
    return proof


def run(scope, fighter, side):
    preflight(scope,fighter,side)
    repaired=prepared.original.repaired
    leaf=f'{PREFIX}{fighter}_p{side}'
    namespace=dict(vars(repaired),__file__=__file__,INIT=ROOT/(leaf+'_initializer'),OLD_INIT=ROOT/(leaf+'_previous_initializer'))
    exec(compile(inspect.getsource(repaired.expectation),__file__+'::whole_current_independent_initializer','exec'),namespace)
    guest,gfx,build,_=namespace['expectation']()
    captured=scope['collector'](fighter,side,True,guest)
    folder,headers,pcm,chunks,dac,rom,buffers,expected=captured
    RAM.update(captured=captured,guest=guest,gfx=gfx,build=build,folder=folder)
    with gzip.open(folder/'run.log.gz','rt') as reader:text=reader.read()
    need((folder/'stderr.log').read_text()=='' and 'MK2_TOMB_SOURCE_HOST_DEADLINE'not in text, 'Real original native terminal, never deadline success')
    state,model=pit.host.state,pit.host.model
    native=state.check_log(text,fighter,side,6,guest=guest)
    earned=state.actual_faults(text,fighter,side,guest)
    gate,fault=model.dac_models(len(headers))
    dac_proof,dac_faults=gate(chunks,dac,headers),fault(chunks,dac,headers)
    mix_pins={};waveform=model.predict_mix(chunks,dac,pcm,text,fighter,mix_pins)
    need(waveform['passed'] and waveform['actualMixedRawPCMByteFaultSuiteAccepted'], 'Entire source-exact mixed PCM; no fitting or trimming')
    rg,rf=model.rom_models(expected)
    live=dict(passed=True,nativeEarnedPitState=native,pcmHeaders=headers,dacHeaders=dac,soundROMHeaders=rom,
              actualNativeDACSourceProof=dac_proof,actualDACFaultsRejected=dac_faults,
              actualWholeSoundROMProof=[rg(bytes(buffers[p]),p)for p in ('startup','terminal')],
              actualSoundROMFaultsRejected=[f for p in ('startup','terminal')for f in rf(bytes(buffers[p]),p)],
              waveform=waveform,samplesEnabled=True,importedWinnerMixedWaveformAccepted=True,
              actualMixedRawPCMByteFaultSuiteAccepted=True,actualEarnedStateFaultsRejected=earned)
    meta=json.loads((folder/'result.json').read_text())
    accepted=scope['check_faults'](text,meta,live,fighter,side,guest,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),expected)
    records=pit.inventory(text)
    terminal=records.get('MK2_CROSS_TOMB_AUDIO_TERMINAL',[]);pool=records.get('MK2_CROSS_TOMB_AUDIO_POOL',[])
    need(len(terminal)==19 and {int(r['channel'])for r in terminal}==set(range(19)) and
         all(r['sample']=='4294967295' and r['writes']=='0' and r['assistance']=='none'for r in terminal) and
         len(pool)==1 and pool[0]['actor']==pool[0]['main']=='00000000' and
         pool[0]['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0', 'All19 channels and five priority owners retired at actual terminal')
    current=scope['current']
    report=dict(live,currentCrossPit19ChannelFiniteAudioAccepted=True,accepted=accepted,
                mixedWaveformSourceInputHashes=mix_pins,candidate=current.NAME,guestSHA256=current.GUEST_SHA,
                nativeTerminalChannels=terminal,nativeTerminalOwnerPool=pool,
                cinematicVictimAudioOwnershipAccepted=False,allNativePitCuePriorityAndRNGAccepted=False,
                fullStageArtAccepted=False,allStageFinishersAccepted=False,fullPortAcceptance=False,
                goalStatus='active',newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
    RAM['report']=report
    (folder/'current_19_audio_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteCurrentCrossPit19ChannelAudio=True,fighter=fighter,
                         physicalSlot=side,stereoFrames=len(pcm),originalAudioWindowFaults=len(accepted['actualAudioSourceWindowFaultsRejected']),
                         fullPortAcceptance=False)),flush=True)
    return report


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
        if folder.exists()and not(folder/'current_19_audio_failure.json').exists():
            (folder/'current_19_audio_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
        else:
            target=ROOT/'audit_native_current_cross_pit_19_audio_preflight_failure'
            if not target.exists():target.mkdir();(target/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure),flush=True)
        if args.source_only:raise SystemExit(1)
    if not args.source_only:
        code.interact(banner='Same actual current Pit capture; original sound retained only in RAM.',local=dict(RAM=RAM))
