"""Full single-player continue gate with the actual native exit boundary.

The controller exits during register_frame at reReady+180; frame_done exists
from reLive through terminal-1, not after the exit request. Preserve the
original rejection and qualify the same trace, never invent a terminal field.
Also run further independent normal-CMD cases using the unchanged controller.
"""
import argparse,gzip,inspect,json,re,subprocess
from pathlib import Path
import capture_single_continue_v6568 as original

ROOT,need,sha,rows=original.ROOT,original.need,original.sha,original.rows
LUA=ROOT/'mk2ks_single_continue_ready_v6573.lua'
DEPENDENCIES=[ROOT/'mk2ks_single_continue_v6567.lua',LUA,
 ROOT/'tools/capture_single_continue_v6568.py',Path(__file__),
 ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp']

def bindings():
 source=inspect.getsource(original.gate)
 changes={
  "e['reLive']<int(q['frame'])<=terminal":"e['reLive']<=int(q['frame'])<terminal",
  "range(e['reLive']+1,terminal+1)":"range(e['reLive'],terminal)",
  "[('Coin',20,5),('Start',80,5)]":"[('Coin',20,5),('Coin',270,5),('Start',310,5)]",
  "if q['button']==button and e['continue']<=int(q['frame'])<e['reselect']":
   "if q['button']==button and e['continue']+start<=int(q['frame'])<e['continue']+start+hold",
 }
 for a,b in changes.items():
  need(source.count(a)==1,'Exact complete original gate adaptation '+a)
  source=source.replace(a,b,1)
 scope=dict(original.__dict__,__file__=__file__,LUA=LUA,DEPENDENCIES=DEPENDENCIES)
 exec(compile(source,__file__+'::whole_original_gate_native_boundary','exec'),scope)
 source=inspect.getsource(original.capture)
 changes={
  'audit_v6569_single_continue_':'audit_v6577_single_continue_checked_',
  'for p in (LUA,Path(__file__),':'for p in (*DEPENDENCIES,LUA,Path(__file__),',
 }
 for a,b in changes.items():
  need(source.count(a)==1,'Original collector with fresh destination and full dependency pins')
  source=source.replace(a,b,1)
 exec(compile(source,__file__+'::whole_original_capture_checked_boundary','exec'),scope)
 return scope['gate'],scope['capture']

gate,capture=bindings()

def qualify(fighter,side,target):
 folder=ROOT/f'audit_v6575_single_continue_ready_{fighter}_p{side}_to_{target}'
 out=ROOT/f'audit_v6578_single_continue_same_run_{fighter}_p{side}_to_{target}'
 need(not out.exists() and not original.census(),'Same terminal native capture, no replay')
 old=json.loads((folder/'report.json').read_text())
 terminal=json.loads((folder/'native_terminal.json').read_text())
 need(old['passed']is False and old['error']=="ValueError('Every continued physical actor callback, no omitted fields')" and
      terminal['exitCode']==0 and not terminal['observationErrors'] and len(old['actualGuestGFXProofs'])==2 and
      not(folder/'stderr.log').read_text().strip(),'Exactly failed post-exit callback assumption; no native/observer error')
 pins=dict(old['inputHashes'])
 need(all(sha(p)==h for p,h in pins.items()),'All executed native inputs remain intact')
 driver=(ROOT/'mk2ks_single_continue_v6567.lua').read_text()
 need(driver.count('if age>=180 then manager.machine:exit()end')==1 and
      driver.index('if age>=180 then manager.machine:exit()end')<driver.index('emu.register_frame_done(function()'),
      'Actual exit precedes subsequent rendered-frame observer')
 with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',text,re.I),'Clean actual native trace')
 good=gate(text,fighter,side,target);end=int(rows(text,'RESULT')[0]['frame'])
 fields=rows(text,'FIELD');indexed={(int(q['frame']),int(q['slot']))for q in fields}
 need(all((end,n)not in indexed and (end-1,n)in indexed and (good['events']['reLive'],n)in indexed for n in (1,2)),
      'Every real continued callback, including first; no fictitious post-exit field')
 faults=[]
 for label,tag,key,value in [('wrong ID','FIELD','id','1'),('wrong Main owner','FIELD','owner','00000000'),
  ('human instead of CPU','FIELD','state','1'),('false ready','RESULT','reReady','-1'),
  ('wrong physical payment','INPUT','button','Down'),('false native damage','HEALTH','pc','00000000')]:
  selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_'+tag+' ')and
   (tag!='FIELD'or ('slot='+str(3-side if label=='human instead of CPU'else side)+' ')in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>=good['events']['reLive'])and
   (tag!='INPUT'or 'button=Coin 'in l and int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])>good['events']['continue'])and
   (tag!='HEALTH'or 'pc=FF836700 'in l and ('slot='+str(side)+' ')in l))
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+value,selected,count=1)
  need(changed!=selected,'Effective original actual-record fault')
  try:gate(text.replace(selected,changed,1),fighter,side,target)
  except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('False single-player evidence admitted '+label)
 for n in (1,2):
  for at in (good['events']['reLive'],end-1):
   selected=next(l for l in text.splitlines()if l.startswith('MK2_SC_FIELD ')and f'slot={n} 'in l and f'frame={at} 'in l)
   try:gate(text.replace(selected+'\n','',1),fighter,side,target)
   except(ValueError,AssertionError,KeyError)as e:faults.append(dict(kind=f'missing boundary slot{n} frame{at}',rejectedBy=str(e)))
   else:raise ValueError('Missing actual boundary callback admitted')
 need(gate(text,fighter,side,target)==good,'Complete positive restored after all faults')
 for p in (*DEPENDENCIES,*folder.rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,candidate=old['candidate'],executableSHA256=old['executableSHA256'],guestSHA256=old['guestSHA256'],
  nativeExit=0,nativeIdentity=old['nativeIdentity'],actualGuestGFXProofs=old['actualGuestGFXProofs'],
  actualFullRGBDigests=old['actualFullRGBDigests'],actualSinglePlayerContinue=good,actualFaultsRejected=faults,
  preservedOriginalRejection=str(folder/'report.json'),actualNativeBoundary='reLive inclusive through terminal-1 inclusive',
  inputHashes=pins,newNativeBoots=0,newBuilds=0,newROMCopies=0,fullPortAcceptance=False,goalStatus='active')
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Lossless proof compression')
 print(json.dumps(dict(passed=True,route=good,actualFaultsRejected=len(faults))),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('operation',choices=('qualify','capture'));p.add_argument('--fighter',choices=original.IDS,required=True)
 p.add_argument('--side',type=int,choices=(1,2),required=True);p.add_argument('--target',choices=original.IDS,required=True);p.add_argument('--hold',action='store_true');a=p.parse_args()
 if a.operation=='qualify':qualify(a.fighter,a.side,a.target)
 else:capture(a.fighter,a.side,a.target,a.hold)
