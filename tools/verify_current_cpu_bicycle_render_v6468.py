"""Whole current CPU Bicycle raster, donor bodies, floor shadows and release push."""
import argparse,copy,datetime,gzip,inspect,json,re,struct,subprocess,sys,traceback
from pathlib import Path
import capture_current_cpu_bicycle_bound_v6471 as capture
import verify_current_cpu_compound_render_v6435 as original
import verify_native_bicycle_release_push_v3337 as push
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6473_current_cpu_bicycle_render_checked'
ring=original.ring


def bindings(text):
 result={}
 for line in text.splitlines():
  if not line.startswith('MK2_CPU_ROUND_FIELD '):continue
  pairs=re.findall(r'(\w+)=([^\s]+)',line);r=dict(pairs)
  need(len(pairs)==len(r),'Unique independent physical round-binding fields')
  frame,slot=int(r['frame']),int(r['slot'])
  if not 2661<=frame<=2798:continue
  need(slot in(1,2)and r['id']==str(17 if slot==1 else 18)and r['ids']=='17,18'and
       r['valid']=='1'and r['writes']=='0'and r['assistance']=='none','Both true physical actors in every pre-entry and recovery callback')
  prefix='v'if slot==1 else'';row=result.setdefault(frame,dict(frame=frame))
  for key in('actor','main','owner','id','floor'):
   name=prefix+key;need(name not in row,'Independent physical role exactly once')
   row[name]=int(r[key],16 if key in('actor','main','owner')else 10)
  need(row[prefix+'actor']==row[prefix+'owner'],'Actual physical Main owns native actor')
 need(set(result)==set(range(2661,2799))and all(len(r)==11 for r in result.values()),
      'Both complete independent round bindings include the two mode7 pre-entry fields')
 return list(result.values())


def adapted(fn,changes):
 source=inspect.getsource(fn)
 for before,after in changes.items():
  need(source.count(before)==1,'Only explicit current Bicycle context differs '+before)
  source=source.replace(before,after,1)
 # Keep the original complete physical parser; it reads supplied text, not
 # the older capture. Only the drawing interval is context-specific.
 scope=dict(fn.__globals__,CASE=CASE,bindings=bindings)
 exec(compile(source,__file__+'::whole_original_'+fn.__name__+'_Bicycle_context','exec'),scope)
 return scope[fn.__name__]


native_gate=adapted(original.native_gate,{
 "assert r['mode']==2 and":"assert r['mode']==(7 if r['frame'] in(2661,2662)else 2) and",
 "physical=capture.compound.square.P.rows(text,'FIELD')":'physical=bindings(text)',
 "frames=set(range(timeline['leg']['start']-2,timeline['ordinaryContinuation']['lastObservedTail']+1))":
 "frames=set(range(timeline['start']-2,timeline['victimReady']+31))",
})
shadow_gate=adapted(original.shadow_gate,{
 'for this finite CPU compound':'for this finite CPU Bicycle',
 "physical={r['frame']:r for r in capture.compound.square.P.rows(text,'FIELD')}":"physical={r['frame']:r for r in bindings(text)}",
})


def visible_bicycle(groups,records):
 by={r['frame']:r for r in records}
 need(all(r['body'][str(s)]['pixels']>0 for r in records for s in(1,2)),
      'Both independently modeled native body masks visible in every complete Bicycle/recovery screen')
 held={s:{q['pose']for q in groups['FLOOR_QUEUE']if q['slot']==s and q['frame']+1 in by and
          by[q['frame']+1]['body'][str(s)]['pixels']>0}for s in(1,2)}
 need((set(capture.phase.INTRO)|set(capture.phase.BIKE_CYCLE))<=held[2],'Every original Bicycle startup/cycling pose reaches visible scanout')
 need(set(capture.phase.VICTIM_POSES)<=held[1],'All six native owned Kano victim poses reach visible scanout')
 return dict(allOriginalStartupAndCyclePosesVisible=True,allSixKanoVictimPosesVisible=True,bothBodiesVisibleEveryScreen=True,
             minimumBodyPixels={str(s):min(r['body'][str(s)]['pixels']for r in records)for s in(1,2)})


def main(preflight=False):
 need(not OUT.exists(),'Fresh immutable current Bicycle qualification')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(meta['passed']and terminal['naturalTerminal']and terminal['exitCode']==meta['nativeExit']==0 and not terminal['observationErrors'],
      'Actual native terminal before host qualification; no warning/error waiver')
 need(meta['wholeEarlierPhysicalTrajectoryIdentical']and not capture.prior.prior.original.previous.terminal.process_tools.census(),
      'Entire original5324 controls/AI/RNG/HP/state chronology unchanged, no extra native replay')
 pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All executed/current inputs unchanged')
 guest,_,scene,_,extra=capture.init_model();pins.update(extra)
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 groups,buffers=ring.observations(text,scene.graphics)
 records=json.loads((CASE/'continuous_scene_records.json').read_text());timeline=meta['independentSemantics']['phase']
 parent=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json'
 incomplete=ROOT/'audit_v6467_current_cpu_bicycle_render_ram'
 earlier=json.loads((incomplete/'result.json').read_text());earlier_terminal=json.loads((incomplete/'native_terminal.json').read_text())
 need(not earlier['passed']and earlier['nativeExit']==earlier_terminal['exitCode']==0 and earlier_terminal['naturalTerminal']and
      not earlier_terminal['observationErrors']and earlier['error']=="ValueError('One real Bicycle contact branch, not unrelated ordinary damage')",
      'Preserve original missing read-only contact evidence rejection, not a gameplay failure')
 need(timeline==json.loads(parent.read_text())['phase']and [r['frame']for r in records]==list(range(2662,2798)),
      'Full original paired Bicycle mechanics and every pre-entry/flight/recovery/thirty-tail screen')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff801070,0xff8017b0),(0xff804000,0xff804470)):
  a,b=(lo-0xff800000)//8,(hi-0xff800000)//8
  need(guest[a:b]==stock[a:b],'Whole original body/eligibility/projection/publication kernels unchanged')
 positive=native_gate(groups,records,text,guest,scene.payload,timeline)
 shadow=shadow_gate(groups,buffers,text,guest,scene.payload)
 donor=original.donor_art(groups,scene.payload,scene.graphics,pins)
 visible=visible_bicycle(groups,records)
 horizontal=push.verify(text,guest,scene.payload,timeline)
 if preflight:
  print(json.dumps(dict(preflightPassed=True,positive=positive,shadow=shadow,donor=donor,visible=visible,horizontal=horizontal)),flush=True);return
 faults=[]
 def reject(label,fn):
  try:fn()
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Actual Bicycle record fault admitted '+label)
 for label,tag,key,delta in[
  ('ground anchor shifted','FLOOR_QUEUE_TRANSFORM','floor',1),('camera shifted','FLOOR_QUEUE_TRANSFORM','camera',65536),
  ('body source shifted','FLOOR_QUEUE_PART','source',1),('body pivot shifted','FLOOR_QUEUE_PART','dy',1),
  ('DMA source shifted','FLOOR_DMA','source',1),('native body hidden','FLOOR_QUEUE_DISPATCH','actor',1)]:
  bad=copy.deepcopy(groups);bad[tag][0][key]+=delta
  reject(label,lambda:native_gate(bad,records,text,guest,scene.payload,timeline))
 for label,tag,key,value in[
  ('shadow absolute camera','MK2_HPHASE_PROJECTION','b4','00000000'),('shadow ground','MK2_HPHASE_PROJECTION','floor','999'),
  ('shadow eligibility','MK2_HPHASE_SHADOW_BEGIN','body','0002'),('shadow source','MK2_HPHASE_SHADOW_DMA','source','00000001'),
  ('shadow absolute position','MK2_HPHASE_SHADOW_DMA','x','999')]:
  line=next(s for s in text.splitlines()if s.startswith(tag+' '))
  badline=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1);bad=text.replace(line,badline,1)
  need(bad!=text,'Real observed native shadow field changed')
  reject(label,lambda:shadow_gate(groups,buffers,bad,guest,scene.payload))
 bad=copy.deepcopy(groups);bad['FLOOR_STATE'][0]['mode']=2
 reject('pre-entry native mode erased',lambda:native_gate(bad,records,text,guest,scene.payload,timeline))
 line=next(s for s in text.splitlines()if s.startswith('MK2_CPU_ROUND_FIELD ')and 'frame=2662 'in s and 'slot=2 'in s)
 badline=re.sub(r'\bid=\S+','id=1',line,count=1);bad=text.replace(line,badline,1)
 reject('pre-entry physical identity proxy',lambda:shadow_gate(groups,buffers,bad,guest,scene.payload))
 # Actual current horizontal fields, including source suppression decay,
 # repulsion, shared-speed publication and the independently landing victim.
 for label,frame,key,value in[
  ('own release position',2714,'xraw','00000000'),('victim release position',2716,'vxraw','00000000'),
  ('wrong own repel speed',2715,'vx','00020000'),('wrong victim shared speed',2718,'vvx','00040000'),
  ('early suppression clear',2714,'suppression','0'),('late suppression clear',2715,'suppression','1'),
  ('grounded victim speed',2745,'vvx','00040000'),('late victim position',2760,'vxraw','00000000')]:
  line=next(s for s in text.splitlines()if s.startswith('MK2_CPU_PAIR_FIELD ')and re.search(r'\bframe='+str(frame)+r'\b',s))
  badline,n=re.subn(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(n==1 and badline!=line,'Real current released field changed')
  bad=text.replace(line,badline,1);reject(label,lambda:push.verify(bad,guest,scene.payload,timeline))
 for label,key in [('real cache height','height'),('real cache pivot','dy'),('real cache source','source')]:
  line=next(s for s in text.splitlines()if s.startswith('MK2_NAT_CAMPAIGN_FLOOR_CACHE_PART ')and 'frame=2716 'in s and 'slot=2 'in s)
  actual=re.search(r'\b'+key+r'=(\S+)',line).group(1)
  value=format(int(actual,16)+1,'08X')if key=='source'else str(int(actual)+1)
  badline=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1);bad=text.replace(line,badline,1)
  reject(label,lambda:push.verify(bad,guest,scene.payload,timeline))
 for label,offset in [('native push opcode',(0xff827c40-0xff800000)//8),('source suppression literal',0xf3b82)]:
  bad=bytearray(guest);bad[offset]^=1;reject(label,lambda:push.verify(text,bytes(bad),scene.payload,timeline))
 bad=copy.deepcopy(records);bad[0]['body']['2']['pixels']=0
 reject('actual native Bicycle body mask hidden',lambda:visible_bicycle(groups,bad))
 need(native_gate(groups,records,text,guest,scene.payload,timeline)==positive and
      shadow_gate(groups,buffers,text,guest,scene.payload)==shadow and push.verify(text,guest,scene.payload,timeline)==horizontal,
      'Whole original unmodified positives restore after every actual fault')
 for module in tuple(sys.modules.values()):
  p=getattr(module,'__file__',None)
  if p and Path(p).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(p).resolve())]=sha(p)
 for p in(parent,*(p for folder in(CASE,incomplete)for p in folder.rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All final current/executed/evidence inputs unchanged')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),nativeTerminal=terminal,
             wholeOriginalBicyclePhase=timeline,wholeOriginalMixedMatch=meta['independentSemantics']['wholeOriginalMixedMatch'],
             completeContinuousRender=meta['continuousRender'],nativeFIFOProjectionArt=positive,ownedNativeFloorShadow=shadow,
             originalDonorArt=donor,visibleOriginalPoses=visible,wholeNativeReleaseHorizontalPush=horizontal,
             actualFaultsRejected=faults,inputHashes=pins,remaining=json.loads((ROOT/'audit_v6281_current_existing_cpu_inventory/report.json').read_text())['remaining'],
             preservedIncompleteNativeCapture=str(incomplete),exactPreEntryModes=[7,7],
             fullCPUContactBodyShadowPushAccepted=True,fullAudioAcceptance=False,allArenasAccepted=False,fullPortAcceptance=False,
             newNativeBoots=0,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,goalStatus='active',
             previousGoalTurnClassification='progress: full CPU ball source audio and evidence compression qualified',
             thisGoalTurnClassification='progress: whole current CPU Bicycle raster/body/shadow and independent release body push qualified')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact lossless finite proof compression')
 print(json.dumps(dict(passed=True,fields=len(records),pixels=meta['continuousRender']['exactRGBPixels'],
                       shadowCopies=shadow['absoluteGeometryCopies'],horizontalBranches=horizontal['branches'],faultsRejected=len(faults))),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
