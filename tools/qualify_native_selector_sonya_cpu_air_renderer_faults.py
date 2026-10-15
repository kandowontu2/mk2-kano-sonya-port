"""Original pure native renderer equations: effective faults on actual50372."""
import json,traceback
from collections import ChainMap
from pathlib import Path
import qualify_native_selector_sonya_cpu_air_display as display_proof
import qualify_native_selector_sonya_pressure_renderer_faults as equations

ROOT,need,sha=display_proof.ROOT,display_proof.need,display_proof.sha
OUT=ROOT/'audit_native_selector_sonya_cpu_air_renderer_faults_checked'
CONTEXT=None


def execute(state):
    global CONTEXT
    need(not OUT.exists(),'Fresh immutable actual airborne renderer fault proof')
    parent=display_proof.OUT/'report.json';proof=json.loads(parent.read_text())
    capture=display_proof.control.capture;held=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed'] and held['process'].poll()==0 and held['identity']==proof['actualNativeIdentity'],
         'Same whole scanout-qualified terminal50372, not new gameplay')
    pins=dict(proof['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Whole original source/capture inventory intact')
    folder,text,_=capture.RAM_CASES[capture.KEY];display=capture.DISPLAY
    CONTEXT=equations.prepare(text,display)
    frames=(1818,2392,2732,2752,2761,2777,2803,2814,3617)
    need(set(frames)<=set(CONTEXT['latches']),'Real native flips across miss/contact/float/release/both recoveries/UI')
    positive={f:equations.one_pass(folder,CONTEXT,f,display) for f in frames};faults=[]
    def reject(label,frame,action):
        try:action()
        except (ValueError,AssertionError) as error:faults.append(dict(kind=label,frame=frame,rejectedBy=str(error)))
        else:raise ValueError('Effective native renderer fault admitted: '+label)
        need(equations.one_pass(folder,CONTEXT,frame,display)==positive[frame],'Whole untouched independent native pass restored after each fault')
    for f in frames:
        file=CONTEXT['latches'][f]['file'];raw=bytearray(display['buffers'][file]);raw[-1]^=1
        changed=dict(display,buffers=ChainMap({file:bytes(raw)},display['buffers']))
        reject('actual_full_target_VRAM_word_'+str(f),f,lambda:equations.one_pass(folder,CONTEXT,f,changed))
    f=1818;events=equations.window(CONTEXT,f);anchor=events[0][1]
    raw=bytearray(display['buffers'][anchor['file']]);raw[-1]^=1
    changed=dict(display,buffers=ChainMap({anchor['file']:bytes(raw)},display['buffers']))
    reject('actual_hidden_prepass_word',f,lambda:equations.one_pass(folder,CONTEXT,f,changed))
    flip=events[-1][1];changed_flip=dict(flip,value=flip['value']^16)
    reject('actual_native_flip_row',f,lambda:equations.one_pass(folder,CONTEXT,f,display,{flip['event']:changed_flip}))
    body_frame,body=next((frame,r) for frame in sorted(CONTEXT['latches']) for kind,r in reversed(equations.window(CONTEXT,frame))
                        if kind=='FLOOR_DMA' and r['slot']==2 and r['command']&15==2 and r['width'] and r['height'])
    positive[body_frame]=equations.one_pass(folder,CONTEXT,body_frame,display)
    for label,key,value in (('actual_native_body_palette','palette',body['palette']^0x100),
                            ('actual_native_body_X','x',body['x']^1),('actual_native_body_clip','right',0)):
        mutated=dict(body);mutated[key]=value
        reject(label,body_frame,lambda:equations.one_pass(folder,CONTEXT,body_frame,display,{body['event']:mutated}))
    cpu_frame,cpu=next((frame,r) for frame in sorted(CONTEXT['latches']) for kind,r in equations.window(CONTEXT,frame)
                       if kind=='FLOOR_CPU' and r['mask'])
    positive[cpu_frame]=equations.one_pass(folder,CONTEXT,cpu_frame,display)
    before='before%d'%(0 if cpu['mask']&255 else 1);mutated=dict(cpu);mutated[before]^=1
    reject('actual_consumed_CPU_prewrite_word',cpu_frame,
           lambda:equations.one_pass(folder,CONTEXT,cpu_frame,display,{cpu['event']:mutated}))
    need(len(faults)==15,'All target/independent-anchor/flip/body/CPU faults effective')
    restored=CONTEXT['renderer'](folder)
    need(json.loads(json.dumps(restored))==proof['sourceExactSavedPassCPUandDMAReplay'],
         'Entire original full-pass positive restored, with exact JSON key representation')
    for p in (Path(__file__),parent,Path(equations.__file__)):
        key=str(p.resolve());digest=sha(p);need(key not in pins or pins[key]==digest,'No executed source or prior proof changed');pins[key]=digest
    need(all(sha(p)==h for p,h in pins.items()),'All whole source/native pins unchanged after restored renderer')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        actualIndependentPassPositives=list(positive.values()),effectiveRendererFaultsRejected=faults,
        originalWholeSavedPassPositiveRestored=True,wholeExactPassVRAMWords=proof['wholeExactNativePassVRAMWords'],
        actualClassifiedBodyFaultFrame=body_frame,actualConsumedCPUStore=dict(frame=cpu_frame,event=cpu['event'],at=cpu['at'],pc=cpu['pc'],mask=cpu['mask']),
        actualAirTrialRendererFaultSuiteAccepted=True,allUnsavedErasureAccepted=False,allEffectOwnershipAccepted=False,
        fullPortAcceptance=False,publicPlayableChanged=False,inputHashes=pins,requirements=proof['requirements'],remainingGroups=proof['remainingGroups'],
        newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n');return value


def safe_execute(state):
    try:return execute(state)
    except Exception as error:
        need(not OUT.exists(),'Preserve actual native renderer proof failure')
        OUT.mkdir();(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False),indent=2)+'\n')
        raise
