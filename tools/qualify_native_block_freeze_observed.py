"""Finite true-identity Freeze/guard/release comparison, not full-port QA."""
import copy,gzip,hashlib,json,re,struct
from pathlib import Path
import native_ai_response_full_context as native
ROOT,need,sha=native.ROOT,native.need,native.sha
IDENTITIES={'kano':17,'sonya':18,'liu_kang':1}

def rows(text):
    found={}
    for line in text.splitlines():
        if line.startswith(('MK2_NORMAL_FREEZE_','MK2_STOCK_HEAD_V921_')):
            found.setdefault(line.split()[0],[]).append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    return found

def check(data,fighter,side,policy,guest):
    f=data['MK2_NORMAL_FREEZE_FIELD'];identity=IDENTITIES[fighter]
    need(len(f)==701 and [int(r['age']) for r in f]==list(range(701)),'701 contiguous native live fields')
    first=data['MK2_STOCK_HEAD_V921_FIRST_LIVE'];need(len(first)==1,'One original human match admission')
    start=int(first[0]['frame']);base=f[0]
    for age,r in enumerate(f):
        need(int(r['frame'])==start+age and r['writes']=='0' and r['assistance']=='none' and
             r['mode']=='2' and r['finish']=='0','Unassisted ordinary live chronology')
        need(int(r['victim_id'])==int(r['roster'])==identity and r['state']=='1' and
             r['victim_actor']==r['victim_owner']==base['victim_actor'] and r['victim_main']==base['victim_main'] and
             r['own_id']=='8' and r['own_actor']==r['own_owner']==base['own_actor'] and r['own_main']==base['own_main'],
             'Actual independent stable native human actor/main/roster ownership')
        need(r['hp']==r['own_hp']=='161','Normal-health native Freeze/guard preserves full health')
        need(r['y']==r['floor']==base['floor'],'Actual native ground remains unchanged')
    for tag,address,opcode in [('ICE_REQUEST',0xff86f9d0,0x09c0),('PROJECTILE_SETUP',0xff8a5900,0x24a0)]:
        actual=data.get('MK2_NORMAL_FREEZE_'+tag,[]);need(len(actual)==1,'One real native Freeze request/setup')
        r=actual[0]
        need(int(r['entry'],16)==address and int(r['pc'],16)==address+16 and int(r['value'],16)==opcode and
             r['mask']=='FFFF' and r['age']=='108' and r['id']=='8' and r['actor']==r['owner']==base['own_actor'] and
             r['main']==base['own_main'],'Original native ice instruction/PC/actor owner')
        need(struct.unpack_from('<H',guest,(address-0xff800000)//8)[0]==opcode,'Actual compiled source-bound ice opcode')
    need(data['MK2_NORMAL_FREEZE_PROJECTILE_SETUP'][0]['a0']=='0000000D','Native human projectile13 actually created')
    cold=[int(r['age']) for r in f if r['action']=='0401']
    if policy=='none':
        need(len(cold)==160 and cold==list(range(cold[0],cold[0]+160)) and 120<=cold[0]<=160,'Native unblocked 160-field freeze')
        need(all(f[a]['bank']=='0505' and int(f[a]['flags'],16)&16 for a in cold),'Native frozen palette and body flag')
        need(all(r['bank']==base['bank'] for r in f[cold[-1]+1:]),'Natural thaw restores original palette')
        block_start=None
    else:
        block_start=70 if policy=='held' else 109
        need(not cold and all(r['bank']==base['bank'] for r in f),'Blocked projectile never freezes or corrupts palette')
        guard=[int(r['age']) for r in f if r['action']=='0700']
        need(guard==list(range(block_start+1,301)),'Native guard follows ordinary Block and releases normally')
    forward='Left' if side==1 else 'Right';toward='Right' if side==1 else 'Left'
    inputs=[(int(r['frame'])-start,int(r['slot']),r['button']) for r in data['MK2_STOCK_HEAD_V921_INPUT'] if int(r['frame'])>=start]
    expected=[]
    for age in range(701):
        if block_start is not None and block_start<=age<300:expected.append((age,side,'Block'))
        if 90<=age<93:expected.append((age,3-side,'Down'))
        if 98<=age<101:expected.append((age,3-side,forward))
        if 106<=age<109:expected.append((age,3-side,'Low_Punch'))
        if 450<=age<466:expected.append((age,side,toward))
        if 510<=age<513:expected.append((age,side,'High_Punch'))
    need(inputs==expected,'Every physical live input accounted, no hidden assistance')
    need(all(r['action']=='0000' for r in f[451:467]) and (int(f[467]['x'])-int(f[450]['x']))*(1 if side==1 else -1)>20,
         'Physical movement after guard release/thaw')
    need(all(r['action']=='0101' for r in f[512:530]) and f[530]['action']!='0101','Physical punch naturally completes')
    ends=data.get('MK2_NORMAL_FREEZE_END',[])
    need(len(ends)==1 and ends[0]['age']=='700','Actual native controller reaches its normal terminal field')
    need(all(r['before']==r['after'] for r in data.get('MK2_STOCK_HEAD_V921_HEALTH',[])),'No hidden health damage/refill assistance')
    return dict(fighter=fighter,physicalSlot=side,policy=policy,identity=identity,fieldCount=701,
                frozenFields=len(cold),guardFields=0 if block_start is None else 300-block_start,
                actualProjectile=13,ordinaryControlsAfterRelease=True)

def qualify(captures):
    out=ROOT/'audit_native_block_freeze_observed_checked'
    need(not out.exists(),'Fresh immutable guard comparison')
    checks=[];faults=[];pins={str(Path(__file__).resolve()):sha(__file__)}
    for key,c in captures.items():
        fighter,slot,policy=key.rsplit('_',2);side=int(slot[1:])
        folder=ROOT/f'audit_native_block_freeze_observed_{policy}_{fighter}_p{side}'
        meta=c['meta'];terminal=json.loads((folder/'native_terminal.json').read_text())
        need(meta['nativeExit']==terminal['nativeExit']==0 and meta['executableSHA256']==native.EXE_SHA and
             hashlib.sha256(c['guest']).hexdigest().upper()==meta['guestSHA256']==native.GUEST_SHA,'Actual current compiled native terminal identity')
        need(all(sha(p)==h for p,h in meta['inputHashes'].items()),'Every originally executed input remains frozen')
        need(len(c['images'])==len(meta['actualScenes'])==4,'Four real native image stages remain in same RAM host')
        data=rows(c['text']);check_result=check(data,fighter,side,policy,c['guest'])
        mutations=[('victim_id','0'),('roster','0'),('state','0'),('victim_owner','00000000'),('victim_main','00000000'),
                   ('own_id','17'),('mode','6'),('finish','1'),('writes','1'),('assistance','forced'),('hp','160'),
                   ('own_hp','160'),('y','-999'),('age','999')]
        for field,value in mutations:
            bad=copy.deepcopy(data);bad['MK2_NORMAL_FREEZE_FIELD'][140][field]=value
            try:check(bad,fighter,side,policy,c['guest'])
            except (AssertionError,RuntimeError,ValueError) as e:faults.append(dict(case=key,field=field,rejected=str(e)))
            else:raise AssertionError('Actual field corruption accepted: '+field)
        for tag,field,value in [('ICE_REQUEST','value','0000'),('PROJECTILE_SETUP','a0','0000000C'),('PROJECTILE_SETUP','owner','00000000')]:
            bad=copy.deepcopy(data);bad['MK2_NORMAL_FREEZE_'+tag][0][field]=value
            try:check(bad,fighter,side,policy,c['guest'])
            except (AssertionError,RuntimeError,ValueError) as e:faults.append(dict(case=key,field=tag+'.'+field,rejected=str(e)))
            else:raise AssertionError('Actual native launch corruption accepted')
        bad=copy.deepcopy(data);bad['MK2_STOCK_HEAD_V921_INPUT'].pop()
        try:check(bad,fighter,side,policy,c['guest'])
        except (AssertionError,RuntimeError,ValueError) as e:faults.append(dict(case=key,field='physical_input',rejected=str(e)))
        else:raise AssertionError('Dropped physical input accepted')
        check_result['ramRGBHashes']=[hashlib.sha256(i.tobytes()).hexdigest().upper() for i in c['images']]
        checks.append(check_result)
        pins.update(meta['inputHashes'])
        for p in folder.iterdir():
            if p.is_file():pins[str(p)]=sha(p)
    need(len(checks)==6 and len(faults)==108,'Complete declared six-case guard/recovery comparison and effective faults')
    out.mkdir()
    report=dict(passed=True,finiteFreezeBlockRecoveryAccepted=True,cases=checks,effectiveFaults=faults,inputHashes=pins,
                nativeGames=6,nativeFields=4206,visualReviewAccepted=False,fullAudioAcceptance=False,
                continuousShadowRenderAcceptance=False,fullPortAcceptance=False,goalStatus='active',
                newBuilds=0,newROMCopies=0,newZIPs=0,
                limitation='Dead Pool two-human P2 cases only; no CPU, other arenas, continuous RGB/audio, finisher or full-port claim.')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return dict(passed=True,cases=len(checks),nativeFields=4206,effectiveFaults=len(faults))
