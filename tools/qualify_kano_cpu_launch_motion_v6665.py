"""Both actually chosen rolls and declared completed pairs in terminal6664.

No new native dispatch and no historical trajectory equality. Preserve the
entire qualified6298 roll algorithm and whole1800-field state/HP/AI ledgers.
Distance determines flight duration; source rebound and landing holds do not.
All actual choices are checked, never a prefix spliced into an older scenario.
Raster, audio, interrupted pairs and full-port acceptance remain separate.
"""
import inspect,json,re,struct
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from pathlib import Path
import verify_current_kano_cpu_ball_v6294 as original
import current_kano_cpu_extended_contract_v6291 as state
import kano_ball_launch_context_v6642 as candidate
import native_process_census_v6647 as process
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
CASE=ROOT/'audit_v6664_kano_launch_cpu_native_audio'
OUT=ROOT/'audit_v6666_kano_cpu_launch_motion_checked'


def phase_gate():
 source=inspect.getsource(original.gate)
 changes={
  'def gate(text,guest,payload):':'def gate(text,guest,payload,serial):',
  "choices=inventory['nativeChoices'];need(len(choices)==1 and choices[0]['move']=='ball','Actual one naturally selected ball, not prescribed move')":
   "choices=inventory['nativeChoices'];need(choices and all(c['move']=='ball'for c in choices),'Every actual native choice is a roll in this observed match');need(serial in range(len(choices)),'One real choice index')",
  "choice=choices[0];start=choice['frame']":"choice=choices[serial];start=choice['frame']",
  '(57,9,72,31,0x1417,0x1805,0,0,1)':'(57,14-5-1,72,31,0x1417,0x1805,0,0,1)',
  "need(start+1==inventory['wholeNativeHealthLedger']['first'] and end-start==59,\n      'Real native first scheduler-field choice, then full59-field recovery; no invented entry callback')":
   "need(inventory['wholeNativeHealthLedger']['first']<=start+1<=end<=inventory['wholeNativeHealthLedger']['last'],'Every actual choice and complete recovery inside the whole observed native ledger')",
  "first=by[start+1]":"first=by[start+1];need(end-at==42+4,'Source-native42-field rebound plus four landing holds, independent of initial contact distance')",
  "for f in range(start+1,end+1):\n  r=by[f];need":
   "for f in range(start+1,end+1):\n  r=by[f]\n  coordinate=lambda v:(v&65535)-65536 if v&32768 else v&65535\n  need((r['x'],r['y'],r['vxpos'],r['vypos'])==tuple(coordinate(r[k]>>16)for k in('xraw','yraw','vxraw','vyraw')),'Every actual raw/integer two-body coordinate agrees')\n  need",
  "'Every constant-speed native rolling field with finite push suppression')":
   "'Every constant-speed native rolling field with finite push suppression')\n  need(r['yraw']==first['yraw'],'Entire constant raw roll height, not only integer plane')",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact whole original strengthened roll adaptation: '+before)
  source=source.replace(before,after,1)
 scope=dict(original.__dict__)
 exec(compile(source,__file__+'::whole6298_roll_all_actual_choices','exec'),scope)
 return scope['gate']


def mutate(text,tag,key,value,where):
 lines=[s for s in text.splitlines()if s.startswith(tag+' ')and all(re.search(r'\b'+re.escape(k)+'='+re.escape(str(v))+r'(?: |$)',s)for k,v in where.items())]
 need(lines,'Real captured record selected for '+tag+' '+str(where))
 line=lines[0];bad,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1)
 need(n==1 and bad!=line,'Nonvacuous actual native row mutation')
 return text.replace(line,bad,1)


def verify(carrier):
 text,guest=carrier['text'],carrier['guest']
 need(guest==candidate.expected(),'Entire actual new initialized guest equals independently source-derived candidate')
 payload=(ROOT/candidate.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 inventory=state.verify(text,guest);choices=inventory['nativeChoices'];gate=phase_gate()
 phases=[gate(text,guest,payload,i)for i in range(len(choices))]
 complete=state.original.pair.rows(text,'COMPLETE')
 pairs=[state.original.pair.verify_pair(text,'kano',r['cycle'],guest)for r in complete]
 need(len(pairs)==len(complete)>0 and all(p['passed']for p in pairs),'Every actually declared completed paired action passes its entire unchanged native contract')
 faults=[]
 def reject(label,bad,fn):
  need(bad!=text,'Actual record changed: '+label)
  try:fn(bad)
  except(AssertionError,ValueError,KeyError,IndexError)as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual native motion fault: '+label)
 for i,phase in enumerate(phases):
  start,hit,end,limit=map(phase.get,('start','contact','ownReady','separationLimit'))
  checks=[
   ('proxy','MK2_CPU_PAIR_FIELD','id','1',dict(frame=start+2)),
   ('raw height','MK2_CPU_PAIR_FIELD','yraw','00000000',dict(frame=start+2)),
   ('speed','MK2_CPU_PAIR_FIELD','vx','FFF50000',dict(frame=start+3)),
   ('roll pose','MK2_CPU_PAIR_FIELD','pose','00000000',dict(frame=start+2)),
   ('rebound pose','MK2_CPU_PAIR_FIELD','pose','00000000',dict(frame=hit+3)),
   ('gravity','MK2_CPU_PAIR_FIELD','gravity','00004000',dict(frame=hit+4)),
   ('integration','MK2_CPU_PAIR_FIELD','yraw','00000000',dict(frame=hit+4)),
   ('separation','MK2_CPU_PAIR_FIELD','x','1',dict(frame=limit)),
   ('push counter','MK2_CPU_PAIR_FIELD','suppression','3',dict(frame=limit)),
   ('damage kind','MK2_CPU_OVERLAP_HEALTH','a10','00000005',dict(frame=hit)),
   ('block input','MK2_KNIFE_PAIR_BLOCK','controls','FFFFFFDF',dict(frame=hit,decision=2)),
   ('block branch','MK2_KNIFE_PAIR_BLOCK','decision','1',dict(frame=hit,decision=0)),
   ('own cleanup','MK2_CPU_OVERLAP_EVENT','body','005E',dict(frame=end,kind='regain')),
   ('victim fling','MK2_CPU_OVERLAP_EVENT','a2','00008000',dict(frame=hit,kind='fling')),
   ('native choice threshold','MK2_CPU_CHOICE_EVENT','a0','000000FB',dict(frame=start,kind='first_call')),
   ('native choice owner','MK2_CPU_CHOICE_EVENT','owner','01000000',dict(frame=start,kind='ball')),
  ]
  for label,tag,key,value,where in checks:
   reject('roll'+str(i+1)+' '+label,mutate(text,tag,key,value,where),lambda bad:gate(bad,guest,payload,i))
  line=next(s+'\n'for s in text.splitlines()if s.startswith('MK2_CPU_PAIR_FIELD ')and f'frame={end+31} 'in s)
  reject('roll'+str(i+1)+' missing subsequent callback',text.replace(line,'',1),lambda bad:gate(bad,guest,payload,i))
  need(gate(text,guest,payload,i)==phase,'Whole real roll restored after every fault')
 for pair in pairs:
  cycle=pair['cycle'];start=pair['start'];release=pair['release']
  checks=[
   ('pose','MK2_CPU_PAIR_FIELD','pose','00000000',dict(cycle=cycle,frame=start+10)),
   ('victim offset','MK2_CPU_PAIR_FIELD','vxpos','0',dict(cycle=cycle,frame=start+10)),
   ('grip state','MK2_CPU_PAIR_FIELD','vaction','0',dict(cycle=cycle,frame=start+10)),
   ('pulse damage','MK2_CPU_PAIR_EVENT','a10','00000001',dict(cycle=cycle,kind='damage')),
   ('release fling','MK2_CPU_PAIR_EVENT','a2','00004000',dict(cycle=cycle,kind='fling')),
   ('own handoff','MK2_CPU_PAIR_OWN_REGAIN','body','005E',dict(cycle=cycle)),
  ]
  for label,tag,key,value,where in checks:
   fn=lambda bad:need(state.original.pair.verify_pair(bad,'kano',cycle,guest)['passed'],'Entire original paired action rejected')
   reject('choke'+str(cycle)+' '+label,mutate(text,tag,key,value,where),fn)
  need(state.original.pair.verify_pair(text,'kano',cycle,guest)==pair,'Whole real pair restored after every fault')
 reject('real round reset refill',mutate(text,'MK2_CPU_ROUND_HEALTH','after','160',dict(mode=6,slot=1)),lambda bad:state.verify(bad,guest))
 return dict(passed=True,wholeNativeStateHealthAndChoices=inventory,allActualRollPhases=phases,declaredCompletedPairs=pairs,
             actualNativeMotionFaultsRejected=faults,allActualChoicesChecked=True,otherPairEntriesNotClaimedComplete=True,
             sourceAudioAcceptance=False,sourceRasterAcceptance=False,fullPortAcceptance=False)


def finish(carrier):
 need(not OUT.exists()and not process.census(),'Fresh same-terminal host proof without replay')
 terminal=json.loads((CASE/'native_terminal.json').read_text());failure=json.loads((CASE/'failure.json').read_text())
 need(terminal['nativeExit']==carrier['code']==0 and not terminal['hostDecodeErrors']and not carrier['decode_errors'],
      'Actual retained job terminal with every transport decoded')
 need(failure['passed']is False,'Original executed fixed-trajectory rejection remains false')
 pins=dict(carrier['pins']);need(all(sha(p)==h for p,h in pins.items()),'All actually executed sources intact')
 proof=verify(carrier)
 for p in(Path(__file__),Path(original.__file__),Path(state.__file__),Path(candidate.__file__),Path(process.__file__),*CASE.rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All source and immutable native evidence still intact')
 result=dict(passed=True,candidate=candidate.NAME,nativeTerminal=terminal,proof=proof,inputHashes=pins,
             preservedOriginalFailure=str(CASE/'failure.json'),newNativeBoots=0,newBuilds=0,newZIPs=0,newRawMedia=0,
             previousGoalTurnClassification='no progress: acknowledgement only; retained live host carrier revalidated',
             thisGoalTurnClassification='progress: both actual current CPU rolls and complete paired actions checked against native source and full match ledger',
             remaining=carrier['remaining'],goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(dict(passed=True,rolls=len(proof['allActualRollPhases']),pairs=len(proof['declaredCompletedPairs']),
                       actualFaultsRejected=len(proof['actualNativeMotionFaultsRejected']),newNativeBoots=0)),flush=True)
 return result
