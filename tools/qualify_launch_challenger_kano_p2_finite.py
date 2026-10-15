"""Kano P2 gameplay and own-source teardown, without unobserved CPU audio.

CPU Sonya already owns Bicycle samples when the audio window opens. The launch
which produced that carry-in is outside this observer window; do not infer its
clock from the captured PCM or pretend the CPU channels were idle.
"""
import inspect,json
from pathlib import Path
import qualify_launch_challenger_transition_remaining_v2 as previous
ROOT,need,sha=previous.ROOT,previous.need,previous.sha

def own_source(c,events):
 original=previous.original
 source=inspect.getsource(original.prior.mirror.owners)
 changes=[("rows(text,'MK2_HSPECIAL_READY')","rows(text,'MK2_MAUDIO_BEGIN')"),("rows(text,'MK2_HSPECIAL_RESULT')","rows(text,'MK2_JR_RESULT')"),("rows(text,'MK2_HSPECIAL_FIELD')","rows(text,'MK2_KO_FIELD')"),
 ("records=rows(text,'MK2_INTERRUPT_OWNER');channels=rows(text,'MK2_INTERRUPT_CHANNEL')","records=[r for r in rows(text,'MK2_INTERRUPT_OWNER')if r['slot']=='2'];channels=[r for r in rows(text,'MK2_INTERRUPT_CHANNEL')if r['channel']in('12','13')]"),
 ("len(records)==2*(last-first+1)","len(records)==last-first+1"),("for s in(1,2)","for s in(2,)"),
 ("len(channels)==4*(last-first+1)","len(channels)==2*(last-first+1)"),("for c in range(10,14)","for c in(12,13)")]
 for before,after in changes:need(source.count(before)==1,'Entire original own-slot lifetime and channel clock contract');source=source.replace(before,after,1)
 cache={}
 def rows(text,tag):
  if tag not in cache:cache[tag]=original.rows(text,tag)
  return cache[tag]
 scope=dict(vars(original.prior.mirror),rows=rows)
 exec(compile(source,__file__+'::exact_native_P2_owned_source_inventory','exec'),scope)
 return scope['owners'](c,events)

def qualify(c):
 need(c['move']=='ball'and c['side']==2 and c['terminal']['nativeExit']==0 and c['report']['passed'],'Exact same-terminal Kano P2 run')
 out=ROOT/'audit_launch_challenger_transition_finite_ball_p2';need(not out.exists(),'Fresh explicit partial-audio proof')
 original=previous.original;pins=dict(c['pins']);physical,by=previous.physical_inventory(c)
 game=original.gameplay_gate(c['text'],'kano',2);events=original.source_events(c,pins);owned=own_source(c,events)
 first=int(original.prior.one(c['text'],'MK2_MAUDIO_BEGIN')['frame'])
 carry=[r for r in original.rows(c['text'],'MK2_INTERRUPT_OWNER')if int(r['frame'])==first and r['slot']=='1'];channels=[r for r in original.rows(c['text'],'MK2_INTERRUPT_CHANNEL')if int(r['frame'])==first and r['channel']in('10','11')]
 need(len(carry)==1 and carry[0]['id']=='18'and carry[0]['actor']==by[first,1]['actor']and carry[0]['main']==by[first,1]['main']and [r['length']for r in channels]==['40720','66523'],'Actual CPU Sonya Bicycle carry-in is retained, not treated as idle')
 rejection=ROOT/'audit_launch_challenger_transition_cpu_carry_rejection_ball_p2';need(not rejection.exists(),'Retain whole-audio ownership rejection')
 try:original.owners(c,events)
 except ValueError as error:need(str(error)=='Full owner retirement, no stale or cross-slot owner','Exact rejected idle-other-slot assumption')
 else:raise ValueError('Actual carry-in unexpectedly accepted by idle-slot checker')
 rejection.mkdir();(rejection/'failure.json').write_text(json.dumps(dict(passed=False,nativeGameFailure=False,nativeTerminal=c['terminal'],error='Full owner retirement, no stale or cross-slot owner',actualInitialCPUOwner=carry,actualInitialCPUChannels=channels,executedSourceSHA256=sha(previous.__file__)),indent=2)+'\n')
 faults=[]
 from check_launch_ko_round_faults import change
 boundary=events[0]['nativeBoundaryFrame']
 for key,value in(('actor','01000000'),('main','01000000'),('id','18'),('health','161')):
  bad=change(c['text'],'MK2_INTERRUPT_OWNER',lambda r:r['frame']==str(boundary)and r['slot']=='2',key,value)
  try:own_source(dict(c,text=bad),events)
  except(ValueError,KeyError)as error:faults.append(dict(kind='retired Kano owner '+key,rejectedBy=str(error)))
  else:raise ValueError('Changed own-slot retirement admitted')
 need(own_source(c,events)==owned,'Entire own-source positive restored')
 for p in(Path(__file__),Path(previous.__file__),Path(original.__file__),ROOT/'tools/check_launch_ko_round_faults.py',*c['folder'].rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual executed sources and artifacts stable')
 report=dict(passed=True,nativeTerminal=c['terminal'],completePhysicalAndHealthInventory=physical,wholeOriginalJoinedGameplay=game,completeOwnSourceOwnership=owned,sourceEvents=[{k:v for k,v in e.items()if k not in('sample','positions')}for e in events],actualInitialCPUOwner=carry,actualInitialCPUChannels=channels,actualFaultsRejected=faults,completeSourceWaveformAccepted=False,allSlotOwnershipAccepted=False,fullPortAcceptance=False,inputHashes=pins,newNativeBoots=0,newBuilds=0,newRawMedia=0,nextAction='Use an observer that starts before the CPU launch for any future whole mixed-audio acceptance; do not derive a missing marker clock by fitting PCM.')
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,completeGameplay=True,wholeAudioAccepted=False,physicalFields=physical['continuousPhysicalFields'])),flush=True);return report
