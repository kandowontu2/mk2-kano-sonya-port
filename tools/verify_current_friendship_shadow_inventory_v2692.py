"""Actual physical Friendship shadow-command inventory and native retirement.
Eight current-build scenes cover original Cage/Liu controls and true Kano/Sonya
in both slots. Source-bound cache data, native shadow first/last row and count,
continuous field accounting and actual original actor-global stores are checked.
Intermediate shadow rows, rendered pixels/palettes, complete raster/erasure,
other arenas/victims/finishers and full-port acceptance remain separate gates.
"""
import argparse,copy,json,re,struct,traceback
from pathlib import Path
from collections import defaultdict
import verify_current_friendship_v2655 as scene
import verify_current_ground_shadow_v1859 as graphics
ROOT=scene.ROOT
CASES={f'{fighter}_p{side}':(fighter,side)for fighter in ('cage','liu_kang','kano','sonya')for side in (1,2)}
IDS=dict(cage=2,liu_kang=1,kano=17,sonya=18)
need=scene.need

def integer(row,key):return int(row[key])
def hexadecimal(row,key):return int(row[key],16)

def physical(rows,fighter,side,guest):
 fid=IDS[fighter];vid={2:1,1:2,17:18,18:17}[fid]
 boot=scene.previous.select(rows,'BOOT');final=scene.previous.select(rows,'RESULT');window=scene.previous.select(rows,'WINDOW')
 need(len(boot)==len(final)==len(window)==1,'One actual terminal physical Friendship')
 need(all(row['writes']=='0'and row['assistance']=='none'for tag,row in rows),'Every record physical input/read-only observations')
 need(integer(boot[0],'own_id')==fid and integer(boot[0],'victim_id')==vid and integer(boot[0],'requested_gap')==160 and integer(boot[0],'observation')==1600,'Actual stock/new true-ID extended control')
 selected=scene.previous.select(rows,'SELECT_ID')
 need(len(selected)==2 and all(integer(row,'target')==integer(row,'actual')==(fid if integer(row,'slot')==side else vid)for row in selected),'Actual native physical selection, no proxies')
 damage=scene.previous.select(rows,'DAMAGE');expected=161;kos=[]
 for row in damage:
  before,after=integer(row,'before'),integer(row,'after')
  need(before==expected and 0<=after<before<=161 and row['pc']=='FF836700','Complete original native earned damage chain')
  expected=after
  if after==0:kos.append(integer(row,'frame'));expected=161
 need(len(kos)==2 and sum(integer(row,'before')-integer(row,'after')for row in damage)==322 and integer(final[0],'kos')==2,'Two actually earned original KO rounds')
 wins=scene.previous.select(rows,'WIN')
 need(len(wins)==2,'Two actual native winner-table dispatches')
 for index,row in enumerate(wins):
  health=list(map(int,row['health'].split(',')))
  need(integer(row,'slot')==side and integer(row,'id')==integer(row,'actor_id')==integer(row,'roster')==fid and row['owner']==row['actor']and
   hexadecimal(row,'entry')==0xfffef800+fid*32 and row['pc']=='FF8296B0'and health[side-1]>0 and health[2-side]==0 and integer(row,'frame')>=kos[index],'Actual true native winner and owned original dispatch')
 need(all(value=='0'for key in ('hp_counters','lp_counters')for value in window[0][key].split(',')),'Actual no-punch Friendship eligibility')
 need(final[0]['cleanup']=='true'and final[0]['retired']=='true'and integer(final[0],'action')>integer(final[0],'window'),'Actual original action, handoff and retirement')
 if fid>=17:scene.check(rows,fighter,side)
 else:
  address=struct.unpack_from('<I',guest,(0xff880d90-0xff800000)//8+fid*4)[0]
  entries=scene.previous.select(rows,'ENTRY')
  need(any(hexadecimal(row,'entry')==address and integer(row,'id')==fid for row in entries),'Original character-owned stock Friendship action')
  poses=scene.previous.select(rows,'POSE')
  need(poses and all(integer(row,'id')==integer(row,'roster')==fid and row['owner']==row['actor']for row in poses),'Original stock body ownership throughout its scene')
 need(scene.previous.select(rows,'FIELD')[-1]['mode']=='3','Native next-screen transition')
 return dict(actualTrueID=fid,actualVictimID=vid,earnedKOFrames=kos,actualWINFrames=[integer(row,'frame')for row in wins],
  window=integer(final[0],'window'),action=integer(final[0],'action'),terminal=integer(final[0],'frame'))

def inventory(rows,fighter,side,guest):
 control=physical(rows,fighter,side,guest)
 select=scene.previous.select
 begin=select(rows,'SHADOW_BEGIN');final=select(rows,'SHADOW_RESULT');actions=select(rows,'SHADOW_ACTION');cleanup=select(rows,'SHADOW_CLEANUP')
 need(len(begin)==len(final)==len(actions)==len(cleanup)==1,'One actual continuous shadow observer/action/handoff')
 need(integer(begin[0],'frame')>max(integer(row,'frame')for row in select(rows,'SELECT_ID')),'Observer begins after actual physical selection, not attract/demo')
 need(integer(actions[0],'frame')==control['action']==integer(final[0],'action')and integer(cleanup[0],'frame')==integer(final[0],'cleanup'),'Actual native scene callback chronology')
 fields=select(rows,'SHADOW_FIELD');start=integer(begin[0],'frame')
 need([integer(row,'frame')for row in fields]==list(range(start,control['window']+1601)),'Every continuous actual native field through extended next-screen observation')
 components=select(rows,'SHADOW_COMPONENT');by_frame=defaultdict(list);gfx={row['key']:row for row in select(rows,'SHADOW_GFX')}
 need(len(gfx)==len(select(rows,'SHADOW_GFX')),'Unique complete source-buffer records')
 for row in components:
  fid=control['actualTrueID']if integer(row,'slot')==side else control['actualVictimID']
  need(integer(row,'id')==integer(row,'roster')==fid and row['owner']==row['actor']and 0x01000000<=hexadecimal(row,'actor')<0x01100000 and
   0x01000000<=hexadecimal(row,'main')<0x01100000,'Actual owned native shadow cache identity')
  cache,address=hexadecimal(row,'cache'),hexadecimal(row,'row');part=(address-cache)//112
  need(address==cache+part*112 and 0<=part<12,'Native physical descriptor-cache component')
  source,command,w,h=(hexadecimal(row,'source'),hexadecimal(row,'command'),integer(row,'width'),integer(row,'height'))
  key=f'{source:08X}_{command|0x8002:04X}_{w}_{h}';need(key in gfx,'Complete source-bound shadow cache buffer')
  buffer=gfx[key];raw=bytes.fromhex(buffer['data']);bit=integer(buffer,'offset')%8;origin=bit;starts=[]
  bpp=(command>>12)&7 or 8
  need(bpp==6 and h>=4 and w>0,'Actual six-bit native physical shadow source')
  for y in range(h):
   starts.append(source+bit-origin)
   if command&0x80:
    need(bit+8<=len(raw)*8,'Complete compressed native header')
    header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255
    pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
    bit+=8+bpp*max(0,w-pre-post)
   else:bit+=bpp*w
   need(bit<=len(raw)*8,'Complete native source-row bounds')
  indices=list(range(0,4*(h//4),4));indices.append(indices[-1]);copies=integer(row,'copies')
  need(copies==len(indices)and hexadecimal(row,'first')==starts[0]and hexadecimal(row,'last')==starts[indices[-1]]and
   integer(row,'firstX')==integer(row,'lastX')and integer(row,'lastY')==(integer(row,'firstY')+copies-1)&511 and row['lastPC']=='FF801610','Native source/cadence/first-last geometry and original final caller')
  by_frame[integer(row,'frame')].append(row)
 for row in fields:
  frame=integer(row,'frame');actual=by_frame[frame]
  need(integer(row,'unresolvedCopies')==0 and integer(row,'copies')==integer(row,'ownedCopies')==sum(integer(c,'copies')for c in actual)and integer(row,'components')==len(actual),'Every actual shadow DMA callback accounted to its physical cache')
 need(integer(final[0],'nativeCopies')==sum(integer(row,'copies')for row in fields)and integer(final[0],'physicalComponents')==len(components)and integer(final[0],'unresolvedCopies')==0,'Actual terminal shadow totals preserve continuous field ledger')
 need(sum(integer(row,'copies')for row in fields if integer(row,'frame')<control['action'])>1000,'Real ordinary shadow callbacks prove observer coverage before Friendship')
 stores=[row for row in select(rows,'SHADOW_POINTER')if integer(row,'frame')>control['action']and row['value']=='0000']
 wanted=[(n,at,pc)for n,base,pc in ((1,0x01060220,'FF82BBF0'),(2,0x01060df0,'FF82BC20'))for at in (base,base+16)]
 need(len(stores)==4 and [(integer(row,'slot'),hexadecimal(row,'at'),row['pc'])for row in stores]==wanted and len({row['frame']for row in stores})==1 and
  all(row['mask']=='FFFF'and row['mode']=='3'for row in stores),'All four actual original actor-global retirement stores')
 retired=integer(stores[0],'frame');need(retired>integer(cleanup[0],'frame'),'Actual pointer teardown follows original common handoff')
 absent=select(rows,'SHADOW_ABSENT')
 need(all(any(integer(row,'frame')==frame and integer(row,'slot')==slot and row['actor']=='00000000'for row in absent)for frame in (retired,control['window']+1600)for slot in (1,2)),'Actual both physical actors absent after native teardown and at terminal scene')
 need(not any(integer(row,'frame')>=retired for row in components),'No physical floor-shadow projection survives actual actor retirement')
 action=control['action'];buckets={}
 for label,low,high in (('startup',action,action+47),('native_body_scene',action+48,integer(cleanup[0],'frame')-1),('handoff_until_retirement',integer(cleanup[0],'frame'),retired-1),('after_retirement',retired,control['window']+1600)):
  subset=[row for row in components if low<=integer(row,'frame')<=high]
  buckets[label]=dict(firstFrame=low,lastFrame=high,nativeComponents=len(subset),nativeCopies=sum(integer(row,'copies')for row in subset),
   actualShadowAges=sorted({integer(row,'frame')-action for row in subset}),slots=sorted({integer(row,'slot')for row in subset}))
 return dict(**control,cleanup=integer(cleanup[0],'frame'),actualPointerRetirement=retired,continuousFields=len(fields),
  nativeShadowCopies=integer(final[0],'nativeCopies'),nativeShadowComponents=len(components),sourceBuffers=len(gfx),
  firstLastSourceAndCadenceChecked=True,intermediateShadowRowsAccepted=False,unresolvedNativeShadowCallbacks=0,
  phases=buckets,nativeActorRetirementChecked=True)

def verify(case):
 fighter,side=CASES[case];folder=ROOT/f'audit_v2691_current_{fighter}_friendship_shadow_p{side}'
 pins=scene.launch.source_pins()
 def pin(path,wanted=None):
  path=str(path);actual=scene.launch.sha(path);need(wanted is None or actual==wanted,'Unchanged actual dependency '+path)
  need(path not in pins or pins[path]==actual,'Consistent source/capture dependency '+path);pins[path]=actual
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));before=json.loads((folder/'inputs_before.json').read_text(encoding='utf-8-sig'))
 build=json.loads((ROOT/scene.current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['candidate']==scene.current.NAME and meta['winner']==fighter and meta['side']==side and meta['command_case']=='positive'and meta['samples_enabled']and
  meta['requested_gap']==160 and meta['observation']==1600 and meta['guest_writes']==0 and meta['assistance']=='none'and before==meta['input_hashes']and
  meta['executable_sha256']==build['executable_sha256']and meta['payload_sha256']==build['payload_sha256']and all(before.get(file)==wanted for file,wanted in build['input_hashes'].items()),'Matched terminal current-build physical scene')
 for file,wanted in before.items():
  pin(file,wanted)
  if Path(file).suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/Path(file).name,wanted)
 observer=ROOT/'mk2ks_current_friendship_shadow_v2689.lua';pin(observer,'B686815082909164CEB923092B198E1C10B2EBFB4571D9A62606899FDA2B9531')
 need(not re.search(r'write_u\d+|:write_|set_value|clear_value|load_?state|\.value\s*=(?!=)',observer.read_text()),'Entire shadow observer is read-only')
 normalized=lambda path:path.read_text().rstrip()+'\n'
 need(normalized(ROOT/'mk2ks_native_friendship_audio_v790.lua').replace('mk2ks_native_friendship_probe_v784.lua','mk2ks_native_friendship_probe_v788.lua')==normalized(ROOT/'mk2ks_current_friendship_extended_audio_v2687.lua'),'Only extended physical driver filename changes in immutable audio observer')
 need(normalized(ROOT/'mk2ks_current_friendship_wins_v2651.lua').replace('mk2ks_native_friendship_audio_v790.lua','mk2ks_current_friendship_extended_audio_v2687.lua')==normalized(ROOT/'mk2ks_current_friendship_extended_wins_v2688.lua'),'Only audio observer filename changes in immutable winner observer')
 source=normalized(ROOT/'tools/run_current_friendship_v2650.ps1')
 source=source.replace("[ValidateSet('kano','sonya')]","[ValidateSet('kano','sonya','cage','liu_kang')]").replace('mk2ks_current_friendship_wins_v2651.lua','mk2ks_current_friendship_shadow_v2689.lua')
 source=source.replace('"$root/mk2ks_native_friendship_audio_v790.lua","$root/mk2ks_native_friendship_probe_v784.lua",','"$root/mk2ks_current_friendship_extended_wins_v2688.lua","$root/mk2ks_current_friendship_extended_audio_v2687.lua","$root/mk2ks_native_friendship_probe_v788.lua","$root/mk2ks_current_friendship_wins_v2651.lua","$root/mk2ks_native_friendship_audio_v790.lua","$root/mk2ks_native_friendship_probe_v784.lua",')
 source=source.replace('$sampleOption=if($NoSamples)','$env:MK2KS_FRIEND_GAP="160";$env:MK2KS_FRIEND_OBSERVATION="1600"\n $sampleOption=if($NoSamples)').replace('command_case=$CommandCase;samples_enabled=','command_case=$CommandCase;requested_gap=160;observation=1600;samples_enabled=')
 need(source==normalized(ROOT/'tools/run_current_friendship_shadow_v2690.ps1'),'Entire current launcher exact except original stock fixture options, observation, filenames and tracking')
 guest,_,payload=scene.current.expected();need((folder/'guest_maincpu.bin').read_bytes()==guest and (ROOT/scene.current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Whole actual current guest/payload source reconstruction')
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();first=(0xff801400-0xff800000)//8;last=(0xff801650-0xff800000)//8
 need(guest[first:last]==original[first:last],'Entire original native shadow scanning/copy routine unchanged')
 log=(folder/'run.log').read_text(encoding='utf-8-sig');need(not re.search(r'LUA ERROR|fatal error|access violation|stack traceback|WRONG CHECKSUMS',log,re.I),'No observer/native runtime errors')
 rows=scene.previous.parse(folder/'run.log');control=inventory(rows,fighter,side,guest)
 image=graphics.graphics(pins)
 for row in scene.previous.select(rows,'SHADOW_GFX'):
  first,count=integer(row,'first'),integer(row,'bytes')
  need(0<=first<first+count<=len(image)and bytes.fromhex(row['data'])==image[first:first+count],'Every actual shadow source byte matches independent original/imported ROMs')
 if fighter in ('kano','sonya'):
  baseline=ROOT/f'audit_v2653_current_{fighter}_friendship_p{side}/run.log';pin(baseline)
  before_rows=scene.previous.parse(baseline)
  def prefix(rs):
   return [(tag,{k:v for k,v in row.items()if k not in ('requested_gap','observation')})for tag,row in rs if not tag.startswith('SHADOW_')and tag!='RESULT'and integer(row,'frame')<=control['window']+720]
  need(prefix(rows)==prefix(before_rows),'Every actual existing current physical input/native scene/pose/part/WIN/cue record unchanged through original 720-field window')
 indices={tag:next(i for i,(kind,row)in enumerate(rows)if kind==tag)for tag in ('SHADOW_FIELD','SHADOW_COMPONENT','WIN')}
 pointer=next(i for i,(tag,row)in enumerate(rows)if tag=='SHADOW_POINTER'and integer(row,'frame')>control['action']and row['value']=='0000')
 mutations=[('missing_actual_continuous_field',indices['SHADOW_FIELD'],None,None,'Every continuous actual native field'),
  ('wrong_physical_shadow_owner',indices['SHADOW_COMPONENT'],'owner','01000000','Actual owned native shadow cache identity'),
  ('wrong_original_last_shadow_source',indices['SHADOW_COMPONENT'],'last','00000000','Native source/cadence/first-last geometry'),
  ('wrong_original_copy_count',indices['SHADOW_COMPONENT'],'copies',str(integer(rows[indices['SHADOW_COMPONENT']][1],'copies')+1),'Native source/cadence/first-last geometry'),
  ('wrong_original_final_shadow_caller',indices['SHADOW_COMPONENT'],'lastPC','FF801590','Native source/cadence/first-last geometry'),
  ('proxy_actual_native_winner',indices['WIN'],'id','99','Actual true native winner'),
  ('missing_actual_actor_global_retirement',pointer,None,None,'All four actual original actor-global retirement stores')]
 outcomes=[]
 for label,at,key,value,expected in mutations:
  changed=copy.deepcopy(rows)
  if key is None:changed.pop(at)
  else:changed[at][1][key]=value
  need(changed!=rows,'Non-vacuous actual native shadow/retirement corruption')
  try:inventory(changed,fighter,side,guest)
  except ValueError as error:
   need(expected in str(error),'Intended actual invariant for '+label+': '+str(error));outcomes.append(dict(name=label,rejectedBy=str(error)))
  else:raise ValueError('Malformed native shadow/retirement accepted '+label)
 need(inventory(rows,fighter,side,guest)==control,'Final untouched full native shadow-command/retirement control')
 for path in folder.rglob('*'):
  if path.is_file():pin(path)
 pin(folder/'native_mix.wav',meta['mix_sha256']);pin(Path(__file__).resolve());scene.launch.module_pins(pins)
 return dict(passed=True,case=case,**control,wholeActualGuestAndPayloadReconstructed=True,originalNativeShadowRoutineUnchanged=True,
  allActualShadowSourceBuffersROMBound=True,physicalInputAndBuildUnchanged=True,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,
  finalUnmodifiedControlPassed=True,inputHashes=pins,gameChanged=False,fullShadowRowsOrPixelsAccepted=False,fullSceneRasterShadowAudioAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('case',choices=CASES);a=p.parse_args()
 output=ROOT/f'audit_v2693_current_{CASES[a.case][0]}_friendship_shadow_p{CASES[a.case][1]}_checked'
 need(not output.exists(),'Immutable actual native shadow inventory proof')
 try:report=verify(a.case)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 output.mkdir();(output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','outcomes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
