"""Specific in-memory corruption checks for all four clean uppercut render cases.
Never changes game state, source capture files or accepted reports. Only a matching
ValueError from the intended acceptance invariant counts as a rejected case.
"""
import argparse,copy,contextlib,io,json
from pathlib import Path
from unittest.mock import patch
import verify_current_human_uppercut_full_render_v2158 as model
import verify_current_interrupt_v1870 as launch
ROOT=model.ROOT
CASES=('kano_p1','kano_p2','sonya_p1','sonya_p2')
MUTATIONS=(
 ('wrong_origin','FLOOR_BEGIN','origin',1,'Actual native activation'),
 ('missing_scanout_count','FLOOR_RESULT','snapshots',-1,'Every consecutive special-phase'),
 ('proxy_roster','FLOOR_STATE','roster1',1,'True physical fighters'),
 ('wrong_body_owner','FLOOR_QUEUE','owner',16,'Actual true-ID physical draw owner'),
 ('wrong_cache_source','FLOOR_QUEUE_PART','source',16,'Every cached multipart piece'),
 ('shifted_floor','FLOOR_QUEUE_TRANSFORM','floor',1,'Original character-owned floor anchors'),
 ('shifted_camera','FLOOR_QUEUE_TRANSFORM','camera',1,'Exact native world/camera/cache/flip/display'),
 ('wrong_dispatch_slot','FLOOR_QUEUE_DISPATCH','slot',1,'Published actor/process dispatch binding'),
 ('shifted_dma','FLOOR_DMA','x',1,'Every physical coordinate/palette bank'),
 ('wrong_clip_viewport','FLOOR_CANDIDATE','clipHigh',1,'Actual original native viewport bounds'),
 ('wrong_candidate_cursor','FLOOR_CANDIDATE','row',112,'Exact native clipping caller/cache iterator'),
 ('wrong_candidate_size','FLOOR_CANDIDATE','size',1,'Pre-clip source matches'),
)
def run(case):
 folder=ROOT/f'audit_v2159_current_uppercut_{case}_full_render'
 positive=ROOT/f'audit_v2160_current_uppercut_{case}_full_render_checked/report.json'
 report=json.loads(positive.read_text());assert report['passed']and report['interPassEraseAcceptance']
 pins=dict(report['inputHashes'])
 for file,wanted in pins.items():assert launch.sha(file)==wanted,'Changed accepted input '+file
 pins[str(positive)]=launch.sha(positive)
 original=model.raster.data(folder);groups=original[0]
 outcomes=[]
 for name,tag,key,delta,message in MUTATIONS:
  changed=copy.deepcopy(original)
  # Geometry/control records are duplicated; mutate the actual authoritative
  # first physical record, not an absent synthetic row or accidental KeyError.
  rows=changed[0][tag]
  if tag=='FLOOR_DMA':row=next(r for r in rows if r['slot']in(1,2)and r['command']&15==2)
  else:row=rows[0]
  before=row[key];row[key]+=delta
  try:
   with patch.object(model.raster,'data',return_value=changed),contextlib.redirect_stdout(io.StringIO()):
    model.verify(folder)
  except ValueError as error:
   assert message in str(error),f'{name}: wrong failure {error!r}'
   outcomes.append(dict(name=name,record=tag,key=key,before=before,after=row[key],rejectedBy=str(error)))
  else:raise AssertionError('Accepted wrong actual data '+name)
  print(case+' rejects '+name,flush=True)
 # A genuine unmodified replay must still succeed, not merely the malformed inputs fail.
 control=model.verify(folder);assert control['passed']and control['interPassEraseAcceptance']
 pins.update(control['inputHashes']);pins[str(Path(__file__).resolve())]=launch.sha(__file__)
 launch.module_pins(pins)
 return dict(passed=True,case=case,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,
  unchangedDefaultdictPreserved=True,finalUnmockedFullReplayPassed=True,inputHashes=pins,
  fullPortAcceptance=False,scope=__doc__)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('case',choices=CASES);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 assert not args.output.exists(),'Immutable counterexample evidence'
 try:report=run(args.case)
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 args.output.mkdir();(args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','outcomes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
