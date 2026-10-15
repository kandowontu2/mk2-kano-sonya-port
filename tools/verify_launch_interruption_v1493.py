"""One real incoming-hit audio cleanup; other attempts explicitly not accepted."""
import json,re
from pathlib import Path
import verify_sonya_launch_audio_v1489 as sound
ROOT=sound.ROOT;OUT=ROOT/'audit_v1493_launch_interruption_checked';need=sound.need
def verify_hit_log(log):
 h=sound.human;fields=h.rows(log,'FIELD');result=h.rows(log,'RESULT');need(len(result)==1 and not h.rows(log,'FAILED'),'Complete actual interrupted match')
 r=result[0];side=r['side'];move=r['move'];need((move,side)==('square',1),'This observed incoming uppercut is P1 square only')
 by={(q['frame'],q['slot']):q for q in fields};frames=range(r['ready'],r['frame']+1)
 need(len(by)==len(fields)==len(frames)*2,'Every actual native fighter callback')
 actors={n:(by[r['ready'],n]['actor'],by[r['ready'],n]['main'])for n in(1,2)}
 for f in fields:
  slot=f['slot'];need(f['id']==f['roster']==(18 if slot==side else 8)and f['state']==1 and f['mode']==2 and f['owner']==f['actor']and(f['actor'],f['main'])==actors[slot]and f['writes']==0,'Stable real actors and humans, never proxy IDs')
 health=h.rows(log,'HEALTH');incoming=[q for q in health if q['slot']==side and q['after']<q['before']]
 need(len(incoming)==1 and incoming[0]['before']==161 and incoming[0]['after']==121,'Actual single original 40-damage uppercut')
 for q in health:need(q['pc']==0xff836700 and q['mask']==0xffff and q['writes']==0,'Native collision damage stores only')
 hit=incoming[0]['frame'];need(r['entry']<hit<r['recovered'],'Hit actually interrupts the launched action')
 for frame in range(r['ready'],r['frame']):
  for slot in(1,2):
   writes=[q for q in health if q['frame']==frame and q['slot']==slot];a=by[frame,slot]['hp'];b=by[frame+1,slot]['hp']
   if writes:need(writes[0]['before']==a and writes[-1]['after']==b and all(x['after']==y['before']for x,y in zip(writes,writes[1:])),'Actual collision ledger explains every callback HP change')
   else:need(a==b,'No unexplained health changes')
 need(by[hit+1,side]['action']==0x503 and by[hit+1,side]['gravity']==0x6000 and by[hit+1,side]['vy']==0xfff40000,'Original real uppercut knockdown takes over, not merely an attempted input')
 owners=sound.media.records(log,'MK2_LAUNCH_OWNER');channels=sound.media.records(log,'MK2_LAUNCH_CHANNEL')
 ob={(int(q['frame']),int(q['slot'])):q for q in owners};cb={(int(q['frame']),int(q['channel'])):q for q in channels}
 cframes=range(1450,r['frame']+1);need(len(ob)==len(owners)==len(cframes)*2 and len(cb)==len(channels)==len(cframes)*4,'Whole actual sample and audio owner ledger')
 actor,main=actors[side]
 for frame in cframes:
  for slot in(1,2):
   q=ob[frame,slot];need(q['writes']=='0','Read-only host observer')
   active=slot==side and r['entry']<frame<=hit
   if active:need(int(q['actor'],16)==actor and int(q['main'],16)==main and q['health']=='161','Actual launch owner exists before interruption')
   else:need(q['actor']==q['main']=='00000000'and q['health']=='0','Audio owner clears by first callback after the real hit; other player untouched')
 for channel in range(10,14):
  rows=[cb[f,channel]for f in cframes];need(all(q['writes']==q['loop']==q['paused']=='0'for q in rows),'Unlooped audio channel with no observer writes')
  if channel!=10:need(all(q['length']=='0'and float(q['pos'])==0 for q in rows),'Other player and unused channels untouched')
  else:
   length=45512;need(cb[r['entry'],channel]['length']=='0'and all(cb[f,channel]['length']==str(length)for f in range(r['entry']+1,r['frame']+1)),'Only exact original square asset starts')
   pos=float(cb[hit,channel]['pos']);need(0<pos<length and all(float(cb[f,channel]['pos'])==pos for f in range(hit+1,r['frame']+1)),'Playback truly stops mid-cue on damage and never restarts')
 for frame in (r['recovered'],r['frame']):need(all(h.clean(by[frame,n])for n in(1,2)),'Both real fighters recover cleanly on their own floors')
 follow=r['followup'];need(follow==r['recovered']+16 and r['frame']==follow+160,'Complete ordinary follow-up horizon')
 need(any(by[f,side]['vx']!=0 for f in range(follow+3,follow+9))and any(by[f,side]['y']<by[f,side]['floor']for f in range(follow+42,follow+65))and any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),'Actual walking, jumping and high punch respond after interrupted recovery')
 return dict(move=move,side=side,entry=r['entry'],actualHit=hit,damage=40,cleanupByFrame=hit+1,stoppedSourcePosition=pos,recovered=r['recovered'],terminal=r['frame'],actualIncomingHitCleanupAccepted=True)
def verify():
 pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve());actual=pins.setdefault(key,sound.sha(p));need(wanted is None or actual==wanted,'Changed actual source/evidence: '+key)
 proofpath=ROOT/'audit_v1489_sonya_launch_audio_checked/report.json';proof=json.loads(proofpath.read_text());need(proof['passed']and proof['wholeGuestIndependentlyReconstructed'],'Bound actual source/guest/channel proof');pin(proofpath)
 for p,h in proof['inputHashes'].items():pin(p,h)
 guest=sound.expected_guest()[0];cases={};accepted=None
 for name,move,side in [('audit_v1491_square_interruption_p1','square',1),('audit_v1492_square_interruption_p2','square',2),('audit_v1492_bicycle_interruption_p1','bicycle',1),('audit_v1492_bicycle_interruption_p2','bicycle',2)]:
  folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));need(meta['exit_code']==0 and meta['candidate']==sound.NAME and meta['assistance']=='none'and not meta['cheats_enabled'],'Actual unassisted incoming-hit attempt')
  for p,h in meta['input_hashes'].items():pin(p,h)
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Entire actual guest exact')
  log=(folder/'run.log').read_text(encoding='utf-8-sig');need(not re.search('LUA ERROR|fatal error|access violation',log,re.I),'Runtime error')
  incoming=[q for q in sound.human.rows(log,'HEALTH')if q['slot']==side and q['after']<q['before']]
  if incoming:cases[name]=verify_hit_log(log);accepted=log
  else:
   result=sound.human.rows(log,'RESULT');need(len(result)==1 and not sound.human.rows(log,'FAILED'),'Attempt still reaches ordinary recovery')
   cases[name]=dict(move=move,side=side,actualIncomingHitCleanupAccepted=False,reason='Physical uppercut attempt did not damage Sonya; not an interruption acceptance')
  for p in folder.rglob('*'):
   if p.is_file():pin(p)
 need(accepted is not None and sum(q['actualIncomingHitCleanupAccepted']for q in cases.values())==1,'Exactly the actually observed incoming-hit fixture')
 mutations=[('wrong_damage',accepted.replace('slot=1 before=161 after=121 mask=FFFF','slot=1 before=161 after=122 mask=FFFF')),('wrong_native_store',accepted.replace('pc=FF836700','pc=FF000000')),('proxy_id',accepted.replace('id=18 roster=18','id=1 roster=1')),('missing_health', '\n'.join(q for q in accepted.splitlines()if not q.startswith('MK2_HSPECIAL_HEALTH'))),('missing_sample_ledger','\n'.join(q for q in accepted.splitlines()if not q.startswith('MK2_LAUNCH_CHANNEL'))),('looped_voice',accepted.replace('loop=0 paused=0','loop=1 paused=0')),('observer_writes',accepted.replace('writes=0','writes=1'))]
 tests=[]
 for name,log in mutations:
  need(log!=accepted,'Effective in-memory corruption')
  try:verify_hit_log(log)
  except ValueError as error:tests.append(dict(name=name,rejected=True,reason=str(error)))
  else:raise ValueError('Counterexample accepted: '+name)
 pin(Path(__file__));pin(ROOT/'tools/verify_sonya_launch_audio_v1489.py')
 return dict(passed=True,candidate=sound.NAME,cases=cases,acceptedActualIncomingHitCases=1,counterexamples=tests,inputHashes=pins,bothSlotsInterruptionAccepted=False,bicycleInterruptionAccepted=False,fullPortAccepted=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Do not overwrite proof')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'passed':report['passed'],'error':report.get('error'),'acceptedIncomingHitCases':report.get('acceptedActualIncomingHitCases'),'counterexamples':len(report.get('counterexamples',[]))}),flush=True)
 raise SystemExit(0 if report['passed']else 1)
