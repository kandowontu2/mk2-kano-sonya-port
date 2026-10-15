"""Whole current19 Tomb preparation with the already-qualified block boundary.

Preserve the predecessor's actual source-preflight failure. Correct only its
use of the obsolete source comparator; no controller or audio contract edits.
"""
import argparse
import code
import hashlib
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_cross_tomb_19_audio as previous
import qualify_native_paired_stumble_table_spacing as spacing

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
SOURCE=ROOT/'audit_native_cross_tomb_19_audio_checked_source'
FAILURE=ROOT/'audit_native_cross_tomb_19_audio_preflight_failure/failure.json'
RAM={}


def functions():
    if not FAILURE.exists():
        try:previous.source_guard()
        except ValueError as error:
            need(str(error)=='Whole driver differs only by new packed table',
                 'Preserve exactly the actual predecessor source-comparison failure')
            FAILURE.parent.mkdir()
            FAILURE.write_text(json.dumps(dict(passed=False,sourceOnlyAccepted=False,
                error=repr(error),traceback=traceback.format_exc(),nativeBoots=0,emulatorBuilds=0,
                inputHashes={str(Path(previous.__file__)):sha(previous.__file__),
                    str(Path(previous.repair_source.__file__)):sha(previous.repair_source.__file__)},
                fullPortAcceptance=False),indent=2)+'\n')
        else:raise ValueError('Expected original preflight failure no longer reproduces')
    failure=json.loads(FAILURE.read_text())
    need(not failure['passed']and failure['nativeBoots']==failure['emulatorBuilds']==0 and
         all(sha(p)==h for p,h in failure['inputHashes'].items()),
         'Exact failed predecessor and unchanged executed sources preserved')
    contract=inspect.getsource(previous.repair_source.source_contract)
    before="first = after.index('\\n\\t' + BEGIN)"
    after="first = after.index('\\n\\n\\t' + BEGIN)"
    need(contract.count(before)==1 and before in inspect.getsource(spacing.run) .replace('\\\\','\\'),
         'Only the previously qualified exact inserted-block boundary')
    scope=dict(vars(previous.repair_source))
    exec(compile(contract.replace(before,after),__file__+'::whole_qualified_source_contract','exec'),scope)
    source=SimpleNamespace(**vars(previous.repair_source))
    source.source_contract=scope['source_contract']
    namespace=dict(vars(previous),__file__=__file__,SOURCE=SOURCE,RAM=RAM,repair_source=source)
    for fn in (previous.context,previous.voice_models,previous.branch_models,previous.channel_models,previous.collector):
        exec(compile(inspect.getsource(fn),__file__+'::whole_current19_'+fn.__name__,'exec'),namespace)
    body=inspect.getsource(previous.source_guard)
    body=previous.once(body,'paths=[Path(__file__),Path(repaired.__file__),',
        'paths=[Path(__file__),Path(previous_file),FAILURE,Path(spacing_file),Path(repaired.__file__),')
    namespace.update(previous_file=previous.__file__,FAILURE=FAILURE,spacing_file=spacing.__file__)
    exec(compile(body,__file__+'::whole_current19_source_guard_with_actual_failure_pins','exec'),namespace)
    exec(compile(inspect.getsource(previous.run),__file__+'::whole_current19_runtime','exec'),namespace)
    return namespace


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true')
    parser.add_argument('--fighter',choices=('kano','sonya'));parser.add_argument('--side',type=int,choices=(1,2))
    args=parser.parse_args();scope=functions()
    if args.source_only:
        proof=scope['source_guard']()
        print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,totalSampleChannels=19,
            wholePythonHostCompiled=True,newNativeBoots=0,nativeAudioAccepted=False)),flush=True)
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
        code.interact(banner='Same actual earned Tomb trial; complete raw audio stays in RAM.',local=dict(RAM=RAM))
