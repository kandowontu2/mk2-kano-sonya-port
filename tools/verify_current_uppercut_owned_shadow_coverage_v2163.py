"""Own-character floor-shadow coverage for each clean uppercut render field.
Extends the source-bound full-scene proof with a one-to-one shadow component
inventory. A stock opponent's shadow cannot stand in for a missing Kano/Sonya
shadow. This is only the four actual Dead Pool human uppercut cases.
"""
import copy,json
from collections import defaultdict
from pathlib import Path
import verify_current_human_uppercut_full_render_v2158 as model
import verify_current_interrupt_v1870 as launch
ROOT=model.ROOT;OUT=ROOT/'audit_v2164_current_uppercut_owned_shadow_coverage'
def need(ok,message):
 if not ok:raise ValueError(message)
def coverage(groups,side,identity):
 queues={(q['frame'],q['slot'],q['part']):q for q in groups['FLOOR_QUEUE']if q['slot']==side}
 need(queues and len(queues)==sum(q['slot']==side for q in groups['FLOOR_QUEUE']),'Unique actual own body components')
 copies=defaultdict(list)
 for row in groups['SHADOW_COMPONENT']:
  need(row['slot']==side and row['id']==identity,'Only the declared own character supplies imported shadows')
  copies[row['frame'],row['slot'],row['component']].append(row)
 need(set(copies)==set(queues),'Every actual own visible body component has its own floor shadow, with no missing or unowned component')
 events=set()
 for key,rows in copies.items():
  q=queues[key]
  for row in rows:
   need(row['actor']==row['owner']==q['actor']==q['owner']and row['main']==q['main']and row['id']==q['id']==identity,'Every shadow copy remains bound to its genuine own physical fighter')
   need(row['cache']==q['cache']and row['row']==q['row']==q['cache']+key[2]*112,'Every own shadow copy comes from the actual native cache component')
   need(row['first_source']==q['source']and row['width']==q['size']&65535 and row['height']==q['size']>>16 and row['command']|0x8002==q['command']>>16,'Every own shadow copy uses its exact rendered body source')
   need(row['x']==q['x']and row['y']==q['y']and row['floor']==q['floor'],'Every own shadow copy retains actual physical position and character floor')
   need(row['event']not in events,'No aliased actual owned shadow events');events.add(row['event'])
 return dict(ownBodyComponents=len(queues),ownShadowCopies=len(events),ownShadowDrawFields=len({key[0]for key in queues}),everyOwnBodyComponentProjected=True)
def verify():
 pins={};cases={}
 for case in ('kano_p1','kano_p2','sonya_p1','sonya_p2'):
  side=int(case[-1]);identity=17 if case.startswith('kano')else 18
  folder=ROOT/f'audit_v2159_current_uppercut_{case}_full_render'
  path=ROOT/f'audit_v2160_current_uppercut_{case}_full_render_checked/report.json'
  positive=json.loads(path.read_text())
  need(positive['passed']and positive['interPassEraseAcceptance']and positive['sourceBoundNativeClippedParts']==0,'Complete current source-exact scene with no clipped body components')
  for file,wanted in positive['inputHashes'].items():
   need(launch.sha(file)==wanted,'Changed current render dependency '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path)
  groups=model.raster.data(folder)[0];checked=coverage(groups,side,identity);outcomes=[]
  for kind,expected in (
   ('missing_component','Every actual own visible body component'),
   ('wrong_owner','genuine own physical fighter'),
   ('wrong_cache','actual native cache component'),
   ('wrong_source','exact rendered body source'),
   ('shifted_physical_floor','actual physical position and character floor')):
   changed=copy.deepcopy(groups);row=changed['SHADOW_COMPONENT'][0]
   if kind=='missing_component':
    key=tuple(row[k]for k in ('frame','slot','component'))
    changed['SHADOW_COMPONENT']=[r for r in changed['SHADOW_COMPONENT']if tuple(r[k]for k in ('frame','slot','component'))!=key]
   elif kind=='wrong_owner':row['owner']+=16
   elif kind=='wrong_cache':row['row']+=112
   elif kind=='wrong_source':row['first_source']+=16
   else:row['floor']+=1
   try:coverage(changed,side,identity)
   except ValueError as error:
    need(expected in str(error),'Specific intended own shadow failure, not incidental exception');outcomes.append(dict(name=kind,rejectedBy=str(error)))
   else:raise ValueError('Incorrect own shadow evidence accepted '+kind)
  need(coverage(groups,side,identity)==checked,'Unchanged actual own-shadow control still passes')
  cases[case]=dict(passed=True,side=side,identity=identity,fullSceneReport=str(path),**checked,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes)
  print(case+' every own body component has its own shadow; five specific corruptions rejected',flush=True)
 pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,cases=cases,totalOwnShadowCopies=sum(c['ownShadowCopies']for c in cases.values()),
  rejectedSpecificCounterexamples=sum(c['rejectedSpecificCounterexamples']for c in cases.values()),
  inputHashes=pins,allMoveArenaGroundShadowAccepted=False,fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Immutable owned-shadow coverage')
 try:report=verify()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
