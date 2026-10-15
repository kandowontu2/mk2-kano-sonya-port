"""In-memory corruption tests for the current P2 Sonya square miss and display.

These are false-evidence tests only: no captured file, executable, ROM or
emulated gameplay state is changed. Rendering checks retain the same scope.
"""
import json
from pathlib import Path
from unittest.mock import patch
import verify_native_cpu_square_hit_render_v3044 as model

ROOT=model.ROOT;OUT=ROOT/'audit_v3051_native_cpu_square_hit_render_units'

def run():
    pins={};tests=[]
    for player in model.CASES:
        checked=ROOT/f'audit_v3045_native_cpu_square_hit_render_{player}_checked/report.json'
        proof=json.loads(checked.read_text());assert proof['passed']and not proof['fullPortAcceptance']
        for file,wanted in proof['inputHashes'].items():
            assert model.state.sha(file)==wanted
            assert file not in pins or pins[file]==wanted
            pins[file]=wanted
        pins[str(checked)]=model.state.sha(checked)
        actual=model.raster.data(ROOT/model.CASES[player][0]);groups,buffers,a,b,owners=actual
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
            assert mutated!=groups,'Nonvacuous actual scene mutation '+name
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
        # Return corrupt arrays only. Original palette files remain immutable.
        displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
        original_fromfile=model.np.fromfile
        def bad_palette(name,q):
            path=ROOT/model.CASES[player][0]/displays[q['frame']+1]['palette_file'];bank=q['bank']&0x7f00
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
        landed=next(r for r in groups['FLOOR_QUEUE']if r['slot']==2 and r['frame']==proof['state']['ready']+1)
        bad_palette('post_regain_costume_recoloured',landed)
        real=model.verify(player)
        for k in('sampledFrames','exactReplayedFrames','exactScreenPixels','exactOwnedPixels','fullPhysicalPaletteChecks','nativeShadowCopies','sourceBoundProjections'):
            assert real[k]==proof[k],'Unmodified actual capture must still pass identically'
    assert len(tests)==16,'All16 actual source/FIFO/projection/floor/shadow/costume corruptions rejected'
    for file,wanted in pins.items():assert model.state.sha(file)==wanted,'Original evidence changed'
    model.state.launch.module_pins(pins)
    return dict(passed=True,candidate=model.state.launch.NAME,counterexamples=tests,inputHashes=pins,
        actualCounterexamplesRejected=len(tests),originalCapturesUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Preserve executed evidence'
    try:result=run()
    except Exception as error:
        import traceback
        result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(passed=result['passed'],counterexamples=len(result.get('counterexamples',[])),error=result.get('error'))),flush=True)
    raise SystemExit(0 if result['passed']else 1)
