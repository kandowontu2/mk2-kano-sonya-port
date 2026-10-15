"""One individually viewed original current native selection, not full UI QA.

Keep the failed Kitana policy and full native evidence; retire its exact RAM
producer/review server, safely against Windows PID reuse, after preservation.
"""
import hashlib
import inspect
import json
import os
import subprocess
from pathlib import Path
from types import SimpleNamespace
import retire_native_kano_zoning_losing_kitana as common

ROOT,need,sha=common.ROOT,common.need,common.sha
REVIEW=ROOT/'audit_native_kano_current_selection_snapshot_review'
PORT=64880


def review(ram,carrier,server):
    need(os.getpid()==common.PARENT and not REVIEW.exists() and server.server_port==PORT,
         'Exact original retained parent and original native review server')
    folder=common.capture.OUT
    metadata=json.loads((folder/'result.json').read_text())
    terminal=json.loads((folder/'native_terminal.json').read_text())
    stop=json.loads((folder/'explicit_unsuccessful_physical_policy_stop.json').read_text())
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    prefix_path=ROOT/'audit_native_kano_prefix_complete_move_inventory_checked/report.json'
    prefix=json.loads(prefix_path.read_text())
    need(prefix['passed'] and prefix['finiteCurrentKanoFirstThreeLadderAdvancesAccepted'] and
         terminal['identity']==stop['exactNativeIdentity']==prefix['actualNativeIdentity'] and terminal['nativeExit']==0xffffffff and
         not metadata['passed'] and stop['physicalPolicyUnsuccessful'] and not stop['stoppedSolelyForObservationTimeout'] and
         proof['everyActualByteComparedInRAM'] and hashlib.sha256(ram['guest']).hexdigest().upper()==proof['sha256'] and
         all(sha(p)==h for p,h in prefix['inputHashes'].items()),
         'Actual complete current guest, exact failed terminal identity and independent native gameplay prefix retained')
    raw,images=ram['scope']['RAM_RAW'],ram['scope']['RAM_IMAGES']
    name='campaign_selection_1_146.png'
    need(list(raw)==list(images)==[name] and len(carrier['rgbFrames'])==1,'Exactly one original retained raw/PIL selection snapshot')
    record=carrier['rgbFrames'][0]
    need(record['pixels'] is raw[name] and len(raw[name])==406400 and
         hashlib.sha256(raw[name]).hexdigest().upper()==record['header']['sha256']=='EA0E5EF588B32673DBE6353EB5560118CEC081C8828CCEFD9A1732FA32DEB972' and
         record['header'] in [dict(q,width='400',height='254') for q in metadata['actualScenes']],
         'Exact original individually viewed400x254 native raster, zero-copy alias and native host digest bound')
    source_path=common.capture.SOURCE/'report.json';source=json.loads(source_path.read_text())
    pins=dict(prefix['inputHashes'])
    for p in (Path(__file__),Path(common.__file__),prefix_path,source_path,folder/'result.json',folder/'native_terminal.json',
              folder/'explicit_unsuccessful_physical_policy_stop.json',folder/'guest_memory_proof.json'):
        pins[str(p.resolve())]=sha(p)
    REVIEW.mkdir();(REVIEW/'report.json').write_text(json.dumps(dict(passed=True,finiteCurrentKanoSelectionSnapshotReviewed=True,
        exactNativeIdentity=terminal['identity'],exactRAMParent=common.PARENT,exactReviewPort=PORT,
        individuallyViewedOriginalRaster=record['header'],zeroCopyOriginalNativePixels=True,
        visualObservations=['Dedicated Kano portrait at top-left and dedicated Sonya portrait at top-right.',
          'Native green P1 border and player-number1 appear on the Kano portrait in this actual frame.',
          'Left selection preview is the own Kano body, not Liu Kang.',
          'The unselected Sonya portrait has no persistent selection border in this frame.'],
        blinkingAnimationAccepted=False,onePixelBackdropAlignmentAccepted=False,fullSelectionTransitionsAccepted=False,
        ladderOrFightArtworkAccepted=False,groundOrAudioAccepted=False,fullPortAcceptance=False,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        imageFilesWritten=0,newBuilds=0,newROMCopies=0,newZIPs=0,publicPlayableChanged=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(passed=True,finiteCurrentKanoSelectionSnapshotReviewed=True,fullPortAcceptance=False)),flush=True)


def prepare(ram):
    need(json.loads((REVIEW/'report.json').read_text())['passed'],'Original individual native raster reviewed before release')
    old=common.previous
    scope=dict(vars(old),__file__=__file__,capture=common.capture,GAME=common.GAME,PARENT=common.PARENT,
               OUT=common.OUT,RETIRED=common.RETIRED)
    source=inspect.getsource(old.prepare)
    before="stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0"
    after="stats['lossesByStage']['3']>=30 and stats['latestNativeField']['stage']=='3'"
    need(source.count(before)==1,'Whole original failed run preservation boundary')
    source=source.replace(before,after).replace('range(9)','range(3)').replace('failed Scorpion policy','failed Kitana policy').replace('earlier nine-fight','earlier three-fight')
    need(source.count('individuallyViewedInThisTrial=False,')==1,'Exact original raster-review metadata boundary')
    source=source.replace('individuallyViewedInThisTrial=False,','individuallyViewedInThisTrial=True,')
    exec(compile(source,__file__+'::whole_original_preservation_with_actual_selection_review','exec'),scope)
    return scope['prepare'](ram)


def retire():
    old=common.previous
    prior=SimpleNamespace(**dict(vars(old),__file__=__file__,capture=common.capture,GAME=common.GAME,PARENT=common.PARENT,
                               OUT=common.OUT,RETIRED=common.RETIRED))
    saved=json.loads((REVIEW/'report.json').read_text())
    need(saved['passed'] and all(sha(p)==h for p,h in saved['inputHashes'].items()),'Whole actual individual raster review remains frozen')
    query=subprocess.run(['powershell.exe','-NoProfile','-Command',
        f'Get-NetTCPConnection -LocalPort {PORT} -State Listen -ErrorAction SilentlyContinue | Select-Object OwningProcess | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(not query.stdout.strip() and not query.stderr.strip(),'Original review port has no listener after owned server/parent exit')
    source=inspect.getsource(common.identity_retirement.run)
    need(source.count('noReviewServerCreated=True,')==1,'Whole original accurate preview retirement boundary')
    source=source.replace('noReviewServerCreated=True,','originalReviewServerClosed=True, exactReviewPort=64880,')
    before='str(Path(prior.__file__).resolve()): sha(prior.__file__)},'
    after="str(Path(prior.__file__).resolve()): sha(prior.__file__),str(REVIEW/'report.json'):sha(REVIEW/'report.json')},"
    need(source.count(before)==1,'Whole original review receipt pin extension')
    scope=dict(vars(common.identity_retirement),__file__=__file__,prior=prior,REVIEW=REVIEW)
    exec(compile(source.replace(before,after),__file__+'::entire_original_PID_reuse_safe_retirement_and_closed_preview','exec'),scope)
    return scope['run']()


if __name__=='__main__':retire()
