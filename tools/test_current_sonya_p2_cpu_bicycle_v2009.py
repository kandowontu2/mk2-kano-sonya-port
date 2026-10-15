"""In-memory corruption tests for the current P2 Sonya bicycle miss and display.

These are false-evidence tests only: no captured file, executable, ROM or
emulated gameplay state is changed. Rendering checks retain the same scope.
"""
import json
from pathlib import Path
from unittest.mock import patch
import verify_current_sonya_p2_cpu_bicycle_display_v2007 as model

ROOT=model.ROOT;OUT=ROOT/'audit_v2009_current_sonya_p2_cpu_bicycle_counterexamples'

def run():
    pins={};tests=[]
    for player in model.CASES:
        checked=ROOT/f'audit_v2007_current_sonya_p2_cpu_bicycle_display_{player}_checked/report.json'
        proof=json.loads(checked.read_text());assert proof['passed']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():
            assert model.state.sha(file)==wanted
            assert file not in pins or pins[file]==wanted
            pins[file]=wanted
        pins[str(checked)]=model.state.sha(checked)
        actual=model.raster.data(ROOT/model.CASES[player]);groups,buffers,a,b,owners=actual
        queue=next(q for q in groups['FLOOR_QUEUE']if q['slot']==2 and q['pose']==model.bicycle.INTRO[0]and q['part']==0)
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
            with patch.object(model.raster,'data',return_value=variant),patch.object(model.raster.base,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant):
                try:model.verify(player)
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
        log=(ROOT/model.CASES[player]/'run.log').read_text(encoding='utf-8-sig')
        guest=(ROOT/model.CASES[player]/'guest_maincpu.bin').read_bytes()
        def mutate_line(prefix,frame,key,value):
            lines=log.splitlines();hits=[]
            for index,line in enumerate(lines):
                if line.startswith(prefix+' ')and ('frame='+str(frame)+' ')in line:
                    if prefix=='MK2_CPU_OVERLAP_EVENT'and 'kind=regain 'not in line:continue
                    hits.append(index)
            assert len(hits)==1,(prefix,frame,len(hits))
            index=hits[0]
            import re
            lines[index],count=re.subn(r'(?<!\\w)'+re.escape(key)+r'=([^\\s]+)',key+'='+value,lines[index])
            assert count==1
            return '\\n'.join(lines)+'\\n'
        def bad_state(name,altered):
            try:model.bicycle.verify(altered,guest)
            except(AssertionError,ValueError,KeyError,IndexError)as error:
                tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
            else:raise AssertionError('Accepted corrupted native bicycle evidence '+name)
            print(player+' rejected '+name+' ('+str(len(tests))+')',flush=True)
        field='MK2_CPU_PAIR_FIELD'
        bad_state('native_CPU_proxy_identity',mutate_line(field,1878,'id','1'))
        bad_state('native_CPU_floor_shift',mutate_line(field,1878,'floor','82'))
        bad_state('active_bicycle_lock_missing',mutate_line(field,1878,'flags','00000000'))
        bad_state('cycling_pose_changed',mutate_line(field,1878,'pose','FE83EC00'))
        bad_state('fixed_point_bicycle_Y_step_changed',mutate_line(field,1878,'yraw','006C4001'))
        bad_state('negative_gravity_changed',mutate_line(field,1878,'gravity','FFFF5000'))
        lines=log.splitlines()
        bad_state('missing_active_bicycle_callback','\\n'.join(r for r in lines if not r.startswith(field+' frame=1878 '))+'\\n')
        bad_state('missed_bicycle_invents_damage',mutate_line(field,1878,'vhp','134'))
        bad_state('native_fractional_landing_discarded',mutate_line('MK2_CPU_OVERLAP_EVENT',1931,'yraw','00510000'))
        # Alter the single actual native fall call without modifying any source.
        fall=next(r for r in lines if r.startswith('MK2_CPU_OVERLAP_EVENT frame=1889 ')and 'kind=fall 'in r)
        bad_state('wrong_original_bicycle_fall_argument',log.replace(fall,fall.replace('a2=0000A000','a2=00008000')))
        bad_state('wrong_original_bicycle_fall_callback',log.replace(fall,fall.replace('a6=FFF9DC00','a6=FFF8DC00')))
        regain=next(r for r in lines if r.startswith('MK2_CPU_OVERLAP_EVENT frame=1931 ')and 'kind=regain 'in r)
        bad_state('regain_leaves_native_action_lock',log.replace(regain,regain.replace('flags=0000','flags=0010')))
        real=model.verify(player)
        for k in('sampledFrames','exactReplayedFrames','exactScreenPixels','exactOwnedPixels','fullPhysicalPaletteChecks','nativeShadowCopies','sourceBoundProjections'):
            assert real[k]==proof[k],'Unmodified actual capture must still pass identically'
    for file,wanted in pins.items():assert model.state.sha(file)==wanted,'Original evidence changed'
    model.state.launch.module_pins(pins)
    return dict(passed=True,candidate=model.state.launch.NAME,counterexamples=tests,inputHashes=pins,
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
