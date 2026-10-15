"""Before boot: entire original P2 observer/model and qualified current controls.

Deferred cold winner/KO admission retains every native operation before its
one base. No field/timing/pixel exception, actor classifier or reanchoring.
"""
import ast,hashlib,inspect,json,re,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_p1_ending_deferred_source_v5265 as parent
import qualify_ending_cpu_cycle_source_v4750 as original
import qualify_ending_display_source_v4541 as grammar
import ending_raster_cpu_cycle_model_v4740 as model
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5706_current_p2_ending_source_checked'
LUA='mk2ks_current_p2_ending_deferred_campaign_v5704.lua'
DISPLAY='mk2ks_current_p2_ending_deferred_display_v5701.lua'
CLOCK='mk2ks_current_p2_ending_deferred_clock_v5702.lua'
IO='mk2ks_current_p2_ending_deferred_io_v5703.lua'
EXTRA=[LUA,DISPLAY,CLOCK,IO,*parent.EXTRA]


def restore_display(source):
 need(source.count('assert(side==1)')==1,'One source-qualified P1 admission, restored to native P2')
 source=source.replace('assert(side==1)','assert(side==2)',1)
 first=source.index('local winner_entry=');last=source.index('\n]])',first)
 addresses=dict(parent.parent.ADDRESSES)
 admission=re.sub(r'0x010[0-9a-f]+',lambda m:addresses.get(m[0],m[0]),source[first:last])
 old='mode,roster,p:read_u16(0x01060280)';new='mode,p:read_u16(0x01060280),roster'
 need(admission.count(old)==1,'One original physical attract-roster output restore')
 admission=admission.replace(old,new,1)
 return source[:first]+admission+source[last:]


def observer_source(sources=None):
 sources=sources or {p:(ROOT/p).read_text()for p in (LUA,DISPLAY,CLOCK,IO)}
 # Exact wrapper texts are themselves pinned; separately expand and compare
 # the complete underlying observer against original P2 plus the proved defer.
 for path in (LUA,DISPLAY,CLOCK,IO):
  need(sources[path]==(ROOT/path).read_text(),'Only exact whole source wrapper '+path)
 for fresh,old,oldpath,newpath in [(CLOCK,parent.CLOCK,parent.DISPLAY,DISPLAY),(IO,parent.IO,parent.CLOCK,CLOCK)]:
  wrapper=sources[fresh]
  need(wrapper.count("local path='"+old+"'")==1 and wrapper.count("local old='"+oldpath+"'")==1 and
   wrapper.count("..'"+newpath+"'..")==1,'Unique whole immutable clock/IO parent mapping')
 displayed=restore_display((ROOT/parent.DISPLAY).read_text())
 marker="assert(load(source,'@entire2062_native_ending_window_RAM_transport_no_actor_classifier_4518','t',_ENV))()"
 baseline=(ROOT/'mk2ks_ending_display_ram_v4542.lua').read_text()
 need(displayed==baseline.replace(marker,parent.DEFER_SOURCE+marker,1),
  'Every original P2 admission/retirement/source window/observer byte retained plus exact proved defer')
 executed,ram=original.observer_source()
 executed=executed.replace('p:install_read_tap(','ending_read_tap(').replace('p:install_write_tap(','ending_write_tap(')
 pattern=r'\bonce\(\s*('+grammar.TOKEN+r')\s*,\s*('+grammar.TOKEN+r')\s*\)'
 actions=[tuple(grammar.literal(t)for t in m.groups())for m in re.finditer(pattern,parent.DEFER_SOURCE)]
 need(len(actions)==2,'Only full helper definition and arm-before-base addition')
 for before,after in actions:
  need(executed.count(before)==1,'One actual complete native observer boundary')
  executed=executed.replace(before,after,1)
 recovered=executed
 for before,after in reversed(actions):recovered=recovered.replace(after,before,1)
 recovered=recovered.replace('ending_read_tap(','p:install_read_tap(').replace('ending_write_tap(','p:install_write_tap(')
 need(recovered==original.observer_source()[0],
  'Every actual native callback/operation/clock/IO/pixel/window byte recovers the exact original P2 observer')
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',executed),
  'Expanded observer strictly passive, RAM only, no game or controller writes')
 return executed,ram


def preflight():
 current.expected()
 parent_path=parent.OUT/'report.json';prior=json.loads(parent_path.read_text())
 model_path=original.OUT/'report.json';old=json.loads(model_path.read_text())
 matrix_path=ROOT/'audit_v5698_current_campaign_four_case_matrix_checked/report.json';matrix=json.loads(matrix_path.read_text())
 need(prior['passed']and prior['everyWholeObserverCallbackAndRendererGateRetained']and
  old['passed']and old['wholeOriginalNativeOneBasePipelineRetained']and
  matrix['passed']and matrix['actualNativeFourCaseBossOwnEndingAttractMatrixAccepted'],
  'Whole prior native/deferred/full pixel source and actual four current native campaigns proved before boot')
 pins={}
 for report in(prior,old,matrix):
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual prior source/proof byte unchanged')
  for p,h in report['inputHashes'].items():
   need(p not in pins or pins[p]==h,'Consistent actual source provenance');pins[p]=h
 executed,ram=observer_source()
 need(model.Model.line.__globals__['parse']is model.parse and model.Model.__init__.__globals__['Scanline']is model.Scanline and
  model.source==parent.model.original.source,
  'Entire original P2 CPU-cycle/IO/one-base VRAM/RGB model, no P1 namespace leak or pixel/timing relaxation')
 import run_current_p2_ending_pixels_v5707 as host
 for fighter in ('kano','sonya'):
  generated=host.collector(fighter)
  scope=generated.__globals__
  need(scope['fighter']==fighter and scope['native']is current and scope['model']is model and
   scope['source'].__file__==__file__ and scope['LUA']==LUA and set(EXTRA).issubset(scope['CONTROLLERS'])and
   'ram_transport'in generated.__code__.co_varnames and 'transport'in generated.__code__.co_varnames,
   'Actual generated complete current P2 host, independent RAM decoder/native bool and full renderer bound before boot')
  code=scope['declared_physical_source']
  need("MK2KS_CAMPAIGN_SIDE='2'"in code and 'CREATE_NO_WINDOW'in code and
   'PREVIEW_DATAURL'not in code,'Actual qualified current cold P2 controls, hidden native launch, no persisted image previews')
 faults=[];sources={p:(ROOT/p).read_text()for p in(LUA,DISPLAY,CLOCK,IO)}
 for file,before,after,label in [(DISPLAY,'assert(side==2)','assert(side==1)','wrong restored side'),
  (DISPLAY,"['0x01060280']='0x01060e50'","['0x01060280']='0x01060280'",'wrong native roster map'),
  (CLOCK,DISPLAY,parent.DISPLAY,'wrong P1 observer'),(IO,CLOCK,parent.CLOCK,'wrong P1 clock'),
  (LUA,'mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua','mk2ks_sonya_extended_tested_ram_v5206.lua','wrong physical policy'),
  (LUA,"MK2KS_CAMPAIGN_SIDE')=='2'","MK2KS_CAMPAIGN_SIDE')=='1'",'wrong cold physical side')]:
  need(before in sources[file],'Actual source fault, never a vacuous fixture '+label)
  damaged=dict(sources);damaged[file]=damaged[file].replace(before,after,1)
  try:observer_source(damaged)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual changed full source admitted '+label)
  observer_source(sources)
 for p in [Path(__file__),Path(host.__file__),Path(model.__file__),parent_path,model_path,matrix_path,*map(lambda n:ROOT/n,EXTRA)]:
  if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual source/model/control/proof bytes retained')
 return dict(passed=True,physicalSlot=2,characters=['kano','sonya'],sourceOnly=True,
  entireOriginalP2DeferredObserverAndRendererRetained=True,actualSourceFaultsRejected=faults,
  executedObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),
  completeModelSHA256=model.MODEL_SOURCE_SHA256,inputHashes=pins,
  actualNewEndingPixelsAccepted=False,completeEndingArtAudioAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)


if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete-source preflight')
 try:report=preflight()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
