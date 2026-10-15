"""In-memory corruption tests for the current P2 Sonya square miss and display.

These are false-evidence tests only: no captured file, executable, ROM or
emulated gameplay state is changed. Rendering checks retain the same scope.
"""
import json
from pathlib import Path
from unittest.mock import patch
import verify_current_sonya_p2_cpu_square_display_v2046 as model

ROOT=model.ROOT;OUT=ROOT/'audit_v2047_current_sonya_p2_cpu_square_counterexamples'

def run():
    pins={};tests=[]
    for player in model.CASES:
        checked=ROOT/f'audit_v2046_current_sonya_p2_cpu_square_display_{player}_checked/report.json'
        proof=json.loads(checked.read_text());assert proof['passed']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():
            assert model.state.sha(file)==wanted
            assert file not in pins or pins[file]==wanted
            pins[file]=wanted
        pins[str(checked)]=model.state.sha(checked)
        actual=model.raster.data(ROOT/model.CASES[player]);groups,buffers,a,b,owners=actual
        queue=next(q for q in groups['FLOOR_QUEUE']if q['slot']==2 and q['pose']==model.square.INTRO[0]and q['part']==0)
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
            lines[index],count=re.subn(r'(?<!\w)'+re.escape(key)+r'=([^\s]+)',key+'='+value,lines[index])
            assert count==1
            return '\n'.join(lines)+'\n'
        def bad_state(name,altered):
            try:model.square.verify(altered,guest)
            except(AssertionError,ValueError,KeyError,IndexError)as error:
                tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
            else:raise AssertionError('Accepted corrupted native square evidence '+name)
            print(player+' rejected '+name+' ('+str(len(tests))+')',flush=True)
        field='MK2_CPU_PAIR_FIELD'
        bad_state('native_CPU_proxy_identity',mutate_line(field,2337,'id','1'))
        bad_state('native_CPU_floor_shift',mutate_line(field,2337,'floor','82'))
        bad_state('active_square_lock_missing',mutate_line(field,2337,'flags','00000000'))
        bad_state('original_rise_pose_changed',mutate_line(field,2337,'pose','FE835C20'))
        bad_state('fixed_point_rise_Y_changed',mutate_line(field,2337,'yraw','00450001'))
        bad_state('original_rise_velocity_changed',mutate_line(field,2337,'vy','FFF50000'))
        lines=log.splitlines()
        bad_state('missing_active_rise_callback','\n'.join(r for r in lines if not r.startswith(field+' frame=2337 '))+'\n')
        bad_state('miss_invents_damage',mutate_line(field,2337,'vhp','78'))
        bad_state('original_flight_pose_changed',mutate_line(field,2348,'pose','FE835C80'))
        bad_state('original_flight_speed_changed',mutate_line(field,2348,'vx','00090000'))
        bad_state('original_flight_height_changed',mutate_line(field,2348,'yraw','FFF20000'))
        fling=next(r for r in lines if r.startswith('MK2_CPU_OVERLAP_EVENT frame=2369 ')and 'kind=fling 'in r)
        bad_state('flight_ends_before_all_26_checks',log.replace(fling,fling.replace('frame=2369','frame=2368')))
        bad_state('original_drop_gravity_changed',mutate_line(field,2371,'gravity','00009000'))
        bad_state('fixed_point_drop_Y_changed',mutate_line(field,2371,'yraw','FFF38001'))
        bad_state('original_drop_pose_changed',mutate_line(field,2371,'pose','FE835C80'))
        bad_state('landing_action_changed',mutate_line(field,2387,'action','771'))
        bad_state('missing_grounded_landing_hold','\n'.join(r for r in lines if not r.startswith(field+' frame=2387 '))+'\n')
        bad_state('missing_post_regain_callback','\n'.join(r for r in lines if not r.startswith(field+' frame=2401 '))+'\n')
        regain=next(r for r in lines if r.startswith('MK2_CPU_OVERLAP_EVENT frame=2389 ')and 'kind=regain 'in r)
        bad_state('regain_retains_special_lock',log.replace(regain,regain.replace('flags=0000','flags=0010')))
        first=next(r for r in lines if r.startswith('MK2_CPU_CHOICE_EVENT frame=2335 ')and 'kind=first_result 'in r)
        second=next(r for r in lines if r.startswith('MK2_CPU_CHOICE_EVENT frame=2335 ')and 'kind=second_result 'in r)
        chosen=next(r for r in lines if r.startswith('MK2_CPU_CHOICE_EVENT frame=2335 ')and 'kind=square 'in r)
        bad_state('native_first_carry_contradicts_status',log.replace(first,first.replace('carry=0','carry=1')))
        bad_state('native_second_RNG_result_outside_square_branch',log.replace(second,second.replace('a0=00000062','a0=000001F4')))
        bad_state('native_router_executes_for_wrong_owner',log.replace(chosen,chosen.replace('owner=010350A0','owner=010350B0')))
        bad_state('native_first_RNG_result_missing','\n'.join(r for r in lines if r!=first)+'\n')
        fall=next(r for r in lines if r.startswith('MK2_SQUARE_NATIVE_FALL frame=2369 '))
        bad_state('native_fall_argument_changed',log.replace(fall,fall.replace('a2=00008000','a2=00009000')))
        bad_guest=bytearray(guest);bad_guest[(0xffffcdd0-0xff800000)//8+2]=25
        try:model.square.verify(log,bytes(bad_guest))
        except(AssertionError,ValueError,KeyError,IndexError)as error:
            tests.append(dict(player=player,name='native_flight_count_program_changed',rejected=True,errorType=type(error).__name__,error=str(error)))
        else:raise AssertionError('Accepted altered native Square program')
        # Return corrupt arrays only. Original palette files remain immutable.
        displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
        original_fromfile=model.np.fromfile
        def bad_palette(name,q):
            path=ROOT/model.CASES[player]/displays[q['frame']+1]['palette_file'];bank=q['bank']&0x7f00
            def changed(file,*args,**kwargs):
                array=original_fromfile(file,*args,**kwargs)
                if Path(file)==path:
                    array=array.copy();array[bank+10]^=1
                return array
            with patch.object(model.np,'fromfile',side_effect=changed):
                try:model.verify(player)
                except(AssertionError,ValueError,KeyError,IndexError)as error:
                    tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
                else:raise AssertionError('Accepted altered costume palette '+name)
        bad_palette('original_rising_costume_recoloured',queue)
        landed=next(r for r in groups['FLOOR_QUEUE']if r['slot']==2 and r['frame']==2390)
        bad_palette('post_regain_costume_recoloured',landed)
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
