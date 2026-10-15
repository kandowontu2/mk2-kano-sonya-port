"""Source-bound two-cycle physical specials, owned actors and native publication.

One Prison/airborne Kitana square wave case per player slot. Routine-entry RGB exists but
entry body provenance is unavailable because its marker is set after draw. Not other arenas, CPU, blocked,
KO, overlap, shadows, audio, full art or full-port acceptance.
"""
import copy,hashlib,json,re,struct,subprocess
from collections import defaultdict
from pathlib import Path
import native_subzero_legs_context_v4993 as native
from verify_move_phase_shadow_v5089 import native_group,short
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_v5124_special_repeat_checked'
SPECS={'knife':(17,0xffffb000),'ball':(17,0xffffde00),'blade':(17,0xfff8cc00),'choke':(17,0xfff91400),
 'ring':(18,0xffffb400),'square':(18,0xffffca00),'bicycle':(18,0xfff9a400),'leg':(18,0xfff80800)}
HEX=set('actor main owner pose vx vy gravity flags body trail bank expectedEntry entry pc at opcode mask a8 a13 facing cache row source size xy command palette clipLow clipHigh display'.split())
def num(r,k):return int(r[k],16 if k in HEX else 10)
def decimal(r,k):return int(r[k])
def load(move,side):
 folder=ROOT/f'audit_v5118_square_air_repeat_{move}_p{side}_kitana'
 report_path=ROOT/f'audit_v5119_square_air_repeat_{move}_p{side}_kitana_observed/report.json'
 report=json.loads(report_path.read_text());text=(folder/'run.log').read_text()
 need('hex='not in text,'No raw guest/GFX/RGB/audio persisted')
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_HSPECIAL_FAILED',text+(folder/'stderr.log').read_text(),re.I),'No runtime/observer failure')
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):
   rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
 return dict(move=move,side=side,folder=folder,report_path=report_path,report=report,rows=rows)
def clean(r):
 return num(r,'y')==num(r,'floor')and all(num(r,k)==0 for k in('vx','vy','gravity','trail'))and num(r,'flags')&0x1c==0 and num(r,'body')&0x0c==0 and num(r,'action')==0x303
def check(b,guest,payload):
 move,side,rows,r=b['move'],b['side'],b['rows'],b['report'];identity,entry=SPECS[move]
 need(r['passed']and r['nativeExit']==0 and r['candidate']==native.NAME and r['executableSHA256']==native.EXE_SHA and r['guestSHA256']==native.GUEST_SHA and r['payloadSHA256']==native.PAYLOAD_SHA,'Actual current terminal candidate')
 need(all(t['move']==move and int(t['side'])==side and t.get('writes','0')=='0'and t.get('assistance','none')=='none'for tag,records in rows.items()if tag not in('MK2_HPHASE_GUEST_DIGEST','MK2_HPHASE_GFX_DIGEST')for t in records),'Every observation belongs to this unassisted physical case')
 terminal=rows['MK2_HSPECIAL_RESULT'];ready=rows['MK2_HSPECIAL_READY'];final=rows['MK2_HSPECIAL_FINAL']
 need(len(terminal)==len(ready)==len(final)==1,'One real ready/final/terminal chronology')
 terminal=terminal[0];first=int(ready[0]['frame']);last=int(final[0]['frame'])
 need(terminal==r['terminalResult']and int(terminal['frame'])==last+1 and terminal['completed']=='2'and terminal['attempt']=='2'and int(terminal['live'])<first,'Both actual cycles and ordinary follow-up reach a real terminal')
 fields=rows['MK2_HPHASE_POST_FIELD'];pre=rows['MK2_HSPECIAL_FIELD']
 by={(int(t['frame']),int(t['slot'])):t for t in fields}
 before={(int(t['frame']),int(t['slot'])):t for t in pre}
 need(len(by)==len(fields)==2*(last-first+1)and set(by)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Complete contiguous post-engine owned fields')
 need(len(before)==len(pre)==2*(last-first+2)and set(before)=={(f,s)for f in range(first,last+2)for s in(1,2)},'Complete contiguous pre-engine owned fields')
 owners={s:(num(by[first,s],'actor'),num(by[first,s],'main'))for s in(1,2)}
 ids={side:identity,3-side:4};floors={s:num(by[first,s],'floor')for s in(1,2)};banks={s:num(by[first,s],'bank')for s in(1,2)}
 need(floors[side]==(82 if identity==17 else 81)and floors[3-side]==83,'Independent own/stock floor anchor values')
 for t in fields+pre:
  s=int(t['slot']);a,m=owners[s]
  need(num(t,'mode')==2 and num(t,'id')==num(t,'roster')==ids[s]and num(t,'state')==1 and num(t,'actor')==num(t,'owner')==a and num(t,'main')==m,'Stable real selected characters and owned live actors, never proxies')
  need(0x01000000<=a<0x01100000 and 0x01000000<=m<0x01100000 and num(t,'floor')==floors[s],'Stable native actor/main and character floor')
  glow=move=='ring'and s==side and num(t,'bank')==0x0404 and num(t,'action')==4 and num(t,'pose')in(0xfe83dbe0,0xfe83dc40,0xfe83dca0,0xfe83dd00)
  need(0<num(t,'hp')<=161 and (num(t,'bank')==banks[s]or glow),'No KO or unowned palette; only source-defined ring charge poses may temporarily use native glow')
 need(all(clean(by[first,s])and clean(by[last,s])and num(by[last,s],'bank')==banks[s]for s in(1,2)),'Both genuine actors clean at ready and final')
 commands=rows['MK2_HSPECIAL_COMMAND'];recoveries=rows['MK2_HSPECIAL_RECOVERED'];repeat=rows['MK2_HSPECIAL_REPEAT_READY']
 need(len(commands)==len(recoveries)==2 and [int(t['attempt'])for t in commands]==[1,2]and [int(t['attempt'])for t in recoveries]==[1,2]and len(repeat)==1,'Two distinct actual command/recovery cycles')
 native_entries=[t for t in rows['MK2_HSPECIAL_EVENT']if num(t,'entry')==entry]
 need(len(native_entries)==2 and [int(t['attempt'])for t in native_entries]==[1,2],'Two actual native special routine entries, not action labels')
 for t in rows['MK2_HSPECIAL_EVENT']:
  at=num(t,'entry');need(at in(entry,0xff861350,0xff861500)and num(t,'pc')==at+16 and num(t,'at')==at and num(t,'mask')==65535 and num(t,'opcode')==struct.unpack_from('<H',guest,(at-0xff800000)//8)[0],'Actual original/native routine opcode, PC and tap mask')
  need(num(t,'actor')==num(t,'a8')==owners[side][0]and num(t,'main')==num(t,'a13')==owners[side][1]and num(t,'id')==identity,'Actual special entry belongs to true own actor and native task')
 inputs=rows['MK2_HSPECIAL_INPUT'];cycle_results=[]
 for i in range(2):
  command,recovery,event=commands[i],recoveries[i],native_entries[i]
  c,z,e=int(command['frame']),int(recovery['frame']),int(event['frame'])
  need(first<c<e<z<last and z-e<400 and num(command,'expectedEntry')==entry,'Real bounded activation and complete natural recovery')
  own,victim=before[c,side],before[c,3-side];forward='Right'if num(own,'x')<num(victim,'x')else'Left';backward='Left'if forward=='Right'else'Right'
  need(command['forward']==forward and int(command['gap'])==abs(num(own,'x')-num(victim,'x'))and all(clean(before[c,s])and clean(before[z,s])and clean(by[z,s])and num(by[z,s],'bank')==banks[s]for s in(1,2)),'Actual physical spacing/facing and both own recovery states')
  if move not in('knife','ring'):need(int(command['gap'])<=63,'Real close approach, no position write')
  schedule=[(c+age,3-side,'Up')for age in range(3)]
  def pulse(button,start,duration):schedule.extend((c+age,side,button)for age in range(start,start+duration))
  if move in('knife','ring','blade','choke'):
   pulse('Down',0,3);pulse(backward if move=='knife'else forward,5,3);pulse('High_Punch'if move in('knife','blade')else'Low_Punch',6,3)
  elif move=='square':pulse(forward,0,3);pulse(backward,5,3);pulse('High_Punch',6,3)
  elif move=='ball':pulse('Low_Kick',0,84)
  elif move=='bicycle':pulse(backward,0,3);pulse(backward,6,3);pulse('Down',12,3);pulse('High_Kick',13,3)
  elif move=='leg':pulse('Down',0,7);pulse('Low_Punch',3,4);pulse('Block',3,4)
  actual=[(int(t['frame']),int(t['slot']),t['button'])for t in inputs if c<=int(t['frame'])<=z]
  need(actual==sorted(schedule,key=lambda v:v[0]),'Exact real physical command inputs through recovery; no hidden writes or helper attacks')
  victim_damage=num(before[c,3-side],'hp')-num(by[z,3-side],'hp')
  need(victim_damage>=0 and num(before[c,side],'hp')==num(by[z,side],'hp')==161,'Actual passive victim damage, never own identity/health substitution')
  need(victim_damage==27,'Actual airborne square wave delivers native27 damage in each cycle')
  hits=[h for h in rows['MK2_HSPECIAL_HEALTH']if c<=int(h['frame'])<=z and int(h['after'])<int(h['before'])]
  need(len(hits)==1 and e<int(hits[0]['frame'])<z and all(num(before[int(hits[0]['frame']),s],'y')<floors[s]for s in(1,2)),'Actual single square hit while both genuine actors are airborne')
  cycle_results.append(dict(attempt=i+1,command=c,entry=e,recovered=z,forward=forward,victimDamage=victim_damage,activationLatency=e-c,recoveryFields=z-e))
 need(int(repeat[0]['frame'])==cycle_results[0]['recovered']+32 and int(commands[1]['frame'])>int(repeat[0]['frame'])and all(clean(before[int(repeat[0]['frame']),s])for s in(1,2)),'First complete cleanup and real settling before reuse')
 followup=int(terminal['followup']);need(followup==cycle_results[1]['recovered']+16 and last==followup+160,'Actual ordinary follow-up timing')
 want=[(followup+i,side,cycle_results[1]['forward'])for i in range(8)]+[(followup+i,side,'Up')for i in range(40,43)]+[(followup+i,side,'High_Punch')for i in range(112,115)]
 got=[(int(t['frame']),int(t['slot']),t['button'])for t in inputs if int(t['frame'])>=followup]
 need(got==want,'Exact physical walk/jump/punch after second recovery')
 need(any(num(by[f,side],'x')!=num(by[followup,side],'x')for f in range(followup+1,followup+16))and any(num(by[f,side],'y')<floors[side]for f in range(followup+40,followup+85))and any(num(by[f,side],'action')==0x101 for f in range(followup+112,followup+140)),'Post-special movement, jump and native punch actually activate')
 health=rows['MK2_HSPECIAL_HEALTH'];health_by=defaultdict(list)
 for h in health:
  need(num(h,'pc')==0xff836700 and num(h,'mask')==65535 and int(h['slot'])==3-side and 0<int(h['after'])<=int(h['before'])<=161,'Health changes use actual unchanged native damage primitive only')
  health_by[int(h['frame']),int(h['slot'])].append(h)
 for key,t in by.items():
  hp=num(before[key],'hp')
  for h in health_by[key]:need(hp==int(h['before']),'Complete real damage-write chronology');hp=int(h['after'])
  need(hp==num(t,'hp'),'Every actual health change explained by native write observations')
 scenes=r['actualScenes'];need(len({s['frame']for s in scenes})==len(scenes),'Actual uniquely captured native RGB fields')
 snaps=rows['MK2_HPHASE_SNAP'];digests=rows['MK2_HPHASE_RGB_DIGEST']
 need([(int(t['frame']),int(t['attempt']),t['stage'])for t in snaps]==[(s['frame'],s['attempt'],s['stage'])for s in scenes],'Every actual frame_done scene label accounted')
 need([(int(t['frame']),int(t['attempt']),t['stage'],t['sha256'])for t in digests]==[(s['frame'],s['attempt'],s['stage'],s['sha256'])for s in scenes]and all(s['width']==400 and s['height']==254 and s['bytes']==406400 and s['rawMediaFilesWritten']==0 for s in scenes),'Actual full native scene transport digests, never proxy screenshots')
 for c in cycle_results:
  for stage,key in [('special_before','command'),('entry','entry'),('special_recovered','recovered')]:
   need(any(s['frame']==c[key]and s['stage']==stage and s['attempt']==c['attempt']for s in scenes),'Before/actual-entry/complete-recovery scene for each cycle')
 frames={s['frame']for s in scenes};candidates=rows['MK2_HPHASE_CANDIDATE'];queues=rows['MK2_HPHASE_QUEUE']
 cm={(int(t['frame']),int(t['slot']),int(t['part'])):t for t in candidates};qm={(int(t['frame']),int(t['slot']),int(t['part'])):t for t in queues}
 need(len(cm)==len(candidates)and len(qm)==len(queues)and cm,'Unique actual pre-clip candidates and body publications')
 compositions=defaultdict(list);visible=set();clipped=0
 for key,t in cm.items():
  f,s,part=key;need(f in frames and s in(1,2)and num(t,'pc')==0xff8042b0 and num(t,'row')==num(t,'cache')+part*112,'Exact actual native pre-clip instruction/cache provenance')
  need(num(t,'actor')==num(t,'owner')==owners[s][0]and num(t,'main')==owners[s][1]and num(t,'id')==num(t,'roster')==ids[s],'Source publication belongs to real stable own character')
  group=native_group(t,payload,guest);need(part in range(len(group)),'Actual part index in complete terminated source group');p=group[part]
  need((num(t,'source'),num(t,'size'),num(t,'command'))==(p['graphic'],p['width']|(p['height']<<16),(p['command']|0x8002)<<16),'Actual native source/size/command matches independently read complete picture descriptor')
  need(num(t,'clipLow')==0 and num(t,'clipHigh')==0x00fe0190,'Original native clip rectangle')
  x,y=short(num(t,'xy')),short(num(t,'xy')>>16);w,h=p['width'],p['height'];shown=x+w>0 and y+h>0 and x<400 and y<254
  need((key in qm)==shown,'Every complete native body component published iff it intersects screen')
  if shown:
   visible.add(key);q=qm[key]
   need(num(q,'pc')==0xff804420 and all(q[k]==t[k]for k in('actor','main','owner','id','roster','pose','facing','body','cache','part','row','source','size','command')),'Actual candidate-to-FIFO ownership and source unchanged')
   dx,dy=short(num(t,'display')),short(num(t,'display')>>16);cmd=num(t,'command')>>16
   need(num(q,'xy')==(((x+(w-1 if cmd&16 else 0)+dx)&65535)|(((y+(h-1 if cmd&32 else 0)+dy)&65535)<<16)),'Exact native flips and display-base position')
  else:clipped+=1
  compositions[f,s].append(part)
 entry_frames={c['entry']for c in cycle_results}
 need(visible==set(qm)and set(compositions)=={(f,s)for f in frames-entry_frames for s in(1,2)},'Both entire genuine body composites evaluated at all pre-marked sampled fields; entry marked only after native draw remains unproven')
 for key,parts in compositions.items():
  t=cm[key[0],key[1],0];need(parts==list(range(len(native_group(t,payload,guest)))),'Every owned terminated composite part accounted, including culled parts')
 return dict(move=move,side=side,trueIdentity=identity,cycles=cycle_results,contiguousPostFields=len(fields),actualFullRGBFields=len(scenes),entryBodyPublicationUnobservedFrames=sorted(entry_frames),sourceBoundBodyCandidates=len(candidates),nativePublishedBodyParts=len(queues),nativeClippedParts=clipped,actualNativeHealthWrites=len(health),ownDistinctPoses=len({t['pose']for t in fields if int(t['slot'])==side}),twoRealSpecialCyclesAndCleanupVerified=True,actualSquareContactVerified=True,fullArtAcceptance=False,nativeShadowAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False)
def main():
 need(not OUT.exists(),'Fresh independently checked repeated-special report')
 guest=native.expected();payload=(ROOT/native.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes();original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 lo=(0xff804160-0xff800000)//8;hi=(0xff804430-0xff800000)//8
 need(guest[lo:hi]==original[lo:hi],'Entire native multipart clipping/flip/publication path unchanged')
 pins={str(Path(__file__).resolve()):sha(__file__),str((ROOT/'tools/verify_move_phase_shadow_v5089.py').resolve()):sha(ROOT/'tools/verify_move_phase_shadow_v5089.py')};cases=[];faults=[]
 for move in('square',):
  for side in(1,2):
   b=load(move,side);cases.append(check(b,guest,payload))
   for p,h in b['report']['inputHashes'].items():need(sha(p)==h,'Executed immutable source/candidate inputs');pins[p]=h
   for p in[b['report_path'],*(p for p in b['folder'].rglob('*')if p.is_file())]:pins[str(p.resolve())]=sha(p)
   tests=[]
   def change(label,tag,index,key,value):
    v=copy.deepcopy(b);v['rows'][tag][index][key]=value;tests.append((label,v))
   change('proxy_identity','MK2_HPHASE_POST_FIELD',0,'id','1')
   change('owner_replaced','MK2_HPHASE_POST_FIELD',0,'owner','01000000')
   change('floor_shifted','MK2_HPHASE_POST_FIELD',0,'floor','99')
   change('palette_stuck','MK2_HPHASE_POST_FIELD',0,'bank','00000505')
   change('missing_actual_entry_opcode','MK2_HSPECIAL_EVENT',0,'opcode','FFFF')
   change('missing_physical_command','MK2_HSPECIAL_INPUT',next(i for i,t in enumerate(b['rows']['MK2_HSPECIAL_INPUT'])if int(t['frame'])==int(b['rows']['MK2_HSPECIAL_COMMAND'][0]['frame'])and int(t['slot'])==side),'button','Up')
   hit_frame=int(next(h for h in b['rows']['MK2_HSPECIAL_HEALTH']if int(h['after'])<int(h['before']))['frame'])
   air_index=next(i for i,t in enumerate(b['rows']['MK2_HSPECIAL_FIELD'])if int(t['frame'])==hit_frame and int(t['slot'])==3-side)
   change('victim_never_airborne_at_contact','MK2_HSPECIAL_FIELD',air_index,'y','83')
   change('recovery_still_moving','MK2_HPHASE_POST_FIELD',len(b['rows']['MK2_HPHASE_POST_FIELD'])-1,'vx','00010000')
   change('descriptor_source_corrupt','MK2_HPHASE_CANDIDATE',0,'source','00000000')
   change('fifo_position_shifted','MK2_HPHASE_QUEUE',0,'xy','00000000')
   v=copy.deepcopy(b);v['rows']['MK2_HPHASE_POST_FIELD'].pop();tests.append(('missing_live_field',v))
   v=copy.deepcopy(b);v['rows']['MK2_HSPECIAL_RECOVERED'].pop();tests.append(('missing_second_recovery',v))
   v=copy.deepcopy(b);v['rows']['MK2_HPHASE_CANDIDATE'].pop();tests.append(('missing_native_body_part',v))
   if move=='ring':
    glow_index=next(i for i,t in enumerate(b['rows']['MK2_HPHASE_POST_FIELD'])if num(t,'bank')==0x0404)
    change('glow_on_uncharged_pose','MK2_HPHASE_POST_FIELD',glow_index,'pose','FE83DEC0')
   for label,v in tests:
    try:check(v,guest,payload)
    except ValueError as error:faults.append(dict(move=move,side=side,fault=label,rejectedBy=str(error)))
    else:raise ValueError('Actual semantic fault accepted: '+label)
   print(f'{move} P{side}: two true entries/recoveries, {cases[-1]["contiguousPostFields"]} contiguous post-fields; {len(tests)} semantic faults rejected',flush=True)
 need(all(sha(p)==h for p,h in pins.items()),'All compiled/source/evidence pins unchanged at final independent check')
 report=dict(passed=True,candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,payloadSHA256=native.PAYLOAD_SHA,cases=cases,actualCases=len(cases),actualVerifiedSpecialCycles=4,actualContiguousPostFields=sum(c['contiguousPostFields']for c in cases),actualFullRGBFields=sum(c['actualFullRGBFields']for c in cases),sourceBoundBodyCandidates=sum(c['sourceBoundBodyCandidates']for c in cases),actualNativePublishedBodyParts=sum(c['nativePublishedBodyParts']for c in cases),actualSemanticFaultsRejected=faults,inputHashes=pins,scope=__doc__,airborneSquareBothPlayerSlotsRepeatTwiceAndRecoverVerified=True,actualSquareContactCoverageAccepted=False,nativeFloorShadowCoverageAccepted=False,fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,rawGuestGFXRGBPCMOrWAVFilesWritten=0)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress compact proof')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','actualSemanticFaultsRejected')},indent=2))
if __name__=='__main__':main()






