"""Actual scheduled-Shao lookup/descriptor/damage provenance under unchanged inputs.
Animation/pose addresses alone are not treated as semantic attack names.
An exact replay is not independent strategy coverage or a new full-port gate.
"""
import argparse,copy,json,re,struct,traceback
from pathlib import Path
from collections import Counter,defaultdict
import verify_current_shao_guard_walk_boss_ledger_v2551 as ledger
import verify_shao_descriptor_observer_boundary_v2567 as source
ROOT=ledger.ROOT;launch=ledger.launch;native=ledger.native
native.HEX|={'sp','descriptor','damage_word','a10'}
NEW_TAGS={'CPU_COLLISION_ENTRY','CPU_COLLISION_RETURN','CPU_DAMAGE_CONTEXT'}

def need(ok,label):
 if not ok:raise ValueError(label)

def legacy(raw):
 return[line for line in raw.splitlines()if line.startswith('MK2_NAT_CAMPAIGN_')and not any(line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')for tag in NEW_TAGS)]

def exact(a,b):need(a==b,'Every original native selection/button/state/health/win/progression/ending row byte-exact')

def u32(raw,address):return struct.unpack_from('<I',raw,(address-0xff800000)//8)[0]
def data(raw,address,bits):return raw[(address-0xff800000)//8:(address+bits-0xff800000)//8]

def check(rows,descriptors):
 fields={r['frame']:r for r in rows if r['tag']=='BOSS_FIELD'and r['stage']==16}
 entries={};returns={};contexts=[]
 def common(r):
  need(r['human_slot']==1 and r['fighter']=='kano'and r['writes']==0 and r['assistance']=='none'and r['stage']==16,'Actual diagnostic scope remains physical Kano P1, no writes or assistance')
  f=fields.get(r['frame']);need(f is not None,'Actual positive-health scheduled Shao field')
  need(r['id']==r['roster']==13 and r['owner']==r['actor']==f['cpu_actor']and r['main']==f['cpu_main'],'Actual scheduled native Shao actor/Main/ID provenance')
  need(r['stack_valid']in(0,1),'Explicit actual native stack validity')
  if r['stack_valid']:
   need(0x01000000<=r['sp']and r['sp']+6*32<=0x01100000 and re.fullmatch(r'[0-9A-F]{8}(,[0-9A-F]{8}){5}',str(r['stack'])),'Bounded actual six-word native stack; not invented call sites')
  else:need(r['stack']=='unavailable','Invalid stack is not interpreted')
  return f
 for r in rows:
  if r['tag']not in NEW_TAGS:continue
  f=common(r)
  if r['tag']in('CPU_COLLISION_ENTRY','CPU_COLLISION_RETURN'):
   need(r['a8']==r['actor']and r['a13']==r['main'],'Actual scheduled native Shao registers/actor/Main')
   need(r['selector']in descriptors,'Actual original Shao collision selector and descriptor match')
   if r['tag']=='CPU_COLLISION_ENTRY':
    need(r['entry']==0xff8eb9e0 and r['pc']==0xff8eb9f0 and r['serial']not in entries,'Unique actual native collision-selector instruction')
    entries[r['serial']]=r
   else:
    need(r['entry']==0xff8eba80 and r['pc']==0xff8eba90 and r['serial']not in returns,'Unique actual native descriptor-return instruction')
    e=entries.get(r['serial']);need(e is not None and e['event']<r['event']and all(e[k]==r[k]for k in('frame','actor','main','selector')),'Coherent ordered actual lookup entry/return pair')
    wanted=descriptors[r['selector']]
    need(r['descriptor']==wanted['address'],'Actual original Shao collision selector and descriptor match')
    need(r['damage_word']==wanted['damageWord'],'Actual returned descriptor word equals immutable original ROM')
    returns[r['serial']]=r
  else:
   need(r['at']==0x010602f0 and r['slot']==1 and r['pc']==0xff836700 and r['mask']==0xffff and 0<=r['after']<r['before']<=161,'Actual original own combat health store')
   need(r['scheduled_writer']==int(r['a8']==r['actor']and r['a13']==r['main']),'Actual writer/scheduled-boss register classification')
   need(0<r['a10']<=161 and r['before']-r['after']==min(r['before'],r['a10']),'Actual native effective damage and clipping agree with health store')
   if r['serial']:
    d=returns.get(r['serial']);need(d is not None and d['event']<r['event']and all(d[k]==r[k]for k in('frame','selector','descriptor'))and d['actor']==r['a8']and d['main']==r['a13'],'Owned same-field actual returned descriptor precedes damage')
    word=d['damage_word'];need(r['a10']in(word&255,word>>8),'Actual effective damage is an original full/blocked descriptor value, not appended-ID scaling')
   else:need(r['selector']==-1 and r['descriptor']==0,'Unattributed damage is explicitly unassigned, never guessed from a pose')
   contexts.append(r)
 need(entries and set(entries)==set(returns)and sorted(entries)==list(range(1,len(entries)+1)),'Complete consecutive actual native lookup entry/return pairs')
 health=[r for r in rows if r['tag']=='HEALTH'and r['frame']in fields and r['slot']==1 and r['pc']==0xff836700 and r['after']<r['before']]
 key=lambda r:tuple(r[k]for k in('frame','slot','at','pc','before','after','a8','a13'))
 need(Counter(map(key,health))==Counter(map(key,contexts)),'Every actual Shao-stage own health decrement has exactly one matching context')
 inputs=defaultdict(set)
 for r in rows:
  if r['tag']=='INPUT'and r['frame']in fields:inputs[r['frame']].add(r['button'])
 groups={};examples=[]
 for r in contexts:
  f=fields[r['frame']];index=r['selector'];name='descriptor_'+str(index)if r['serial']else'unattributed'
  group=groups.setdefault(name,dict(lookupSelector=index if r['serial']else None,stores=0,damage=0,effectiveDamageHistogram=Counter(),actualCPUPoses=Counter(),physicalBlockHeldStores=0))
  group['stores']+=1;group['damage']+=r['before']-r['after'];group['effectiveDamageHistogram'][str(r['a10'])]+=1;group['actualCPUPoses'][f"{f['cpu_pose']:08X}"]+=1;group['physicalBlockHeldStores']+='Block'in inputs[r['frame']]
  if len(examples)<16:examples.append(dict(r,preInputCPUField={k:f[k]for k in('gap','cpu_pose','cpu_action','cpu_flags','cpu_body','cpu_height')},physicalInputs=sorted(inputs[r['frame']])))
 return dict(actualLookupPairs=len(entries),actualIncomingDamageContexts=len(contexts),actualIncomingDamage=sum(r['before']-r['after']for r in contexts),
  actualAttributedContexts=sum(bool(r['serial'])for r in contexts),actualUnattributedContexts=sum(not r['serial']for r in contexts),groups=groups,examples=examples),entries,returns,contexts

def verify(folder):
 pins={}
 def accept(path):
  r=json.loads(path.read_text());need(r['passed']and not r['fullPortAcceptance'],'Accepted actual bounded evidence '+str(path))
  for file,wanted in r['inputHashes'].items():
   if file in pins:need(pins[file]==wanted,'Consistent actual graph')
   else:need(launch.sha(file)==wanted,'Unchanged accepted source/capture '+file);pins[file]=wanted
  pins[str(path)]=launch.sha(path);return r
 bound=accept(ROOT/'audit_v2569_shao_descriptor_observer_boundary_checked/report.json')
 need(bound['physicalInputsUnchanged']and bound['fullReadOnlyObserverInverse']and len(bound['rejectedSpecificSourceCounterexamples'])==5,'Whole original controller plus five read-only/source negatives')
 baseline=ROOT/'audit_v2543_current_kano_p1_shao_guard_walk_campaign'
 old_proof=accept(ROOT/'audit_v2544_current_kano_p1_shao_guard_walk_checked/report.json')
 book=accept(ROOT/'audit_v2556_current_kano_shao_guard_walk_boss_ledger_checked/report.json')
 negative=accept(ROOT/'audit_v2557_current_kano_shao_guard_walk_input_counterexamples/report.json')
 progress=accept(ROOT/'audit_v2558_current_kano_shao_guard_walk_progress/report.json')
 need(book['rejectedSpecificCounterexamples']==8 and negative['rejectedSpecificCounterexamples']==29 and len(progress['rejectedSpecificPrefixCounterexamples'])==3,'Entire original accepted physical trajectory, ordered ledger and input controls')
 before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'));meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
 old_meta=json.loads((baseline/'result.json').read_text(encoding='utf-8-sig'))
 need(meta['exit_code']==0 and meta['input_hashes']==before,'Matched terminal actual read-only capture')
 for key in('candidate','executable_sha256','payload_sha256','player','human_slot','cpu_slot','boot_frame','seconds','strategy','boss_policy','assistance','cheats_enabled'):
  need(meta[key]==old_meta[key],'Entire actual current build/physical launch contract unchanged '+key)
 for file,wanted in before.items():
  need(launch.sha(file)==wanted,'Executed current input unchanged');pins[file]=wanted
  if Path(file).suffix in('.lua','.ps1','.json'):
   frozen=folder/'input_sources'/Path(file).name;need(launch.sha(frozen)==wanted,'Frozen executed observer/launcher unchanged');pins[str(frozen.resolve())]=wanted
 harness=folder/'input_sources/mk2ks_natural_campaign_boss_shao_descriptor_observed_v2565.lua'
 source.restore(harness.read_text().rstrip()+'\n')
 runner=folder/'input_sources/run_current_boss_shao_descriptor_observed_v2566.ps1'
 restored=runner.read_text().replace('mk2ks_natural_campaign_boss_shao_descriptor_observed_v2565','mk2ks_natural_campaign_boss_shao_guard_walk_v2540')
 need(restored.rstrip()+'\n'==(ROOT/'tools/run_current_boss_shao_guard_walk_v2541.ps1').read_text().rstrip()+'\n','Full physical launcher unchanged except read-only observer')
 raw=(folder/'run.log').read_text(encoding='utf-8-sig');old_raw=(baseline/'run.log').read_text(encoding='utf-8-sig')
 need(not re.search(r'LUA ERROR|Lua error|fatal error|stack traceback|access violation|WRONG CHECKSUMS|might not run correctly',raw,re.I),'No runtime/observer/source errors')
 old_lines=legacy(old_raw);observed_lines=legacy(raw);exact(old_lines,observed_lines)
 failures=[];index=next(i for i,l in enumerate(old_lines)if l.startswith('MK2_NAT_CAMPAIGN_BOSS_FIELD '))
 for name in('missing_native_field','changed_actual_ID','changed_actual_health'):
  changed=list(observed_lines)
  if name=='missing_native_field':changed.pop(index)
  elif name=='changed_actual_ID':changed[index]=changed[index].replace('human_id=17','human_id=1',1)
  else:changed[index]=re.sub(r' health=(\d+),',lambda m:' health='+str(int(m[1])-1)+',',changed[index],count=1)
  need(changed!=observed_lines,'Non-vacuous unchanged-trajectory control')
  try:exact(old_lines,changed)
  except ValueError as error:failures.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Changed native trajectory accepted')
 exact(old_lines,observed_lines)
 guest,previous,payload=launch.current.expected();need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actual current guest independently reconstructed')
 original_path=ROOT/'mk2/mk2-maincpu.bin';original=original_path.read_bytes();row=u32(original,0xff8eba90+13*32)
 need(u32(guest,u32(guest,0xff8eba30)+13*32)==row and data(guest,row,160)==data(original,row,160),'All five scheduled-Shao collision descriptor pointers byte-exact original')
 descriptors={}
 for i in range(5):
  address=u32(original,row+i*32);need(data(guest,address,144)==data(original,address,144),'Entire original Shao descriptor unchanged')
  words=struct.unpack('<9H',data(original,address,144));descriptors[i]=dict(address=address,damageWord=words[5],fullDamage=words[5]>>8,blockedDamage=words[5]&255,words=list(words))
 rows=native.parse(raw,1,'kano');ledger.check(rows,17,1);control,entries,returns,contexts=check(rows,descriptors)
 need(control['actualIncomingDamage']==progress['actualShaoIncomingDamage'],'Actual new descriptor/damage inventory reconciles with complete unchanged original run')
 indices={r['event']:i for i,r in enumerate(rows)};first_entry=next(iter(entries.values()));first_return=next(iter(returns.values()));first_context=next(r for r in contexts if r['serial'])
 mutations=[('wrong_Shao_lookup_selector',indices[first_entry['event']],'selector',5,'Actual original Shao collision selector'),
  ('foreign_Shao_register',indices[first_entry['event']],'a8',first_entry['a8']+16,'Actual scheduled native Shao registers'),
  ('wrong_returned_descriptor',indices[first_return['event']],'descriptor',first_return['descriptor']+16,'Actual original Shao collision selector'),
  ('changed_original_damage_word',indices[first_return['event']],'damage_word',first_return['damage_word']^1,'Actual returned descriptor word'),
  ('wrong_effective_damage',indices[first_context['event']],'a10',first_context['a10']+1,'Actual native effective damage'),
  ('missing_actual_damage_context',indices[first_context['event']],None,None,'Every actual Shao-stage own health decrement')]
 for name,index,key,value,label in mutations:
  changed=copy.deepcopy(rows)
  if key is None:changed.pop(index)
  else:changed[index][key]=value
  try:check(changed,descriptors)
  except ValueError as error:need(label in str(error),'Specific native provenance rejection '+str(error));failures.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Corrupted native descriptor/damage context accepted '+name)
 need(check(rows,descriptors)[0]==control,'Final untouched complete native descriptor control')
 for p in folder.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=launch.sha(p)
 pins[str(original_path)]=launch.sha(original_path);pins[str(Path(__file__).resolve())]=launch.sha(__file__);launch.module_pins(pins)
 return dict(passed=True,**control,originalDescriptors=descriptors,exactUnchangedNativeRows=len(old_lines),onlyThreeReadOnlyTagsExcluded=True,
  rejectedSpecificCounterexamples=failures,physicalInputsUnchanged=True,wholeGuestReconstructed=True,captureModified=False,gameChanged=False,
  exactReplayNotIndependentStrategyContext=True,unassisted_clear_proven=old_proof['unassisted_clear_proven'],fullPortAcceptance=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable actual descriptor provenance')
 try:r=verify(a.folder)
 except Exception as error:r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),gameChanged=False,fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k not in('inputHashes','examples')},indent=2),flush=True)
 raise SystemExit(0 if r['passed']else 1)
