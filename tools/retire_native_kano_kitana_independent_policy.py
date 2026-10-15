"""Exact failed physical policy retirement with authenticated RAM release.

Preserve the entire actual terminal/source/guest/raster inventory. Neither
controller losses nor an explicit stop are labelled an engine defect/pass.
"""
import argparse
import gzip
import hashlib
import json
import re
import subprocess
import urllib.request
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_kitana_independent_host as capture
import check_native_scorpion_guard_first_five_prefix as reader
import inspect_native_campaign_progress as progress

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_kano_kitana_reactive_independent_failed_policy_preserved'
RETIRED=ROOT/'audit_native_kano_kitana_reactive_independent_failed_policy_retirement'
GAME,PARENT=156012,173688


def metadata():
    session=json.loads((capture.HOST/'review_session.json').read_text())
    need(session['hostPID']==PARENT and session['sourceSHA256']==sha(capture.__file__),
         'Exact original independent host and read-only RAM review service')
    with urllib.request.urlopen(f"http://127.0.0.1:{session['port']}/metadata",timeout=10)as response:
        actual=json.load(response)
    need(actual['hostPID']==PARENT,'Same actual live retained RAM owner')
    return session,actual


def stop():
    path=capture.OUT/'explicit_unsuccessful_physical_policy_stop.json'
    need(not path.exists(),'Fresh exact failed reactive policy stop')
    identity=json.loads((capture.OUT/'native_identity.json').read_text())
    need(identity['ProcessId']==GAME and identity['ParentProcessId']==PARENT and
         identity in progress.census.census(),'Exact actual native birth/path/parent/command still live')
    lines=reader.complete_lines(capture.OUT/'run.log.gz')
    parse=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',l))for l in lines if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    losses=[r for r in parse('LOSS')if r['stage']=='3']
    own=[r for r in parse('WIN')if r['stage']=='3'and r['slot']=='1']
    latest=parse('LIVE')[-1]
    need(len(losses)>=30 and not own and latest['human']=='17:17'and latest['cpu']=='4:4'and latest['stage']=='3'and
         not any(r['stage']=='4'for r in parse('STAGE'))and
         not any(l.startswith(('MK2_CURRENT_CAMPAIGN_CACHE_FAILURE ','MK2_MILEENA_CAMPAIGN_OVERRUN '))for l in lines),
         '30+ genuine failed Kitana attempts, no owned round/next stage or observed cache corruption')
    path.write_text(json.dumps(dict(passed=False,physicalPolicyUnsuccessful=True,exactNativeIdentity=identity,
        actualFailedKitanaAttempts=len(losses),actualOwnedKitanaRounds=own,latestObservedNativeField=latest,
        stoppedSolelyForObservationTimeout=False,engineDefectNotInferredFromControllerLosses=True,
        inputHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(reader.__file__)):sha(reader.__file__)},
        fullPortAcceptance=False),indent=2)+'\n')
    need(identity in progress.census.census(),'Exact native rechecked immediately before the owned policy stop')
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Stop-Process -Id {GAME} -ErrorAction Stop'],
        capture_output=True,text=True)
    need(result.returncode==0 and not result.stderr.strip(),'Only the exact unsuccessful-policy native process stopped')
    print(json.dumps(dict(explicitStop=True,nativePID=GAME,failedKitanaAttempts=len(losses))),flush=True)


def preserve():
    need(not OUT.exists(),'Fresh complete failed-policy preservation')
    terminal_path=capture.OUT/'native_terminal.json'
    terminal=json.loads(terminal_path.read_text())
    result=json.loads((capture.OUT/'result.json').read_text())
    failure=json.loads((capture.OUT/'current_capture_failure.json').read_text())
    stopped=json.loads((capture.OUT/'explicit_unsuccessful_physical_policy_stop.json').read_text())
    guest=json.loads((capture.OUT/'guest_memory_proof.json').read_text())
    pins=json.loads((capture.OUT/'input_hashes_before.json').read_text())
    source=json.loads((capture.SOURCE/'report.json').read_text())
    need(terminal['identity']==stopped['exactNativeIdentity']and terminal['nativeExit']==0xffffffff and
         not result['passed']and not failure['passed']and stopped['physicalPolicyUnsuccessful']and
         guest['everyActualByteComparedInRAM']and guest['bytes']==1048576 and
         not any(q==terminal['identity']for q in progress.census.census())and
         all(sha(p)==h for p,h in pins.items()),'Exact original failed native terminal, whole actual guest and every source pin')
    session,actual=metadata()
    need(actual['nativeTerminalRecorded']and not actual['nativeCensus'],'Actual independent native terminal and retained RAM inventory')
    build=json.loads((ROOT/capture.previous.original.repaired.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    _,host=capture.functions(SimpleNamespace(GUEST_SHA=build['expected_guest_sha256'],
        EXE_SHA=build['executable_sha256'],PAYLOAD_SHA=build['payload_sha256']))
    need(hashlib.sha256(host.encode()).hexdigest().upper()==guest['transportSourceSHA256'],
         'Entire original executed host independently reconstructed and bound to actual guest receipt')
    OUT.mkdir()
    with gzip.open(OUT/'original_executed_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump(dict(wholeExecutedHost=host,files={p:dict(sha256=h,text=Path(p).read_text())for p,h in pins.items()
            if Path(p).suffix.lower()in('.py','.lua','.cpp','.h','.cmd')}),stream)
    bound=dict(pins)
    for folder in (capture.OUT,capture.SOURCE,capture.INIT,capture.OLD_INIT):
        bound.update({str(p.resolve()):sha(p)for p in folder.rglob('*')if p.is_file()})
    for p in (OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)
    report=dict(passed=False,preservationPassed=True,failedPhysicalPolicyPreserved=True,
        exactNativeGame=GAME,exactRAMParent=PARENT,nativeExit=terminal['nativeExit'],
        actualFailedKitanaAttempts=stopped['actualFailedKitanaAttempts'],originalRawRasterInventory=actual['frames'],
        originalRawBuffersToRelease=len(actual['frames']),individuallyViewedInThisTrial=False,
        imagesNotUsedToInferGameplayAcceptance=True,inputHashes=bound,
        originalNaturalIntegrationRequirements=source['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=source['originalRemainingWorkGroups'],fullPortAcceptance=False,
        engineDefectNotInferredFromControllerLosses=True,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        publicPlayableChanged=False,goalStatus='active')
    report_path=OUT/'report.json';report_path.write_text(json.dumps(report,indent=2)+'\n')
    authorization=capture.OUT/'ram_release_authorization.json'
    need(not authorization.exists(),'One exact source/report-bound release authorization')
    authorization.write_text(json.dumps(dict(releaseAuthorized=True,exactHostPID=PARENT,
        nativeTerminalSHA256=sha(terminal_path),inputHashes={str(report_path):sha(report_path),
            str(Path(__file__).resolve()):sha(__file__)}),indent=2)+'\n')
    request=urllib.request.Request(f"http://127.0.0.1:{session['port']}/release",method='POST',
        headers={'Authorization':'Bearer '+session['releaseToken']})
    with urllib.request.urlopen(request,timeout=10)as response:need(response.status==200,'Same original RAM service released buffers')
    print(json.dumps(dict(preserved=True,rawBuffersReleased=len(actual['frames']),nativePID=GAME)),flush=True)


def retire():
    need(not RETIRED.exists(),'Fresh exact independent host retirement receipt')
    saved_path=OUT/'report.json';saved=json.loads(saved_path.read_text())
    released_path=capture.OUT/'ram_buffers_released.json';released=json.loads(released_path.read_text())
    terminal_path=capture.OUT/'native_terminal.json';terminal=json.loads(terminal_path.read_text())
    need(saved['preservationPassed']and released['released']and released['hostPID']==PARENT and
         released['rawBuffers']==released['pilBuffers']==saved['originalRawBuffersToRelease']and
         all(sha(p)==h for p,h in saved['inputHashes'].items())and
         not any(q==terminal['identity']for q in progress.census.census()),
         'Entire failed evidence conserved and every exact retained raw/PIL buffer released')
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',
        f'Get-CimInstance Win32_Process -Filter "ProcessId={PARENT}" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress'],
        capture_output=True,text=True)
    need(result.returncode==0 and not result.stdout.strip()and not result.stderr.strip(),'Original independent RAM host actually exited')
    session=json.loads((capture.HOST/'review_session.json').read_text())
    try:urllib.request.urlopen(f"http://127.0.0.1:{session['port']}/metadata",timeout=2)
    except urllib.error.URLError:pass
    else:raise ValueError('Original independent RAM review service still running')
    RETIRED.mkdir()
    report=dict(passed=True,exactNativeGameRetired=GAME,exactRAMParentRetired=PARENT,
        originalRawBuffersReleased=released['rawBuffers'],originalPILBuffersReleased=released['pilBuffers'],
        originalReviewServerClosed=True,failedPhysicalPolicyPreserved=True,
        inputHashes={str(p):sha(p)for p in (saved_path,released_path,terminal_path,Path(__file__).resolve())},
        fullPortAcceptance=False,goalStatus='active')
    (RETIRED/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(retired=True,rawBuffersReleased=released['rawBuffers'],reviewServerClosed=True)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('stop','preserve','retire'));args=parser.parse_args()
    {'stop':stop,'preserve':preserve,'retire':retire}[args.action]()
