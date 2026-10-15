"""Whole qualified blade/knife art, native single/multipart projection and erase.

Reuse the exact source-corrected6358 geometry and6356 same-field retirement
order contracts on the new capture, not its historical acceptance or failures.
"""
import copy,gzip,inspect,json,subprocess
from pathlib import Path
from types import SimpleNamespace
import capture_repaired_kano_effects_v6540 as capture
import verify_current_cpu_effect_render_v6350 as original
import verify_current_cpu_effect_render_v6358 as corrected
import verify_current_cpu_effect_render_v6356 as order
import verify_repaired_kano_chronology_v6548 as chronology
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6543_repaired_kano_effects_checked'

def main():
 need(not OUT.exists(),'Fresh exact new candidate source/art/cleanup qualification')
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 core=corrected.source_gate()
 def gate(g,records,guest,payload,seq,sources):
  result=core(g,records,guest,payload,seq,sources)
  result['actualIntraFieldRetirementOrder']=order.order_contract(text,sources)
  return result
 terminal=SimpleNamespace(current=capture.candidate,process_tools=capture.original.terminal.process_tools)
 actual=SimpleNamespace(**dict(capture.original.__dict__,terminal=terminal,init_model=capture.init_model))
 source=inspect.getsource(original.main)
 a='for path in(PARENT,Path(__file__),'
 b='for path in(Path(original.__file__),Path(corrected.__file__),Path(order.__file__),Path(capture_source.__file__),PARENT,Path(__file__),'
 need(source.count(a)==1,'Pin all whole original and corrected geometry/retirement/capture gates')
 source=source.replace(a,b,1)
 changes={
  "meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())":'meta,terminal,chronology_proof=chronology.qualified_meta()',
  "meta['passed']and terminal['naturalTerminal']":"chronology_proof['passed']and terminal['naturalTerminal']",
  "meta['originalWholePhysicalTrajectoryUnchanged']":"chronology_proof['exactSourceDerivedChronology']['allOtherRowsAndCharactersExact']",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Exact source-derived task-ID admission; complete native/art gate retained');source=source.replace(before,after,1)
 scope=dict(original.__dict__,__file__=__file__,CASE=CASE,OUT=OUT/'native_gate',capture=actual,capture_source=capture,
            original=original,corrected=corrected,order=order,gate=gate,chronology=chronology)
 OUT.mkdir();exec(compile(source,__file__+'::whole_original_art_FIFO_source_correct_projection_erase','exec'),scope);scope['main']()
 report=json.loads((OUT/'native_gate/report.json').read_text());meta,_,task_proof=chronology.qualified_meta()
 need(task_proof['passed'] and meta['candidate']==capture.candidate.NAME and meta['proof']['sha256']==capture.candidate.GUEST_SHA and
      meta['proof']['everyActualByteComparedInRAM'] and Path(meta['nativeIdentity']['ExecutablePath']).resolve()==
      (ROOT/capture.candidate.NAME/'mkport_candidate.exe').resolve(),'Actual full repaired native guest and executable, not old runtime admission')
 oldpath=ROOT/'audit_v6349_current_cpu_effect_render_ram/continuous_scene_records.json'
 records=json.loads((CASE/'continuous_scene_records.json').read_text())
 need(records==json.loads(oldpath.read_text()),'Every one of641 consecutive full native VRAM/RGB/body/effect/shadow scenes identical to prior source-qualified run')
 guest,_,scene,_,_=capture.init_model();g=original.groups(text)
 sequences,_=original.art.independent_art(scene.payload,scene.graphics,{})
 blades=original.blade_art(guest,scene.payload,scene.graphics,{})
 positive=gate(g,records,guest,scene.payload,sequences['knife'],blades['sources'])
 pubs=[l for l in text.splitlines()if l.startswith('MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ') and
       int(original.re.search(r'\bsource=([0-9A-F]+)',l)[1],16) in blades['sources']]
 need(pubs,'Actual attached blade publications exist')
 lines=text.splitlines();last=pubs[-1];lines.remove(last)
 cut=next(i for i,l in enumerate(lines)if l.startswith('MK2_BLADE_ALLOC_RETIRE ')and 'frame=1909 ' in l and 'object=01031B00 ' in l)
 lines.insert(cut+1,last);bad='\n'.join(lines)
 try:order.order_contract(bad,blades['sources'])
 except(ValueError,AssertionError,KeyError)as e:fault=dict(kind='same-field blade publication after actual native retirement',rejectedBy=str(e))
 else:raise ValueError('False same-field blade lifetime admitted')
 need(gate(g,records,guest,scene.payload,sequences['knife'],blades['sources'])==positive,'Whole original physical/art/geometry positive restored')
 report.update(repairedNativeCPUBladeBlockedKnifeKOResetRenderAccepted=True,publicPlayableChanged=False,
               everyContinuousNativeSceneRecordIdenticalToPrior=True,actualAdditionalRetirementFault=fault,
               wholeActualGuestSHA256=capture.candidate.GUEST_SHA,executableSHA256=capture.candidate.EXE_SHA,fullPortAcceptance=False)
 report['originalCaptureRejectionPreserved']=True
 report['exactSourceDerivedChronology']=task_proof['exactSourceDerivedChronology']
 for p in (oldpath,Path(__file__),Path(capture.__file__),Path(chronology.__file__),chronology.OUT/'report.json'):report['inputHashes'][str(p.resolve())]=sha(p)
 need(all(sha(k)==h for k,h in report['inputHashes'].items()),'All actual gate and native inputs intact')
 p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact repaired effect proof compression')
 print(json.dumps(dict(passed=True,fields=641,exactRGBPixels=meta['continuousRender']['exactRGBPixels'],nativeFaults=len(report['actualFaultsRejected']),retirementFaults=1)),flush=True)

if __name__=='__main__':main()
