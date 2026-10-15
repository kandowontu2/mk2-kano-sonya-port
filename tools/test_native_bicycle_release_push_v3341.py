"""Specific release-trajectory corruptions and original push-branch boundaries."""
import json
import re
import traceback
from pathlib import Path
import verify_native_bicycle_release_push_v3337 as checked

ROOT=checked.ROOT
OUT=ROOT/'audit_v3342_native_bicycle_release_push_counterexamples'
need=checked.need

def replace_field(log,tag,frame,key,value,slot=None):
    found=0;lines=log.splitlines()
    for index,line in enumerate(lines):
        if not line.startswith(tag+' ') or not re.search(r'\bframe='+str(frame)+r'\b',line):continue
        if slot is not None and not re.search(r'\bslot='+str(slot)+r'\b',line):continue
        altered,count=re.subn(r'\b'+key+r'=\S+',key+'='+value,line)
        need(count==1,'Actual single mutation target '+key)
        lines[index]=altered;found+=1
    need(found>0,'Actual captured mutation line required')
    return '\n'.join(lines)+'\n'

def run():
    positive=checked.run()
    proof=json.loads((checked.prior.OUT/'report.json').read_text())
    typed=proof['case']['phase'];case=ROOT/checked.prior.CASE
    log=(case/'run.log').read_text(encoding='utf-8-sig');guest=(case/'guest_maincpu.bin').read_bytes()
    payload=(ROOT/checked.prior.current.current.CANDIDATE/'roms/mk2ks/mk2ks.mdata').read_bytes()
    field='MK2_CPU_PAIR_FIELD';cache='MK2_NAT_CAMPAIGN_FLOOR_CACHE_PART'
    specs=[
        ('own_position',field,2714,'xraw','021A0000',None,'Both exact horizontal fixed-point integrations'),
        ('victim_position',field,2716,'vxraw','01E60000',None,'Both exact horizontal fixed-point integrations'),
        ('own_repel_speed',field,2715,'vx','00020000',None,'Every source-derived original release velocity publication'),
        ('victim_repel_speed',field,2717,'vvx','FFFC0000',None,'Every source-derived original release velocity publication'),
        ('shared_own_speed',field,2718,'vx','FFFF0000',None,'Every source-derived original release velocity publication'),
        ('shared_victim_speed',field,2718,'vvx','FFFC0000',None,'Every source-derived original release velocity publication'),
        ('early_suppression_clear',field,2714,'suppression','0',None,'Exact three-tick original release suppression decay'),
        ('late_suppression_clear',field,2715,'suppression','1',None,'Exact three-tick original release suppression decay'),
        ('cache_height',cache,2716,'height','1',2,'Every actual release cache part equals complete ROM composite'),
        ('cache_y_offset',cache,2717,'dy','-11',1,'Every actual release cache part equals complete ROM composite'),
        ('cache_source',cache,2716,'source','10935C95',2,'Every actual release cache part equals complete ROM composite'),
        ('grounded_victim_speed',field,2745,'vvx','FFFC0000',None,'Original victim requested velocity then separate grounded zero'),
        ('late_victim_position',field,2760,'vxraw','016A0000',None,'Every released victim horizontal integration through its ready'),
    ]
    rejected=[]
    def reject(label,altered_log,altered_guest,reason):
        try:checked.verify(altered_log,altered_guest,payload,typed)
        except ValueError as error:
            need(reason in str(error),'Only the specifically intended release invariant may reject '+label+': '+str(error))
            rejected.append(dict(label=label,reason=str(error)))
        else:raise ValueError('Actual corruption accepted: '+label)
    for label,tag,frame,key,value,slot,reason in specs:
        reject(label,replace_field(log,tag,frame,key,value,slot),guest,reason)
    missing='\n'.join(line for line in log.splitlines()if not(line.startswith(cache+' ')and
              'frame=2716 'in line and 'slot=2 'in line))+'\n'
    reject('missing_cache_publication',missing,guest,'Every released field has actual previous-tick native cache publication')
    for label,offset,reason in (
        ('original_body_opcode',(0xff827c40-0xff800000)//8,'Original complete body-push/bounds/request/facing code unchanged'),
        ('suppression_literal',0xf3b82,'Original three-tick Bicycle suppression refresh')):
        changed=bytearray(guest);changed[offset]^=1
        reject(label,log,bytes(changed),reason)
    # Pure branch boundaries are not relabelled as runtime fixtures. These
    # vectors include both physical orders, signed half-speed, exactly61/64,
    # opposing desired requests and equality at the vertical48px boundary.
    overlap=((0,100),(0,100));apart=((0,47),(0,47));vectors=[]
    for x1,x2,req1,req2,supp,old1,old2,expected in (
        (0,60,0,0,0,0,0,(-196608,196608,'repel')),
        (60,0,0,0,0,0,0,(196608,-196608,'repel')),
        (0,60,4,-2,1,-65536,-65536,(-65536,-65536,'suppressed')),
        (0,61,-262144,-65536,0,0,0,(-32768,-32768,'shared_p2')),
        (0,63,3,0,0,0,0,(1,1,'shared_p1')),
        (63,0,-3,0,0,0,0,(-2,-2,'shared_p1')),
        (0,63,0,-3,0,0,0,(-2,-2,'shared_p2')),
        (0,63,4,-4,0,0,0,(0,0,'opposed')),
        (0,64,4,-4,0,0,0,(4,-4,'requested')),
        (0,63,4,-4,1,0,0,(4,-4,'requested')),
    ):
        actual=checked.push(x1,x2,*overlap,req1,req2,supp,old1,old2)
        need(actual==expected,'Independent original body-push boundary vector')
        vectors.append(dict(x1=x1,x2=x2,requests=[req1,req2],suppression=supp,result=actual))
    need(checked.push(0,48,*apart,4,-4,0,0,0)==(4,-4,'requested'),'Strict original 48px vertical overlap threshold')
    need(checked.push(0,48,(0,48),(0,48),4,-4,0,0,0)==(-196608,196608,'repel'),'Inclusive original 48px equality')
    # Same exact verification path after all in-memory negatives, unchanged data.
    need(checked.verify(log,guest,payload,typed)['records']==positive['records'],'Same-path original release positive control')
    pins=positive['inputHashes'];pins[str(checked.OUT/'report.json')]=checked.prior.current.assembly.sha(checked.OUT/'report.json')
    pins[str(Path(__file__).resolve())]=checked.prior.current.assembly.sha(__file__)
    return dict(passed=True,actualCounterexamplesRejected=len(rejected),specificFailures=rejected,
                independentBranchBoundaryVectors=len(vectors)+2,branchVectors=vectors,
                samePathPositiveControlsAccepted=True,unrelatedMissingEventExceptionsNeverAccepted=True,
                sourceCaptureAndGameUnchanged=True,inputHashes=pins,fullPortAcceptance=False)

if __name__=='__main__':
    need(not OUT.exists(),'Never overwrite counterexample evidence')
    try:result=run()
    except Exception as error:result=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()if k not in ('inputHashes','specificFailures','branchVectors')},indent=2),flush=True)
    raise SystemExit(0 if result['passed']else 1)
