"""Whole5533 paired audio and exact physical/raster gates, lexical Lua fix.

Preserve actual boot-loader failure5535; no game source/ROM/EXE changes.
"""
import inspect,json,traceback
from pathlib import Path
import current_baraka_audio_capture_v5533 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
FAILURE=ROOT/'audit_v5535_current_baraka_audio_observation/progress.json'
OUT=ROOT/'audit_v5539_current_baraka_audio_observation'
BASE=ROOT/'audit_v5538_current_baraka_audio_ram'
LUA=ROOT/'mk2ks_current_baraka_audio_ram_v5536.lua'
COMPLETED=[]
failed=json.loads(FAILURE.read_text())
need(not failed['passed']and failed['error']=="ValueError('Warning-free native terminal0')",
     'Actual preserved boot-wrapper failure, never relabelled native gameplay evidence')
error=(ROOT/'audit_v5534_current_baraka_audio_ram/kano_p1_samples/stderr.log').read_text()
need("attempt to call a nil value (global 'read')"in error,'Exact actual lexical loader failure')
prior.capture.__globals__.update(BASE=BASE,LUA=LUA,COMPLETED=COMPLETED)
source=inspect.getsource(prior.run)
before="for p in(Path(__file__),LUA,ROOT/'mk2ks_kitana_audio_queue_ram_v3939.lua'"
after="for p in(Path(__file__),Path(prior.__file__),FAILURE,ROOT/'mk2ks_current_baraka_audio_ram_v5532.lua',LUA,ROOT/'mk2ks_kitana_audio_queue_ram_v3939.lua'"
need(source.count(before)==1,'Entire original paired pipeline preserved, failed wrapper/trace and fix pinned')
source=source.replace(before,after,1)
scope=dict(prior.__dict__,prior=prior,FAILURE=FAILURE,BASE=BASE,OUT=OUT,LUA=LUA,COMPLETED=COMPLETED,__file__=__file__)
exec(compile(source,__file__+'.whole5533_paired_physical_pixels_native_audio_with_lexical_loader_fix','exec'),scope)
run=scope['run']


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable actual native lexical-fix observation')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();prior.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','remaining','newInputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
