"""Original native guard/crouch/HP timing comparison, with specific corruptions.
Same physical sequences on true Kano/Sonya/Liu/Sub-Zero IDs, both human slots.
Accepted no-activation diagnostics are never counted as successful attacks.
This bounded comparison does not certify all gameplay, art, sound or endings.
"""
import argparse,json,re,struct
from pathlib import Path
import verify_current_guard_uppercut_comparison_v2217 as check
ROOT=check.ROOT

def need(ok,message):
 if not ok:raise ValueError(message)

def physical_handler(log,meta):
 terminal,fields,by=check.verify_context(log,meta)
 handlers=check.rows(log,'HANDLER')
 punch=[h for h in handlers if h['entry']==0xff8300c0]
 if terminal['entry']>0:
  state=check.verify_log(log,meta['move'],meta['side'])
  need(len(punch)==1 and punch[0]['frame']==terminal['entry'],'One actual native crouch HP dispatch at the uppercut entry')
  hp=0x10 if meta['side']==1 else 0x1000;block=hp*2
  need(not punch[0]['hardware0']&hp and punch[0]['hardware0']&block,'Actual native HP word is active and Block released at dispatch')
 else:
  check.verify_no_activation(log,meta,terminal,fields,by)
  need(not punch,'Unactivated diagnostic never fabricates native HP dispatch')
 exits=[h for h in handlers if h['entry']==0xff8304d0]
 if meta['profile']=='guard_release':
  need(exits and exits[0]['frame']==terminal['command']+130,'Observed original guard-to-crouch completion ten fields after release')
  need(terminal['entry']==-1 if meta['lead']==6 else terminal['entry']==terminal['command']+120+meta['lead']+2,'Actual early/later HP transition result, not a presumed activation')
 return dict(actualEntry=terminal['entry'],command=terminal['command'],
  guardToCrouchField=exits[0]['frame']if exits else None,
  dispatchWord=punch[0]['hardware0']if punch else None,
  nativeUppercutAccepted=terminal['entry']>0,pairedFields=len(fields))

def verify():
 pins={};cases={};negative=[];guest=check.current_source.expected()[0]
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for address,length in ((0xff82f9f0,6),(0xff8304d0,4),(0xff8322e0,4),(0xff830120,6)):
  at=(address-0xff800000)//8
  need(guest[at:at+length]==original[at:at+length],'Original actual guard exit/crouch table/HP route unchanged')
 need(struct.unpack_from('<I',original,(0xff8322e0-0xff800000)//8)[0]==0xff8300c0,'Original crouch HP table target')
 for fighter in ('kano','sonya','liu','subzero'):
  for side in (1,2):
   for version,profile,lead in ((2215,'neutral',6),(2215,'guard_release',6),(2219,'guard_release',12),(2219,'guard_release',24)):
    case=f'{fighter}_p{side}_{profile}_lead{lead}'
    path=ROOT/f'audit_v2221_current_{case}_checked/report.json';proof=json.loads(path.read_text())
    need(proof['passed']and proof['boundedGuardTransitionContextAccepted']and not proof['fullPortAcceptance'],'Full independent actual comparison context')
    for file,wanted in proof['inputHashes'].items():
     if file in pins:need(pins[file]==wanted,'Consistent actual dependency graph')
     else:need(check.current_launch.sha(file)==wanted,'Changed accepted source/capture '+file)
     pins[file]=wanted
    pins[str(path)]=check.current_launch.sha(path)
    folder=ROOT/f'audit_v{version}_current_{case}';meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
    log=(folder/'run.log').read_text(encoding='utf-8-sig');actual=physical_handler(log,meta)
    need(actual['nativeUppercutAccepted']==proof['nativeUppercutAccepted'],'Actual handler/physical word agrees with full damage/recovery acceptance')
    if actual['nativeUppercutAccepted']:need(proof['nativeContactDamage']==40 and proof['fullOwnedRecoveryAndFollowupAccepted'],'Actual full native40damage/recovery/walk/jump/punch follow-up')
    need(actual['nativeUppercutAccepted']==(profile=='neutral'or lead>=12),'Same exact tested timing outcome for native and added characters')
    cases[case]=dict(report=str(path),**actual,nativeContactDamage=proof['nativeContactDamage'])
    if fighter not in('kano','sonya')or side!=1 or profile!='guard_release'or lead!=12:continue
    lines=log.splitlines(keepends=True)
    handler=next(i for i,line in enumerate(lines)if line.startswith('MK2_HSPECIAL_HANDLER ')and'entry=FF8300C0 'in line)
    field=next(i for i,line in enumerate(lines)if line.startswith('MK2_HSPECIAL_FIELD ')and f'slot={side} 'in line)
    hp=next(i for i,line in enumerate(lines)if line.startswith('MK2_HSPECIAL_INPUT ')and'button=High_Punch'in line and int(re.search(r'frame=(\d+)',line)[1])>=actual['command'])
    health=next(i for i,line in enumerate(lines)if line.startswith('MK2_HSPECIAL_HEALTH ')and'pc=FF836700'in line)
    for name,index,kind,message in (
     ('wrong_handler_pc',handler,'pc','Own actual native instruction handler provenance'),
     ('wrong_dispatch_hp_word',handler,'word','Actual native HP word'),
     ('proxy_field_id',field,'id','True actual human IDs'),
     ('missing_paired_field',field,'remove','All consecutive physical paired fields'),
     ('missing_real_hp',hp,'remove','Every exact physical guard/release/HP command field'),
     ('wrong_actual_damage',health,'damage','Actual collision stores explain')):
      changed=list(lines)
      if kind=='remove':changed.pop(index)
      elif kind=='pc':changed[index]=changed[index].replace('pc=FF8300D0','pc=FF870DC0')
      elif kind=='word':changed[index]=re.sub(r'hardware0=[0-9A-F]+','hardware0=FFFF',changed[index])
      elif kind=='id':changed[index]=re.sub(r' id=\d+',' id=1',changed[index],count=1)
      else:changed[index]=re.sub(r' after=(\d+)',lambda m:' after='+str(int(m[1])+1),changed[index],count=1)
      try:physical_handler(''.join(changed),meta)
      except ValueError as error:
       need(message in str(error),'Specific native invariant, not incidental parser failure '+str(error));negative.append(dict(case=case,name=name,rejectedBy=str(error)))
      else:raise ValueError('Corrupted actual guard transition accepted '+name)
    need(physical_handler(log,meta)==actual,'Final unmodified actual guard transition control passes')
 failed_path=ROOT/'audit_v2216_current_kano_p1_neutral_lead6_checked/report.json'
 failed=json.loads(failed_path.read_text());need(not failed['passed']and 'exact unassisted scope'in failed['error'],'Preserve superseded parser failure')
 pins[str(failed_path)]=check.current_launch.sha(failed_path)
 pins[str(ROOT/'tools/verify_current_guard_uppercut_comparison_v2214.py')]=check.current_launch.sha(ROOT/'tools/verify_current_guard_uppercut_comparison_v2214.py')
 pins[str(Path(__file__).resolve())]=check.current_launch.sha(__file__);check.current_launch.module_pins(pins)
 return dict(passed=True,cases=cases,acceptedActualUppercuts=sum(c['nativeUppercutAccepted']for c in cases.values()),
  acceptedNativeNoActivationDiagnostics=sum(not c['nativeUppercutAccepted']for c in cases.values()),
  specificCounterexamplesRejected=len(negative),negative=negative,inputHashes=pins,
  originalGuardCrouchHPRouteUnchanged=True,gameBytesChanged=False,fullPortAcceptance=False,
  conclusion='Every tested true character/slot fails the six-field post-guard HP sequence and succeeds with fresh HP after12or24fields. Original guard completion occurs ten fields after release. This demonstrates a physical command phase error, not a custom-ID-specific uppercut defect in these cases.',scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 need(not args.output.exists(),'Immutable native comparison aggregate')
 report=verify();args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes','negative')},indent=2),flush=True)
