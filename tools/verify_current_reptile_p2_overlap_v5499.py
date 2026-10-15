"""Retain the two accepted P1 cases; finish P2 with body-specific faults.

Actual P2 queue ordering publishes the detached head before the headless body.
The original floor counterexample accidentally mutated the head. Bind every
body floor/owner/camera fault to body001E and DMA faults to its nonzero pose.
Keep the complete original physical and pixel contract; do not loosen it.
"""
import concurrent.futures, inspect, json, traceback
from pathlib import Path
import verify_current_reptile_overlap_v5492 as canonical
import verify_current_reptile_overlap_v5495 as qualified

ROOT,need,sha=canonical.ROOT,canonical.need,canonical.sha
BASE=ROOT/'audit_v5500_current_reptile_p2_overlap_ram'
OUT=ROOT/'audit_v5501_current_reptile_overlap_progress'
FAILED=ROOT/'audit_v5497_current_reptile_overlap_progress/progress.json'


def corrected_physical_faults():
    source=inspect.getsource(canonical.canonical.faults)
    before="r'(^MK2_DEATH_ART_V897_QUEUE .*?y=)(-?\\d+)'"
    after="r'(^MK2_DEATH_ART_V897_QUEUE .*? y=)(-?\\d+)'"
    need(source.count(before)==1,'Exact previously corrected native Y-field boundary')
    source=source.replace(before,after)
    for before,after,count in(
      ('(^MK2_DEATH_ART_V897_QUEUE ','(^MK2_DEATH_ART_V897_QUEUE (?=.* body=001E )',5),
      ('(^MK2_DEATH_ART_V897_DMA ','(^MK2_DEATH_ART_V897_DMA (?!.* fifo_pose=00000000 )',2)):
        need(source.count(before)==count,'Every original body fault explicitly targets the body, never its separate head')
        source=source.replace(before,after)
    scope=dict(canonical.canonical.__dict__)
    exec(compile(source,__file__+'.whole_original21_faults_actual_body_not_detached_head','exec'),scope)
    return scope['faults']


def preserved_p1():
    failed=json.loads(FAILED.read_text())
    need(not failed['passed']and failed['error']=="ValueError('Actual native-record counterexample accepted: actual body loses owned floor')"and
         len(failed['completedCases'])==2,'Exact preserved P2 first-head mutation failure and two qualified native P1 cases')
    cases=[]
    for fighter in('kano','sonya'):
        folder=qualified.BASE/f'{fighter}_p1';proof=json.loads((folder/'result.json').read_text())
        before=json.loads((folder/'input_hashes_before.json').read_text())
        need(proof['passed']and proof['process']['input_hashes']==before and
             proof['actualNativeBodyBloodPixelsAndScanout']['passed']and len(proof['effectiveActualNativeRecordFaults'])==21,
             'Entire actual prior P1 physical/pixel/fault acceptance preserved without unnecessary repeat')
        need(all(sha(p)==h for p,h in before.items()),'Every original P1 executed source/current/public pin stable')
        need(proof in failed['completedCases'],'Prior completed native P1 result exactly retained in failed matrix journal')
        cases.append(proof)
    return cases


def run():
    prior=preserved_p1()
    scope=dict(qualified.__dict__)
    scope.update(BASE=BASE,OUT=OUT,__file__=str(Path(__file__).resolve()),COMPLETED=[],
                 corrected_physical_faults=corrected_physical_faults,preserved_cases=prior)
    source=inspect.getsource(canonical.capture)
    before="faults=pixels.corrected_faults()(log,result,ram,reference,images,guest,payload,contract)"
    after="faults=corrected_physical_faults()(log,result,ram,reference,images,guest,payload,contract)"
    need(source.count(before)==1,'Only physical counterexample target selection corrected')
    source=source.replace(before,after)
    exec(compile(source,__file__+'.whole5492_native_capture_body_specific_faults','exec'),scope)
    source=inspect.getsource(canonical.run)
    before="""    first=capture(('kano',1),guest,payload,expected_gfx,reference,pins,image)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=[first]+list(pool.map(lambda spec:capture(spec,guest,payload,expected_gfx,reference,pins,image),[('kano',2),('sonya',1),('sonya',2)]))"""
    after="""    for p in (Path(canonical.__file__),Path(qualified.__file__),FAILED):pins[str(p.resolve())]=sha(p)
    for p in qualified.BASE.rglob('*'):
        if p.is_file():pins[str(p.resolve())]=sha(p)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=preserved_cases+list(pool.map(lambda spec:capture(spec,guest,payload,expected_gfx,reference,pins,image),[('kano',2),('sonya',2)]))"""
    need(source.count(before)==1,'Retain accepted two native P1 cases and capture only missing physical P2 qualification')
    source=source.replace(before,after)
    source=source.replace('newNativeBoots=4,newBuilds=0','newNativeBoots=2,preservedAcceptedNativeBoots=2,newBuilds=0',1)
    exec(compile(source,__file__+'.whole5492_additive_both_slots_no_repeated_P1_boot','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable completed both-slot Reptile checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();canonical.canonical.save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','independentSourcePNGNativeReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
