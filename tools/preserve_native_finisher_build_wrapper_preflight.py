"""Record pre-build scriptblock path binding failure; no compiler was launched."""
import gzip,json
from pathlib import Path
import native_ai_response_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
if __name__=='__main__':
    out=ROOT/'audit_native_cpu_finisher_build_wrapper_preflight_failure'
    need(not out.exists() and not (ROOT/'diagnostic_native_cpu_finisher_dispatch').exists() and
         not (ROOT/'mame-mkp/build/mingw-gcc').exists(),'Pre-compiler failure, no candidate/cache created')
    source=ROOT/'tools/build_native_cpu_finisher_dispatch.ps1';out.mkdir()
    with gzip.open(out/'original_wrapper.ps1.gz','wt',encoding='utf-8')as stream:stream.write(source.read_text())
    (out/'report.json').write_text(json.dumps(dict(passed=False,compilerLaunched=False,
        sourceSHA256=sha(source),reason='Scriptblock has no automatic PSScriptRoot; bind caller paths explicitly.',
        newBuilds=0,publicBuildChanged=False,fullPortAcceptance=False),indent=2)+'\n')
    print('Original pre-compiler wrapper failure preserved; no cache or candidate created.')
