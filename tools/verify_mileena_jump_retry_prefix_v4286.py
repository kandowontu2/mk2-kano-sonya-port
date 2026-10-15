"""Independent actual physical Ring/retreat replay; never a tower-clear shortcut."""
import collections,hashlib,json,re,subprocess
from pathlib import Path
import verify_mirror_guard_zoning_prefix_v4194 as original
import run_mileena_jump_retry_campaign_v4283 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
FOLDER=ROOT/'audit_v4284_sonya_mileena_jump_retry_p2_campaign'
OUT=ROOT/'audit_v4287_mileena_jump_retry_actual_prefix_checked'
parse,change=original.parse,original.change

def replay(text):
    rows=parse(text);fields=[r for r in rows if r['tag']=='RANGE_FIELD']
    decisions={r['frame']:r for r in rows if r['tag']=='RANGE_DECISION'}
    need(fields and len(fields)==len(decisions)==len({f['frame'] for f in fields}),
         'One complete native field and physical decision per observed field')
    inputs=collections.defaultdict(list)
    for r in rows:
        if r['tag']=='INPUT':inputs[r['frame']].append(r['button'])
    last,ring,ring_dir,jump,jump_dir=None,None,None,-1000,None
    reasons=collections.Counter();by={r['frame']:r for r in fields}
    live={r['frame']:r for r in rows if r['tag']=='LIVE'}
    for f in fields:
        frame=f['frame'];d=decisions[frame]
        need(f['human_slot']=='2' and f['fighter']=='sonya' and
             f['human_id']==f['human_roster']=='18' and f['cpu_id']==f['cpu_roster']=='5',
             'Actual native SonyaP2 versus real Mileena, never identity substitution')
        need(f['writes']==d['writes']=='0' and f['assistance']==d['assistance']=='none',
             'Actual read-only field and physical input')
        for who in ('human','cpu'):
            need(0x01000000<=int(f[who+'_actor'],16)<0x01100000 and
                 0x01000000<=int(f[who+'_main'],16)<0x01100000 and
                 f[who+'_owner']==f[who+'_actor'],'True native actor/Main ownership')
        need(all(0<int(n)<=161 for n in f['health'].split(',')),'Real positive health')
        reset=last is None or frame-last!=1
        need(int(f['reset'])==int(reset),'Independent consecutive-field controller reset')
        if reset:ring,ring_dir,jump,jump_dir=None,None,-1000,None
        last=frame;hx,cx=int(f['h_x']),int(f['c_x']);gap=abs(hx-cx)
        forward='Right' if hx<cx else 'Left';back='Left' if forward=='Right' else 'Right'
        expected=[]
        if ring is not None and frame-ring<64 and (frame-ring<12 or gap>=150):
            reason='ring_sequence';age=frame-ring
            if 2<=age<5:expected.append('Down')
            if 7<=age<10:expected.append(ring_dir)
            if 8<=age<12:expected.append('Low_Punch')
            if age>=15:expected+=['Down','Block']
        elif int(f['h_floor'])-int(f['h_y'])>8:
            reason='actual_air_kick'
            if jump_dir is not None and frame-jump<48:expected.append(jump_dir)
            if frame%6<3:expected.append('High_Kick')
        elif gap<150:
            ring=None
            if frame-jump>=4:jump=frame;jump_dir=back
            if frame-jump<3:reason='grounded_jump_retry_edge';expected=['Up',jump_dir]
            else:reason='grounded_jump_retry_release';expected=[jump_dir]
        else:reason='ring_attempt';ring=frame;ring_dir=forward
        need(d['reason']==reason and int(d['ring_start'])==(ring if ring is not None else -1) and
             d['ring_dir']==(ring_dir or 'none') and int(d['jump_start'])==jump and
             d['jump_dir']==(jump_dir or 'none'),'Every physical decision and all persistent state independently replayed')
        need(inputs[frame]==expected,'Every exact physical direction/button edge at '+str(frame))
        reasons[reason]+=1
        if frame in live:
            old=live[frame]
            mapping=dict(human_actor=f['human_actor'],human_main=f['human_main'],cpu_actor=f['cpu_actor'],cpu_main=f['cpu_main'],
              human='18:18',cpu='5:5',hpos=f['h_x']+','+f['h_y'],cpos=f['c_x']+','+f['c_y'],hfloor=f['h_floor'],cfloor=f['c_floor'],
              actions=f['human_action']+','+f['cpu_action'],flags=f['flags']+','+f['cpu_flags'],
              poses=f['human_pose']+','+f['cpu_pose'],health=f['health'])
            need(all(old[k]==v for k,v in mapping.items()),'Complete original LIVE native state cross-check')
    actions=[r for r in rows if r['tag'] in ('RANGE_ACTION','RANGE_CPU_ACTION')]
    cpu_throws=[];victim_clears=[];jumps=[];kicks=[]
    for r in actions:
        is_cpu=r['tag']=='RANGE_CPU_ACTION';identity='5' if is_cpu else '18';who='cpu' if is_cpu else 'human'
        need(r['id']==r['roster']==identity and r['actor']==r['owner']==r['a8'] and r['main']==r['a13'] and
             int(r['at'],16)==int(r['main'],16)+0x1f0 and r['mask']=='FFFF' and
             r['writes']=='0' and r['assistance']=='none' and all(0<int(n)<=161 for n in r['health'].split(',')),
             'Actual native action store has true owner/Main/address/mask/registers/positive health')
        if r['frame'] in by:
            f=by[r['frame']];need(r['actor']==f[who+'_actor'] and r['main']==f[who+'_main'],
                                  'Actual action belongs to same-field native combatant')
        if is_cpu and int(r['after'])==0x507:
            need(r['pc']=='FF8B6FA0' and int(r['a0'],16)&0xffff==0x507,
                 'Actual original CPU ground-throw setter/operand, not category-only inference')
            cpu_throws.append(r)
        if not is_cpu and r['pc']=='FF8428A0':
            need(r['after']=='0','Actual original opponent victim-capture clears human Main')
            victim_clears.append(r)
        if not is_cpu and int(r['after'])==0x308:
            need(r['pc']=='FF831360' and int(r['a0'],16)&0xffff==0x308,
                 'Actual original HUMAN308 jump store/operand, never hurt/throw airborne motion')
            jumps.append(r)
        if not is_cpu and int(r['after'])==0x200:
            need(r['pc']=='FF871F50' and int(r['a0'],16)&0xffff==0x200,
                 'Actual original HUMAN200 air-kick store/operand, not HK input count')
            kicks.append(r)
    rings=[r for r in rows if r['tag']=='SPECIAL' and r['move']=='ring' and int(r['stage'])==9]
    for r in rings:
        need(r['id']==r['roster']=='18' and r['actor']==r['a8'] and r['main']==r['a13'] and
             r['entry']=='FFFFB400' and r['at']=='FFFFB410' and r['pc']=='FFFFB420',
             'Genuine true own Ring task instruction fetch, not a planned projectile')
    return dict(actualCompleteRangeFields=len(fields),firstFrame=fields[0]['frame'],lastFrame=fields[-1]['frame'],
      reasons=dict(reasons),actualNativeOwnRingTasks=len(rings),actualNativeOwnedActionStores=len(actions),
      actualNativeCpuGroundThrowStores=len(cpu_throws),actualOriginalHumanVictimCaptures=len(victim_clears),
      actualNativeHuman308JumpStores=len(jumps),actualNativeHuman200AirKickStores=len(kicks),
      cpu507Classification='Actual logged setter is original ground throw; category-only fields never credited as activation.',
      stages=[int(r['stage']) for r in rows if r['tag']=='STAGE'],
      actualOwnRoundWins=sum(r['tag']=='WIN' and r['slot']=='2' for r in rows),actualPaidLosses=sum(r['tag']=='LOSS' for r in rows))

def main():
    need(not OUT.exists(),'Fresh immutable actual prefix proof');capture.source.source_boundary()
    raw=(FOLDER/'run.log').read_bytes();raw=raw[:raw.rfind(b'\n')+1];lines=raw.splitlines(keepends=True)
    last=max(i for i,l in enumerate(lines) if l.startswith(b'MK2_NAT_CAMPAIGN_RANGE_DECISION '))
    raw=b''.join(lines[:last+1]);text=raw.decode();positive=replay(text)
    need(positive['actualNativeOwnRingTasks']>0,'Actual native Ring tasks required, not intended input counts')
    rows=parse(text);f=next(r for r in rows if r['tag']=='RANGE_FIELD' and
        next(d for d in rows if d['tag']=='RANGE_DECISION' and d['frame']==r['frame'])['reason']=='ring_attempt')
    frame=f['frame'];faults=[]
    cases=[('RANGE_FIELD',frame,'human_id',0),('RANGE_FIELD',frame,'cpu_roster',18),
      ('RANGE_FIELD',frame,'human_owner','01000000'),('RANGE_FIELD',frame,'health','0,161'),
      ('RANGE_FIELD',frame,'reset',1-int(f['reset'])),('RANGE_FIELD',frame,'h_x',int(f['c_x'])+149),
      ('RANGE_FIELD',frame,'h_y',int(f['h_floor'])-9),('RANGE_DECISION',frame,'reason','grounded_jump_retry_edge'),
      ('RANGE_DECISION',frame,'ring_start',-1),('RANGE_DECISION',frame,'ring_dir','none')]
    lp=next(r for r in rows if r['tag']=='INPUT' and r['button']=='Low_Punch' and
            r['frame']>=frame and r['frame']<=frame+11)
    cases.append(('INPUT',lp['frame'],'button','High_Punch'))
    for tag,n,key,value in cases:
        try:replay(change(text,tag,n,key,value))
        except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
        else:raise ValueError('Actual physical state/input fault accepted '+key)
        need(replay(text)==positive,'Exact original positive restored')
    for tag in ('RANGE_ACTION','RANGE_CPU_ACTION'):
        r=next(r for r in rows if r['tag']==tag)
        line=next(l for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ') and
          dict(re.findall(r'(\w+)=([^\s]+)',l))=={k:str(v) for k,v in r.items() if k!='tag'})
        for key,value in (('owner','01000000'),('at','01000000'),('mask','00FF'),('a8','01000000')):
            damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Actual non-vacuous native store fault')
            try:replay(text.replace(line,damaged,1))
            except ValueError as error:faults.append(dict(tag=tag,key=key,rejectedBy=str(error)))
            else:raise ValueError('Actual native action store fault accepted '+key)
            need(replay(text)==positive,'Exact original native action positive restored')
    throw=next((r for r in rows if r['tag']=='RANGE_CPU_ACTION' and int(r['after'])==0x507),None)
    if throw:
        line=next(l for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_RANGE_CPU_ACTION ') and
          dict(re.findall(r'(\w+)=([^\s]+)',l))=={k:str(v) for k,v in throw.items() if k!='tag'})
        for key,value in (('pc','FFF00000'),('a0','00000303')):
            damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Actual CPU throw writer fault')
            try:replay(text.replace(line,damaged,1))
            except ValueError as error:faults.append(dict(tag='RANGE_CPU_ACTION_THROW',key=key,rejectedBy=str(error)))
            else:raise ValueError('Actual native CPU throw writer fault accepted '+key)
            need(replay(text)==positive,'Actual original CPU throw positive restored')
    for action,pc in ((0x308,'FF831360'),(0x200,'FF871F50')):
        event=next((r for r in rows if r['tag']=='RANGE_ACTION' and int(r['after'])==action),None)
        if not event:continue
        line=next(l for l in text.splitlines() if l.startswith('MK2_NAT_CAMPAIGN_RANGE_ACTION ') and
          dict(re.findall(r'(\w+)=([^\s]+)',l))=={k:str(v) for k,v in event.items() if k!='tag'})
        for key,value in (('pc','FFF00000'),('a0','00000000')):
            damaged,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and damaged!=line,'Actual native jump/kick store fault')
            try:replay(text.replace(line,damaged,1))
            except ValueError as error:faults.append(dict(tag='RANGE_ACTION_'+f'{action:04X}',key=key,rejectedBy=str(error)))
            else:raise ValueError('Actual native jump/kick writer fault accepted '+key)
            need(replay(text)==positive,'Actual original native jump/kick positive restored')
    proof=FOLDER/'guest_memory_proof.json';p=json.loads(proof.read_text());guest=capture.expected()
    need(p['everyActualByteComparedInRAM'] and p['sha256']==hashlib.sha256(guest).hexdigest().upper() and
         p['captureSourceSHA256']==sha(capture.__file__) and p['transportSourceSHA256']==sha(ROOT/capture.LUA) and
         p['guestDumpFilesWritten']==0,'Exact actual whole guest verified in RAM/source bound')
    pins=json.loads((FOLDER/'input_hashes_before.json').read_text())
    for p,h in pins.items():need(sha(p)==h,'Executed source unchanged')
    for p in (Path(__file__),Path(original.__file__),proof,FOLDER/'input_hashes_before.json',ROOT/'audit_v4282_mileena_jump_retry_source_preflight/report.json'):
        pins[str(p.resolve())]=sha(p)
    report=dict(passed=True,actualCapturedPrefix=positive,actualRowFaultsRejected=faults,inputHashes=pins,
      nativeLogPrefixBytes=len(raw),nativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
      prefixProofOnly=True,completedWholeCampaignAccepted=False,naturalTowerClearAccepted=False,
      endingPixelsAccepted=False,completeCampaignAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress report before writing')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,prefix=positive,actualFaultsRejected=len(faults),fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
