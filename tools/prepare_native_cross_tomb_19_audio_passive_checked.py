"""Preserve passive-scan false positive; retain both literal no-write guards.

The old wrappers contain ':write_' only as a literal forbidden by asserts.
Mask those two exact inspected literals, never an actual game-writing call.
No source/controller edits, new native boot or audio acceptance from preflight.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
import prepare_native_cross_tomb_19_audio_checked as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
SOURCE=ROOT/'audit_native_cross_tomb_19_audio_passive_checked_source'
FAILURE=ROOT/'audit_native_cross_tomb_19_audio_passive_scan_failure/failure.json'
RAM={}


def functions():
    if not FAILURE.exists():
        try:previous.functions()['source_guard']()
        except ValueError as error:
            need(str(error)=='Every whole transitive controller remains physical-input/passive-observation only',
                 'Exact predecessor literal-scan failure reproduced')
            FAILURE.parent.mkdir()
            FAILURE.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                nativeBoots=0,emulatorBuilds=0,inputHashes={str(Path(previous.__file__)):sha(previous.__file__),
                str(Path(previous.previous.__file__)):sha(previous.previous.__file__)},fullPortAcceptance=False),indent=2)+'\n')
        else:raise ValueError('Predecessor literal-scan failure no longer reproduces')
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and all(sha(p)==h for p,h in failed['inputHashes'].items()),
         'Whole failed source preparation preserved')
    factory=dict(vars(previous),__file__=__file__,SOURCE=SOURCE,RAM=RAM)
    exec(compile(inspect.getsource(previous.functions),__file__+'::whole_checked_factory','exec'),factory)
    scope=factory['functions']()
    original=previous.previous
    literal="source:find(':write_',1,true)"
    for name in ('mk2ks_current_cross_tomb_driver_v5833.lua','mk2ks_current_cross_tomb_provenance_v5834.lua'):
        text=(ROOT/name).read_text()
        need(text.count(literal)==1 and 'assert(not '+literal in text,
             'Each sole quoted guard is the unchanged assert forbidding game writes')
    body=inspect.getsource(original.source_guard)
    body=original.once(body,'text=(ROOT/name).read_text()',
        'text=(ROOT/name).read_text()\n        text=text.replace("source:find(\':write_\',1,true)","source:find(\'passive_no_write_guard\',1,true)")')
    body=original.once(body,'paths=[Path(__file__),Path(repaired.__file__),',
        'paths=[Path(__file__),Path(original_file),Path(checked_file),FAILURE,source_failure,Path(spacing_file),Path(repaired.__file__),')
    scope.update(original_file=original.__file__,checked_file=previous.__file__,FAILURE=FAILURE,
        source_failure=previous.FAILURE,spacing_file=previous.spacing.__file__)
    exec(compile(body,__file__+'::whole_source_preflight_exact_literal_guard_scan','exec'),scope)
    return scope


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
        code.interact(banner='Same actual earned Tomb trial; complete raw audio remains in RAM.',local=dict(RAM=RAM))
