"""Retain first failed count gate; requalify same actual terminal, no replay.

Original exit occurs at age480 before its frame_done callback. Therefore the
full unchanged observer emits 38 pre-draw buffers and 37 displayed frames,
not 37 of each. Require exact source-derived chronology, including the extra
age479 pre-draw buffer. No missing/extra buffer or raster is excused.
"""
import gzip
import inspect
import json
from pathlib import Path
import re
import capture_native_kano_laser_ground_ram as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_ground_complete_buffers_checked'
RECHECK=ROOT/'audit_native_kano_laser_ground_kano_p1_complete_buffers_recheck'
RAM_CASES=prior.RAM_CASES
COMPLETED=[]

def factories():
    capture=inspect.getsource(prior.capture)
    old="need(set(buffers)==expected_buffers and len(buffers)==111,'All exact pre-DMA, displayed VRAM, palette buffers')"
    new="""need(set(buffers)==expected_buffers and len(buffers)==112,'All exact38pre-DMA/37displayed VRAM/37palette buffers')
        ages=[a for a in range(481)if a%8==0 and(16<=a<=96 or 128<=a<=192 or 248<=a<=312 or 368<=a<=392 or 432<=a<=456 or a==480)]
        need(len(ages)==38 and [r['age']for r in snaps]==ages[:-1] and
             [(r['frame'],r['age'])for r in ground.rows(text,'PRE')]==[(finish[0]['ready']+a-1,a-1)for a in ages],
             'All exact original source-derived capture ages; terminal exit omits only age480 frame_done, no replay/drop')"""
    need(capture.count(old)==1,'Exact preserved failed buffer-count boundary');capture=capture.replace(old,new)
    scope=dict(vars(prior),__file__=__file__,OUT=OUT,RAM_CASES=RAM_CASES,COMPLETED=COMPLETED)
    exec(compile(capture,__file__+'::entire_original_native_ground_capture_with_exact_buffer_chronology','exec'),scope)
    # Reuse the entire identical acceptance body on the first actual terminal.
    # Raw startup inventory was already independently equal before the failed
    # count assertion; verify its exactly-once digests and frozen provenance.
    first=capture.index('    result=dict(passed=False,')
    last=capture.index("    save(folder/'result.json',result)",first)
    body=capture[first:last]
    revalidate='''def revalidate(c,pins,inspect_ram):
    folder=c['folder'];text=c['log'];images=c['images'];buffers=c['buffers'];headers=c['headers']
    terminal=c['terminal'];exitcode=terminal['nativeExit'];errors=terminal['hostDecodeErrors']
    fighter=c['result']['fighter'];side=c['result']['side']
    with gzip.open(folder/'run.log.gz','rt')as stream:digests=stream.read()
    inventories={tag:len(re.findall(r'^'+tag+r'_DIGEST ',digests,re.M))for tag in('MK2_GR_GUEST','MK2_GR_GFX')}
''' + body + '''    need(result['passed'],'Complete whole original gate on same terminal evidence')
    need(not RECHECK.exists(),'Fresh same-handle recheck, preserve failed original');RECHECK.mkdir()
    result['originalFailedResultSHA256']=sha(folder/'result.json')
    result['sameActualNativeHandleRequalified']=True
    result['nativeReplay']=False
    save(RECHECK/'result.json',result)
    c['result']=result;COMPLETED.append(result)
    print(json.dumps(dict(case='kano_p1',passed=True,sameActualNativeHandle=terminal['pid'],nativeReplay=False)),flush=True)
    return c
'''
    scope.update(RECHECK=RECHECK)
    exec(compile(revalidate,__file__+'::same_terminal_entire_native_ground_gate','exec'),scope)
    run=inspect.getsource(prior.run)
    changes=[
        ("need(not BASE.exists() and not OUT.exists() and not identity.census(),'Fresh four-case ground run, no native replay')",
         "need(BASE.exists() and not OUT.exists() and not identity.census() and set(RAM_CASES)=={'kano_p1'},'First original handle terminal, remaining three cases never dispatched')"),
        ("for p in(Path(__file__),LUA,GUARD,initializer,", "for p in(Path(__file__),Path(prior.__file__),ROOT/'audit_native_kano_laser_ground_checked/failure.json',ROOT/'audit_native_kano_laser_ground_ram/kano_p1/result.json',ROOT/'audit_native_kano_laser_ground_ram/kano_p1/native_terminal.json',LUA,GUARD,initializer,"),
        ("for fighter,side in(('kano',1),('sonya',1),('kano',2),('sonya',2)):",
         "revalidate(RAM_CASES['kano_p1'],pins,inspect_ram)\n    for fighter,side in(('sonya',1),('kano',2),('sonya',2)):")]
    for old,new in changes:
        need(run.count(old)==1,'Whole original four-case proof; exact first-handle requalification boundary');run=run.replace(old,new)
    scope.update(prior=prior)
    exec(compile(run,__file__+'::same_first_terminal_plus_three_remaining_actual_jobs','exec'),scope)
    return scope['run']

def guarded_run(guest,gfx):
    try:return factories()(guest,gfx)
    except Exception as error:
        need(not OUT.exists(),'Never overwrite executed recheck');OUT.mkdir()
        prior.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=prior.traceback.format_exc(),
            completedCases=COMPLETED,fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
        return None
