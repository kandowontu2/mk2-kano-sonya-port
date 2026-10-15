"""Effective coverage/native horizontal/source faults on original terminal44988.

Full drawing geometry, all store-operand registers, repeated-cue waveform and
broader integration remain open. No new game or altered guest state.
"""
import inspect
import json
import re
from pathlib import Path
import qualify_native_selector_sonya_shadow_bound_startup as previous
import qualify_native_selector_sonya_choice_av_observed_bound as phases

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_shadow_bound_faults_checked'


def execute(state):
    need(not OUT.exists(),'Fresh immutable actual native counterexample checkpoint')
    scope=dict(vars(previous))
    source=inspect.getsource(previous.execute)
    source=phases.original.phase_source.replace(source,"return scope['execute'](state)",'return scope')
    exec(compile(source,__file__+'::entire_original_bindings_without_second_execution','exec'),scope)
    bindings=scope['execute'](state)
    base=previous.previous.previous
    capture=base.capture
    folder,text,images=capture.RAM_CASES[capture.KEY]
    held=capture.NATIVE_HANDLES[capture.KEY]
    parent=json.loads((previous.OUT/'report.json').read_text())
    need(parent['passed'] and held['process'].poll()==0 and held['identity']==parent['actualNativeIdentity'],
         'Same original terminal native capture, not a replay')
    def check(text,guest):
        phases.original.phase_source.source_gate(text,guest)
        return dict(coverage=bindings['gate'](text,guest),horizontal=bindings['horizontal'](text,guest))
    positive=check(text,state['guest'])
    need(positive==dict(coverage=parent['coverage'],horizontal=parent['horizontal']),
         'Exact entire accepted native coverage/store result, plus whole initialized source')
    def change(tag,key,value,**where):
        line=next(s for s in text.splitlines() if s.startswith(tag+' ') and
                  all(dict(re.findall(r'(\w+)=([^\s]+)',s)).get(k)==str(v) for k,v in where.items()))
        bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
        need(n==1 and bad!=line,'Actual effective native record corruption')
        return text.replace(line,bad,1)
    mutations=[('post_owner',change('MK2_HPHASE_POST_FIELD','owner','01000000',frame=3200,slot=2)),
               ('post_floor',change('MK2_HPHASE_POST_FIELD','floor','82',frame=3200,slot=2)),
               ('shadow_pose',change('MK2_HPHASE_SHADOW_BEGIN','pose','00000000',frame=3200,slot=2)),
               ('entry_proxy',change('MK2_HPHASE_CPU_NATIVE_ENTRY','id','1',frame=3191)),
               ('opening_opcode',change('MK2_FIRST_PROJECTILE_ENTRY','opcode','FFFF',frame=1817)),
               ('binding_not_executed',change('MK2_SONYA_SHADOW_BIND','count','0')),
               ('boundary_high_word',change('MK2_SONYA_HORIZONTAL_STORE','data','0000003D',frame=3232,slot=2,pc='FF805630')),
               ('boundary_PC',change('MK2_SONYA_HORIZONTAL_STORE','pc','FF805640',frame=3232,slot=2,pc='FF805630')),
               ('velocity_before',change('MK2_SONYA_HORIZONTAL_STORE','before','00000000',frame=3232,slot=2,pc='FF805580',at='010350E0')),
               ('velocity_mask',change('MK2_SONYA_HORIZONTAL_STORE','mask','0000FFFE',frame=3232,slot=2,pc='FF805580',at='010350E0'))]
    line=next(s for s in text.splitlines() if s.startswith('MK2_HPHASE_POST_FIELD ') and 'frame=3200 ' in s and 'slot=2 ' in s)
    mutations.append(('missing_actual_draw',text.replace(line+'\n','',1)))
    faults=[]
    for name,bad in mutations:
        try:check(bad,state['guest'])
        except (AssertionError,ValueError,KeyError,IndexError) as error:faults.append(dict(fault=name,rejectedBy=str(error)))
        else:raise ValueError('Actual corrupted native evidence accepted: '+name)
        print('Native draw/horizontal fault rejected: '+name,flush=True)
    guest=bytearray(state['guest']);guest[(0xff805560-0xff800000)//8]^=1
    try:check(text,bytes(guest))
    except (AssertionError,ValueError) as error:faults.append(dict(fault='actual_boundary_instruction',rejectedBy=str(error)))
    else:raise ValueError('Changed actual native boundary code accepted')
    need(check(text,state['guest'])==positive and len(faults)==12,'Whole unchanged positive restored after every effective corruption')
    pins=dict(parent['inputHashes'])
    for p in (Path(__file__),Path(previous.__file__),Path(phases.__file__),previous.OUT/'report.json',
              ROOT/'mame-mkp/src/frontend/mame/mame.cpp',ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp'):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No historical source pin replacement');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'Fresh entire source/build/evidence census')
    OUT.mkdir()
    value=dict(passed=True,actualNativeIdentity=held['identity'],qualification=positive,effectiveFaultsRejected=faults,
               requirements=parent['requirements'],remainingGroups=json.loads(capture.previous.PARENT.read_text())['remainingGroups'],
               goalStatus='active',inputHashes=pins,wholeShadowGeometryAccepted=False,wholeSourceMixedPCMStillOpen=True,
               allStoreOperandRegistersCaptured=False,allContactsArenasAccepted=False,fullPortAcceptance=False,
               publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    phases.original.capture.choices.current.prior.save(OUT/'report.json',value)
    print('PASS actual complete drawing admission and all bicycle masked x/vx stores;12 effective faults rejected',flush=True)
    return value
