"""Source-bound actual native round-reset queue cancellation, no fabricated DMA."""
import copy,ctypes,datetime,json,re,struct,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import save_current_cpu_audio_progress_v5326 as scope
ROOT,need,sha=current.ROOT,current.need,current.sha
FOLDER=ROOT/'audit_v5397_ko_queue_lifecycle'
OBSERVED=ROOT/'audit_v5398_ko_queue_lifecycle_observed/report.json'
PARENT=ROOT/'audit_v5395_current_ko_round_body_shadow_progress/progress.json'
BODY=ROOT/'audit_v5393_current_ko_round_body_shadow_checked/report.json'
OUT=ROOT/'audit_v5400_ko_queue_lifecycle_checked'
HEX=set('p1 p2 queue b13 b14 b8 a1 at pc opcode mask before after'.split())
def num(t,k):return int(t[k],16 if k in HEX else 10)

def decode(log):
 result=[]
 for line in log.splitlines():
  if line.startswith('MK2_QUEUE_LIFECYCLE_')and not line.startswith('MK2_QUEUE_LIFECYCLE_GUEST '):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique actual lifecycle fields')
   t=dict(pairs);t['kind']=line.split()[0].split('MK2_QUEUE_LIFECYCLE_',1)[1];result.append(t)
 return result

def check(rows,guest):
 need([num(t,'event')for t in rows]==list(range(1,len(rows)+1)),'Entire actual ordered queue observer, no omitted or invented event')
 need(all(t['assistance']=='none'and num(t,'writes')==0 for t in rows),'Actual lifecycle taps remain read-only')
 for kind in('PRE','POST'):
  need([num(t,'frame')for t in rows if t['kind']==kind]==list(range(3198,3221)),'Every genuine native boundary callback retained')
 code=[t for t in rows if t['kind']=='CODE']
 for t in code:
  address=num(t,'at');need(num(t,'pc')==address+16 and num(t,'mask')==65535 and
   struct.unpack_from('<H',guest,(address-0xff800000)//8)[0]==num(t,'opcode'),'Every actual native queue instruction equals whole independently reconstructed guest')
 resets=[]
 for i,t in enumerate(rows):
  if t['kind']=='CODE'and num(t,'at')==0xff808b00:
   need(i+2<len(rows),'Complete native queue register reset')
   b,c=rows[i+1:i+3]
   need(b['kind']==c['kind']=='CODE'and(num(b,'at'),num(c,'at'))==(0xff808b10,0xff808b20)and
    (num(t,'frame'),num(t,'mode'))==(num(b,'frame'),num(b,'mode'))==(num(c,'frame'),num(c,'mode')),
    'Actual adjacent MOV A1,B14 / CLR B13 / RETS sequence, no callback substitution')
   need(num(t,'a1')==0x0101f700 and num(b,'b14')==num(c,'b14')==num(t,'a1')and
    num(t,'b13')==num(b,'b13')and num(c,'b13')==0,'Exact native pointer reset and complete pending packet cancellation')
   resets.append(dict(frame=num(t,'frame'),mode=num(t,'mode'),pendingBefore=num(t,'b13'),pendingAfter=num(c,'b13'),oldDrainPointer=f'{num(t,"b14"):08X}',newDrainPointer=f'{num(c,"b14"):08X}'))
 need(len(resets)==24 and [r for r in resets if r['pendingBefore']]!=[],'Every original per-field reset plus actual extra transition reset')
 cancellations=[r for r in resets if r['pendingBefore']]
 need(len(cancellations)==1 and (cancellations[0]['frame'],cancellations[0]['mode'],cancellations[0]['pendingBefore'],cancellations[0]['pendingAfter'])==(3208,6,89,0),
  'Only actual native retirement mode6 cancels89 outstanding queue packets')
 timeline=[t for t in rows if num(t,'frame')==3208]
 addresses=(0xff818e30,0xff818e80,0xff83f410,0xff83f4c0,0xff808310,0xff8083b0,0xff808780,0xff808900,0xff808930,0xff808960)
 selected=[]
 for address in addresses:
  found=[t for t in timeline if t['kind']=='CODE'and num(t,'at')==address]
  need(len(found)==1,'Exactly one source-bound actual round-reset chain node');selected.append(found[0])
 need([num(t,'event')for t in selected]==sorted(num(t,'event')for t in selected),'Entire native mode6/reset/callback order exact')
 need(num(selected[0],'mode')==5 and all(num(t,'mode')==6 for t in selected[1:]),'Real mode5-to-mode6 state transition, not fabricated retirement')
 clears=[t for t in timeline if t['kind']=='STORE'and num(t,'at')in(0x01060220,0x01060df0)]
 need(len(clears)==2 and [(num(t,'at'),num(t,'before'),num(t,'after'),num(t,'mask'),num(t,'pc'))for t in clears]==
  [(0x01060220,0x01034e90,0,65535,0xff841c80),(0x01060df0,0x010350a0,0,65535,0xff841c80)],
  'Both genuine lower-word actor-clear callbacks from original longword table clearer; high-word writes not invented')
 need(num(selected[5],'event')<num(clears[0],'event')<num(clears[1],'event')<num(selected[6],'event')and
  all(num(selected[6],k)==0 for k in('p1','p2')),'Whole actor pointers genuinely null after original table clear, not inferred from just low halves')
 late=[t for t in timeline if num(t,'event')>=num(selected[0],'event')]
 need(not any(t['kind']=='CODE'and num(t,'at')in(0xff804410,0xff804430,0xff8045d0,0xff8046b0)for t in late),
  'No old FIFO enqueue or native DMA drain between retirement entry and complete queue reset')
 before=[t for t in timeline if t['kind']=='CODE'and num(t,'at')==0xff804430 and num(t,'event')<num(selected[0],'event')]
 need(before and all(num(t,'p1')==0x01034e90 and num(t,'p2')==0x010350a0 for t in before),'All final old-body enqueue phase precedes actual both-actor retirement')
 post=next(t for t in timeline if t['kind']=='POST')
 pre=next(t for t in rows if t['kind']=='PRE'and num(t,'frame')==3209)
 need(all(num(t,k)==0 for t in(post,pre)for k in('p1','p2','b13'))and
  all(num(t,'b14')==0x0101f700 and num(t,'mode')==6 for t in(post,pre)),'No pending old packets or old actors survive to next genuine callback')
 return dict(actualLifecycleEvents=len(rows),observedFields=23,sourceBoundNativeCodeEvents=len(code),actualQueueResetCalls=len(resets),
  actualPendingQueueCancellation=cancellations[0],actualActorClearCallbacks=clears,originalMode6ResetChainObserved=True,
  retirementQueueDiscardMechanismSourceProven=True,oldActorQueuePacketsNeverDrainedAfterNativeReset=True,
  allKOContextsOrArenasAccepted=False,fullPortAcceptance=False)

def run():
 guest=current.expected();parent=json.loads(PARENT.read_text());observed=json.loads(OBSERVED.read_text());body=json.loads(BODY.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and parent['remaining']==scope.REMAINING and body['passed']and
  observed['passed']and observed['nativeExit']==0 and observed['originalWholePhysicalTrajectoryUnchanged']and
  observed['actualGuestMemoryProof']['sha256']==current.GUEST_SHA,'Actual unchanged current guest and physical lifecycle prerequisites')
 pins={str(p.resolve()):sha(p)for p in(PARENT,OBSERVED,BODY,Path(__file__),Path(scope.__file__))}
 for table in(parent['newInputHashes'],observed['inputHashes'],body['inputHashes']):
  for p,h in table.items():need(sha(p)==h,'Every retained native source/input/evidence stable: '+p);pins[p]=h
 stock=ROOT/'mk2/mk2-maincpu.bin';raw=stock.read_bytes();exe=ROOT/'mame-mkp/unidasm.exe'
 need(sha(exe)=='31E81DA741B36E2417C3304ABEFB0D924C9A1C588134573E53AC2FFDD61B8C36','Bound original native disassembler executable')
 pins[str(exe)]=sha(exe);pins[str(stock)]=sha(stock)
 windows=((0xff818e30,0xff818eb0),(0xff83f410,0xff83f520),(0xff808310,0xff808b30),(0xff804410,0xff8046e0),(0xff841c40,0xff841c90))
 asm={}
 for a,z in windows:
  lo,hi=(a-0xff800000)//8,(z-0xff800000)//8
  need(guest[lo:hi]==raw[lo:hi],'Entire relevant original mode/reset/queue/table-clear instruction window unchanged')
  result=subprocess.run([str(exe),str(stock),'-arch','tms34010','-basepc',f'{a:X}','-skip',str(lo),'-count',str(z-a),'-norawbytes'],capture_output=True,text=True,check=True,creationflags=subprocess.CREATE_NO_WINDOW)
  for line in result.stdout.splitlines():
   if re.match(r'^[0-9a-f]{8}:',line):address,text=line.split(':',1);asm[int(address,16)]=text.strip()
 expected={0xff818e30:'MOVI   6h,A0',0xff818e50:'MOVE   A0,@10601D0h,0',0xff818e80:'CALLA  FF83F410h',
  0xff83f410:'CALLR  FF83F4C0h',0xff83f4c0:'CALLA  FF808310h',0xff808420:'CALLA  FF841BE0h',
  0xff808450:'MOVI   FF808C50h,A1',0xff808480:'CALLA  FF841C40h',0xff841c40:'CLR    A0',
  0xff841c50:'MOVE   *A1+,A2,1',0xff841c70:'MOVE   A0,*A2,1',0xff808930:'MOVE   A1,@101F700h,1',
  0xff808a40:'CLR    B8',0xff808ad0:'MOVI   101F700h,A1',0xff808b00:'MOVE   A1,B14',
  0xff808b10:'CLR    B13',0xff808b20:'RETS',0xff804410:'MMTM   A1,A6,A8-A12',0xff804430:'INC    B13',
  0xff8045e0:'MOVE   -*B14,-*B10,1',0xff804630:'MOVE   -*B14,-*B10,1',0xff804640:'DSJS   B13,FF8046B0h'}
 need(all(asm.get(a)==text for a,text in expected.items()),'Independent original ISA disassembly proves mode/table-clear/enqueue/drain/reset semantics')
 # The original longword clear table contains actual P1/P2 actor slots.
 off=(0xff808c50-0xff800000)//8;table=[]
 for i in range(128):
  address=struct.unpack_from('<I',guest,off+i*4)[0]
  if not address:break
  table.append(address)
 need(len(table)<128 and 0x01060220 in table and 0x01060df0 in table,'Complete original terminated longword clear table contains both physical actor publications')
 log=(FOLDER/'run.log').read_text();rows=decode(log);case=check(rows,guest);faults=[]
 tests=[('wrong_reset_counter',lambda r:next(t for t in r if t['kind']=='CODE'and t.get('at')=='FF808B20'and t['mode']=='6').update(b13='00000001')),
  ('wrong_reset_pointer',lambda r:next(t for t in r if t['kind']=='CODE'and t.get('at')=='FF808B10'and t['mode']=='6').update(b14='0101F040')),
  ('missing_actor_clear',lambda r:r.remove(next(t for t in r if t['kind']=='STORE'and t.get('at')=='01060220'))),
  ('wrong_retire_opcode',lambda r:next(t for t in r if t['kind']=='CODE'and t.get('at')=='FF818E30').update(opcode='0000')),
  ('stale_next_field_actor',lambda r:next(t for t in r if t['kind']=='PRE'and t['frame']=='3209').update(p1='01034E90')),
  ('wrong_pending_cancellation',lambda r:next(t for t in r if t['kind']=='CODE'and t.get('at')=='FF808B00'and t['mode']=='6').update(b13='00000058'))]
 for label,mutate in tests:
  changed=copy.deepcopy(rows);mutate(changed);need(changed!=rows,'Effective actual lifecycle fault')
  try:check(changed,guest)
  except ValueError as error:faults.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Actual lifecycle fault accepted: '+label)
 for p in FOLDER.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All final authoritative source/evidence/public bytes stable')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=scope.REMAINING,
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification='progress: whole observed KO/rebuild body/source/shadow transition and15 actual-record faults accepted; three queued-but-undrawn parts retained as unproven lifecycle mechanism.',
  thisGoalTurnClassification='progress: fresh actual original physical run and full RAM guest bind native mode6/table actor clear/89-packet cancellation/pointer reset and next genuine callback; entire relevant original ISA code unchanged; six effective lifecycle faults rejected.',
  candidate=current.NAME,case=case,actualFaultsRejected=faults,inputHashes=pins,originalInstructionSemantics={f'{a:08X}':v for a,v in expected.items()},
  actualOriginalActorClearTable=table,observedBodySourceProof=str(BODY),previousWholeSceneProof=parent['parentAdditiveJournal'],
  originalWholePhysicalTrajectoryUnchanged=True,all8848ActualPhysicalRecordsEqual=True,
  threeQueuedOldBodyPartsCoveredByActualNativeQueueCancellation=body['case']['actualPreRetirementQueuedButNotDrawnBodyParts']==3,
  originalEntireQueueLifecycleWindowsUnchanged=True,newNativeBoots=1,newBuilds=0,newDeletedFiles=0,rawMediaFilesWritten=0,
  publicPlayableChanged=False,refreshedReleaseZIP=False,fullPortAcceptance=False,canonicalArtisticFidelityAccepted=False,
  nextAction='The observed Dead Pool KO/rebuild scene, body/source/shadow and original queue cancellation are now independently bound. Broaden naturally reached arena/CPU/overlap and KO contexts while retaining every original unfinished group; finish combined UI/names/audio regression, dependency-aware obsolete-folder cleanup and refreshed release ZIP.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable actual native queue lifecycle proof')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','remaining','originalInstructionSemantics','actualOriginalActorClearTable')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
