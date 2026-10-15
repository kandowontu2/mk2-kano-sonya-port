"""Real current3836 Scorpion second-fatality activation/victim state.

Two stock controls plus true17/18 in both slots. Unchanged original physical
inputs, entire current guest bytes, actual collision KOs, native HP release,
instruction-qualified cooperative callbacks and complete physical state.
RGB is transported only in RAM and digested, NOT called art/floor/audio proof.
No old/retired captures are loaded or recreated; no EXE/ROM/raw-media writes.
"""
import concurrent.futures,hashlib,json,os,re,shutil,subprocess,traceback
from pathlib import Path
import check_scorpion_secondary_source_v4535 as source
ROOT,need,sha,NAME=source.ROOT,source.need,source.sha,source.NAME
OUT=ROOT/'audit_v4539_current_scorpion_secondary_state_observed'
CASES=(('kitana',1),('liu_kang',2),('kano',1),('kano',2),('sonya',1),('sonya',2))

def rows(text,prefix,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith(prefix+tag+' ')]

def contract(text,fighter,side):
    identity={'kano':17,'sonya':18,'kitana':4,'liu_kang':1}[fighter];winner=3-side
    native=lambda tag:rows(text,'MK2_SSECOND_',tag)
    original=lambda tag:rows(text,'MK2_STOCK_HEAD_V921_',tag)
    begin,complete,terminal=native('BEGIN'),native('COMPLETE'),native('RESULT')
    need(len(begin)==len(complete)==len(terminal)==1,'Exactly one actual instruction-qualified native activation/completion/terminal')
    b,c,t=begin[0],complete[0],terminal[0];start=int(b['frame'])
    need(b['entry']=='FF8BBFE0'and b['pc']=='FF8BBFF0'and b['winner_id']=='10'and b['victim_id']==str(identity)and
      b['victim_slot']==str(side)and b['winner_slot']==str(winner)and b['mode']=='2',
      'Real Scorpion10 second fatality and true physical victim, not a data read/proxy/action assignment')
    need(c['entry']=='FF8CDC40'and c['pc']=='FF8CDC50'and c['age']=='96'and c['actor']==b['actor']and c['main']==b['main']and
      int(c['frame'])==start+96 and int(t['origin'])==start and int(t['completed'])==start+96,
      'Original full96-field cooperative completion and actual owned actor/Main')
    action,ready,live=original('ACTION'),original('READY'),original('FIRST_LIVE')
    need(len(action)==len(ready)==len(live)==1 and action[0]['frame']==b['frame']and action[0]['address']=='FF8BBFE0'and
      action[0]['variant']=='2'and action[0]['damage']=='322'and live[0]['ids']==f'10,{identity}'and
      action[0]['actor']==b['actor']and action[0]['main']==b['main']and action[0]['victim_actor']==b['victim_actor']and
      action[0]['victim_main']==b['victim_main'],'Whole unchanged original controller events match genuine source instruction activation')
    hp=161;damage=0;killed=0;collisions=[]
    for r in original('HEALTH'):
        if r['pc']!='FF836700'or int(r['frame'])>start:continue
        before,after=int(r['before']),int(r['after']);need(before==hp and 0<=after<before<=161,'Entire actual native collision damage chain')
        hp=after;damage+=before-after;collisions.append(r)
        if hp==0:killed+=1;hp=161
    need(len(collisions)==10 and damage==322 and killed==2 and len(original('WIN'))==2 and len(native('WIN'))==2,
      'Two actual native collision KOs, original round winners and instruction-qualified winner-table reads')
    need(all(r['pc']=='FF8296B0'and r['entry']=='FFFEF940'and r['victim_actor']==b['victim_actor']and
      r['victim_main']==b['victim_main']for r in native('WIN')),'Every native winner data read belongs to the actual physical contexts')
    ready=ready[0];zero=int(ready['frame']);forward='Left'if side==1 else'Right'
    physical={(int(r['frame'])-zero,r['button'])for r in original('INPUT')if int(r['slot'])==winner and int(r['frame'])>=zero}
    expected={(age,'Block')for age in range(50)}|{(age,'High_Punch')for age in range(5,50)}|\
      {(age,'Down')for age in range(10,14)}|{(age,forward)for offset in (20,30,40)for age in range(offset,offset+4)}
    need(physical==expected and start==zero+52 and ready['continuation']=='FFA17E10'and
      ready['victim_actor']==b['victim_actor']and ready['victim_main']==b['victim_main']and 60<=int(ready['gap'])<=69,
      'Every original Block lead-in/45-field held HP/Down F F F release and real dizzy/range gate')
    calls=native('CALL');signature=[]
    for entry,age in ((0xff8bbfe0,0),(0xff8bc810,27+side),(0xff8bca00,71+side),
      (0xff876650,71+side),(0xff8bc710,96),(0xff8cdc40,96)):
        found=[r for r in calls if int(r['entry'],16)==entry and int(r['age'])<=96]
        need(len(found)==1 and int(found[0]['age'])==age and int(found[0]['pc'],16)==entry+16 and found[0]['mask']=='FFFF',
          'Actual original cooperative native instruction chronology '+hex(entry))
        r=found[0];victim=entry in (0xff8bc810,0xff8bca00,0xff876650)
        need(r['actor']==b['victim_actor'if victim else'actor']and r['main']==b['victim_main'if victim else'main']and
          int(r['id'])==(identity if victim else10)and r['owner']==r['actor'],'True actual owned victim/winner instruction register contexts')
        signature.append(dict(entry=r['entry'],age=age,pc=r['pc']))
    fields=native('FIELD');need([int(r['age'])for r in fields]==list(range(1,961)),
      'Every native physical field after actual activation through960; no sparse-state acceptance')
    retired=native('RETIRED');need(len(retired)==1 and int(t['retired'])==int(retired[0]['frame']) and
      96<=int(retired[0]['age'])<=960 and not original('CACHE_OVERWRITE'),'Actual both-pointer retirement, no sprite-cache overrun')
    end=int(retired[0]['frame'])
    for r in fields:
        need(r['roster'+str(side)]==str(identity)and r['roster'+str(winner)]=='10','True physical roster remains original throughout observed continuation')
        if int(r['frame'])<end:
            need(r['actor'+str(side)]==b['victim_actor']and r['main'+str(side)]==b['victim_main']and
              r['actor'+str(winner)]==b['actor']and r['main'+str(winner)]==b['main'],
              'No physical actor/Main substitution before genuine native retirement')
        else:need(r['actor1']==r['actor2']=='00000000','Retired physical fighter pointers remain cleared')
    return dict(identity=identity,victimSlot=side,actualNativeActivation=start,actualNativeCompletion=start+96,
      actualNativeRetirement=end,actualNativeCollisionWrites=len(collisions),actualEarnedKOs=killed,
      nativeInstructionCallbackSignature=signature,exactPhysicalStateFields=len(fields),actualHeldReleaseInputFields=len(physical))

def capture(case):
    fighter,side=case;folder=ROOT/f'audit_v4538_scorpion_secondary_{fighter}_p{side}_native_state_ram'
    need(not folder.exists(),'Fresh immutable actual native finisher context')
    source.source_boundary();preflight=json.loads((source.OUT/'report.json').read_text())
    need(preflight['passed']and all(sha(p)==h for p,h in preflight['inputHashes'].items()),'Actual source preflight unchanged before boot')
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'));guest=source.current.expected()
    files={Path(p)for p in build['input_hashes']}|{Path(__file__).resolve(),Path(source.__file__),ROOT/source.LUA,ROOT/source.CONTROL,
      candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',source.OUT/'report.json'}
    for directory in ('roms/mk2ks','samples/mk2ks','artwork'):files.update(p for p in (ROOT/directory).glob('*')if p.is_file())
    pins={str(p.resolve()):sha(p)for p in files}
    need(all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items())and
      sha(candidate/'mkport_candidate.exe')=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
      sha(candidate/'roms/mk2ks/mk2ks.mdata')=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24',
      'Exact unchanged current3836 build/payload and every compiled source input')
    folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compress actual native evidence before writes')
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    for p in files:
        if p.suffix in ('.lua','.py','.ps1','.json'):
            dest=folder/'input_sources/tree'/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
            need(sha(dest)==pins[str(p.resolve())],'Exact collision-free actually executed source snapshot')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='scorpion',
      MK2KS_STOCK_COMMAND='dfff_hp_release',MK2KS_STOCK_GAP='64',MK2KS_REPTILE_AUDIT_DIR=str(folder))
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000','-nocheat','-skip_gameinfo',
      '-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','95',
      '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
      '-autoboot_script',str(ROOT/source.LUA)]
    guest_sha=None;rgb=[]
    with(folder/'stderr.log').open('w',encoding='utf-8')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8')as process:
        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n')
        print(f'{fighter} victimP{side} genuine Scorpion secondary pid={process.pid}',flush=True)
        with(folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith(('MK2_SSECOND_GUEST ','MK2_SSECOND_RGB ')):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'))
                    if line.startswith('MK2_SSECOND_GUEST '):
                        need(guest_sha is None and h==dict(frame='1',bytes='1048576')and raw==guest,'Every actual first-frame initialized current guest byte exact in RAM')
                        guest_sha=hashlib.sha256(raw).hexdigest().upper();h['sha256']=guest_sha
                    else:
                        need(h['width']=='400'and h['height']=='254'and len(raw)==int(h['bytes'])==406400,'Every complete actual native RGB32 transfer')
                        h['sha256']=hashlib.sha256(raw).hexdigest().upper();rgb.append(h)
                    log.write(line.split(' ',1)[0]+'_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\n')
                else:
                    need('hex='not in line,'No raw or encoded native media persisted');log.write(line)
                    if line.startswith(('MK2_SSECOND_BEGIN ','MK2_SSECOND_COMPLETE ','MK2_SSECOND_RETIRED ','MK2_SSECOND_RESULT ')):
                        print(line.strip(),flush=True);log.flush()
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'All actual executed build/source inputs unchanged')
    text=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
    meta=dict(exit_code=code,candidate=NAME,fighter=fighter,victim_slot=side,winner_slot=3-side,
      guestSHA256=guest_sha,completeGuestBytesComparedInRAM=1048576 if guest_sha else0,nativeRGBFramesDigested=len(rgb),
      rawMediaGuestROMOrBuildFilesWritten=0,assistance='none',cheatsEnabled=False,input_hashes=pins,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    (folder/'native_rgb_digests.json').write_text(json.dumps(rgb,indent=2)+'\n')
    need(code==0 and guest_sha and not re.search(r'LUA ERROR|Lua error|stack traceback|fatal error|access violation|WRONG CHECKSUMS',text+error,re.I),
      'Actually terminal full native/current guest observer with no runtime failure')
    need(not list(folder.rglob('*.png'))and not list(folder.rglob('*.wav'))and not list(folder.rglob('*.bin')),
      'No raw native raster/audio/VRAM/guest/build files')
    positive=contract(text,fighter,side)
    need(len(rgb)==62,'All original61 action images plus original continue image transported in RAM, not omitted')
    for p in folder.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
    return dict(fighter=fighter,side=side,capture=str(folder),passed=True,native=positive,inputHashes=pins,
      fullArtFloorShadowOrAudioAccepted=False)

def main():
    need(not OUT.exists(),'Fresh immutable current native secondary matrix')
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:cases=list(pool.map(capture,CASES))
    controls={c['side']:c['native']['nativeInstructionCallbackSignature']for c in cases if c['fighter']in('kitana','liu_kang')}
    need(set(controls)=={1,2}and all(c['native']['nativeInstructionCallbackSignature']==controls[c['side']]for c in cases),
      'Every true17/18 context retains same-slot actual current stock cooperative instruction chronology')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for c in cases:
        for p,h in c['inputHashes'].items():need(p not in pins or pins[p]==h,'Consistent exact current inputs');pins[p]=h
    need(all(sha(p)==h for p,h in pins.items()),'All native inputs/evidence unchanged')
    return dict(passed=True,candidate=NAME,actualCurrentNativeContexts=6,cases=cases,inputHashes=pins,
      bothTrueAddedVictimsBothSlotsCurrentSecondaryNativeStateAccepted=True,
      fullArtFloorShadowAllArenaAlternateOrAudioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as e:report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Immutable actual matrix result');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress matrix result before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
    if report['passed']:print(json.dumps([{k:v for k,v in c.items()if k!='inputHashes'}for c in report['cases']],indent=2),flush=True)
    raise SystemExit(0 if report['passed']else1)
