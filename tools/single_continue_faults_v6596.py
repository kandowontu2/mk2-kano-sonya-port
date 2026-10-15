"""Full continue/ownership gate; mutate a real CPU loss, not attract HP.

The original collector's first matching health row may be outside this route.
Select a positive-damage callback inside either actual loss window. Preserve
the fault-selector rejection and qualify the same completed native game.
"""
import argparse,gzip,inspect,json,re,subprocess
from pathlib import Path
import single_continue_origins_v6592 as current
ROOT,need,sha,rows,gate=current.ROOT,current.need,current.sha,current.rows,current.gate
DEPENDENCIES=[*current.DEPENDENCIES,Path(current.__file__),Path(__file__)]
def loss_damage(line,result,side):
 q=dict(re.findall(r'(\w+)=([^\s]+)',line));e=result['events']
 return(q['slot']==str(side)and q['pc']=='FF836700'and q['mode']=='2'and int(q['before'])>int(q['after'])and
        any(lo<=int(q['frame'])<=hi for lo,hi in ((e['live'],e['ko']),(e['reset'],e['secondKO']))))
source=inspect.getsource(current.executed.prior.original.capture)
for a,b in {'audit_v6569_single_continue_':'audit_v6598_single_continue_faults_',
 'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),',
 "(tag!='HEALTH'or 'pc=FF836700 'in l and ('slot='+str(side)+' ')in l))":
 "(tag!='HEALTH'or loss_damage(l,result,side)))"}.items():
 need(source.count(a)==1,'Only actual native loss fault selector/provenance/output correction');source=source.replace(a,b,1)
scope=dict(current.capture.__globals__,__file__=__file__,DEPENDENCIES=DEPENDENCIES,loss_damage=loss_damage,gate=gate)
exec(compile(source,__file__+'::whole_original_collector_actual_loss_counterexample','exec'),scope)
capture=scope['capture']

def qualify(fighter,side,target):
 folder=ROOT/f'audit_v6593_single_continue_origins_{fighter}_p{side}_to_{target}'
 out=ROOT/f'audit_v6597_single_continue_actual_faults_{fighter}_p{side}_to_{target}'
 need(not out.exists()and not current.executed.prior.original.census(),'Same naturally completed game, no replay')
 old=json.loads((folder/'report.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
 need(old['passed']is False and old['error']=="ValueError('False single-player native route admitted false native damage')"and
  terminal['exitCode']==0 and not terminal['observationErrors']and not(folder/'stderr.log').read_text().strip()and
  len(old['actualGuestGFXProofs'])==2,'Only ineffective original counterexample selection, not failed gameplay')
 pins=dict(old['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Actually executed inputs intact')
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 good=gate(text,fighter,side,target);faults=[]
 for label,tag,key,value in [('wrong ID','FIELD','id','1'),('wrong Main owner','FIELD','owner','00000000'),
  ('human instead of CPU','FIELD','state','1'),('false ready','RESULT','reReady','-1'),
  ('wrong physical payment','INPUT','button','Down'),('false native damage','HEALTH','pc','00000000')]:
  selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_'+tag+' ')and
   (tag!='FIELD'or ('slot='+str(3-side if label=='human instead of CPU'else side)+' ')in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>=good['events']['reLive'])and
   (tag!='INPUT'or 'button=Coin 'in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>good['events']['continue'])and
   (tag!='HEALTH'or loss_damage(l,good,side)))
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1);need(changed!=selected,'Effective actual-route fault')
  try:gate(text.replace(selected,changed,1),fighter,side,target)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False real single-player evidence admitted '+label)
 need(gate(text,fighter,side,target)==good,'Full positive restored')
 for p in (*DEPENDENCIES,*folder.rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,candidate=old['candidate'],executableSHA256=old['executableSHA256'],guestSHA256=old['guestSHA256'],
  nativeExit=0,nativeIdentity=old['nativeIdentity'],actualGuestGFXProofs=old['actualGuestGFXProofs'],actualFullRGBDigests=old['actualFullRGBDigests'],
  actualSinglePlayerContinue=good,actualFaultsRejected=faults,preservedOriginalRejection=str(folder/'report.json'),inputHashes=pins,
  newNativeBoots=0,newBuilds=0,newROMCopies=0,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Lossless proof compression')
 print(json.dumps(dict(passed=True,actualSinglePlayerContinue=good,actualFaultsRejected=len(faults))),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('operation',choices=('qualify','capture'));p.add_argument('--fighter',choices=current.executed.prior.original.IDS,required=True)
 p.add_argument('--side',type=int,choices=(1,2),required=True);p.add_argument('--target',choices=current.executed.prior.original.IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 if a.operation=='qualify':qualify(a.fighter,a.side,a.target)
 else:capture(a.fighter,a.side,a.target,a.hold)
