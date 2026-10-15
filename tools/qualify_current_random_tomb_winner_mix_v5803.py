"""Whole physical unpressed Tomb random branch, current enabled source gate."""
import ast,inspect,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_pressed_tomb_winner_mix_v5792 as previous
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5804_current_random_tomb_winner_mix_source_checked'
DRIVER_INSERT="local delay=assert(tonumber(os.getenv('MK2KS_TOMB_COMMAND_DELAY')))\nassert(delay>=1 and delay<=80 and delay==math.floor(delay),'Declared physical command delay only')\nreplace('frame-window>=65 then','frame-window>='..(65+delay)..' then')\nprint(string.format('MK2_TOMB_TIMING_CONFIGURATION delay=%d writes=0 assistance=none',delay))\n"

def run():
 current.expected()
 parentpath=ROOT/'audit_v5798_current_pressed_tomb_enabled_winner_mix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentHeldAndPressedEnabledWinnerMixAccepted'],
  'Completed current held/pressed source-exact mixer and all original goal groups retained')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'Every retained actual input/source/evidence intact')
 import run_current_random_tomb_winner_mix_v5802 as host
 import run_current_pressed_tomb_winner_mix_v5790 as old
 prepath=previous.OUT/'report.json';pre=json.loads(prepath.read_text())
 need(pre['passed']and all(sha(p)==h for p,h in pre['inputHashes'].items()),
  'Whole original mixer/raw faults/compiled route/clip/observer source qualification retained')
 pins[str(prepath)]=sha(prepath)
 driver=(ROOT/'mk2ks_tomb_mirror_driver_ram_v4340.lua').read_text()
 wanted=driver.replace('assert(load(source,',DRIVER_INSERT+'assert(load(source,',1)
 need((ROOT/'mk2ks_current_random_tomb_driver_v5799.lua').read_text()==wanted,
  'Whole original earned true-ID driver retained; only physical command delay added, no RNG/state writes')
 provenance=(ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua').read_text().replace(
  'mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_current_random_tomb_driver_v5799.lua')
 need((ROOT/'mk2ks_current_random_tomb_provenance_v5800.lua').read_text()==provenance,
  'Whole original source PC/actor/Main/control/motion provenance unchanged')
 top=(ROOT/old.LUA).read_text().replace(
  '-- Whole original earned mirror Tomb; real both-Down and passive enabled mix.',
  '-- Whole original earned mirror Tomb; ordinary delayed command, no held Down.').replace(
  'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_random_tomb_provenance_v5800.lua')
 need((ROOT/host.LUA).read_text()==top and host.OBSERVER==old.OBSERVER,
  'Whole original1100window/retirement/passive deadline and precise sound observer retained')
 fn,digest=host.collector();prior,_=old.collector()
 expected=prior.source.replace('audit_v5794_current_pressed_tomb_winner_mix_','audit_v5805_current_random_tomb_winner_mix_').replace(
  old.LUA,host.LUA).replace('mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua','mk2ks_current_random_tomb_driver_v5799.lua').replace(
  'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_current_random_tomb_provenance_v5800.lua').replace(
  "MK2KS_STAGE_OUT=str(folder))","MK2KS_STAGE_OUT=str(folder),MK2KS_TOMB_COMMAND_DELAY=str(physical_delay(fighter,side)))")
 need(fn.source==expected and fn.__globals__['NAME']==current.NAME and
  fn.__globals__['state']is host.pressed and fn.__globals__['model']is old.model and
  fn.__globals__['source']is __import__(__name__)and fn.__globals__['physical_delay']is host.physical_delay and
  "fn(fighter,side,True,guest)"in Path(host.__file__).read_text(),
  'Whole cold gzip RAM/DAC/ROM/PCM collector unchanged except declared driver, delay and destinations; actual bound full contract and enabled samples')
 host.runtime.preflight()
 need(host.pressed.contract_source==host.pressed.native.source.replace('victim = 18 if own == 17 else 17','victim = own')and
  host.pressed.drop_source==inspect.getsource(host.pressed.native.qualify_drop).replace(
   "victim_id=18 if fighter=='kano'else 17","victim_id=17 if fighter=='kano'else 18"),
  'Whole1731earned/801cleanup and original3643unpressed source/RNG/269phase gates retained, real mirror only')
 vg,vf=host.voice_models()
 need(vg.source==inspect.getsource(host.original_voice.qualify_scream).replace(
  "'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA))and
  vf.__globals__['qualify_scream']is vg,
  'Whole native late Main-role/female/caller/RNG voice and eight actual faults retained')
 for p in (Path(__file__),Path(host.__file__),Path(host.original_branches.__file__),Path(host.pressed.__file__),
  ROOT/host.LUA,ROOT/'mk2ks_current_random_tomb_driver_v5799.lua',ROOT/'mk2ks_current_random_tomb_provenance_v5800.lua'):
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All exact executed source/native/control inputs stable before boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,
  wholeEarnedRandomContractSHA256=host.pressed.CONTRACT_SHA256,
  wholeOriginalRandomDropContractSHA256=host.pressed.DROP_SHA256,
  actualCurrentNaturalRandomDropEnabledMixerAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable whole current unpressed source preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
