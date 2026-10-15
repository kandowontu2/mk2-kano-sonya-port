"""Actual owned Knife children: native branch/extraction/scaler/HP/retirement."""
import copy,json,re,struct,subprocess
from collections import Counter
from pathlib import Path
import verify_current_campaign_shao_knife_observer_v3526 as native
import verify_current_knife_boss_source_v3517 as source
ROOT=native.ROOT;need=native.need;sha=native.sha
CASE=ROOT/'audit_v3516_current_kano_natural_knife_retreat_campaign'
PROOF=ROOT/'audit_v3521_current_kano_knife_campaign_checked/report.json'
OUT=ROOT/'audit_v3530_current_owned_knife_boss_checked'
HEX=set('entry at pc owner parent actor main birth_parent action descriptor pose xraw yraw vx vy flags body mask victim_main victim_actor victim_flags'.split())|{f'a{i}'for i in range(15)}
TEXT=set('kind roster states actors mains health assistance scope'.split())
EVENTS={'entry':{0xffffb000},'release':{0xfffc3800},'create':{0xfffc5800},'child':{0xfffc6000},
 'frontgate':{0xff8b6ac0},'strike':{0xff835410},'guard':{0xff837d40},'tested_guard':{0xff837d90},
 'unblocked':{0xff837ae0},'blocked':{0xff837b90,0xff837bd0},'physical_block':{0xff832040},
 'normal_damage_extract':{0xff835d20},'blocked_damage_extract':{0xff836040},'shao_scaler':{0xff8369f0},
 'travel':{0xff8afe80},'impact':{0xff8affb0},'group':{0xff838790},'retire':{0xff8b6820},
 'ready':{0xff861350},'regain':{0xff861500}}
def parse(log):
    result=[]
    for index,line in enumerate(log.splitlines()):
        if not line.startswith('MK2_BOSS_KNIFE_'):continue
        tag=line.split()[0].removeprefix('MK2_BOSS_KNIFE_');pairs=re.findall(r'(\w+)=([^\s]+)',line)
        need(len(pairs)==len(dict(pairs)),'Unique actual observer fields')
        r={k:v if k in TEXT else int(v,16 if k in HEX else 10)for k,v in pairs}
        r.update(tag=tag,event=index);result.append(r)
    return result
def health_key(r):return tuple(r[k]for k in('frame','slot','at','before','after','pc','a8','a13'))
def contract(rows,base,descriptors):
    live={};entries={};births=[];dead=[];hits=[];fields=0;branches=Counter();retire_modes=Counter()
    base_health=Counter(health_key(r)for r in base if r['tag']=='HEALTH')
    for r in rows:
        need(r['writes']==0 and r['assistance']=='none' and r['human_slot']==1,'Read-only actual physical-slot scope')
        tag=r['tag']
        if tag=='RESULT':continue
        if tag=='CHILD_FIELD':
            c=live.get(r['actor'])
            need(c is not None and c['main']==r['main'],'Actual child field only during observed native allocation lifetime')
            need(r['child_serial']==c['serial'] and r['owner']==r['actor'] and r['id']==17
               and r['parent']==r['birth_parent']==c['parent'],'Actual child field retains independent own17 process/parent')
            fields+=1;continue
        if tag=='EVENT':
            need(r['entry']in EVENTS.get(r['kind'],set()) and r['pc']==r['entry']+16,'Actual original native event instruction')
            if r['kind']=='entry':
                a,b=map(lambda x:int(x,16),r['actors'].split(','));m,n=map(lambda x:int(x,16),r['mains'].split(','))
                need(r['serial']not in entries and r['id']==17 and r['a8']==r['owner']==a and r['a13']==m
                   and r['mode']==2 and r['stage']==16 and r['roster']=='17,13' and r['states']=='1,0',
                   'Actual own17 parent entry, never a child or proxy')
                entries[r['serial']]=dict(frame=r['frame'],parent=a,parent_main=m,victim=b,victim_main=n)
        if tag=='BIRTH':
            e=entries.get(r['serial'])
            need(e is not None and r['a8']not in live and r['reused_unretired']==0,'Native child allocation has actual own entry and no unretired reuse')
            need(r['entry']==0xfffc6000 and r['pc']==0xfffc6010 and r['owner']==r['a8'] and r['id']==17
               and r['parent']==e['parent'] and r['victim_actor']==e['victim'] and r['victim_main']==e['victim_main']
               and r['victim_id']==13,'Actual child birth has true17 parent and actual13 victim linkage')
            need(len({r['a8'],r['a13'],e['parent'],e['parent_main'],e['victim'],e['victim_main']})==6,'Independent physical parent/child/victim objects and processes')
            c=dict(e,actor=r['a8'],main=r['a13'],serial=r['serial'],birth=r['frame'],branch=None,extract=None,scale=None)
            live[r['a8']]=c;births.append(c);continue
        c=live.get(r.get('a8'))
        if c is None or c['main']!=r.get('a13'):
            if tag=='HEALTH':need(base_health[health_key(r)]>0,'Every independently observed native health store matches full campaign')
            continue
        need(r['owner']==r['a8'] and r['id']==17 and r['parent']==c['parent'],
             'Every live native child event retains actual allocated owner/parent identity')
        if tag=='EVENT':
            need(r['child_serial']==c['serial'],'Actual event belongs to exact allocated child serial')
            kind=r['kind']
            if kind in('blocked','unblocked'):c['branch']=r
            elif kind in('normal_damage_extract','blocked_damage_extract'):
                branch=c['branch'];need(branch is not None and branch['frame']==r['frame']
                   and (kind=='blocked_damage_extract')==(branch['kind']=='blocked'),
                   'Actual blocked/normal extraction follows observed native branch, not input guard intent')
                need(r['descriptor']in descriptors,'Actual dedicated Knife descriptor selected')
                c['extract']=r
            elif kind=='shao_scaler':
                extract=c['extract'];need(extract is not None and extract['frame']==r['frame'],'Actual scaler follows same-field native damage extraction')
                words=descriptors[extract['descriptor']]
                raw=words[5]&255 if extract['kind']=='blocked_damage_extract' else words[5]>>8
                need(r['a10']==raw and r['a3']==13 and r['victim_id']==13
                   and r['victim_actor']==c['victim'] and r['victim_main']==c['victim_main'],
                   'Actual original Shao callback receives exact selected raw native damage and victim13')
                c['scale']=dict(frame=r['frame'],raw=raw,scaled=(raw>>1)+(raw>>2),blocked=extract['kind']=='blocked_damage_extract')
        elif tag=='HEALTH':
            need(base_health[health_key(r)]>0,'Every independently observed native health store matches full campaign')
            if r['slot']==2 and r['before']>r['after']:
                scale=c['scale'];need(scale is not None and scale['frame']==r['frame'],'Actual owned child hit follows source-bound same-field scaler')
                need(r['pc']==0xff836700 and r['at']==0x01060ec0 and r['mask']==65535
                   and r['a10']==scale['scaled'] and r['before']-r['after']==min(r['before'],scale['scaled']),
                   'Actual original child health store uses scaled damage and original zero clamp')
                hits.append(dict(frame=r['frame'],serial=c['serial'],raw=scale['raw'],scaled=scale['scaled'],
                   damage=r['before']-r['after'],blocked=scale['blocked'],key=health_key(r)))
                branches['blocked'if scale['blocked']else'normal']+=1
                c['scale']=None
        elif tag=='RETIRE':
            need(r['pc']==0xff8b6830 and r['child_serial']==c['serial'] and r['birth_parent']==c['parent'],
               'Exact allocated child retires through original native routine')
            dead.append(dict(serial=c['serial'],frame=r['frame']));retire_modes[r['mode']]+=1;del live[r['a8']]
    result=[r for r in rows if r['tag']=='RESULT']
    need(len(result)==1 and result[0]['tracked_unretired_children']==len(live)==0,'No unretired child at native terminal')
    need(len(entries)==len(births)==len(dead)==30 and {c['serial']for c in births}==set(entries),
         'All actual parent entries own one separately allocated and natively retired child')
    boss_frames={r['frame']for r in base if r['tag']=='BOSS_FIELD'and r['stage']==16}
    actual=[r for r in base if r['tag']=='HEALTH' and r['frame']in boss_frames and r['slot']==2 and r['pc']==0xff836700 and r['before']>r['after']]
    need(Counter(health_key(r)for r in actual)==Counter(r['key']for r in hits),'Every original opponent boss collision attributed to exact child, not temporal proximity')
    need(len(hits)==30 and sum(r['damage']for r in hits)==426 and branches==Counter(normal=28,blocked=2),
         'Actual30owned hits:28normal including2clamped KOs and2native blocked chips')
    return dict(actualOwnParentEntries=len(entries),actualNativeChildBirths=len(births),actualNativeChildRetirements=len(dead),
       actualNativeChildFields=fields,actualOwnedChildCollisionStores=len(hits),actualOwnedChildDamage=sum(r['damage']for r in hits),
       actualNativeBranchCounts=dict(branches),actualDamageHistogram=dict(Counter(r['damage']for r in hits)),
       actualNativeRetirementModes=dict(retire_modes),allObservedBossCollisionStoresAttributed=True,
       actualOwnedClampedKOFrames=[r['frame']for r in hits if r['damage']<r['scaled']],
       blockNeverAssumedFromIntentOrVictimFlags=True,fullPhasePixelsGroundShadowAudioOrAllContextsAccepted=False)
def main():
    need(not OUT.exists(),'Immutable actual owned-contact evidence')
    proof=json.loads(PROOF.read_text());need(proof['passed'] and proof['unassisted_clear_proven'],'Actual whole native campaign accepted first')
    logpath=CASE/'run.log';need(proof['inputHashes'][str(logpath)]==sha(logpath),'Exact already accepted terminal log')
    native.source_boundary()
    guest=(CASE/'guest_maincpu.bin').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();donor=(ROOT/'mk3/mk3-maincpu.bin').read_bytes()
    model=source.model(guest,original,donor)
    for lo,hi in((0xff837900,0xff837dd0),(0xff8b6820,0xff8b68e0)):
        need(source.data(guest,lo,hi)==source.data(original,lo,hi),'Whole original native guard and child retirement routines unchanged')
    descriptors={r['address']:r['words']for r in model['actualKnifeDescriptors']}
    log=logpath.read_text(encoding='utf-8-sig');rows=parse(log);base=native.old.parse(log,1,'kano')
    positive=contract(rows,base,descriptors);faults=[]
    variants=[]
    changed=copy.deepcopy(rows);next(r for r in changed if r['tag']=='BIRTH')['parent']+=0x210
    variants.append(('wrong_actual_child_parent',changed,'Actual child birth has true17 parent'))
    changed=copy.deepcopy(rows);next(r for r in changed if r['tag']=='HEALTH' and r['slot']==2)['a10']+=1
    variants.append(('wrong_actual_scaled_damage',changed,'Actual original child health store uses scaled damage'))
    changed=copy.deepcopy(rows);next(r for r in changed if r['tag']=='EVENT'and r['kind']=='blocked_damage_extract')['kind']='normal_damage_extract'
    variants.append(('wrong_actual_native_branch',changed,'Actual original native event instruction'))
    changed=copy.deepcopy(rows);i=next(i for i,r in enumerate(changed)if r['tag']=='RETIRE')
    orphan=copy.deepcopy(next(r for r in rows if r['tag']=='CHILD_FIELD' and r['child_serial']==changed[i]['child_serial']))
    orphan['frame']=changed[i]['frame']+1;changed.insert(i+1,orphan)
    variants.append(('orphan_field_after_actual_retirement',changed,'Actual child field only during observed native allocation lifetime'))
    for name,changed,message in variants:
        need(changed!=rows,'Non-vacuous actual source-bound runtime fault')
        try:contract(changed,base,descriptors)
        except ValueError as error:
            need(message in str(error),'Specific intended actual native ownership/branch/scaler/lifetime invariant');faults.append(name)
        else:raise ValueError('Corrupted actual child-contact trace accepted')
    need(contract(rows,base,descriptors)==positive,'Same-path original native-contact positive')
    pins=dict(proof['inputHashes'])
    for p in(PROOF,Path(__file__),Path(source.__file__),ROOT/'audit_v3518_current_knife_boss_source_checked/report.json'):
        pins[str(p.resolve())]=sha(p)
    for file,digest in pins.items():need(sha(file)==digest,'Actual accepted source/capture/gameplay bytes unchanged')
    value=dict(passed=True,actualNativeContact=positive,actualQualifiedRuntimeFaults=faults,
       samePathOriginalNativeContactPositiveAccepted=True,actualCaptureOrGameChanged=False,
       fullPortAcceptance=False,inputHashes=pins)
    OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(value,indent=2)+'\n');digest=sha(p)
    result=subprocess.run(['compact.exe','/C','/I','/Q',str(p)],capture_output=True,text=True)
    need(result.returncode==0 and sha(p)==digest,'Lossless compact contact proof')
    print(json.dumps({k:v for k,v in value.items()if k!='inputHashes'},indent=2),flush=True)
if __name__=='__main__':main()
