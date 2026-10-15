"""Qualified faults against actual current Ring rows; same-path positive controls."""
import json,linecache,subprocess,traceback
from collections import defaultdict
from pathlib import Path
from unittest.mock import patch
import verify_current_cpu_ring_v3431 as current
ROOT=current.ROOT;need=current.need;sha=current.sha
OUT=ROOT/'audit_v3439_current_cpu_ring_counterexamples'

def main():
    need(not OUT.exists(),'Immutable current faults report')
    proofpath=ROOT/'audit_v3432_current_cpu_ring_checked/report.json'
    proof=json.loads(proofpath.read_text())
    need(proof['passed'] and proof['firstCompleteRingPhaseArtShadowEraseAccepted']
         and not proof['fullPortAcceptance'],'Actual terminal full native scene positive first')
    expected=current.current.expected_current()
    current.current.assembly.NAME=current.current.current.CANDIDATE
    current.current.assembly.expected=lambda:expected
    model=current.render;model.matched=current.matched_adapter()
    prior=json.loads((ROOT/'audit_v2972_native_cpu_ring_checked/report.json').read_text())
    actual=model.raster.data(current.CASE);groups,buffers,a,b,owners=actual
    queue=next(q for q in groups['FLOOR_QUEUE']if q['slot']==2 and q['pose']==model.state.BODY[18][0] and q['part']==0)
    key={k:queue[k]for k in ('frame','cursor')}
    def row(g,tag,match):
        found=[r for r in g[tag]if all(r.get(k)==v for k,v in match.items())]
        need(len(found)==1,'Unique actual row for non-vacuous fault');return found[0]
    tests=[]
    def reject_render(label,change,source_assert):
        changed=defaultdict(list,{tag:[dict(r)for r in rows]for tag,rows in groups.items()});change(changed)
        need(changed!=groups,'Non-vacuous actual native scene fault')
        variant=(changed,buffers,a,b,owners)
        with patch.object(model.raster,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant):
            try:model.verify(current.CASE,'new_kano',prior,expected[0],expected[2])
            except AssertionError as error:
                frames=traceback.extract_tb(error.__traceback__)
                need(any(Path(f.filename).resolve()==Path(model.__file__).resolve()
                     and source_assert in linecache.getline(f.filename,f.lineno)for f in frames),
                     'Qualified intended original scene invariant, not unrelated exception')
                tests.append(dict(name=label,rejectedByOriginalInvariant=source_assert))
            else:raise ValueError('Actual corrupted Ring scene accepted')
    def floor(g):
        row(g,'FLOOR_QUEUE',key)['floor']+=1
        row(g,'FLOOR_QUEUE_TRANSFORM',key)['floor']+=1
    reject_render('own_floor_shifted_one_pixel',floor,"t['floor']==q['floor']==t['stageY']")
    reject_render('camera_shifted_one_pixel',lambda g:row(g,'FLOOR_QUEUE_TRANSFORM',key).update(
        camera=row(g,'FLOOR_QUEUE_TRANSFORM',key)['camera']+65536),'Every part uses actual queued camera and display geometry')
    reject_render('cached_body_offset_shifted_one_pixel',lambda g:row(g,'FLOOR_QUEUE_PART',{**key,'part':0}).update(
        dy=row(g,'FLOOR_QUEUE_PART',{**key,'part':0})['dy']+1),'len(actual)==len(composition)')
    def orphan(g):
        child=next(r for r in groups['FLOOR_QUEUE']if r['slot']==3 and r['pose']==model.state.FLIGHT[18][0])
        dead=groups['FLOOR_CHILD_RETIRE'][0]['frame']
        publication=next(r for r in g['FLOOR_ALL_QUEUE']if r['frame']>dead)
        publication.update(actor=child['actor'],pose=child['pose'],source=child['source'])
    reject_render('projectile_republished_after_retirement',orphan,'No knife/impact art outside either actual child lifetime')
    for label,change,message in (
        ('missing_native_source_load',lambda g:g['FLOOR_SHIFT_LOAD'].pop(0),'Store uses its actual original preceding source load'),
        ('wrong_native_source_address',lambda g:g['FLOOR_SHIFT_LOAD'][0].update(address=0x1fc000,index=260096),'Original source template address')):
        changed=defaultdict(list,{tag:[dict(r)for r in rows]for tag,rows in groups.items()});change(changed)
        need(changed!=groups,'Non-vacuous actual native erase fault')
        with patch.object(current.erase.raster,'data',return_value=(changed,buffers,a,b,owners)):
            try:current.erase.inspect(current.CASE,expected[0],current.current.current.CANDIDATE)
            except ValueError as error:
                need(message in str(error),'Specific intended original erase invariant')
                tests.append(dict(name=label,rejectedByOriginalInvariant=message))
            else:raise ValueError('Corrupted actual native erase accepted')
    positive=model.verify(current.CASE,'new_kano',prior,expected[0],expected[2])
    erased=current.erase.inspect(current.CASE,expected[0],current.current.current.CANDIDATE)
    need(positive['passed'] and erased['passed'] and len(tests)==6,'Same-path unchanged full scene and one-base erase positive controls')
    pins=dict(proof['inputHashes']);pins[str(proofpath.resolve())]=sha(proofpath)
    pins[str(Path(__file__).resolve())]=sha(__file__)
    for file,digest in pins.items():need(sha(file)==digest,'Actual game/capture/input bytes unchanged')
    value=dict(passed=True,actualQualifiedCounterexamples=tests,qualifiedRejectedCount=6,
        samePathOriginalSceneAndErasePositiveAccepted=True,actualCaptureOrGameChanged=False,
        rawAudioFilesWritten=0,newBuildsOrROMCopies=0,fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(value,indent=2)+'\n');digest=sha(path)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(result.returncode==0 and sha(path)==digest,'Lossless current fault report compression')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
