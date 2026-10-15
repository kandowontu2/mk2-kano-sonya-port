"""Original throw/victim routing plus current owned capture/HP callbacks; no emulator."""
import json,subprocess
import verify_native_source_sync as sync
from check_campaign_stage_chronology import load
sync.verify()
root=sync.ROOT;stock=root/'mk2/mk2-maincpu.bin';exe=root/'mame-mkp/unidasm.exe'
out=root/'audit_current_sonya_p1_kintaro_victim_capture_checked';assert not out.exists()
assert sync.sha(stock)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
def dis(at,bits):return subprocess.check_output([str(exe),str(stock),'-arch','tms34010','-skip',str((at-0xff800000)//8),'-count',str(bits),'-basepc',hex(at),'-norawbytes'],text=True)
segments={'throw':dis(0xff9cbf80,1456),'capture':dis(0xff842710,1152),'victim':dis(0xff8e5c90,160),'hp_route':dis(0xff837340,176),'hp_store':dis(0xff8364c0,576),'attack_flag':dis(0xff877bc0,384),'range_gate':dis(0xff9cfb20,160),'throw_gate':dis(0xff9cbea0,256),'airkick':dis(0xff871e40,1136)}
needles={'throw':['ff9cc030: CALLA  FF842710h','ff9cc060: MOVI   507h,A1','ff9cc080: MOVE   A1,*A13(1F0h),0','ff9cc300: MOVI   FF8E5C90h,A7','ff9cc330: CALLA  FF8429A0h'],
 'capture':['ff842830: MOVE   *A13(140h),A8,1','ff842850: MOVE   *A13(170h),A13,1','ff842880: MOVE   A0,*A13(1F0h),0','ff8429a0: MOVE   *A13(170h),A0,1','ff8429c0: JA     FF83F930h'],
 'victim':['ff8e5c90: MOVI   28h,A10','ff8e5cc0: CALLA  FF837340h'],
 'hp_route':['ff837360: MOVE   @1060220h,A7,1','ff837390: CMP    A7,A8','ff8373d0: JR     FF8364C0h'],
 'hp_store':['ff8366c0: SUB    A10,A1','ff8366f0: MOVE   A1,*A6,0'],
 'attack_flag':['ff877d00: ORI    10h,A4','ff877d30: MOVE   A4,*A13(210h),0'],
 'range_gate':['ff9cfb50: CMPI   78h,A3','ff9cfb70: JRHI   FF9CFBA0h','ff9cfb80: SETC'],
 'throw_gate':['ff9cbea0: CALLA  FF9CFB20h','ff9cbed0: JRC    FF9CBF80h'],
 'airkick':['ff872090: MOVI   60Dh,A0','ff8720b0: MOVE   A0,*A13(1F0h),0','ff872250: MOVI   60Dh,A0','ff872270: MOVE   A0,*A13(1F0h),0']}
def sourcegate(parts):
 for tag,needed in needles.items():assert all(n in parts[tag] for n in needed)
sourcegate(segments)
faults=[]
for tag,needed in needles.items():
 for i,n in enumerate(needed):
  broken=dict(segments);broken[tag]=broken[tag].replace(n,'',1)
  try:sourcegate(broken)
  except AssertionError:faults.append(tag+':'+str(i))
  else:raise AssertionError('Removed original instruction accepted')
path=root/'audit_current_sonya_p1_liukang_short_leg_runtime/run.log';rows=load(path)
fields={int(r['frame']):r for r in rows['BOSS_FIELD'] if r['stage']=='15'}
captures=[r for r in rows['BOSS_ACTION'] if r['stage']=='15' and r['pc']=='FF8428A0' and r['after']=='0']
pairs=[]
for c in captures:
 assert c['id']==c['roster']=='18' and c['actor']==c['owner']==c['a8'] and c['main']==c['a13'] and int(c['at'],16)==int(c['main'],16)+0x1f0 and c['mask']=='FFFF'
 frame=int(c['frame'])+32
 matching=[r for r in rows['HEALTH'] if int(r['frame'])==frame and r['slot']=='1' and r['pc']=='FF836700' and r['a8']==c['actor'] and r['a13']==c['main'] and int(r['before'])-int(r['after'])==min(40,int(r['before']))]
 if not matching:continue
 f=fields[frame]
 assert f['human_id']=='18' and f['cpu_id']=='12' and f['cpu_action']=='1287' and f['human_actor']==c['actor'] and f['human_main']==c['main']
 pairs.append(dict(captureStore=c,healthWrite=matching[0],damageField=f,delayFields=32))
assert len(pairs)==5
light=load(root/'audit_current_sonya_p1_boss_light_runtime/run.log')
plans=[r for r in light['BOSS_PLAN'] if r['stage']=='15' and r['move']=='close_pressure_jumpkick_attempt' and r['cpu_action']=='1287']
report=dict(originalRoutingInstructions=segments,removedInstructionFaults=faults,
 actualOwnedHumanCaptureStores=captures,matchedVictimDamagePairs=pairs,
 originalKintaroThrowVictimDamage=40,originalKintaroThrowRangeGate=120,
 actualBaselineJumpPlansDuringCPUThrowAction=plans,
 callbackActorRegistersAreVictimContextNotAttackerOwnership=True,
 CPUThrowSetterInstructionObserved=False,completeAttackCausalityAccepted=False,
 airkick1549IsBothContactAndMissRecoveryNotBlockedProof=True,
 proposedUnexecutedVariant='Keep forward jumps; guard rather than begin a new grounded jump while native CPU attack flag10 is set, preserve stomp upper/airborne continuation priority',
 fullPortAccepted=False,logSHA256=sync.sha(path))
out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(sourceFaults=len(faults),captureStores=len(captures),pairedVictimDamage=len(pairs),jumpPlansDuringCPUThrow=len(plans))))
