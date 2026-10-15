"""Correct the host adapter's source-variable spelling; preserve its preflight failure.

No physical gameplay job was dispatched by the original host. Reuse the
already-terminal actual native compiler proof; keep all original gates.
"""
import code
import inspect
import json
import traceback
import capture_native_kano_laser_cpu_choke_shadow as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_cpu_choke_shadow_terminal_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_choke_terminal_initializer_source'


def run():
    failed=prior.OUT/'failure.json'
    failure=json.loads(failed.read_text())
    need(not failure['passed'] and 'adapter boundary line.startswith'in failure['error'] and
         not prior.BASE.exists(), 'Original actual pre-dispatch host failure retained, no gameplay terminal to replay')
    def qualified():
        path=prior.GUARD/'report.json'
        guard=json.loads(path.read_text())
        need(guard['passed'] and guard['actualNativeParserAccepted'] and
             guard['wholePhysicalCPUUnchangedExceptSixSinks'] and not guard['gameplayAccepted'] and
             all(sha(p)==h for p,h in guard['inputHashes'].items()), 'Same actual full-source native compiler proof')
        # Pins bind the preserved original rejection and this explicit successor.
        guard['inputHashes'].update({str(p.resolve()):sha(p)for p in(failed,prior.GUARD/'native_terminal.json')})
        return guard
    source=inspect.getsource(prior.run)
    need(source.count('line.startswith(')==2, 'Exactly both host predicate source spellings')
    source=source.replace('line.startswith(','s.startswith(')
    scope=dict(vars(prior),OUT=OUT,INIT=INIT,__file__=__file__,qualify=qualified)
    exec(compile(source,__file__+'::whole_original_capture_with_two_host_spelling_corrections','exec'),scope)
    scope['run']()


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Immutable successor rejection')
        OUT.mkdir();prior.base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                                         fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=prior.base.preview.serve(prior.RAM_CASES)
    code.interact(banner='Same actual CPU mirror/cross captures retained; no native replay.',
                  local=dict(cases=prior.RAM_CASES,server=server,module=__import__(__name__)))
