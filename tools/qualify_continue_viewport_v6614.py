"""Additive same-native qualification; retain original false collector report.

Called with real native buffers still held by its terminal host, never replays
or synthesizes scene/state. All sparse inspection PNGs are declared explicitly.
"""
import json,re,hashlib,subprocess
from pathlib import Path
import numpy as np
import continue_viewport_contract_v6610 as contract
ROOT,need,sha=contract.ROOT,contract.need,contract.sha

def qualify(folder,text,images,old,fighter,side,target):
 folder=Path(folder);out=ROOT/f'audit_v6615_continue_viewport_checked_{fighter}_p{side}_to_{target}'
 need(not out.exists(),'New additive proof; never rewrite failed evidence')
 terminal=json.loads((folder/'native_terminal.json').read_text())
 need(terminal['exitCode']==0 and not terminal['observationErrors']and old['nativeExit']==0 and
      not(folder/'stderr.log').read_text().strip()and len(old['actualGuestGFXProofs'])==2,
      'Actual completed native game, full RAM guest/GFX proofs and no observer error')
 need(all(sha(p)==h for p,h in old['inputHashes'].items()),'Exact captured sources remain intact')
 for q in old['actualFullRGBDigests']:
  raw=images[(q['frame'],q['label'])]
  need(len(raw)==406400 and hashlib.sha256(raw).hexdigest().upper()==q['sha256'],
       'Every RAM image byte matches its actual native callback digest')
 load=lambda name:np.frombuffer(images[(int(name[3:7]),name)],np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
 good=contract.gate(text,fighter,side,target);pixels=contract.render(folder,text,target,side,load=load);faults=[]
 def reject(label,call):
  try:call()
  except(ValueError,AssertionError,KeyError,IndexError)as e:faults.append(dict(kind=label,rejectedBy=str(e)))
  else:raise ValueError('Effective actual native counterexample admitted: '+label)
 def state(label,prefix,predicate,key,value):
  line=next(l for l in text.splitlines()if l.startswith(prefix)and predicate(dict(re.findall(r'(\w+)=([^\s]+)',l))))
  changed=re.sub(r'\b'+key+r'=\S+',key+'='+str(value),line,count=1)
  need(line!=changed,'Effective actual source-row counterexample')
  reject(label,lambda:contract.gate(text.replace(line,changed,1),fighter,side,target))
 e=good['events'];initial=lambda q:int(q['frame'])<e['live'];continued=lambda q:int(q['frame'])>=e['reLive']
 state('wrong real continued ID','MK2_SC_FIELD ',lambda q:continued(q)and q['slot']==str(side),'id',1)
 state('wrong continued Main owner','MK2_SC_FIELD ',lambda q:continued(q)and q['slot']==str(side),'owner','00000000')
 state('human replacing real CPU','MK2_SC_FIELD ',lambda q:continued(q)and q['slot']==str(3-side),'state',1)
 state('false final ready','MK2_SC_RESULT ',lambda q:True,'reReady',-1)
 state('wrong paid input','MK2_SC_INPUT ',lambda q:q['button']=='Coin'and int(q['frame'])>e['continue'],'button','Down')
 state('false positive CPU damage','MK2_SC_HEALTH ',lambda q:contract.original.prior.loss_damage(' '.join(k+'='+z for k,z in q.items()),good,side),'pc','00000000')
 for label,predicate in [('initial native ladder consumer',initial),('continued native ladder consumer',lambda q:int(q['frame'])>e['continue'])]:
  state(label,'MK2_UI_LADDER ',predicate,'pc','00000000')
 state('bad native settled neighbor','MK2_UI_SELECT ',lambda q:q['age']=='180','roster',1)
 state('bad final selected true ID','MK2_UI_SELECT ',lambda q:int(q['frame'])==good['actualUIState']['exit'],'roster',1)
 state('missing native player-number slot','MK2_UI_FIELD ',lambda q:q['age']=='0'and q['slot']==str(side),'side',3-side)
 if side==2:
  state('persistent P1 startup punch','MK2_SC_IO ',lambda q:q['frame']=='305','in0','FFEF')
 else:state('persistent other-player punch','MK2_SC_IO ',lambda q:q['frame']=='305','in0','EFFF')
 # Actual viewport-world mutations must fail the source-derived position gate.
 exit_at=good['actualUIState']['exit']
 object_line=next(l for l in text.splitlines()if l.startswith('MK2_UI_LADDER_OBJECT ')and 'xraw=010A0000 'in l and
  exit_at+2<=int(dict(re.findall(r'(\w+)=([^\s]+)',l))['frame'])<=exit_at+100)
 for label,key,value in [('wrong tower world Y','yraw','00000000'),('false native object birth','born','1'),('false tower identity','id','1')]:
  bad=re.sub(r'\b'+key+r'=\S+',key+'='+value,object_line,count=1)
  reject(label,lambda bad=bad:contract.render(folder,text.replace(object_line,bad,1),target,side,load=load))
 css=good['actualUIState']['css'];snaps=contract.model.records(text,'SNAP')
 sample=next(q for q in snaps if q['scene']=='select'and 54<=int(q['age'])<=70)
 sample_name=sample['file'];a=load(sample_name);left=19 if target=='kano'else 319
 def raster(label,changed):
  need(not np.array_equal(changed,a),'Effective whole native image mutation')
  reject(label,lambda:contract.render(folder,text,target,side,load=lambda name:changed if name==sample_name else load(name)))
 b=a.copy();b[20:98,left:left+63]=np.roll(b[20:98,left:left+63],1,axis=1);raster('one-pixel cursor shift',b)
 b=a.copy();b[20:24,left:left+63]=0;raster('thin/missing native border',b)
 b=a.copy();y1,y2=(30,56)if side==1 else(62,87);b[y1:y2,left+24:left+40]=0;raster('missing actual player number',b)
 # Source matching of the whole name shadow is checked in the restored positive.
 need(contract.gate(text,fighter,side,target)==good,'All actual state/IO positives restored')
 restored=contract.render(folder,text,target,side,load=load);need(restored==pixels,'All whole native raster positives restored')
 pins=dict(old['inputHashes'])
 for p in (*contract.DEPENDENCIES,Path(__file__),*folder.rglob('*')):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 result=dict(passed=True,nativeCapture=str(folder),preservedOriginalReportSHA256=sha(folder/'report.json'),
  preservedOriginalPassed=old['passed'],actualSinglePlayerContinue=good,actualUIPixels=pixels,
  actualFaultsRejected=faults,actualGuestGFXProofs=old['actualGuestGFXProofs'],
  actualFullRGBDigests=old['actualFullRGBDigests'],nativeIdentity=old['nativeIdentity'],inputHashes=pins,
  correctedEarlierHostExpectation='IO callbacks are exactly0..terminal-1; boot frame0 is present, not an omitted game field',
  offscreenIconRasterNotClaimed=True,fullPortAcceptance=False,goalStatus='active',newBuilds=0,newROMCopies=0,
  inspectionPNGs=[str(p)for p in folder.glob('*.png')])
 out.mkdir();path=out/'report.json';path.write_text(json.dumps(result,indent=2)+'\n')
 before=sha(path);need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==before,'Lossless report compression')
 print(json.dumps(dict(passed=True,case=f'{fighter} P{side} to {target}',faults=len(faults),pixels=pixels)),flush=True)
 return result
