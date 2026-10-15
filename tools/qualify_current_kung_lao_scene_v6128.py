"""Current earned Kung Lao split: four own victims and two real stock controls.

Retain whole original command/constructor/cursor/mirror/palette/continuation
and native FIFO/projection/shadow contracts. Compare held winner-page behavior
with actual current stock controls, not a proxy-ID or clear-screen workaround.
Full audio, other finishers/arenas and integrated port completion remain open.
"""
import copy,json,re,struct
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import verify_kung_lao_split_native_fifo_v3994 as fifo
import verify_kung_lao_split_earned_grammar_v3998 as grammar
import qualify_current_kitana_scene_v6116 as refill_source
ROOT,need,sha=current.ROOT,current.need,current.sha
OUT=ROOT/'audit_v6129_current_kung_lao_scene_checked'
CONTEXTS=(('kitana',1),('liu_kang',2),('kano',1),('kano',2),('sonya',1),('sonya',2))

def state_gate(rs,fighter,side,guest,payload):
 report=grammar.gate(rs,fighter,side,guest,payload)
 report['nativeInterRoundRefill']=refill_source.refill(rs,side,guest)
 return report

def state_faults(rs,fighter,side,guest,payload):
 positive=state_gate(rs,fighter,side,guest,payload);faults=[]
 def reject(name,changed):
  try:state_gate(changed,fighter,side,guest,payload)
  except (ValueError,KeyError,AssertionError):faults.append(name)
  else:raise ValueError('Actual split state fault accepted '+name)
 trials=[('proxy_id','FIRST_LIVE','ids','0,8'),('foreign_action','ACTION','actor','01000000'),
 ('wrong_health_writer','HEALTH','pc','FF838860'),('wrong_parser','COMPARE','actual','999'),
 ('wrong_row','TABLE_RETURN','value','00000000'),('wrong_palette','PALETTE','pointer','00000000'),
 ('wrong_wrap_owner','WRAP','main','01000000'),('wrong_terminal','RESULT','wins','3')]
 for label,tag,key,value in trials:
  changed=copy.deepcopy(rs)
  target=next(r for r in changed if r['tag']==tag and(tag!='COMPARE'or r['table']==('FF878BF0'if side==1 else'FF878B90'))and
              (tag!='TABLE_RETURN'or r['table']=='FFFDFA00'))
  need(target[key]!=value,'Non-vacuous actual split command/table corruption');target[key]=value;reject(label,changed)
 for label,at,key,value in [('main0_replaced',0xff8cece0,'a9',positive['splitStream']),
  ('secondary_proxy',0xff8cf030,'other_id',8),('wrong_mirror',0xff8cefb0,'flags',0),
  ('wrong_half_cursor',0xff842690,'a9',0),('wrong_cadence',0xff842630,'age',0),('wrong_saved_stack',0xff8426b0,'sp',0)]:
  changed=copy.deepcopy(rs);target=next(r for r in changed if r['tag']=='SPLIT'and r['id']==grammar.IDS[fighter]and r['at']==at)
  need(target[key]!=value,'Non-vacuous native paired constructor corruption');target[key]=value;reject(label,changed)
 at=positive['nativeInterRoundRefill']['startFrame']
 for label,age,value in [('wrong_refill_sentinel',0,'65534'),('wrong_refill_value',1,'7')]:
  changed=copy.deepcopy(rs);target=next(r for r in changed if r['tag']=='HEALTH'and int(r['frame'])==at+age and r['after']==('65535'if age==0 else'6'))
  target['after']=value;reject(label,changed)
 need(state_gate(rs,fighter,side,guest,payload)==positive,'Entire actual constructor/command/refill restored')
 return faults

def fifo_faults(g,guest,payload,identity,side,positive):
 faults=[];oi=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==side and 0xfffdf100<=r['pose']<0xfffdf600)
 q=g['FLOOR_QUEUE'][oi];key=q['frame'],q['cursor']
 trials=[('proxy_id','FLOOR_QUEUE',oi,'id',1),('wrong_owner','FLOOR_QUEUE',oi,'owner',0),
 ('wrong_cached_row','FLOOR_QUEUE',oi,'row',0),('wrong_source','FLOOR_QUEUE',oi,'source',0),
 ('wrong_native_xy','FLOOR_QUEUE',oi,'xy',q['xy']^1)]
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_TRANSFORM'])if(r['frame'],r['cursor'])==key)
 trials.append(('shifted_backdrop_projection','FLOOR_QUEUE_TRANSFORM',i,'camera',g['FLOOR_QUEUE_TRANSFORM'][i]['camera']^1))
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_PART'])if(r['frame'],r['cursor'])==key)
 trials.append(('wrong_art_width','FLOOR_QUEUE_PART',i,'width',g['FLOOR_QUEUE_PART'][i]['width']+1))
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE_DISPATCH'])if r['slot']==side)
 trials.append(('wrong_consumer_slot','FLOOR_QUEUE_DISPATCH',i,'slot',3-side))
 trials.extend([('wrong_teardown_pointer','FLOOR_RETIRED',0,'p1',1),('wrong_live_identity','FLOOR_STATE',0,f'roster{side}',1)])
 i=next(i for i,r in enumerate(g['FLOOR_QUEUE'])if r['slot']==3)
 trials.extend([('secondary_proxy','FLOOR_QUEUE',i,'id',1),('secondary_detached_main','FLOOR_QUEUE',i,'main',0),
                ('secondary_wrong_parent','FLOOR_QUEUE',i,'parent',0)])
 component=g['SHADOW_COMPONENT'][0]
 trials.extend([('wrong_shadow_owner','SHADOW_COMPONENT',0,'owner',0),
                ('wrong_shadow_source','SHADOW_COMPONENT',0,'first_source',component['first_source']^1)])
 i=next(i for i,r in enumerate(g['FLOOR_DMA'])if r['event']==component['event'])
 trials.append(('wrong_shadow_caller','FLOOR_DMA',i,'pc',0))
 for label,tag,index,key,value in trials:
  changed=copy.deepcopy(g);changed[tag][index][key]=value
  try:fifo.contract(changed,guest,payload,identity,side)
  except (ValueError,KeyError,AssertionError):faults.append(label)
  else:raise ValueError('Actual paired FIFO fault accepted '+label)
 need(fifo.contract(g,guest,payload,identity,side)==positive,'Complete actual own paired FIFO restored')
 return faults

def source_gate(guest):
 stock=(ROOT/'mk2/mk2-maincpu.bin').read_bytes();off=lambda a:(a-0xff800000)//8
 kernel=bytearray(stock[off(0xff8ce9f0):off(0xff8cf110)])
 struct.pack_into('<I',kernel,off(0xff8cea70)-off(0xff8ce9f0),0xff800000+0xfbf40*8)
 need(guest[off(0xff8ce9f0):off(0xff8cf110)]==kernel and
      guest[off(0xff842590):off(0xff842710)]==stock[off(0xff842590):off(0xff842710)],
      'Whole native split victim constructor/paired animation unchanged except declared true-ID table operand')
 need(guest[0xfbf40:0xfbf40+17*4]==stock[off(0xff8cf110):off(0xff8cf110)+17*4],'All17original stock victim rows retained')
 for at,value in ((0xff8ceca0,0x5729),(0xff8cefd0,0x4d2b),(0xff842680,0x4d69),(0xff8426c0,0x4d2b)):
  need(struct.unpack_from('<H',stock,off(at))[0]==value,'Independent original seed/restore/cursor instructions')
 need(struct.unpack_from('<I',stock,off(0xff8cecc0))[0]==0xff906090,'Original MAIN0 stance seed call')
 main=bytearray(stock[off(0xff906090):off(0xff906150)]);struct.pack_into('<I',main,2,0xfffe4000)
 need(guest[off(0xff906090):off(0xff906150)]==main and
      guest[off(0xfffe4000):off(0xfffe4000)+17*4]==stock[off(0xff906150):off(0xff906150)+17*4],
      'Whole original MAIN0 selector and17stock roots retained; only declared true-ID extension')

def run():
 guest=current.expected();source_gate(guest);payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 pins={str(Path(__file__).resolve()):sha(__file__)}
 for module in (current,fifo,grammar,fifo.shadow,refill_source):pins[str(Path(module.__file__).resolve())]=sha(module.__file__)
 cases=[];semantics=[]
 for fighter,side in CONTEXTS:
  folder=ROOT/f'audit_v6126_current_kung_lao_{fighter}_p{side}_native_scene_ram'
  reportpath=ROOT/f'audit_v6127_current_kung_lao_{fighter}_p{side}_scene_observed/report.json'
  observed=json.loads(reportpath.read_text());meta=json.loads((folder/'result.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
  need(observed['passed']and observed['candidate']==meta['candidate']==current.NAME and
       meta['exit_code']==terminal['nativeExit']==0 and meta['ramGuestSHA256']==current.GUEST_SHA and
       not meta['modelErrors']and observed['actualContinuousNativeSceneAccepted']and
       observed['actualNativeHeldWinnerPageAfterPointersClear']and observed['postRetirementNewVictimFIFO']==0 and
       observed['postRetirementNewRender']is False and observed['newSourceDirectoryCopies']==0,
       'Actual current native terminal/whole guest and complete unweakened paired scene replay')
  process=json.loads((folder/'process.json').read_text());native_identity=terminal['actualWindowsIdentity']
  need(process['actualWindowsIdentity']==native_identity and process['pid']==terminal['pid']==native_identity['ProcessId']and
       native_identity['Name']=='mkport_candidate.exe'and
       Path(native_identity['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve()and
       str(folder)in native_identity['CommandLine'],'Actual Windows creation/executable/full-command terminal binding')
  need(meta['input_hashes']==json.loads((folder/'input_hashes_before.json').read_text()),'Complete actual preboot input ledger')
  for p,h in meta['input_hashes'].items():need(sha(p)==h,'Every executed native/model input unchanged');pins[p]=h
  text=(folder/'run.log').read_text();need((folder/'stderr.log').read_text()==''and not re.search('LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS',text,re.I),'No native or observer fault')
  rs=grammar.rows(text);positive=state_gate(rs,fighter,side,guest,payload)
  need(observed['actualEarnedNativeState']==grammar.gate(rs,fighter,side,guest,payload),'Source-bound native state regenerated exactly from actual rows')
  g=defaultdict(list)
  for index,line in enumerate(text.splitlines()):
   parsed=fifo.model.parse(line)
   if parsed and parsed[0]!='FLOOR_CPU':parsed[1]['_observed_line']=index;g[parsed[0]].append(parsed[1])
  g['SPLIT_STATE']=[r for r in rs if r['tag']=='SPLIT']
  identity=grammar.IDS[fighter];own=identity in(17,18);projection=fifo.contract(g,guest,payload,identity,side)if own else None
  records=json.loads((folder/'continuous_scene_records.json').read_text());rgb=json.loads((folder/'visible_digests.json').read_text())
  retired=observed['nativeBothPointerTeardown'];origin=positive['origin'];later=[r for r in records if r['frame']>=retired+3]
  need(len(records)==meta['observedRGBFields']==meta['modelExactFields']==observed['exactFields']and
       [r['frame']for r in records]==list(range(origin+1,retired+31))and len(rgb)==len(records)and
       all(v['file']==f"display_{r['frame']}.png"and v['rgbSHA256']==r['rgbSHA256']for v,r in zip(rgb,records)),
       'Every consecutive actual whole-scene RGB/VRAM replay target retained and source-bound')
  need(later and all(not r['modeledFlip']and r['rgbSHA256']==records[retired-origin-1]['rgbSHA256']for r in later)and
       later[-1]['body'][str(side)]['pixels']>0 and later[-1]['nativeSecondarySplitPixels']>0,
       'Original native final split page held without new actor rendering, not forced pixel clearing')
  semantics.append(dict(fighter=fighter,side=side,stockReferenceOnly=not own,pointerTeardownAge=retired-origin,
       postRetirementFields=len(later),newFlips=0,newVictimFIFO=0,
       heldVictimPixels=later[-1]['body'][str(side)]['pixels'],heldSecondaryPixels=later[-1]['nativeSecondarySplitPixels']))
  faults=state_faults(rs,fighter,side,guest,payload)
  if own:faults+=fifo_faults(g,guest,payload,identity,side,projection)
  reviews=list((folder/'review').glob('*.png'));need(len(reviews)==1 and observed['essentialNativeReviewPNGsWritten']==1,'One bounded actual ten-phase/post-match native review')
  need(not list(folder.glob('*.bin'))and not list(folder.glob('*.wav'))and not(folder/'input_sources').exists(),'No raw native media or duplicate sources')
  need(len(observed['rejectedActualPixelTargetFaults'])==2,'Actual first-native RGB and VRAM target corruptions both rejected')
  for p in folder.rglob('*'):
   if p.is_file():pins[str(p.resolve())]=sha(p)
  pins[str(reportpath)]=sha(reportpath)
  cases.append(dict(fighter=fighter,side=side,stockReferenceOnly=not own,exactFields=len(records),
       actualEarnedNativeState=positive,nativeFIFO=projection,actualSemanticFaultsRejected=faults,
       actualWindowsTerminal=terminal,nativeReview=str(reviews[0]),postRetirementNewRender=False))
 need({s['fighter']for s in semantics if s['stockReferenceOnly']}=={'kitana','liu_kang'}and
      len({(s['pointerTeardownAge'],s['postRetirementFields'],s['newFlips'],s['newVictimFIFO'])for s in semantics})==1,
      'Actual current two-stock and four-own contexts have identical native held-page lifecycle semantics')
 need(all(sha(p)==h for p,h in pins.items()),'All executed source/capture/review evidence unchanged')
 return dict(passed=True,candidate=current.NAME,cases=cases,inputHashes=pins,actualContexts=6,ownContexts=4,currentStockReferenceContexts=2,
     exactNativeFields=sum(c['exactFields']for c in cases),exactRGBPixels=sum(c['exactFields']for c in cases)*400*254,
     actualSemanticFaultsRejected=sum(len(c['actualSemanticFaultsRejected'])for c in cases),actualNativePixelTargetFaultsRejected=12,
     currentSplitConstructorStreamMirrorPaletteStateAndSceneAccepted=True,currentStockHeldWinnerPageSemanticsAccepted=True,
     heldPageComparisons=semantics,artAestheticReviewPending=True,fullAudioAcceptance=False,fullPortAcceptance=False,
     newSourceDirectoryCopies=0,newBuildCopies=0,nativeGameChanges=0,rawMediaFilesWritten=0,scope=__doc__)

if __name__=='__main__':
 need(not OUT.exists(),'Fresh full current split/stock-reference matrix')
 try:report=run()
 except Exception as error:
  import traceback
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','cases','heldPageComparisons')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
