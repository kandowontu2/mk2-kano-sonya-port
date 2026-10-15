"""Current Jax head-clap: full original earned grammar, native scenes/FIFO/shadows.

Four own-character/physical-slot contexts, normal Dead Pool only. Preserve
the entire original state algorithm and generic source FIFO contract. Verify
all immutable input files separately so private row fault trials need not
rehash unchanged large executable files. Full audio/arenas/port remain open.
"""
import copy,inspect,json,re,struct
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_jax_clap_earned_v4038 as earned
import verify_jax_clap_native_fifo_v4040 as fifo
import verify_kung_lao_split_earned_grammar_v3998 as row_parser
import qualify_current_kitana_scene_v6116 as refill_source
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6138_current_jax_clap_scene_checked'
CONTEXTS=(('kano',1),('kano',2),('sonya',1),('sonya',2))
CASES=tuple(f'audit_v6135_current_jax_clap_{f}_p{s}_native_scene_ram'for f,s in CONTEXTS)

def make_gate(guest):
 earned.capture.NAME=current.NAME
 source=inspect.getsource(earned.make_gate)
 before="'91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24'"
 need(source.count(before)==1,'One declared current payload provenance adaptation')
 source=source.replace(before,'(current.PAYLOAD_SHA)')
 scope=dict(vars(earned),CASES=CASES,current=current,__file__=__file__)
 exec(compile(source,__file__+'::whole_original_earned_constructor','exec'),scope)
 return scope['make_gate'](guest)

def run():
 guest=current.expected();earned.source_contract(guest);payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 pins={str(Path(__file__).resolve()):sha(__file__)}
 for module in(current,earned,fifo,fifo.old,fifo.old.shadow,row_parser,refill_source):pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 texts={case:(ROOT/case/'run.log').read_text()for case in CASES}
 gate=make_gate(guest);positive=gate(texts=texts,check_files=False)
 need(positive['passed'],'Entire original current Jax earned grammar '+repr(positive['errors']))
 contract=fifo.make_contract();cases=[];semantic_faults=[]
 for (fighter,side),case in zip(CONTEXTS,CASES):
  folder=ROOT/case;rp=ROOT/f'audit_v6136_current_jax_clap_{fighter}_p{side}_scene_observed/report.json'
  observed=json.loads(rp.read_text());meta=json.loads((folder/'result.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
  need(observed['passed']and observed['candidate']==meta['candidate']==current.NAME and
       meta['exit_code']==terminal['nativeExit']==0 and meta['ramGuestSHA256']==current.GUEST_SHA and
       not meta['modelErrors']and observed['actualContinuousNativeSceneAccepted']and observed['originalJaxSourceAccepted']and
       observed['actualNativeHeldWinnerPageAfterPointersClear']and observed['postRetirementNewVictimFIFO']==0 and
       observed['postRetirementNewRender']is False and observed['newSourceDirectoryCopies']==0,
       'Actual current native terminal, full guest and complete unweakened scene replay')
  process=json.loads((folder/'process.json').read_text());wi=terminal['actualWindowsIdentity']
  need(process['actualWindowsIdentity']==wi and process['pid']==terminal['pid']==wi['ProcessId']and wi['CreationDate']and
       wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
       str(folder)in wi['CommandLine'],'Actual Windows creation/executable/full-command terminal identity')
  need(meta['input_hashes']==json.loads((folder/'input_hashes_before.json').read_text()),'Whole actual preboot input ledger')
  for p,h in meta['input_hashes'].items():need(sha(p)==h,'Every executed input unchanged');pins[p]=h
  text=texts[case];need((folder/'stderr.log').read_text()==''and not re.search('LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS',text,re.I),'No native/observer fault')
  rs=row_parser.rows(text);refill=refill_source.refill(rs,side,guest)
  g=fifo.parsed(text);identity=17 if fighter=='kano'else 18;projection=contract(g,guest,payload,identity,side)
  records=json.loads((folder/'continuous_scene_records.json').read_text());rgb=json.loads((folder/'visible_digests.json').read_text())
  origin,end=projection['origin'],projection['disappearance'];later=[r for r in records if r['frame']>=end+3]
  need(len(records)==meta['observedRGBFields']==meta['modelExactFields']==observed['exactFields']and
       [r['frame']for r in records]==list(range(origin+1,end+31))and len(rgb)==len(records)and
       all(v['file']==f"display_{r['frame']}.png"and v['rgbSHA256']==r['rgbSHA256']for v,r in zip(rgb,records)),
       'Every consecutive actual whole-native scene RGB/VRAM target source-bound')
  need(later and all(not r['modeledFlip']and r['rgbSHA256']==records[end-origin-1]['rgbSHA256']for r in later),
       'Actual original held final winner page, no artificial erase or post-retirement rendering')
  faults=[]
  def state_fault(label,tag,key,value,chosen=None):
   lines=text.splitlines();indices=[i for i,l in enumerate(lines)if l.startswith('MK2_STOCK_HEAD_V921_'+tag+' ')and(chosen is None or all(token in l.split()for token in chosen.split()))]
   need(indices,'Actual executed state row exists '+label);i=indices[0]
   changed,n=re.subn(r'\b'+key+r'=\S+',key+'='+str(value),lines[i],count=1)
   need(n==1 and changed!=lines[i],'Non-vacuous actual state fault');lines[i]=changed
   damaged=dict(texts);damaged[case]='\n'.join(lines)+'\n'
   negative=gate(texts=damaged,check_files=False)
   if label.startswith('refill_'):
    try:refill_source.refill(row_parser.rows(damaged[case]),side,guest)
    except(ValueError,KeyError,AssertionError):faults.append(label);return
    raise ValueError('Actual native refill fault accepted '+label)
   need(not negative['passed'],'Actual original state fault rejected '+label);faults.append(label)
  for label,tag,key,value in [('proxy_identity','FIRST_LIVE','ids','11,1'),('wrong_action','ACTION','address','FF8C6040'),
   ('fabricated_damage','ACTION','damage','321'),('wrong_wrap_age','WRAP','age','187'),('wrong_wrap_pc','WRAP','pc','FFF00000'),
   ('fabricated_terminal','RESULT','wins','3'),('wrong_spacing','APPROACH','gap','100'),('wrong_health_writer','HEALTH','pc','FFF00000')]:state_fault(label,tag,key,value)
  state_fault('refill_sentinel','HEALTH','after',65534,f"frame={refill['startFrame']} before=161 after=65535")
  state_fault('refill_value','HEALTH','after',7,f"frame={refill['startFrame']+1} before=4 after=6")
  oi=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and r['pose']in fifo.capture.death_art.GROUPS[fighter]);q=g['FLOOR_QUEUE'][oi];key=q['frame'],q['cursor']
  trials=[('proxy_fifo','FLOOR_QUEUE',oi,'id',1),('wrong_owner','FLOOR_QUEUE',oi,'owner',0),('wrong_main','FLOOR_QUEUE',oi,'main',0),
          ('wrong_cache','FLOOR_QUEUE',oi,'row',0),('wrong_art_source','FLOOR_QUEUE',oi,'source',0),('shifted_body','FLOOR_QUEUE',oi,'xy',q['xy']^1)]
  i=next(i for i,r in enumerate(g['FLOOR_QUEUE_TRANSFORM'])if(r['frame'],r['cursor'])==key)
  trials.extend([('shifted_camera','FLOOR_QUEUE_TRANSFORM',i,'camera',g['FLOOR_QUEUE_TRANSFORM'][i]['camera']^1),('floating_floor','FLOOR_QUEUE_TRANSFORM',i,'floor',q['floor']+1)])
  i=next(i for i,r in enumerate(g['FLOOR_QUEUE_PART'])if(r['frame'],r['cursor'])==key);trials.append(('wrong_art_width','FLOOR_QUEUE_PART',i,'width',g['FLOOR_QUEUE_PART'][i]['width']+1))
  i=next(i for i,r in enumerate(g['FLOOR_QUEUE_DISPATCH'])if r['slot']==side);trials.append(('wrong_consumer','FLOOR_QUEUE_DISPATCH',i,'slot',3-side))
  trials.extend([('wrong_pointer_teardown','FLOOR_RETIRED',0,'p1',1),('wrong_live_roster','FLOOR_STATE',0,f'roster{side}',1)])
  component=g['SHADOW_COMPONENT'][0]
  trials.extend([('wrong_shadow_owner','SHADOW_COMPONENT',0,'owner',0),('wrong_shadow_source','SHADOW_COMPONENT',0,'first_source',component['first_source']^1)])
  i=next(i for i,r in enumerate(g['FLOOR_DMA'])if r['event']==component['event']);trials.append(('wrong_shadow_caller','FLOOR_DMA',i,'pc',0))
  for label,tag,index,key,value in trials:
   changed=copy.deepcopy(g);need(changed[tag][index][key]!=value,'Actual non-vacuous FIFO/shadow fault');changed[tag][index][key]=value
   try:contract(changed,guest,payload,identity,side)
   except(ValueError,KeyError,AssertionError):faults.append(label)
   else:raise ValueError('Actual FIFO/shadow fault accepted '+label)
  need(contract(g,guest,payload,identity,side)==projection and gate(texts=texts,check_files=False)==positive and
       refill_source.refill(rs,side,guest)==refill,'Entire actual original state/FIFO/refill restored')
  reviews=list((folder/'review').glob('*.png'));need(len(reviews)==1 and observed['essentialNativeReviewPNGsWritten']==1,'One bounded actual seven-phase/post-match review')
  need(not list(folder.glob('*.bin'))and not list(folder.glob('*.wav'))and not(folder/'input_sources').exists(),'No raw media or duplicate source tree')
  need(len(observed['rejectedActualPixelTargetFaults'])==2,'Both actual native VRAM and fullscreen RGB corruptions rejected')
  for p in folder.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
  pins[str(rp)]=sha(rp);semantic_faults+=faults
  cases.append(dict(fighter=fighter,side=side,exactFields=len(records),actualWindowsTerminal=terminal,
       actualEarnedState=positive['cases'][case],nativeRefill=refill,nativeFIFO=projection,nativeReview=str(reviews[0]),
       actualSemanticFaultsRejected=faults,postRetirementNewRender=False))
  print(f'Qualified current Jax head-clap {fighter}P{side}: {len(records)} native fields / {len(faults)} semantic faults',flush=True)
 need(all(sha(p)==h for p,h in pins.items()),'All executed source/native evidence unchanged')
 return dict(passed=True,candidate=current.NAME,cases=cases,inputHashes=pins,actualContexts=4,
     exactNativeFields=sum(c['exactFields']for c in cases),exactRGBPixels=sum(c['exactFields']for c in cases)*400*254,
     actualSemanticFaultsRejected=len(semantic_faults),actualNativePixelTargetFaultsRejected=8,
     currentEarnedClapStateFullSceneFIFOProjectionGroundingShadowAndCleanupAccepted=True,
     artAestheticReviewPending=True,fullAudioAcceptance=False,fullPortAcceptance=False,
     newBuildCopies=0,newSourceDirectoryCopies=0,nativeGameChanges=0,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh complete current head-clap matrix')
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
