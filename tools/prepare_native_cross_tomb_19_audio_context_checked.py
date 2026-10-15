"""Bind both whole19-channel gates to the current victim-voice context.

Conserve all waveform and branch algorithms. The late-drop gate must not keep
the historical whole-guest SHA through a transitive observed.voice_models alias.
Legacy actual14-channel captures are explicitly rejected as current19 coverage.
"""
import argparse
import code
import gzip
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_cross_tomb_19_audio_passive_checked as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
SOURCE=ROOT/'audit_native_cross_tomb_19_audio_context_checked_source'
RAM={}


def functions():
    previous_path=previous.SOURCE/'report.json'
    previous_proof=json.loads(previous_path.read_text())
    need(previous_proof['passed']and previous_proof['sourceOnlyAccepted']and
         all(sha(p)==h for p,h in previous_proof['inputHashes'].items()),
         'Entire qualified passive19 observer and compiled host unchanged')
    factory=dict(vars(previous),__file__=__file__,SOURCE=SOURCE,RAM=RAM)
    exec(compile(inspect.getsource(previous.functions),__file__+'::whole_passive_factory','exec'),factory)
    scope=factory['functions']()
    original=previous.previous.previous
    observed=SimpleNamespace(**vars(original.verification.observed))
    current=scope['context']()
    observed.current=current
    observed.voice_models=lambda:scope['voice_models'](current)
    branches=scope['branch_models'](current)
    body=inspect.getsource(original.channel_models)
    body=original.once(body,'observed=verification.observed','observed=observed')
    body=original.once(body,'scope=dict(original.__globals__,channel_gate=channel)',
        'scope=dict(original.__globals__,channel_gate=channel,observed=observed,branches=branches)')
    body=original.once(body,"exec(compile(body,__file__+'::whole_precise_channel_gate_expanded_to19','exec'),scope)",
        "body=body.replace('All14','All19')\n    exec(compile(body,__file__+'::whole_precise_channel_gate_expanded_to19','exec'),scope)")
    body=original.once(body,"exec(compile(body,__file__+'::whole_cross_audio_gate_expanded_to19','exec'),scope)",
        "body=body.replace('Every14','Every19')\n        exec(compile(body,__file__+'::whole_cross_audio_gate_expanded_to19','exec'),scope)")
    scope.update(observed=observed,branches=branches)
    exec(compile(body,__file__+'::whole19_gates_current_voice_globals','exec'),scope)
    channel,gates=scope['channel_models']()
    need(all(g.__globals__['observed']is observed and g.__globals__['branches']is branches for g in gates),
         'Both held and random-drop entire gates use actual current voice/guest context')
    voice,_=observed.voice_models()
    need(repr(current.GUEST_SHA)in voice.source and repr(original.previous.current.GUEST_SHA)not in voice.source,
         'Only actual current whole-guest SHA in complete late victim-voice gate')
    # Real historical full captures must pass their original channel gate,
    # but cannot stand in for observations of five channels added afterwards.
    old_folder=ROOT/'audit_v5841_current_cross_tomb_winner_mix_kano_p1_samples'
    old_live_path=old_folder/'audio_live_source_model.json'
    old_live=json.loads(old_live_path.read_text())
    with gzip.open(old_folder/'run.log.gz','rt')as reader:old_text=reader.read()
    records=original.verification.inventory(old_text)
    old_channel=original.verification.channel_gate(records,old_live['pcmHeaders'],old_live,'kano')
    need(old_channel['passed'],'Original real full14-channel source-clock receipt remains valid at its original scope')
    try:channel(records,old_live['pcmHeaders'],old_live,'kano')
    except ValueError as error:
        need(str(error).startswith('All19 precise states'),'Legacy capture rejects specifically for missing current channels')
    else:raise ValueError('Historical14-channel capture admitted as actual19-channel coverage')
    # Rebuild the entire same source guard only to bind this successor and
    # its tested historical inputs, not to change runtime or source contracts.
    body=inspect.getsource(original.source_guard)
    body=original.once(body,'text=(ROOT/name).read_text()',
        'text=(ROOT/name).read_text()\n        text=text.replace("source:find(\':write_\',1,true)","source:find(\'passive_no_write_guard\',1,true)")')
    body=original.once(body,'paths=[Path(__file__),Path(repaired.__file__),',
        'paths=[Path(__file__),Path(original_file),Path(checked_file),Path(passive_file),previous_path,old_live_path,old_folder/"run.log.gz",FAILURE,source_failure,Path(spacing_file),Path(repaired.__file__),')
    scope.update(passive_file=previous.__file__,previous_path=previous_path,old_live_path=old_live_path,old_folder=old_folder,
        FAILURE=previous.FAILURE,source_failure=previous.previous.FAILURE)
    exec(compile(body,__file__+'::whole_current19_context_and_legacy_scope_source_guard','exec'),scope)
    return scope


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true')
    parser.add_argument('--fighter',choices=('kano','sonya'));parser.add_argument('--side',type=int,choices=(1,2))
    args=parser.parse_args();scope=functions()
    if args.source_only:
        proof=scope['source_guard']()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,totalSampleChannels=19,
            wholePythonHostCompiled=True,wholeCurrentVoiceContextBound=True,
            historical14ChannelCoverageNotSubstituted=True,newNativeBoots=0,nativeAudioAccepted=False)),flush=True)
    else:
        need(args.fighter and args.side,'Actual fighter and physical slot required')
        try:scope['run'](args.fighter,args.side)
        except Exception as error:
            folder=RAM.get('folder',ROOT/f'audit_native_cross_tomb_19_audio_{args.fighter}_p{args.side}_samples')
            failure=folder/'current_19_audio_failure.json'
            if folder.exists()and not failure.exists():
                failure.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                    fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual current Tomb trial; complete raw audio retained only in RAM.',local=dict(RAM=RAM))
