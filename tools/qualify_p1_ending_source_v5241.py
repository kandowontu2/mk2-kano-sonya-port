"""Before boot: exact P1 observer mapping and unchanged full renderer/controls."""
import ast,hashlib,inspect,json,re,sys
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_ending_cpu_cycle_source_v4750 as prior
import qualify_ending_display_source_v4541 as grammar
import p1_ending_cpu_cycle_model_v5240 as model
import run_corrected_p1_campaigns_v5230 as policies
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5242_p1_ending_source_checked'
LUA='mk2ks_p1_ending_campaign_ram_v5239.lua'
DISPLAY='mk2ks_p1_ending_display_ram_v5236.lua'
CLOCK='mk2ks_p1_ending_raster_clock_ram_v5237.lua'
IO='mk2ks_p1_ending_raster_io_ram_v5238.lua'
EXTRA=[LUA,DISPLAY,CLOCK,IO,'mk2ks_native_tomb_ram_v3624.lua','mk2ks_native_tomb_display_v2062.lua']
ADDRESSES={'0x01060e50':'0x01060280','0x010602f0':'0x01060ec0','0x010602ff':'0x01060ecf',
 '0x01060ec0':'0x010602f0','0x01060dc0':'0x010601f0','0x01060df0':'0x01060220',
 '0x01060220':'0x01060df0','0x01060280':'0x01060e50'}

def swap_native(s):
 s=re.sub(r'0x010[0-9a-f]+',lambda m:ADDRESSES.get(m[0],m[0]),s)
 before='mode,p:read_u16(0x01060e50),roster'
 need(s.count(before)==1,'Exact physical attract-roster output order')
 return s.replace(before,'mode,roster,p:read_u16(0x01060e50)',1)

def expected_display():
 s=(ROOT/'mk2ks_ending_display_ram_v4542.lua').read_text()
 need(s.count('assert(side==2)')==1,'One old physical admission')
 s=s.replace('assert(side==2)','assert(side==1)',1)
 first=s.index('local winner_entry=');last=s.index('\n]])',first)
 return s[:first]+swap_native(s[first:last])+s[last:]

def observer_source(sources=None):
 sources=sources or {p:(ROOT/p).read_text()for p in EXTRA}
 need(sources[DISPLAY]==expected_display(),'Exact full immutable observer; only source-proven P1 native admission addresses')
 need(sources[CLOCK]==(ROOT/'mk2ks_ending_raster_clock_ram_v4706.lua').read_text().replace(
  'mk2ks_ending_display_ram_v4542.lua',DISPLAY,1),'Entire raster-clock observer unchanged except P1 parent path')
 need(sources[IO]==(ROOT/'mk2ks_ending_raster_io_ram_v4719.lua').read_text().replace(
  'mk2ks_ending_raster_clock_ram_v4706.lua',CLOCK,1),'Entire explicit display-IO observer unchanged except P1 parent path')
 expected="""-- Exact accepted P1 buttons; one strictly read-only complete ending observer.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')
if fighter=='kano'then
 dofile('mk2ks_current_kano_p1_campaign_ram_v5194.lua')
elseif fighter=='sonya'then
 dofile('mk2ks_sonya_extended_tested_ram_v5206.lua')
else error('Only true Kano/Sonya P1 ending contexts')end
dofile('mk2ks_p1_ending_raster_io_ram_v5238.lua')
"""
 need(sources[LUA]==expected,'Both complete accepted physical controllers plus one readonly observer only')
 old,ram=prior.observer_source()
 first=old.index('local winner_entry=');last=old.index('-- Observe actual native sound-port writes;',first)
 executed=old[:first]+swap_native(old[first:last])+old[last:]
 before="local side=tonumber(assert(os.getenv('MK2KS_CAMPAIGN_SIDE')));assert(side==2)"
 need(executed.count(before)==1,'Exact original whole observer physical admission')
 executed=executed.replace(before,before.replace('==2','==1'),1)
 # Validate the actual addresses against the original independent physical ledger.
 state=(ROOT/'mk2ks_native_tomb_display_v2062.lua').read_text()
 for token in('p:read_u16(0x01060280),p:read_u16(0x01060e50)',
  'p:read_u16(0x010601f0),p:read_u16(0x01060dc0)',
  'p:read_u16(0x010602f0),p:read_u16(0x01060ec0)',
  'p:read_u32(0x01060220),p:read_u32(0x01060df0)'):
  need(token in state,'Original physical P1/P2 typed memory map '+token)
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|set_value|clear_value|return\s+data|io\.open|snapshot\(|machine:exit|set_input',executed),
  'Entire final expanded observer strictly readonly and RAM-only')
 return executed,ram

def preflight():
 current.expected()
 proof=json.loads((ROOT/'audit_v4751_ending_cpu_cycle_source_checked/report.json').read_text())
 need(proof['passed']and proof['wholeOriginalNativeOneBasePipelineRetained']and
  proof['actualSourceDefinedCPUClockBoundaryQualified']and
  all(sha(p)==h for p,h in proof['inputHashes'].items()),'Complete original source-defined cycle/IO/pixel model gates retained')
 pins=dict(proof['inputHashes'])
 for fighter in ('kano','sonya'):
  p=ROOT/f'audit_v5235_{fighter}_corrected_p1_campaign_checked/report.json'
  campaign=json.loads(p.read_text())
  need(campaign['passed']and campaign['actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted']and
   all(sha(k)==v for k,v in campaign['inputHashes'].items()),'Actually completed full current P1 physical campaign '+fighter)
  pins[str(p)]=sha(p)
  for k,v in campaign['inputHashes'].items():
   need(k not in pins or pins[k]==v,'Consistent complete original/current source');pins[k]=v
 executed,ram=observer_source()
 need(model.source.replace('self.ids in ((17,13),(18,13))','self.ids in ((13,17),(13,18))',1)==model.original.source and
  model.scanline_source==inspect.getsource(model.original.Scanline),
  'Whole one-base CPU/DMA/shift/VRAM/RGB/bitfault and entire source-cycle scanline state machine retained')
 need(model.Model.line.__globals__['parse']is model.parse and
  model.Model.__init__.__globals__['Scanline']is model.Scanline and
  model.Scanline.advance.__globals__['previous'].previous.validate_context is model.validate_context and
  model.Model.snapshot.__globals__['validate_context']is model.validate_context,
  'Every generated class/parser/state-machine bound to explicit P1 context, no old P2 globals mutated')
 faults=[]
 sources={p:(ROOT/p).read_text()for p in EXTRA}
 for file,before,after,label in (
  (DISPLAY,'assert(side==1)','assert(side==2)','wrong physical slot'),
  (DISPLAY,'cpu.PC.value~=0xff836700','cpu.PC.value~=0xff836710','wrong native collision PC'),
  (DISPLAY,'p:read_u16(0x01060280)~=identity','p:read_u16(0x01060e50)~=identity','wrong own roster'),
  (DISPLAY,'p:read_u16(0x010602f0)<=0','p:read_u16(0x01060ec0)<=0','wrong own health'),
  (DISPLAY,'p:read_u16(0x010601f0)==1','p:read_u16(0x01060dc0)==1','wrong own state'),
  (DISPLAY,'p:read_u32(0x01060df0)==0','true','missing opponent actor retirement'),
  (DISPLAY,'ending_completed+300','ending_completed+30','shortened attract window'),
  (DISPLAY,'origin=frame;ensure_base()','origin=frame;p:write_u16(0x01060280,1);ensure_base()','guest write'),
  (CLOCK,"raster_clock('finish')",'-- removed finish clock','missing complete clock'),
  (IO,'p:read_u16(at),data,mask','0,data,mask','missing pre-store IO state'),
  (LUA,'mk2ks_current_kano_p1_campaign_ram_v5194.lua','mk2ks_kano_current_p2_campaign_ram_v4472.lua','wrong controls')):
  need(sources[file].count(before)>=1,'Actual nonvacuous source fault '+label)
  bad=dict(sources);bad[file]=bad[file].replace(before,after,1)
  try:observer_source(bad)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual source fault accepted '+label)
  observer_source(sources)
 for p in [Path(__file__).resolve(),Path(model.__file__),ROOT/'tools/run_p1_ending_pixels_v5243.py',*map(lambda p:ROOT/p,EXTRA)]:
  if p.suffix=='.py':ast.parse(p.read_text(),filename=str(p))
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual retained and new complete source bytes intact')
 return dict(passed=True,physicalSlot=1,characters=['kano','sonya'],sourceFaultsRejected=faults,
  executedObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),
  originalRAMTransportSHA256=hashlib.sha256(ram.encode()).hexdigest().upper(),
  continuousModelSHA256=model.MODEL_SOURCE_SHA256,sourceOnly=True,
  originalCompleteRendererAndPhysicalPoliciesRetained=True,inputHashes=pins,
  actualP1EndingPixelsAccepted=False,completeAudioAccepted=False,fullPortAcceptance=False,
  newBuilds=0,rawMediaWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable P1 whole source preflight')
 report=preflight();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
