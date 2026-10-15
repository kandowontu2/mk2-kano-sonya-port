"""Whole native CPU ball bodies, original donor indices and absolute shadows.

Reuse full6435 FIFO/cache/projection/pre-clip/shadow contracts. Only explicit
Kano mirror identities, actual ball interval and pre-entry physical binds differ.
"""
import argparse,copy,datetime,gzip,inspect,json,re,struct,subprocess,sys,traceback
from pathlib import Path
import capture_current_cpu_ball_render_v6452 as capture
import verify_current_cpu_compound_render_v6435 as original
from current_cpu_ball_context_v6451 import bindings
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6455_current_cpu_ball_render_checked'
ring=original.ring


def adapted(function,changes):
 source=inspect.getsource(function)
 for before,after in changes.items():
  need(source.count(before)==1,'Only explicit finite ball body/shadow context differs '+before)
  source=source.replace(before,after,1)
 scope=dict(function.__globals__,capture=capture,CASE=CASE,bindings=bindings)
 exec(compile(source,__file__+'::whole_original_'+function.__name__+'_ball_context','exec'),scope)
 return scope[function.__name__]


native_gate=adapted(original.native_gate,{
 'block=source[first:last]':"""block=source[first:last]
 need(block.count('(human if s==1 else 18)')==2 and block.count('(134 if s==1 and human==17 else 135)')==2,
      'Both original FIFO/DMA identity and anchor checks retain exact explicit Kano mirror context')
 block=block.replace('(human if s==1 else 18)','(human)').replace('(134 if s==1 and human==17 else 135)','(134)')""",
 "assert r['mode']==2 and":"assert r['mode']==(7 if r['frame']==timeline['start']-1 else 2) and",
 '(17 if s==1 else 18)':'(17)',
 "physical=capture.compound.square.P.rows(text,'FIELD')":'physical=bindings(text)',
 "frames=set(range(timeline['leg']['start']-2,timeline['ordinaryContinuation']['lastObservedTail']+1))":
 "frames=set(range(timeline['start']-1,timeline['victimReady']+31))",
 '{1:17,2:18}':'{1:17,2:17}',
})
shadow_gate=adapted(original.shadow_gate,{
 '{(1,17),(2,18)}':'{(1,17),(2,17)}',
 "physical={r['frame']:r for r in capture.compound.square.P.rows(text,'FIELD')}":"physical={r['frame']:r for r in bindings(text)}",
 '(17 if slot==1 else 18)':'(17)',
 '(134 if slot==1 else 135)':'(134)',
 'for this finite CPU compound':'for this finite CPU ball mirror',
})


def visible_ball(groups,records,payload):
 by={r['frame']:r for r in records}
 need(all(r['body'][str(s)]['pixels']>0 for r in records for s in(1,2)),
      'Both actual native body masks remain visible in every complete ball/cleanup screen')
 poses=struct.unpack_from('<11I',payload,(0xff004010-0xfe800000)//8)
 executed={q['pose']for q in groups['FLOOR_QUEUE']if q['slot']==2 and q['frame']+1 in by and by[q['frame']+1]['body']['2']['pixels']>0}
 need(set(poses[1:8])<=executed,'Every original seven-phase roll pose actually reaches a visible modeled native screen')
 return dict(allSevenOriginalRollPosesVisible=True,bothBodyMasksVisibleEveryScreen=True,
             minimumBodyPixels={str(s):min(r['body'][str(s)]['pixels']for r in records)for s in(1,2)})


def main(preflight=False):
 need(not OUT.exists(),'Fresh current ball body/shadow acceptance')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(meta['passed']and terminal['naturalTerminal']and terminal['exitCode']==meta['nativeExit']==0 and not terminal['observationErrors'],
      'Same actual native process naturally terminal without warning/error waiver')
 need(meta['originalWholePhysicalTrajectoryUnchanged']and not capture.original.terminal.process_tools.census(),
      'Whole6293 original controls/state/HP/RNG identical; no extra replay')
 pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All executed/current inputs unchanged')
 guest,_,scene,_,extra=capture.init_model();pins.update(extra)
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 groups,buffers=ring.observations(text,scene.graphics)
 records=json.loads((CASE/'continuous_scene_records.json').read_text());timeline=meta['independentSemantics']
 prior=ROOT/'audit_v6299_current_kano_cpu_ball_checked/report.json'
 need(timeline==json.loads(prior.read_text())['case']and [r['frame']for r in records]==list(range(1814,1919)),
      'Entire original ball phase plus every pre-entry/full-body/recovery/thirty-field screen')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff801070,0xff8017b0),(0xff804000,0xff804470)):
  a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
  need(guest[a:b]==stock[a:b],'Whole original eligibility/body/projection/publication kernels')
 positive=native_gate(groups,records,text,guest,scene.payload,timeline)
 shadow=shadow_gate(groups,buffers,text,guest,scene.payload)
 donor=original.donor_art(groups,scene.payload,scene.graphics,pins)
 visible=visible_ball(groups,records,scene.payload)
 if preflight:
  print(json.dumps(dict(preflightPassed=True,positive=positive,shadow=shadow,donor=donor,visible=visible)),flush=True);return
 faults=[];check=lambda value:native_gate(value,records,text,guest,scene.payload,timeline)
 for label,tag,key,delta in[
  ('ground anchor shifted','FLOOR_QUEUE_TRANSFORM','floor',1),('camera shifted','FLOOR_QUEUE_TRANSFORM','camera',65536),
  ('body source shifted','FLOOR_QUEUE_PART','source',1),('body offset shifted','FLOOR_QUEUE_PART','dy',1),
  ('DMA source shifted','FLOOR_DMA','source',1),('native body hidden','FLOOR_QUEUE_DISPATCH','actor',1)]:
  bad=copy.deepcopy(groups);bad[tag][0][key]+=delta
  try:check(bad)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(label=label,rejectedBy=str(e)))
  else:raise ValueError('Actual ball body/DMA fault admitted '+label)
 for label,tag,key,value in[
  ('shadow camera','MK2_HPHASE_PROJECTION','b4','00000000'),('shadow floor','MK2_HPHASE_PROJECTION','floor','999'),
  ('shadow eligibility','MK2_HPHASE_SHADOW_BEGIN','body','0002'),('shadow source','MK2_HPHASE_SHADOW_DMA','source','00000001'),
  ('shadow absolute position','MK2_HPHASE_SHADOW_DMA','x','999'),
  ('pre-entry actor proxy','MK2_NAT_CAMPAIGN_BALL_BINDING','id','1')]:
  line=next(s for s in text.splitlines()if s.startswith(tag+' '))
  badline=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1);bad=text.replace(line,badline,1)
  need(bad!=text,'Real actual native shadow/pre-entry record changed')
  try:shadow_gate(groups,buffers,bad,guest,scene.payload)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(label=label,rejectedBy=str(e)))
  else:raise ValueError('Actual ball shadow/native binding fault admitted '+label)
 bad=copy.deepcopy(records);bad[0]['body']['2']['pixels']=0
 try:visible_ball(groups,bad,scene.payload)
 except ValueError as e:faults.append(dict(label='actual CPU body hidden at pre-entry screen',rejectedBy=str(e)))
 else:raise ValueError('Hidden actual body mask admitted')
 need(check(groups)==positive and shadow_gate(groups,buffers,text,guest,scene.payload)==shadow,'Complete native positives restore after all real faults')
 for module in tuple(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p and Path(p).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(p).resolve())]=sha(p)
 for p in(prior,*(p for p in CASE.rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All current/executed/proof bytes remain unchanged')
 result=dict(passed=True,candidate=capture.original.terminal.current.NAME,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             nativeTerminal=terminal,wholeOriginalBallPhase=timeline,completeContinuousRender=meta['continuousRender'],
             nativeFIFOProjectionArt=positive,ownedNativeFloorShadow=shadow,originalDonorArt=donor,visibleBallPhases=visible,actualFaultsRejected=faults,
             independentRasterSourceSHA256=capture.model.MODEL_SOURCE_SHA256,preEntryPhysicalBindings=len(bindings(text))*2,
             inputHashes=pins,goalStatus='active',fullAudioAcceptance=False,fullPortAcceptance=False,allArenasAccepted=False,
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,
             previousGoalTurnClassification='progress: source-exact compound Sonya audio and complete native channel cleanup qualified',
             thisGoalTurnClassification='progress: actual current CPU ball full art/raster/absolute floor shadows and pre-entry recovery scope qualified')
 OUT.mkdir();p=OUT/'report.json';p.write_text(json.dumps(result,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact finite proof compressed')
 print(json.dumps(dict(passed=True,fields=len(records),pixels=meta['continuousRender']['exactRGBPixels'],
                       shadowCopies=shadow['absoluteGeometryCopies'],faultsRejected=len(faults),donor=donor)),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
