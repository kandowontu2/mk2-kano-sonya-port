"""Before boot: whole qualified ending/DAC/ROM observers, all four true slots."""
import ast,hashlib,inspect,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import current_ending_audio_model_v5733 as model
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5738_current_ending_audio_source_checked'
OBSERVER='mk2ks_current_ending_audio_observer_v5734.lua'
LUA='mk2ks_current_ending_audio_campaign_v5735.lua'


def once(source,before,after,count=1):
 need(source.count(before)==count,'Only exact whole passive source adapter '+before)
 return source.replace(before,after)


def expected_observer():
 audio=(ROOT/'mk2ks_native_ending_audio_observer_ram_v4495.lua').read_text()
 audio=once(audio,'assert(side==2)','assert(side==1 or side==2);local other=3-side')
 audio=once(audio,'slots[1].hp','slots[other].hp',5)
 audio=once(audio,'local h1,h2=p:read_u16(slots[other].hp),p:read_u16(slots[2].hp)',
  'local h1,h2=p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)')
 audio=once(audio,'valid(a2)and h2>0','valid(side==1 and a1 or a2)and(side==1 and h1 or h2)>0')
 audio=once(audio,'roster==identity and h1==0 and h2>0 and a1==0 and a2==0',
  'roster==identity and p:read_u16(slots[other].hp)==0 and p:read_u16(slots[side].hp)>0 and a1==0 and a2==0')
 audio=once(audio,'p:read_u16(slots[1].roster),roster',
  'p:read_u16(slots[1].roster),p:read_u16(slots[2].roster)',2)
 dac=(ROOT/'mk2ks_current_native_dac_ram_v5592.lua').read_text()
 dac=dac[dac.index('local frame,serial,previous,previous_time='):]
 dac=once(dac," local origin=rawget(_G,'MK2_STOCK_V921_ACTION_START')\n if not origin or frame<origin or frame>origin+749 then return end",
  ' if not active()then return end')
 rom=(ROOT/'mk2ks_current_dcs_rom_source_v5585.lua').read_text()
 rom=rom[rom.index('local region=assert('):]
 rom=once(rom,'checks==2 and frame==5198','checks==2 and origin and completed and frame==completed+300')
 return audio.rstrip()+'\n-- Entire passive5592 DAC observer; only its ending admission changes.\n'+dac.rstrip()+\
  '\n-- Entire passive5585 ROM observer; only its actual native terminal changes.\n'+rom.rstrip()+'\n'


CAMPAIGN="""-- All four exact qualified cold physical policies; one passive audio observer.
local fighter=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local side=tonumber(assert(os.getenv('MK2KS_CAMPAIGN_SIDE')))
assert(side==1 or side==2)
if fighter=='kano'then
 if side==1 then dofile('mk2ks_current_kano_p1_campaign_ram_v5194.lua')
 else dofile('mk2ks_kano_current_p2_campaign_ram_v4472.lua')end
elseif fighter=='sonya'then
 if side==1 then dofile('mk2ks_sonya_extended_tested_ram_v5206.lua')
 else dofile('mk2ks_sonya_p2_verified_subzero_campaign_v5687.lua')end
else error('Only true Kano/Sonya cold campaigns')end
dofile('mk2ks_current_ending_audio_observer_v5734.lua')
"""


def observer_source(observer=None,campaign=None):
 observer=(ROOT/OBSERVER).read_text()if observer is None else observer
 campaign=(ROOT/LUA).read_text()if campaign is None else campaign
 need(observer==expected_observer()and campaign==CAMPAIGN,
  'Every full original callback/ROM/DAC/channel/route and exact declared native controller retained')
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|dofile\(|\bload\(|snapshot\(|machine:exit|return\s+data|force_update|flush\(',observer),
  'Entire composed observer passive, no controls/guest/AI/palette/ROM/sound/channel/cursor writes or forced flushes')
 return observer


def run():
 current.expected();executed=observer_source()
 proofpath=ROOT/'audit_v5732_current_four_case_ending_pixels_progress/progress.json'
 proof=json.loads(proofpath.read_text())
 need(proof['passed']and proof['actualCurrentFourCaseNaturalEndingPipelineAccepted']and len(proof['cases'])==4,
  'All four actual current cold boss/own-ending/300attract/full native pixel cases established first')
 pins={}
 for p,h in proof['sourceInputs'].items():
  need(sha(p)==h,'Actual current whole physical/guest/pixel/art/hardware sources remain byte-exact');pins[p]=h
 dacpath=ROOT/'audit_v5598_current_native_dac_clock_progress/progress.json'
 stockpath=ROOT/'audit_v5618_original_mk2_qualified_waveform_progress/progress.json'
 dac=json.loads(dacpath.read_text());stock=json.loads(stockpath.read_text())
 need(dac['passed']and dac['allObservedKanoP1NativeDACToMixerWaveformSourceExact']and stock['passed'],
  'Real prior original native+stock DAC/source-clock/whole waveform positives, not a newly fitted model')
 for p in [Path(model.original_dac.__file__),Path(model.original_clock.__file__),Path(model.original_rom.__file__),
  ROOT/'mk2ks_current_native_dac_ram_v5592.lua',ROOT/'mk2ks_current_dcs_rom_source_v5585.lua',
  ROOT/'mame-mkp/src/mame/shared/dcs.cpp',ROOT/'mame-mkp/src/devices/sound/dmadac.cpp',
  ROOT/'mame-mkp/src/devices/sound/dmadac.h',ROOT/'mame-mkp/src/emu/sound.cpp',
  ROOT/'mame-mkp/src/emu/sound.h',ROOT/'mame-mkp/src/emu/attotime.h',
  ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp']:
  key=str(p.resolve())
  references=[r.get('newInputHashes',{}).get(key)for r in (dac,stock)]
  references=[h for h in references if h]
  need(references and all(sha(p)==h for h in references),'Every reused complete native audio/model/source byte bound to actual prior waveform proof '+key)
  pins[key]=sha(p)
 import run_current_ending_audio_v5736 as host
 for side in (1,2):
  for fighter in ('kano','sonya'):
   fn=host.collector(fighter,side);scope=fn.__globals__
   declared=scope['declared_physical_source']
   need(scope['native']is current and scope['model']is model and scope['LUA']==LUA and
    scope['source'].__file__==__file__ and f"MK2KS_CAMPAIGN_SIDE='{side}'"in declared and
    'CREATE_NO_WINDOW'in declared and 'PREVIEW_DATAURL'not in declared and
    all(n in fn.__code__.co_varnames for n in ('pcm_chunks','dac_chunks','dcs_buffers')),
    'Actual entire canonical capture bound to true selected physical slot/current game/RAM-only complete audio parser')
 need(model.predict_waveform is model.original_clock.predict_waveform,
  'Every original integer attosecond/float32/cached-boundary/whole waveform/bit-fault byte retained')
 g,f=model.dac_models(3043);expected,_=model.expected_region(pins);rg,rf=model.rom_models(expected)
 need(g.__globals__['expected_callbacks']==3043 and f.__globals__['dac_gate']is g and
  rg.__globals__['EXPECTED']is expected and rf.__globals__['region_gate']is rg,
  'All full model and actual fault defining namespaces bound before native launch')
 faults=[]
 for before,after,label in [
  ('cpu.PC.value~=0xff836700','cpu.PC.value~=0xff836710','wrong actual final native collision'),
  ('slots[other].hp','slots[side].hp','wrong physical opponent health'),
  ('for n=0,13 do','for n=0,12 do','missing actual audio channel'),
  (' if not active()then return end',' if false then return end','missing complete native DAC window'),
  ("dac.m_buffer:read_block(first*4,a*4)","dac.m_buffer:read_block(first*4,a*4-4)",'missing actual native DAC float'),
  ('frame==completed+300','frame==completed+30','shortened actual native terminal'),
  ('region:read_u32(at)','0','missing actual sound firmware/data bytes')]:
  need(before in executed,'Actual observer source fault, never a vacuous fixture '+label)
  bad=executed.replace(before,after,1)
  try:observer_source(bad)
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Actual altered complete audio source admitted '+label)
  observer_source(executed)
 for p in [proofpath,dacpath,stockpath,Path(__file__),Path(model.__file__),Path(host.__file__),ROOT/OBSERVER,ROOT/LUA,
  ROOT/'mk2ks_native_ending_audio_observer_ram_v4495.lua']:
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Entire actual game/control/observer/model/native clock provenance unchanged')
 return dict(passed=True,sourceOnly=True,characters=['kano','sonya'],physicalSlots=[1,2],
  entireOriginalEndingDACROMObserverAndModelRetained=True,
  actualSourceFaultsRejected=faults,executedObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),
  wholeActualAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,newBuilds=0,rawMediaWritten=0)


if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable pre-boot full ending audio source report')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
