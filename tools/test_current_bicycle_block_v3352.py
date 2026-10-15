"""Qualified corruptions of actual both-slot current Bicycle block evidence."""
import json
import re
import traceback
from pathlib import Path
import verify_current_bicycle_block_v3350 as checked

ROOT=checked.ROOT;OUT=ROOT/'audit_v3353_current_bicycle_block_counterexamples';need=checked.need

def alter(log,tag,frame,slot,key,value,kind=None):
    lines=log.splitlines();count=0
    for index,line in enumerate(lines):
        if not line.startswith('MK2_BBLOCK_'+tag+' ')or not re.search(r'\bframe='+str(frame)+r'\b',line):continue
        if slot is not None and not re.search(r'\bslot='+str(slot)+r'\b',line):continue
        if kind is not None and not re.search(r'\bkind='+kind+r'\b',line):continue
        match=re.search(r'\b'+key+r'=(\S+)',line);need(match is not None,'Existing native mutation key')
        replacement=value(match[1])if callable(value)else value
        need(replacement!=match[1],'Mutation actually changes captured evidence')
        lines[index]=line[:match.start(1)]+replacement+line[match.end(1):];count+=1
    need(count==1,'Unique exact actual native mutation target')
    return '\n'.join(lines)+'\n'

def run():
    proof_path=checked.OUT/'report.json';proof=json.loads(proof_path.read_text());need(proof['passed'],'Executed current native both-slot proof')
    pins=dict(proof['inputHashes']);pins[str(proof_path)]=checked.current.assembly.sha(proof_path)
    for file,digest in pins.items():need(checked.current.assembly.sha(file)==digest,'All real executed source/capture pins unchanged')
    rejected=[];controls=[]
    for side in (1,2):
        folder=ROOT/f'audit_v3347_current_bicycle_block_p{side}_kano'
        log=(folder/'run.log').read_text(encoding='utf-8-sig');guest=(folder/'guest_maincpu.bin').read_bytes()
        expected=next(c for c in proof['cases']if c['side']==side);positive=checked.phase(log,guest,side)
        need(positive=={k:v for k,v in expected.items()if k!='case'},'Same-path actual blocked positive control')
        start,hit=positive['start'],positive['contact'];victim=3-side
        flip=lambda text:format(int(text,16)^1,'08X')
        specs=[
            ('entry_snapshot_frame','ENTRY_STATE',start,side,'frame',str(start+1),None,'Both native entry snapshots belong to exact actual entry field'),
            ('wrong_real_id','FIELD',start+3,side,'id','1',None,'Every real selected human ID, owner, arena and native anchor'),
            ('wrong_floor_anchor','FIELD',start+4,side,'floor','82',None,'Every real selected human ID, owner, arena and native anchor'),
            ('proxy_paired_catch','FIELD',hit+2,side,'action','00000214',None,'No paired catch or persistent trail after actual block'),
            ('persistent_trail','FIELD',hit+2,side,'trail','00000001',None,'No paired catch or persistent trail after actual block'),
            ('wrong_instruction_owner','EVENT',hit,None,'a8','01000000','contact','Every actual blocked native instruction'),
            ('wrong_source_opcode','EVENT',hit,None,'opcode','0000','blocked','Every actual blocked native instruction'),
            ('no_native_block_flag','EVENT',hit,None,'b2','00000000','block_test','Actual collision carry and nonzero original block flag'),
            ('wrong_rebound_gravity_argument','EVENT',hit,None,'a2','0000A000','fling','Source-derived blocked stationary -6/half-gravity rebound parameters'),
            ('full_hit_instead_of_chip','HEALTH',hit,victim,'after','139',None,'Exactly3actual chip damage'),
            ('unexplained_chip_callback','FIELD',hit+1,victim,'hp','139',None,'Every physical HP callback matches exact original chip ledger'),
            ('wrong_owned_flag_target','FLAG',hit,side,'at','01000000','action','Each blocked state writer targets its actual owned field'),
            ('wrong_flag_opcode','FLAG',hit,side,'op0','0000','action','Every blocked state store source-bound'),
            ('wrong_flag_publication','FLAG',hit,side,'after','0610','action','Every blocked state callback matches all native stores'),
            ('startup_pixel_shift','FIELD',start+3,side,'xraw',flip,None,'All six original blocked startup fields'),
            ('lost_floor_fraction','FIELD',hit+1,side,'yraw','00510000',None,'Exact original blocked fling initial floor clamp preserves fractional Y'),
            ('rebound_coordinate','FIELD',hit+6,side,'yraw',flip,None,'Every original stationary blocked rebound vertical step'),
            ('rebound_pose','FIELD',hit+2,side,'pose','FE83EBC0',None,'Every original four-field continuing blocked cycle pose'),
            ('landing_coordinate','FIELD',positive['landing']+1,side,'yraw',flip,None,'Every original blocked grounded landing hold'),
        ]
        def reject(label,changed_log,changed_guest,reason):
            try:checked.phase(changed_log,changed_guest,side)
            except ValueError as error:
                need(reason in str(error),'Only intended invariant rejects '+label+': '+str(error))
                rejected.append(dict(side=side,label=label,reason=str(error)))
            else:raise ValueError('Actual blocked corruption accepted: '+label)
        for label,tag,frame,slot,key,value,kind,reason in specs:
            reject(label,alter(log,tag,frame,slot,key,value,kind),guest,reason)
        # Preserve actual C/status consistency but contradict the reached contact.
        changed=alter(log,'EVENT',hit,None,'carry','0','contact')
        changed=alter(changed,'EVENT',hit,None,'status','00200030','contact')
        reject('lost_contact_carry',changed,guest,'Actual collision carry and nonzero original block flag')
        lines=log.splitlines();indices=[i for i,line in enumerate(lines)if line.startswith('MK2_BBLOCK_EVENT ')and
                                     ('kind=contact 'in line or 'kind=block_test 'in line)]
        need(len(indices)==2,'Actual causal ordering mutation targets')
        lines[indices[0]],lines[indices[1]]=lines[indices[1]],lines[indices[0]]
        reject('reordered_block_contact','\n'.join(lines)+'\n',guest,'Exact original collision/contact/block/rebound/ready causal event order')
        for label,offset,reason in (
            ('changed_attack_block_damage',(0xfff9ee00-0xff800000)//8+2,'Entire actual own22hit/3block collision descriptor'),
            ('changed_original_floor_clamp',(0xff876900-0xff800000)//8,'Original fling/timer/cleanup/ready routines unchanged')):
            changed=bytearray(guest);changed[offset]^=1;reject(label,log,bytes(changed),reason)
        need(checked.phase(log,guest,side)==positive,'Same-path untouched blocked phase still passes after all negatives')
        controls.append(dict(side=side,contact=hit,regain=positive['regain']))
    pins[str(Path(__file__).resolve())]=checked.current.assembly.sha(__file__)
    return dict(passed=True,actualCounterexamplesRejected=len(rejected),physicalSlots=2,
                specificFailures=rejected,samePathPositiveControlsAccepted=True,positiveControls=controls,
                unrelatedMissingEventExceptionsNeverAccepted=True,captureSourceAndGameUnchanged=True,
                inputHashes=pins,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Immutable actual blocked corruption evidence')
    try:result=run()
    except Exception as error:result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ('inputHashes','specificFailures')},indent=2),flush=True)
    raise SystemExit(0 if result['passed']else 1)
