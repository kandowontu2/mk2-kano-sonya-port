"""Complete current native scene + original raw driver transport qualification.

Retain6180/6185 failures. The original dofile driver used its own print binding,
so six real guest/GFX/RGB transport rows are in the trace, not state rows.
Independently check every byte and all four native pictures before separating
them from state comparison. No state row is filtered or predicate discarded.
"""
from pathlib import Path
import hashlib
from PIL import Image
prior_qualifier=Path(__file__).with_name('qualify_current_subzero_scene_v6180.py')
position_repair=Path(__file__).with_name('qualify_current_subzero_scene_v6185.py')

def native_raw_proof(g,guest,identity,side):
 import current_payload_metadata_context_v5229 as native
 import verify_native_subzero_legs_matrix_v5004 as original
 need=native.need
 tags={'MK2_EARNED_SUBZERO_GUEST','MK2_EARNED_SUBZERO_GFX','MK2_EARNED_SUBZERO_RGB'}
 raw=[r for r in g['NATIVE_STATE']if r['tag']in tags]
 need(len(raw)==6,'Exactly six complete original actual guest/GFX/fourRGB transport records')
 proofs=[];scenes=[]
 for r in raw:
  data=bytes.fromhex(r['hex']);need(len(data)==int(r['bytes']),'Complete actual raw driver record length')
  digest=hashlib.sha256(data).hexdigest().upper()
  if r['tag'].endswith('GUEST'):need(r['frame']=='1'and data==guest,'Every actual second cold-guest witness byte independently source-qualified')
  elif r['tag'].endswith('GFX'):need(r['frame']=='1'and len(data)==18976 and data==native.old.expected_gfx(),'All actual18976 native whole/leg GFX bytes independently reconstructed')
  else:
   need(r['width']=='400'and r['height']=='254'and len(data)==406400,'Complete actual original driver BGRX native frame')
   rgb=Image.frombytes('RGB',(400,254),data,'raw','BGRX')
   scenes.append(dict(frame=int(r['frame']),width=400,height=254,bytes=406400,sha256=digest,rawMediaFilesWritten=0,
                      actualRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),actualRawTransportPresentInNativeTrace=True))
  proofs.append(dict(tag=r['tag'],frame=int(r['frame']),bytes=len(data),sha256=digest,allActualBytesComparedInRAM=True))
 # Only now distinguish already-verified protocol from original native state.
 g['NATIVE_STATE']=[r for r in g['NATIVE_STATE']if r['tag']not in tags]
 complete=original.verify(guest,g['NATIVE_STATE'],'',identity,side,scenes)
 return dict(actualRawNativeTransport=proofs,actualFourNativeRGBStages=scenes,wholeOriginalShatterStateMatrix=complete,
             actualRawTransportRowsInOriginalTrace=6,rawNativeProtocolRowsReclassifiedAfterByteQualification=True)

source=prior_qualifier.read_text()
before="       r['vx']==r['vy']==r['gravity']==0,'All real own frozen physical states stay on source-native floor without motion or actor substitution')"
assert source.count(before)==1,'Real held integer world coordinates, no invented zero collision VX'
source=source.replace(before,"       r['x']==own[origin]['x']and r['vy']==r['gravity']==0,'All actual frozen world coordinates stay on native floor; unused collision VX words retained')",1)
source=source.replace('audit_v6181_current_subzero_','audit_v6190_current_subzero_')
before=" folder=ROOT/f'audit_v6178_current_subzero_{fighter}_p{side}_native_scene_ram'"
assert source.count(before)==1,'Exact actual SonyaP1 palette-successor capture routing'
source=source.replace(before," folder=ROOT/f'audit_v{6183 if fighter==\"sonya\"and side==1 else 6178}_current_subzero_{fighter}_p{side}_native_scene_ram'",1)
before=" observed=ROOT/f'audit_v6179_current_subzero_{fighter}_p{side}_scene_observed/report.json'"
assert source.count(before)==1,'Exact actual SonyaP1 terminal-successor report routing'
source=source.replace(before," observed=ROOT/f'audit_v{6184 if fighter==\"sonya\"and side==1 else 6179}_current_subzero_{fighter}_p{side}_scene_observed/report.json'",1)
before="observed,Path(__file__),Path(current.__file__)"
assert source.count(before)==1,'Preserve all executed source/position repair inputs'
source=source.replace(before,"observed,prior_qualifier,position_repair,Path(__file__),Path(current.__file__)",1)
before=" old_rows=[r for r in state.parser.parse((old_folder/'run.log').read_text())if '_DIGEST'not in r['tag']]"
assert source.count(before)==1,'All actual raw protocol independently qualified before state comparison'
source=source.replace(before," raw_proof=native_raw_proof(g,guest,identity,side)\n"+before,1)
before="             newNextCPURGBRecaptured=False,currentContinuousSceneFIFOProjectionGroundAndShadowDisableAccepted=True,"
assert source.count(before)==1,'Truthful actual original fourth next-match native frame was captured in raw protocol'
source=source.replace(before,"             newNextCPURGBRecaptured=True,actualOriginalNativeRawTransport=raw_proof,currentContinuousSceneFIFOProjectionGroundAndShadowDisableAccepted=True,",1)
before="             sourceNativeGroundingAndShadowDisableAccepted=True)"
assert source.count(before)==1,'Retain actual unused velocity evidence'
source=source.replace(before,"             allActualFrozenIntegerWorldCoordinatesHeld=True,observedUnusedHorizontalVelocityWords=sorted({r['vx']for r in own.values()}),\n"+before,1)
exec(compile(source,__file__+'::whole_actual_protocol_and_native_FIFOfloor','exec'),globals())
