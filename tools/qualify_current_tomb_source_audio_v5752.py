"""Whole current earned Tomb controller and passive DAC/ROM source preflight."""
import ast,hashlib,inspect,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import current_tomb_source_audio_model_v5748 as model
import run_tomb_mirror_audio_ram_v4350 as runtime
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5753_current_tomb_source_audio_source_checked'
OBSERVER='mk2ks_current_tomb_source_audio_observer_v5750.lua'
LUA='mk2ks_current_tomb_source_audio_campaign_v5751.lua'


def once(code,before,after):
 need(code.count(before)==1,'Exact original whole-source adapter '+before)
 return code.replace(before,after,1)


def expected_observer():
 audio=(ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua').read_text()
 audio=audio[audio.index("local device=manager.machine.devices[':maincpu']"):]
 for before,after in [
  ('frame<=origin+749','frame<=origin+1100'),
  ("0xff8be240,0xff8be24f,'actual native Jax arm-rip audio origin'",
   "0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'"),
  ('at~=0xff8be240','at~=0xff8bdfe0'),
  ('p:read_u16(a+0x1f0)~=11',"p:read_u16(a+0x1f0)~=assert(({kano=17,sonya=18})[os.getenv('MK2KS_STAGE_WINNER')])"),
  ("'origin=%d a8=%08X a13=%08X id=11',origin,a,m",
   "'origin=%d a8=%08X a13=%08X id=%d',origin,a,m,p:read_u16(a+0x1f0)")]:audio=once(audio,before,after)
 dac=(ROOT/'mk2ks_current_native_dac_ram_v5592.lua').read_text()
 dac=dac[dac.index('local frame,serial,previous,previous_time='):]
 dac=once(dac," local origin=rawget(_G,'MK2_STOCK_V921_ACTION_START')\n if not origin or frame<origin or frame>origin+749 then return end",
  ' if not active()then return end')
 rom=(ROOT/'mk2ks_current_dcs_rom_source_v5585.lua').read_text()
 rom=rom[rom.index('local region=assert('):]
 rom=once(rom,'checks==2 and frame==5198','checks==2 and origin and frame==origin+1101')
 return ('-- Full original true-mirror Tomb audio, native DAC and sound-ROM observers.\n'
  '-- Passive only; original controller is loaded separately.\n'+audio.rstrip()+'\n'
  '-- Entire qualified5592 DAC observer, only actual Tomb window adapter.\n'+dac.rstrip()+'\n'
  '-- Entire qualified5585 ROM observer, only original Tomb terminal adapter.\n'+rom.rstrip()+'\n')


CAMPAIGN="""-- Original true-ID earned matches and facing commands; passive audio only.
dofile('mk2ks_tomb_mirror_provenance_ram_v4341.lua')
dofile('mk2ks_current_tomb_source_audio_observer_v5750.lua')
local frame=0
emu.register_frame_done(function()
 frame=frame+1
 if emu.time()>=890 then
  print(string.format('MK2_TOMB_SOURCE_HOST_DEADLINE frame=%d writes=0 assistance=none',frame))
  manager.machine:exit()
 end
end)
"""


def observer_source(text=None,campaign=None):
 text=(ROOT/OBSERVER).read_text()if text is None else text
 campaign=(ROOT/LUA).read_text()if campaign is None else campaign
 need(text==expected_observer()and campaign==CAMPAIGN,
  'Entire original15tap/PCM/14channel/DAC/ROM observer and true-ID physical controller retained')
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|set_value|clear_value|load_?state|io\.open|dofile\(|\bload\(|snapshot\(|machine:exit|return\s+data|force_update|flush\(',text),
  'Passive whole observer: no guest/control/identity/health/RNG/palette/sound/cursor writes or forced flushes')
 return text


def run():
 current.expected();executed=observer_source()
 parentpath=ROOT/'audit_v5747_current_four_case_ending_audio_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['actualCurrentFourCaseEndingSourceClockAudioAccepted']and
  parent['goalStatus']=='active','Whole current ending-audio proof and original goal retained')
 pins=dict(parent['inputHashes']);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'Every qualified current native/controller/DAC/clock/ROM byte retained')
 # Preserve the entire legacy earned/two-full-health-KO/physical-command/
 # native action/801field/retirement contract, not activation-only acceptance.
 need(runtime.state.contract_source==runtime.state.native.source.replace(
  'victim = 18 if own == 17 else 17','victim = own'),
  'Exactly one true-mirror identity expectation in whole original earned contract')
 import run_current_tomb_source_audio_v5749 as host
 fn,digest=host.collector()
 need(fn.__globals__['NAME']==current.NAME and fn.__globals__['model']is model and
  fn.__globals__['source'].__file__==__file__ and
  'CREATE_NO_WINDOW'in fn.source and "'-str','900'"in fn.source and
  'MK2KS_STAGE_ARENA=\'1\''in fn.source and '-nocheat'in fn.source and
  'shutil.copy2('not in fn.source and 'run.log.gz'in fn.source and
  all(n in fn.__code__.co_varnames for n in('dac_chunks','dcs_buffers','expected_sound')),
  'Actual entire canonical collector bound to current game, genuine controls and RAM-only native sound buffers')
 need(model.predict_waveform is model.original.predict_waveform,
  'Entire original source-clock float32/cached-view model, no fitted new predictor')
 g,f=model.dac_models(1006)
 need(g.__globals__['callbacks']==1006 and f.__globals__['dac_gate']is g,
  'Whole original DAC and actual faults bound to complete Tomb window namespace')
 expected,_=model.expected_region(pins);rg,rf=model.rom_models(expected)
 need(rg.__globals__['EXPECTED']is expected and rf.__globals__['region_gate']is rg,
  'Entire actual stock-ROM byte/fault gate bound to independent complete source')
 faults=[]
 for before,after,label in [
  ('at~=0xff8bdfe0','at~=0xff8bdff0','wrong original native stage entry'),
  ('cpu.PC.value~=at+16','cpu.PC.value~=at+32','wrong actual instruction-fetch provenance'),
  ('frame<=origin+1100','frame<=origin+500','truncated native stage window'),
  ('for n=0,13 do','for n=0,12 do','missing actual imported channel'),
  (' if not active()then return end',' if false then return end','missing actual native DAC window'),
  ('dac.m_buffer:read_block(first*4,a*4)','dac.m_buffer:read_block(first*4,a*4-4)','missing actual DAC float'),
  ('frame==origin+1101','frame==origin+501','truncated native terminal'),
  ('region:read_u32(at)','0','missing original loaded sound byte')]:
  need(before in executed,'Nonvacuous real whole-source fault '+label)
  try:observer_source(executed.replace(before,after,1))
  except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
  else:raise ValueError('Altered actual full native observer admitted '+label)
  observer_source(executed)
 sources=[Path(__file__),Path(host.__file__),Path(model.__file__),ROOT/OBSERVER,ROOT/LUA,
  Path(runtime.__file__),Path(runtime.old.__file__),Path(runtime.state.__file__),Path(runtime.state.native.__file__),
  Path(runtime.state.native.legacy.__file__),ROOT/'tools/verify_current_tomb_drop_physics_v3618.py',
  ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua',ROOT/'mk2ks_tomb_mirror_driver_ram_v4340.lua',
  ROOT/'mk2ks_current_stage_provenance_v3595.lua',ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',
  ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua',ROOT/'mk2ks_tomb_mirror_audio_ram_v4342.lua']
 for p in sources:
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every full current/source/legacy/native-controller/model input unchanged')
 return dict(passed=True,sourceOnly=True,characters=['kano','sonya'],physicalSlots=[1,2],
  entireOriginalEarnedControllerAndNativeAudioObserversRetained=True,
  executedObserverSHA256=hashlib.sha256(executed.encode()).hexdigest().upper(),transportSourceSHA256=digest,
  actualSourceFaultsRejected=faults,actualCurrentTombWaveformAccepted=False,
  importedWinnerMixedWaveformAccepted=False,completeStageVictimAudioAccepted=False,
  fullPortAcceptance=False,inputHashes=pins,newBuilds=0,rawMediaWritten=0)


if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current Tomb preflight before any boot')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
