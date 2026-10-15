"""Actual in-memory counterexamples; no changes to native evidence or ROM."""
import copy,json
from pathlib import Path
import verify_human_projectile_display_v1293 as hit
import verify_human_projectile_negative_display_v1297 as negative
ROOT=hit.ROOT;OUT=ROOT/'audit_v1301_projectile_lifetime_counterexamples'

def verify():
    pins={};results=[];baseline=[]
    def pin(path,wanted=None):
        path=Path(path);key=str(path);actual=pins.get(key)or hit.current.digest(path)
        assert wanted is None or actual==wanted,'Changed evidence '+key;pins[key]=actual
    guest,_,_,payload=hit.current.reconstruct();image=bytearray(hit.ground.graphics(pins))
    for header,source,dest in((0x1c0000,0x1c4000,0x1e04000),(0x1c1000,0x1e6000,0x1e50000),(0x1c2000,0x1f4000,0x1e60000)):
        start,count,destination=hit.struct.unpack_from('<III',payload,header+4);assert(start,destination)==(source,dest)
        image[dest:dest+count]=payload[source:source+count]
    sequences,pieces=hit.independent_art(payload,bytes(image),pins)
    for move in('knife','ring'):
        for side in(1,2):
            for scenario in('hit','block','miss'):
                suffix=f'{move}_p{side}'if scenario=='hit'else f'{move}_{scenario}_p{side}'
                path=ROOT/f'audit_v{1293 if scenario=="hit"else 1297}_projectile_{suffix}_render_checked/report.json'
                proof=json.loads(path.read_text());assert proof['passed']and proof['candidate']==hit.current.CANDIDATE
                pin(path)
                for file,wanted in proof['inputHashes'].items():pin(file,wanted)
                folder=ROOT/f'audit_v{1291 if scenario=="hit"else 1296}_projectile_{suffix}'
                groups,*_=hit.raster.data(folder);first=groups['FLOOR_STATE'][0];actors={s:first[f'p{s}']for s in(1,2)}
                spawn=groups['FLOOR_CHILD_SPAWN'][0];retirement=groups['FLOOR_CHILD_RETIRE'][0]
                poses=set(sequences[move]['intro']+sequences[move]['flight']+sequences[move]['impact'])
                sources={d[4]for pose in poses for _,d in hit.source_groups(payload,pose,0xfe800000)}
                accepted=hit.verify_publications(groups,actors,spawn,retirement,poses,sources)
                phase=hit.phase_order(groups['FLOOR_QUEUE'],sequences[move],side)if scenario=='hit'else negative.phase_order(groups['FLOOR_QUEUE'],sequences[move],side,scenario)
                assert json.loads(json.dumps(accepted))==proof['publicationInventory']and phase==proof['nativePhaseOrder'],'Unchanged actual baseline'
                baseline.append(suffix+'/'+scenario)
                if (move,side,scenario)!=('knife',1,'hit'):continue
                def counter(label,mutate):
                    altered={key:copy.deepcopy(groups[key])for key in('FLOOR_ALL_QUEUE','FLOOR_QUEUE')}
                    mutate(altered)
                    try:hit.verify_publications(altered,actors,spawn,retirement,poses,sources)
                    except AssertionError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
                    else:raise AssertionError('Invalid evidence accepted: '+label)
                def post(g):return next(q for q in g['FLOOR_ALL_QUEUE']if q['frame']>retirement['frame'])
                counter('lingering_projectile_pose_after_cleanup',lambda g:post(g).update(pose=next(iter(poses))))
                counter('lingering_projectile_source_after_cleanup',lambda g:post(g).update(source=next(iter(sources))))
                counter('ghost_projectile_at_different_actor',lambda g:post(g).update(actor=spawn['actor']+0x1000,pose=next(iter(poses))))
                counter('missing_live_child_publication',lambda g:g['FLOOR_QUEUE'].remove(next(q for q in g['FLOOR_QUEUE']if q['slot']==3)))
                counter('missing_physical_actor_publication',lambda g:g['FLOOR_QUEUE'].remove(next(q for q in g['FLOOR_QUEUE']if q['slot']==side)))
                counter('wrong_native_FIFO_entry',lambda g:g['FLOOR_ALL_QUEUE'][0].update(pc=0))
                counter('duplicate_inventory_publication',lambda g:g['FLOOR_ALL_QUEUE'].append(copy.deepcopy(g['FLOOR_ALL_QUEUE'][0])))
                counter('duplicate_tracked_publication',lambda g:g['FLOOR_QUEUE'].append(copy.deepcopy(g['FLOOR_QUEUE'][0])))
                def change_tracked(g,key,value):
                    q=next(q for q in g['FLOOR_QUEUE']if q['slot']==3)
                    row=next(r for r in g['FLOOR_ALL_QUEUE']if(r['frame'],r['cursor'])==(q['frame'],q['cursor']))
                    row[key]=value
                counter('independent_inventory_changed_child_id',lambda g:change_tracked(g,'id',1))
                counter('independent_inventory_changed_child_cache',lambda g:change_tracked(g,'cache',0))
                def remove_tail(g):
                    for key in g:g[key]=[q for q in g[key]if q['frame']<=retirement['frame']]
                counter('no_post_cleanup_inventory',remove_tail)
    # Execute native phase contracts on unchanged source-bound rows, then prove
    # reordered rotations/missing bodies/fake impacts cannot pass them.
    for scenario in('hit','block','miss'):
        suffix='knife_p1'if scenario=='hit'else 'knife_'+scenario+'_p1'
        folder=ROOT/f'audit_v{1291 if scenario=="hit"else 1296}_projectile_{suffix}'
        groups,*_=hit.raster.data(folder);original=groups['FLOOR_QUEUE']
        def check(rows):return hit.phase_order(rows,sequences['knife'],1)if scenario=='hit'else negative.phase_order(rows,sequences['knife'],1,scenario)
        mutations=[]
        missing_body=[q for q in original if not(q['slot']==1 and q['pose']==sequences['knife']['body'][-1])]
        mutations.append(('missing_release_body_'+scenario,missing_body))
        rows=copy.deepcopy(original);first=next(q for q in rows if q['slot']==3 and q['pose']in sequences['knife']['flight'])
        frame=first['frame']
        for q in rows:
            if q['slot']==3 and q['frame']==frame:q['pose']=sequences['knife']['flight'][1]
        mutations.append(('reordered_first_flight_rotation_'+scenario,rows))
        if scenario=='miss':
            rows=copy.deepcopy(original);fake=copy.deepcopy(first);fake['frame']=max(q['frame']for q in rows)+1;fake['pose']=sequences['knife']['impact'][0];rows.append(fake)
            mutations.append(('fake_contact_impact_on_miss',rows))
        else:
            rows=[q for q in original if not(q['slot']==3 and q['pose']==sequences['knife']['impact'][-1])]
            mutations.append(('missing_last_impact_'+scenario,rows))
        for label,rows in mutations:
            try:check(rows)
            except AssertionError as error:results.append(dict(case=label,rejected=True,reason=str(error)))
            else:raise AssertionError('Invalid evidence accepted: '+label)
    # Rehash the actual files after all in-memory changes; cached pins are not
    # used for this second pass.
    for file,wanted in pins.items():assert hit.current.digest(file)==wanted,'Actual artifact changed'
    pin(Path(__file__));pin(ROOT/'tools/test_current_projectile_lifetime_v1300.py');pin(ROOT/'audit_v1300_projectile_lifetime_counterexamples/report.json')
    return dict(passed=True,candidate=hit.current.CANDIDATE,baselines=baseline,counterexamples=results,count=len(results),
        originalDonorPiecesCompared=pieces,actualArtifactsUnchanged=True,inMemoryOnly=True,inputHashes=pins,fullPortAccepted=False)

if __name__=='__main__':
    assert not OUT.exists()
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Projectile lifetime/phase counterexamples passed='+str(report['passed'])+' '+report.get('error',''),flush=True)
    raise SystemExit(0 if report['passed']else 1)
