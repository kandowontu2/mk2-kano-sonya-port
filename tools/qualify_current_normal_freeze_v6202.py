"""Current ordinary ice/thaw/controls and complete701-field native shadows.

Retain the complete5059 command/state/source/component/projection/row/pen
algorithm and its21 actual corruptions, six contexts and fresh Sonya repeat.
Extend the four sampled shadow passes to every actual live field; resolve
only the exact original raw Subzero ice hand with the independently qualified
unconditional signed native scanner. No imported raw sprites admitted.
Four event RGB fields, not continuous full-scene/audio/all-arena acceptance.
"""
import argparse,copy,hashlib,json,re,traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
import native_stock_raw_shadow_scanner_v5315 as scanner
ROOT,need,sha=current.ROOT,current.need,current.sha
PRIOR=Path(__file__).with_name('verify_normal_subzero_freeze_shadow_v5059.py')
OUT=ROOT/'audit_v6206_current_normal_subzero_freeze_checked'
source=PRIOR.read_text()
source=source.replace('import native_subzero_legs_context_v4993 as native','import current_payload_metadata_context_v5229 as native')
source=source.replace('report_version=5047,folder_version=5046','report_version=6201,folder_version=6200')
source=source.replace('audit_v{folder_version}_normal_subzero_','audit_v{folder_version}_current_normal_subzero_').replace('audit_v{report_version}_normal_subzero_','audit_v{report_version}_current_normal_subzero_')
before=" need(len(raw_stock)==1,'The exact original raw Sub-Zero hand counterexample is preserved in every control case')"
need(source.count(before)==1,'Entire old sampled contract retained; continuous native casting has36actual raw-hand fields')
source=source.replace(before," need(len(raw_stock)==36,'All36 actual native raw-hand fields preserved, not only one sampled original hand')",1)
scope=dict(__name__='original_complete_freeze_predicates',__file__=str(PRIOR))
exec(compile(source,str(PRIOR)+'::whole_current_continuous_shadow','exec'),scope)
load,original_check,num,group,reconstruct=(scope[k]for k in('load','check','num','native_group','reconstruct'))

def complete_shadow(b,identity,guest,payload,gfx):
 rows=b['rows'];side=b['side'];fields={num(r,'frame'):r for r in rows['MK2_NORMAL_FREEZE_FIELD']}
 ps=rows['MK2_NORMAL_FREEZE_PROJECTION'];parts={(num(p,'frame'),num(p,'row')):p for p in b['parts']}
 by=defaultdict(list)
 for p in ps:by[num(p,'frame'),num(p,'slot')].append(p)
 need(set(by)=={(f,s)for f in fields for s in(1,2)},'Both real physical shadows present in every one of701actual live fields; no omitted window')
 for (frame,slot),items in by.items():
  actual=group(items[0],payload,guest)
  need([num(p,'component')for p in items]==list(range(len(actual)))and
       len({num(p,'pose')for p in items})==1,'Entire independently reconstructed native multipart shadow group in every physical field')
  if slot==side:
   need(all(num(p,'floor')==num(fields[frame],'floor')and num(p,'id')==identity for p in items),
        'Every owned native shadow uses genuine character and constant actual native floor')
 raw=[];raw_copies=0
 for p in ps:
  if num(p,'command')&128:continue
  graphic,width,height,command=(num(p,k)for k in('graphic','width','height','command'))
  need(num(p,'id')==8 and graphic==0x025816f6 and width==11 and height==18 and command in(0x6000,0x6010),
       'Only exact source-owned original raw Subzero11x18ice hand enters signed header scanner')
  proof=parts[num(p,'frame'),num(p,'row')]
  need(proof['streamFormat']=='stockRaw6'and not proof['compressedRowStreamVerified']and
       proof['actualRowStarts']==proof['actualRowHeaders']==[]and proof['usedBits']==0 and not proof['stockRawNativeShadowRowSteppingAccepted'],
       'Actual raw body capture remains raw; separate source-native shadow stepping evidence')
  bit=graphic;starts=[]
  for _ in range(height):
   need(0<=bit and bit+8<=len(gfx)*8,'Every unconditional stock header inside whole independently interleaved ROM')
   starts.append(bit);header=(int.from_bytes(gfx[bit//8:bit//8+2],'little')>>(bit%8))&255
   pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
   bit=(bit+8+6*(width-pre-post))&0xffffffff
   need(0<=bit<=len(gfx)*8,'Original signed width-minus-skips pointer bounded in complete native ROM')
  indices=list(range(0,4*(height//4),4));indices.append(indices[-1])
  dmas=[d for d in rows['MK2_NORMAL_FREEZE_DMA']if num(d,'frame')==num(p,'frame')and num(d,'cache_row')==num(p,'row')and num(d,'pc')in(0xff8015a0,0xff801610)]
  need([num(d,'source')for d in dmas]==[starts[i]for i in indices],
       'Every actual raw-hand shadow source step and duplicate-tail row equals independent signed native scanner, never fitted')
  raw_copies+=len(dmas);raw.append(dict(frame=num(p,'frame'),slot=num(p,'slot'),graphic=f'{graphic:08X}',sourceSteps=[starts[i]for i in indices]))
 need(len(raw)==36 and raw_copies==180,'Complete36raw-hand fields and180actual native shadow rows')
 return dict(actualPairedShadowFields=701,actualPhysicalShadowPasses=len(by),nativeProjectionParts=len(ps),
             actualSourceNativeRawHandFields=len(raw),actualSourceNativeRawHandShadowCopies=raw_copies,
             sourceNativeRawHandSteps=raw,complete701NativeFieldShadowLedgerAccepted=True,
             originalRawBodyDecoderUnchanged=True,importedRawSpritesAdmitted=0)

def scenes(b):
 r=b['report'];records=json.loads((b['folder']/'rgb_memory_proofs.json').read_text())
 need(records==r['actualScenes']and len(records)==4,'All actual four native screen-bitmap records, no modeled/borrowed stage')
 first=num(b['rows']['MK2_STOCK_HEAD_V921_FIRST_LIVE'][0],'frame')
 need([p['frame']for p in records]==[first+x for x in(60,145,240,580)],'Four exact native bitmap callback phases tied to actual live origin')
 atlas=np.asarray(Image.open(r['nativeReview']).convert('RGB'));need(atlas.shape==(556,800,3),'Single bounded four-panel actual native review')
 for i,p in enumerate(records):
  x,y=i%2*400,i//2*278
  need(hashlib.sha256(atlas[y+24:y+278,x:x+400].tobytes()).hexdigest().upper()==p['actualRGBSHA256'],
       'Every complete native review panel equals actual captured RGB pixels')
 return dict(actualNativeReviewPanels=4,actualNativeEventRGBPixels=406400,allNativeReviewPanelsPixelBound=True,
             nativeReview=r['nativeReview'])

def check(b,identity,guest,payload,gfx):
 base=original_check(b,identity,guest,payload,gfx)
 base.update(complete_shadow(b,identity,guest,payload,gfx));base.update(scenes(b))
 return base

def trials(b,identity,floor):
 # Same21 original5059 corruptions, generated one at a time, not21 retained
 # duplicate inventories in RAM. Add two real continuous-window omissions.
 for label,index,key,value in(('proxy_identity',240,'victim_id','17'if identity==1 else'1'),
  ('owner_replaced',240,'victim_owner','01000000'),('health_damage',150,'hp','160'),
  ('thaw_never_restores',340,'action','0401'),('wrong_blue_palette',240,'bank','0303'),
  ('floating_ground',240,'y',str(floor-1)),('movement_stuck',467,'x',b['rows']['MK2_NORMAL_FREEZE_FIELD'][450]['x']),
  ('punch_never_starts',512,'action','0303')):
  v=copy.deepcopy(b);v['rows']['MK2_NORMAL_FREEZE_FIELD'][index][key]=value;yield label,v
 v=copy.deepcopy(b);start=num(v['rows']['MK2_STOCK_HEAD_V921_FIRST_LIVE'][0],'frame')
 v['rows']['MK2_STOCK_HEAD_V921_INPUT']=[t for t in v['rows']['MK2_STOCK_HEAD_V921_INPUT']if num(t,'frame')!=start+108];yield'physical_lp_missing',v
 v=copy.deepcopy(b);v['rows']['MK2_NORMAL_FREEZE_ICE_REQUEST'][0]['value']='09C1';yield'native_opcode_changed',v
 for label,key,value in(('wrong_camera','b4','00000000'),('wrong_native_ground','b2','00000000'),('descriptor_shift','dx','99'),('shadow_owner','owner','01000000')):
  v=copy.deepcopy(b);v['rows']['MK2_NORMAL_FREEZE_PROJECTION'][0][key]=value;yield label,v
 for label,key,value in(('shadow_x_shift','x','999'),('shadow_y_shift','y','499'),('wrong_shadow_pen','color','0101'),('wrong_row_source','source','00000001')):
  v=copy.deepcopy(b);next(d for d in v['rows']['MK2_NORMAL_FREEZE_DMA']if num(d,'pc')==0xff8015a0)[key]=value;yield label,v
 v=copy.deepcopy(b);v['parts'][0]['actualRowStarts'][1]+=1;yield'packed_row_start_changed',v
 v=copy.deepcopy(b);v['parts'][0]['sha256']='0'*64;yield'actual_GFX_bytes_wrong',v
 v=copy.deepcopy(b);next(q for q in v['parts']if q['streamFormat']=='stockRaw6')['stockRawNativeShadowRowSteppingAccepted']=True;yield'stock_raw_falsely_accepted',v
 # Removing one complete unmarked physical window defeats sampled-only
 # checks but must not defeat the full701-field native shadow contract.
 v=copy.deepcopy(b);frame=start+241
 for tag in('MK2_NORMAL_FREEZE_PROJECTION','MK2_NORMAL_FREEZE_DMA'):v['rows'][tag]=[p for p in v['rows'][tag]if num(p,'frame')!=frame]
 v['parts']=[p for p in v['parts']if num(p,'frame')!=frame];yield'omitted_entire_unmarked_shadow_field',v
 v=copy.deepcopy(b);raw=next(p for p in v['rows']['MK2_NORMAL_FREEZE_PROJECTION']if not num(p,'command')&128)
 ds=[d for d in v['rows']['MK2_NORMAL_FREEZE_DMA']if num(d,'frame')==num(raw,'frame')and num(d,'cache_row')==num(raw,'row')and num(d,'pc')in(0xff8015a0,0xff801610)]
 ds[1]['source']=f'{num(ds[1],"source")^1:08X}';yield'wrong_original_raw_hand_interior_shadow_step',v

def pin_case(b,pins):
 r=b['report'];terminal=r['actualWindowsTerminal'];meta=json.loads((b['folder']/'result.json').read_text())
 need(r['passed']and r['nativeExit']==terminal['nativeExit']==meta['nativeExit']==0 and not meta['modelErrors']and
      terminal['actualWindowsIdentity']['ProcessId']==terminal['pid']and Path(terminal['actualWindowsIdentity']['ExecutablePath']).resolve()==(ROOT/current.NAME/'mkport_candidate.exe').resolve(),
      'Actual current Windows identity/creation/full command, consumed native terminal and clean collector')
 for p,h in r['inputHashes'].items():need(sha(p)==h,'Every current compiled/controller/input source unchanged');pins[p]=h
 g=json.loads((b['folder']/'guest_memory_proof.json').read_text());x=json.loads((b['folder']/'gfx_memory_proof.json').read_text())
 need(g['everyActualByteComparedInRAM']and g['sha256']==current.GUEST_SHA and g['executableSHA256']==current.EXE_SHA and
      x['everyActualByteComparedInRAM'],'Every actual current guest and native frozen-art initialization byte checked in RAM')
 for p in(b['report_path'],*(p for p in b['folder'].rglob('*')if p.is_file())):pins[str(p.resolve())]=sha(p)

def main():
 need(not OUT.exists(),'Fresh entire current ordinary freeze/shadow matrix')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 pins={str(p.resolve()):sha(p)for p in(PRIOR,Path(__file__),Path(current.__file__),Path(scanner.__file__))}
 original_source=scanner.qualify();need(original_source['currentOriginalShadowKernelByteExact']and original_source['originalUnconditionalHeaderAndSignedWidthAdvanceQualified'],
                                         'Whole independently disassembled original signed shadow scanner retained')
 pins.update(original_source['inputHashes']);gfx=reconstruct(pins);cases=[];faults=[];panel_faults=[]
 for fighter,side,identity in scope['CASES']:
  b=load(fighter,side);pin_case(b,pins);positive=check(b,identity,guest,payload,gfx);cases.append(positive)
  # The exact four old native full-size stages remain independent baselines;
  # no old raw media is recreated or used in place of current observations.
  old_folder=ROOT/f'audit_v5046_normal_subzero_{fighter}_p{side}'
  prior_rgb=json.loads((old_folder/'rgb_memory_proofs.json').read_text())
  need(all(all(p[k]==q[k]for k in p)for p,q in zip(prior_rgb,b['report']['actualScenes']))and len(prior_rgb)==4,
       'All four new current native screen bitmaps equal every complete protected stage record')
  pins[str((old_folder/'rgb_memory_proofs.json').resolve())]=sha(old_folder/'rgb_memory_proofs.json')
  count=0
  for label,v in trials(b,identity,positive['floor']):
   try:check(v,identity,guest,payload,gfx)
   except(ValueError,KeyError,AssertionError,StopIteration)as error:faults.append(dict(case=f'{fighter}_p{side}',fault=label,rejectedBy=str(error)));count+=1
   else:raise ValueError('Actual native freeze/shadow fault admitted '+label)
  need(count==23 and check(b,identity,guest,payload,gfx)==positive,'All original21and two whole-window/raw scanner faults rejected, uncached positive restored')
  for index in(0,1):
   v=copy.deepcopy(b);v['report']['actualScenes'][index]['actualRGBSHA256']='0'*64
   # File inventory stays unchanged; actual semantic panel comparison must
   # reject the changed RGB target, not a source-pin guard.
   try:scenes(v)
   except ValueError as error:panel_faults.append(dict(case=f'{fighter}_p{side}',panel=index,rejectedBy=str(error)))
   else:raise ValueError('Native review RGB target corruption admitted')
  print(f'{fighter}P{side}:701 complete paired native shadow fields,160ice fields,thaw/controls;23semantic and2RGB faults rejected',flush=True)
 repeat=load('sonya',1,6204,6203);pin_case(repeat,pins);repeat_result=check(repeat,18,guest,payload,gfx);first=load('sonya',1)
 need(repeat['report']['actualScenes']==first['report']['actualScenes']and repeat['rows']==first['rows']and repeat['parts']==first['parts']and repeat_result['sourceNativeRawHandSteps']==cases[2]['sourceNativeRawHandSteps'],
      'Fresh current Sonya repeat: every native row, complete stream inventory, raw shadow step and whole RGB stage identical')
 need(len(cases)==6 and len(faults)==138 and len(panel_faults)==12 and all(sha(p)==h for p,h in pins.items()),'Whole current six-case/source/fault/pixel matrix intact')
 report=dict(passed=True,candidate=current.NAME,executableSHA256=current.EXE_SHA,guestSHA256=current.GUEST_SHA,cases=cases,repeat=repeat_result,
  actualCurrentOwnCharacterSlotCases=4,actualCurrentStockControls=2,actualFreshRepeats=1,
  actualOrdinaryFields=sum(c['ordinaryFields']for c in cases)+repeat_result['ordinaryFields'],
  actualPairedShadowFields=sum(c['actualPairedShadowFields']for c in cases)+repeat_result['actualPairedShadowFields'],
  actualProjectionParts=sum(c['nativeProjectionParts']for c in cases)+repeat_result['nativeProjectionParts'],
  actualSourceBoundCompressedShadowCopies=sum(c['sourceBoundCompressedShadowCopies']for c in cases)+repeat_result['sourceBoundCompressedShadowCopies'],
  actualSourceNativeRawHandShadowCopies=sum(c['actualSourceNativeRawHandShadowCopies']for c in cases)+repeat_result['actualSourceNativeRawHandShadowCopies'],
  actualFaultsRejected=faults,actualSemanticFaultsRejected=len(faults),actualNativePanelFaults=panel_faults,actualNativePanelFaultsRejected=len(panel_faults),
  actualNativeReviewPanels=28,actualEventRGBPixels=2844800,allNativePanelsPixelBound=True,currentSonyaP1RepeatEveryNativeRowStreamAndRGBIdentical=True,
  completeCurrentOrdinaryFreezeThawControlsAnd701NativeShadowFieldsAccepted=True,originalSourceNativeRawHandStepsAccepted=True,inputHashes=pins,
  fullArtAcrossAllArenasAccepted=False,continuousNativeRGBReplayAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,scope=__doc__)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','repeat','inputHashes','actualFaultsRejected','actualNativePanelFaults')},indent=2),flush=True)

if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True);raise SystemExit(1)
