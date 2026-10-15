"""Source-bound original crouch exit and measured Shao damage in that state.
No guessed walk-state label, per-hit CPU attack name or universal balance claim.
No guest, controller, source program or captured byte is modified.
"""
import argparse,json,struct,copy
from pathlib import Path
import verify_current_shao_opening_escape_boss_ledger_v2431 as ledger
from analyze_current_shao_opening_damage_states_v2408 import own_damage
ROOT=ledger.ROOT;launch=ledger.launch

def need(ok,label):
 if not ok:raise ValueError(label)

def source_check(guest,original):
 def data(raw,a,b):return raw[(a-0xff800000)//8:(b-0xff800000)//8]
 ranges=((0xff82f9f0,0xff82fe00),(0xff831fc0,0xff832040),
  (0xff836f70,0xff8370e0),(0xff83c430,0xff83c5b0),(0xff834830,0xff834860))
 for a,b in ranges:need(data(guest,a,b)==data(original,a,b),'Original crouch exit/physical direction table/reverse animation/ready path unchanged')
 expected={0xff831fc0:(0xb7a0,0x0100,0x8600,0x03e0,0x0b80,0xfff0,0xffff),
  0xff82fbf0:(0x0d3f,0x023b,0x1fc0,0xcbe1),
  0xff82fd70:(0x09c1,0x0301,0xb02d,0x01f0,0x18a9,0x1841,0xc080,0xc430,0xff83),
  0xff834830:(0xc080,0x1350,0xff86)}
 for a,words in expected.items():
  need(data(original,a,a+len(words)*16)==struct.pack('<'+'H'*len(words),*words),'Exact original physical Down test/301 write/animation5 reverse/ready signatures')
 return dict(originalUnchangedRanges=[dict(first=a,lastExclusive=b)for a,b in ranges],
  native301WriterPC=0xff82fdb0,reverseAnimationIndex=5,reverseFrameSleepFields=2,
  originalReadyTarget=0xff861350)

def check_entries(rows,identity):
 entries=[r for r in rows if r['tag']=='BOSS_ACTION'and r['stage']==16 and r['after']==0x301]
 need(entries,'Actual current Shao crouch exits')
 for r in entries:
  need(r['before']==0x302 and r['pc']==0xff82fdb0 and r['a1']==0x301,
   'Every actual301 assignment follows original crouch302 retirement instruction')
  need(r['id']==r['roster']==identity and r['actor']==r['owner']==r['a8']and r['main']==r['a13'],
   'Native crouch exit keeps true own actor/Main/ID, never a proxy')
 return entries

def verify():
 pins={};path=ROOT/'audit_v2436_current_shao_opening_escape_progress/report.json'
 progress=json.loads(path.read_text());need(progress['passed']and not progress['fullPortAcceptance'],'Accepted actual source-bound physical campaigns')
 for file,wanted in progress['inputHashes'].items():
  need(launch.sha(file)==wanted,'Unchanged actual graph '+file);pins[file]=wanted
 pins[str(path)]=launch.sha(path)
 guest=ledger.native.current_source.expected()[0];original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 source=source_check(guest,original);source_negatives=[]
 for label,address in(('changed_native301_word',0xff82fd80),('changed_reverse_animation',0xff82fdb0),('changed_original_ready',0xff834840)):
  changed=bytearray(guest);changed[(address-0xff800000)//8]^=1
  try:source_check(changed,original)
  except ValueError as error:
   need('Original crouch exit'in str(error),'Specific source invariant');source_negatives.append(label)
  else:raise ValueError('Changed native crouch code accepted')
 cases={};negatives=[]
 for case,(fighter,side,capture,_)in ledger.CASES.items():
  identity=17 if fighter=='kano'else 18
  need((ROOT/capture/'guest_maincpu.bin').read_bytes()==guest,'Every actual initialized guest equals independent source')
  rows=ledger.native.parse((ROOT/capture/'run.log').read_text(encoding='utf-8-sig'),side,fighter)
  ledger.check(rows,identity,side);entries=check_entries(rows,identity)
  for label,key,value,expected in(('wrong_native_exit_PC','pc',0xff83c340,'Every actual301'),
   ('wrong_prior_native_state','before',0x303,'Every actual301'),
   ('proxy_crouch_exit_ID','id',1,'Native crouch exit keeps')):
   changed=copy.deepcopy(rows);index=next(i for i,r in enumerate(changed)if r['event']==entries[0]['event']);changed[index][key]=value
   try:check_entries(changed,identity)
   except ValueError as error:
    need(expected in str(error),'Specific actual exit invariant');negatives.append(dict(case=case,name=label))
   else:raise ValueError('Changed actual native crouch exit accepted')
  need(check_entries(rows,identity)==entries,'Untouched actual native exit control')
  incoming=own_damage(rows,side);in_exit=[r for r in incoming if r['actionAtOwnDamage']==0x301]
  need(sum(r['damage']for r in in_exit)==progress['cases'][case]['actualShaoIncomingDamageByActualAction']['nativeAction_0301']['damage'],'Ordered original damage during actual301 reconciles')
  cases[case]=dict(actualNativeCrouchExitAssignments=len(entries),actualExitDamageStores=len(in_exit),
   actualExitDamage=sum(r['damage']for r in in_exit),nativeExitAssignments=entries,
   scope='Measured original native crouch exit; whether an Up pulse spans this retirement must be compared in real cold stock/addition controls')
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,source=source,cases=cases,rejectedSpecificSourceCounterexamples=source_negatives,
  rejectedSpecificActualExitCounterexamples=negatives,inputHashes=pins,gameOrCaptureModified=False,
  fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 need(not a.output.exists(),'Immutable native crouch exit diagnosis')
 r=verify();a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({case:{k:v for k,v in row.items()if k!='nativeExitAssignments'}for case,row in r['cases'].items()},indent=2),flush=True)
