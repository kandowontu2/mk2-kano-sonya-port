"""Current samples-disabled baselines preserve every actual native scene record.
This isolates audible sample output without gameplay/identity/timing changes.
It does not accept PCM fidelity, all-scene shadows or complete Friendship audio.
"""
import json,copy
from pathlib import Path
import verify_current_friendship_v2655 as scene
ROOT=scene.ROOT;launch=scene.launch
OUT=ROOT/'audit_v2669_current_friendship_audio_baselines_checked'

def need(ok,label):
 if not ok:raise ValueError(label)

def exact(a,b):
 need(a==b,'Every actual physical input/native state/ownership/pose/part/win/audio-command record matches the samples-enabled case')

def verify():
 pins={};cases={}
 def pin(path,wanted=None):
  path=str(path)
  if path in pins:need(wanted is None or pins[path]==wanted,'Consistent actual dependency '+path);return
  actual=launch.sha(path);need(wanted is None or actual==wanted,'Unchanged actual dependency '+path);pins[path]=actual
 guest,_,payload=scene.current.expected()
 build=json.loads((ROOT/scene.current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 for fighter in ('kano','sonya'):
  for side in (1,2):
   positive=ROOT/f'audit_v2653_current_{fighter}_friendship_p{side}'
   proof_path=ROOT/f'audit_v2656_current_{fighter}_friendship_p{side}_checked/report.json'
   proof=json.loads(proof_path.read_text())
   need(proof['passed']and proof['currentBuildPhysicalFriendshipAccepted']and not proof['fullPortAcceptance'],'Accepted current actual physical Friendship')
   for file,wanted in proof['inputHashes'].items():pin(file,wanted)
   pin(proof_path)
   folder=ROOT/f'audit_v2667_current_{fighter}_friendship_nosamples_p{side}'
   meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
   need(meta['exit_code']==0 and not meta['samples_enabled']and meta['winner']==fighter and meta['side']==side and meta['command_case']=='positive'and
    meta['guest_writes']==0 and meta['assistance']=='none'and meta['candidate']==scene.current.NAME and meta['executable_sha256']==build['executable_sha256']and
    meta['payload_sha256']==build['payload_sha256']and before==meta['input_hashes'],'Actual matched current terminal samples-disabled baseline')
   for file,wanted in before.items():
    pin(file,wanted)
    if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
   need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/scene.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual unchanged guest/payload source reconstruction')
   a=scene.previous.parse(positive/'run.log');b=scene.previous.parse(folder/'run.log');exact(a,b)
   control=scene.check(b,fighter,side)
   indices=[next(i for i,(tag,row)in enumerate(b)if tag==kind)for kind in ('WIN','DAMAGE','AUDIO')]
   corruptions=[]
   for kind,index in zip(('missing_actual_win','changed_actual_damage','shifted_actual_audio_cue'),indices):
    changed=copy.deepcopy(b)
    if kind=='missing_actual_win':changed.pop(index)
    elif kind=='changed_actual_damage':changed[index][1]['after']=str(int(changed[index][1]['after'])-1)
    else:changed[index][1]['frame']=str(int(changed[index][1]['frame'])+1)
    need(changed!=b,'Non-vacuous actual baseline mutation')
    try:exact(a,changed)
    except ValueError as error:
     need('Every actual physical input'in str(error),'Intended exact actual native chronology rejection');corruptions.append(kind)
    else:raise ValueError('Changed actual baseline accepted '+kind)
   exact(a,b);need(scene.check(b,fighter,side)==control,'Final untouched samples-disabled current scene control')
   for name in ('run.log','result.json','inputs_before.json','guest_maincpu.bin','native_mix.wav'):pin(folder/name)
   need(launch.sha(folder/'native_mix.wav')==meta['mix_sha256'],'Actual baseline PCM capture matches terminal metadata')
   cases[f'{fighter}_p{side}']=dict(exactNativeSceneRecords=len(b),exactNativeOwnWins=2,
    originalTrueFighterID=control['actualTrueFighterID'],rejectedSpecificChronologyCounterexamples=corruptions,
    finalUnmodifiedControlPassed=True,samplesDisabledOnly=True,actualAudioCommands=sum(tag=='AUDIO'for tag,row in b),
    capture=str(folder),acceptedCurrentPositiveScene=str(proof_path))
 pin(Path(__file__).resolve());launch.module_pins(pins)
 return dict(passed=True,cases=cases,samplesSettingNeverChangedGameplay=True,
  wholeActualGuestAndPayloadReconstructed=True,inputHashes=pins,gameChanged=False,
  originalPCMAndAudibleOverlapAccepted=False,completeSceneRasterShadowAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable current audio baseline chronology proof')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='inputHashes'},indent=2),flush=True)
