"""Actual checked-CMD CPU-earned loss and paid single-player re-selection.

Every guest/art byte and native child identity is checked. Native HP ledgers,
both actors, physical buttons and full display digests are retained compressed;
raw guest/GFX/RGB stays in RAM. Scope is explicitly finite single-player routes,
not all UI/art/audio/campaign/finishers. Failed native runs remain failures.
"""
import argparse,code,datetime,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import native_projectile_identifiers_context_v6509 as current
from capture_current_cmd_specials_v6261 import census
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_single_continue_v6567.lua'
IDS={'kano':17,'sonya':18}

def rows(text,tag):
 return [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_SC_'+tag+' ')]

def gate(text,fighter,side,target):
 results=rows(text,'RESULT');need(len(results)==1 and not rows(text,'DEADLINE'),'One complete controller terminal; no deadline substitute')
 r=results[0];events={k:int(r[k])for k in ('css','live','ready','ko','reset','nextReady','secondKO','continue','reselect','reselectExit','reLive','reReady')}
 e=events
 need(r['fighter']==fighter and r['target']==target and r['side']==str(side) and
      0<e['css']<e['live']<=e['ready']<e['ko']<e['reset']<=e['nextReady']<e['secondKO']<e['continue']<e['reselect']<e['reselectExit']<e['reLive']<=e['reReady'],
      'Whole ordered native CPU rounds, paid continue, selection, ladder and true new match')
 terminal=int(r['frame']);need(terminal==e['reReady']+180,'Complete actual post-continue control tail, not early exit')
 fields=rows(text,'FIELD');after=[q for q in fields if e['reLive']<int(q['frame'])<=terminal]
 for n in (1,2):
  actual=[q for q in after if q['slot']==str(n)]
  need([int(q['frame'])for q in actual]==list(range(e['reLive']+1,terminal+1)),'Every continued physical actor callback, no omitted fields')
  if n==side:
   need(all(q['id']==q['roster']==str(IDS[target])and q['owner']==q['actor']and q['mode']=='2'and q['state']=='1'and
            q['writes']=='0'and q['assistance']=='none'for q in actual),'Requested true continued fighter and own Main, no human proxy')
  else:
   need(all(q['state']=='0'and q['id']==q['roster']and q['owner']==q['actor']for q in actual),'Other player remains a genuine CPU opponent; not two-human continue')
 own=[q for q in after if q['slot']==str(side)];tail=[q for q in own if int(q['frame'])>=e['reReady']]
 need(len({q['x']for q in tail if e['reReady']+12<=int(q['frame'])<=e['reReady']+38})>1,'Actual physical walk, not input-only marker')
 need(any(int(q['y'])<int(q['floor'])for q in tail if e['reReady']+64<=int(q['frame'])<=e['reReady']+110),'Actual post-continue airborne jump')
 need(any(q['action']=='257'for q in tail if e['reReady']+128<=int(q['frame'])<=e['reReady']+160),'Actual ordinary native punch after continue')
 controls=rows(text,'INPUT')
 for button,start,hold in [('Coin',20,5),('Start',80,5)]:
  want=list(range(e['continue']+start,e['continue']+start+hold))
  need([int(q['frame'])for q in controls if q['button']==button and e['continue']<=int(q['frame'])<e['reselect']]==want,'Exact paid normal continue input '+button)
 for button,start,hold in [('Up',64,3),('High_Punch',128,3)]:
  need([int(q['frame'])for q in controls if q['button']==button and int(q['frame'])>=e['reReady']]==list(range(e['reReady']+start,e['reReady']+start+hold)),
       'Exact post-continue physical input '+button)
 health=rows(text,'HEALTH');windows=((e['live'],e['ko']),(e['reset'],e['secondKO']))
 damages=[q for q in health if q['slot']==str(side)and q['mode']=='2'and q['pc']=='FF836700'and
          any(lo<=int(q['frame'])<=hi for lo,hi in windows)and int(q['before'])>int(q['after'])]
 need(sum(int(q['before'])-int(q['after'])for q in damages)==322 and sum(q['after']=='0'for q in damages)==2 and
      all(q['mask']=='FFFF'and q['id']==str(IDS[fighter])and q['owner']==q['actor']for q in damages),'Two complete161HP CPU collision-earned losses, no health assist')
 for q in damages:
  enemy=[f for f in fields if f['slot']==str(3-side)and int(f['frame'])==int(q['frame'])]
  need(len(enemy)==1 and enemy[0]['state']=='0'and q['a8']==enemy[0]['actor']and q['a13']==enemy[0]['main'],
       'Actual native damage delivered by original CPU actor/Main, not another human or forced HP')
 selected=[q for q in rows(text,'SELECT')if int(q['origin'])==e['reselect']]
 need(selected and selected[-1]['roster']==selected[-1]['wanted']==str(IDS[target]),'Final continued highlight is the requested native character')
 return dict(fighter=fighter,physicalSlot=side,target=target,trueIdentity=IDS[target],events=e,
             nativeCPUID=int(r['cpuID']),collisionEarnedLosses=2,continuedActorFields=len(after),ordinaryTailFields=len(tail),
             actualCPUHealthStores=len(damages),singlePlayerCPUNotSecondHuman=True,scope=__doc__)

def capture(fighter,side,target,hold=False):
 out=ROOT/f'audit_v6569_single_continue_{fighter}_p{side}_to_{target}'
 need(not out.exists()and not census(),'Fresh exact native capture; do not restart pending/failed evidence')
 guest=current.expected();gfx=current.expected_gfx();build=ROOT/current.NAME
 source=LUA.read_text();need(not re.search(r':write_|\.value\s*=(?!=)|load_?state',source),'Physical buttons/passive observation only')
 pins={str(p.resolve()):sha(p)for p in (LUA,Path(__file__),Path(current.__file__),ROOT/'PLAY_MK2_KANO_SONYA.cmd',
       ROOT/'PLAY_CURRENT_V6508_CHECKED.cmd',ROOT/'tools/check_repaired_playtest_v6552.ps1',
       ROOT/'audit_v6566_repaired_native_handoff/report.json',build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata')}
 out.mkdir();env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
 env.update(MK2PORT_SINGLE_CONTINUE_FIGHTER=fighter,MK2PORT_SINGLE_CONTINUE_TARGET=target,MK2PORT_SINGLE_CONTINUE_SIDE=str(side))
 command=[os.environ['ComSpec'],'/d','/c',str(ROOT/'PLAY_MK2_KANO_SONYA.cmd'),'-video','none','-sound','none','-noautoframeskip',
          '-frameskip','0','-nothrottle','-str','250','-snapsize','400x254','-inipath',str(out),'-cfg_directory',str(out/'cfg'),
          '-nvram_directory',str(out/'nvram'),'-snapshot_directory',str(out/'snap'),'-autoboot_script',str(LUA)]
 started=time.time();native=None;errors=[];proofs={};images={};digests=[]
 with(out/'stderr.log').open('w',encoding='utf-8')as err:
  process=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace')
  (out/'process.json').write_text(json.dumps(dict(command=command,cmdPID=process.pid,startedUnix=started),indent=2)+'\n')
  print(f'{fighter} P{side} to {target}: actual checked CMD pid={process.pid}',flush=True)
  try:
   time.sleep(2);jobs=census();(out/'live_census.json').write_text(json.dumps(jobs,indent=2)+'\n')
   matches=[j for j in jobs if j['ParentProcessId']==process.pid and j['ExecutablePath']and Path(j['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve()and j['createdUnix']>=started and str(out)in(j['CommandLine']or'')]
   need(len(matches)==1,'Actual exact native executable child, birth time and isolated full command');native=matches[0]
   (out/'native_identity.json').write_text(json.dumps(native,indent=2)+'\n')
  except Exception as e:errors.append(repr(e))
  with gzip.open(out/'run.log.gz','wt',encoding='utf-8')as log:
   for line in process.stdout:
    try:
     if line.startswith(('MK2_SC_GUEST ','MK2_SC_GFX ','MK2_SC_RGB ')):
      r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'));h=hashlib.sha256(raw).hexdigest().upper();tag=line.split()[0]
      if tag.endswith(('GUEST','GFX')):
       kind='guest'if tag.endswith('GUEST')else'gfx';wanted=guest if kind=='guest'else gfx
       need(kind not in proofs and raw==wanted,'Entire independently reconstructed actual '+kind);proofs[kind]=dict(bytes=len(raw),sha256=h,everyActualByteComparedInRAM=True)
      else:
       need(len(raw)==406400 and r['width']=='400'and r['height']=='254','Complete native unscaled display buffer')
       key=(int(r['frame']),r['label']);need(key not in images,'Unique displayed native scene')
       images[key]=raw;digests.append(dict(frame=key[0],label=key[1],bytes=len(raw),sha256=h))
      log.write(tag+'_DIGEST '+' '.join(k+'='+v for k,v in r.items())+' sha256='+h+'\n')
     else:
      need('hex='not in line,'Never persist raw memory/media');log.write(line)
      if re.match(r'MK2_SC_(CSS|LIVE|READY|KO|ROUND_RESET|NEXT_READY|SECOND_KO|CONTINUE|RESELECT |RESELECT_EXIT|RE_LIVE|RE_READY|DEADLINE|RESULT)',line):print(line.strip(),flush=True)
    except Exception as e:errors.append(repr(e))
   exitcode=process.wait()
 terminal=dict(cmdPID=process.pid,nativePID=native['ProcessId']if native else None,exitCode=exitcode,naturalTerminal=True,observationErrors=errors,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (out/'native_terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
 r=dict(passed=False,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,nativeExit=exitcode,
        nativeIdentity=native,actualGuestGFXProofs=proofs,actualFullRGBDigests=digests,inputHashes=pins,
        newBuilds=0,newROMCopies=0,newRawMedia=0,fullPortAcceptance=False)
 with gzip.open(out/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 try:
  need(exitcode==0 and native and not errors and len(proofs)==2 and not census()and not(out/'stderr.log').read_text().strip(),
       'Same native process naturally terminal; exact memory, identity and no observer errors')
  need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),'No native runtime error')
  result=gate(text,fighter,side,target);faults=[]
  for label,tag,key,value in [('wrong ID','FIELD','id','1'),('wrong Main owner','FIELD','owner','00000000'),
                             ('human instead of CPU','FIELD','state','1'),('false ready','RESULT','reReady','-1'),
                             ('wrong physical payment','INPUT','button','Down'),('false native damage','HEALTH','pc','00000000')]:
   selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_'+tag+' ')and
    (tag!='FIELD'or ('slot='+str(3-side if label=='human instead of CPU'else side)+' ')in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>result['events']['reLive'])and
    (tag!='INPUT'or 'button=Coin 'in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>result['events']['continue'])and
    (tag!='HEALTH'or 'pc=FF836700 'in l and ('slot='+str(side)+' ')in l))
   bad=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1);need(bad!=selected,'Effective actual-record fault')
   try:gate(text.replace(selected,bad,1),fighter,side,target)
   except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
   else:raise ValueError('False single-player native route admitted '+label)
  need(gate(text,fighter,side,target)==result and all(sha(p)==h for p,h in pins.items()),'All positive gates and executed bytes restored/intact')
  r.update(passed=True,actualSinglePlayerContinue=result,actualFaultsRejected=faults)
 except Exception as e:r.update(error=repr(e),traceback=traceback.format_exc())
 (out/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 for p in out.rglob('*'):
  if p.is_file():
   h=sha(p);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact terminal evidence compression')
 print(json.dumps(dict(passed=r['passed'],fighter=fighter,side=side,target=target,nativeExit=exitcode,error=r.get('error'),scenes=len(digests))),flush=True)
 if hold:code.interact(banner='Same terminal native process; full actual display buffers remain in RAM, no replay.',local=dict(images=images,text=text,report=r,guest=guest,folder=out))
 need(r['passed'],'Single-player route rejected; retain actual native failure')
 return r

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--fighter',choices=IDS,required=True);p.add_argument('--side',type=int,choices=(1,2),required=True);p.add_argument('--target',choices=IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 capture(a.fighter,a.side,a.target,a.hold)
