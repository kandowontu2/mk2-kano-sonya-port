"""Release the actual29 buffers and both temporary local review listeners.

The inherited retirement helper was not run: its no-review-server claim is
not true for this trial. Preserve the real failed PIL review and successful
array adapter, then verify exact original native/RAM producers are absent.
"""
import gc
import hashlib
import json
import os
import socket
import subprocess
from pathlib import Path
import seal_native_sonya_shang_actual_cause as preserved
import capture_native_sonya_shang_cache_cause as capture

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
OUT=ROOT/'audit_native_sonya_shang_actual_cause_ram_release'
RETIRED=preserved.RETIRED
CAUSE=ROOT/'audit_native_shang_actual_cache_cause_checked/report.json'


def release(ram,server,frames):
    need(os.getpid()==35228 and not OUT.exists() and not capture.core.base.census.census(),
         'Same original retained RAM host, native terminal and fresh release receipt')
    paths=[preserved.OUT/'report.json',CAUSE]
    saved,cause=[json.loads(p.read_text()) for p in paths]
    need(saved['preservationPassed'] and not saved['passed'] and cause['passed'] and
         cause['nativeCauseAccepted'] and not cause['nativeRepairAccepted'] and
         all(sha(p)==h for proof in (saved,cause) for p,h in proof['inputHashes'].items()),
         'All frozen real corruption/actual cause evidence unchanged before release')
    raw,images=ram['scope']['RAM_RAW'],ram['scope']['RAM_IMAGES']
    need(len(raw)==len(images)==29 and set(raw)==set(images) and
         set(frames)=={0} and server.server_port==54905 and
         hashlib.sha256(ram['guest']).hexdigest().upper()==
             json.loads((capture.OUT/'guest_memory_proof.json').read_text())['sha256'] and
         all(len(raw[n])==saved['originalRawRasterInventory'][n]['bytes'] and
             hashlib.sha256(raw[n]).hexdigest().upper()==saved['originalRawRasterInventory'][n]['sha256']
             for n in raw),'Every actual original RAM buffer remains intact and accounted')
    name='shang_victim_provenance_age1.png'
    viewed_rgb_sha=hashlib.sha256(images[name].tobytes()).hexdigest().upper()
    server.shutdown();server.server_close()
    for port in (51135,54905):
        with socket.socket() as probe:probe.bind(('127.0.0.1',port))
    frames.clear()
    for im in images.values():im.close()
    images.clear();raw.clear();ram.clear();gc.collect()
    need(not ram and not images and not raw and not frames,'All29 raw/PIL buffers and one review-array reference released')
    OUT.mkdir()
    report=dict(passed=True,exactRAMParent=35228,originalRawBuffersReleased=29,originalPILBuffersReleased=29,
        reviewArrayReferencesReleased=1,reviewServerPortsCreated=[51135,54905],bothReviewListenersClosed=True,
        actualFirstReviewFailure="TypeError: a bytes-like object is required, not 'Image'",
        originalReviewHelperUnmodified=True,successfulReviewAdapter='numpy.asarray of the same original captured PIL frame',
        individuallyViewedNativeRasters=[dict(name=name,rgbSHA256=viewed_rgb_sha)],
        nativeRepairAccepted=False,artAccepted=False,audioAccepted=False,fullPortAcceptance=False,
        inputHashes={str(p.resolve()):sha(p) for p in (*paths,Path(__file__).resolve(),
                    ROOT/'tools/native_ram_raster_review.py')},newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(releasedRaw=29,releasedPIL=29,bothReviewListenersClosed=True,fullPortAcceptance=False)),flush=True)
    return report


def retire():
    need(not RETIRED.exists(),'Fresh exact original producer retirement receipt')
    paths=[preserved.OUT/'report.json',CAUSE,OUT/'report.json']
    saved,cause,released=[json.loads(p.read_text()) for p in paths]
    need(saved['preservationPassed'] and not saved['passed'] and cause['passed'] and released['passed'] and
         released['bothReviewListenersClosed'] and released['originalRawBuffersReleased']==29 and
         released['originalPILBuffersReleased']==29 and
         all(sha(p)==h for proof in (saved,cause,released) for p,h in proof['inputHashes'].items()),
         'Whole actual failed campaign, confirmed diagnosis and all29 buffer release receipts retained')
    query=subprocess.run(['powershell.exe','-NoProfile','-Command',
        'Get-CimInstance Win32_Process -Filter "ProcessId=2008 OR ProcessId=35228" | Select-Object ProcessId | ConvertTo-Json -Compress'],
        capture_output=True,text=True)
    need(query.returncode==0 and not query.stdout.strip() and not query.stderr.strip() and
         not capture.core.base.census.census(),'Both exact original processes absent; no emulator still running')
    for port in (51135,54905):
        with socket.socket() as probe:probe.bind(('127.0.0.1',port))
    RETIRED.mkdir()
    report=dict(passed=True,confirmedNativeFailurePreserved=True,nativeCauseAccepted=True,nativeRepairAccepted=False,
        exactNativeGameRetired=2008,exactRAMParentRetired=35228,originalRawBuffersReleased=29,originalPILBuffersReleased=29,
        reviewArrayReferencesReleased=1,reviewServersCreated=2,bothReviewListenersClosed=True,
        inheritedNoReviewServerRetirementNotExecuted=True,
        inputHashes={str(p.resolve()):sha(p) for p in (*paths,Path(__file__).resolve())},
        fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active')
    (RETIRED/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(retired=True,rawBuffersReleased=29,pilBuffersReleased=29,nativeCauseAccepted=True,
                         nativeRepairAccepted=False,fullPortAcceptance=False)),flush=True)
    return report


if __name__=='__main__':retire()
