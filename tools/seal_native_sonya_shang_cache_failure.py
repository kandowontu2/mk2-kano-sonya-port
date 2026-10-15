"""Preserve the actual later cache corruption, not a losing-policy stop.

Earlier twelve conservation remains separately qualified. Transport exit0
does not qualify gameplay: the real renderer overrun is retained in full.
"""
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
import inspect_native_campaign_progress as progress
import run_native_sonya_liu_early_leg_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
GAME, PARENT = 10800,33348
OUT = ROOT/'audit_native_sonya_shang_cache_failure_preserved'
RETIRED = ROOT/'audit_native_sonya_shang_cache_failure_retirement'


def prepare(ram):
    need(os.getpid()==PARENT and not OUT.exists(), 'Same original retained RAM host; fresh immutable preservation')
    terminal=json.loads((capture.OUT/'native_terminal.json').read_text())
    result=json.loads((capture.OUT/'result.json').read_text())
    failed=json.loads((capture.OUT/'current_capture_failure.json').read_text())
    guest=json.loads((capture.OUT/'guest_memory_proof.json').read_text())
    preceding_path=ROOT/'audit_native_liu_early_leg_preceding_campaign_checked/report.json'
    preceding=json.loads(preceding_path.read_text())
    identity=terminal['identity']
    need(identity['ProcessId']==GAME and identity['ParentProcessId']==PARENT and
         identity['createdUnix']==1791711060.8420143 and not progress.census.census() and
         terminal['nativeExit']==0 and result['nativeCacheOverrunObserved'] and
         not failed['passed'] and failed['error']=="ValueError('No original cache writes into global state')" and
         not result['actualNaturalTowerClearAccepted'] and not result['fullPortAcceptance'] and
         guest['everyActualByteComparedInRAM'] and guest['bytes']==1048576 and
         hashlib.sha256(ram['guest']).hexdigest().upper()==guest['sha256'] and
         preceding['passed'] and preceding['actualLiveNativeIdentity']==identity and
         preceding['accepted']['completedOpponents']==12 and preceding['accepted']['completeOriginalRows']==1001809 and
         len(preceding['allObservedCategoryFaultsRejected'])==56 and
         not (capture.OUT/'stderr.log').read_text().strip(),
         'Original terminal/cache fault, actual guest and full twelve-match conservation, never a tower pass')
    pins=json.loads((capture.OUT/'input_hashes_before.json').read_text())
    for p,h in preceding['inputHashes'].items():
        need(p not in pins or pins[p]==h, 'Consistent frozen prerequisite hashes')
        pins[p]=h
    need(all(sha(p)==h for p,h in pins.items()), 'All original sources/evidence unchanged before preservation')
    stats=progress.inspect(capture.OUT.name)
    need(not stats['originalNativeStillLive'] and stats['nativeGlobalCacheFailureRows']==146 and
         stats['latestNativeField']['stage']=='14' and stats['latestNativeField']['human']=='18:18' and
         stats['latestNativeField']['cpu']=='6:6' and stats['latestNativeField']['frame']=='480960' and
         stats['lossesByStage']['14']==23 and stats['ownWinReadsByStage']['14']==2 and
         stats['lossesByStage']['12']==0 and stats['ownWinReadsByStage']['12']==2,
         'Entire actual terminal inventory; two isolated Shang rounds are not a match clear')
    raw,images=ram['scope']['RAM_RAW'],ram['scope']['RAM_IMAGES']
    need(set(raw)==set(images) and len(raw)==28 and
         result['actualNativeRGBFrameCallbacks']==467 and result['nativeRGBBytesComparedInRAM']==189788800,
         'Full original transport and bounded28 raw/PIL rasters remain accounted')
    OUT.mkdir()
    with gzip.open(OUT/'original_executed_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=ram['executedHost'],files={p:dict(sha256=h,text=Path(p).read_text())
            for p,h in pins.items() if Path(p).suffix.lower() in ('.py','.lua','.cpp','.h','.cmd')}),stream)
    for folder in (capture.OUT,capture.SOURCE,capture.INIT,capture.OLD_INIT):
        for p in folder.rglob('*'):
            if p.is_file(): pins[str(p.resolve())]=sha(p)
    for p in (Path(__file__).resolve(),Path(progress.__file__),Path(capture.__file__),preceding_path,
              OUT/'original_executed_sources.json.gz'):
        pins[str(p.resolve())]=sha(p)
    source=json.loads((capture.SOURCE/'report.json').read_text())
    report=dict(passed=False,preservationPassed=True,confirmedRealGlobalCacheCorruption=True,
        exactNativeGame=GAME,exactRAMParent=PARENT,actualNativeIdentity=identity,statistics=stats,
        nativeExit=0,hostCaptureFailed=True,transportPassedNotGameplayAcceptance=True,
        actualGlobalStores=146,actualCorruptingNativeFrame=480976,actualObserverStopFrame=480977,
        actualNativeRGBFrameCallbacks=467,nativeRGBBytesComparedInRAM=189788800,
        originalRawRasterInventory={name:dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest().upper()) for name,data in raw.items()},
        originalRawBuffersToRelease=len(raw),originalPILBuffersToRelease=len(images),
        individuallyViewedInThisTrial=False,imagesNotUsedToInferGameplayAcceptance=True,
        earlierTwelveExactConservationAccepted=True,liuEarnedClearIndependentVerificationPending=True,
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False,artAccepted=False,audioAccepted=False,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],inputHashes=pins,
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        publicPlayableChanged=False,goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(preserved=True,confirmedCacheCorruption=True,globalStores=146,
                         rawBuffersToRelease=len(raw),pilBuffersToRelease=len(images),fullPortAcceptance=False)),flush=True)
    return report


def retire():
    need(not RETIRED.exists(), 'Fresh exact original producer retirement')
    saved=json.loads((OUT/'report.json').read_text())
    need(saved['preservationPassed'] and not saved['passed'] and
         all(sha(p)==h for p,h in saved['inputHashes'].items()), 'Entire frozen failure/source inventory unchanged')
    query=subprocess.run(['powershell.exe','-NoProfile','-Command',
        f'Get-CimInstance Win32_Process -Filter "ProcessId={GAME} OR ProcessId={PARENT}" | Select-Object ProcessId | ConvertTo-Json -Compress'],
        capture_output=True,text=True)
    need(query.returncode==0 and not query.stdout.strip() and not query.stderr.strip(),
         'Both exact original processes absent; no review server created')
    RETIRED.mkdir()
    (RETIRED/'report.json').write_text(json.dumps(dict(passed=True,confirmedNativeFailurePreserved=True,
        exactNativeGameRetired=GAME,exactRAMParentRetired=PARENT,originalRawBuffersReleased=28,
        originalPILBuffersReleased=28,noReviewServerCreated=True,
        inputHashes={str(OUT/'report.json'):sha(OUT/'report.json'),str(Path(__file__).resolve()):sha(__file__)},
        fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(retired=True,confirmedNativeFailurePreserved=True,rawBuffersReleased=28,pilBuffersReleased=28)),flush=True)


if __name__=='__main__':
    retire()
