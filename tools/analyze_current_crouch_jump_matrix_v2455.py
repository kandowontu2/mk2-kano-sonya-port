"""Cold native crouch-exit/Up comparison, both slots, with deliberately failing controls.
Not all-arena art/audio, CPU balance, complete campaign or full-port acceptance.
"""
import argparse,json,re
from pathlib import Path
import verify_current_crouch_jump_comparison_v2452 as v
ROOT=v.ROOT
def need(ok,label):
 if not ok:raise ValueError(label)
def changed_line(lines,index,key,value):
 out=lines[:]
 out[index],count=re.subn(r'(?<!\w)'+key+r'=\S+',key+'='+str(value),out[index],count=1)
 need(count==1,'Exact requested counterexample field')
 return '\n'.join(out)+'\n'
def reject(text,meta,label,wanted):
 try:v.verify_log(text,meta)
 except ValueError as error:
  need(str(error)==wanted,'Specific counterexample rejection '+label+': '+str(error))
  return dict(label=label,rejected=True,reason=str(error))
 raise ValueError('Invalid counterexample accepted: '+label)
def case(name):
 folder=ROOT/('audit_v2453_current_'+name)
 checked=ROOT/('audit_v2454_current_'+name+'_checked/report.json')
 proof=json.loads(checked.read_text());need(proof['passed'],'Actual complete case accepted '+name)
 pins={str(checked):v.launch.sha(checked)}
 for file,digest in proof['inputHashes'].items():
  need(v.launch.sha(file)==digest,'Current actual proof graph '+file);pins[file]=digest
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 text=(folder/'run.log').read_text(encoding='utf-8-sig');lines=text.splitlines()
 result=v.verify_log(text,meta);rows=v.check.rows
 terminal=rows(text,'RESULT')[0];command=terminal['command'];follow=terminal['followup'];side=meta['side']
 def find(tag,**values):
  return next(i for i,line in enumerate(lines)if line.startswith('MK2_HSPECIAL_'+tag+' ')and all(re.search(r'(?<!\w)'+k+'='+str(val)+r'(?:\s|$)',line)for k,val in values.items()))
 negatives=[]
 up=find('INPUT',frame=command+120+meta['lead'],slot=side,button='Up')
 for label,mutated in [('missing first Up',lines[:up]+lines[up+1:]),('conflicting Down during Up',lines+[lines[up].replace('button=Up','button=Down')])]:
  negatives.append(reject('\n'.join(mutated)+'\n',meta,label,'Exact physical Down release and Up/direction duration; no conflicting Down/Block/HP'))
 negatives.append(reject(changed_line(lines,up,'slot',3-side),meta,'wrong input owner','Exact physical Down release and Up/direction duration; no conflicting Down/Block/HP'))
 field=find('FIELD',frame=command+1,slot=side)
 negatives.append(reject(changed_line(lines,field,'id',1 if meta['move']!='jump_liu'else 17),meta,'proxy ID','True selected IDs and stable native Main/actor, never proxies'))
 negatives.append(reject('\n'.join(lines[:field]+lines[field+1:])+'\n',meta,'missing native field','Every consecutive paired native field'))
 negatives.append(reject(changed_line(lines,field,'floor',999),meta,'wrong ground floor','Stable actual character-owned floor and native health'))
 event=find('HANDLER',entry='FF82FD70')
 negatives.append(reject(changed_line(lines,event,'pc','FF82FD90'),meta,'wrong actual native PC','Own actual native instruction/ID/Main/register provenance'))
 without_exit=[line for line in lines if not(line.startswith('MK2_HSPECIAL_HANDLER ')and 'entry=FF82FD70 'in line)]
 negatives.append(reject('\n'.join(without_exit)+'\n',meta,'missing native crouch exit','Observed original302 to301 crouch-exit retirement'))
 final=find('FIELD',frame=terminal['frame'],slot=side)
 negatives.append(reject(changed_line(lines,final,'vx','00000001'),meta,'unfinished recovery','Both humans retire and finish naturally clean on own floors'))
 walk=find('FIELD',frame=follow+3,slot=side)
 negatives.append(reject(changed_line(lines,walk,'vx','00014000'),meta,'wrong free backwalk velocity','Real native collision-free back walking after crouch/jump'))
 negatives.append(reject(changed_line(lines,field,'writes',1),meta,'guest assistance','Every recorded row exact true comparison scope'))
 if result['nativeCommandJumpObserved']:
  air=next(f for f in rows(text,'FIELD')if f['slot']==side and command<=f['frame']<terminal['recovered']and f['y']<f['floor']and f['vy']!=0)
  index=find('FIELD',frame=air['frame'],slot=side)
  negatives.append(reject(changed_line(lines,index,'action',0x503),meta,'hurt credited as jump','No uppercut/hurt credited as a jump'))
 else:
  index=find('RESULT');negatives.append(reject(changed_line(lines,index,'entry',command+129),meta,'fabricated command activation','No-activation recording never fabricated entry or airborne motion'))
 need(v.verify_log(text,meta)==result,'Untouched final log still accepted')
 return dict(name=name,**result,negativeControls=negatives),pins
def main(output):
 need(not output.exists(),'Immutable matrix analysis')
 source=(ROOT/'mk2ks_crouch_jump_comparison_v2450.lua').read_text().rstrip()+'\n';v.restore_driver(source)
 runner=(ROOT/'tools/run_current_crouch_jump_comparison_v2451.ps1').read_text().rstrip()+'\n'
 old=(ROOT/'tools/run_current_crouch_jump_comparison_v2446.ps1').read_text().rstrip()+'\n'
 need(runner.replace('comparison_v2450','comparison_v2445')==old,'Only declared driver path differs in complete frozen launcher')
 need(v.launch.sha(ROOT/'tools/run_current_crouch_jump_comparison_v2446.ps1')=='26105CD1E5380E31FE0EEDFD6AB424A32ADDDCB56760AE7CDCF0C0C1D0EDC888','Pinned old executed launcher')
 cases=[];pins={}
 for character in('kano','sonya','liu','subzero'):
  for side in(1,2):
   for lead,hold in((0,3),(0,16),(12,3)):
    name=f'{character}_p{side}_crouch_lead{lead}_hold{hold}_away';result,graph=case(name);cases.append(result);pins.update(graph)
 chronology=[]
 for hold in(3,16):
  stem=f'kano_p1_crouch_lead0_hold{hold}'
  old_folder=ROOT/('audit_v2448_current_'+stem);new_folder=ROOT/('audit_v2453_current_'+stem+'_away')
  before=(old_folder/'run.log').read_text(encoding='utf-8-sig');after=(new_folder/'run.log').read_text(encoding='utf-8-sig')
  follow=v.check.rows(before,'RESULT')[0]['followup']
  def prefix(text):return [line for line in text.splitlines()if line.startswith('MK2_HSPECIAL_')and int(re.search(r'frame=(\d+)',line)[1])<follow]
  need(prefix(before)==prefix(after),'Complete original pilot native chronology unchanged before intentional away follow-up')
  pins[str(old_folder/'run.log')]=v.launch.sha(old_folder/'run.log')
  chronology.append(dict(hold=hold,exactOriginalRows=len(prefix(before)),intentionalDifferenceBeginsAtFollowup=follow))
 pins[str(Path(__file__).resolve())]=v.launch.sha(__file__)
 for path in('mk2ks_crouch_jump_comparison_v2445.lua','tools/run_current_crouch_jump_comparison_v2446.ps1','tools/verify_current_crouch_jump_comparison_v2447.py','tools/verify_current_crouch_jump_comparison_v2452.py'):
  pins[str(ROOT/path)]=v.launch.sha(ROOT/path)
 report=dict(passed=True,cases=cases,originalPilotChronology=chronology,negativeControls=sum(len(c['negativeControls'])for c in cases),inputHashes=pins,
  gameModified=False,oldFailedPilotDiscarded=False,fullPortAcceptance=False,scope=__doc__)
 output.mkdir();(output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:val for k,val in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
 for c in cases:print(c['name'],'jump=',c['nativeCommandJumpObserved'],'entry=',c['actualNativeJumpEntry'],'air=',c['actualAirborneCommandFields'],flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();main(args.output)
