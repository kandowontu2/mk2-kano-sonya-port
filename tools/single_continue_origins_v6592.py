"""Native CPU damage ownership includes paired victims and real child objects.

Main+230 is the projectile's originating ACTOR (not Main). This is the
existing independently checked Ring contract, and the new passive trace
observes it directly. Preserve the rejected report; qualify the same game.
"""
import argparse,gzip,inspect,json,re,subprocess,types
from pathlib import Path
import single_continue_visible_v6588 as executed
ROOT,need,sha,rows=executed.ROOT,executed.need,executed.sha,executed.rows
REFERENCE=ROOT/'tools/current_sonya_cpu_ring_contract_v2017.py'
DEPENDENCIES=[*executed.DEPENDENCIES,Path(executed.__file__),Path(__file__),REFERENCE,
 ROOT/'source_v6502_native_projectile_identifiers/midtunit_m.cpp']
reference=REFERENCE.read_text()
need("(guard['owner'],guard['parent'],guard['victim'],guard['vmain'],guard['vowner'],guard['vid'])==(child,actor,victim,vmain,victim,17)"in reference,
     'Established native child Main+230 points to CPU actor, not CPU Main')

def origin(q,enemy):
 if enemy['state']!='0'or enemy['owner']!=enemy['actor']:return False
 if q['a8']==enemy['actor']and q['a13']==enemy['main']:return True
 if q['a8']==q['actor']and q['a13']==q['main']and q['ctxOwner']==q['actor']:
  return enemy['id']=='18'and q['pairActor']==enemy['actor']and q['pairMain']==enemy['main']and q['pairAction']=='272'
 return (enemy['state']=='0'and enemy['owner']==enemy['actor']and
  q['a8']not in (q['actor'],enemy['actor'])and q['a13']not in (q['main'],enemy['main'])and
  q['ctxOwner']==q['a8']and q['parent']==enemy['actor']and q['ctxID']==enemy['id']and
  q['pairActor']==q['actor']and q['pairMain']==q['main']and q['caller']=='FF835D70')

base=types.FunctionType(executed.base_gate.__code__,dict(executed.base_gate.__globals__,damage_origin=origin),'gate')
gate=types.FunctionType(executed.gate.__code__,dict(executed.gate.__globals__,base_gate=base),'gate')
source=inspect.getsource(executed.prior.original.capture)
for a,b in {'audit_v6569_single_continue_':'audit_v6593_single_continue_origins_',
 'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),'} .items():
 need(source.count(a)==1,'Complete original collector with source-derived ownership and fresh route');source=source.replace(a,b,1)
scope=dict(executed.capture.__globals__,__file__=__file__,DEPENDENCIES=DEPENDENCIES,gate=gate)
exec(compile(source,__file__+'::whole_original_capture_native_damage_origins','exec'),scope)
capture=scope['capture']

def qualify():
 folder=ROOT/'audit_v6591_single_continue_visible_kano_p2_to_kano'
 out=ROOT/'audit_v6595_single_continue_origins_strict_checked'
 need(not out.exists()and not executed.prior.original.census(),'Same terminal game, no replay')
 old=json.loads((folder/'report.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
 need(old['passed']is False and old['error']=="ValueError('Actual native damage delivered by original CPU actor/Main, not another human or forced HP')"and
  terminal['exitCode']==0 and not terminal['observationErrors']and not(folder/'stderr.log').read_text().strip()and
  len(old['actualGuestGFXProofs'])==2,'Only incorrect source parent-field meaning rejected; full actual runtime intact')
 pins=dict(old['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every actual executed byte unchanged')
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 good=gate(text,'kano',2,'kano');fields=rows(text,'FIELD');health=rows(text,'HEALTH');faults=[]
 damages=[q for q in health if q['slot']=='2'and q['pc']=='FF836700'and int(q['before'])>int(q['after'])and int(q['frame'])<=good['events']['secondKO']]
 pair=next(q for q in damages if q['a8']==q['actor']);child=next(q for q in damages if q['a8']!=q['actor']and q['a8']!=next(v['actor']for v in fields if v['slot']=='1'and v['frame']==q['frame']))
 for tag,key,value,label in [('HEALTH','pairActor',pair['actor'],'false paired CPU actor'),('HEALTH','pairMain','00000000','false paired CPU Main'),
  ('HEALTH','pairAction','0','false active grab'),('HEALTH','parent',child['actor'],'false projectile origin'),
  ('HEALTH','ctxOwner','00000000','false child owner'),('HEALTH','ctxID','1','false child identity'),
  ('HEALTH','caller','00000000','false native child collision caller'),('HEALTH','pc','00000000','false native health kernel'),
  ('HEALTH','parent',next(v['main']for v in fields if v['slot']=='1'and v['frame']==child['frame']),'false projectile Main masquerading as origin'),
  ('FIELD','state','1','human instead of CPU'),('FIELD','id','1','proxy after continue'),
  ('FIELD','owner','00000000','wrong continued Main owner'),('RESULT','reReady','-1','false readiness'),
  ('INPUT','button','Down','false physical payment')]:
  if 'paired'in label or label=='false active grab':q=pair
  elif label.startswith('false projectile')or label.startswith('false child')or label.startswith('false native child'):q=child
  elif tag=='HEALTH':q=damages[0]
  else:q=next(v for v in rows(text,tag)if
   (tag!='FIELD'or v['slot']==str(1 if label=='human instead of CPU'else 2)and int(v['frame'])>=good['events']['reLive'])and
   (tag!='INPUT'or v['button']=='Coin'and int(v['frame'])>good['events']['continue']))
  selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_'+tag+' ')and dict(re.findall(r'(\w+)=([^\s]+)',l))==q)
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1);need(changed!=selected,'Effective actual-row fault')
  try:gate(text.replace(selected,changed,1),'kano',2,'kano')
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False CPU continue ownership admitted '+label)
 need(gate(text,'kano',2,'kano')==good,'Full positive restored')
 for p in (*DEPENDENCIES,*folder.rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,candidate=old['candidate'],executableSHA256=old['executableSHA256'],guestSHA256=old['guestSHA256'],
  nativeExit=0,nativeIdentity=old['nativeIdentity'],actualGuestGFXProofs=old['actualGuestGFXProofs'],actualFullRGBDigests=old['actualFullRGBDigests'],
  actualSinglePlayerContinue=good,actualFaultsRejected=faults,actualPairedVictimStores=sum(q['a8']==q['actor']for q in damages),
  actualChildOwnershipSample=child,preservedOriginalRejection=str(folder/'report.json'),inputHashes=pins,
  newNativeBoots=0,newBuilds=0,newROMCopies=0,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Lossless terminal proof compression')
 print(json.dumps(dict(passed=True,actualSinglePlayerContinue=good,actualFaultsRejected=len(faults))),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('operation',choices=('qualify','capture'));p.add_argument('--fighter',choices=executed.prior.original.IDS)
 p.add_argument('--side',type=int,choices=(1,2));p.add_argument('--target',choices=executed.prior.original.IDS);p.add_argument('--hold',action='store_true');a=p.parse_args()
 if a.operation=='qualify':qualify()
 else:
  need(a.fighter and a.side and a.target,'Exact physical route required');capture(a.fighter,a.side,a.target,a.hold)
