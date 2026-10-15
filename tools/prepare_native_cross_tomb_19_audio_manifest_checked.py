"""Whole current19 Tomb; manifest source namespace includes its real file.

Preserve the original pre-boot AttributeError. Exercise the entire actual
input-manifest prefix before native boot, not just compile the Python body.
"""
import argparse
import code
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_cross_tomb_19_audio_context_checked as previous
import prepare_native_cross_tomb_19_audio as original

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
SOURCE=ROOT/'audit_native_cross_tomb_19_audio_manifest_checked_source'
FAILURE=ROOT/'audit_native_cross_tomb_19_audio_manifest_failure/failure.json'
RAM={}
PREFIX='audit_native_cross_tomb_19_audio_manifest_checked_'


def functions():
    scope=previous.functions()
    prior_report=previous.SOURCE/'report.json'
    qualified=json.loads(prior_report.read_text())
    need(qualified['passed']and all(sha(p)==h for p,h in qualified['inputHashes'].items()),
         'Whole current19 source, precise gates and current victim-voice context frozen')
    old_collector=scope['collector']
    if not FAILURE.exists():
        fn=old_collector(scope['context']())
        need(not hasattr(fn.__globals__['source'],'__file__'),'Exact original manifest namespace defect')
        try:fn('kano',1,True,None)
        except AttributeError as error:
            need("has no attribute '__file__'" in str(error),'Same actual pre-boot manifest failure')
            FAILURE.parent.mkdir();FAILURE.write_text(json.dumps(dict(passed=False,error=repr(error),
                traceback=traceback.format_exc(),failureBeforeNativeBoot=True,nativeBoots=0,
                initializedGuestArgumentNotReached=True,inputHashes={str(Path(previous.__file__)):sha(previous.__file__),
                    str(Path(original.__file__)):sha(original.__file__),str(prior_report):sha(prior_report)},
                fullPortAcceptance=False),indent=2)+'\n')
        else:raise ValueError('Original pre-boot manifest failure no longer reproduces')
    failed=json.loads(FAILURE.read_text())
    need(not failed['passed']and all(sha(p)==h for p,h in failed['inputHashes'].items()),'Original failed manifest inputs preserved')
    scope.update(__file__=__file__,SOURCE=SOURCE,RAM=RAM,manifest_failure=FAILURE,
        context_file=previous.__file__,context_report=prior_report)
    def collector(current):
        fn=old_collector(current)
        body=original.once(fn.source,'audit_native_cross_tomb_19_audio_',PREFIX)
        namespace=dict(fn.__globals__,__file__=__file__,source=SimpleNamespace(OUT=SOURCE,__file__=__file__))
        exec(compile(body,__file__+'::whole_actual_collector_with_complete_manifest_namespace','exec'),namespace)
        result=namespace['capture'];result.source=body;return result
    scope['collector']=collector
    body=inspect.getsource(original.source_guard)
    body=original.once(body,'text=(ROOT/name).read_text()',
        'text=(ROOT/name).read_text()\n        text=text.replace("source:find(\':write_\',1,true)","source:find(\'passive_no_write_guard\',1,true)")')
    body=original.once(body,'paths=[Path(__file__),Path(repaired.__file__),',
        'paths=[Path(__file__),Path(context_file),context_report,manifest_failure,Path(original_file),Path(checked_file),Path(passive_file),previous_path,old_live_path,old_folder/"run.log.gz",FAILURE,source_failure,Path(spacing_file),Path(repaired.__file__),')
    exec(compile(body,__file__+'::whole_current19_manifest_source_preflight','exec'),scope)
    body=original.once(inspect.getsource(original.run),'audit_native_cross_tomb_19_audio_',PREFIX)
    exec(compile(body,__file__+'::whole_current19_fresh_manifest_runtime','exec'),scope)
    return scope


def preflight(scope):
    proof=scope['source_guard']()
    fn=scope['collector'](scope['context']())
    body=fn.source
    before=body.index('    folder.mkdir();')
    prefix=body[:before]+'    return len(files),pins\n'
    namespace=dict(fn.__globals__)
    exec(compile(prefix,__file__+'::whole_actual_input_manifest_before_native_boot','exec'),namespace)
    count,pins=namespace['capture']('kano',1,True,None)
    need(count>100 and all(sha(p)==h for p,h in pins.items()),'Entire real compiled/observer/model/media manifest validates without boot')
    print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,totalSampleChannels=19,
        actualWholeInputManifestFiles=count,newNativeBoots=0,nativeAudioAccepted=False)),flush=True)
    return proof


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true')
    parser.add_argument('--fighter',choices=('kano','sonya'));parser.add_argument('--side',type=int,choices=(1,2))
    args=parser.parse_args();scope=functions();preflight(scope)
    if not args.source_only:
        need(args.fighter and args.side,'Actual fighter and physical slot required')
        try:scope['run'](args.fighter,args.side)
        except Exception as error:
            folder=RAM.get('folder',ROOT/f'{PREFIX}{args.fighter}_p{args.side}_samples')
            failure=folder/'current_19_audio_failure.json'
            if folder.exists()and not failure.exists():
                failure.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                    fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        code.interact(banner='Same actual current Tomb trial; original raw sound remains in RAM.',local=dict(RAM=RAM))
