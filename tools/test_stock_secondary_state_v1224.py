"""In-memory rejection checks. Never change runtime evidence or game state."""
import json,re
import verify_stock_scorpion_secondary_v1222 as proof
ROOT=proof.ROOT;OUT=ROOT/'audit_v1224_stock_secondary_state_corruption_checks';assert not OUT.exists()
reconstructed=proof.headed.reconstruct()
texts={key:(ROOT/f'audit_v1220_secondary_{key}/run.log').read_text(encoding='utf-8-sig') for key in proof.CASES}
baseline=proof.verify(texts,reconstructed);assert baseline['passed'],baseline['errors']
key='sonya_p2';text=texts[key];checks=[dict(name='unchanged actual baseline',accepted=True)]
def replace_line(predicate,old,new):
 lines=text.splitlines(keepends=True);found=[i for i,line in enumerate(lines) if predicate(line)]
 assert len(found)==1,(old,found)
 i=found[0];assert old in lines[i];lines[i]=lines[i].replace(old,new,1)
 return ''.join(lines)
def rejection(name,changed=None,guest=None):
 altered=dict(texts)
 if changed is not None:altered[key]=changed
 report=proof.verify(altered,guest if guest is not None else reconstructed,check_files=False)
 assert not report['passed'] and report['errors'],'Invalid evidence accepted: '+name
 checks.append(dict(name=name,rejected=True,errors=report['errors']))
 print('Rejected '+name,flush=True)
rejection('foreign victim callback ID',replace_line(lambda s:'FIRE_CALL ' in s and 'entry=FF8BC810 ' in s,'id=18 ','id=1 '))
ready=baseline['cases'][key]['actionFrame']-52
lines=text.splitlines(keepends=True)
removed=[s for s in lines if 'V921_INPUT ' in s and f'frame={ready+5} ' in s and 'button=High_Punch' in s]
assert len(removed)==1
rejection('missing physical HP hold field',text.replace(removed[0],'',1))
rejection('insufficient original hold timer',replace_line(lambda s:'FIRE_GATE ' in s and 'entry=FF8687D0 ' in s,'a1=0000002D ','a1=00000027 '))
rejection('wrong native distance limit',replace_line(lambda s:'V921_GATE ' in s,'limit=69 ','limit=160 '))
line=next(s for s in lines if 'V921_HEALTH ' in s and 'pc=FF836700' in s)
rejection('non-collision KO writer',text.replace(line,line.replace('pc=FF836700','pc=FF836710'),1))
rejection('proxy lower-stump lookup',replace_line(lambda s:'V921_LOOKUP ' in s and 'index=00000041 ' in s,'index=00000041 ','index=00000000 '))
rejection('wrong completion age',replace_line(lambda s:'V921_WRAP ' in s,'age=96 ','age=97 '))
rejection('recovering instead of dizzy victim',replace_line(lambda s:'V921_READY ' in s,'continuation=FFA17E10 ','continuation=FF83C3D0 '))
guest=bytearray(reconstructed[0]);guest[-1]^=1
rejection('changed whole guest ROM',guest=(bytes(guest),*reconstructed[1:]))
OUT.mkdir();(OUT/'report.json').write_text(json.dumps(dict(passed=True,checks=checks,
 inputHashes=baseline['inputHashes'],inMemoryOnly=True,actualRuntimeEvidenceChanged=False,
 fullPortAccepted=False),indent=2)+'\n')
print('Actual baseline and all nine negative checks passed',flush=True)
