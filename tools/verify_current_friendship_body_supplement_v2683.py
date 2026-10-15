"""Current original Friendship body groups in both slots, one arena/two gaps.
Supplement the actual P2 Sonya capture with normal physical gap-140 movement.
The exact original scene/control remains unchanged apart from retreat distance
and filenames. Preserve the gap-160 obscured groups as unaccepted evidence.
This is not whole-scene raster, floor-shadow, all-arena or finisher acceptance.
"""
import copy,hashlib,json,re
from pathlib import Path
import numpy as np
from PIL import Image
import verify_current_friendship_v2655 as scene
import verify_native_friendship_audio_v791 as audio
ROOT=scene.ROOT
OUT=ROOT/'audit_v2684_current_friendship_body_supplement_checked'
FOLDER=ROOT/'audit_v2682_current_sonya_friendship_gap140_p2'
need=scene.need

def text(path):return path.read_text().rstrip()+'\n'

def check(rows):
 result=scene.check(rows,'sonya',2)
 position=scene.previous.select(rows,'COMMAND_POSITION')
 need(len(position)==1 and 140<=int(position[0]['gap'])<146,'Actual physical gap-140 command position')
 result['audioCueChronology']=audio.runtime(rows,'sonya',2,'positive')
 return result

def match(actual,sprite):
 found=[]
 for flip in (False,True):
  try:origin,pixels=scene.previous.image_match(actual,sprite[:,::-1]if flip else sprite)
  except ValueError:continue
  found.append(dict(flip=flip,origin=origin,opaquePixels=pixels))
 need(len(found)==1,'Every original opaque body pixel at one unique native origin/facing')
 return found[0]

def reject(call,label,expected):
 try:call()
 except ValueError as error:
  need(expected in str(error),'Intended body/control invariant for '+label+': '+str(error))
  return dict(name=label,rejectedBy=str(error))
 raise ValueError('Specific malformed original-body evidence accepted '+label)

def verify():
 pins={}
 def pin(path,wanted=None):
  path=str(path)
  if path in pins:need(wanted is None or pins[path]==wanted,'Consistent actual current dependency');return
  actual=scene.launch.sha(path);need(wanted is None or actual==wanted,'Unchanged actual current dependency '+path);pins[path]=actual
 diagnostic_path=ROOT/'audit_v2675_current_friendship_body_pixels_diagnostic/report.json';pin(diagnostic_path)
 diagnostic=json.loads(diagnostic_path.read_text())
 need(diagnostic['passed']and diagnostic['diagnosticCompleted']and not diagnostic['currentAllOriginalBodyGroupsBothSlotsPixelMatched'],'Prior partial body coverage retained, not silently promoted')
 for file,wanted in diagnostic['inputHashes'].items():pin(file,wanted)
 prior=diagnostic['cases']
 need(prior['kano_p1']['exactMatchedBodyGroups']==prior['kano_p2']['exactMatchedBodyGroups']==18 and prior['sonya_p1']['exactMatchedBodyGroups']==11 and prior['sonya_p2']['exactMatchedBodyGroups']==9 and prior['sonya_p2']['missingOriginalBodyGroups']==['FF9D3070','FF9D30F0'],'Exact original gap-160 missing evidence retained')
 base=ROOT/'mk2ks_native_friendship_probe_v784.lua';new=ROOT/'mk2ks_current_friendship_gap140_v2678.lua'
 need(text(base).count('if math.abs(h.x-v.x)<160 then')==1 and text(base).replace('if math.abs(h.x-v.x)<160 then','if math.abs(h.x-v.x)<140 then')==text(new),'Sole physical retreat distance change; no guest assistance')
 a=ROOT/'mk2ks_native_friendship_audio_v790.lua';b=ROOT/'mk2ks_current_friendship_gap140_audio_v2679.lua'
 need(text(a).replace('mk2ks_native_friendship_probe_v784.lua','mk2ks_current_friendship_gap140_v2678.lua')==text(b),'Read-only audio observer changes only physical control filename')
 a=ROOT/'mk2ks_current_friendship_wins_v2651.lua';b=ROOT/'mk2ks_current_friendship_gap140_wins_v2680.lua'
 need(text(a).replace('mk2ks_native_friendship_audio_v790.lua','mk2ks_current_friendship_gap140_audio_v2679.lua')==text(b),'Read-only winner observer changes only audio observer filename')
 source=ROOT/'tools/run_current_friendship_v2650.ps1';runner=ROOT/'tools/run_current_friendship_gap140_v2681.ps1'
 expected=text(source).replace('mk2ks_current_friendship_wins_v2651.lua','mk2ks_current_friendship_gap140_wins_v2680.lua')
 expected=expected.replace('"$root/mk2ks_native_friendship_audio_v790.lua","$root/mk2ks_native_friendship_probe_v784.lua",','"$root/mk2ks_current_friendship_gap140_audio_v2679.lua","$root/mk2ks_current_friendship_gap140_v2678.lua","$root/mk2ks_current_friendship_wins_v2651.lua","$root/mk2ks_native_friendship_audio_v790.lua","$root/mk2ks_native_friendship_probe_v784.lua",')
 expected=expected.replace('command_case=$CommandCase;samples_enabled=','command_case=$CommandCase;requested_gap=140;samples_enabled=')
 need(expected==text(runner),'Exact current launcher, same gameplay build/settings; only filenames/tracking and requested-gap metadata changed')
 for path in (base,new,ROOT/'mk2ks_native_friendship_audio_v790.lua',ROOT/'mk2ks_current_friendship_gap140_audio_v2679.lua',ROOT/'mk2ks_current_friendship_wins_v2651.lua',ROOT/'mk2ks_current_friendship_gap140_wins_v2680.lua',source,runner):
  pin(path)
  if path.suffix=='.lua':need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)',text(path)),'No guest/register/loaded-state writes')
 meta=json.loads((FOLDER/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((FOLDER/'inputs_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/scene.current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['candidate']==scene.current.NAME and meta['winner']=='sonya'and meta['side']==2 and meta['requested_gap']==140 and meta['command_case']=='positive'and meta['samples_enabled']and meta['guest_writes']==0 and meta['assistance']=='none'and before==meta['input_hashes']and meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256'],'Actual complete cold unchanged-build physical supplement')
 need(all(before.get(file)==wanted for file,wanted in build['input_hashes'].items()),'All actual compiled inputs match the current executable')
 for file,wanted in before.items():
  pin(file,wanted)
  if Path(file).suffix in ('.lua','.ps1','.json'):pin(FOLDER/'input_sources'/Path(file).name,wanted)
 guest,_,payload=scene.current.expected()
 need((FOLDER/'guest_maincpu.bin').read_bytes()==guest and (ROOT/scene.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual current guest/payload independently reconstructed')
 rows=scene.previous.parse(FOLDER/'run.log');control=check(rows)
 original_rows=scene.previous.parse(ROOT/'audit_v2653_current_sonya_friendship_p2/run.log')
 window=int(scene.previous.select(rows,'WINDOW')[0]['frame'])
 prefix=lambda rs:[(tag,row)for tag,row in rs if int(row['frame'])<=window and tag!='RESULT']
 need(prefix(rows)==prefix(original_rows),'Every actual input/selection/damage/native WIN record before distance change remains exact')
 index=lambda tag,predicate=lambda row:True:next(i for i,(kind,row)in enumerate(rows)if kind==tag and predicate(row))
 mutations=[('wrong_actual_physical_gap',index('COMMAND_POSITION'),'gap','160','Actual physical gap-140 command position'),
  ('proxy_own_body',index('POSE',lambda r:int(r['age'])==48),'id','1','Body ownership or actual fighter ID changed'),
  ('wrong_native_ground_anchor',index('POSE',lambda r:int(r['age'])==48),'y','82','Scene moved the fighter off its native ground anchor'),
  ('incorrect_original_scene_cadence',index('POSE',lambda r:int(r['age'])==48),'age','49','Original five-field body timing changed'),
  ('missing_true_native_winner',index('WIN'),None,None,'Two actual original winner-table dispatches'),
  ('missing_native_scene_cleanup',index('ENTRY',lambda r:r['entry']=='FF880CC0'),None,None,'Native Friendship finish handoff changed')]
 outcomes=[]
 for label,at,key,value,expected_error in mutations:
  changed=copy.deepcopy(rows)
  if key is None:changed.pop(at)
  else:changed[at][1][key]=value
  need(changed!=rows,'Non-vacuous actual supplement chronology corruption')
  outcomes.append(reject(lambda:check(changed),label,expected_error))
 reference_path=ROOT/'audit_v755_original_friendship_art/reference.json';reference=json.loads(reference_path.read_text())
 poses=scene.previous.select(rows,'POSE');matches=[];pixel_outcomes=[];images={}
 for record in reference['records']['sonya']['groups']:
  need(not record['effect'],'Exact original Sonya body-only group')
  path=reference_path.parent/record['file'];pin(path);sprite=np.asarray(Image.open(path).convert('RGBA'))
  need(hashlib.sha256(sprite.tobytes()).hexdigest()==record['rgba_sha256'].lower(),'Complete original RGBA reference')
  found=None
  for start in (int(row['age'])for row in poses if int(row['pose'],16)+0x1000000==record['group']):
   for age in range(start+1,min(start+5,199)):
    photo=FOLDER/'snap'/f'native_field_{age}.png'
    if not photo.is_file():continue
    if age not in images:images[age]=np.asarray(Image.open(photo).convert('RGB'))
    actual=images[age]
    try:result=match(actual,sprite)
    except ValueError:continue
    found=dict(group=f'{record["group"]:08X}',age=age,render=str(photo),**result);pin(photo);break
   if found:break
  need(found is not None,'Every original Sonya body group rendered exactly in the current unassisted supplement '+hex(record['group']))
  actual=images[found['age']];flipped=sprite[:,::-1]if found['flip']else sprite;mask=flipped[:,:,3]!=0
  x,y=found['origin'];sy,sx=np.argwhere(mask)[len(np.argwhere(mask))//2]
  corrupted=actual.copy();corrupted[y+sy,x+sx]^=255
  need(not np.array_equal(actual,corrupted),'Non-vacuous actual opaque body-pixel corruption')
  pixel_outcomes.append(reject(lambda:match(corrupted,sprite),'changed_opaque_body_pixel_'+found['group'],'Every original opaque body pixel'))
  need(match(actual,sprite)=={k:found[k]for k in ('flip','origin','opaquePixels')},'Final untouched actual original-body pixel control')
  matches.append(found)
 need(len(matches)==11 and check(rows)==control,'All original Sonya body groups and final actual untouched scene control')
 combined={key:len({match['group']for match in case['matches']} | ({item['group']for item in matches}if key=='sonya_p2'else set()))for key,case in prior.items()}
 need(combined==dict(kano_p1=18,kano_p2=18,sonya_p1=11,sonya_p2=11),'Every original body group both slots across actual current gap-160/140 scenes')
 for name in ('run.log','result.json','inputs_before.json','guest_maincpu.bin','native_mix.wav'):pin(FOLDER/name)
 pin(FOLDER/'native_mix.wav',meta['mix_sha256']);pin(Path(__file__).resolve());scene.launch.module_pins(pins)
 return dict(passed=True,case='sonya_gap140_p2',currentTrueID=18,actualCommandGap=int(scene.previous.select(rows,'COMMAND_POSITION')[0]['gap']),
  wholeActualGuestAndPayloadReconstructed=True,solePhysicalRetreatDistanceChange=True,completePreDistanceNativeChronologyExact=True,
  originalBodyMatches=matches,bodyGroupsByCharacterSlot=combined,originalBodyGroupsBothSlotsPixelAccepted=True,
  specificNativeCounterexamples=outcomes,specificOpaquePixelCounterexamples=pixel_outcomes,rejectedSpecificCounterexamples=len(outcomes)+len(pixel_outcomes),
  finalUnmodifiedControlPassed=True,priorObscuredGroupsRetainedAsUnaccepted=True,nativeSceneControl=control,
  originalBodyPixelsAcceptedOnlyInCapturedOneArenaTwoDistanceContexts=True,gameChanged=False,
  completeSceneRasterShadowAudioAccepted=False,supplementAudiblePCMAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,
  inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Immutable current body supplement proof')
 try:r=verify()
 except Exception as error:
  import traceback
  r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in ('inputHashes','originalBodyMatches','specificNativeCounterexamples','specificOpaquePixelCounterexamples')},indent=2),flush=True)
 raise SystemExit(0 if r['passed']else 1)
