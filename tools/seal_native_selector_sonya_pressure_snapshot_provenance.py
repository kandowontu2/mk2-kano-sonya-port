"""Final whole provenance: include both storage successor sources themselves."""
import json
import subprocess
from pathlib import Path
import seal_native_selector_sonya_pressure_snapshot_metadata as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_snapshot_sealed.json'


def execute():
    need(not OUT.exists(),'Fresh immutable full pressure snapshot source/storage seal')
    proof=json.loads(previous.OUT.read_text());pins=dict(proof['inputHashes'])
    capture=previous.previous.capture;held=capture.NATIVE_HANDLES[capture.KEY]
    need(proof['passed']and held['process'].poll()==proof['nativeExit']==0 and
         held['identity']==proof['actualNativeIdentity']and held['identity']['ProcessId']==47004 and
         not capture.reference.base.choices.current.prior.identity.census(),
         'Original47004 remains terminal, no pending or substituted native game')
    need(proof['completeCurrentScanoutBindingPassed']and proof['wholeCurrentSnapshotsCaptured']==1800 and
         proof['sourceExactSavedPassCPUAndDMAReplayPassed']and proof['actualReplayedPasses']==1746 and
         proof['wholeExactPassVRAMWords']==457703424 and proof['exactCurrentDisplayedPixels']==182880000 and
         proof['effectiveFaultsRejected']==14 and len(proof['limitedActualVisualInspection']['selectedFrames'])==12,
         'All actual whole scanout/pass positives, fourteen faults and twelve source-bound reviewed views retained')
    need(all(sha(p)==h for p,h in pins.items()),'Every whole original input/source/evidence pin unchanged')
    files=(Path(__file__).resolve(),Path(previous.__file__).resolve(),previous.OUT)
    entries=[]
    for p in files:
        key=str(p);h=sha(p);need(key not in pins or pins[key]==h,'Never replace prior immutable source/evidence');pins[key]=h
        before=dict(sha256=h,logicalBytes=p.stat().st_size,storedBefore=previous.previous.storage.stored(p))
        call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True)
        need(call.returncode==0 and sha(p)==h,'Every complete successor source/receipt intact after exact LZX')
        entries.append(dict(path=str(p),**before,storedAfter=previous.previous.storage.stored(p)))
    need(previous.previous.storage.source.verify()['passed']and all(sha(p)==h for p,h in pins.items()),
         'Final all15 compiled-source sync and whole provenance inventory')
    value=dict(proof,inputHashes=pins,fullInputPins=len(pins),inputMismatches=0,
        fullStorageSuccessorSourceProvenanceAccepted=True,additionalExactSourceCompression=entries,
        originalMetadataStorageReportSHA256=sha(previous.OUT),finalSealedReport=True)
    OUT.write_text(json.dumps(value,indent=2)+'\n');h=sha(OUT)
    call=subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(OUT)],capture_output=True)
    need(call.returncode==0 and sha(OUT)==h,'Whole final finite pressure snapshot evidence seal unchanged')
    return value
