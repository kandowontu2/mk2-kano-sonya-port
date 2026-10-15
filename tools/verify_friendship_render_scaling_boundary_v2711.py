"""Immutable original zoom-model limitation and exact source-verified extension.
Keep original incomplete drawing results unaccepted. The physical captures,
every old screenshot and all existing identity/source/scanout/erasure gates
must stay unchanged. This is not a full finisher or port acceptance claim.
"""
import json,re
import numpy as np
from pathlib import Path
import verify_current_interrupt_v1870 as launch
import verify_native_scaled_raster_units_v1718 as units
ROOT=launch.ROOT
OUT=ROOT/'audit_v2712_friendship_render_scaling_boundary_checked'
def need(ok,label):
 if not ok:raise ValueError(label)
def verify():
 pins=launch.source_pins()
 def pin(path,wanted=None):
  path=str(path);actual=launch.sha(path);need(wanted is None or actual==wanted,'Immutable actual render dependency '+path)
  need(path not in pins or pins[path]==actual,'Consistent actual render dependency '+path);pins[path]=actual
 old=ROOT/'tools/inspect_current_friendship_full_render_v2705.py';new=ROOT/'tools/inspect_current_friendship_scaled_render_v2709.py'
 source=old.read_text().replace('import inspect_ball_register_erase_v1843 as erase','import inspect_ball_register_erase_v1843 as erase\nimport inspect_current_cpu_knife_raster_v1975 as scaling')
 source=source.replace(" meta=json.loads((folder/'result.json')"," scaling.source(pins)\n meta=json.loads((folder/'result.json')")
 source=source.replace('Read-only current Friendship complete-render diagnostic, not universal acceptance.','Read-only current Friendship scaled complete-render diagnostic, not universal acceptance.')
 need(source==new.read_text(),'Only original native scaling model import/source binding and diagnostic title changed; all prior gates retained')
 pin(old);pin(new)
 unit=units.check()
 need(unit['passed'] and unit['independentScaleModeFlipCases']==108 and unit['exactCompressedUnitScaleRegressions']==16,'All 124 independent original fixed-point/compressed-row unit controls fully repeated')
 for file,wanted in unit['inputHashes'].items():pin(file,wanted)
 cases={};same_images=0
 for fighter in ('kano','sonya'):
  old_path=ROOT/f'audit_v2706_current_{fighter}_friendship_full_render_p1_diagnostic/report.json'
  new_path=ROOT/f'audit_v2710_current_{fighter}_friendship_scaled_render_p1_diagnostic/report.json'
  original=json.loads(old_path.read_text());current=json.loads(new_path.read_text())
  need(original['passed'] and original['diagnosticCompleted'] and not original['fullDrawingAndContinuousErasureAccepted'] and all(not x['passed'] and 'Unmodeled scaling' in x['error'] for x in original['diagnostics'].values()),'Original actual unit-only renderer limitation retained and never promoted')
  need(current['passed'] and current['diagnosticCompleted'] and current['control']==original['control'] and current['actualConsecutiveScanouts']==original['actualConsecutiveScanouts']==1600 and current['actualBoundPixels']==162560000 and current['physicalInputAndNativeChronologyUnchanged'] and not current['gameChanged'] and not current['fullPortAcceptance'],'Entire actual physical/control/raster binding repeated unchanged')
  for report,path in ((original,old_path),(current,new_path)):
   pin(path)
   for file,wanted in report['inputHashes'].items():pin(file,wanted)
  prior=ROOT/f'audit_v2691_current_{fighter}_friendship_shadow_p1/snap';capture=ROOT/f'audit_v2704_current_{fighter}_friendship_full_render_p1/snap'
  images=list(prior.glob('*.png'));need(len(images)>300,'Actual entire original extended screenshot set')
  for image in images:
   wanted=launch.sha(image);pin(image,wanted);pin(capture/image.name,wanted);same_images+=1
  groups=current['diagnostics']['drawing'];erase=current['diagnostics']['continuousErasure']
  black_shadow_frames=0
  if groups['passed']:
   for record in groups['records']:
    if record['shadow_pixels']:
     colors=np.fromfile(capture.parent/f"display_palette_{record['frame']}.bin",dtype='<u4')
     need(colors[15]==0 and record['shadow_mismatches']==0,'Every actual visible source-reconstructed shadow pen is black')
     black_shadow_frames+=1
   need(black_shadow_frames>=10,'Actual visible startup/pre-command floor shadows, not empty pixel coverage')
  publications=post_retirement=0;last_bubble=None
  with (capture.parent/'run.log').open(encoding='utf-8-sig') as stream:
   for line in stream:
    if 'MK2_NAT_CAMPAIGN_FLOOR_ALL_QUEUE ' not in line:continue
    values=dict(re.findall(r'(\w+)=([^\s]+)',line));frame=int(values['frame']);pose=int(values['pose'],16)
    post_retirement+=frame>current['control']['actualPointerRetirement']
    if 0xfe9d2610<=pose<=0xfe9d2790:
     publications+=1;last_bubble=frame
     need(frame<=current['control']['actualPointerRetirement'],'No bubble publication after actual physical actor retirement; complete inventory remains visible')
  need(post_retirement>1000,'Real whole-render-list coverage after physical retirement')
  need(fighter!='kano' or publications>100,'Actual independent native Kano bubble publication coverage')
  cases[fighter]=dict(originalReport=str(old_path),extendedReport=str(new_path),originalDrawingAccepted=False,
   repeatedConsecutiveScanouts=1600,fullDrawingAndContinuousErasureAccepted=current['fullDrawingAndContinuousErasureAccepted'],
   drawingPassed=groups['passed'],continuousErasurePassed=erase['passed'],sourceExactBlackShadowFrames=black_shadow_frames,
   actualBubblePublications=publications,lastActualBubblePublication=last_bubble,allQueuePublicationsAfterPhysicalRetirement=post_retirement,
   noBubblePublicationAfterPhysicalRetirement=True,completeChildFreelistAndProcessTeardownAccepted=False,
   diagnosticErrors={name:value.get('error') for name,value in current['diagnostics'].items() if not value['passed']})
 pin(Path(__file__).resolve());launch.module_pins(pins)
 return dict(passed=True,onlyExistingSourceVerifiedScalingAndSourceBindingAdded=True,allOriginalChecksRetained=True,
  independentScaleModeFlipCasesRepeated=108,exactCompressedUnitScaleRegressionsRepeated=16,
  cases=cases,entirePriorScreenshotsByteIdentical=same_images,gameChanged=False,executedSourcesAndCapturesNeverEdited=True,
  fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 need(not OUT.exists(),'Immutable original model correction boundary')
 r=verify();OUT.mkdir();(OUT/'report.json').write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({key:value for key,value in r.items() if key!='inputHashes'},indent=2),flush=True)
