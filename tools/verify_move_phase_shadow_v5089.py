"""Actual ordinary ice/thaw/control instances and source-derived native shadows.

Not acceptance of unsampled move phases, arenas, audio, finishers or the port.
All picture streams reconstructed in RAM from compiled ROM_LOAD32_BYTE inputs.
"""
import copy,hashlib,json,re,struct,subprocess,zipfile
from collections import defaultdict
from pathlib import Path
import native_subzero_legs_context_v4993 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5090_move_phase_shadow_checked'
CASES=[('kano',1,17),('kano',2,17),('sonya',1,18),('sonya',2,18),('kitana',1,4),('liu_kang',2,1)]
HEX=set('actor main owner pose cache row graphic command body facing world b1 b2 b4 b7 a5 shadow_camera pc value mask source palette color actor_register main_register cache_row entry a0 a7 a9 bank flags own_actor own_main own_owner victim_actor victim_main victim_owner action'.split())
def num(r,k):return int(r[k],16 if k in HEX else 10)
def short(v):return (v&65535)-65536 if v&32768 else v&65535
def subxy(a,b):return (((short(a>>16)-short(b>>16))&65535)<<16)|((short(a)-short(b))&65535)

def native_group(r,payload,guest):
 def read(address,fmt):
  raw,base=(payload,0xfe800000) if 0xfe800000<=address<0xff800000 else (guest,0xff800000)
  need(address>=base and (address-base)%8==0,'Aligned actual picture descriptor')
  off=(address-base)//8;need(0<=off<=len(raw)-struct.calcsize(fmt),'Complete actual picture descriptor bounds')
  return struct.unpack_from(fmt,raw,off)
 result=[];pose=num(r,'pose');facing=num(r,'facing')
 for index in range(12):
  ptr=read(pose+index*32,'<I')[0]
  if not ptr:break
  w,h,dx,dy,g,c=read(ptr,'<HHhhIH')
  if facing&16:dx=w-dx
  if facing&32:dy=h-dy
  result.append(dict(graphic=g,width=w,height=h,dx=dx,dy=dy,command=(c&~0x30)|(facing&0x30)))
 need(0<len(result)<12,'Complete terminated native fighter picture')
 return result

def reconstruct(pins):
 source=ROOT/native.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 pins[str(source.resolve())]=sha(source)
 text=source.read_text();block=text.split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0]
 block=block.split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
 entries=re.findall(r'ROM_LOAD32_BYTE\( "([^"]+)", (0x[0-9a-f]+), (0x[0-9a-f]+), CRC\([0-9a-f]+\) SHA1\(([0-9a-f]+)\)',block)
 need(len(entries)==32,'Exact compiled stock plus imported graphics lane inventory')
 gfx=bytearray(0x2000000);archive=ROOT/'roms/mk2.zip';pins[str(archive.resolve())]=sha(archive)
 with zipfile.ZipFile(archive)as z:
  for name,address,size,digest in entries:
   address,size=int(address,16),int(size,16);p=ROOT/'roms/mk2ks'/name
   if p.exists():raw=p.read_bytes();pins[str(p.resolve())]=sha(p)
   else:raw=z.read(name)
   need(len(raw)==size and hashlib.sha1(raw).hexdigest()==digest,'Compiled complete native graphics ROM lane SHA1: '+name)
   gfx[address:address+size*4:4]=raw
 return gfx

def load(fighter,side,report_version=5085,folder_version=5084):
 folder=ROOT/f'audit_v{folder_version}_move_phase_{fighter}_p{side}'
 report_path=ROOT/f'audit_v{report_version}_move_phase_{fighter}_p{side}_observed/report.json'
 report=json.loads(report_path.read_text());need(report['passed']and report['nativeExit']==0,'Actual terminal transport case')
 log=(folder/'run.log').read_text().replace('\\nMK2_','\nMK2_')
 need('hex='not in log,'No raw buffers persisted')
 rows=defaultdict(list)
 for line in log.splitlines():
  if line.startswith(('MK2_NORMAL_FREEZE_','MK2_STOCK_HEAD_V921_')):
   tag=line.split()[0];rows[tag].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 parts=json.loads((folder/'packed_part_memory_proofs.json').read_text())
 return dict(fighter=fighter,side=side,folder_version=folder_version,report=report,folder=folder,report_path=report_path,rows=rows,parts=parts)

def check(b,identity,guest,payload,gfx):
 rows=b['rows'];side=b['side'];r=b['report']
 need(r['executableSHA256']==native.EXE_SHA and r['guestSHA256']==native.GUEST_SHA,'Actual compiled candidate identity')
 fields=rows['MK2_NORMAL_FREEZE_FIELD'];first=rows['MK2_STOCK_HEAD_V921_FIRST_LIVE']
 need(len(first)==1 and len(fields)==1101 and [num(f,'age')for f in fields]==list(range(1101)),'Complete ordinary live chronology')
 start=num(first[0],'frame');need(all(num(f,'frame')==start+i for i,f in enumerate(fields)),'Every native live field contiguous')
 actor=num(fields[0],'victim_actor');main=num(fields[0],'victim_main')
 own=num(fields[0],'own_actor');own_main=num(fields[0],'own_main')
 floor=num(fields[0],'floor');base_bank=num(fields[0],'bank')
 for f in fields:
  need(f['writes']=='0'and f['assistance']=='none'and num(f,'mode')==2 and num(f,'finish')==0,'Ordinary unassisted live fight, no finisher')
  need(num(f,'victim_id')==num(f,'roster')==identity and num(f,'state')==1 and
       num(f,'victim_actor')==num(f,'victim_owner')==actor and num(f,'victim_main')==main and
       num(f,'own_id')==8 and num(f,'own_actor')==num(f,'own_owner')==own and num(f,'own_main')==own_main,
       'Stable genuine owned human identities; never proxy or replaced actors')
  need(num(f,'hp')==num(f,'own_hp')==161,'Native ordinary ice preserves health')
  need(num(f,'floor')==floor and num(f,'y')<=floor,'Native floor stays fixed and airborne height never penetrates it')
  if not 600<=num(f,'age')<=650:
   need(num(f,'y')==floor,'Every non-jump action remains at its owned native floor')
 cold=[num(f,'age')for f in fields if num(f,'action')==0x0401]
 need(len(cold)==160 and cold==list(range(cold[0],cold[0]+160))and 120<=cold[0]<=160,'One continuous original 160-field freeze')
 need(all(num(fields[i],'bank')==0x0505 and num(fields[i],'flags')&16 for i in cold),'Own pose uses real blue frozen palette and shadow eligibility')
 need(all(num(fields[i],'bank')==base_bank and num(fields[i],'action')!=0x0401 for i in range(cold[-1]+1,1101)),
      'Natural thaw restores own palette and never relocks')
 need(num(fields[450],'action')!=0 and all(num(fields[i],'action')==0 for i in range(451,467))and
      (num(fields[467],'x')-num(fields[450],'x'))*(1 if side==1 else -1)>20,
      'Physical movement works after thaw toward opponent')
 need(all(num(fields[i],'action')==0x0101 for i in range(512,530))and num(fields[530],'action')!=0x0101,
      'Physical punch activates and naturally completes after thaw')
 # Genuine physical move activation, air trajectory and natural recovery, not labels alone.
 airborne=[num(f,'age')for f in fields if num(f,'y')<floor]
 need(airborne==list(range(605,643))and min(num(f,'y')for f in fields)==floor-95 and num(fields[622],'y')==floor-95,
      'Original38-field neutral jump and95-pixel height, followed by exact landing')
 need(num(fields[610],'action')==0x030b and num(fields[610],'y')<floor and num(fields[635],'action')==0x030b and
      num(fields[635],'y')<floor and num(fields[635],'y')>num(fields[622],'y')and num(fields[650],'y')==floor,
      'Genuine rise/apex/descending/landing physiology')
 for age,action in[(720,0x0302),(735,0x0301),(750,0x0303),(774,0x060c),(824,0x060c),(860,0x0700),(916,0x0107),(924,0x0603),(960,0),(1040,0x0303)]:
  need(num(fields[age],'action')==action,'Actual intended native movement/attack/guard phase at'+str(age))
 need(any(num(fields[i],'action')==0x0103 for i in range(760,774))and
      any(num(fields[i],'action')==0x0104 for i in range(810,824)),
      'Native high/low kick launch before their shared contact action')
 need(num(fields[1100],'bank')==base_bank and num(fields[1100],'y')==floor and num(fields[1100],'action')==0x0303,
      'Natural final own ready state/palette/floor; no locked animation')
 need(len(rows['MK2_NORMAL_FREEZE_END'])==1 and num(rows['MK2_NORMAL_FREEZE_END'][0],'age')==1100,
      'Actual ordinary test ends at expected live field')
 inputs=[(num(t,'frame')-start,num(t,'slot'),t['button'])for t in rows['MK2_STOCK_HEAD_V921_INPUT']if num(t,'frame')>=start]
 forward='Left'if side==1 else 'Right';toward='Right'if side==1 else 'Left'
 expected=[(age,3-side,button)for ages,button in[(range(90,93),'Down'),(range(98,101),forward),(range(106,109),'Low_Punch')]for age in ages]
 expected +=[(age,side,toward)for age in range(450,466)]+[(age,side,'High_Punch')for age in range(510,513)]
 expected +=[(age,side,'Up')for age in range(600,603)]
 expected +=[(age,side,'Down')for age in range(710,731)]
 expected +=[(age,side,'High_Kick')for age in range(760,763)]+[(age,side,'Low_Kick')for age in range(810,813)]
 expected +=[(age,side,'Block')for age in range(850,871)]
 expected +=[(age,side,'Down')for age in range(900,924)]+[(age,side,'High_Punch')for age in range(910,913)]
 expected +=[(age,side,toward)for age in range(950,971)]
 expected.sort(key=lambda row:row[0])
 need(inputs==expected,'Every actual physical live input exactly D,F,LP then victim movement/punch; no hidden assistance')
 for tag,entry,opcode in[('ICE_REQUEST',0xff86f9d0,0x09c0),('PROJECTILE_SETUP',0xff8a5900,0x24a0)]:
  actual=rows['MK2_NORMAL_FREEZE_'+tag]
  need(len(actual)==1,'One genuine native human ice request/setup')
  t=actual[0];need(num(t,'entry')==entry and num(t,'pc')==entry+16 and num(t,'value')==opcode and num(t,'mask')==65535 and
    num(t,'age')==108 and num(t,'id')==8 and num(t,'actor')==num(t,'owner')==own and num(t,'main')==own_main,
    'Source-bound original human ice branch opcode/PC/owner')
  need(struct.unpack_from('<H',guest,(entry-0xff800000)//8)[0]==opcode,'Actual guest ice instruction')
 need(num(rows['MK2_NORMAL_FREEZE_PROJECTILE_SETUP'][0],'a0')==13,'Original human ice task selects native projectile13')
 need(all(t['before']==t['after']for t in rows['MK2_STOCK_HEAD_V921_HEALTH']),'Observed native ice health writes remain nondamaging')
 stages=['before','ice','wait','after_controls','air_rise']
 stages +=['apex','air_fall','landing'] if b['folder_version']==5084 else ['air_fall']
 stages +=['landed','crouch','uncrouch','stand']
 stages +=['high_kick_start','high_kick','high_kick_recovery','low_kick_start','low_kick','low_kick_recovery'] if b['folder_version']==5084 else ['high_kick','low_kick']
 stages +=['block']
 stages +=['uppercut_start','uppercut','uppercut_recovery'] if b['folder_version']==5084 else ['uppercut']
 stages +=['walk','ready']
 need(len(r['actualScenes'])==len(stages) and [s['stage']for s in r['actualScenes']]==stages,
      'All four actual native RGB fields accounted')
 projections=rows['MK2_NORMAL_FREEZE_PROJECTION'];need(len(projections)>0,'Actual direct owned shadow observations')
 part_by={(num(t,'frame'),num(t,'row')):t for t in b['parts']}
 need(len(part_by)==len(b['parts'])==len(projections),'Exactly one real RAM stream per owned direct shadow component')
 copies=rows['MK2_NORMAL_FREEZE_DMA'];counts=defaultdict(int);raw_stock=[];checked_copies=0;own_copies=0
 for p in projections:
  key=(num(p,'frame'),num(p,'row'));need(key in part_by,'Every actual owned shadow has real stream proof')
  q=part_by[key];slot=num(p,'slot');pid=identity if slot==side else 8
  need(num(p,'id')==pid and num(p,'actor')==num(p,'owner')==(actor if slot==side else own)and
       num(p,'main')==(main if slot==side else own_main),'Projection ownership bound to actual live slot')
  component=num(p,'component');parts=native_group(p,payload,guest)
  need(component in range(len(parts))and num(p,'row')==num(p,'cache')+component*112,'Actual component in complete owned ROM group and cache')
  part=parts[component]
  need(all(num(p,k)==v for k,v in part.items()),'Every actual projected word equals draw-time native descriptor and flips')
  need(all(num(q,k)==num(p,k)for k in('frame','slot','actor','row','graphic','width','height','command')),'Stream proof belongs to that exact native component')
  mapped=part['graphic']-(0x0a000000 if 0x10000000<=part['graphic']<0x1a000000 else 0)
  size=int(q['bytes']);need(int(q['mapped'],16)==mapped and size==(part['width']*part['height']*6+part['height']*8+15)//8+4,
                           'Exact compiled native rebasing and complete stream capture bound')
  raw=bytes(gfx[mapped//8:mapped//8+size])
  need(len(raw)==size and hashlib.sha256(raw).hexdigest().upper()==q['sha256'],'Every actual captured sprite byte matches independently interleaved compiled ROM graphics')
  need(num(p,'pc')==0xff8012c0 and num(p,'value')==0x4e90 and num(p,'mask')==65535 and num(p,'body')&16,
       'Actual original shadow opcode and eligible native actor flags')
  camera=num(p,'shadow_camera');b2=num(p,'b2');b4=num(p,'b4');a5=num(p,'a5')
  need(b4==subxy(num(p,'world'),camera)and b2==((num(p,'stageY')-short(camera>>16)+num(p,'b7'))&65535)<<16,
       'Exact original world/camera/B7 native ground projection')
  gap=(short(b2>>16)-(short(b4>>16)-part['dy']))&65535
  x=(short(b4)-part['dx']+(part['width']-1 if part['command']&16 else 0)+short(a5))&1023
  y=(short(b2>>16)-gap//4+short(a5>>16))&511
  actual=[d for d in copies if (num(d,'frame'),num(d,'cache_row'))==key and num(d,'pc')in(0xff8015a0,0xff801610)]
  h=part['height'];need(len(actual)==h//4+1 and bool(actual),'Original quarter-height native DMA count')
  for i,d in enumerate(actual):
   need((num(d,'x'),num(d,'y'),num(d,'width'),num(d,'height'),num(d,'command'),num(d,'palette'),num(d,'color'),num(d,'mask'),num(d,'pc'))==
        (x,(y+i)&511,part['width'],1,part['command']|0x8008,0,0x0f0f,65535,0xff801610 if i==len(actual)-1 else 0xff8015a0),
        'Each original projected shadow copy has exact geometry, native pen and instruction cadence')
  need(num(actual[0],'source')==part['graphic']and num(actual[-1],'source')==num(actual[-2],'source'),
       'Native first source and repeated final row are exact')
  if part['command']&128:
   need(q['streamFormat']=='compressed6'and q['compressedRowStreamVerified'],'Strict six-bit compressed native stream')
   bit=mapped%8;origin=bit;starts=[];headers=[]
   for row in range(h):
    starts.append(part['graphic']+bit-origin)
    header=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&255;bit+=8
    pre=(header&15)<<((part['command']>>8)&3);post=(header>>4)<<((part['command']>>10)&3)
    need(pre+post<=part['width'],'Valid real source-derived row header')
    pixels=part['width']-pre-post;headers.append(dict(row=row,pre=pre,post=post,pixels=pixels));bit+=pixels*6
    need(bit<=len(raw)*8,'Entire independently decoded actual stream')
   need(q['actualRowStarts']==starts and q['actualRowHeaders']==headers and q['usedBits']==bit-origin,
        'Every actual packed row agrees with independent original-ROM decoding')
   indices=list(range(0,4*(h//4),4));indices.append(indices[-1])
   need([num(d,'source')for d in actual]==[starts[i]for i in indices],'All original compressed shadow source steps are exact')
   checked_copies+=len(actual)
   if pid in(17,18):own_copies+=len(actual)
  else:
   need(pid==8 and part==dict(graphic=0x025816f6,width=11,height=18,dx=28 if side==2 else -17,dy=-124,command=0x6000 if side==2 else 0x6010),
        'Only source-proven original Sub-Zero raw ice hand is distinguished, not arbitrary parts')
   need(q['streamFormat']=='stockRaw6'and not q['compressedRowStreamVerified']and not q['stockRawNativeShadowRowSteppingAccepted']and
        q['actualRowStarts']==q['actualRowHeaders']==[],'Stock raw counterexample retained explicitly without claiming compressed stepping')
   raw_stock.append(dict(stage=p['stage'],graphic=f"{part['graphic']:08X}",command=f"{part['command']:04X}",shadowCopies=len(actual)))
  counts[slot,p['stage']]+=1
 need(all(counts[s,stage]==len(native_group(next(p for p in projections if num(p,'slot')==s and p['stage']==stage),payload,guest))
          for s in(1,2)for stage in stages),'Every component of both genuine fighters in all four marked phases')
 need(len(raw_stock)==1,'The exact original raw Sub-Zero hand counterexample is preserved in every control case')
 return dict(fighter=b['fighter'],side=side,identity=identity,ordinaryFields=len(fields),actualPhysicalInputs=len(inputs),actualFullRGBFields=len(stages),jumpTrajectory=[floor-num(fields[i],'y')for i in range(600,681)],
  freezeBegin=cold[0],freezeEnd=cold[-1],freezeFields=len(cold),floor=floor,afterThawMovement=num(fields[467],'x')-num(fields[450],'x'),
  nativeProjectionParts=len(projections),sourceBoundCompressedShadowCopies=checked_copies,addedFighterCompressedShadowCopies=own_copies,
  stockRawCounterexamples=raw_stock,normalFreezeThawAndControlsInstanceVerified=True,sampledSourceBoundShadowInstancesVerified=True,
  fullPortAcceptance=False,normalFreezeCoverageAccepted=False,nativeFloorShadowCoverageAccepted=False)

def main():
 need(not OUT.exists(),'Fresh independently checked native freeze report')
 guest=native.expected();payload=(ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();pins={str(Path(__file__).resolve()):sha(__file__)}
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();lo=(0xff801070-0xff800000)//8;hi=(0xff8017b0-0xff800000)//8
 need(guest[lo:hi]==original[lo:hi],'Entire original native direct shadow kernel unchanged')
 gfx=reconstruct(pins);cases=[];faults=[]
 for fighter,side,identity in CASES:
  b=load(fighter,side)if identity in(17,18)else load(fighter,side,5079,5078);cases.append(check(b,identity,guest,payload,gfx))
  for p,h in b['report']['inputHashes'].items():need(sha(p)==h,'All actual immutable case inputs');pins[p]=h
  for p in[b['report_path'],*(q for q in b['folder'].rglob('*')if q.is_file())]:pins[str(p.resolve())]=sha(p)
  # Faults alter actual records and run semantic/source gates, not merely hashes.
  tests=[]
  def field_fault(label,index,key,value):
   v=copy.deepcopy(b);v['rows']['MK2_NORMAL_FREEZE_FIELD'][index][key]=value;tests.append((label,v))
  field_fault('proxy_identity',240,'victim_id','17' if identity==1 else '1');field_fault('owner_replaced',240,'victim_owner','01000000')
  field_fault('health_damage',150,'hp','160');field_fault('thaw_never_restores',340,'action','0401')
  field_fault('wrong_blue_palette',240,'bank','0303');field_fault('floating_ground',240,'y',str(cases[-1]['floor']-1))
  field_fault('movement_stuck',467,'x',b['rows']['MK2_NORMAL_FREEZE_FIELD'][450]['x']);field_fault('punch_never_starts',512,'action','0303')
  v=copy.deepcopy(b);v['rows']['MK2_STOCK_HEAD_V921_INPUT']=[t for t in v['rows']['MK2_STOCK_HEAD_V921_INPUT']if num(t,'frame')!=num(v['rows']['MK2_STOCK_HEAD_V921_FIRST_LIVE'][0],'frame')+108];tests.append(('physical_lp_missing',v))
  v=copy.deepcopy(b);v['rows']['MK2_NORMAL_FREEZE_ICE_REQUEST'][0]['value']='09C1';tests.append(('native_opcode_changed',v))
  for label,key,value in[('wrong_camera','b4','00000000'),('wrong_native_ground','b2','00000000'),('descriptor_shift','dx','99'),('shadow_owner','owner','01000000')]:
   v=copy.deepcopy(b);v['rows']['MK2_NORMAL_FREEZE_PROJECTION'][0][key]=value;tests.append((label,v))
  for label,key,value in[('shadow_x_shift','x','999'),('shadow_y_shift','y','499'),('wrong_shadow_pen','color','0101'),('wrong_row_source','source','00000001')]:
   v=copy.deepcopy(b);d=next(d for d in v['rows']['MK2_NORMAL_FREEZE_DMA']if num(d,'pc')==0xff8015a0);d[key]=value;tests.append((label,v))
  v=copy.deepcopy(b);v['parts'][0]['actualRowStarts'][1]+=1;tests.append(('packed_row_start_changed',v))
  v=copy.deepcopy(b);v['parts'][0]['sha256']='0'*64;tests.append(('actual_GFX_bytes_wrong',v))
  v=copy.deepcopy(b);next(q for q in v['parts']if q['streamFormat']=='stockRaw6')['stockRawNativeShadowRowSteppingAccepted']=True;tests.append(('stock_raw_falsely_accepted',v))
  for label,index,key,value in[('jump_never_leaves_floor',610,'y',str(cases[-1]['floor'])),
   ('wrong_jump_apex',622,'y',str(cases[-1]['floor']-94)),('landing_stays_airborne',680,'y',str(cases[-1]['floor']-1)),
   ('crouch_not_entered',720,'action','0303'),('high_kick_not_active',774,'action','0103'),
   ('low_kick_not_active',824,'action','0104'),('block_not_active',860,'action','0303'),
   ('uppercut_not_active',924,'action','0302'),('ready_not_restored',1100,'action','0603')]:
   field_fault(label,index,key,value)
  for label,v in tests:
   try:check(v,identity,guest,payload,gfx)
   except ValueError as error:faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(error)))
   else:raise ValueError('Actual-record fault was accepted: '+label)
  print(f'{fighter} P{side}:1101 live fields,38-field native jump, floor/controls/attacks/shadows; {len(tests)} semantic faults rejected',flush=True)
 need(all(case['jumpTrajectory']==cases[4]['jumpTrajectory']for case in cases),
      'Every added fighter/player slot has the entire actual stock Kitana normalized jump trajectory')
 need(all(sha(p)==h for p,h in pins.items()),'All source/native/evidence inputs unchanged at final check')
 report=dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
  cases=cases,actualOrdinaryHealthCases=6,actualAddedFighterPlayerSlotCases=4,actualStockControlCases=2,
  actualOrdinaryFields=sum(c['ordinaryFields']for c in cases),actualFullRGBFields=sum(c['actualFullRGBFields']for c in cases),actualSourceBoundCompressedShadowCopies=sum(c['sourceBoundCompressedShadowCopies']for c in cases),
  actualAddedFighterCompressedShadowCopies=sum(c['addedFighterCompressedShadowCopies']for c in cases),actualFaultsRejected=faults,
  entireAddedFighterJumpTrajectoriesEqualStockControl=True,inputHashes=pins,
  originalShadowKernelUnchanged=True,rawGuestGFXRGBPCMOrWAVFilesWritten=0,
  scope='Four true17/18 human player-slot instances with24 fullRGB idle/ice/jump/landing/crouch/uncrouch/kick-start/contact/recovery/block/uppercut-start/strike/recovery/walk/ready checkpoints and two stock controls with16 checkpoints,1101 contiguous physical live fields each. Entire95-pixel38-field jump trajectories match stock Kitana. Every owned compressed shadow row and exact original projection bound to compiledROM sprite descriptors/bytes and real actor/cache. Stock raw ice-hand stepping remains unaccepted. Older stock sample label air_fall at650 actually means landing; true added falling shadow at635 is observed in5084. No other arena, unsampled move-phase, CPU/repeated/KO/overlap, audio, campaign, finishers or full-port acceptance.',
  normalFreezeThawAndControlsInstancesVerified=True,sampledNativeFloorShadowInstancesVerified=True,
  normalHealthFreezeCoverageAccepted=False,nativeFloorShadowCoverageAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact proof')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','inputHashes','actualFaultsRejected','repeatedReview')},indent=2))

if __name__=='__main__':main()



