"""Current CMD, earned two-round loss, paid cross-reselect and real control.

The old driver is reused in full. Raw guest/GFX/RGB travel only to RAM;
compressed chronology/digests persist. No build, forced state or old acceptance
transfer. A failed gate is preserved after this same process drains.
"""
import argparse,datetime,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
from capture_current_cmd_specials_v6261 import census
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_current_continue_ram_v6478.lua'
DRIVER=ROOT/'mk2ks_continue_cross_v18_probe.lua'

def rows(text,tag):
 return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines() if line.startswith(tag+' ')]

def gate(text,fighter,side):
 result=rows(text,'MK2_GROUND_RESULT');need(len(result)==1,'One complete physical-driver terminal')
 r=result[0];target='sonya' if fighter=='kano' else 'kano';identity=18 if target=='sonya' else 17
 keys=('css','live','ready','ko','reset','nextReady','secondKO','continue','reselect','reselectExit','reLive','reReady')
 events=[int(r[k]) for k in keys]
 need(r['target']==target and events[0]>0 and all(a<b for a,b in zip(events,events[1:])),
      'Entire earned two-round loss, paid continue, cross-reselect, match and individual ready timeline')
 need(int(r['frame'])==int(r['reReady'])+140,'Original complete walk/jump/landing tail, not deadline exit')
 controls=rows(text,'MK2_GROUND_INPUT')
 start=int(r['continue'])
 for button,first,hold in (('Coin',20,5),('Coin',270,5),('Start',310,5)):
  actual=[int(q['frame']) for q in controls if q['slot']==str(side) and q['button']==button and start+first<=int(q['frame'])<start+first+hold]
  need(actual==list(range(start+first,start+first+hold)),'Every real paid continue input '+button+'/'+str(first))
 fields=[q for q in rows(text,'MK2_CR_FIELD') if q['slot']==str(side) and int(r['reLive'])+1<=int(q['frame'])<=int(r['frame'])]
 need([int(q['frame']) for q in fields]==list(range(int(r['reLive'])+1,int(r['frame'])+1)),
      'Every continued-match post callback, no omitted actor field')
 for q in fields:
  need(q['id']==q['roster']==str(identity) and q['owner']==q['actor'] and q['state']=='1' and q['mode']=='2' and
       q['writes']=='0' and q['assistance']=='none','Real cross-selected owner/ID/controller throughout continued combat')
 ready=int(r['reReady']);tail=[q for q in fields if int(q['frame'])>=ready]
 need(len(tail)==141 and len({q['x'] for q in tail if ready+24<=int(q['frame'])<=ready+44})>1,
      'Actual ordinary walk after continued ready')
 need(any(int(q['y'])<int(q['floor']) for q in tail if ready+64<=int(q['frame'])<=ready+110),
      'Actual physical jump, not input-only marker')
 end=tail[-1]
 need(end['y']==end['floor'] and end['vx']==end['vy']==end['gravity']=='00000000' and int(end['flags'],16)&0x1c==0,
      'Continued fighter landed with native velocities/locks cleared')
 health=rows(text,'MK2_GROUND_HEALTH')
 damage=[q for q in health if q['slot']==str(side) and int(q['before'])>int(q['after']) and int(q['frame'])<=int(r['secondKO'])]
 need(sum(int(q['before'])-int(q['after']) for q in damage)==322 and
      sum(q['after']=='0' for q in damage)==2 and all(q['pc']=='FF836700' for q in damage),
      'Both full161HP losses earned by native collision, no HP assist')
 selection=rows(text,'MK2_GROUND_SELECT')
 need(selection and selection[-1]['roster']==str(identity),'Final continued highlight is the requested real fighter')
 return dict(fighter=fighter,physicalSlot=side,target=target,trueIdentity=identity,events=dict(zip(keys,events)),
             continuedActorFields=len(fields),ordinaryTailFields=len(tail),collisionEarnedLosses=2,
             sourceDriverUnchangedExceptSnapshotSink=True,scope='current two-human paid cross-continue/reselect and ordinary control; not full UI pixel/audio or CPU/post-ending/secret routes')

def capture(fighter,side):
 out=ROOT/f'audit_v6480_current_continue_{fighter}_p{side}_ram'
 need(not out.exists(),'Fresh immutable evidence; never restart a pending or failed run')
 guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 wrapper=LUA.read_text();driver=DRIVER.read_text()
 need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state',wrapper+driver),
      'Read-only state and real buttons only')
 need(driver.count('screen:snapshot(file)')==1 and not census(),'One declared snapshot sink and no live conflicting native job')
 paths=[LUA,DRIVER,Path(__file__),Path(current.__file__),ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd',
        ROOT/'tools/check_current_playtest_v5975.ps1',build/'mkport_candidate.exe',build/'roms/mk2ks/mk2ks.mdata',build/'build-info.json']
 pins={str(p.resolve()):sha(p) for p in paths};out.mkdir()
 env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
 env.update(MK2PORT_CONTINUE_FIGHTER=fighter,MK2PORT_CONTINUE_SIDE=str(side))
 command=[os.environ['ComSpec'],'/d','/c',str(ROOT/'PLAY_MK2_KANO_SONYA.cmd'),'-video','none','-sound','none',
          '-noautoframeskip','-frameskip','0','-nothrottle','-str','250','-cfg_directory',str(out/'cfg'),
          '-nvram_directory',str(out/'nvram'),'-snapshot_directory',str(out/'snap'),'-autoboot_script',str(LUA)]
 errors=[];proofs={};scenes=[];native=None;started=time.time()
 with (out/'stderr.log').open('w',encoding='utf-8') as err:
  process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace')
  (out/'process.json').write_text(json.dumps(dict(command=command,cmdPID=process.pid,startedUnix=started),indent=2)+'\n')
  print(f'{fighter} P{side}: current CMD pid={process.pid}',flush=True)
  time.sleep(2)
  try:
   jobs=census();matches=[j for j in jobs if j['ParentProcessId']==process.pid and j['ExecutablePath'] and Path(j['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve() and str(out) in (j['CommandLine'] or '') and j['createdUnix']>=started]
   need(len(matches)==1,'Exact live current executable child, full command and creation time');native=matches[0]
   (out/'native_identity.json').write_text(json.dumps(native,indent=2)+'\n')
  except Exception as error:errors.append(repr(error))
  with gzip.open(out/'run.log.gz','wt',encoding='utf-8') as log:
   for line in process.stdout:
    try:
     if line.startswith(('MK2_CR_GUEST ','MK2_CR_GFX ','MK2_CR_RGB ')):
      r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'));digest=hashlib.sha256(raw).hexdigest().upper();tag=line.split()[0]
      if tag.endswith(('GUEST','GFX')):
       kind='guest' if tag.endswith('GUEST') else 'gfx';wanted=guest if kind=='guest' else gfx
       need(kind not in proofs and raw==wanted,'Entire actual independently reconstructed '+kind);proofs[kind]=dict(bytes=len(raw),sha256=digest)
      else:
       need(len(raw)==406400,'Full current RGB transport');scenes.append(dict(frame=int(r['frame']),sha256=digest))
      log.write(tag+'_DIGEST '+' '.join(k+'='+v for k,v in r.items())+' sha256='+digest+'\n')
     elif line.startswith('MK2_GROUND_GFX '):
      r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('data'))
      log.write('MK2_GROUND_GFX_DIGEST '+' '.join(k+'='+v for k,v in r.items())+' sha256='+hashlib.sha256(raw).hexdigest().upper()+'\n')
     else:
      need('hex=' not in line and ' data=' not in line,'No raw buffer persists');log.write(line)
      if re.match(r'MK2_GROUND_(CSS|LIVE|READY|KO|ROUND_RESET|NEXT_READY|SECOND_KO|CONTINUE|RESELECT |RESELECT_EXIT|RE_LIVE|RE_READY|RESULT)',line):print(line.strip(),flush=True)
    except Exception as error:errors.append(repr(error))
   code=process.wait()
 report=dict(passed=False,candidate=current.NAME,executableSHA256=current.EXE_SHA,payloadSHA256=current.PAYLOAD_SHA,
             nativeExit=code,nativeIdentity=native,observationErrors=errors,actualGuestGFXProofs=proofs,actualRGBDigests=scenes,inputHashes=pins,
             nativeGamesInterrupted=0,newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False)
 try:
  need(code==0 and native and not census() and not errors and len(proofs)==2 and not(out/'stderr.log').read_text().strip(),
       'Same natural native terminal, whole memory proofs and empty stderr/observation errors')
  need(all(sha(p)==h for p,h in pins.items()),'All executed and playable bytes unchanged')
  with gzip.open(out/'run.log.gz','rt',encoding='utf-8') as f:text=f.read()
  need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),'No runtime error')
  result=gate(text,fighter,side);faults=[]
  for label,tag,key,value in [('wrong real ID','MK2_CR_FIELD','id','1'),('wrong owner','MK2_CR_FIELD','owner','00000000'),
                             ('false ready','MK2_GROUND_RESULT','reReady','-1'),('incomplete walk tail','MK2_GROUND_RESULT','frame','1')]:
   selected=next(l for l in text.splitlines() if l.startswith(tag+' ') and (tag!='MK2_CR_FIELD' or f'slot={side} ' in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>result['events']['reLive']))
   altered=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1);need(altered!=selected,'Effective current record fault')
   try:gate(text.replace(selected,altered,1),fighter,side)
   except(ValueError,KeyError) as error:faults.append(dict(kind=label,rejectedBy=str(error)))
   else:raise ValueError('Actual faulty continuation accepted '+label)
   need(gate(text,fighter,side)==result,'Full positive restored after fault')
  report.update(passed=True,actualCurrentContinuation=result,actualFaultsRejected=faults)
 except Exception as error:report.update(error=repr(error),traceback=traceback.format_exc())
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 for p in out.rglob('*'):
  if p.is_file():
   before=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==before,'Exact terminal evidence compression')
 print(json.dumps(dict(passed=report['passed'],fighter=fighter,side=side,nativeExit=code,error=report.get('error'),scenes=len(scenes))),flush=True)
 need(report['passed'],'Current continuation rejected; preserve actual failure')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));a=parser.parse_args();capture(a.fighter,a.side)
