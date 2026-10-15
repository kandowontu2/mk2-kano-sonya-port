"""Current ordinary control/state/health plus unchanged full body/shadow kernels.

Four real character/physical-slot Dead Pool/Kitana contexts only. Require actual
settled crouch attacks, not phase labels/input attempts. No universal arena/CPU,
KO, full scene/audio/artistic or all-aspects port claim.
"""
import copy,inspect,json,re,struct,traceback
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_special_shadow_v5141 as body
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6015_current_ordinary_ground_shadow_checked'
PHASES=[(0,'idle'),(32,'forward_walk'),(76,'backward_walk'),(120,'neutral_jump'),(200,'forward_jump'),(280,'backward_jump'),
        (360,'crouch'),(420,'standing_block'),(480,'crouch_block'),(540,'high_punch'),(600,'low_punch'),(660,'high_kick'),(720,'low_kick'),
        (780,'crouch_punch'),(840,'crouch_kick'),(900,'uppercut'),(960,'sweep'),(1020,'roundhouse'),(1080,'close_approach'),
        (1160,'close_high_punch'),(1220,'close_high_kick'),(1280,'opponent_blocked_punch'),(1360,'close_low_punch'),(1420,'close_low_kick'),(1480,'final_recovery')]

def state_gate(b,guest,payload):
 rows=b['rows'];side=b['side'];identity=17 if b['fighter']=='kano'else 18
 final=rows['MK2_BASIC_RESULT'];need(len(final)==1,'One ordinary native terminal result')
 final=final[0];ready=int(final['ready'])
 need(final['completed']=='1'and final['phases']=='25'and int(final['terminalAge'])==1541 and
      [(int(r['frame'])-ready,r['phase'])for r in rows['MK2_BASIC_STEP']]==PHASES,'Whole real ordinary phase sequence and queued-exit terminal')
 fields=rows['MK2_HPHASE_POST_FIELD'];posts={(int(r['frame'])-ready,int(r['slot'])):r for r in fields}
 pres={(int(r['frame'])-ready,int(r['slot'])):r for r in rows['MK2_BASIC_FIELD']}
 need(len(posts)==len(fields)==3082 and set(posts)=={(a,s)for a in range(1541)for s in(1,2)}and
      set(pres)=={(a,s)for a in range(1542)for s in(1,2)},'Every pre/draw-complete actor field contiguous, one extra shutdown callback but no invented draw')
 ids={side:identity,3-side:4};anchors={17:134,18:135,4:133}
 for (age,slot),r in posts.items():
  need(r['writes']=='0'and r['assistance']=='none'and int(r['mode'])==2 and int(r['stage'])==0 and
       int(r['id'])==int(r['roster'])==ids[slot]and int(r['state'])==1 and r['actor']==r['owner']and
       0<int(r['hp'])<=161 and int(r['floor'])==int(r['stageY'])-anchors[ids[slot]],
       'Every true original physical actor, healthy ordinary match and source-defined stage-relative own floor')
 own=lambda a:posts[a,side]
 pre=lambda a:pres[a,side]
 sign=1 if int(pre(0)['x'])<int(pres[0,3-side]['x'])else-1
 need(sign*(int(pre(56)['x'])-int(pre(32)['x']))==60 and sign*(int(pre(100)['x'])-int(pre(76)['x']))==-48,
      'Native24field forward2.5/backward2pixel walking distance, both physical facings')
 jumps=[]
 for start,label in((120,'neutral_jump'),(200,'forward_jump'),(280,'backward_jump')):
  window=[own(a)for a in range(start,start+60)]
  airborne=[r for r in window if int(r['y'])<int(r['floor'])]
  need(len(airborne)>=24 and max(int(r['floor'])-int(r['y'])for r in window)>=60 and
       int(own(start+60)['y'])==int(own(start+60)['floor'])and own(start+60)['vy']=='00000000'and own(start+60)['gravity']=='00000000',
       'Actual airborne path and complete grounded/velocity/gravity landing: '+label)
  jumps.append(dict(phase=label,airborneFields=len(airborne),peakAboveOwnedFloor=max(int(r['floor'])-int(r['y'])for r in window)))
 observed=[]
 for start,label,code in((360,'crouch',770),(420,'standing_block',1792),(480,'crouch_block',1793),
                         (540,'high_punch',257),(600,'low_punch',258),(660,'high_kick',259),(720,'low_kick',260),
                         (780,'crouch_punch',281),(840,'crouch_kick',282),(900,'uppercut',263),(960,'sweep',262),(1020,'roundhouse',261)):
  window=[own(a)for a in range(start,start+55)]
  need(any(int(r['action'])==code for r in window)and len({r['pose']for r in window})>1,
       'Actual native action/owned pose phase activated, not a label or ignored button: '+label)
  observed.append(dict(phase=label,nativeAction=code,actionFields=sum(int(r['action'])==code for r in window),poses=len({r['pose']for r in window})))
 for age in range(1541):
  if not any(start<=age<start+60 for start in(120,200,280)):
   need(int(own(age)['y'])==int(own(age)['floor']),'No persistent vertical shift during ordinary non-airborne phases')
 # Complete both physical health histories, including actual hit/block events.
 stores=rows['MK2_BASIC_HEALTH'];totals={1:0,2:0};count=0
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();at=(0xff836700-48-0xff800000)//8
 need(guest[at:at+6]==original[at:at+6],'Whole original native health-store instruction')
 for age in range(1541):
  for slot in(1,2):
   hp=int(pres[age,slot]['hp'])
   for r in [r for r in stores if int(r['frame'])-ready==age and int(r['slot'])==slot]:
    need(int(r['before'])==hp and 0<=int(r['after'])<=hp and int(r['pc'],16)==0xff836700 and int(r['mask'],16)==65535,
         'Every actual native damage store continuous and source-bound')
    totals[slot]+=hp-int(r['after']);hp=int(r['after']);count+=1
   need(hp==int(posts[age,slot]['hp'])==int(pres[age+1,slot]['hp']),'Exact pre/store/draw-complete/next-callback health chain')
 need(count==len(stores)>=3 and totals[side]==0 and totals[3-side]>0,'Actual ordinary contacts, no synthetic damage or omitted stores')
 end=own(1540)
 need(int(end['y'])==int(end['floor'])and all(end[k]=='00000000'for k in('vx','vy','gravity','trail'))and
      int(end['flags'],16)&0x1c==0 and int(end['body'],16)&0x0c==0 and int(end['action'])==771,
      'Clean final real native stance, ground, velocities, body flags and trail retirement')
 return dict(passed=True,actualPhases=25,completePostActorFields=len(fields),completePreActorFields=len(pres),
             actualJumps=jumps,actualOrdinaryActionPhases=observed,nativeHealthStores=count,totalActualDamageByPhysicalSlot=totals,
             trueIdentity=identity,physicalSlot=side,stage=0,sourceDefinedOwnedFloorAccepted=True,
             allThreePreviouslyUnactivatedCrouchAttacksNowActivated=True,fullPortAcceptance=False)

def bindings():
 source=inspect.getsource(body.check)
 first=source.index(' # The older physical/ownership/health checker');last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
 source=source[:first]+" state=state_gate(b,guest,payload)\n entry_frames=set()\n"+source[last:]
 scope=dict(body.check.__globals__,state_gate=state_gate)
 exec(compile(source,__file__+'::whole_original_body_shadow_kernels_ordinary_physical_gate','exec'),scope)
 return scope['check']

def load(fighter,side):
 folder=ROOT/f'audit_v6012_basic_{fighter}_p{side}';report_path=ROOT/f'audit_v6013_basic_{fighter}_p{side}_observed/report.json'
 report=json.loads(report_path.read_text());need(report['passed']and report['nativeExit']==0 and report['candidate']==current.NAME and
      report['executableSHA256']==current.EXE_SHA and report['guestSHA256']==current.GUEST_SHA and report['payloadSHA256']==current.PAYLOAD_SHA,
      'Actual terminal current no-proxy ordinary capture')
 text=(folder/'run.log').read_text();need('hex='not in text and (folder/'stderr.log').read_text()==''and 'MK2_BASIC_FAILED'not in text,'No raw buffer persistence or native/control failure')
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_BASIC_','MK2_HPHASE_')):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique real protocol fields');rows[line.split()[0]].append(dict(pairs))
 return dict(fighter=fighter,move='knife'if fighter=='kano'else'ring',side=side,folder=folder,report_path=report_path,report=report,
             rows=rows,streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))

def run():
 need(not OUT.exists(),'Fresh immutable full ordinary grounding proof')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 baseline_path=ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json';baseline=json.loads(baseline_path.read_text())
 need(baseline['passed']and sha(body.__file__)==baseline['inputHashes'][str(Path(body.__file__).resolve())],
      'Entire independently qualified original body/shadow model unchanged')
 pins={str(Path(__file__).resolve()):sha(__file__),str(baseline_path):sha(baseline_path)}
 gfx=body.reconstruct(pins)
 own=current.expected_gfx();gfx[0x1fa0000:0x1fa0000+11944]=own[:11944];gfx[0x1fa4000:0x1fa4000+7032]=own[11944:]
 for header,magic in((0x1c0000,b'KFX1'),(0x1c1000,b'KPI1'),(0x1c2000,b'KPJ1'),(0x1d0000,b'KBL1')):
  need(payload[header:header+4]==magic,'Actual runtime graphics patch header');source,count,dest=struct.unpack_from('<III',payload,header+4)
  need(source+count<=len(payload)and dest+count<=len(gfx),'Whole source-bounded payload graphics patch');gfx[dest:dest+count]=payload[source:source+count]
 current_driver=ROOT/current.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 prior_driver=ROOT/'diagnostic_v4992_native_subzero_legs/input_sources/mame-mkp/src/mame/midway/midtunit.cpp'
 declaration=lambda p:p.read_text().split('ROM_START( mk2ks )',1)[1].split('ROM_END',1)[0].split('ROM_REGION( 0x2000000, "gfxrom", ROMREGION_ERASE00 )',1)[1]
 need(declaration(current_driver)==declaration(prior_driver),'Actual current full compiled graphics lanes equal independent source constructor')
 pins[str(current_driver)]=sha(current_driver)
 original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
  need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],'Whole original native body/shadow kernels unchanged')
 check=bindings();cases=[];faults=[]
 for fighter in('kano','sonya'):
  for side in(1,2):
   b=load(fighter,side);case=check(b,guest,payload,gfx);case['fighter']=fighter
   case.update(entryBodyPublicationProven=False,ordinaryControlEntryAndAllFieldsChecked=True,
               currentOrdinaryBodyAndOriginalFloorShadowGeometryAccepted=True,
               fullArtAcceptance=False,fullAudioAcceptance=False,allArenaCPUOrKOOverlapAccepted=False)
   for p,h in b['report']['inputHashes'].items():need(sha(p)==h,'Every current executed source/compiled dependency stable');pins[p]=h
   for p in b['folder'].rglob('*'):
    if p.is_file():pins[str(p)]=sha(p)
   pins[str(b['report_path'])]=sha(b['report_path'])
   tests=[('physical_proxy_ID','MK2_HPHASE_POST_FIELD','id','1'),('physical_wrong_floor','MK2_HPHASE_POST_FIELD','floor','999'),
          ('physical_owner','MK2_HPHASE_POST_FIELD','owner','01000000'),('physical_hp','MK2_HPHASE_POST_FIELD','hp','160'),
          ('body_wrong_source','MK2_HPHASE_CANDIDATE','source','00000000'),('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),
          ('projection_shift','MK2_HPHASE_PROJECTION','dy','999'),('native_floor','MK2_HPHASE_PROJECTION','floor','999'),
          ('native_shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),('native_shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),
          ('native_shadow_row','MK2_HPHASE_SHADOW_DMA','source','00000001')]
   for label,tag,key,value in tests:
    changed=copy.deepcopy(b);need(changed['rows'][tag][0][key]!=value,'Fault changes an actual record, never no-op');changed['rows'][tag][0][key]=value
    try:check(changed,guest,payload,gfx)
    except ValueError as error:faults.append(dict(fighter=fighter,side=side,fault=label,rejectedBy=str(error)))
    else:raise ValueError('Actual ordinary semantic fault accepted: '+label)
   changed=copy.deepcopy(b);changed['streams'][0]['sha256']='0'*64
   try:check(changed,guest,payload,gfx)
   except ValueError as error:faults.append(dict(fighter=fighter,side=side,fault='actual_ROM_stream_changed',rejectedBy=str(error)))
   else:raise ValueError('Actual graphics source fault accepted')
   cases.append(case);print(fighter+' P'+str(side)+': all actual ordinary state/body/shadow fields and12 semantic faults qualified',flush=True)
 for p in(Path(body.__file__).resolve(),ROOT/'tools/verify_move_phase_shadow_v5089.py'):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual captures/sources/old evidence unchanged')
 return dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,
             payloadSHA256=current.PAYLOAD_SHA,cases=cases,actualSemanticFaultsRejected=faults,inputHashes=pins,
             actualCurrentBothCharactersBothPhysicalSlotsOrdinaryGroundingAndNativeShadowsAccepted=True,
             allThreeSettledCrouchAttacksActuallyActivated=True,actualActorFields=sum(c['actualContiguousActorFields']for c in cases),
             nativeBodyCandidates=sum(c['actualNativeBodyCandidates']for c in cases),
             nativeShadowCopies=sum(c['actualSourceBoundShadowCopies']for c in cases),
             previewPNGArtifactsWritten=24,rawGuestGFXVRAMRGBPCMOrWAVFilesWritten=0,
             continuousWholeRGBSceneReplayAccepted=False,allArenaCPUOrKOOverlapAccepted=False,
             fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
