"""Cold real-input ordinary throws: true IDs, headed victims, damage and recovery."""
import json,re,struct
from pathlib import Path
import verify_native_ground_throw_source_v1598 as source
import verify_active_launch_cpu_display_v1525 as native
ROOT=source.ROOT
OUT=ROOT/'audit_v1606_native_ground_throw_humans_checked'
HEX={'actor','main','owner','pose','vx','vy','gravity','flags','body','trail','bank','entry','expectedEntry','pc','a8','a13','a9','at','mask'}
def rows(log,tag):
    result=[]
    for line in log.splitlines():
        if not line.startswith('MK2_HSPECIAL_'+tag+' '):continue
        r=dict(re.findall(r'(\w+)=(\S+)',line))
        for k,v in tuple(r.items()):
            if k in HEX and not(tag=='RESULT' and k=='entry'):r[k]=int(v,16)
            elif re.fullmatch(r'-?\d+',v):r[k]=int(v)
        result.append(r)
    return result
def need(ok,label):
    if not ok:raise ValueError(label)
def clean(r):
    return r['y']==r['floor'] and r['vx']==r['vy']==r['gravity']==r['trail']==0 and not(r['flags']&0x1c) and not(r['body']&0x0c) and r['action']==0x303
def pose_sources(pose,payload,guest):
    # Source identity is invariant under facing; do not invent missing cache/flip observations.
    def read(address,fmt):
        raw,base=(payload,0xfe800000)if 0xfe800000<=address<0xff800000 else(guest,0xff800000)
        at=(address-base)//8
        need(address>=base and (address-base)%8==0 and 0<=at<=len(raw)-struct.calcsize(fmt),'Complete aligned actual ROM descriptor')
        return struct.unpack_from(fmt,raw,at)
    result=[]
    for part in range(12):
        ptr=read(pose+part*32,'<I')[0]
        if ptr==0:
            need(bool(result),'Nonempty complete actual pose');return result
        width,height,sourcebits=read(ptr,'<HH4xI')
        need(width>0 and height>0,'Actual ROM pose dimensions')
        result.append(dict(source=sourcebits))
    raise ValueError('Unterminated actual ROM pose')
def verify_log(log,fighter,side,victim,payload,guest):
    need(not re.search('LUA ERROR|fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),'No runtime error')
    need(not rows(log,'FAILED'),'No failed runtime lifecycle')
    finals=rows(log,'RESULT');need(len(finals)==1,'One terminal result');final=finals[0]
    need(final['command']>0 and final['entry']>final['command'] and final['entry']<final['recovered']<final['followup']<final['frame'],'Genuine activation and bounded recovery')
    ids={'kano':17,'sonya':18,'sub_zero':8};ownid=ids[fighter];victimid=ids[victim]
    fields=rows(log,'FIELD');need(fields,'Actual physical actor callbacks')
    by={(r['frame'],r['slot']):r for r in fields}
    need(len(by)==len(fields)==2*(final['frame']-final['ready']+1),'Every pair callback retained exactly once')
    first=[by[final['ready'],n]for n in(1,2)]
    expected=[ownid,victimid]if side==1 else[victimid,ownid]
    for (frame,n),r in by.items():
        need(r['id']==r['roster']==expected[n-1] and r['mode']==2 and r['state']==1 and r['owner']==r['actor']==first[n-1]['actor'] and r['main']==first[n-1]['main'],'Stable true native identity/ownership in every field')
        need(r['writes']==0 and r['assistance']=='none','Input-only observed state')
    entries=[r for r in rows(log,'EVENT')if r['entry']==0xff8b6bb0]
    need(len(entries)==1 and entries[0]['frame']==final['entry'] and entries[0]['id']==ownid and entries[0]['a8']==first[side-1]['actor'] and entries[0]['a13']==first[side-1]['main'],'Actual own normal-throw entry')
    requests=[r for r in rows(log,'LOOKUP')if r['at']==0xff842d90 and r['frame']==final['entry']]
    need(len(requests)==1 and requests[0]['a9']==43 and requests[0]['own']==ownid and requests[0]['victim']==victimid,'Dedicated native semantic living-victim index')
    selections=[r for r in rows(log,'LOOKUP')if r['at']==0xff906110 and r['frame']==final['entry'] and r['a8']==first[2-side]['actor']]
    need(len(selections)==1 and selections[0]['a9']==43 and selections[0]['a13']==first[2-side]['main'],'Animation looked up through real victim root/Main, not proxy')
    parts=0;poses=set()
    for r in fields:
        if not final['entry']<=r['frame']<=final['recovered']:continue
        group=pose_sources(r['pose'],payload,guest);need(group,'Source-bound complete native pose')
        need(all(not(0x1ec0000*8<=q['source']<0x1ee0000*8)for q in group),'No death-art source in ordinary living throw')
        parts+=len(group)
        if r['slot']==3-side:poses.add(r['pose'])
    damage=[r for r in rows(log,'HEALTH')if r['after']<r['before'] and final['command']<=r['frame']<=final['recovered']]
    need(len(damage)==1 and damage[0]['slot']==3-side and damage[0]['before']==161 and damage[0]['after']==129 and damage[0]['pc']==0xff836700,'Exactly normal 32-point original native throw damage')
    need(all(clean(by[final['recovered'],n])for n in(1,2)),'Both native actors fully recover')
    need(all(by[final['recovered'],n]['hp']==(161 if n==side else 129)for n in(1,2)),'Health unchanged except real throw contact')
    follow=[by[f,side]for f in range(final['followup'],final['frame']+1)]
    need(len(follow)==161 and any(r['x']!=follow[0]['x']for r in follow) and any(r['y']<r['floor']for r in follow) and any(r['action']==0x101 for r in follow) and clean(follow[-1]),'Ordinary walking, jumping and punch follow-up returns to clean readiness')
    return dict(fighter=fighter,side=side,victim=victim,entry=final['entry'],recovered=final['recovered'],nativeDamage=32,semanticVictimIndex=43,observedROMParts=parts,victimPoses=[hex(x)for x in sorted(poses)],trueIDsEveryCallback=True,headedOrdinaryThrow=True,ordinaryFollowupFields=len(follow),fullPortAcceptance=False)
def verify():
    guest,_,payload=source.expected();pins={}
    def pin(p,h=None):
        p=Path(p);v=source.prior.sha(p);need(h is None or h==v,'Changed immutable input '+str(p));pins[str(p.resolve())]=v
    proofpath=source.OUT/'report.json';proof=json.loads(proofpath.read_text());need(proof['passed'],'Exact source-built guest proof');pin(proofpath)
    for p,h in proof['inputHashes'].items():pin(p,h)
    build=json.loads((ROOT/source.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    cases=[];negatives=[]
    for fighter in('kano','sonya'):
        for side in(1,2):
            victim='sonya'if fighter=='kano'else'kano'
            folder=ROOT/f'audit_v1602_{fighter}_ground_throw_p{side}'
            meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
            need(meta['exit_code']==0 and meta['candidate']==source.NAME and meta['fighter']==fighter and meta['side']==side and meta['victim']==victim and meta['assistance']=='none','Actual declared cold case')
            need(meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'],'Exact current candidate')
            before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            need(before==meta['input_hashes'] and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Complete immutable execution manifest')
            for p,h in before.items():
                pin(p,h)
                if Path(p).suffix in('.ps1','.lua','.json'):pin(folder/'input_sources'/Path(p).name,h)
            script=(folder/'input_sources/mk2ks_human_ground_throw_v1601.lua').read_text()
            need(not re.search(r':write_|write_u\d+|load_?state|\.value\s*=(?!=)|dofile\(',script),'No guest/CPU assignments or save states')
            need((folder/'guest_maincpu.bin').read_bytes()==guest,'Entire observed guest matches exact two-patch source model')
            log=(folder/'run.log').read_text(encoding='utf-8-sig')
            case=verify_log(log,fighter,side,victim,payload,guest);cases.append(case)
            for p in folder.rglob('*'):
                if p.is_file():pin(p)
            if fighter=='sonya' and side==1:
                request=next(line for line in log.splitlines()if line.startswith('MK2_HSPECIAL_LOOKUP ')and 'at=FF842D90' in line)
                mutations={'wrong_victim_index':log.replace(request,request.replace('a9=0000002B','a9=0000003C'),1),
                           'missing_real_damage':re.sub(r'^MK2_HSPECIAL_HEALTH[^\n]*\n','',log,flags=re.M),
                           'wrong_damage_writer':log.replace('pc=FF836700','pc=FF000000'),
                           'missing_entry':re.sub(r'^MK2_HSPECIAL_EVENT[^\n]*entry=FF8B6BB0[^\n]*\n','',log,flags=re.M),
                           'wrong_actual_victim_id':log.replace('id=17 roster=17','id=1 roster=17',1),
                           'no_recovery':re.sub(r'(MK2_HSPECIAL_RESULT[^\n]*?)recovered=\d+',r'\1recovered=-1',log)}
                for label,bad in mutations.items():
                    need(bad!=log,'Real negative mutation')
                    try:verify_log(bad,fighter,side,victim,payload,guest)
                    except (ValueError,AssertionError,KeyError):negatives.append(label)
                    else:raise ValueError('Accepted corrupt actual lifecycle '+label)
    pin(__file__);pin(native.__file__)
    return dict(passed=True,candidate=source.NAME,bothAddedAttackersBothPhysicalSlots=True,cases=cases,rejectedInMemoryCorruptions=negatives,inputHashes=pins,noCapturedEvidenceChanged=True,fullPortAcceptance=False,scope='Bounded normal human throw state/ROM pose proof; not full cached raster, every victim, CPU, cinematic or release acceptance')
if __name__=='__main__':
    assert not OUT.exists(),'Never overwrite evidence'
    try:report=verify()
    except Exception as e:report=dict(passed=False,error=repr(e),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2))
    raise SystemExit(0 if report['passed']else 1)
