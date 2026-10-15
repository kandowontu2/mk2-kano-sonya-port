"""Same full ending observer; defer its inactive pre-ending taps, fix exporter alias.

No game, physical policy, native admission, observed field or pixel gate changes.
Both admission taps stay active from cold boot. All other exact callbacks arm
before the one original beginning base; nothing inside the window is omitted.
"""
import ast,hashlib,inspect,json,re
from pathlib import Path
import qualify_p1_ending_source_v5248 as parent
import current_payload_metadata_context_v5229 as current
import p1_ending_cpu_cycle_model_v5240 as model
import qualify_ending_display_source_v4541 as grammar
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5263_p1_ending_deferred_source_checked'
LUA='mk2ks_p1_ending_deferred_campaign_ram_v5260.lua'
DISPLAY='mk2ks_p1_ending_deferred_display_ram_v5257.lua'
CLOCK='mk2ks_p1_ending_deferred_clock_ram_v5258.lua'
IO='mk2ks_p1_ending_deferred_io_ram_v5259.lua'
EXTRA=[LUA,DISPLAY,CLOCK,IO,*parent.EXTRA]
DEFER_SOURCE=r'''-- Defer only taps whose callbacks were inactive before command. The two
-- original winner/KO admission taps remain installed from cold boot.
local read_count,write_count
source,read_count=source:gsub('p:install_read_tap%(','ending_read_tap(')
source,write_count=source:gsub('p:install_write_tap%(','ending_write_tap(')
assert(read_count>=8 and write_count>=6,'Complete original observer tap family')
once('local function log(tag,value)',[[
local ending_pending_taps={}
local ending_taps_armed=false
local function ending_defer_tap(kind,first,last,label,callback)
 if label=='actual own final-stage first winner'then
  assert(kind=='read');return p:install_read_tap(first,last,label,callback)
 elseif label=='actual own final-stage final collision KO'then
  assert(kind=='write');return p:install_write_tap(first,last,label,callback)
 end
 local actual=nil
 local handle={}
 function handle:remove()if actual then actual:remove()end end
 ending_pending_taps[#ending_pending_taps+1]=function()
  assert(not actual)
  if kind=='read'then actual=p:install_read_tap(first,last,label,callback)
  else actual=p:install_write_tap(first,last,label,callback)end
 end
 return handle
end
local function ending_read_tap(first,last,label,callback)
 return ending_defer_tap('read',first,last,label,callback)
end
local function ending_write_tap(first,last,label,callback)
 return ending_defer_tap('write',first,last,label,callback)
end
local function ending_arm_taps()
 assert(command and not ending_taps_armed)
 ending_taps_armed=true
 for _,activate in ipairs(ending_pending_taps)do activate()end
 ending_pending_taps={}
end
local function log(tag,value)]])
once("command=frame;origin=frame;ensure_base();raster_clock('begin')",
 "command=frame;origin=frame;ending_arm_taps();ensure_base();raster_clock('begin')")
'''

def observer_source(sources=None):
 sources=sources or{p:(ROOT/p).read_text()for p in (LUA,DISPLAY,CLOCK,IO)}
 marker="assert(load(source,'@entire2062_native_ending_window_RAM_transport_no_actor_classifier_4518','t',_ENV))()"
 old=(ROOT/parent.DISPLAY).read_text()
 need(old.count(marker)==1 and sources[DISPLAY]==old.replace(marker,DEFER_SOURCE+marker,1),
  'Exact whole original observer plus only complete inactive-tap defer boundary')
 for fresh,oldname,before,after in[
  (CLOCK,parent.CLOCK,parent.DISPLAY,DISPLAY),(IO,parent.IO,parent.CLOCK,CLOCK),(LUA,parent.LUA,parent.IO,IO)]:
  need(sources[fresh]==(ROOT/oldname).read_text().replace(before,after,1),
   'Whole clock/IO/physical controller source unchanged except exact declared parent '+fresh)
 executed,ram=parent.observer_source()
 read_count=executed.count('p:install_read_tap(');write_count=executed.count('p:install_write_tap(')
 need(read_count>=8 and write_count>=6,'Actual full prior observer tap counts')
 executed=executed.replace('p:install_read_tap(','ending_read_tap(').replace('p:install_write_tap(','ending_write_tap(')
 pattern=r'\bonce\(\s*('+grammar.TOKEN+r')\s*,\s*('+grammar.TOKEN+r')\s*\)'
 actions=[tuple(grammar.literal(t)for t in m.groups())for m in re.finditer(pattern,DEFER_SOURCE)]
 need(len(actions)==2,'Only exact helper definition and before-base arm insertion')
 for before,after in actions:
  need(executed.count(before)==1,'Exact whole observed renderer boundary')
  executed=executed.replace(before,after,1)
 need('command=frame;origin=frame;ending_arm_taps();ensure_base();raster_clock(\'begin\')'in executed and
  not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',executed),
  'Full actual admission then arm-before-original-base, strictly readonly complete observation')
 # Removing the exact helper/arm and inverse renaming recovers every byte of
 # the already qualified full native observer, including each callback.
 recovered=executed
 for before,after in reversed(actions):recovered=recovered.replace(after,before,1)
 recovered=recovered.replace('ending_read_tap(','p:install_read_tap(').replace('ending_write_tap(','p:install_write_tap(')
 need(recovered==parent.observer_source()[0],'Every full native operation/callback/pixel/clock/window byte retained')
 return executed,ram,read_count,write_count

def main():
 need(not OUT.exists(),'Fresh immutable whole defer/export preflight')
 current.expected()
 oldpath=parent.OUT/'report.json';old=json.loads(oldpath.read_text())
 need(old['passed']and old['sourceOnly']and all(sha(p)==h for p,h in old['inputHashes'].items()),
  'Complete P1 physical map, whole renderer/source-cycle/bitfault/control baseline retained')
 failure=ROOT/'audit_v5250_kano_current_p1_ending_pixels_checked/report.json'
 actual=ROOT/'audit_v5250_kano_current_p1_ending_pixels/result.json'
 failed=json.loads(failure.read_text());meta=json.loads(actual.read_text())
 need(not failed['passed']and "'bool' object has no attribute 'records'"in failed['error']and
  meta['nativeExit']==0 and meta['passed']and not meta['endingModelErrors']and
  meta['exactContinuousEndingFields']==meta['observedEndingRGBFields']==3040 and
  len(meta['endingNativePixelFaults'])==2 and all(sha(p)==h for p,h in meta['inputHashes'].items()),
  'Actual complete native terminal0/checker3040-bitfault observation, then real post-terminal exporter alias failure; not full final video acceptance')
 executed,ram,reads,writes=observer_source()
 import run_p1_ending_deferred_pixels_v5261 as host
 import run_p1_ending_pixels_v5247 as oldhost
 for fighter in ('kano','sonya'):
  generated=host.collector(fighter)
  need(generated.__globals__['fighter']==fighter and generated.__globals__['native']is current and
   generated.__globals__['model']is model and generated.__globals__['source'].__file__==__file__ and
   generated.__globals__['LUA']==LUA and set(EXTRA).issubset(generated.__globals__['CONTROLLERS'])and
   'ram_transport'in generated.__code__.co_varnames and 'transport'in generated.__code__.co_varnames,
   'Actual generated full capture exact current scope, distinct RAM decoder and native transport bool before boot')
 newsource=Path(host.__file__).read_text();oldsource=Path(oldhost.__file__).read_text()
 normalized=newsource.replace('qualify_p1_ending_deferred_source_v5262','qualify_p1_ending_source_v5248').replace('audit_v5264_','audit_v5250_')
 for before,after in [('ram_transport=model.Transport()','transport=model.Transport()'),
  ('raw=ram_transport.decode(fields,encoded)','raw=transport.decode(fields,encoded)'),
  ('json.dumps(ram_transport.records,indent=2)','json.dumps(transport.records,indent=2)')]:
  need(normalized.count(before)==1,'Only exact old RAM alias collision repair '+before)
  normalized=normalized.replace(before,after,1)
 need(normalized==oldsource,'Entire full native guest/control/GFX/VRAM/RGB/bitfault/export/chronology gate retained except unique RAM alias')
 sources={p:(ROOT/p).read_text()for p in(LUA,DISPLAY,CLOCK,IO)};faults=[]
 for file,before,after,label in[
  (DISPLAY,"kind=='read';return p:install_read_tap","kind=='write';return p:install_read_tap",'wrong cold winner admission'),
  (DISPLAY,"ending_arm_taps();ensure_base()","ensure_base();ending_arm_taps()",'base before tap arm'),
  (DISPLAY,"for _,activate in ipairs(ending_pending_taps)do activate()end","ending_pending_taps={}",'dropped callback family'),
  (DISPLAY,"p:install_write_tap(first,last,label,callback)","p:install_write_tap(first,last,label,function()return 0 end)",'altered native store callback'),
  (DISPLAY,"assert(command and not ending_taps_armed)","assert(command)",'multiple-arm scope'),
  (CLOCK,"mk2ks_p1_ending_deferred_display_ram_v5257.lua",parent.DISPLAY,'old always-active tap scope'),
  (LUA,"mk2ks_current_kano_p1_campaign_ram_v5194.lua","mk2ks_kano_current_p2_campaign_ram_v4472.lua",'wrong physical controls')]:
  need(before in sources[file],'Nonvacuous actual defer source fault '+label)
  bad=dict(sources);bad[file]=bad[file].replace(before,after,1)
  try:observer_source(bad)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual source fault accepted '+label)
  observer_source(sources)
 pins=dict(old['inputHashes'])
 for p in [oldpath,failure,actual,Path(__file__).resolve(),Path(host.__file__),*map(lambda p:ROOT/p,EXTRA)]:
  if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
  key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No old/failure/source evidence overwrite');pins[key]=h
 need(all(sha(p)==h for p,h in pins.items()),'All exact original/failure/defer sources preserved')
 report=dict(passed=True,sourceOnly=True,physicalSlot=1,characters=['kano','sonya'],
  everyWholeObserverCallbackAndRendererGateRetained=True,bothNativeColdAdmissionTapsRetained=True,
  allOtherTapsArmBeforeOriginalBase=True,originalReadTapDeclarations=reads,originalWriteTapDeclarations=writes,
  actualExportAliasFailurePreserved=str(failure),exportAliasRepairedBeforeBoot=True,
  sourceFaultsRejected=faults,executedObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),
  completeModelSHA256=model.MODEL_SOURCE_SHA256,inputHashes=pins,fullPortAcceptance=False,
  actualNewNativePixelAcceptance=False,newBuilds=0,rawMediaWritten=0)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
