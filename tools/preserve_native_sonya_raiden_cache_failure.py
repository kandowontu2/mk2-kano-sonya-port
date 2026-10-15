"""Preserve real current CPU-Raiden/Sonya cache corruption; retire exact RAM.

Not campaign acceptance. Two passive observers independently record the same
146 original decoder stores. Native zero exit is diagnostic stop, not a fix.
"""
import gzip
import hashlib
import inspect
import json
import os
import re
import socket
import subprocess
from pathlib import Path
import capture_native_kano_laser_sonya_postending_leg_guard_late as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_sonya_raiden_cache_failure_preserved'
RETIRED=ROOT/'audit_native_sonya_raiden_cache_failure_retirement'
PARENT,GAME=186024,176712


def prepare(ram,carrier,server):
    need(not OUT.exists() and os.getpid()==PARENT,'Exact retained original failed native RAM parent')
    folder=capture.OUT
    terminal=json.loads((folder/'native_terminal.json').read_text())
    metadata=json.loads((folder/'result.json').read_text())
    failure=json.loads((folder/'current_capture_failure.json').read_text())
    before=json.loads((folder/'input_hashes_before.json').read_text())
    proof=json.loads((folder/'guest_memory_proof.json').read_text())
    need(terminal['nativeExit']==0 and terminal['identity']['ProcessId']==GAME and
         terminal['identity']['ParentProcessId']==PARENT and metadata['nativeCacheOverrunObserved'] and
         not failure['passed'] and 'No original cache writes into global state' in failure['error'],
         'Actual naturally terminal diagnostic corruption, not successful campaign')
    need(all(sha(p)==h for p,h in before.items()) and proof['everyActualByteComparedInRAM'] and
         hashlib.sha256(ram['guest']).hexdigest().upper()==proof['sha256']==metadata['guestSHA256'] and
         not (folder/'stderr.log').read_text().strip(),
         'Whole actual source-bound initialized guest, frozen inputs and empty error stream')
    with gzip.open(folder/'run.log.gz','rt',encoding='utf-8') as stream: text=stream.read()
    parse=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',s)) for s in text.splitlines() if s.startswith(tag+' ')]
    bad=parse('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE');legacy=parse('MK2_MILEENA_CAMPAIGN_OVERRUN')
    stop=parse('MK2_CURRENT_CAMPAIGN_CACHE_STOP');results=parse('MK2_CURRENT_CAMPAIGN_CACHE_RESULT')
    need(len(bad)==len(legacy)==146 and len(stop)==len(results)==1 and
         stop[0]['global_cache_stores']==results[0]['global_cache_stores']=='146' and
         stop[0]['observer_callback']=='54866' and all(r['observer_callback']=='54865' for r in bad) and
         all(r['frame']=='54865' and r['id']=='18' for r in legacy),
         'Exact real same-frame decoder corruption and automatic diagnostic stop/complete terminal observer census')
    for a,b in zip(bad,legacy):
        need(all(a[k]==b[k] for k in ('pc','at','data','mask','a8','a13','writes','assistance')) and
             a['pc']=='FF838860' and a['mask']=='FFFF' and a['writes']=='0' and a['assistance']=='none' and
             0x01060000<=int(a['at'],16)<=0x01061fff,
             'Two actual independent passive taps agree on every original global decoder store')
    states=parse('MK2_NAT_CAMPAIGN_STATE');live=parse('MK2_NAT_CAMPAIGN_LIVE')
    preceding=[r for r in live if int(r['frame'])<54865][-1]
    need(preceding['stage']=='2' and preceding['human']=='18:18' and preceding['cpu']=='7:7' and
         preceding['health']=='0,115' and all(r['a8']==preceding['human_actor'] and r['a13']==preceding['cpu_main'] for r in bad) and
         any(r['at']=='010601F0' and r['data']=='FFFF' for r in bad) and
         any(r['at']=='01060260' and r['data']=='FFFF' for r in bad),
         'Actual Sonya victim actor/CPU Raiden Main pairing; native cache overwrites human state/Main globals after earned KO')
    need(not parse('MK2_NAT_CAMPAIGN_ENDING_COMPLETED') and not parse('MK2_POSTENDING_COMPLETE'),
         'No ending/fresh join falsely credited to native zero exit')
    raw=ram['scope']['RAM_RAW'];images=ram['scope']['RAM_IMAGES']
    need(len(raw)==len(images)==len(carrier['rgbFrames'])==1 and
         carrier['rgbFrames'][0]['pixels'] is next(iter(raw.values())) and
         hashlib.sha256(carrier['rgbFrames'][0]['pixels']).hexdigest().upper()==carrier['rgbFrames'][0]['header']['sha256'],
         'Exactly one original native selection raster and one PIL rendering; aliases allocate no raw copies')
    provider=ram['scope']['native'];scope,host=capture.prior.prior.functions(provider)
    need(scope['capture'].__code__.co_code==ram['scope']['capture'].__code__.co_code,
         'Entire original actually executed host reconstructed without capture invocation')
    OUT.mkdir()
    with gzip.open(OUT/'original_corrupting_executed_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump(dict(wholeExecutedHost=host,files={p:dict(sha256=h,text=Path(p).read_text()) for p,h in before.items()
                  if Path(p).suffix.lower() in ('.py','.lua','.cpp','.h','.cmd')}),stream)
    pins=dict(before)
    for p in [Path(__file__),*folder.rglob('*'),OUT/'original_corrupting_executed_sources.json.gz']:
        if p.is_file(): pins[str(p.resolve())]=sha(p)
    report=dict(passed=False,preservationPassed=True,confirmedCurrentNativeGraphicsCacheCorruption=True,
        exactNativeGame=GAME,exactRAMParent=PARENT,exactReviewPort=server.server_port,nativeExit=0,
        diagnosticStoppedAutomatically=True,originalTransportPassNotGameplayAcceptance=True,
        actualFailureCallback=54865,actualGlobalCacheStores=146,actualSourceDecoderPC='FF838860',
        actualTwoObserverStoreAgreement=True,actualVictimIdentity=18,actualCPUIdentity=7,
        actualPrecedingNativeField=preceding,actualDecoderStores=bad,actualLegacyDecoderStores=legacy,
        actualFailureIsCurrentNotHistorical=True,currentGuestProof=proof,
        actuallyReachedStages=metadata['actualStages'],actualNativeRasterCallbacks=metadata['actualNativeRGBFrameCallbacks'],
        originalRawBuffersToRelease=1,originalPILBuffersToRelease=1,
        individuallyViewedNativeSelectionRaster=carrier['rgbFrames'][0]['header'],
        firstTwoStagePhysicalReplayNotFullyQualified=True,
        originalRemainingWorkGroups=json.loads((capture.SOURCE/'report.json').read_text())['originalRemainingWorkGroups'],
        originalNaturalIntegrationRequirements=json.loads((capture.SOURCE/'report.json').read_text())['originalNaturalIntegrationRequirements'],
        inputHashes=pins,endingReached=False,postEndingJoinAccepted=False,fullPortAcceptance=False,goalStatus='active',
        nextAction='Trace actual Sonya-victim/CPU-Raiden native animation root, stream, descriptor and caller stack before frame54865; fix the source lookup/ABI, not by suppressing damage/CPU/finisher/caches.',
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(preserved=True,currentGameDefect=True,actualGlobalStores=146,nativeExit=0,campaignAccepted=False)),flush=True)


def retire():
    need(not RETIRED.exists(),'Fresh exact current corrupting-trial RAM retirement')
    report=json.loads((OUT/'report.json').read_text())
    need(report['preservationPassed'] and not report['passed'] and report['confirmedCurrentNativeGraphicsCacheCorruption'] and
         all(sha(p)==h for p,h in report['inputHashes'].items()),'Actual current failed outcome and all executed sources preserved')
    query=f'Get-CimInstance Win32_Process -Filter "ProcessId={PARENT} OR ProcessId={GAME}" | Select-Object ProcessId | ConvertTo-Json -Compress'
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(result.returncode==0 and not result.stdout.strip() and not result.stderr.strip(),'Both exact original producers actually absent')
    with socket.socket() as connection:
        connection.settimeout(1);need(connection.connect_ex(('127.0.0.1',report['exactReviewPort']))!=0,'Exact original native preview port closed')
    dirs=[capture.OUT,capture.INIT,capture.SOURCE,OUT]
    files=[p for d in dirs for p in d.rglob('*') if p.is_file()]
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),
         'No raw media/ROM/build/archive in this failed current batch')
    RETIRED.mkdir()
    (RETIRED/'report.json').write_text(json.dumps(dict(passed=True,failedCurrentGameOutcomePreserved=True,
        exactNativeGameRetired=GAME,exactRAMParentRetired=PARENT,exactReviewPortClosed=report['exactReviewPort'],
        originalRawBuffersReleased=1,originalPILBuffersReleased=1,batchEvidenceLogicalBytes=sum(p.stat().st_size for p in files),
        inputHashes={str(p.resolve()):sha(p) for p in [Path(__file__),*files]},
        newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,fullPortAcceptance=False,goalStatus='active'),indent=2)+'\n')
    print(json.dumps(dict(retired=True,currentCacheFailurePreserved=True,newRawMedia=0)),flush=True)


if __name__=='__main__': retire()
