"""Whole5908 scene with independently observed original Pit shadow scheduling.

The original game emits no fighter-floor shadow commands on the Pit, before
or during its native cinematic. Retain all source-native movie/floor/raster/
earned gates. Reject an introduced floor call/pixel or misowned movie shadow;
qualify each native font-mode8 descriptor separately, never count it as feet.
"""
import copy,hashlib,json,struct
from pathlib import Path
from types import SimpleNamespace
import current_pit_phase_ground_contract_v5908 as previous
from current_pit_phase_ground_contract_v5908 import need,ROOT,source_graphics,native_gate,movie_faults,native,phase_ground,ground_faults
REFERENCE=ROOT/'audit_v5928_original_stock_pit_shadow_schedule_checked/report.json'
ORDINARY=ROOT/'audit_v5919_original_stock_pit_shadow_inventory_checked/report.json'

def shadow_schedule(scene,guest,stock,reference,ordinary):
 need(reference['passed']and reference['originalStockPitShadowSchedulingAccepted']and reference['originalDriver']=='mk2'and
      reference['genuineFullHealthMatches']==7 and reference['genuineCollisionDamage']==2254 and reference['completedFields']==1101 and
      len(reference['effectiveActualScheduleFaultsRejected'])==14 and reference['originalNativeShadowEntries']==reference['originalNativeShadowCopies']==0 and
      ordinary['passed']and ordinary['originalDriver']=='mk2','Independent genuine original ordinary and cinematic Pit schedule, not an assumed zero policy')
 pit=[r for r in ordinary['shadowExecutionByArena']if r['arena']==6]
 earlier=[r for r in ordinary['shadowExecutionByArena']if r['arena']<6 and r['slot']in(1,2)]
 need(len(pit)==3 and all(r['fields']==301 and r['entries']==r['components']==r['copies']==r['allMode8']==0 for r in pit)and
      all(r['eligibleFields']==r['fields']for r in pit if r['slot']in(1,2))and all(r['copies']>0 for r in earlier),
      'Original Pit omission distinguished from positive working original shadow observations in six preceding arenas')
 off=lambda a:(a-0xff800000)//8
 for lo,hi in ((0xff8046e0,0xff804990),(0xff80a810,0xff80ab60),(0xff801000,0xff8017b0),(0xff841be0,0xff841c40)):
  need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)],'Whole current original shadow eligibility/dispatcher/clear source matches independent stock')
 g=scene.groups;commands=g['FLOOR_DMA']
 need(not g['SHADOW_COMPONENT']and not any(d['pc']in(0xff8015a0,0xff801610)for d in commands)and
      not any(0x10000000<=d['source']<0x1a000000 and d['command']&15==8 for d in commands)and
      all(r['shadowPixels']==0 for r in scene.records),
      'Actual complete current Pit issues no native/imported physical floor-shadow command or visible floor-shadow pixels, matching original')
 physical=[b for b in g['FLOOR_BODY']if b['slot']in(1,2)]
 cinematic=[b for b in g['FLOOR_BODY']if b['slot']==4]
 need(physical and {b['id']for b in physical}=={17,18}and all(b['owner']==b['actor']and b['body']&16 for b in physical),
      'Current Pit retains real physical actors and native shadow eligibility flags, no disabled-character substitute')
 need(cinematic and all(b['owner']==b['actor']and b['body']==2 for b in cinematic),
      'Current own Main+140 cinematic body has exact observed original native no-shadow flags')
 descriptors={};fonts=[d for d in commands if d['command']&15==8]
 for d in fonts:
  source,width,height=d['source'],d['width'],d['height']
  need(d['pc']==0xff804640 and d['command']==0x9008 and 0x04000000<=source<0x04010000,
       'Every current non-floor mode8 command is original font FIFO, not floor shadow or imported body')
  key=source,width,height
  if key in descriptors:continue
  found=[];needle=struct.pack('<I',source);pos=0
  while True:
   at=stock.find(needle,pos)
   if at<0:break
   pos=at+1;address=0xff800000+(at-8)*8
   if at>=8 and 0xffc00000<=address<0xffc10000 and struct.unpack_from('<HH',stock,at-8)==(width,height)and struct.unpack_from('<H',stock,at+4)[0]==0x1000:
    need(guest[at-8:at+6]==stock[at-8:at+6],'Actual current stock font descriptor is unchanged, not fitted to DMA')
    found.append(address)
  need(found,'Every actual current font source/width/height/1bpp descriptor independently matches original stock')
  descriptors[key]=found
 return dict(passed=True,independentOrdinaryStockFields=301,independentWholeStockCinematicFields=1101,
             actualCurrentFloorShadowCommands=0,actualCurrentNativeFontMode8Commands=len(fonts),
             actualCurrentNativeFontDescriptors=len(descriptors),physicalShadowFlagsRetained=True,
             ownCinematicNoShadowFlagsMatchOriginal=True,currentPitShadowSchedulingMatchesOriginal=True,
             directCurrentShadowEnableVariableObservation=False)

def policy(scene,guest):
 from current_payload_metadata_context_v5229 import sha
 reference=json.loads(REFERENCE.read_text());ordinary=json.loads(ORDINARY.read_text())
 for proof in (reference,ordinary):
  need(all(sha(p)==h for p,h in proof['inputHashes'].items()),'Every independent original stock source/capture/effective-fault input unchanged')
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 positive=shadow_schedule(scene,guest,stock,reference,ordinary);faults=[]
 def copied():return SimpleNamespace(groups={k:[dict(r)for r in rows]for k,rows in scene.groups.items()},records=copy.deepcopy(scene.records))
 def reject(name,bad,code=guest):
  try:shadow_schedule(bad,code,stock,reference,ordinary)
  except ValueError as error:faults.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Actual current Pit shadow policy corruption accepted '+name)
 bad=copied();next(d for d in bad.groups['FLOOR_DMA']if d['command']&15==8)['pc']=0xff8015a0
 reject('actual font DMA attributed to floor-shadow kernel',bad)
 bad=copied();next(d for d in bad.groups['FLOOR_DMA']if d['command']&15==8)['width']=999
 reject('actual original font descriptor width corrupted',bad)
 bad=copied();next(b for b in bad.groups['FLOOR_BODY']if b['slot']==4)['body']|=16
 reject('shadow enabled on actual own cinematic actor',bad)
 bad=copied();bad.records[0]['shadowPixels']=1
 reject('visible floor-shadow pixel survives on Pit',bad)
 code=bytearray(guest);code[(0xff801090-0xff800000)//8]^=1
 reject('actual original eligibility program corrupted',scene,bytes(code))
 need(len(faults)==5 and shadow_schedule(scene,guest,stock,reference,ordinary)==positive,
      'All five actual current shadow/font/source corruptions reject and unchanged full policy restores')
 return dict(**positive,actualShadowPolicyFaultsRejected=faults)

# Replace only the erroneous requirement for positive floor copies/identities
# with the stronger source/independent-stock/whole-current phase policy.
source=previous.source
old=""" need(shadows['rowStreamVerified'] and not shadows['failures'] and not shadows['oversized_rows'] and
      set(map(tuple,shadows['identities']))=={(s,ids[s-1])for s in (1,2)},
      'All actual own compressed physical floor-shadow rows and identities retained')
"""
need(source.count(old)==1,'Entire5908 scene retained except independently disproven positive-Pit-shadow requirement')
source=source.replace(old," shadow_policy=policy(scene,guest)\n need(shadows['components']==shadows['checked_copies']==0 and not shadows['failures']and not shadows['oversized_rows'],\n      'Complete actual compressed-shadow inventory agrees with independent original native Pit omission')\n",1)
old="proof.update(actualNativePhaseGround=ground,"
need(source.count(old)==1,'All original movie/floor/earned/raster results retained')
source=source.replace(old,"proof.update(actualNativePitShadowPolicy=shadow_policy,wholeNativePitShadowPolicyAccepted=True,actualNativePhaseGround=ground,",1)
scope=dict(vars(previous),policy=policy,__file__=__file__)
exec(compile(source,__file__+'::whole5908_independent_original_Pit_shadow_schedule','exec'),scope)
scene_contract=scope['scene_contract']
CONTRACT_SOURCE_SHA256=hashlib.sha256(source.encode()).hexdigest().upper()
