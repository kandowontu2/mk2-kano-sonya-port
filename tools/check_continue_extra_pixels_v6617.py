"""Actual own ladder icon plus additional effective native image regressions.

Uses the terminal host's unchanged native buffers. Its image faults are test
copies in RAM, never supplied to the game or saved as native screenshots.
"""
import json,hashlib,subprocess
from pathlib import Path
import numpy as np
import continue_viewport_contract_v6610 as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha

def check(folder,text,images,fighter,side,target):
 folder=Path(folder);proof=ROOT/f'audit_v6615_continue_viewport_checked_{fighter}_p{side}_to_{target}/report.json'
 old=json.loads(proof.read_text());need(old['passed']and all(sha(p)==h for p,h in old['inputHashes'].items()),'Same actual qualified native inputs intact')
 out=ROOT/f'audit_v6618_continue_extra_pixels_{fighter}_p{side}_to_{target}'
 need(not out.exists(),'New separate actual-pixel proof')
 load=lambda name:np.frombuffer(images[(int(name[3:7]),name)],np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
 for q in old['actualFullRGBDigests']:
  need(hashlib.sha256(images[(q['frame'],q['label'])]).hexdigest().upper()==q['sha256'],'Every actual native pixel/alpha buffer intact')
 ui=(ROOT/'roms/mk2ks/mk2ks.ui').read_bytes();template=contract.model.portrait(ui,0 if target=='kano'else 1,35,45)
 exit_at=old['actualSinglePlayerContinue']['actualUIState']['exit'];snaps=contract.model.records(text,'SNAP')
 settled=[q for q in snaps if q['scene']=='transition'and exit_at+2<=int(q['frame'])<=exit_at+100]
 own=[q for q in contract.model.records(text,'LADDER_OBJECT')if q['id']==str(17 if target=='kano'else 18)and
      int(q['xraw'],16)==146<<16 and exit_at+2<=int(q['frame'])<=exit_at+100]
 need([int(q['frame'])for q in own]==list(range(exit_at+2,exit_at+101))and
      len({q['actor']for q in own})==len({q['born']for q in own})==1 and
      all(q['yraw']=='009B0000'and q['flags']=='0001'for q in own),
      'Every actual screen-fixed selected player icon allocation/position field')
 matches=[int(q['frame'])for q in settled if np.array_equal(load(q['file'])[158:203,128:163],template)]
 need(len(matches)>=3,'Repeated complete selected player ladder portrait equals own source, not CPU/proxy')
 faults=[]
 def reject(label,changed_load):
  try:contract.render(folder,text,target,side,load=changed_load)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('Actual image regression admitted: '+label)
 if fighter=='kano'and side==1:
  selected=next(q for q in snaps if q['scene']=='select'and 54<=int(q['age'])<=70)['file']
  def shifted(name):
   a=load(name)
   if name==selected:
    x=5 if side==1 else 325;a[106:242,x:x+70]=np.roll(a[106:242,x:x+70],1,axis=1)
   return a
  reject('one-pixel selected backdrop shift',shifted)
 if fighter=='kano'and side==2:
  changed={q['file']for q in snaps if int(q['frame'])>=exit_at}
  def lingering(name):
   a=load(name)
   if name in changed:a[24:94,23:78]=contract.model.portrait(ui,0,55,70)
   return a
  reject('CSS portrait retained during ladder/match',lingering)
 if fighter=='sonya'and side==1:
  locked=next(q for q in reversed(snaps)if q['scene']=='select'and int(q['age'])>=260)
  pose=load(locked['file'])[106:242,5:75].copy();changed={q['file']for q in snaps if q['scene']=='transition'}
  def lingering_pose(name):
   a=load(name)
   if name in changed:a[106:242,5:75]=pose
   return a
  reject('locked character pose retained during ladder',lingering_pose)
 if fighter=='sonya'and side==2:
  top=old['actualUIPixels']['continuedViewport']['objects']['18']['projectedTop']
  changed={q['file']for q in snaps if q['scene']=='transition'}
  def erased_icon(name):
   a=load(name)
   if name in changed:a[top:top+45,248:283]=0
   return a
  reject('visible scheduled Sonya ladder portrait missing',erased_icon)
  fight=next(q for q in snaps if q['scene']=='fight'and int(q['age'])>=60)['file']
  face,edge,x=contract.model.shadow(ui,18,side)
  def erased_name_shadow(name):
   a=load(name)
   if name==fight:a[30:40,x:x+face.shape[1]][edge]=[255,255,0]
   return a
  reject('missing native lifebar-name black-shadow pen',erased_name_shadow)
 # Own-icon check must independently reject removal of every observed copy.
 bad_matches=[]
 for q in settled:
  actual=load(q['file']);changed=actual.copy();changed[158:203,128:163]=0
  need(not np.array_equal(actual,changed),'Effective actual native player-portrait erasure')
  if np.array_equal(changed[158:203,128:163],template):bad_matches.append(int(q['frame']))
 need(len(bad_matches)<3,'Missing player ladder icon is actually rejected')
 faults.append(dict(kind='missing selected player ladder portrait',rejectedBy='Fewer than3 complete own-source native portrait matches',mutatedNativeSnapshots=len(settled)))
 restored=contract.render(folder,text,target,side,load=load)
 need(json.loads(json.dumps(restored))==old['actualUIPixels'],'Full JSON-equivalent native viewport/name/teardown positive restored after image faults')
 pins={str(p.resolve()):sha(p)for p in [proof,Path(__file__),*contract.DEPENDENCIES]}
 result=dict(passed=True,case=dict(fighter=fighter,side=side,target=target),nativeCapture=str(folder),
  selectedPlayerLadderIcon=dict(nativeObjectFields=len(own),fullSourceRasterMatches=len(matches),firstFrame=matches[0],position=[128,158]),
  additionalActualImageFaultsRejected=faults,inputHashes=pins,rawPixelsOnlyInHostRAM=True,
  fullPortAcceptance=False,goalStatus='active',newBuilds=0,newROMCopies=0)
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Lossless additional pixel proof')
 print(json.dumps(result['selectedPlayerLadderIcon']|dict(passed=True,faults=len(faults))),flush=True)
 return result
