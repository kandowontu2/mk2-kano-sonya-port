"""Original full photo/font/shadow/common-background gate for actual current P1.

Reuse the entire source-qualified page verifier, not a screenshot-only claim.
Require the new complete native P1 renderer terminal first. Four exact RGB
records bind the actual continuous RAM fields to retained qualified reference
bytes. All original photo/glyph/background faults and exclusions remain.
"""
import argparse,gzip,inspect,json,re
from pathlib import Path
from types import SimpleNamespace
import current_payload_metadata_context_v5229 as current
import verify_sonya_p2_native_ending_pages_v4448 as original
ROOT,need,sha=current.ROOT,current.need,current.sha

def run(fighter):
 identity=17 if fighter=='kano'else 18
 folder=ROOT/f'audit_v5250_{fighter}_current_p1_ending_pixels'
 fullpath=ROOT/f'audit_v5250_{fighter}_current_p1_ending_pixels_checked/report.json'
 need(fullpath.exists(),'Await actual complete original native pixel terminal, never restart or fabricate success on timeout')
 proof=json.loads(fullpath.read_text())
 wholepath=ROOT/f'audit_v5235_{fighter}_corrected_p1_campaign_checked/report.json'
 whole=json.loads(wholepath.read_text())
 need(proof['passed']and proof['actualCurrentP1EndingAttractNativeRendererVideoAccepted']and
  proof['actualColdNativeCampaignExactlyUnchanged']and proof['physicalSlot']==1 and proof['fighter']==fighter and
  proof['candidate']==current.NAME and proof['executableSHA256']==current.EXE_SHA and
  whole['passed']and whole['actualCorrectedExecutableNaturalTowerOwnEndingAttractAccepted']and
  all(sha(p)==h for p,h in proof['inputHashes'].items())and
  all(sha(p)==h for p,h in whole['inputHashes'].items()),
  'Actual entire source-timed pixel/physical/true-ID/winner/own-ending/300attract current P1 proof')
 with gzip.open(folder/'run.log.gz','rt')as reader:raw=reader.read()
 records=json.loads((folder/'ending_continuous_records.json').read_text())
 byframe={r['frame']:r for r in records}
 need(len(byframe)==proof['exactConsecutiveNativeVideoFields'],'Every actual complete continuous RGB field uniquely bound')
 pageevents=original.photos.rows(raw,'PAGE_SNAP')
 actual_page_rgb={r['file']:byframe[int(r['frame'])]['rgbSHA256']for r in pageevents}
 carrier=SimpleNamespace(OUT=fullpath.parent,FOLDER=folder,NAME=current.NAME,
  capture=SimpleNamespace(expected=current.expected))
 source=inspect.getsource(original.main)
 changes=[
 ("proof['passed'] and proof['case']['passed'] and\n         proof['actualNaturalSonyaP2TowerClearAccepted'] and\n         proof['case']['unassisted_clear_proven']",
  "proof['passed'] and proof['actualCurrentP1EndingAttractNativeRendererVideoAccepted'] and proof['actualColdNativeCampaignExactlyUnchanged']"),
 ("pins=dict(proof['case']['inputHashes'])","pins=dict(proof['inputHashes'])"),
 ("raw=(campaign.FOLDER/'run.log').read_text()","raw=actual_log"),
 ("starts[0]['winner']=='2'","starts[0]['winner']=='1'"),
 ("starts[0]['roster']=='18'",f"starts[0]['roster']=='{identity}'"),
 ("True own Sonya18 ending",f"True own {fighter}{identity} P1 ending"),
 ("need(len(frames)==78 and", """for f in frames:
        if f['filename']in actual_page_rgb:f['rgbSHA256']=actual_page_rgb[f['filename']]
    need(len(frames)==json.loads((campaign.FOLDER/'result.json').read_text())['actualNativeRGBFrameCallbacks'] and"""),
 ("['cases']['sonya']['snapshots']",f"['cases']['{fighter}']['snapshots']"),
 ("index=52+page-1",f"index={50 if fighter=='kano'else 52}+page-1"),
 ("dispatch['roster']=='18'",f"dispatch['roster']=='{identity}'"),
 ("(18*3+int",f"({identity}*3+int"),
 ("s['roster']=='18'",f"s['roster']=='{identity}'"),
 ("text.model(guest,original,graphics,18,page)",f"text.model(guest,original,graphics,{identity},page)"),
 ("physicalSlot=2,identity=18",f"physicalSlot=1,identity={identity}"),
 ("actualNaturalSonyaP2EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted",
  "actualCurrentP1EndingEarlyLatePhotoTextShadowCommonBackgroundAccepted"),
 ("for m in (photos,text,background,campaign,campaign.capture):pin(m.__file__)",
  "for m in (photos,text,background,current,source_module):pin(m.__file__)\n    pin(wholepath)\n    pin(campaign.FOLDER/'ending_continuous_records.json')")]
 if fighter=='kano':
  own='photos.original.reference(donor,1,page-1)';other='photos.original.reference(donor,0,page-1)'
  need(source.count(own)==source.count(other)==1,'Exact source-derived own/other photo oracle')
  source=source.replace(own,'photos.original.reference(donor,OWN,page-1)').replace(other,'photos.original.reference(donor,OTHER,page-1)')
  source=source.replace('photos.original.reference(donor,OWN,page-1)',other).replace('photos.original.reference(donor,OTHER,page-1)',own)
 for before,after in changes:
  need(source.count(before)==(2 if before=='physicalSlot=2,identity=18'else 1),
   'Only actual physical scope/current terminal/RAM target addition in full original page gate '+before)
  source=source.replace(before,after)
 scope=dict(vars(original),__file__=__file__,campaign=carrier,current=current,source_module=original,
  actual_log=raw,actual_page_rgb=actual_page_rgb,wholepath=wholepath,
  OUT=ROOT/f'audit_v5254_{fighter}_current_p1_original_ending_pages_checked')
 exec(compile(source,__file__+'::entire_original_photo_font_shadow_background_RAM_gate','exec'),scope)
 return scope['main']()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 run(parser.parse_args().fighter)
