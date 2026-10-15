"""Fresh current physical Babality matrix; original native semantics and ROM art.

No actor/ID/health/stage writes, proxy, savestate, new build or public promotion.
Original controllers and semantic checks unchanged; guest/display remain RAM.
Old capture folders are not restored or treated as current runtime evidence.
"""
import concurrent.futures,copy,datetime,hashlib,json,os,re,struct,subprocess,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import verify_native_babality_performers_v739 as model
import build_original_babality_reference_v1 as original_reference
import upgrade_ksui_previews as ui
import verify_move_phase_shadow_v5089 as graphics

ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v5445_current_ui_visual_progress/progress.json'
BASE=ROOT/'audit_v5447_current_babality_ram'
OUT=ROOT/'audit_v5448_current_babality_progress'
LUA=ROOT/'mk2ks_current_babality_ram_v5446.lua'
ORIGINAL=ROOT/'mk2ks_native_babality_performer_probe_v738.lua'
COMPLETED=[]
SPECS=[(w,v,s,c)for w,v in(('kano','sonya'),('sonya','kano'))for s in(1,2)
       for c in('positive','wrong_direction','punch_used')]
SPECS += [('kitana',v,s,'positive')for v in('liu_kang','kano','sonya')for s in(1,2)]
SPECS += [(w,w,s,'positive')for w in('kano','sonya')for s in(1,2)]

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def digest(raw):return hashlib.sha256(raw).hexdigest().upper()
def off(address):return (address-0xff800000)//8

def reference(guest,pins):
 donor_path=ROOT/'mk3/mk3-maincpu.bin';stock_path=ROOT/'mk2/mk2-maincpu.bin'
 donor=donor_path.read_bytes();stock=stock_path.read_bytes()
 for path in(donor_path,stock_path):pins[str(path)]=sha(path)
 need(len(donor)==len(stock)==len(guest)==0x100000,'Whole independent original and current guests')
 instructions=donor[off(0xffa2a350):off(0xffa2a3f0)]
 need(instructions==struct.pack('<10H',0xb505,0x01f0,0x24a5,0x0b25,0xa5b0,0xffa2,0x86a5,0x0d5f,0xca80,0xff95),
      'Original true-ID baby dispatch and single-frame constructor')
 gfx=ui.load_gfx(ROOT/'mk3')
 for _,chips in ui.GFX_BANKS:
  for chip in chips:
   path=ROOT/'mk3'/f'l1_mortal_kombat_3_u{chip}_game_rom.u{chip}';pins[str(path)]=sha(path)
 stock_gfx=graphics.reconstruct(pins)
 report=dict(source='original_mk3_2_1_and_original_mk2',records={},victim_dispatch_instructions=instructions.hex())
 sprites={}
 need(guest[0xf9600:0xf9600+68]==stock[off(0xff87f020):off(0xff87f020)+68],
      'All seventeen original victim table rows preserved')
 need(struct.unpack_from('<I',guest,off(0xff87eb30))[0]==model.v.TABLE,'Actual native victim table operand')
 need(guest[0xf97a0:0xf97a0+68]==stock[off(0xff87e3a0):off(0xff87e3a0)+68] and
      struct.unpack_from('<I',guest,off(0xff87e250))[0]==0xff800000+0xf97a0*8,
      'All original performer commands preserved and real extended native consumer')
 for index,name in enumerate(('kano','sonya','liu_kang')):
  own=name!='liu_kang';program=donor if own else stock
  frame=original_reference.FRAMES[name]if own else 0xffb1c960
  if own:need(struct.unpack_from('<I',donor,off(original_reference.TABLE)+index*4)[0]==frame,'Original actual own baby dispatch')
  raw=program[off(frame):off(frame)+18]
  width,height,dx,dy,source,command,palette=struct.unpack('<HHhhIHI',raw)
  need((width,height)==({'kano':(27,44),'sonya':(35,54),'liu_kang':(30,47)}[name])and dx==dy==0 and command&0x80,
       'Original bounded native baby geometry and compressed source')
  count=struct.unpack_from('<H',program,off(palette))[0];need(1<count<=32,'Original baby palette bounds')
  palette_raw=program[off(palette):off(palette)+2+count*2]
  words=struct.unpack_from(f'<{count}H',palette_raw,2)
  colors=[(0,0,0,0)]+[(*ui.xrgb555(word),255)for word in words[1:]]
  colors += [(0,0,0,0)]*(256-len(colors))
  sprite=np.asarray(ui.decode_component(gfx if own else stock_gfx,colors,source,command,width,height))
  expected=bytearray(raw)
  pointer=model.v.FRAMES[name]if own else frame
  if own:
   struct.pack_into('<I',expected,8,source+0x10000000)
   struct.pack_into('<I',expected,14,0xff800000+model.v.PALETTES[name]*8)
   need(guest[model.v.PALETTES[name]:model.v.PALETTES[name]+len(palette_raw)]==palette_raw,'Original own baby palette copied exactly')
  else:need(guest[off(palette):off(palette)+len(palette_raw)]==palette_raw,'Original stock baby palette preserved')
  need(guest[off(pointer):off(pointer)+18]==expected and
       struct.unpack_from('<I',guest,0xf9600+model.v.IDS[name]*4)[0]==pointer,'Exact original true-ID baby frame, native format and dispatch')
  report['records'][name]=dict(original_id=index if own else 1,frame=frame,descriptor_hex=raw.hex(),width=width,height=height,
    source_bits=source,command=command,palette_pointer=palette,palette_count=count,palette_hex=palette_raw.hex(),rgba_sha256=digest(sprite.tobytes()).lower())
  sprites[name]=sprite
  if own:
   record=0xff986470 if name=='kano'else 0xff98aa80
   need(struct.unpack_from('<IIHII',donor,off(record))==(0x20000,0x200000,7,0xff993660,0xff97f390),'Actual original LK command record')
   history=struct.unpack_from('<13H',donor,off(record)+18);need(history==model.HISTORIES[index],'Original character-owned history')
   native=tuple(value-1 if word and value else value for word,value in enumerate(history));destination=0xf97f0+index*0x20
   need(struct.unpack_from('<13H',guest,destination)==native and
        struct.unpack_from('<I',guest,0xf97a0+(17+index)*4)[0]==0xff800000+destination*8,'Real own native Babality command encoding')
   parser=0xf9840+index*0x20;fallback=0xff800000+0xf5440*8 if name=='kano'else 0xff80de20
   need(struct.unpack_from('<6H',guest,parser)==(0x0d5f,0xe120,0xff87,0xc080,fallback&65535,fallback>>16) and
        struct.unpack_from('<I',guest,0xff2c0+(17+index)*4)[0]==0xff800000+parser*8,'Final actual LK parser Babality/fallback binding')
 return report,sprites

def runtime(rows,spec,ref):
 winner,victim,side,command=spec
 if command=='positive':
  model.v.runtime_check(rows,victim,side,ref,winner_id=model.WINNERS[winner]);model.command_check(rows,winner,side,command)
  for r in model.v.entries(rows,'FIELD'):
   if int(r['slot'])==side:
    need(int(r['id'])==int(r['roster'])==model.WINNERS[winner]and r['actor']==r['owner'],'Every observed winner field retains true own identity and native owner')
  for age in(160,200,240):
   samples=[r for r in model.v.entries(rows,'BABY')if int(r['age'])==age];need(len(samples)==1,'Actual baby source sample every required native age')
   r=samples[0];rec=ref['records'][victim]
   need((int(r['width']),int(r['height']))==(rec['width'],rec['height'])and int(r['y'])+rec['height']==216,'Native source geometry and common floor including stock control')
   wanted=list(struct.unpack_from(f"<{rec['palette_count']}H",bytes.fromhex(rec['palette_hex']),2))
   need([int(v,16)for v in r['colors'].split(',')][:len(wanted)]==wanted,'Actual source-exact stock/imported baby palette')
 else:model.negative_check(rows,winner,victim,side,command)
 damage=model.v.entries(rows,'DAMAGE');health=161;kos=0
 for r in damage:
  need(int(r['before'])==health and 0<=int(r['after'])<health and r['pc']=='FF836700','Continuous native collision health ledger, no missing or fabricated damage')
  health=int(r['after'])
  if health==0:kos+=1;health=161
 need(kos==2,'Two earned ordinary knockouts')

def pixel_checks(rows,images,spec,ref,sprites):
 winner,victim,side,command=spec;results=[]
 need(set(images)=={'selection_p1.png','selection_p2.png','finish_window.png'}|{f'babality_{age}.png'for age in range(0,721,8)},
      'All91 native finish/transition snapshots and both selections transported, no skipped targets')
 if command!='positive':return results
 for age in(160,200,240):
  (x,y),pixels=model.v.image_match(images[f'babality_{age}.png'],sprites[victim])
  r=next(r for r in model.v.entries(rows,'BABY')if int(r['age'])==age)
  need(y==int(r['y'])and y+ref['records'][victim]['height']==216,'Actual displayed baby anchored on native floor')
  results.append(dict(age=age,origin=[x,y],exactOpaqueSourcePixels=pixels))
 return results

def faults(rows,images,spec,ref,sprites):
 runtime(rows,spec,ref);pixel_checks(rows,images,spec,ref,sprites)
 winner,victim,side,command=spec;accepted=[]
 def reject(label,fn):
  try:fn()
  except ValueError as error:accepted.append(dict(label=label,rejectedBy=str(error)))
  else:raise ValueError('Actual-record/RAM-pixel counterexample accepted: '+label)
 changes=[('unearned rounds','RESULT','wins','1',lambda r:True),('assistance','RESULT','writes','1',lambda r:True),
  ('proxy selected winner','SELECT_ID','actual','1',lambda r:int(r['slot'])==side),
  ('non-native collision','DAMAGE','pc','FF80DE20',lambda r:True)]
 if command=='positive':
  changes += [('wrong baby ID','CONSTRUCT','victim_id','0',lambda r:True),
   ('wrong lookup','LOOKUP','value','FFFF',lambda r:True),
   ('wrong physical winner','FIELD','owner','01000000',lambda r:r['age']=='0'and int(r['slot'])==side),
   ('wrong floor','BABY','y',str(217-ref['records'][victim]['height']),lambda r:r['age']=='160'),
   ('wrong native palette','BABY','colors','FFFF,'+','.join(model.v.entries(rows,'BABY')[0]['colors'].split(',')[1:]),lambda r:r['age']=='160'),
   ('wrong native activation','RESULT','action',str(int(model.v.entries(rows,'RESULT')[0]['action'])+1),lambda r:True)]
 else:changes += [('rejected command activated','RESULT','action','1',lambda r:True)]
 for label,tag,key,value,predicate in changes:
  changed=copy.deepcopy(rows);target=next(r for t,r in changed if t==tag and predicate(r));need(target[key]!=value,'Effective actual record counterexample');target[key]=value
  reject(label,lambda changed=changed:runtime(changed,spec,ref))
 if command=='positive':
  for label,tag,predicate in(('missing owned action','ENTRY',lambda r:r['entry']=='FF87E520'),
    ('missing native retirement','RETIRE',lambda r:r['entry']=='01060230'),('missing baby reuse','BABY_REUSED',lambda r:True)):
   changed=[(t,r)for t,r in rows if not(t==tag and predicate(r))];need(len(changed)<len(rows),'Effective deletion fault')
   reject(label,lambda changed=changed:runtime(changed,spec,ref))
  actual=images['babality_160.png'];(x,y),_=model.v.image_match(actual,sprites[victim])
  yy,xx=np.argwhere(sprites[victim][:,:,3]!=0)[0];changed=actual.copy();changed[y+yy,x+xx,0]^=1
  reject('one actual displayed source pixel corrupted',lambda:model.v.image_match(changed,sprites[victim]))
 return accepted

def capture(spec,guest,pins,ref,sprites):
 winner,victim,side,command_case=spec;key=f'{winner}_vs_{victim}_p{side}_{command_case}';folder=BASE/key
 need(not folder.exists(),'Fresh immutable native context');folder.mkdir(parents=True)
 for name in('cfg','nvram','snap'):(folder/name).mkdir()
 save(folder/'input_hashes_before.json',pins)
 env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
 env.update(MK2KS_BABY_WINNER=winner,MK2KS_BABY_VICTIM=victim,MK2KS_BABY_WINNER_SIDE=str(side),MK2KS_BABY_CASE=command_case)
 build=ROOT/current.NAME
 command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),
  '-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none',
  '-noautoframeskip','-frameskip','0','-nothrottle','-str','180','-snapsize','400x254','-cfg_directory',str(folder/'cfg'),
  '-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
 images={};headers=[];guest_seen=False
 with(folder/'stderr.log').open('w',encoding='utf-8')as err:
  proc=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
  save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
  print(key+' actual native PID='+str(proc.pid),flush=True)
  with(folder/'run.log').open('w',encoding='utf-8')as out:
   for line in proc.stdout:
    if line.startswith(('MK2_BRAM_GUEST ','MK2_BRAM_RGB ')):
     tag=line.split()[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
     need(len(raw)==int(r['bytes']),'Entire actual native RAM transport');r['sha256']=digest(raw)
     if tag=='MK2_BRAM_GUEST':
      need(not guest_seen and r['frame']=='1'and raw==guest,'Entire actual initialized current guest source-exact');guest_seen=True
     else:
      need((r['width'],r['height'],len(raw))==('400','254',406400),'Whole actual displayed400x254 native raster')
      need(r['filename']not in images,'No duplicated native snapshot target');images[r['filename']]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy();headers.append(r)
     out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n')
    else:need('hex='not in line,'No raw capture persisted');out.write(line)
   code=proc.wait()
 log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
 need(code==0 and guest_seen and not error and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),'Native warning-free terminal0 and whole current guest')
 rows=model.v.records(log);runtime(rows,spec,ref);pixels=pixel_checks(rows,images,spec,ref,sprites);qualification=faults(rows,images,spec,ref,sprites)
 result=dict(passed=True,candidate=current.NAME,winner=winner,victim=victim,side=side,command=command_case,nativePID=proc.pid,nativeExit=code,
  assistance='none',guestWrites=0,cheatsEnabled=False,wholeActualCurrentGuestSourceExact=True,nativeResult=model.v.entries(rows,'RESULT')[0],
  actualDisplayHeaders=headers,originalNativeRuntimeAndCommandModelAccepted=True,originalBabyArtPaletteFloorChecks=pixels,
  effectiveActualRecordAndRAMPixelFaults=qualification,fullPortAcceptance=False,audioAccepted=False,wholeSceneRasterAccepted=False,inputHashes=pins)
 save(folder/'result.json',result)
 cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True,text=True)
 need(cp.returncode==0,'Lossless retained small native text trace compression')
 COMPLETED.append(result);print(key+' native command/identity/retirement and exact baby art accepted',flush=True)
 return result

def run():
 guest=current.expected();parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Current combined UI/audio authoritative checkpoint')
 pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
 for path in(LUA,ORIGINAL,Path(__file__).resolve(),Path(current.__file__).resolve(),Path(model.__file__).resolve(),Path(model.v.__file__).resolve(),
  Path(original_reference.__file__).resolve(),Path(ui.__file__).resolve(),Path(graphics.__file__).resolve()):pins[str(path)]=sha(path)
 original=ORIGINAL.read_text();need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|dofile\(',original),'Original standalone physical controller read-only')
 ref,sprites=reference(guest,pins)
 need(all(sha(p)==h for p,h in pins.items()),'Current compiled/source/public/evidence inputs stable before capture')
 first=capture(SPECS[0],guest,pins,ref,sprites)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=[first]+list(pool.map(lambda spec:capture(spec,guest,pins,ref,sprites),SPECS[1:]))
 need(len(cases)==22,'Complete both-slot perform/victim/mirror/rejection and stock-control matrix')
 for p in BASE.rglob('*'):
  if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'No guest/raster/audio media persisted');pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every authoritative input/public byte unchanged after actual matrix')
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
  parentAdditiveJournal=str(PARENT),previousGoalTurnClassification='progress: current combined UI/name-audio and exact native visual backing; intervening thanks acknowledgement made no changes',
  thisGoalTurnClassification='progress: actual current22-context physical Babality performers/victims/mirrors and both-slot rejection/stock controls; source-ROM baby art, palette, floor and native retirement; effective actual-record/RAM-pixel faults',
  cases=cases,independentOriginalROMBabyReference=ref,newNativeBoots=22,newBuilds=0,newDeletedFiles=0,rawGuestRGBPCMOrWAVFilesWritten=0,
  currentBabalityMatrixAccepted=True,newInputHashes=pins,publicPlayableChanged=False,refreshedReleaseZIP=False,
  allFinisherContextsAccepted=False,allArenasAccepted=False,audioAccepted=False,wholeSceneRasterAccepted=False,fullPortAcceptance=False,
  nextAction='Continue actual current remaining finishers/victims/branches, arena/CPU/overlap and complete audio; preserve every original remaining group and promote release only after required combined acceptance.')

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable Babality progress checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();save(OUT/'progress.json',report)
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentOriginalROMBabyReference')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
