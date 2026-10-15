"""Whole original source/FIFO/DMA/shadow/raster gates on repaired Ring branches.

No previous acceptance transfer: each new native capture must have exact whole
guest identity, immutable inputs, clean natural terminal and original physical
trajectory. Add same-field retirement order faults and physical state faults.
"""
import argparse,copy,gzip,inspect,json,re,subprocess,types
from pathlib import Path
from types import SimpleNamespace
import capture_repaired_ring_render_v6536 as capture
import verify_current_cpu_ring_render_v6379 as core
import verify_current_cpu_ring_render_v6381 as hit
import verify_current_cpu_ring_mirror_render_v6391 as blocked
import verify_current_cpu_ring_miss_render_v6414 as missed
ROOT,need,sha=capture.ROOT,capture.need,capture.sha

def rebind(fn,**values):
 scope=dict(fn.__globals__,**values)
 return types.FunctionType(fn.__code__,scope,fn.__name__,fn.__defaults__,fn.__closure__)

def main(branch,preflight=False):
 case=capture.folder(branch);out=ROOT/f'audit_v6539_repaired_ring_{branch}_checked'
 need(not out.exists(),'Fresh immutable full new-candidate branch qualification')
 module=capture.BRANCHES[branch]
 terminal=SimpleNamespace(current=capture.candidate,process_tools=capture.hit.previous.terminal.process_tools)
 previous=SimpleNamespace(terminal=terminal)
 actual=SimpleNamespace(**dict(module.__dict__,model=capture.blocked.model if branch=='block' else capture.hit.model,
                              previous=previous,init_model=lambda:capture.init_model(branch)))
 native_base=rebind(core.native_gate,CASE=case)
 if branch=='hit':native_gate=rebind(hit.native_gate,original=SimpleNamespace(native_gate=native_base))
 elif branch=='block':native_gate=rebind(blocked.native_gate,CASE=case,capture=actual)
 else:native_gate=rebind(missed.native_gate,CASE=case,capture=actual)
 shadow_gate=rebind(blocked.shadow_gate if branch=='block' else core.shadow_gate,CASE=case)
 source=inspect.getsource(core.main)
 a='Path(__file__),Path(original.__file__),Path(shadows.__file__)'
 b='Path(__file__),Path(capture_source.__file__),Path(core.__file__),Path(hit.__file__),Path(blocked.__file__),Path(missed.__file__),Path(original.__file__),Path(shadows.__file__)'
 need(source.count(a)==1,'Pin all actual full predecessor and branch gate sources')
 source=source.replace(a,b,1)
 a='currentCPUFullRingHitRenderShadowAndEraseAccepted=True'
 flag={'hit':'repairedCPUFullRingHitRenderShadowAndEraseAccepted','block':'repairedCPUBlockedMirrorRingRenderShadowAndEraseAccepted','miss':'repairedCPUMissedRingRenderShadowAndEraseAccepted'}[branch]
 need(source.count(a)==1,'Report actual tested repaired branch only');source=source.replace(a,flag+'=True',1)
 scope=dict(core.__dict__,__file__=__file__,CASE=case,OUT=out/'native_gate',capture=actual,capture_source=capture,
            core=core,hit=hit,blocked=blocked,missed=missed,native_gate=native_gate,shadow_gate=shadow_gate)
 scope['observations']=rebind(core.observations,capture=actual)
 exec(compile(source,__file__+'::whole_original_positive_and_actual_record_faults_'+branch,'exec'),scope)
 if not preflight:out.mkdir()
 scope['main'](preflight)
 if preflight:return
 p=out/'report.json';report=json.loads((out/'native_gate/report.json').read_text());meta=json.loads((case/'result.json').read_text())
 guest,build,scene,_,_=capture.init_model(branch)
 need(meta['candidate']==capture.candidate.NAME and meta['proof']['sha256']==capture.candidate.GUEST_SHA and
      meta['proof']['bytes']==1048576 and meta['proof']['everyActualByteComparedInRAM'],
      'Actual complete new native initialized guest, never old candidate observation')
 need(Path(meta['nativeIdentity']['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve(),
      'Actual newly repaired executable native identity')
 with gzip.open(case/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 groups,buffers=scope['observations'](text,scene.graphics)
 sequences,_=core.original.art.independent_art(scene.payload,scene.graphics,{})
 records=json.loads((case/'continuous_scene_records.json').read_text());timeline=meta['independentSemantics']['ring']['acceptedRings'][0]
 positive=native_gate(groups,records,text,guest,scene.payload,sequences['ring'],timeline)
 faults=[]
 if branch in ('block','miss'):
  lines=text.splitlines();child=groups['FLOOR_CHILD_SPAWN'][0]['actor']
  pubs=[i for i,l in enumerate(lines) if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ') and actual.model.parse(l)[1]['actor']==child]
  need(pubs,'Actual child has native publications')
  last=lines.pop(pubs[-1]);dead=next(i for i,l in enumerate(lines)if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_CHILD_RETIRE ') and actual.model.parse(l)[1]['actor']==child)
  lines.insert(dead+1,last);bad='\n'.join(lines)
  try:native_gate(groups,records,bad,guest,scene.payload,sequences['ring'],timeline)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind='same-field child publication after retirement',rejectedBy=str(e)))
  else:raise ValueError('False same-field child lifetime admitted')
 phase=capture.missed.miss.full_phase if branch=='miss' else capture.blocked.full_phase if branch=='block' else capture.hit.full_phase
 full=phase(text,guest);need(json.loads(json.dumps(full))==meta['independentSemantics'],'Whole actual branch physical/state/health semantics independently restored')
 trials=[('wrong native CPU ID','MK2_CPU_OVERLAP_EVENT','kind=ring ','id','1'),
         ('wrong parent owner','MK2_CPU_OVERLAP_EVENT','kind=ring ','main_owner','00000000'),
         ('wrong child parent','MK2_CPU_OVERLAP_CHILD','entry=FFFC7000','shot_owner','00000000'),
         ('wrong child birth','MK2_CPU_OVERLAP_CHILD','entry=FFFC7000','frame','1'),
         ('wrong child position','MK2_CPU_OVERLAP_CHILD_FIELD','','xraw','00000000'),
         ('wrong child lifetime','MK2_CPU_OVERLAP_CHILD_FIELD','','child_serial','2'),
         ('wrong retirement instruction','MK2_CPU_OVERLAP_RETIRE','','pc','FF8B6831'),
         ('wrong held body pose','MK2_CPU_PAIR_FIELD',f"frame={timeline['start']+1} ",'pose','00000000')]
 for label,tag,where,key,value in trials:
  line=next(l for l in text.splitlines()if l.startswith(tag+' ')and where in l)
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,line,count=1);need(changed!=line,'Effective actual physical fault')
  try:phase(text.replace(line,changed,1),guest)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False native physical Ring state admitted '+label)
 line=next(l for l in text.splitlines()if l.startswith('MK2_CPU_OVERLAP_CHILD_FIELD '))
 for label,bad in [('missing child callback',text.replace(line+'\n','',1)),('duplicate child callback',text.replace(line,line+'\n'+line,1))]:
  try:phase(bad,guest)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('Missing/ambiguous native child callback admitted')
 need(native_gate(groups,records,text,guest,scene.payload,sequences['ring'],timeline)==positive and phase(text,guest)==full,
      'Whole native render and physical positive restored after every fault')
 oldfolder={'hit':ROOT/'audit_v6378_current_cpu_ring_render_ram','block':ROOT/'audit_v6390_current_cpu_ring_mirror_render_ram',
            'miss':ROOT/'audit_v6413_current_cpu_ring_miss_render_ram'}[branch]
 oldrecords=json.loads((oldfolder/'continuous_scene_records.json').read_text())
 need(records==oldrecords,'Every complete continuously reconstructed native frame and owned body/effect mask matches prior actual scene')
 for f in (oldfolder/'continuous_scene_records.json',Path(__file__),Path(capture.__file__)):
  report['inputHashes'][str(f.resolve())]=sha(f)
 report.update(actualAdditionalPhysicalAndRetirementFaults=faults,everyContinuousNativeSceneRecordIdenticalToPrior=True,
               wholeActualGuestSHA256=capture.candidate.GUEST_SHA,executableSHA256=capture.candidate.EXE_SHA,
               publicPlayableChanged=False,fullPortAcceptance=False)
 need(all(sha(k)==h for k,h in report['inputHashes'].items()),'All actual native/qualifier inputs unchanged')
 p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Hash-preserving exact complete proof compression')
 print(json.dumps(dict(passed=True,branch=branch,fields=len(records),exactRGBPixels=meta['continuousRender']['exactRGBPixels'],additionalFaults=len(faults))),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--branch',required=True,choices=capture.BRANCHES);p.add_argument('--preflight',action='store_true');a=p.parse_args()
 main(a.branch,a.preflight)
