"""Independent original stock Pit movie shadow schedule, normal Cage DDD+HK.

Preserve the whole5917 cold RAM-only transport and actual terminal handling.
Do not claim RGB, PCM, port coverage or other victims from this stock control.
"""
import inspect,struct
import capture_stock_pit_shadow_inventory_v5917 as previous
from capture_stock_pit_shadow_inventory_v5917 import *
FOLDER=ROOT/'audit_v5922_original_stock_pit_cinematic_shadow'
OUT=ROOT/'audit_v5924_original_stock_pit_cinematic_shadow_checked'
LUA=ROOT/'mk2_stock_pit_cinematic_shadow_v5920.lua'
STOCK_PROOF=ROOT/'audit_v5919_original_stock_pit_shadow_inventory_checked/report.json'

def original_command(stock):
 off=lambda a:(a-0xff800000)//8
 need(struct.unpack_from('<I',stock,off(0xff862d20)+2*4)[0]==0xff868300,
      'Original Cage2 High Kick event table owns its real parser')
 need(struct.unpack_from('<13H',stock,off(0xff87b4e0))==(0x24,6,6,6,0,0,0,6,6,6,0,0,0),
      'Original Cage native newest-first D,D,D history in both facings, no recalled or port command')
 disasm=subprocess.run([str(ROOT/'mame-mkp/unidasm.exe'),str(STOCK),'-arch','tms34010','-basepc','0xff868300','-skip','0xd060','-count','224','-norawbytes'],capture_output=True,text=True,creationflags=subprocess.CREATE_NO_WINDOW)
 need(disasm.returncode==0 and not disasm.stderr and 'ff8683a0: MOVI   FF87B4E0h,A11'in disasm.stdout and
      'ff8683d0: JR     FF876D20h'in disasm.stdout,'Original character parser supplies exact original history to stage eligibility')
 return dict(originalOwnID=2,originalVictimID=3,eventTable='FF862D20',parser='FF868300',history='FF87B4E0',command='Down,Down,Down,High_Kick',sourceDisassembly=disasm.stdout)

def finish(text,stock,pins,code,initialized):
 original=original_command(stock)
 for path in (Path(previous.__file__),ROOT/'mk2_stock_pit_shadow_inventory_v5916.lua',STOCK_PROOF,ROOT/'mame-mkp/unidasm.exe'):
  pins[str(path)]=sha(path)
 prior=json.loads(STOCK_PROOF.read_text());need(prior['passed']and prior['originalGuestSHA256']==sha(STOCK),'Completed genuine ordinary stock Pit reference retained')
 matches=rows(text,'MK2_STAGE_MATCH');windows=rows(text,'MK2_STAGE_WINDOW');damage=rows(text,'MK2_STAGE_DAMAGE')
 begin=rows(text,'MK2_STOCK_CINE_BEGIN');complete=rows(text,'MK2_STOCK_CINE_COMPLETE');stop=rows(text,'MK2_STOCK_CINE_STOP')
 need(len(matches)==len(windows)==7 and len(begin)==len(complete)==len(stop)==1 and stop[0]['completed']=='true'and complete[0]['age']=='1100',
      'Original stock naturally earns all seven matches and completes its actual full Pit window')
 need([int(r['arena'])for r in matches]==list(range(7))and all(r['ids']=='2,3'for r in matches),'Original identities and normal arena rotation')
 for index in range(1,8):
  ds=[r for r in damage if int(r['match'])==index]
  expected=161;kos=0
  for r in ds:
   need(int(r['before'])==expected and 0<=int(r['after'])<expected and r['pc']=='FF836700'and r['writes']=='0'and r['assistance']=='none',
        'Every original collision store follows the complete unassisted full-health chain')
   expected=int(r['after'])
   if expected==0:kos+=1;expected=161
  need(kos==2 and sum(int(r['before'])-int(r['after'])for r in ds)==322,'Two genuine full-health rounds in every stock match')
 b=begin[0];need(b['pc']=='FF8BDDF0'and b['id']=='2'and b['arena']=='6','Actual original Cage owns native Pit stage entry')
 entries=rows(text,'MK2_STAGE_ENTRY');gate=[r for r in entries if int(r['match'])==7 and r['entry'].startswith('FF877')or int(r['match'])==7 and r['entry'].startswith('FF876')]
 wanted=['FF876D20','FF876E50','FF876E80','FF876F40','FF877000','FF877120','FF8771F0','FF877270','FF877280','FF877300','FF877350','FF8773A0','FF877420']
 need([r['entry']for r in gate]==wanted and all(r['id']=='2'and r['a8']==b['actor']and r['a13']==b['main']for r in gate),
      'Complete actual original history/range/finish/opponent/action gate chain, true owned Cage')
 need(gate[0]['a11']=='FF87B4E0','Actual original controller uses independently verified Cage history row')
 command=rows(text,'MK2_STAGE_COMMAND');inputs=rows(text,'MK2_STAGE_INPUT')
 need(len(command)==1 and command[0]['arena']=='6'and int(command[0]['gap'])<=65,'Natural original stage command at proper proximity')
 c=int(command[0]['frame'])
 required=[('Down',10),('Down',20),('Down',30),('High_Kick',40)]
 need(all(any(r['button']==button and r['slot']=='1'and int(r['frame'])==c+age for r in inputs)for button,age in required),
      'Every original physical D,D,D+HK event is present, no injected action')
 fields=rows(text,'MK2_STOCK_CINE_FIELD');origin=int(b['frame'])
 need([int(r['frame'])for r in fields]==list(range(origin,origin+1101))and [int(r['age'])for r in fields]==list(range(1101)),
      'Every completed original Pit field through1100, no window omission')
 movie=[r for r in fields if r['mode']=='9'];draws=rows(text,'MK2_STOCK_CINE_DRAW');construct=rows(text,'MK2_STOCK_CINE_CONSTRUCTOR')
 need(movie and draws and len(construct)==1 and len({r['actor']for r in draws})==len({r['main']for r in draws})==1 and
      all(r['actor']==r['owner']and r['id']=='3'and int(r['body'],16)&16==0 for r in draws),
      'Actual original Baraka3 cinematic actor is Main+140-owned with native no-shadow body flag')
 need(construct[0]['a11']in {r['p2']for r in fields if r['p2']!='00000000'},'Native original constructor retains real physical victim ancestry')
 need(min(int(r['victim_y'])for r in fields if r['p2']!='00000000')<-100 and any(r['p1']==r['p2']=='00000000'for r in fields),
      'Original physical launch and native physical pointer retirement actually occur')
 next_fields=[r for r in fields if r['mode']=='3'and int(r['frame'])>int(movie[-1]['frame'])]
 need(next_fields and not rows(text,'MK2_STOCK_CINE_DEADLINE'),'Native next-screen transition, never deadline success')
 need(all(int(r['shadow_enable'],16)==int(r['entries'])==int(r['copies'])==int(r['mode8'])==0 for r in fields)and
      not rows(text,'MK2_STOCK_CINE_SHADOW_ENTRY')and not rows(text,'MK2_STOCK_CINE_MODE8'),
      'Every original physical/launch/movie/next-screen field suppresses native shadow globally and issues no shadow copy')
 for r in rows(text,'MK2_STOCK_CINE_ENABLE_STORE'):
  need(r['at']=='0105EBC0'and int(r['before'],16)==int(r['value'],16)==0 and r['mask']=='FFFF','No original cinematic store enables physical shadows')
 guest=current.expected();off=lambda a:(a-0xff800000)//8
 for lo,hi in ((0xff8046e0,0xff804990),(0xff80a810,0xff80ab60),(0xff801000,0xff8017b0)):
  need(guest[off(lo):off(hi)]==stock[off(lo):off(hi)],'Entire original global-enable dispatcher and actual shadow kernel unchanged in current port')
 need(all(sha(p)==h for p,h in pins.items()),'All genuine stock/current/public/prior source bytes unchanged')
 parent=json.loads(PARENT.read_text())
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
  parentAdditiveJournal=str(PARENT),originalDriver='mk2',originalGuestSHA256=initialized,sourceNativeCommand=original,
  genuineFullHealthMatches=7,genuineCollisionDamage=2254,nativeExitCode=code,completedFields=len(fields),
  originalStageAction=begin[0],originalMovieFirstFrame=int(movie[0]['frame']),originalMovieLastFrame=int(movie[-1]['frame']),
  originalNextScreenFrame=int(next_fields[0]['frame']),originalMovieDraws=len(draws),
  originalMovieActor=draws[0]['actor'],originalMovieMain=draws[0]['main'],originalMovieBody=draws[0]['body'],
  originalGlobalShadowEnable=0,originalNativeShadowEntries=0,originalNativeShadowCopies=0,originalAllMode8Copies=0,
  originalPitCinematicShadowScheduleObserved=True,currentPortShadowPolicyAccepted=False,completeNativePitSceneAccepted=False,
  stockRGBOrAudioAccepted=False,fullPortAcceptance=False,inputHashes=pins,newNativeBoots=1,newBuilds=0,requestedRawFilesWritten=0,publicPlayableChanged=False)

# Full prior native cold process, stdout draining, guest byte comparison and
# terminal/error handling remain unchanged. Only preflight and post-gates differ.
source=inspect.getsource(previous.run)
start=source.index(" matches=rows(text,'MK2_STAGE_MATCH')")
source=source[:start]+" return finish(text,stock,pins,code,initialized)\n"
old="need('if false then -- Ordinary-arena inventory, never send port stage commands.'in script and"
need(source.count(old)==1,'Exact ordinary-only preflight replaced by native original stage-command preflight')
source=source.replace(old,"need('whole806_stock_Cage2_Baraka3_native_DDD_HK_no_snapshots'in script and",1)
old="all(s not in script for s in ('write_u','write_i','cpu.PC.value=','loadstate','save_state'))"
need(source.count(old)==1,'One pre-native write detector, comparison is not register assignment')
source=source.replace(old,"not re.search(r'write_u|write_i|cpu\\.PC\\.value\\s*=(?!=)|loadstate|save_state',script)",1)
before=" script=LUA.read_text();driver=(ROOT/'mk2ks_native_stage_performer_v806.lua').read_text()"
need(source.count(before)==1,'Whole cold transport preflight and all original inputs retained')
source=source.replace(before,before+"\n original_command(STOCK.read_bytes())\n need(json.loads(STOCK_PROOF.read_text())['passed'],'Completed ordinary reference before cinematic boot')",1)
scope=dict(globals(),__file__=__file__,finish=finish,original_command=original_command)
exec(compile(source,__file__+'::entire5917_cold_capture_original_cinematic_post_gate','exec'),scope)
run=scope['run'];run.source=source

if __name__=='__main__':
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'report.json',report)
 if FOLDER.exists():save(FOLDER/'result.json',report)
 for p in [Path(__file__),LUA,*FOLDER.rglob('*'),*OUT.rglob('*')]:
  if p.is_file()and p.suffix.lower()in('.py','.lua','.json','.cfg','.log'):
   before=sha(p);done=subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)],capture_output=True)
   need(done.returncode==0 and sha(p)==before,'Lossless bounded sealed stock evidence')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','remaining','sourceNativeCommand')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
