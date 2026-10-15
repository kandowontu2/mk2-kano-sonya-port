"""Preserve6488 rejection; qualify all actual callbacks before native exit.

The physical driver requests exit in register_frame at ready+600. Thus the
ready callback through terminal-1 comprises600 full post-frame callbacks.
Include the first joined callback too; invent no terminal post-frame state.
"""
import argparse,gzip,inspect,json,re,subprocess,traceback
from pathlib import Path
import capture_current_challenger_v6487 as executed
ROOT,need,sha,rows=executed.ROOT,executed.need,executed.sha,executed.rows

def bindings():
 source=inspect.getsource(executed.gate)
 changes={
  "range(events['match']+1,events['terminal']+1)":"range(events['match'],events['terminal'])",
  "len(tail)==601":"len(tail)==600",
  "ordinaryTailFieldsPerSlot=601":"ordinaryTailFieldsPerSlot=600",
 }
 for before,after in changes.items():need(source.count(before)==1,'Only actual stop-callback boundary corrected '+before);source=source.replace(before,after,1)
 scope=dict(executed.__dict__)
 exec(compile(source,__file__+'::whole_original_gate_actual_callback_boundary','exec'),scope)
 return scope['gate']

gate=bindings()

def qualify(fighter,side):
 folder=ROOT/f'audit_v6488_current_challenger_{fighter}_p{side}_ram'
 out=ROOT/f'audit_v6490_current_challenger_{fighter}_p{side}_checked'
 need(not out.exists() and not executed.prior.census(),'Fresh proof, same terminal capture; no native replay')
 original=folder/'report.json';report=json.loads(original.read_text())
 need(not report['passed'] and report['error']=="ValueError('No omitted post-join native actor callback')" and
      report['nativeExit']==0 and not report['observationErrors'] and len(report['actualGuestGFXProofs'])==2 and
      not(folder/'stderr.log').read_text().strip(),'Exactly preserved failed exit-boundary assumption; actual native run successful')
 pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every actually executed input intact')
 driver=(ROOT/'mk2ks_current_challenger_v6486.lua').read_text()
 need(driver.count('if age==600 then manager.machine:exit()end')==1 and driver.index('if age==600 then manager.machine:exit()end')<driver.index('emu.register_frame_done(function()'),
      'Actual stop requests exit during pre-frame controller, before later post-frame callback')
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as f:text=f.read()
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),'No actual runtime error')
 good=gate(text,fighter,side);indexed={(int(q['frame']),int(q['slot'])) for q in rows(text,'MK2_CR_FIELD')}
 need(all((good['events']['terminal'],n) not in indexed and (good['events']['terminal']-1,n) in indexed for n in (1,2)),
      'Both final actual post callbacks exist; no invented callback after native exit request')
 faults=[]
 for label,tag,key,value in [('wrong real ID','MK2_CR_FIELD','id','1'),('wrong Main owner','MK2_CR_FIELD','owner','00000000'),
                           ('false CPU role','MK2_JR_JOIN','otherState','1'),('false highlight','MK2_JR_HIGHLIGHT','roster','1'),
                           ('false ready','MK2_JR_RESULT','ready','-1'),('incomplete native boundary','MK2_JR_RESULT','terminal','1')]:
  selected=next(l for l in text.splitlines() if l.startswith(tag+' ') and (tag!='MK2_CR_FIELD' or f'slot={side} ' in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>=good['events']['match']))
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1);need(changed!=selected,'Effective actual challenger fault')
  try:gate(text.replace(selected,changed,1),fighter,side)
  except(ValueError,KeyError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual false challenger evidence admitted '+label)
  need(gate(text,fighter,side)==good,'Whole actual positive restored after fault')
 for n in (1,2):
  selected=next(l for l in text.splitlines() if l.startswith('MK2_CR_FIELD ') and f'slot={n} ' in l and f"frame={good['events']['terminal']-1} " in l)
  try:gate(text.replace(selected+'\n','',1),fighter,side)
  except(ValueError,KeyError) as error:faults.append(dict(kind='missing final actual slot '+str(n),rejectedBy=str(error)))
  else:raise ValueError('Missing actual final callback admitted')
  need(gate(text,fighter,side)==good,'All original actual fields restored')
 for p in (*folder.rglob('*'),Path(__file__),Path(executed.__file__)):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,candidate=report['candidate'],executableSHA256=report['executableSHA256'],payloadSHA256=report['payloadSHA256'],
             nativeExit=0,nativeIdentity=report['nativeIdentity'],actualCurrentChallenger=good,actualFaultsRejected=faults,
             actualGuestGFXProofs=report['actualGuestGFXProofs'],wholeActualRGBDigestsRetained=report['actualRGBDigests'],
             preservedExecutedRejection=str(original),noInventedTerminalPostFrame=True,firstJoinedPostFrameIncluded=True,
             inputHashes=pins,newNativeBoots=0,newBuilds=0,newRawMedia=0,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Exact terminal proof compression')
 print(json.dumps(dict(passed=True,fighter=fighter,side=side,actualJoinedFields=good['joinedActorFields'],ordinaryFieldsPerSlot=600,actualFaultsRejected=len(faults))),flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));a=parser.parse_args();qualify(a.fighter,a.side)
