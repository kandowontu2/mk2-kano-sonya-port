"""Current whole native pressed Tomb preflight: no forced stage or RNG."""
import ast,inspect,json,re
from pathlib import Path
import qualify_current_tomb_source_audio_v5752 as previous
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5760_current_pressed_tomb_audio_source_checked'
LUA='mk2ks_current_pressed_tomb_source_audio_v5757.lua'


def run():
 current.expected()
 parentpath=previous.OUT/'report.json';parent=json.loads(parentpath.read_text())
 need(parent['passed']and len(parent['actualSourceFaultsRejected'])==8,'Whole current passive observer/ROM/clock qualification retained')
 pins=dict(parent['inputHashes']);pins[str(parentpath)]=sha(parentpath)
 heldpath=ROOT/'audit_v5756_current_tomb_native_source_audio_matrix_checked/report.json'
 held=json.loads(heldpath.read_text())
 need(held['passed']and len(held['cases'])==4 and held['actualCurrentBothCharactersBothSidesHeldTombNativeDCSAudioAccepted'],
  'Actual current four-case held native sound matrix retained; not rerun or relabeled as pressed')
 pins.update(held['inputHashes']);pins[str(heldpath)]=sha(heldpath)
 need(all(sha(p)==h for p,h in pins.items()),'All retained current/stock/controller/source proofs intact before boot')
 previous.observer_source()
 expected=previous.CAMPAIGN.replace('-- Original true-ID earned matches and facing commands; passive audio only.',
  '-- Complete original earned mirror campaign; real physical both-Down branch.').replace(
  'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua')
 need((ROOT/LUA).read_text()==expected,'Complete controller/observer/window/deadline wrapper; only genuine pressed driver changes')
 driver=ROOT/'mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua'
 provenance=ROOT/'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua'
 need(sha(driver)=='C04395834FC0E026044FD9A88F150CC277C00D83778E8FF09107EDC2A7A4DFAA'and
  sha(provenance)=='061176D39896E4706336D26185FBBCC62E29538F5F3279D7DCF43DE4EA2B7761',
  'Whole original pressed physical controller and exact PC-qualified observer unchanged')
 import run_current_pressed_tomb_audio_v5758 as host
 import run_current_tomb_source_audio_v5749 as oldhost
 fn,digest=host.collector();oldfn,_=oldhost.collector()
 wanted=oldfn.source.replace('audit_v5754_current_tomb_source_audio_','audit_v5761_current_pressed_tomb_source_audio_').replace(
  'mk2ks_current_tomb_source_audio_campaign_v5751.lua',LUA).replace(
  'mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua')
 extra="    files.update(ROOT/p for p in ('mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua'))\n    files.update(Path(p.__file__)for p in (pressed,original_voice))\n"
 marker="    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}"
 wanted=host.once(wanted,marker,extra+marker)
 need(fn.source==wanted and fn.__globals__['NAME']==current.NAME and
  fn.__globals__['state']is host.pressed and fn.__globals__['pressed']is host.pressed and
  fn.__globals__['source'].__file__==__file__ and fn.__globals__['model']is host.model,
  'Entire qualified cold capture preserved byte-for-byte apart from output/wrapper/full pressed source inventory; actual bindings checked')
 need(host.pressed.contract_source==host.pressed.old.contract_source.replace(
  'qualify_drop(log,fighter,side,arena,case,guest)','qualify_pressed_drop(log,fighter,side,arena,case,guest)'),
  'Whole original earned1731/current true-ID/full cleanup contract, only separate source-qualified physical pressed branch')
 vg,vf=host.voice_models()
 need(vg.source==inspect.getsource(host.original_voice.qualify_scream).replace(
  "'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA))and
  vf.__globals__['qualify_scream']is vg,
  'Whole original owned native Main-role/female/RNG/caller voice gate and eight actual faults, only exact current whole guest hash')
 need(host.model.predict_waveform is host.model.original.predict_waveform,'Unchanged whole source-clock native mixer oracle')
 for p in (Path(__file__),Path(host.__file__),ROOT/LUA,driver,provenance,
  Path(host.pressed.__file__),Path(host.original_voice.__file__),Path(oldhost.__file__)):
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All complete current/native/physical/source/model inputs unchanged')
 return dict(passed=True,sourceOnly=True,characters=['kano','sonya'],physicalSlots=[1,2],
  transportSourceSHA256=digest,wholeEarnedPressedContractSHA256=host.pressed.CONTRACT_SHA256,
  wholeNativeVoiceSourceSHA256=sha(host.original_voice.__file__),inputHashes=pins,
  actualCurrentPressedTombAccepted=False,importedWinnerMixedWaveformAccepted=False,
  completeStageVictimAudioAccepted=False,fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)


if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable current full pressed preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
