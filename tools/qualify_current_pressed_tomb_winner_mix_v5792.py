"""Current full physical pressed Tomb, exact enabled mixer and actual faults."""
import ast,inspect,json,re
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import qualify_current_tomb_winner_mix_v5782 as held
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v5793_current_pressed_tomb_winner_mix_source_checked'
INSERT=" raw_faults=[];source_faults=[]\n if not len(different):\n  # Alter copies of the actual native PCM in RAM, never guest or audio state.\n  for label,index,channel in [('actual first PCM sample',0,0),('actual final PCM sample',len(pcm)-1,1)]:\n   bad=pcm.copy();bad[index,channel]^=1\n   need(not np.array_equal(predicted,bad),'Actual changed PCM must fail full source equality')\n   raw_faults.append(dict(label=label,rejectedBy='complete source equality',differentChannelSamples=int(np.count_nonzero(predicted!=bad))))\n   need(np.array_equal(predicted,pcm),'Whole actual positive restored after raw bit counterexample')\n  need(predicted.shape!=pcm[:-1].shape,'Actual omitted last stereo frame rejected')\n  raw_faults.append(dict(label='actual last stereo frame omitted',rejectedBy='complete source shape',actualFrames=len(pcm)-1))\n  bad=pcm[1:].copy()\n  need(predicted.shape!=bad.shape,'Actual omitted first cached speaker value rejected')\n  raw_faults.append(dict(label='actual first cached stereo frame omitted',rejectedBy='complete source shape',actualFrames=len(bad)))\n  convert=lambda value:(np.clip(value,-1,1).astype(np.float64)*32767.0).astype('<i2')\n  late=np.zeros_like(voice);late[1:]=voice[:-1]\n  native_integer=convert(dcs).astype('<f4')/np.float32(32767.0)\n  for label,wrong in [\n   ('winner source omitted',convert(dcs)),\n   ('one-sample source-start clock late',convert(np.float32(dcs+late))),\n   ('original .70 route gain omitted',convert(np.float32(dcs+np.float32(voice/np.float32(.70))))),\n   ('native source quantized before speaker addition',convert(np.float32(native_integer+voice)))]:\n   need(wrong.shape==pcm.shape and not np.array_equal(wrong,predicted)and not np.array_equal(wrong,pcm),\n    'Nonvacuous whole source-operation fault rejected '+label)\n   source_faults.append(dict(label=label,rejectedBy='complete actual native mixed waveform',\n    differentChannelSamples=int(np.count_nonzero(wrong!=pcm))))\n   need(np.array_equal(predicted,pcm),'Entire source-positive restored after every operation fault')\n return dict(passed=not len(different),actualRawMixedPCMFaultsRejected=raw_faults,\n  actualMixedSourceOperationFaultsRejected=source_faults,\n  actualMixedRawPCMByteFaultSuiteAccepted=not len(different)and len(raw_faults)==4 and len(source_faults)==4,\n  comparedStereoFrames=len(pcm),differentChannelSamples=len(different),"


def run():
 current.expected()
 parentpath=ROOT/'audit_v5788_current_enabled_tomb_winner_mix_progress/progress.json'
 parent=json.loads(parentpath.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5 and
  parent['actualCurrentBothCharactersBothSlotsHeldTombEnabledWinnerMixAccepted'],
  'Completed full held four-case enabled mixer/precise channel/retirement proof retained, full original scope unchanged')
 pins=dict(parent['newInputHashes']);pins[str(parentpath)]=sha(parentpath)
 need(all(sha(p)==h for p,h in pins.items()),'All authoritative native/current/physical/model inputs intact')
 import run_current_pressed_tomb_winner_mix_v5790 as host
 import run_current_pressed_tomb_audio_v5764 as original
 hpre=held.OUT/'report.json';qualified=json.loads(hpre.read_text())
 need(qualified['passed']and all(sha(p)==h for p,h in qualified['inputHashes'].items()),
  'Whole enabled observer, compiled14channel center speaker/.70/.30 dispatch,16000Hz original clips and native float carrier qualified')
 pins[str(hpre)]=sha(hpre)
 need((ROOT/host.OBSERVER).read_text()==(ROOT/'mk2ks_current_tomb_source_audio_observer_v5750.lua').read_text().rstrip()+'\n'+held.EXTRA,
  'Whole original passive stage/DAC/ROM/PCM plus exact14callback snapshots unchanged')
 wanted=(ROOT/'mk2ks_current_tomb_winner_mix_campaign_v5780.lua').read_text().replace(
  '-- Whole original earned held Tomb campaign; passive full enabled audio.',
  '-- Whole original earned mirror Tomb; real both-Down and passive enabled mix.').replace(
  'mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua')
 need((ROOT/host.LUA).read_text()==wanted,'Whole earned controller/retirement/window/deadline, only real physical pressed driver')
 fn,digest=host.collector();oldfn,_=original.collector()
 expected=oldfn.source.replace('audit_v5765_current_pressed_tomb_source_audio_','audit_v5794_current_pressed_tomb_winner_mix_').replace(
  original.LUA,host.LUA)
 need(fn.source==expected and fn.__globals__['NAME']==current.NAME and fn.__globals__['state']is host.pressed and
  fn.__globals__['model']is host.model and fn.__globals__['source'].__file__==__file__ and
  fn.__globals__['OBSERVER']==host.OBSERVER and "fn(fighter,side,True,guest)"in Path(host.__file__).read_text(),
  'Entire bounded cold pressed transport/namespace retained and genuinely enabled at callsite, no forced guest state')
 need(host.pressed.contract_source==host.pressed.old.contract_source.replace(
  'qualify_drop(log,fighter,side,arena,case,guest)','qualify_pressed_drop(log,fighter,side,arena,case,guest)'),
  'Whole earned1731/801cleanup and source-qualified actual both-Down/269motion contract')
 vg,vf=host.voice_models()
 need(vg.source==inspect.getsource(host.original_voice.qualify_scream).replace(
  "'938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821'",repr(current.GUEST_SHA))and
  vf.__globals__['qualify_scream']is vg,'Whole actual Main-role/female/RNG voice and its original eight real faults retained')
 before=" return dict(passed=not len(different),comparedStereoFrames=len(pcm),differentChannelSamples=len(different),"
 original_model=(ROOT/'tools/current_tomb_winner_mix_model_v5778.py').read_text()
 need(original_model.count(before)==1 and Path(host.model.__file__).read_text()==original_model.replace(before,INSERT,1),
  'Entire source-exact enabled mixer unchanged, only actual RAM PCM/source-operation counterexamples added before report')
 need(host.model.float_model().source==__import__('current_tomb_winner_mix_model_v5778').float_model().source,
  'Whole original native float32/cache carrier identical; no timing/gain/sample fitting')
 for fighter in ('kano','sonya'):host.model.read_winner(fighter,pins)
 for p in (Path(__file__),Path(host.__file__),Path(host.model.__file__),ROOT/host.LUA,ROOT/host.OBSERVER,
  Path(original.__file__),Path(host.pressed.__file__),Path(host.original_voice.__file__)):
  if p.suffix=='.py':ast.parse(p.read_text())
  pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Whole current native/controller/source/model bytes intact before actual boot')
 return dict(passed=True,sourceOnly=True,inputHashes=pins,transportSourceSHA256=digest,
  wholeEarnedPressedContractSHA256=host.pressed.CONTRACT_SHA256,
  actualPressedEnabledMixerAccepted=False,actualRawMixedPCMByteFaultSuiteAccepted=False,
  fullPortAcceptance=False,newBuilds=0,rawMediaWritten=0)


if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable complete pressed enabled-mixer preflight')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
