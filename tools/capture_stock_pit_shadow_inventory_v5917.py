"""Bounded original-game Pit shadow inventory, whole guest in RAM only.

Earn six full-health two-round matches via normal physical controls. This is
an original mk2 reference, never a port-character proxy or full-scene proof.
"""
import datetime,gzip,hashlib,json,os,re,subprocess,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5915_current_cross_pit_movie_ground_progress/progress.json'
FOLDER=ROOT/'audit_v5918_original_stock_pit_shadow_inventory'
OUT=ROOT/'audit_v5919_original_stock_pit_shadow_inventory_checked'
LUA=ROOT/'mk2_stock_pit_shadow_inventory_v5916.lua'
EXE=ROOT/current.NAME/'mkport_candidate.exe'
STOCK=ROOT/'mk2/mk2-maincpu.bin'

def save(path,value):Path(path).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def rows(text,tag):return [dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith(tag+' ')]
def run():
 need(not FOLDER.exists()and not OUT.exists(),'Fresh immutable stock reference')
 current.expected()
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Full original scope preserved')
 paths=[PARENT,Path(__file__),LUA,STOCK,EXE,ROOT/'mk2ks_native_stage_performer_v806.lua',Path(current.__file__),
        ROOT/'mk2_stock_baraka_audio_native_tables_v5606.lua',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',
        ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip']
 pins={str(p):sha(p)for p in paths}
 need(sha(STOCK)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'and sha(EXE)==current.EXE_SHA,'Original stock guest, current compiled binary')
 script=LUA.read_text();driver=(ROOT/'mk2ks_native_stage_performer_v806.lua').read_text()
 need('if false then -- Ordinary-arena inventory, never send port stage commands.'in script and
      all(s not in script for s in ('write_u','write_i','cpu.PC.value=','loadstate','save_state')),'Passive observer and ordinary physical original controls')
 # Exact original kernel independent of imported descriptors or presentation filtering.
 stock=STOCK.read_bytes();guest=current.expected();lo=(0xff801070-0xff800000)//8;hi=(0xff8017a0-0xff800000)//8
 need(stock[lo:hi]==guest[lo:hi],'Whole original native shadow kernel retained by current port')
 FOLDER.mkdir();(FOLDER/'cfg').mkdir();(FOLDER/'nvram').mkdir();(FOLDER/'snap').mkdir()
 save(FOLDER/'input_hashes_before.json',pins)
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_PORT_ROOT=str(ROOT),MK2KS_STAGE_WINNER='cage',MK2KS_STAGE_SIDE='1',MK2KS_STAGE_ARENA='6',MK2KS_STAGE_CASE='positive')
 command=[str(EXE),'mk2','-rompath',str(ROOT/'roms'),'-nosamples','-skip_gameinfo','-nocheat','-inipath',str(FOLDER),
  '-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','900',
  '-cfg_directory',str(FOLDER/'cfg'),'-nvram_directory',str(FOLDER/'nvram'),'-snapshot_directory',str(FOLDER/'snap'),'-autoboot_script',str(LUA)]
 initialized=None;errors=[]
 with(FOLDER/'stderr.log').open('w',encoding='utf-8')as err,gzip.open(FOLDER/'run.log.gz','wt',encoding='utf-8')as out:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(FOLDER/'process.json',dict(pid=proc.pid,hostPID=os.getpid(),command=command,startedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),environment={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print('Genuine stock Cage2/Baraka3 ordinary-Pit reference native PID='+str(proc.pid),flush=True)
  for line in proc.stdout:
   if line.startswith('MK2_STOCK_PIT_GUEST '):
    try:
     r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r['hex'])
     need(initialized is None and len(raw)==int(r['bytes'])==1048576 and raw==stock,'Every initialized stock guest byte equals original ROM')
     initialized=hashlib.sha256(raw).hexdigest().upper();out.write('MK2_STOCK_PIT_GUEST_DIGEST bytes=1048576 sha256='+initialized+'\n')
    except Exception as error:errors.append(repr(error));out.write('MK2_STOCK_PIT_TRANSPORT_ERROR '+repr(error)+'\n')
   else:
    need('hex='not in line,'No unknown raw buffer sink');out.write(line)
  code=proc.wait()
 save(FOLDER/'terminal.json',dict(pid=proc.pid,exit_code=code,completedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 print('Stock native terminal exit='+str(code),flush=True)
 with gzip.open(FOLDER/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 need(code==0 and not(FOLDER/'stderr.log').read_text()and not errors and initialized==sha(STOCK),'Actual clean original terminal and complete source transport')
 matches=rows(text,'MK2_STAGE_MATCH');windows=rows(text,'MK2_STAGE_WINDOW');damage=rows(text,'MK2_STAGE_DAMAGE')
 complete=rows(text,'MK2_STOCK_PIT_COMPLETE');stop=rows(text,'MK2_STOCK_PIT_STOP');start=rows(text,'MK2_STOCK_PIT_PIT_START')
 need(len(matches)==7 and len(windows)==6 and len(start)==len(complete)==len(stop)==1 and
      stop[0]['completed']=='true'and complete[0]['age']=='300'and complete[0]['arena']=='6','Genuinely reach and complete seventh Pit ordinary inventory')
 need([int(r['arena'])for r in matches]==list(range(7))and all(r['ids']=='2,3'for r in matches),'Original true Cage/Baraka IDs and normal seven-arena rotation')
 for index in range(1,7):
  ds=[r for r in damage if int(r['match'])==index]
  need(sum(int(r['before'])-int(r['after'])for r in ds)==322 and sum(r['after']=='0'for r in ds)==2 and
       all(r['writes']=='0'and r['assistance']=='none'and int(r['before'])<=161 and int(r['after'])<int(r['before'])for r in ds),'Every prior stock match earns both full-health rounds without assistance')
 need(not rows(text,'MK2_STAGE_COMMAND')and not rows(text,'MK2_STOCK_PIT_DEADLINE'),'No port-command attempt or deadline acceptance')
 fields=rows(text,'MK2_STOCK_PIT_FIELD');summary=[]
 for arena in range(7):
  subset=[r for r in fields if int(r['arena'])==arena]
  need(subset and {int(r['slot'])for r in subset}=={0,1,2},'Full stock field and unowned DMA inventory in every earned arena')
  for slot in (0,1,2):
   rs=[r for r in subset if int(r['slot'])==slot]
   if slot:need(all(r['actor']==r['owner']and int(r['id'])==(2 if slot==1 else 3)for r in rs),'Actual physical ownership and stock identity')
   summary.append(dict(arena=arena,slot=slot,fields=len(rs),eligibleFields=sum(int(r['body'],16)&16!=0 for r in rs),
    entries=sum(int(r['entries'])for r in rs),components=sum(int(r['components'])for r in rs),copies=sum(int(r['copies'])for r in rs),allMode8=sum(int(r['mode8'])for r in rs)))
 need(all(sha(p)==h for p,h in pins.items()),'All current/public/stock/source and prior proofs unchanged')
 current.expected()
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
  previousGoalTurnClassification='no progress: user acknowledgement only; revalidated authoritative5915 evidence and took fresh original stock control',
  thisGoalTurnClassification='progress: independent original mk2 physically earned seven-arena ordinary shadow execution inventory',parentAdditiveJournal=str(PARENT),
  originalDriver='mk2',originalGuestSHA256=initialized,physicalMatches=matches,completedPitWindow=complete[0],shadowExecutionByArena=summary,
  nativeExitCode=code,inputHashes=pins,newNativeBoots=1,newBuilds=0,requestedRawFilesWritten=0,publicPlayableChanged=False,
  originalPitCinematicShadowPolicyAccepted=False,wholeNativePitShadowPolicyAccepted=False,completeNativePitSceneAccepted=False,fullPortAcceptance=False,
  next='Use actual original ordinary Pit execution and unchanged native dispatcher source to resolve stage shadow scheduling; separately qualify cinematic suppression, retain all full goal groups and final matching ZIP.')

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'report.json',report)
 if FOLDER.exists():save(FOLDER/'result.json',report)
 for p in [Path(__file__),LUA,*FOLDER.rglob('*'),*OUT.rglob('*')]:
  if p.is_file()and p.suffix.lower()in('.py','.lua','.json','.cfg','.log'):
   before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
   need(done.returncode==0 and sha(p)==before,'Sealed bounded evidence compression preserves bytes')
 print(json.dumps({k:report[k]for k in('passed','error','shadowExecutionByArena')if k in report},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
