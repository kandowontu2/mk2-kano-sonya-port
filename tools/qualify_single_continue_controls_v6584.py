"""Same completed native run; Block begins one callback after RECOVER.

Preserve original rejection/executed sources. Full round/selection/ownership/
control/health gate and actual-record faults, without another native boot.
"""
import gzip,json,re,subprocess
from pathlib import Path
import single_continue_controls_v6580 as current
ROOT,need,sha,rows,gate=current.ROOT,current.need,current.sha,current.rows,current.gate

def qualify():
 folder=ROOT/'audit_v6583_single_continue_controls_kano_p1_to_kano'
 out=ROOT/'audit_v6584_single_continue_controls_same_native_checked'
 need(not out.exists() and not current.original.census(),'Same naturally terminal game, no replay')
 old=json.loads((folder/'report.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
 need(old['passed']is False and old['error']=="ValueError('Every finite survival field uses only ordinary physical Block')"and
  terminal['exitCode']==0 and not terminal['observationErrors']and not(folder/'stderr.log').read_text().strip()and
  len(old['actualGuestGFXProofs'])==2,'Only exact next-branch physical Block boundary rejected')
 migrations=[];pins={}
 for path,h in old['inputHashes'].items():
  if sha(path)==h:pins[path]=h;continue
  copy=folder/'executed_sources'/Path(path).name
  need(Path(path).name=='single_continue_controls_v6580.py'and sha(copy)==h,'Only explicitly preserved checker alias changes')
  migrations.append(dict(historicalPath=path,executedSnapshot=str(copy),sha256=h))
  pins[str(copy)]=h
 driver=current.LUA.read_text()
 need('elseif not recover then'in driver and driver.index('recover=frame;')<driver.index("pulse('Block',frame-recover,0,180)"),
      'Recovery observation and Block are mutually exclusive branches, first Block is recover+1')
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 good=gate(text,'kano',1,'kano');faults=[]
 for label,tag,key,value in [('wrong ID','FIELD','id','1'),('wrong Main owner','FIELD','owner','00000000'),
  ('human instead of CPU','FIELD','state','1'),('false ready','RESULT','reReady','-1'),
  ('wrong physical payment','INPUT','button','Down'),('false native damage','HEALTH','pc','00000000'),
  ('CPU hit mistaken for jump','JUMP','start','4009'),('false punch','PUNCH','frame','4005'),
  ('false recovery','RECOVER','frame','4208')]:
  selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_'+tag+' ')and
   (tag!='FIELD'or ('slot='+str(2 if label=='human instead of CPU'else 1)+' ')in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>=good['events']['reLive'])and
   (tag!='INPUT'or 'button=Coin 'in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>good['events']['continue'])and
   (tag!='HEALTH'or 'pc=FF836700 'in l and 'slot=1 'in l))
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1);need(changed!=selected,'Effective actual-record fault')
  try:gate(text.replace(selected,changed,1),'kano',1,'kano')
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False single-player control proof admitted '+label)
 for n in (1,2):
  at=good['events']['recover']+179
  selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_FIELD ')and f'slot={n} 'in l and f'frame={at} 'in l)
  try:gate(text.replace(selected+'\n','',1),'kano',1,'kano')
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=f'missing final actual slot{n}',rejectedBy=str(e)))
  else:raise ValueError('Missing real terminal field admitted')
 need(gate(text,'kano',1,'kano')==good,'All complete positive evidence restored')
 for p in (*current.DEPENDENCIES,*folder.rglob('*'),Path(__file__)):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,candidate=old['candidate'],executableSHA256=old['executableSHA256'],guestSHA256=old['guestSHA256'],
  nativeExit=0,nativeIdentity=old['nativeIdentity'],actualGuestGFXProofs=old['actualGuestGFXProofs'],
  actualFullRGBDigests=old['actualFullRGBDigests'],actualSinglePlayerContinue=good,actualFaultsRejected=faults,
  preservedOriginalRejection=str(folder/'report.json'),intentionalCheckerAliasMigrations=migrations,inputHashes=pins,
  newNativeBoots=0,newBuilds=0,newROMCopies=0,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Lossless same-run proof compression')
 print(json.dumps(dict(passed=True,actualSinglePlayerContinue=good,actualFaultsRejected=len(faults))),flush=True)

if __name__=='__main__':qualify()
