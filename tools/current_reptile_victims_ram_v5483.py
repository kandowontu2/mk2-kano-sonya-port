"""Preserve5482; same Lua environment and exact scanout metadata association.

Payload sizes/digests differ legitimately between actual palette and VRAM.
Every shared frame/flip/register/filename field must match; whole buffer sizes
and every raster pixel are checked separately by the original native model.
No native control/state/artwork edit or loose pixel tolerance.
"""
import inspect, io, json, traceback
from pathlib import Path
import current_reptile_victims_ram_v5480 as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
BASE=ROOT/'audit_v5484_current_reptile_victims_ram'
OUT=ROOT/'audit_v5485_current_reptile_victims_progress'
LUA=ROOT/'mk2ks_current_reptile_ram_v5483.lua'
FAILED=ROOT/'audit_v5482_current_reptile_victims_progress/progress.json'


def run():
    failed=json.loads(FAILED.read_text())
    need(not failed['passed']and failed['error']=="KeyError(('reptile_victim_3135_000.png', 'PALETTE'))",
         'Preserved exact missing passive palette transport from isolated Lua ENV')
    prior=ROOT/'audit_v5481_current_reptile_victims_ram/kano_p1/run.log'
    log=prior.read_text()
    need('RESULT frame=5198'in log and 'native_dma=514 first=3265 last=3752'in log and
         'MK2_CURRENT_REPTILE_RAM_PALETTE_DIGEST'not in log,'Actual original controller terminal; passive palette extension was not applied')
    old=(ROOT/'audit_v5478_current_reptile_victims_ram/kano_p1/run.log').read_text()
    physical=lambda text:[line for line in text.splitlines()if line.startswith(('MK2_REPTILE_V879_','MK2_DEATH_ART_V897_','MK2_CURRENT_REPTILE_RAM_RGB_DIGEST '))]
    need(physical(log)==physical(old),'Whole original physical/art replay and all31 actual displayed buffer digests byte-exact across two preserved captures')
    scope=dict(previous.__dict__)
    scope.update(BASE=BASE,OUT=OUT,LUA=LUA,__file__=str(Path(__file__).resolve()))
    source=inspect.getsource(previous.native_pixels)
    before="meta==vr and meta['frame']==meta['flip_frame']"
    after="all(meta[k]==vr[k]for k in('filename','frame','age','flip_frame','start','control','tap','pc','mask'))and meta['frame']==meta['flip_frame']"
    need(source.count(before)==1,'Only shared actual native scene metadata, not unequal raw buffer sizes/digests')
    source=source.replace(before,after)
    exec(compile(source,__file__+'.whole5480_exact_shared_native_scene_metadata','exec'),scope)
    source=inspect.getsource(previous.run)
    before="    return scope['run']()"
    after="""    report=scope['run']()
    for p in (ROOT/'tools/current_reptile_victims_ram_v5480.py',ROOT/'mk2ks_current_reptile_ram_v5480.lua',ROOT/'audit_v5482_current_reptile_victims_progress/progress.json'):
        report['newInputHashes'][str(p)]=sha(p)
    for p in (ROOT/'audit_v5481_current_reptile_victims_ram').rglob('*'):
        if p.is_file():report['newInputHashes'][str(p)]=sha(p)
    report['preservedTwoPriorNativeCaptures']=dict(originalControllerAndArtRowsExact=True,all31ActualDisplayedBufferDigestsExact=True,notDifferentGameplay=True)
    return report"""
    need(source.count(before)==1,'One final actual current matrix additive provenance boundary')
    source=source.replace(before,after)
    exec(compile(source,__file__+'.whole5480_actual_pixel_capture_same_Lua_ENV','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable shared-ENV current Reptile pixel checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();previous.canonical5467.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','independentSourcePNGNativeReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
