"""Actual current Friendship body-group pixel coverage diagnostic.
Every opaque original source pixel must match one unique native render origin.
Missing groups are retained as missing evidence, never treated as passing or
as gameplay bugs without separating occlusion from changed artwork. This is
not complete scene raster, floor shadow, cleanup or all-finisher acceptance.
"""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_friendship_v2655 as scene
ROOT=scene.ROOT
OUT=ROOT/'audit_v2675_current_friendship_body_pixels_diagnostic'
need=scene.need

def verify():
 pins={};cases={}
 def pin(path,wanted=None):
  path=str(path)
  if path in pins:need(wanted is None or pins[path]==wanted,'Consistent original/current artwork dependency');return
  actual=scene.launch.sha(path);need(wanted is None or wanted==actual,'Unchanged original/current artwork dependency '+path);pins[path]=actual
 source=ROOT/'audit_v756_original_friendship_art_checked/verification.json';pin(source)
 oracle=json.loads(source.read_text())
 need(oracle['fullPortAcceptance']==False and oracle['artwork']['kano']['groups']==25 and oracle['artwork']['sonya']['groups']==11,'Complete original body/prop reference scope retained')
 for file,wanted in oracle['checked_inputs'].items():pin(file,wanted)
 reference_path=ROOT/'audit_v755_original_friendship_art/reference.json';pin(reference_path)
 reference=json.loads(reference_path.read_text())
 for file,wanted in reference['input_hashes'].items():pin(file,wanted)
 guest,_,_=scene.current.expected()
 for fighter in ('kano','sonya'):
  body=[record for record in reference['records'][fighter]['groups']if not record['effect']]
  for side in (1,2):
   folder=ROOT/f'audit_v2653_current_{fighter}_friendship_p{side}'
   proof_path=ROOT/f'audit_v2656_current_{fighter}_friendship_p{side}_checked/report.json';pin(proof_path)
   proof=json.loads(proof_path.read_text())
   need(proof['passed']and proof['currentBuildPhysicalFriendshipAccepted'],'Actual current physical Friendship scene accepted')
   for file,wanted in proof['inputHashes'].items():pin(file,wanted)
   need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual current guest independently reconstructed')
   rows=scene.previous.parse(folder/'run.log');scene.check(rows,fighter,side);poses=scene.previous.select(rows,'POSE')
   images={};matches=[];missing=[];attempts={}
   for record in body:
    asset=reference_path.parent/record['file'];pin(asset)
    sprite=np.asarray(Image.open(asset).convert('RGBA'))
    need(hashlib.sha256(sprite.tobytes()).hexdigest()==record['rgba_sha256'].upper().lower(),'Exact original RGBA pixels')
    starts=[(index,row)for index,row in enumerate(poses)if int(row['pose'],16)+0x1000000==record['group']]
    need(starts,'Actual native body choreography includes original group')
    candidates=[]
    for index,row in starts:
     first=int(row['age']);end=int(poses[index+1]['age'])if index+1<len(poses)else min(first+16,198)
     candidates.extend(range(first+1,min(end,198)+1))
    candidates=sorted(set(candidates));match=None
    for age in candidates:
     path=folder/'snap'/f'native_field_{age}.png'
     if not path.is_file():continue
     pin(path)
     if age not in images:images[age]=np.asarray(Image.open(path).convert('RGB'))
     actual=images[age]
     for flip in (False,True):
      try:origin,pixels=scene.previous.image_match(actual,sprite[:,::-1]if flip else sprite)
      except ValueError:continue
      match=dict(group=f'{record["group"]:08X}',age=age,flip=flip,origin=origin,opaquePixels=pixels,render=str(path));break
     if match:break
    attempts[f'{record["group"]:08X}']=candidates
    if match:matches.append(match)
    else:missing.append(f'{record["group"]:08X}')
   cases[f'{fighter}_p{side}']=dict(originalBodyGroups=len(body),exactMatchedBodyGroups=len(matches),matches=matches,
    missingOriginalBodyGroups=missing,candidateAgesByGroup=attempts,allOriginalBodyGroupsPixelMatched=not missing)
   print(f'{fighter}_p{side}: {len(matches)}/{len(body)} complete original body groups matched; missing={missing}',flush=True)
 pin(Path(__file__).resolve());scene.launch.module_pins(pins)
 return dict(passed=True,diagnosticCompleted=True,cases=cases,inputHashes=pins,
  currentAllOriginalBodyGroupsBothSlotsPixelMatched=all(case['allOriginalBodyGroupsPixelMatched']for case in cases.values()),
  missingGroupsAreUnacceptedNotInferredBugs=True,completeSceneRasterShadowAudioAccepted=False,gameChanged=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable current body-group coverage diagnostic')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in ('cases','inputHashes')},indent=2),flush=True)
