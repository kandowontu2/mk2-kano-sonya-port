"""Real native uppercut damage, owned mid-cue stops and complete ordinary recovery.

Audio stops by the first callback after damage. Original hurt-task dispatch may
take one or two callbacks depending on physical task order; both must enter
the original uppercut trajectory, never a forced observer state. No all-hit,
simultaneous/KO/round or all-game acceptance is implied.
"""
import json,re
from pathlib import Path
import verify_active_launch_timer_v1520 as source
sound=source.sound;ROOT=source.ROOT;need=source.need
OUT=ROOT/'audit_v1532_active_launch_interruption_checked'
def verify_hit_log(log,victim=8):
 h=sound.human;fields=h.rows(log,'FIELD');results=h.rows(log,'RESULT')
 need(len(results)==1 and not h.rows(log,'FAILED'),'Complete actual interrupted match')
 r=results[0];side=r['side'];move=r['move']
 need(move in ('square','bicycle')and side in(1,2),'Actual supported physical Sonya launch')
 by={(q['frame'],q['slot']):q for q in fields};frames=range(r['ready'],r['frame']+1)
 need(len(by)==len(fields)==len(frames)*2,'Every actual native fighter callback')
 actors={s:(by[r['ready'],s]['actor'],by[r['ready'],s]['main'])for s in(1,2)}
 for q in fields:
  s=q['slot'];need(q['id']==q['roster']==(18 if s==side else victim)and q['state']==1 and q['mode']==2 and q['owner']==q['actor']and(q['actor'],q['main'])==actors[s]and q['writes']==0,'Stable real physical fighters/humans, not proxy actors')
 health=h.rows(log,'HEALTH');incoming=[q for q in health if q['slot']==side and q['after']<q['before']]
 need(len(incoming)==1 and incoming[0]['before']==161 and incoming[0]['after']==121,'Actual single original 40-damage uppercut')
 for q in health:need(q['pc']==0xff836700 and q['mask']==0xffff and q['writes']==0,'Original native collision damage store')
 hit=incoming[0]['frame'];need(r['entry']<hit<r['recovered'],'The actual hit interrupts an already launched move')
 for frame in range(r['ready'],r['frame']):
  for s in(1,2):
   stores=[q for q in health if q['frame']==frame and q['slot']==s]
   a=by[frame,s]['hp'];b=by[frame+1,s]['hp']
   if stores:need(stores[0]['before']==a and stores[-1]['after']==b and all(x['after']==y['before']for x,y in zip(stores,stores[1:])),'Original damage ledger explains every callback HP transition')
   else:need(a==b,'No unexplained health transition')
 hurt=[f for f in range(hit+1,hit+3)if by[f,side]['action']==0x503 and by[f,side]['gravity']==0x6000 and by[f,side]['vy']==0xfff40000]
 need(bool(hurt),'Actual original uppercut hurt-task dispatch and knockdown trajectory')
 owners=sound.media.records(log,'MK2_LAUNCH_OWNER');channels=sound.media.records(log,'MK2_LAUNCH_CHANNEL')
 ob={(int(q['frame']),int(q['slot'])):q for q in owners};cb={(int(q['frame']),int(q['channel'])):q for q in channels}
 cframes=range(1450,r['frame']+1)
 need(len(ob)==len(owners)==len(cframes)*2 and len(cb)==len(channels)==len(cframes)*4,'Every actual ownership and source-position callback')
 actor,main=actors[side]
 for frame in cframes:
  for s in(1,2):
   q=ob[frame,s];need(q['writes']=='0','Read-only host owner observer')
   if s==side and r['entry']<frame<=hit:
    need(int(q['actor'],16)==actor and int(q['main'],16)==main and q['health']=='161','Real owned launch exists before damage')
   else:need(q['actor']==q['main']=='00000000'and q['health']=='0','Owner clears by first callback after damage; opponent untouched')
 base=10+(side-1)*2
 lengths={base:45512}if move=='square'else{base:40720,base+1:66523}
 stops={}
 for channel in range(10,14):
  stream=[cb[f,channel]for f in cframes]
  need(all(q['writes']==q['loop']==q['paused']=='0'for q in stream),'Finite unpaused channels; no observer writes')
  if channel not in lengths:
   need(all(q['length']=='0'and float(q['pos'])==0 for q in stream),'Other player and unused channels never start')
  else:
   length=lengths[channel]
   need(all(cb[f,channel]['length']=='0'and float(cb[f,channel]['pos'])==0 for f in range(1450,r['entry']+1)),'No cue before actual native startup')
   need(all(cb[f,channel]['length']==str(length)for f in range(r['entry']+1,r['frame']+1)),'Only complete exact original asset loads')
   positions=[float(cb[f,channel]['pos'])for f in range(r['entry']+1,hit+2)]
   stop=float(cb[hit+1,channel]['pos'])
   need(positions[0]>0 and all(a<=b for a,b in zip(positions,positions[1:]))and 0<stop<length,'Real source playback starts and advances before its mid-cue stop')
   # stop() synchronizes the audio stream to the timer callback, so the last
   # position can advance beyond the previous frame's read-only sample. It
   # must be frozen by the next callback and never resume after recovery.
   need(all(float(cb[f,channel]['pos'])==stop for f in range(hit+1,r['frame']+1)),'Actual voice stops by next callback and never restarts')
   stops[channel]=stop
 marks=[q for q in sound.sound_rows(log)if q['word']in('6B00','6B01','6B02')]
 wanted=['6B00']if move=='square'else['6B01','6B02']
 need([q['word']for q in marks]==wanted and all(int(q['frame'])==r['entry']for q in marks),'Exactly the native launched voice markers')
 for frame in (r['recovered'],r['frame']):need(all(h.clean(by[frame,s])for s in(1,2)),'Both fighters recover cleanly on their own floors')
 follow=r['followup'];need(follow==r['recovered']+16 and r['frame']==follow+160,'Complete ordinary follow-up horizon')
 need(any(by[f,side]['vx']!=0 for f in range(follow+3,follow+9))and any(by[f,side]['y']<by[f,side]['floor']for f in range(follow+42,follow+65))and any(by[f,side]['action']==0x101 for f in range(follow+114,follow+140)),'Real walking, jumping and punch respond after interrupted recovery')
 return dict(move=move,side=side,entry=r['entry'],actualHit=hit,damage=40,hurtTaskFrame=min(hurt),cleanupByFrame=hit+1,stoppedSourcePositions=stops,recovered=r['recovered'],terminal=r['frame'],actualIncomingHitCleanupAccepted=True)
def verify():
 proofpath=source.OUT/'report.json';proof=json.loads(proofpath.read_text());need(proof['passed']and proof['wholeGuestIdenticalToV1473'],'Exact active-only source/guest and finite playback proof')
 pins={}
 def pin(p,wanted=None):
  p=Path(p);key=str(p.resolve())
  if key not in pins:pins[key]=source.sha(p)
  need(wanted is None or pins[key]==wanted,'Changed input '+key)
 pin(proofpath)
 for p,h in proof['inputHashes'].items():pin(p,h)
 build=json.loads((ROOT/source.NAME/'build-info.json').read_text(encoding='utf-8-sig'));guest=source.expected_guest()[0]
 specs=[('audit_v1527_square_interruption_p1','square',1,8),('audit_v1519_interruption_bicycle_p1','bicycle',1,8),('audit_v1519_interruption_bicycle_p2','bicycle',2,8),('audit_v1519_interruption_square_p1','square',1,8),('audit_v1519_interruption_square_p2','square',2,3),('audit_v1529_square_late_interruption_p2','square',2,8),('audit_v1531_square_walk_in_interruption_p2','square',2,8)]
 cases={};accepted=[]
 for name,move,side,victim in specs:
  folder=ROOT/name;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
  need(meta['exit_code']==0 and meta['candidate']==source.NAME and meta['executable_sha256']==source.EXE_SHA and meta['assistance']=='none'and not meta['cheats_enabled'],'Actual matched unassisted capture')
  need(before==meta['input_hashes']and all(before.get(p)==h for p,h in build['input_hashes'].items()),'Complete executed source manifest')
  for p,h in before.items():pin(p,h)
  need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual guest unchanged')
  log=(folder/'run.log').read_text(encoding='utf-8-sig');need(not re.search('LUA ERROR|fatal error|access violation',log,re.I),'No runtime failure')
  incoming=[q for q in sound.human.rows(log,'HEALTH')if q['slot']==side and q['after']<q['before']]
  if incoming:
   row=verify_hit_log(log,victim);cases[name]=row;accepted.append((name,log,victim,row))
  else:
   result=sound.human.rows(log,'RESULT');need(len(result)==1 and not sound.human.rows(log,'FAILED'),'Unexercised attempt still reaches ordinary recovery')
   cases[name]=dict(move=move,side=side,actualIncomingHitCleanupAccepted=False,reason='No native incoming damage occurred; not an interruption acceptance')
  for p in folder.rglob('*'):
   if p.is_file():pin(p)
 required={('square',1),('bicycle',1),('bicycle',2)}
 got={(q['move'],q['side'])for n,l,v,q in accepted};need(required<=got,'At least all three actually observed incoming-hit cases')
 counterexamples=[]
 for name,log,victim,row in accepted:
  mutations=[('wrong_damage',log.replace('before=161 after=121 mask=FFFF','before=161 after=122 mask=FFFF')),('wrong_store',log.replace('pc=FF836700','pc=FF000000')),('proxy_id',log.replace('id=18 roster=18','id=1 roster=1')),('missing_health','\n'.join(q for q in log.splitlines()if not q.startswith('MK2_HSPECIAL_HEALTH'))),('missing_channels','\n'.join(q for q in log.splitlines()if not q.startswith('MK2_LAUNCH_CHANNEL'))),('looped_voice',log.replace('loop=0 paused=0','loop=1 paused=0')),('observer_writes',log.replace('writes=0','writes=1')),('missing_owner','\n'.join(q for q in log.splitlines()if not q.startswith('MK2_LAUNCH_OWNER')))]
  for label,altered in mutations:
   need(altered!=log,'Effective in-memory counterexample')
   try:verify_hit_log(altered,victim)
   except ValueError as error:counterexamples.append(dict(case=name,mutation=label,rejected=True,reason=str(error)))
   else:raise ValueError('Accepted corruption '+name+' '+label)
 pin(__file__)
 return dict(passed=True,candidate=source.NAME,cases=cases,acceptedActualIncomingHitCases=len(accepted),counterexamples=counterexamples,inputHashes=pins,bothSlotsBicycleInterruptionAccepted=True,bothSlotsSquareInterruptionAccepted={('square',1),('square',2)}<=got,simultaneousInterruptionAccepted=False,KOOrRoundInterruptionAccepted=False,fullPortAccepted=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Never overwrite proof')
 try:report=verify()
 except Exception as error:report=dict(passed=False,error=repr(error),candidate=source.NAME,fullPortAccepted=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(dict(passed=report['passed'],error=report.get('error'),acceptedCases=report.get('acceptedActualIncomingHitCases'),squareBothSlots=report.get('bothSlotsSquareInterruptionAccepted'),counterexamples=len(report.get('counterexamples',[]))),indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
