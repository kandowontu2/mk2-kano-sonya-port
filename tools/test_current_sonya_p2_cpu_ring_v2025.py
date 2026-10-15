"""In-memory false-evidence tests for the current natural P2 Sonya ring.

No captured file, source input, executable, ROM, palette or gameplay is changed.
Tests cover physical/child ownership, geometry, shadows, original charging
and restored colours, collision/guard branch, flight/impact and independent cleanup.
"""
import json
from pathlib import Path
from unittest.mock import patch
import verify_current_sonya_p2_cpu_ring_display_v2023 as model
import re
import numpy as np

ROOT=model.ROOT;OUT=ROOT/'audit_v2025_current_sonya_p2_cpu_ring_counterexamples'

def run():
    pins={};tests=[]
    for player in ('kano',):
        checked=ROOT/'audit_v2023_current_sonya_p2_cpu_ring_display_checked/report.json'
        proof=json.loads(checked.read_text());assert proof['passed']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():
            assert model.state.launch.sha(file)==wanted
            assert file not in pins or pins[file]==wanted
            pins[file]=wanted
        pins[str(checked)]=model.state.launch.sha(checked)
        actual=model.raster.data(model.CASE);groups,buffers,a,b,owners=actual
        queue=next(q for q in groups['FLOOR_QUEUE']if q['slot']==2 and q['pose']==model.state.BODY[18][0]and q['part']==0)
        key={k:queue[k]for k in('frame','cursor')}
        dispatched=next(d for d in groups['FLOOR_QUEUE_DISPATCH']if d['cursor']==key['cursor']and d['queue_frame']==key['frame'])
        event=dispatched['event'];shadow_event=groups['SHADOW_COMPONENT'][0]['event']
        def row(g,tag,where):
            found=[r for r in g[tag]if all(r.get(k)==v for k,v in where.items())]
            assert len(found)==1,(tag,where,len(found))
            return found[0]
        q=lambda g:row(g,'FLOOR_QUEUE',key)
        inv=lambda g:row(g,'FLOOR_ALL_QUEUE',key)
        t=lambda g:row(g,'FLOOR_QUEUE_TRANSFORM',key)
        d=lambda g:row(g,'FLOOR_DMA',{'event':event})
        sh=lambda g:row(g,'FLOOR_DMA',{'event':shadow_event})
        def reject(name,change):
            mutated={tag:[dict(r)for r in rows]for tag,rows in groups.items()}
            change(mutated)
            variant=(mutated,buffers,a,b,owners)
            with patch.object(model.raster,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant):
                try:model.verify()
                except(AssertionError,ValueError,KeyError,IndexError)as error:
                    tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
                else:raise AssertionError('Accepted corrupted display evidence '+player+': '+name)
            print(player+' rejected '+name+' ('+str(len(tests))+')',flush=True)
        reject('proxy_CPU_identity',lambda g:q(g).update(id=1))
        reject('detached_physical_owner',lambda g:q(g).update(owner=queue['actor']^0x10))
        def missing_inventory(g):
            g['FLOOR_ALL_QUEUE']=[r for r in g['FLOOR_ALL_QUEUE']if not all(r.get(k)==v for k,v in key.items())]
        reject('physical_publication_missing_from_full_inventory',missing_inventory)
        reject('tracked_source_disagrees_with_independent_inventory',lambda g:inv(g).update(source=queue['source']+8))
        reject('camera_context_belongs_to_wrong_actor',lambda g:t(g).update(actor=queue['actor']^0x10))
        reject('camera_y_shifted_one_pixel',lambda g:t(g).update(camera=t(g)['camera']+65536))
        reject('display_y_shifted_one_pixel',lambda g:t(g).update(display=t(g)['display']+65536))
        reject('native_DMA_y_shifted_one_pixel',lambda g:d(g).update(y=d(g)['y']+1))
        reject('native_DMA_x_shifted_one_pixel',lambda g:d(g).update(x=d(g)['x']+1))
        def shifted_floor(g):
            q(g)['floor']+=1;t(g)['floor']+=1
        reject('own_floor_shifted_one_pixel',shifted_floor)
        def wrong_part(g):
            row(g,'FLOOR_QUEUE_PART',{**key,'part':0})['dy']+=1
        reject('original_cached_body_part_offset_shifted',wrong_part)
        reject('native_shadow_palette_not_black_bank',lambda g:sh(g).update(palette=0x100))
        reject('native_shadow_color_not_black_pen',lambda g:sh(g).update(color=14))
        def missing_shadow(g):
            g['SHADOW_COMPONENT']=[r for r in g['SHADOW_COMPONENT']if r['event']!=shadow_event]
        reject('native_shadow_copy_missing_ownership',missing_shadow)
        child_queue=next(r for r in groups['FLOOR_QUEUE']if r['slot']==3 and r['pose']==model.state.FLIGHT[18][0])
        child_key={k:child_queue[k]for k in('frame','cursor')}
        cq=lambda g:row(g,'FLOOR_QUEUE',child_key)
        reject('projectile_belongs_to_wrong_parent',lambda g:cq(g).update(parent=queue['actor']^0x10))
        reject('projectile_belongs_to_wrong_Main',lambda g:cq(g).update(main=child_queue['main']^0x10))
        def missing_child_inventory(g):
            g['FLOOR_ALL_QUEUE']=[r for r in g['FLOOR_ALL_QUEUE']if not all(r.get(k)==v for k,v in child_key.items())]
        reject('child_publication_missing_from_full_inventory',missing_child_inventory)
        reject('projectile_projection_context_wrong_actor',lambda g:row(g,'FLOOR_QUEUE_TRANSFORM',child_key).update(actor=queue['actor']))
        def orphan(g):
            dead=groups['FLOOR_CHILD_RETIRE'][0]['frame']
            publication=next(r for r in g['FLOOR_ALL_QUEUE']if r['frame']>dead and r['actor']not in {r['actor']for r in g['FLOOR_QUEUE']})
            publication.update(pose=child_queue['pose'],source=child_queue['source'])
        reject('ring_graphic_republished_after_retirement',orphan)
        # Corrupt only returned palette arrays, not the actual stored evidence.
        charged=next(r for r in groups['FLOOR_QUEUE']if r['slot']==2 and r['pose']in model.charge.CHARGE_POSES)
        restored=next(r for r in groups['FLOOR_QUEUE']if r['slot']==2 and r['pose']==model.state.BODY[18][-1])
        displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
        original_fromfile=np.fromfile
        def palette_reject(name,q):
            path=model.CASE/displays[q['frame']+1]['palette_file'];bank=q['bank']&0x7f00
            def changed(file,*args,**kwargs):
                array=original_fromfile(file,*args,**kwargs)
                if Path(file)==path:
                    array=array.copy();array[bank+10]^=1
                return array
            with patch.object(np,'fromfile',side_effect=changed):
                try:model.verify()
                except(AssertionError,ValueError,KeyError,IndexError)as error:
                    tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
                else:raise AssertionError('Accepted corrupted palette '+name)
            print(player+' rejected '+name+' ('+str(len(tests))+')',flush=True)
        palette_reject('original_ring_charge_colour_changed',charged)
        palette_reject('normal_release_colour_not_restored',restored)
        log=(model.CASE/'run.log').read_text(encoding='utf-8-sig');guest=(model.CASE/'guest_maincpu.bin').read_bytes()
        def change(prefix,frame,key,value,kind=None):
            lines=log.splitlines()
            hits=[i for i,r in enumerate(lines)if r.startswith(prefix+' ')and 'frame='+str(frame)+' 'in r and(kind is None or 'kind='+kind+' 'in r)]
            assert len(hits)==1,(prefix,frame,kind,len(hits))
            i=hits[0];lines[i],count=re.subn(r'(?<!\w)'+re.escape(key)+r'=([^\s]+)',key+'='+value,lines[i])
            assert count==1
            return '\n'.join(lines)+'\n'
        def bad_state(name,altered):
            try:model.state.verify(altered,guest)
            except(AssertionError,ValueError,KeyError,IndexError)as error:
                tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
            else:raise AssertionError('Accepted corrupted native ring evidence '+name)
            print(player+' rejected '+name+' ('+str(len(tests))+')',flush=True)
        field='MK2_CPU_PAIR_FIELD';event='MK2_CPU_OVERLAP_EVENT'
        bad_state('native_CPU_proxy_identity',change(field,2979,'id','1'))
        bad_state('ring_parent_lock_missing',change(field,2979,'flags','00000000'))
        bad_state('ring_body_hold_changed',change(field,2973,'pose','FE83DEC0'))
        bad_state('real_damage_relabelled_as_chip',change('MK2_CPU_OVERLAP_HEALTH',2991,'after','155'))
        bad_state('guard_reads_wrong_victim_Main',change('MK2_RING_PAIR_TESTED',2991,'loaded_main','0106BF30'))
        # The native decision stayed CLRC, but fake evidence claims Block pressed.
        lines=log.splitlines()
        false_controls='\n'.join(r.replace('controls=FFFFFFFE','controls=FFFFFFDE')if r.startswith('MK2_RING_PAIR_BLOCK frame=2991 ')else r for r in lines)+'\n'
        bad_state('guard_branch_contradicts_physical_Block',false_controls)
        bad_state('parent_lock_left_at_first_ready',change(event,3013,'flags','0010','regain'))
        bad_state('projectile_fixed_point_velocity_changed',change('MK2_CPU_OVERLAP_CHILD_FIELD',2980,'vx','FFF90000'))
        bad_state('projectile_retired_one_field_early',change('MK2_CPU_OVERLAP_RETIRE',3019,'frame','3018'))
        bad_state('impact_pose_hold_changed',change(event,2995,'a0','FF60C1C0','group'))
        bad_state('missing_impact_callback','\n'.join(r for r in lines if not r.startswith('MK2_CPU_OVERLAP_CHILD_FIELD frame=2992 '))+'\n')
        bad_state('child_orphan_at_stop',change('MK2_CPU_OVERLAP_RESULT',3614,'live_children','1'))
        bad_state('missing_post_retirement_callback','\n'.join(r for r in lines if not r.startswith(field+' frame=3050 '))+'\n')
        real=model.verify()
        for k in('sampledFrames','exactReplayedFrames','exactScreenPixels','exactOwnedPixels','fullPhysicalPaletteChecks','nativeShadowCopies','sourceBoundProjections'):
            assert real[k]==proof[k],'Unmodified actual capture must still pass identically'
    for file,wanted in pins.items():assert model.state.launch.sha(file)==wanted,'Original evidence changed'
    model.state.launch.launch.module_pins(pins)
    return dict(passed=True,candidate=model.state.launch.launch.NAME,counterexamples=tests,inputHashes=pins,
        originalCapturesUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=run()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],counterexamples=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)
