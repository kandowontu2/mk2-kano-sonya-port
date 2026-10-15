"""Specific actual both-slot guard-dispatch/wait/request/integration corruptions."""
import json
import re
import traceback
from pathlib import Path
import verify_current_bicycle_block_push_v3382 as checked

ROOT=checked.ROOT;OUT=ROOT/'audit_v3381_current_bicycle_block_push_counterexamples';need=checked.need

def altered(log,tag,where,key,value,remove=False):
    lines=log.splitlines();found=[]
    for i,line in enumerate(lines):
        if not line.startswith(tag+' '):continue
        row=dict(re.findall(r'(\w+)=([^\s]+)',line))
        if all(row.get(k)==str(v)for k,v in where.items()):found.append(i)
    need(len(found)==1,'Exactly one actual mutation target '+tag+' '+str(where))
    at=found[0]
    if remove:lines.pop(at)
    else:
        lines[at],count=re.subn(r'\b'+key+r'=\S+',key+'='+str(value),lines[at]);need(count==1,'One actual mutated column')
    result='\n'.join(lines)+'\n';need(result!=log,'Nonvacuous actual mutation');return result

def run():
    positive=checked.run();rejected=[]
    guest=checked.prior.current.expected_current()[0]
    for side in (1,2):
        victim=3-side;folder=ROOT/f'audit_v3375_current_bicycle_block_push_p{side}_kano'
        log=(folder/'run.log').read_text(encoding='utf-8-sig');typed=positive['state']['cases'][side-1]
        case=positive['cases'][side-1];first=case['guardEntry'];end=case['guardStop']
        event='MK2_BBPUSH_EVENT';request='MK2_BBPUSH_REQUEST';states='MK2_BBPUSH_REQUEST_STATE';field='MK2_BBLOCK_FIELD'
        own=checked.prior.rows(log,'FIELD');by={(r['frame'],r['slot']):r for r in own}
        specs=[
            ('guard_speed',event,{'kind':'away_request'},'a0','00030000','Actual source-selected reaction/speed/two-wait/three-cycle standing-block parameters'),
            ('handler_selection',event,{'kind':'guard_handler'},'a7','FF8E8A10','Actual source-selected reaction/speed/two-wait/three-cycle standing-block parameters'),
            ('guard_dispatch_late',event,{'kind':'guard_handler'},'frame',first+1,'Original causal guard dispatch and complete twelve-field stop/return timing'),
            ('cycle_delay',event,{'kind':'guard_cycle'},'a11','00000003','Actual source-selected reaction/speed/two-wait/three-cycle standing-block parameters'),
            ('cycle_count',event,{'kind':'guard_cycle'},'a10','00000004','Actual source-selected reaction/speed/two-wait/three-cycle standing-block parameters'),
            ('wait_duration',event,{'kind':'sleep','frame':first+2},'a0','00000003','Every actual native two-field wait and three-cycle decrement'),
            ('wait_remaining_cycles',event,{'kind':'sleep','frame':first+4},'a10','00000003','Every actual native two-field wait and three-cycle decrement'),
            ('early_native_stop',event,{'kind':'guard_stop'},'frame',end-1,'Original causal guard dispatch and complete twelve-field stop/return timing'),
            ('late_native_return',event,{'kind':'guard_return'},'frame',end+1,'Original causal guard dispatch and complete twelve-field stop/return timing'),
            ('detached_guard_owner',event,{'kind':'away_request'},'actor','01000000','Every actual guard event has its native source and physical owner'),
            ('wrong_guard_opcode',event,{'kind':'guard_handler'},'opcode','0000','Every actual guard event has its native source and physical owner'),
            ('wrong_request_mask',request,{'frame':first,'slot':victim,'shift':16,'value':('0002'if side==1 else'FFFE')},'mask','000000FF','Every native physical request half-write and owner source-bound'),
            ('wrong_request_high_half',request,{'frame':first,'slot':victim,'shift':16,'value':('0002'if side==1 else'FFFE')},'value','0003','Exact native half-write replacement'),
            ('wrong_request_caller',request,{'frame':end,'slot':victim,'shift':16},'pc','FF831B30','Every native physical request half-write and owner source-bound'),
            ('wrong_request_shift',request,{'frame':end,'slot':victim,'shift':16},'shift',0,'Every native physical request half-write and owner source-bound'),
            ('invented_request_callback',states,{'frame':first+1,'slot':victim},'requested','00030000','Every requested-velocity callback matches all native stores'),
            ('victim_position_one_pixel',field,{'frame':first+2,'slot':victim},'xraw',f"{by[first+2,victim]['xraw']+65536:08X}",'Both exact blocked horizontal fixed-point integrations'),
            ('own_position_one_pixel',field,{'frame':first+2,'slot':side},'xraw',f"{by[first+2,side]['xraw']+65536:08X}",'Both exact blocked horizontal fixed-point integrations'),
            ('victim_wrong_publication',field,{'frame':first+1,'slot':victim},'vx','00030000','Every source-derived native requested/published blocked velocity'),
            ('own_wrong_publication',field,{'frame':first+1,'slot':side},'vx','00010000','Every source-derived native requested/published blocked velocity'),
            ('late_victim_drift',field,{'frame':end+3,'slot':victim},'xraw',f"{by[end+3,victim]['xraw']+1:08X}",'Both exact blocked horizontal fixed-point integrations'),
            ('defender_floor_fraction',field,{'frame':first+1,'slot':victim},'yraw',f"{by[first+1,victim]['yraw']+1:08X}",'Actual defender remains naturally grounded in standing block'),
            ('defender_wrong_action',field,{'frame':first+1,'slot':victim},'action','00000303','Actual defender remains naturally grounded in standing block'),
        ]
        def reject(label,mutant,program,reason):
            try:checked.verify(mutant,program,side,typed)
            except ValueError as error:
                need(str(error)==reason,'Only specifically intended native push invariant qualifies '+label+': '+str(error))
                rejected.append(dict(side=side,name=label,rejectedBy=str(error)))
            else:raise ValueError('Accepted actual corrupted native guard evidence '+label)
        for label,tag,where,key,value,reason in specs:reject(label,altered(log,tag,where,key,value),guest,reason)
        reject('missing_actual_wait',altered(log,event,{'kind':'sleep','frame':first+4},'',None,True),guest,
               'Every actual native two-field wait and three-cycle decrement')
        reject('missing_actual_stop',altered(log,event,{'kind':'guard_stop'},'',None,True),guest,'Exactly one actual native guard_stop')
        reject('missing_high_half',altered(log,request,{'frame':end,'slot':victim,'shift':16},'',None,True),guest,
               'Every actual thirty-two-bit request includes both ordered sixteen-bit stores')
        lines=log.splitlines();a=next(i for i,s in enumerate(lines)if s.startswith(event+' ')and'kind=guard_stop 'in s)
        b=next(i for i,s in enumerate(lines)if s.startswith(event+' ')and'kind=guard_return 'in s)
        lines[a],lines[b]=lines[b],lines[a]
        reject('return_before_stop','\n'.join(lines)+'\n',guest,'Exact dispatch/request/cycle/stop/return causal order')
        for label,at,reason in (
            ('native_wait_loop_opcode',0xff8ea110,'Original native blocked source with exactly two independently verified table relocations'),
            ('native_speed_operand',0xff8e82c0,'Original native blocked source with exactly two independently verified table relocations'),
            ('native_lookup_operand',0xff9060a0,'Original native blocked source with exactly two independently verified table relocations'),
            ('native_own_callback_table',0xffff8800+17*32,'Entire actual nineteen-ID lookup equals independent whole-port assembly'),
            ('native_block_descriptor_selector',0xfff9ee00+4*16,'Actual Bicycle descriptor selects original two-pixel/two-wait/three-cycle guard reaction')):
            mutant=bytearray(guest);mutant[(at-0xff800000)//8]^=1;reject(label,log,bytes(mutant),reason)
        need(checked.verify(log,guest,side,typed)==case,'Same-path unchanged actual physical-slot positive control')
        print('All32 native horizontal counterexamples rejected for physical slot '+str(side),flush=True)
    need(len(rejected)==64,'All thirty-two specific native push corruptions per actual physical order')
    pins=dict(positive['inputHashes']);pins[str(checked.OUT/'report.json')]=checked.prior.current.assembly.sha(checked.OUT/'report.json')
    pins[str(Path(__file__).resolve())]=checked.prior.current.assembly.sha(__file__)
    for file,digest in pins.items():need(checked.prior.current.assembly.sha(file)==digest,'Source/capture/game bytes unchanged')
    return dict(passed=True,physicalSlots=2,actualCounterexamplesRejected=len(rejected),counterexamples=rejected,
                samePathPositiveControlsAccepted=True,specificRejectionReasonsRequired=True,
                unrelatedMissingEventExceptionsNeverAccepted=True,sourceCaptureAndGameUnchanged=True,
                fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite executed native push counterexamples')
    try:value=run()
    except Exception as error:value=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print(json.dumps({k:v for k,v in value.items()if k not in ('counterexamples','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if value['passed']else 1)
