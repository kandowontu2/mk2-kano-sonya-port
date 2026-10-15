"""Independent complete-field physical duck-pressure replay, not tower proof."""
import collections,hashlib,json,re,subprocess
from pathlib import Path
import verify_mirror_guard_zoning_prefix_v4194 as previous
import run_mileena_duck_pressure_campaign_v4243 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
FOLDER=ROOT/'audit_v4245_sonya_mileena_duck_pressure_p2_campaign'
OUT=ROOT/'audit_v4250_mileena_duck_pressure_actual_prefix_checked'
parse=previous.parse

def replay(text):
    rows=parse(text);decisions={r['frame']:r for r in rows if r['tag']=='DUCK_DECISION'}
    fields=[r for r in rows if r['tag']=='DUCK_FIELD']
    need(fields and len(fields)==len(decisions)==len({r['frame']for r in fields}),'Every actual duck field has exactly1decision')
    inputs=collections.defaultdict(list)
    for r in rows:
        if r['tag']=='INPUT':inputs[r['frame']].append(r['button'])
    live={r['frame']:r for r in rows if r['tag']=='LIVE'}
    last,down=None,None;reasons=collections.Counter();categories=collections.Counter()
    by={r['frame']:r for r in fields}
    for f in fields:
        frame=f['frame'];d=decisions[frame]
        need(f['human_slot']=='2'and f['fighter']=='sonya'and f['human_id']==f['human_roster']=='18'and f['cpu_id']==f['cpu_roster']=='5','Actual true SonyaP2 versus real native Mileena, never proxy/morph')
        need(f['writes']==d['writes']=='0'and f['assistance']==d['assistance']=='none','Read-only native field/physical decision')
        for who in('human','cpu'):
            need(0x01000000<=int(f[who+'_actor'],16)<0x01100000 and 0x01000000<=int(f[who+'_main'],16)<0x01100000 and f[who+'_owner']==f[who+'_actor'],'Actual true actor/Main ownership')
        need(all(0<int(h)<=161 for h in f['health'].split(',')),'Real positive combat health, no supplied victory')
        reset=last is None or frame-last!=1;need(int(f['reset'])==int(reset),'Independent contiguous-field reset')
        if reset:down=None
        last=frame;hx,cx=int(f['h_x']),int(f['c_x']);height=int(f['h_floor'])-int(f['h_y']);gap=abs(hx-cx)
        if height>8:reason,down,expected='air_recovery',None,['Down']
        elif gap>86:reason,down,expected='grounded_approach',None,['Right'if hx<cx else'Left']
        else:
            if down is None:down=frame
            age=(frame-down)%30;expected=['Down']
            if 6<=age<9:reason='uppercut_edge';expected.append('High_Punch')
            else:reason='duck_prepare_or_recovery'
        need(d['reason']==reason and int(d['down_start'])==(down if down is not None else-1),'Exact independent Down preparation/HP6..8/controller state')
        need(inputs[frame]==expected,'Every actual physical input at '+str(frame))
        reasons[reason]+=1;categories[int(f['cpu_action'])]+=1
        if frame in live:
            old=live[frame]
            mapping=dict(human_actor=f['human_actor'],human_main=f['human_main'],cpu_actor=f['cpu_actor'],cpu_main=f['cpu_main'],human='18:18',cpu='5:5',
              hpos=f['h_x']+','+f['h_y'],cpos=f['c_x']+','+f['c_y'],hfloor=f['h_floor'],cfloor=f['c_floor'],actions=f['human_action']+','+f['cpu_action'],
              flags=f['flags']+','+f['cpu_flags'],poses=f['human_pose']+','+f['cpu_pose'],health=f['health'])
            need(all(old[k]==v for k,v in mapping.items()),'Full original LIVE state cross-check')
    actions=[r for r in rows if r['tag']=='DUCK_ACTION'];upper=[]
    for r in actions:
        need(r['id']==r['roster']=='18'and r['actor']==r['owner']==r['a8']and r['main']==r['a13']and r['writes']=='0'and r['assistance']=='none','Actual native owned Sonya action store')
        need(int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF'and 0<int(r['health'].split(',')[0])<=161,'Native Main address/mask/positive health')
        if r['frame']in by:
            f=by[r['frame']];need(r['actor']==f['human_actor']and r['main']==f['human_main'],'Same-field native human action ownership')
        if int(r['after'])==0x107:
            need(r['pc']=='FF83C340'and int(r['a1'],16)&0xffff==0x107,'Actual original HUMAN107 store and operand, never CPU106')
            upper.append(r)
    handlers=[r for r in rows if r['tag']=='DUCK_HANDLER']
    for r in handlers:
        need(r['entry']=='FF870DC0'and r['pc']=='FF870DD0'and r['actor']==r['owner']==r['a8']and r['main']==r['a13']and r['writes']=='0'and r['assistance']=='none','Actual genuine uppercut routine fetch, not intended HP input')
        if r['frame']in by:
            f=by[r['frame']];need(r['actor']==f['human_actor']and r['main']==f['human_main'],'Actual handler belongs to observed human')
    return dict(actualCompleteDuckFields=len(fields),firstFrame=fields[0]['frame'],lastFrame=fields[-1]['frame'],reasons=dict(reasons),
      actualNativeOwnedActionStores=len(actions),actualNativeHuman107Stores=len(upper),actualNativeHumanUppercutFetches=len(handlers),
      cpuActionCategoriesObserved={f'{k:04X}':v for k,v in sorted(categories.items())},cpu507Classification='unclassified',
      stages=[int(r['stage'])for r in rows if r['tag']=='STAGE'],actualOwnRoundWins=sum(r['tag']=='WIN'and r['slot']=='2'for r in rows),actualPaidLosses=sum(r['tag']=='LOSS'for r in rows))

def main():
    need(not OUT.exists(),'Fresh immutable actual prefix qualifier');capture.source.source_boundary()
    raw=(FOLDER/'run.log').read_bytes();raw=raw[:raw.rfind(b'\n')+1]
    lines=raw.splitlines(keepends=True);last=max(i for i,line in enumerate(lines)if line.startswith(b'MK2_NAT_CAMPAIGN_DUCK_DECISION '));raw=b''.join(lines[:last+1]);text=raw.decode('utf-8')
    positive=replay(text);need(positive['actualNativeHuman107Stores']>0 and positive['actualNativeHumanUppercutFetches']>0,'Physical HP edges must activate real HUMAN107 and original routine, not only attempts')
    rows=parse(text);frame=next(r['frame']for r in rows if r['tag']=='DUCK_DECISION'and r['reason']=='uppercut_edge');f=next(r for r in rows if r['tag']=='DUCK_FIELD'and r['frame']==frame)
    trials=[]
    for tag,key,value in(('DUCK_FIELD','human_id',0),('DUCK_FIELD','cpu_roster',18),('DUCK_FIELD','human_owner','01000000'),('DUCK_FIELD','health','0,161'),('DUCK_FIELD','reset',1-int(f['reset'])),('DUCK_FIELD','h_y',int(f['h_floor'])-9),('DUCK_FIELD','h_x',int(f['c_x'])+87),('DUCK_DECISION','reason','grounded_approach'),('DUCK_DECISION','down_start',-1),('INPUT','button','Block')):
        try:replay(previous.change(text,tag,frame,key,value))
        except ValueError as error:trials.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual duck physical field/input fault accepted '+key)
        need(replay(text)==positive,'Exact original duck positive restored')
    for tag,actual,changes in(('DUCK_ACTION',next(r for r in rows if r['tag']=='DUCK_ACTION'and int(r['after'])==0x107),[('owner','01000000'),('at','01000000'),('mask','00FF'),('pc','FFF00000'),('a1','00000106')]),('DUCK_HANDLER',next(r for r in rows if r['tag']=='DUCK_HANDLER'),[('entry','FFF00000'),('a8','01000000')])):
        line=next(l for l in text.splitlines()if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')and dict(re.findall(r'(\w+)=([^\s]+)',l))=={k:str(v)for k,v in actual.items()if k!='tag'})
        for key,value in changes:
            changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and changed!=line,'Actual non-vacuous native action/handler fault')
            try:replay(text.replace(line,changed,1))
            except ValueError as error:trials.append(dict(tag=tag,key=key,rejectedBy=str(error)))
            else:raise ValueError('Actual native action/handler fault accepted '+key)
            need(replay(text)==positive,'Exact positive restored after real action/handler fault')
    proof=FOLDER/'guest_memory_proof.json';p=json.loads(proof.read_text());guest=capture.expected()
    need(p['everyActualByteComparedInRAM']and p['sha256']==hashlib.sha256(guest).hexdigest().upper()and p['guestDumpFilesWritten']==0 and p['captureSourceSHA256']==sha(capture.__file__)and p['transportSourceSHA256']==sha(ROOT/capture.LUA),'Actual full initialized guest and executed source bound')
    pins=json.loads((FOLDER/'input_hashes_before.json').read_text())
    for path,h in pins.items():need(sha(path)==h,'Actual executed input bytes unchanged')
    for path in(Path(__file__),Path(previous.__file__),Path(capture.source.__file__),proof,FOLDER/'input_hashes_before.json',ROOT/'audit_v4248_mileena_duck_pressure_source_preflight/report.json'):pins[str(path.resolve())]=sha(path)
    report=dict(passed=True,actualCapturedPrefix=positive,actualRowFaultsRejected=trials,inputHashes=pins,nativeLogPrefixBytes=len(raw),nativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
      prefixProofOnly=True,completedWholeCampaignAccepted=False,naturalTowerClearAccepted=False,endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,prefix=positive,actualFaultsRejected=len(trials),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
