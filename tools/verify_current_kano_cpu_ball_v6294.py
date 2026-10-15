"""Current naturally chosen CPU ball hit, complete motion/poses and both recoveries.

Reuse one actual terminal6293 match. Native RNG/whole state/HP ledgers remain
mandatory. Source-native separation behavior is checked from both bodies;
register/velocity-store tap acceptance, art, shadows and audio stay separate.
Do not relabel the unmatched original two-knives scenario as accepted.
"""
import datetime,gzip,json,struct,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import current_kano_cpu_extended_contract_v6291 as model
import verify_current_existing_cpu_leg_choices_v6274 as faults_source

ROOT,need,sha=current.ROOT,current.need,current.sha
CASE=ROOT/'audit_v6293_current_kano_cpu_extended_ram'
OUT=ROOT/'audit_v6295_current_kano_cpu_ball_checked'
PARENT=ROOT/'audit_v6283_current_cpu_leg_square_compound_checked/report.json'


def gate(text,guest,payload):
 inventory=model.verify(text,guest)
 choices=inventory['nativeChoices'];need(len(choices)==1 and choices[0]['move']=='ball','Actual one naturally selected ball, not prescribed move')
 choice=choices[0];start=choice['frame'];actor,main=choice['actor'],choice['main']
 route=(0xfffbc0f0-0xff800000)//8
 need(struct.unpack_from('<HI',guest,route)==(0xc080,0xffffde00),'Actual observed AI branch jumps to own native ball routine')
 need(struct.unpack_from('<21H',guest,(0xfffe2000-0xff800000)//8)==
      (0x098f,0x7cc0,0x0d5f,0x87c0,0xff82,0x0b45,0xfecf,0xc805,0x09af,0x033e,0x09c0,3,0x0960,
       0x09af,0x033e,0x09c0,3,0x0580,0x19d0,0x0106,0x0960),
      'Entire native save/helper/304-distance/restore/bounded-counter callback')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 lo,hi=((a-0xff800000)//8 for a in(0xff828000,0xff828900))
 need(guest[lo:hi]==stock[lo:hi],'Original native body separation/velocity/position program unchanged')
 need(struct.unpack_from('<9H',guest,(0xffffec00-0xff800000)//8)==(57,9,72,31,0x1417,0x1805,0,0,1),
      'Exact native translated high-plane ball descriptor, reaction and24 damage')
 root=0xff004010
 poses=struct.unpack_from('<11I',payload,(root-0xfe800000)//8)
 need(poses==(0xff00eae0,*range(0xff00eb40,0xff00ecc1,0x40),1,0xff004030,0xff00ed00),
      'Whole actual owned original roll sequence with loop token and destination')
 fields=model.original.pair.rows(text,'FIELD');by={r['frame']:r for r in fields}
 events=model.knife.overlap.rows(text,'EVENT')
 own=[r for r in events if r['a8']==actor and r['a13']==main]
 ready=next(r for r in own if r['kind']=='regain' and r['frame']>start);end=ready['frame']
 need(start+1==inventory['wholeNativeHealthLedger']['first'] and end-start==59,
      'Real native first scheduler-field choice, then full59-field recovery; no invented entry callback')
 hp=[r for r in model.knife.overlap.rows(text,'HEALTH')if start<=r['frame']<=end and r['before']!=r['after']]
 need(len(hp)==1,'Only native ball damage in complete ball window');hit=hp[0];at=hit['frame']
 first=by[start+1]
 need((hit['slot'],hit['pc'],hit['a8'],hit['a13'],hit['mask'],hit['a10'],hit['before']-hit['after'])==
      (1,0xff836700,actor,main,65535,24,24),'Actual own original unblocked24 contact and physical HP store')
 block=[r for r in model.knife.rows(text,'BLOCK')if r['frame']==at and r['decision']in(0,1)]
 button=[r for r in model.knife.rows(text,'BLOCK')if r['frame']==at and r['decision']==2]
 need(len(block)==len(button)==1 and block[0]['decision']==0 and block[0]['entry']==0xff837ae0
      and button[0]['main']==first['vmain'] and not((~button[0]['controls']&0xffffffff)&0x80000020),
      'Actual original unblocked decision and real physical human Block query')
 need(set(range(start+1,end+32))<=set(by),'Every ball/recovery and thirty subsequent live callbacks')
 sign=-1 if first['facing']&16 else 1
 flight=[by[f]for f in range(start+1,at+1)]
 need(6<len(flight)<26,'Actual contact after source-defined startup, not a relabeled miss')
 for i,r in enumerate(flight):
  need(r['action']==0x20b and r['y']==r['floor']+16 and r['vy']==r['gravity']==r['trail']==0
       and r['vx']==(sign*0xa0000)&0xffffffff and r['suppression']==2,
       'Every constant-speed native rolling field with finite push suppression')
  if i:
   need(r['xraw']==(flight[i-1]['xraw']+sign*0xa0000)&0xffffffff
        and r['pose']==poses[1+((i-1)//3)%7],'Every actual ten-pixel roll step and original three-field pose')
 landing=next(r for r in own if r['kind']=='landing' and r['frame']>at)
 land=landing['frame'];rebound=[by[f]for f in range(at+1,land+1)]
 need(len(rebound)==42 and rebound[0]['vy']==0xfff80000 and rebound[0]['gravity']==0x6000,
      'Complete original42-field rebound, not early fake cleanup')
 vx=(-sign*0x50000)&0xffffffff;limited=None
 signed=lambda v:v-0x100000000 if v&0x80000000 else v
 for i,r in enumerate(rebound):
  need(r['action']==0x602 and r['gravity']==0x6000 and r['trail']==0,
       'Every original rebound action/gravity without persistent trail')
  if i:
   p=rebound[i-1]
   need(r['vy']==(p['vy']+0x6000)&0xffffffff and r['yraw']==(p['yraw']+r['vy'])&0xffffffff
        and r['pose']==poses[1+((i-1)//2)%7],'Every exact fixed-point rebound step and original two-field roll pose')
  if i<20:
   need(r['vx']==vx,'Original first twenty five-pixel away fields')
   if i:need(r['xraw']==(rebound[i-1]['xraw']+vx)&0xffffffff,'Actual first twenty recoil coordinates')
  if r['vx']==0 and limited is None:
   need(i>=20,'Only later original separation limit can stop recoil')
   p=rebound[i-1];px=p['x']+(signed(vx)>>16);tx=p['vxpos']+(signed(p['vvx'])>>16)
   correction=(abs(px-tx)-304)//2
   direction=1 if px>tx else -1
   need(correction>=0 and r['x']==px-direction*correction and r['vxpos']==tx+direction*correction
        and abs(r['x']-r['vxpos'])in(304,305) and r['suppression']==0 and r['vvx']==0,
        'Observed two-body native304-distance correction and short-counter expiry, not arena clamp')
   limited=r['frame']
  need(r['vx']in(vx,0) and (limited is None or r['vx']==0 and r['xraw']==by[limited]['xraw']),
       'No unexplained rebound vector or post-limit displacement')
 need(limited is not None,'Actual source-native separation limit reached')
 last=rebound[-1];projected=(last['yraw']+last['vy']+last['gravity'])&0xffffffff
 need(last['y']<last['floor'] and projected>>16>=last['floor'] and end==land+4,
      'Native floor crossing followed by all four landing holds')
 landing_y=(last['floor']<<16)|(projected&65535)
 for f in range(land+1,end+1):
  r=by[f];need(r['action']==0x304 and r['yraw']==landing_y and r['vx']==r['vy']==r['gravity']==r['trail']==0,
              'Native floor clamp preserves fractional coordinate and full landing wait')
 for f in range(start+1,end+1):
  r=by[f];need(r['flags']&0x1c==0x10 and r['body']&0xc==0xc and r['hp']==first['hp']
              and r['vhp']==(hit['before']if f<=at else hit['after']),
              'Entire owned compact-ball lock and source-damage chronology')
 need(ready['action']==0 and ready['entry']==0xff861500 and ready['pc']==0xff861510 and ready['main_owner']==actor
      and ready['flags']&0x1c==ready['body']&0xc==0 and ready['vx']==ready['vy']==ready['gravity']==ready['trail']==0
      and ready['yraw']==landing_y,'Native ball regain clears both locks and motion, retaining correct floor fraction')
 flags=model.original.pair.flag_rows(text)
 for slot,a,m,f in [(2,actor,main,end)]:
  for kind,pc,mask in [('action',0xff83edd0,65535),('body',0xff83eeb0,0xc),('flags',0xff83efc0,0x14)]:
   rows=[r for r in flags if r['slot']==slot and r['frame']==f and r['kind']==kind and r['pc']==pc]
   need(rows and all((r['actor'],r['main'],r['a8'],r['a13'])==(a,m,a,m)
        and r['after']==r['before']&~mask for r in rows),'Source-owned native ball cleanup store: '+kind)
 victim=[r for r in events if r['a8']==first['vactor']and r['a13']==first['vmain']]
 fling=[r for r in victim if r['kind']=='fling' and r['frame']==at]
 need(len(fling)==1 and tuple(fling[0]['a'+str(n)]for n in range(4))==(0x60000,0xfffd0000,0x4000,5),
      'Actual native victim knockdown parameters and owning Main')
 vf=[]
 for f in range(at+1,end+1):
  if by[f]['vgravity']!=0x4000:break
  vf.append(by[f])
 need(len(vf)>8 and vf[0]['vvy']==0xfffd0000,'Whole original victim flight begins at own floor')
 for a,b in zip(vf,vf[1:]):
  need(b['vvy']==(a['vvy']+0x4000)&0xffffffff and b['vyraw']==(a['vyraw']+b['vvy'])&0xffffffff,
       'Every fixed-point native victim knockdown step')
 vr=next(r for r in victim if r['kind']=='regain' and r['frame']>at)
 need(vr['frame']>end and vr['action']==0 and vr['flags']&0x1c==vr['body']&0xc==0
      and vr['vx']==vr['vy']==vr['gravity']==vr['trail']==0 and vr['yraw']>>16==first['vfloor'],
      'Victim completes its distinct grounded ready/get-up after owning ball recovery')
 for f,prefix in [(end+1,''),(vr['frame']+1,'v')]:
  r=by[f];need(r[prefix+'flags']&0x1c==r[prefix+'body']&0xc==0 and r[prefix+'vy']==r[prefix+'gravity']==r[prefix+'trail']==0
              and r['vypos'if prefix else'y']==r[prefix+'floor'],'Real subsequent clean callback for each owning Main')
 return dict(passed=True,start=start,contact=at,damage=24,flightFields=len(flight),reboundFields=len(rebound),
             separationLimit=limited,landing=land,ownReady=end,victimReady=vr['frame'],victimFlightFields=len(vf),
             nativeStateHealthAndChoices=inventory,fullBoundaryRegisterTapAcceptance=False,
             artShadowAudioAcceptance=False,fullPortAcceptance=False)


def main():
 need(not OUT.exists(),'Fresh bounded current CPU ball evidence')
 report=json.loads((CASE/'result.json').read_text());need(report['passed']and report['nativeExit']==0,'Actual same native job already terminal')
 pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Executed current native sources unchanged')
 need(not faults_source.census.prior.census(),'Actual native census empty; no extra replay')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 positive=gate(text,guest,payload);start=positive['start'];hit=positive['contact'];ready=positive['ownReady'];limit=positive['separationLimit']
 def mutate(tag,key,value,where):return faults_source.mutate_field(text,tag,key,value,lambda r:all(r.get(k)==str(v)for k,v in where.items()))
 tests=[('cpu_proxy',mutate('MK2_CPU_PAIR_FIELD','id','1',{'frame':start+2})),
        ('roll_height',mutate('MK2_CPU_PAIR_FIELD','yraw','00000000',{'frame':start+2})),
        ('roll_speed',mutate('MK2_CPU_PAIR_FIELD','vx','FFF50000',{'frame':start+3})),
        ('roll_pose',mutate('MK2_CPU_PAIR_FIELD','pose','00000000',{'frame':start+2})),
        ('rebound_pose',mutate('MK2_CPU_PAIR_FIELD','pose','00000000',{'frame':hit+3})),
        ('rebound_gravity',mutate('MK2_CPU_PAIR_FIELD','gravity','00004000',{'frame':hit+4})),
        ('rebound_y_integration',mutate('MK2_CPU_PAIR_FIELD','yraw','00000000',{'frame':hit+4})),
        ('native_separation_position',mutate('MK2_CPU_PAIR_FIELD','x','1',{'frame':limit})),
        ('counter_survives_limit',mutate('MK2_CPU_PAIR_FIELD','suppression','3',{'frame':limit})),
        ('damage_kind',mutate('MK2_CPU_OVERLAP_HEALTH','a10','00000005',{'frame':hit})),
        ('false_block_button',mutate('MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFDF',{'frame':hit,'decision':2})),
        ('false_block_branch',mutate('MK2_KNIFE_PAIR_BLOCK','decision','1',{'frame':hit,'decision':0})),
        ('own_cleanup_lock',mutate('MK2_CPU_OVERLAP_EVENT','body','005E',{'frame':ready,'kind':'regain'})),
        ('victim_fling',mutate('MK2_CPU_OVERLAP_EVENT','a2','00008000',{'frame':hit,'kind':'fling'})),
        ('choice_threshold',mutate('MK2_CPU_CHOICE_EVENT','a0','000000FB',{'kind':'first_call'})),
        ('choice_actor',mutate('MK2_CPU_CHOICE_EVENT','owner','01000000',{'kind':'ball'})),
        ('round_refill_changed',mutate('MK2_CPU_ROUND_HEALTH','after','160',{'mode':6,'slot':1})),
        ('missing_live_callback',text.replace(next(line+'\n'for line in text.splitlines()if line.startswith('MK2_CPU_PAIR_FIELD ')and f'frame={ready+31} 'in line),'',1))]
 rejected=[]
 for label,bad in tests:
  need(bad!=text,'Real captured-record mutation: '+label)
  try:gate(bad,guest,payload)
  except(AssertionError,ValueError,KeyError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual CPU ball fault: '+label)
 need(gate(text,guest,payload)==positive,'Full original positive restored after real faults')
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Full objective remains active')
 for p in (PARENT,Path(__file__).resolve(),Path(model.__file__).resolve(),Path(faults_source.__file__).resolve(),*(p for p in CASE.rglob('*')if p.is_file())):
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual native inputs and terminal artifacts unchanged')
 result=dict(passed=True,candidate=current.NAME,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],case=positive,
             actualFaultsRejected=rejected,inputHashes=pins,scope=__doc__,fullPortAcceptance=False,fullGoalComplete=False,
             actualNativeBootsThisTurn=2,newBuilds=0,newZIPs=0,newRawMedia=0,
             preservedOriginalStandaloneKnifeScenarioRejection=True,knifeOrBladeCPUAccepted=False,
             previousGoalTurnClassification='progress: two existing compound Sonya leg/Square/ordinary traces and24faults',
             thisGoalTurnClassification='progress: actual current native Kano CPU ball hit/rebound/recovery, full1800field state/HP and18faults; no knife/blade promotion',
             nextActions=['Current CPU knife/blade: other already-proven current native Kano-versus-Sonya input route',
                          'Remaining mixed CPU art/shadow/audio and integrated release acceptance'])
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact lossless terminal report compression')
 print(json.dumps(dict(passed=True,damage=24,flightFields=positive['flightFields'],reboundFields=42,
                       allModePhysicalFields=positive['nativeStateHealthAndChoices']['wholeNativeHealthLedger']['allModePhysicalFields'],
                       actualFaultsRejected=len(rejected),knifeOrBladeAccepted=False,newBuilds=0)),flush=True)


if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
