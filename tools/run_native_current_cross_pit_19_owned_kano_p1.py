"""Complete native19/owner/RNG KanoP1 capture after its retired baseline.

The old waveform baseline is immutable and already retired. Retain its entire
source preflight, but run the requested fresh manifest on the actual additive
owned capture, not on the already completed baseline directory. No guest writes,
new emulator build, ROM copy or raw media output.
"""
import code
import inspect
import json
import traceback
from pathlib import Path
from types import SimpleNamespace
import run_native_current_cross_pit_19_owned_audio as owned

ROOT,need,sha,once=owned.ROOT,owned.need,owned.sha,owned.once
SOURCE=ROOT/'audit_native_current_cross_pit_19_owned_kano_p1_source'
RAM={}


def original_source_preflight(fighter,side):
    need((fighter,side)==('kano',1),'Only missing actual KanoP1 owned context')
    baseline=ROOT/'audit_native_current_cross_pit_19_audio_kano_p1_samples'
    retired=json.loads((baseline/'current_19_audio_ram_retirement.json').read_text())
    need(retired['passed'] and retired['originalCaptureRAMDictionaryCleared'] and
         retired['originalStereoFrames']==965760 and
         all(sha(p)==h for p,h in retired['inputHashes'].items()),
         'Completed baseline remains fully retired and unchanged')
    # Every original compiled/source/observer/frozen-proof guard above this
    # block is retained. The whole requested manifest runs in owned preflight.
    body=inspect.getsource(owned.original.preflight)
    boundary="    prefix=fn.source[:fn.source.index('    folder.mkdir();')]"
    need(body.count(boundary)==1,'Exact original final manifest boundary')
    prefix=body[:body.index(boundary)]+'    return proof\n'
    scope=dict(vars(owned.original))
    exec(compile(prefix,__file__+'::entire_original_source_preflight','exec'),scope)
    return scope['preflight'](owned.original.functions(),fighter,side)


def preflight(scope,fighter,side):
    body=inspect.getsource(owned.preflight)
    body=once(body,'original.preflight(original.functions(),fighter,side)',
              'original_source_preflight(fighter,side)')
    body=once(body,'for p in(Path(__file__),Path(original.__file__),',
              'for p in(Path(__file__),Path(owned.__file__),Path(original.__file__),')
    namespace=dict(vars(owned),__file__=__file__,SOURCE=SOURCE,
                   original_source_preflight=original_source_preflight,owned=owned)
    exec(compile(body,__file__+'::entire_owned_actual_requested_manifest_preflight','exec'),namespace)
    return namespace['preflight'](scope,fighter,side)


def run():
    scope=owned.functions()
    scope['collector'].__globals__['source']=SimpleNamespace(OUT=SOURCE,__file__=__file__)
    # Retain the complete initialized runtime and all29 real audio faults.
    body=inspect.getsource(owned.original.run)
    before="accepted=scope['check_faults'](text,meta,live,fighter,side,guest,(ROOT/'mk2/mk2-maincpu.bin').read_bytes(),expected)"
    body=once(body,before,before[:-1]+',folder)')
    body=once(body,"    RAM['report']=report",
        "    report.update(passiveCinematicOwnershipAndQueueRNGCaptured=True,actualAddedOwnedObserverQualificationAccepted=False)\n"
        "    RAM['report']=report")
    namespace=dict(vars(owned.original),__file__=__file__,PREFIX=owned.PREFIX,
                   SOURCE=SOURCE,LUA=owned.LUA,RAM=RAM,preflight=preflight)
    exec(compile(body,__file__+'::whole_original_native19_runtime','exec'),namespace)
    return namespace['run'](scope,'kano',1)


if __name__=='__main__':
    try:run()
    except Exception as error:
        folder=RAM.get('folder',ROOT/f'{owned.PREFIX}kano_p1_samples')
        if not folder.exists():folder=ROOT/'audit_native_current_owned_kano_p1_preflight_failure'
        folder.mkdir(exist_ok=True)
        failure=folder/'current_19_audio_failure.json'
        need(not failure.exists(),'Preserve every actual failure without replacement')
        failure.write_text(json.dumps(dict(passed=False,error=repr(error),
            traceback=traceback.format_exc(),fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
        print(failure.read_text(),flush=True)
    code.interact(banner='Same actual KanoP1 owned capture; sound remains in RAM.',local=dict(RAM=RAM))
