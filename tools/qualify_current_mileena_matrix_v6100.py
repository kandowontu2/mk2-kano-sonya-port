"""Qualify four current earned swallowing runs and every retained physical field.

Preserve failed observer reports. Source-native sentinel handling is complete;
no runtime mutation, new boot, raw media or build copy. Bounded native Sonya P2
phase PNGs are inspection evidence, not whole-scene artwork/audio acceptance.
"""
import copy, hashlib, json, re, struct
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import current_mileena_global_refill_v6093 as health
import verify_mileena_fixed_runtime_v3829 as original

ROOT, need, sha = current.ROOT, current.need, current.sha
OUT = ROOT/'audit_v6101_current_mileena_matrix_checked'
CONTEXTS = (
 ('kano',1,'audit_v6083_current_mileena_kano_p1'),
 ('kano',2,'audit_v6088_current_mileena_kano_p2'),
 ('sonya',1,'audit_v6088_current_mileena_sonya_p1'),
 ('sonya',2,'audit_v6096_current_mileena_sonya_p2'),
)
HEX = {'actor','main','owner','pose','xraw','yraw','flags','body','bank'}

def fields(text):
 result=[]
 for line in text.splitlines():
  if not line.startswith('MK2_CURRENT_MILEENA_FIELD '): continue
  row=dict(re.findall(r'(\w+)=([^\s]+)',line))
  result.append({k:int(v,16)if k in HEX else int(v)if re.fullmatch(r'-?\d+',v)else v for k,v in row.items()})
 need('MK2_CURRENT_MILEENA_NO_ACTOR 'not in text,'No omitted physical actor lifecycle fields in these four runs')
 return result

def physical_gate(rows, physical, fighter, side, guest):
 state=health.gate(rows,fighter,side,guest)
 need(state['passed'],repr(state))
 identity=17 if fighter=='kano'else 18
 first=next(r['frame']for r in rows if r['tag']=='FIRST_LIVE')
 terminal=next(r['frame']for r in rows if r['tag']=='HOST_EXIT'and r['kind']=='MILEENA_V3784')
 need([(r['frame'],r['slot'])for r in physical]==[(f,s)for f in range(first,terminal)for s in (1,2)],
      'Every paired frame from first actual combat through native terminal, no lifecycle gaps')
 for r in physical:
  need(r['roster']==r['id']==(identity if r['slot']==side else 5)and
       r['owner']==r['actor']and 0x01000000<=r['actor']<0x01100000 and
       0x01000000<=r['main']<0x01100000 and r['writes']==0 and r['assistance']=='none'and
       0<=r['hp']<=161,'True physical roster/state identity, valid ownership and health in every native field')
 own=[r for r in physical if r['slot']==side]
 byframe={r['frame']:r for r in own}
 start,end=state['lookupFrame'],state['disappearanceFrame']
 index0=0 if identity==17 else 7
 for f in range(start,end):
  r=byframe[f];group=0xffd61000+(index0+(f-start)//4)*64
  need(r['pose']==group and r['actor']==int(state['physicalActor'],16)and
       r['main']==int(state['physicalMain'],16)and r['flags']&0x30==0x10 and
       r['hp']==0 and r['floor']==(82 if identity==17 else 81),
       'Every owned swallowing pose field, stable true actor/task/floor and native visibility')
 before=byframe[end-1]['flags'];after=byframe[end]['flags']
 need(after==((before|0x20)&~0x10),'Exact original disappearance OR20/AND-not10 flag transition')
 for r in own:
  if r['frame']>=end:
   need(r['flags']&0x30==0x20 and r['hp']==0 and
        r['actor']==int(state['physicalActor'],16)and r['main']==int(state['physicalMain'],16),
        'Retired victim remains hidden without resurrection through complete post-finisher window')
 need(any(r['mode']==5 and r['frame']>end for r in physical),'Actual ordinary post-match mode reached')
 return dict(nativeState=state,pairedPhysicalFields=len(physical),ownSwallowingFields=end-start,
             postDisappearanceHiddenFields=terminal-end)

def rejected(rows, physical, fighter, side, guest):
 names=[]
 faults=[('proxy_id','EATEN_TASK','id',1),('wrong_owner','EATEN_TASK','a8',0x01032130),
 ('old_lookup','ROW','a1',0xff9e9140),('wrong_stream','ROW','data',0),('wrong_lookup_pc','ROW','pc',0xff906130),
 ('unearned_damage','ACTION','damage',161),('wrong_cadence','GROUP','frame',0),
 ('wrong_group','GROUP','a0',0xff9e9520),('wrong_descriptor','GROUP','group','FFBFE0C0,00000000'),
 ('wrong_disappearance_pc','DISAPPEAR','pc',0),('wrong_disappearance_owner','DISAPPEAR','a0',0),
 ('bad_cache_exit','RESULT','bad_frame',223502),('invalid_health','HEALTH','after',32383)]
 def must_reject(name,rr,pp):
  try: physical_gate(rr,pp,fighter,side,guest)
  except (AssertionError,RuntimeError): names.append(name);return
  raise AssertionError('Actual semantic counterexample not rejected: '+name)
 for name,tag,key,value in faults:
  rr=copy.deepcopy(rows)
  target=next(r for r in rr if r['tag']==tag and(tag!='GROUP'or 0xffd61000<=r['a0']<0xffd613c0)and
              (tag!='RESULT'or r['kind']=='CACHE_V3780'))
  target[key]=value;must_reject(name,rr,physical)
 state=health.gate(rows,fighter,side,guest);refill=state['nativeInterRoundRefill']['startFrame']
 for name,key,value in [('refill_sentinel','after',65534),('refill_writer','pc',0xff838860),
                       ('refill_register_context','a8',0x01032130)]:
  rr=copy.deepcopy(rows);next(r for r in rr if r['tag']=='HEALTH'and r['frame']==refill and r['after']==65535)[key]=value
  must_reject(name,rr,physical)
 rr=copy.deepcopy(rows);next(r for r in rr if r['tag']=='HEALTH'and r['frame']==refill+1 and r['after']==6)['frame']+=1
 must_reject('refill_field_cadence',rr,physical)
 for name,at,key,value in [('physical_proxy',state['lookupFrame'],'id',1),
  ('owned_phase_pose',state['lookupFrame']+1,'pose',0xff9e9520),
  ('victim_resurrection',state['disappearanceFrame']+10,'flags',0x16)]:
  pp=copy.deepcopy(physical);next(r for r in pp if r['slot']==side and r['frame']==at)[key]=value
  must_reject(name,rows,pp)
 must_reject('missing_physical_field',rows,physical[1:])
 physical_gate(rows,physical,fighter,side,guest)
 return names

def run():
 guest=current.expected();stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 lo,hi=0xff838f60,0xff8390a0
 need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==stock[(lo-0xff800000)//8:(hi-0xff800000)//8],
      'Whole original disappearance kernel unchanged, including original flag store and return')
 need(struct.unpack_from('<6H',guest,(0xff838f80-0xff800000)//8)==(0x0ba4,0x20,0,0x0b84,0x10,0),
      'Source independently defines native hidden bit20 and visible bit10 clearing')
 payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 n0,n1=struct.unpack_from('<I',payload,0x1f6008)[0],struct.unpack_from('<I',payload,0x1f6010)[0]
 gfx=payload[0x122000:0x122000+n0]+payload[0x154000:0x154000+n1]
 expected={'GUEST':(1048576,current.GUEST_SHA),'GFX':(len(gfx),hashlib.sha256(gfx).hexdigest().upper())}
 pins={str(Path(__file__).resolve()):sha(__file__)}
 for module in (current,health,health.prior,original):pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 cases=[]
 for fighter,side,leaf in CONTEXTS:
  folder=ROOT/leaf;terminal=json.loads((folder/'native_terminal.json').read_text());process=json.loads((folder/'process.json').read_text())
  identity=terminal['actualWindowsIdentity']
  need(terminal['nativeExit']==0 and terminal['pid']==process['pid']==identity['ProcessId']and
       identity==process['actualWindowsIdentity']and identity['Name']=='mkport_candidate.exe'and
       Path(identity['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
       all(str(p)in identity['CommandLine']for p in (ROOT/current.NAME,folder)),'Actual recorded native terminal creation/executable/command identity')
  text=(folder/'run.log').read_text();need((folder/'stderr.log').read_text()==''and
       not re.search('LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS|TRANSPORT_ERROR',text,re.I),'Warning-free terminal and complete transport')
  proof=json.loads((folder/'memory_proofs.json').read_text())
  need(set(proof)==set(expected)and all(proof[k]['bytes']==n and proof[k]['sha256']==h and
       proof[k]['everyActualByteComparedInRAM']for k,(n,h)in expected.items()),'All actual guest and swallowing GFX bytes source-bound at native boot')
  before=folder/'input_hashes_before.json'
  if before.exists():
   executed=json.loads(before.read_text());need(all(sha(p)==h for p,h in executed.items()),'All recorded preboot source pins still unchanged');pins.update(executed)
  rows=original.parse(text);physical=fields(text);positive=physical_gate(rows,physical,fighter,side,guest)
  faults=rejected(rows,physical,fighter,side,guest)
  scenes=json.loads((folder/'scene_proofs.json').read_text())
  need(all(sha(s['path'])==s['pngSHA256']and s['frame']==positive['nativeState']['actionFrame']+s['age']for s in scenes),'Actual bounded PNG hashes and exact capture fields')
  if fighter=='sonya'and side==2:
   state=positive['nativeState'];need([s['age']for s in scenes]==[0]+[state['lookupFrame']-state['actionFrame']+i*4 for i in range(8)]+[600],
       'All eight Sonya P2 swallowing phases captured from actual lookup, not guessed action ages')
  else:need([s['age']for s in scenes]==[0,8,16,24,32,64,128,600],'Original generic screenshots retained, not miscredited as swallowing phase raster')
  for p in folder.iterdir():
   if p.is_file():pins[str(p.resolve())]=sha(p)
  cases.append(dict(fighter=fighter,victimSlot=side,capture=str(folder),actualTerminal=terminal,
       **positive,actualSemanticFaultsRejected=faults,storedPrebootPinLedgerAvailable=before.exists(),
       nativeSwallowingPhaseScreensAvailable=fighter=='sonya'and side==2))
 need(all(sha(p)==h for p,h in pins.items()),'Complete captured inputs/evidence immutable')
 return dict(passed=True,candidate=current.NAME,cases=cases,inputHashes=pins,actualContexts=4,
     earnedRoundKOs=8,ownSwallowingPoses=sum(c['nativeState']['poseCount']for c in cases),
     nativeRefillStores=sum(c['nativeState']['nativeInterRoundRefill']['actualStores']for c in cases),
     pairedPhysicalFields=sum(c['pairedPhysicalFields']for c in cases),
     actualSemanticFaultsRejected=sum(len(c['actualSemanticFaultsRejected'])for c in cases),
     completeCurrentEarnedSwallowingStateAndRetirementAccepted=True,
     fullArtAcceptance=False,fullAudioAcceptance=False,fullPortAcceptance=False,
     nativeBootsStarted=0,nativeGameChanges=0,newBuildCopies=0,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh complete current Mileena matrix qualification')
 report=run();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2))
