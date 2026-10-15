"""Actual rendered ring negative evidence for mirror, Kano and fractional control.

Original FIFO/component/camera/palette/shadow/raster checks remain intact.
Only in-memory actual rows or returned palette arrays change; no saved capture,
ROM, executable, script, native input, AI or RNG is altered.
"""
import copy,json,traceback
from pathlib import Path
from unittest.mock import patch
import numpy as np
import verify_native_cpu_ring_render_v2983 as model

ROOT=model.ROOT
OUT=ROOT/'audit_v3086_native_cpu_ring_render_units'

def run():
    checked=ROOT/'audit_v2984_native_cpu_ring_render_checked/report.json'
    proof=json.loads(checked.read_text());assert proof['passed'] and not proof['fullPortAcceptance']
    prior=json.loads((ROOT/'audit_v2972_native_cpu_ring_checked/report.json').read_text())
    guest,control,payload,_,_=model.assembly.expected()
    pins=dict(proof['inputHashes']);pins[str(checked)]=model.assembly.sha(checked)
    tests=[]
    for case_key,case in proof['cases'].items():
        CASE=ROOT/case['case'];player=case_key
        image=guest if case_key.startswith('new')else control
        actual=model.raster.data(CASE);groups,buffers,a,b,owners=actual
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
        # Positive control through the identical mock path; preserve empty
        # defaultdict event groups so no absent-key exception can masquerade
        # as detecting an injected rendering fault.
        variant=copy.deepcopy(actual)
        with patch.object(model.raster,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant):
            positive=model.verify(CASE,case_key,prior,image,payload)
        assert positive['passed'] and positive['exactScreenPixels']==case['exactScreenPixels']
        expected={
            'proxy_CPU_identity': "all(q[k]==inventory[key][k]",
            'detached_physical_owner': "q['owner']==q['actor']",
            'physical_publication_missing_from_full_inventory': "all(q[k]==inventory[key][k]",
            'tracked_source_disagrees_with_independent_inventory': "all(q[k]==inventory[key][k]",
            'camera_context_belongs_to_wrong_actor': "all(t[k]==q[k]",
            'camera_y_shifted_one_pixel': 'Every part uses actual queued camera',
            'display_y_shifted_one_pixel': 'Every part uses actual queued camera',
            'native_DMA_y_shifted_one_pixel': "q['xy']>>16&511==d['y']",
            'native_DMA_x_shifted_one_pixel': "q['xy']&1023==d['x']",
            'own_floor_shifted_one_pixel': "t['stageY']-(134",
            'original_cached_body_part_offset_shifted': 'len(actual)==len(composition)',
            'native_shadow_palette_not_black_bank': "streams['rowStreamVerified']",
            'native_shadow_color_not_black_pen': "streams['rowStreamVerified']",
            'native_shadow_copy_missing_ownership': 'Every imported shadow copy',
            'projectile_belongs_to_wrong_parent': "q['parent']==actors",
            'projectile_belongs_to_wrong_Main': "all(t[k]==q[k]",
            'child_publication_missing_from_full_inventory': "all(q[k]==inventory[key][k]",
            'projectile_projection_context_wrong_actor': "all(t[k]==q[k]",
            'ring_graphic_republished_after_retirement': 'No knife/impact art outside',
        }
        def reject(name,change):
            mutated=copy.deepcopy(groups)
            change(mutated)
            assert mutated!=groups,'Nonvacuous actual display mutation '+name
            variant=(mutated,buffers,a,b,owners)
            with patch.object(model.raster,'data',return_value=variant),patch.object(model.shadow,'data',return_value=variant):
                try:model.verify(CASE,case_key,prior,image,payload)
                except(AssertionError,ValueError,KeyError)as error:
                    condition=traceback.extract_tb(error.__traceback__)[-1].line or ''
                    assert expected[name] in str(error)+' '+condition, (name,type(error).__name__,str(error),condition)
                    if isinstance(error,KeyError):
                        wanted=tuple((key if name=='physical_publication_missing_from_full_inventory' else child_key)[k]for k in ('frame','cursor'))
                        assert name in ('physical_publication_missing_from_full_inventory','child_publication_missing_from_full_inventory') and error.args==(wanted,), 'Only deliberately removed FIFO key may produce KeyError'
                    tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error),rejectedCondition=condition))
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
            publication=next(r for r in g['FLOOR_ALL_QUEUE']if r['frame']>dead)
            publication.update(actor=child_queue['actor'],pose=child_queue['pose'],source=child_queue['source'])
        reject('ring_graphic_republished_after_retirement',orphan)
        # Corrupt only returned palette arrays, not the actual stored evidence.
        charged=next(r for r in groups['FLOOR_QUEUE']if r['slot']==2 and r['pose']in model.charge.CHARGE_POSES)
        restored=next(r for r in groups['FLOOR_QUEUE']if r['slot']==2 and r['pose']==model.state.BODY[18][-1])
        displays={r['frame']:r for r in groups['FLOOR_DISPLAY']}
        original_fromfile=np.fromfile
        def palette_reject(name,q):
            path=CASE/displays[q['frame']+1]['palette_file'];bank=q['bank']&0x7f00
            def changed(file,*args,**kwargs):
                array=original_fromfile(file,*args,**kwargs)
                if Path(file)==path:
                    array=array.copy();array[bank+10]^=1
                return array
            with patch.object(np,'fromfile',side_effect=changed):
                try:model.verify(CASE,case_key,prior,image,payload)
                except(AssertionError,ValueError,KeyError,IndexError)as error:
                    tests.append(dict(player=player,name=name,rejected=True,errorType=type(error).__name__,error=str(error)))
                else:raise AssertionError('Accepted corrupted palette '+name)
            print(player+' rejected '+name+' ('+str(len(tests))+')',flush=True)
        palette_reject('original_ring_charge_colour_changed',charged)
        palette_reject('normal_release_colour_not_restored',restored)

        real=model.verify(CASE,case_key,prior,image,payload)
        for key in ('sampledFrames','exactScreenPixels','exactOwnedPixels','fullOwnedPaletteChecks','nativeShadowCopies','sourceBoundProjections','originalChargePaletteSamples','restoredReleaseBodyPaletteSamples'):
            assert real[key]==case[key],'Final untouched actual scene matches accepted result'
    assert len(tests)==63,'All63 original geometry/identity/FIFO/palette/native shadow/retirement counterexamples rejected'
    for file,wanted in pins.items():assert model.assembly.sha(file)==wanted,'Actual immutable source and captures'
    pins[str(Path(__file__).resolve())]=model.assembly.sha(__file__)
    return dict(passed=True,actualPhysicalFixtures=3,actualOriginalRenderCounterexamplesRejected=len(tests),
        counterexamples=tests,sameMockedPathPositiveControlAccepted=True,unrelatedMissingEventExceptionsNeverAccepted=True,actualCapturesUnmodified=True,gameChanged=False,
        allArenaMoveCPUOrMorphsAccepted=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    assert not OUT.exists(),'Immutable actual ring render negative evidence'
    try:value=run()
    except Exception as error:
        import traceback
        value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('inputHashes','counterexamples','scope')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
