"""Fresh original close-approach human-input trials after a terminal guarded KO.

Do not replay or qualify the guarded loss as paired-contact success. Both
original human strategies are physical inputs only; all gates stay intact.
"""
import code
import gzip
import inspect
import json
import traceback
import capture_native_kano_laser_cpu_choke_shadow as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
BASE=ROOT/'audit_native_kano_laser_cpu_choke_approach_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_choke_approach_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_choke_approach_initializer_source'


def run():
    failed=ROOT/'audit_native_kano_laser_cpu_choke_shadow_ram/choke_cpu_kano_human_kano/result.json'
    failure=json.loads(failed.read_text())
    need(not failure['passed'] and failure['nativeExit']==0 and
         not failure['nativeTerminal']['hostDecodeErrors'] and not prior.base.identity.census(),
         'Exact preceding guarded native trial terminal; preserve rejection and never replay')
    with gzip.open(failed.parent/'run.log.gz','rt')as file:text=file.read()
    fields=prior.cpu_body.cpu.original.rows(text,'FIELD')
    need(fields[-1]['vhp']==0 and fields[-1]['hp']==161 and fields[-1]['id']==fields[-1]['vid']==17 and
         not prior.cpu_body.cpu.original.rows(text,'COMPLETE'), 'Guarded KO, not claimed complete paired choreography')
    def qualified():
        path=prior.GUARD/'report.json';guard=json.loads(path.read_text())
        need(guard['passed'] and guard['actualNativeParserAccepted'] and
             guard['wholePhysicalCPUUnchangedExceptSixSinks'] and not guard['gameplayAccepted'] and
             all(sha(p)==h for p,h in guard['inputHashes'].items()), 'Whole identical native-compiled controller')
        for p in(failed,failed.parent/'native_terminal.json',ROOT/'tools/capture_native_kano_laser_cpu_choke_shadow_terminal.py',
                 ROOT/'audit_native_kano_laser_cpu_choke_shadow_terminal_checked/failure.json',
                 ROOT/'audit_native_kano_laser_cpu_choke_shadow_checked/failure.json'):
            guard['inputHashes'][str(p.resolve())]=sha(p)
        return guard
    source=inspect.getsource(prior.run)
    need(source.count('line.startswith(')==2, 'Exactly two preserved host predicate corrections')
    source=source.replace('line.startswith(','s.startswith(')
    need(source.count("MK2KS_CPU_PAIR_APPROACH='guard_until_close'")==1,'Only original physical human strategy option changes')
    source=source.replace("MK2KS_CPU_PAIR_APPROACH='guard_until_close'","MK2KS_CPU_PAIR_APPROACH='original'")
    scope=dict(vars(prior),BASE=BASE,OUT=OUT,INIT=INIT,__file__=__file__,qualify=qualified)
    exec(compile(source,__file__+'::whole_original_native_CPU_capture_existing_close_approach_inputs','exec'),scope)
    scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Immutable fresh-strategy rejection')
        OUT.mkdir();prior.base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                                         fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=prior.base.preview.serve(prior.RAM_CASES)
    code.interact(banner='Fresh physical close-approach trials; preceding guarded KO remains rejected.',
                  local=dict(cases=prior.RAM_CASES,server=server,module=__import__(__name__)))
