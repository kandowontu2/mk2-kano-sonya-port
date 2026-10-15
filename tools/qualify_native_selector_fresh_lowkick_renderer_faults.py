"""Effective immutable-record faults on current lowkick/Square native renderer."""
import json
import traceback
from collections import ChainMap
from pathlib import Path
import qualify_native_selector_fresh_lowkick_display as display_proof
import qualify_native_selector_sonya_pressure_renderer_faults as equations
import verify_native_source_sync as sync

OUT=sync.ROOT/'audit_native_selector_fresh_lowkick_renderer_faults_checked'
CONTEXT=None


def main(prepared):
    global CONTEXT
    try:
        sync.need(not OUT.exists(),'Fresh immutable renderer fault proof')
        parent=display_proof.OUT/'report.json'; proof=json.loads(parent.read_text())
        key=prepared.SCOPE['KEY']; handle=prepared.NATIVE_HANDLES[key]
        sync.need(proof['passed'] and handle['process'].poll()==0 and handle['identity']==proof['actualNativeIdentity'],
                  'Same independently display-qualified actual terminal')
        pins=dict(proof['inputHashes'])
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'All whole original inputs unchanged')
        folder,text,_=prepared.RAM_CASES[key]; display=prepared.DISPLAY
        CONTEXT=equations.prepare(text,display)
        frames=(1818,1911,1917,1955,2129,2131,2155,2572,3617)
        sync.need(set(frames)<=set(CONTEXT['latches']),'Actual flips across attack/hit/recovery/interruption/Square/UI')
        positives={f:equations.one_pass(folder,CONTEXT,f,display) for f in frames}; faults=[]
        def reject(label,f,action):
            try: action()
            except (AssertionError,ValueError) as error: faults.append(dict(name=label,frame=f,rejected=True,reason=str(error)))
            else: raise AssertionError('Effective fault accepted: '+label)
            sync.need(equations.one_pass(folder,CONTEXT,f,display)==positives[f],'Untouched native pass restored')
        for f in frames:
            file=CONTEXT['latches'][f]['file']; raw=bytearray(display['buffers'][file]); raw[-1]^=1
            changed=dict(display,buffers=ChainMap({file:bytes(raw)},display['buffers']))
            reject('wrong_full_target_word',f,lambda:equations.one_pass(folder,CONTEXT,f,changed))
        f=1818; events=equations.window(CONTEXT,f); anchor=events[0][1]
        raw=bytearray(display['buffers'][anchor['file']]); raw[-1]^=1
        changed=dict(display,buffers=ChainMap({anchor['file']:bytes(raw)},display['buffers']))
        reject('wrong_independent_prepass_word',f,lambda:equations.one_pass(folder,CONTEXT,f,changed))
        flip=events[-1][1]; mutated=dict(flip,value=flip['value']^16)
        reject('shifted_flip_row',f,lambda:equations.one_pass(folder,CONTEXT,f,display,{flip['event']:mutated}))
        body_frame,body=next((f,r) for f in frames for kind,r in reversed(equations.window(CONTEXT,f))
                             if kind=='FLOOR_DMA' and r['slot']==2 and r['command']&15==2 and r['width'] and r['height'])
        for label,key,value in (('wrong_body_palette','palette',body['palette']^0x100),
                                ('one_pixel_body_shift','x',body['x']^1),('wrong_body_clip','right',0)):
            mutated=dict(body); mutated[key]=value
            reject(label,body_frame,lambda:equations.one_pass(folder,CONTEXT,body_frame,display,{body['event']:mutated}))
        cpu_frame,cpu=next((f,r) for f in sorted(CONTEXT['latches']) for kind,r in equations.window(CONTEXT,f)
                           if kind=='FLOOR_CPU' and r['mask'])
        positives[cpu_frame]=equations.one_pass(folder,CONTEXT,cpu_frame,display)
        part='before0' if cpu['mask']&255 else 'before1'; mutated=dict(cpu); mutated[part]^=1
        reject('wrong_consumed_cpu_prewrite',cpu_frame,
               lambda:equations.one_pass(folder,CONTEXT,cpu_frame,display,{cpu['event']:mutated}))
        sync.need(len(faults)==15,'Every target/prepass/flip/body/CPU fault effective')
        print('All15 current renderer faults rejected; full positive replay starting',flush=True)
        restored=CONTEXT['renderer'](folder)
        sync.need(json.loads(json.dumps(restored))==proof['nativeSavedPassReplay'],'All original whole pass positives restored')
        for p in (Path(__file__),Path(equations.__file__),parent): pins[str(p.resolve())]=sync.sha(p)
        sync.need(all(sync.sha(p)==h for p,h in pins.items()),'All complete source and actual evidence unchanged')
        report=dict(passed=True,actualNativeIdentity=proof['actualNativeIdentity'],effectiveFaults=faults,
                    landmarkPasses=list(positives.values()),wholePositiveRestored=True,
                    wholeExactVRAMWords=proof['wholeExactVRAMWords'],inputHashes=pins,
                    allUnsavedErasureAccepted=False,allEffectOwnershipAccepted=False,visualReviewAccepted=False,
                    fullPortAcceptance=False,newGames=0,newBuilds=0,newRawMediaFiles=0)
        OUT.mkdir(); (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n'); return report
    except BaseException:
        OUT.mkdir(exist_ok=True); (OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=traceback.format_exc()),indent=2)+'\n')
        raise
