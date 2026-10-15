"""Preserve the source-kind mismatch; bind host, Python and Lua separately."""
import inspect
import json
import traceback
from pathlib import Path
import retire_native_kano_kitana_independent_policy as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
FAILURE=ROOT/'audit_native_kano_kitana_retirement_source_kind_failure/failure.json'


def preserve():
    if not FAILURE.exists():
        try:previous.preserve()
        except ValueError as error:
            need(str(error)=='Entire original executed host independently reconstructed and bound to actual guest receipt',
                 'Exact original host-versus-Lua hash mismatch preserved')
            FAILURE.parent.mkdir();FAILURE.write_text(json.dumps(dict(passed=False,error=repr(error),
                traceback=traceback.format_exc(),inputHashes={str(Path(previous.__file__)):sha(previous.__file__)},
                fullPortAcceptance=False),indent=2)+'\n')
        else:raise ValueError('Original source-kind failure no longer reproduces')
    failure=json.loads(FAILURE.read_text())
    need(all(sha(p)==h for p,h in failure['inputHashes'].items()),'Failed predecessor source stays frozen')
    body=inspect.getsource(previous.preserve)
    before="hashlib.sha256(host.encode()).hexdigest().upper()==guest['transportSourceSHA256']"
    after="hashlib.sha256(host.encode()).hexdigest().upper()==source['hostSourceSHA256'] and sha(capture.__file__)==guest['captureSourceSHA256'] and sha(ROOT/capture.previous.LUA)==guest['transportSourceSHA256']"
    need(body.count(before)==1,'Bind each original host/Python/Lua SHA to its actual source kind')
    body=body.replace(before,after)
    before="for p in (OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)"
    after="for p in (FAILURE,Path(previous_file),OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)"
    need(body.count(before)==1,'Entire failure and source input pins retained')
    scope=dict(vars(previous),__file__=__file__,FAILURE=FAILURE,previous_file=previous.__file__)
    exec(compile(body.replace(before,after),__file__+'::whole_source_kind_checked_preservation','exec'),scope)
    return scope['preserve']()


if __name__=='__main__':
    import sys
    {'preserve':preserve,'retire':previous.retire}[sys.argv[1]]()
