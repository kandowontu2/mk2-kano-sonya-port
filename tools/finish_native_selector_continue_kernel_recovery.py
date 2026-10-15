"""Finish original recovered run using its real stderr hardlink, not replay.

Keep the preceding missing-sidecar exception and every rejected report. The
recovery report has passed the whole original six-fault capture gate already.
"""
import json
from pathlib import Path
import qualify_native_selector_continue_paired_kernel as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha


def finish(state,cases,handles):
    key='kano_p2_to_sonya';folder,text,images,old=cases[key]
    out=ROOT/'audit_native_selector_continue_kano_p2_to_sonya_kernel_birth_recovery'
    report=json.loads((out/'report.json').read_text())
    need(old['passed']is False and report['passed']and len(report['actualFaultsRejected'])==6 and
         handles[key]['process'].poll()==0 and all(sha(p)==h for p,h in report['inputHashes'].items()),
         'Unchanged recovered original whole capture positive and exact six actual faults')
    need(not(out/'stderr.log').exists()and (folder/'stderr.log').stat().st_size==0,'Exact original empty stderr, missing sidecar only')
    (out/'stderr.log').hardlink_to(folder/'stderr.log')
    need((out/'stderr.log').samefile(folder/'stderr.log'),'Same original stderr inode, not a synthesized clean log')
    proof=ROOT/'audit_native_selector_continue_kernel_sidecar_binding'
    need(not proof.exists(),'Fresh sidecar provenance receipt');proof.mkdir()
    (proof/'report.json').write_text(json.dumps(dict(passed=True,sourceOnlyAccepted=True,
        originalStderr=str(folder/'stderr.log'),recoveryStderr=str(out/'stderr.log'),sameFileIdentity=True,
        originalCaptureStillPassedFalse=True,missingSidecarExceptionPreserved=True,
        inputHashes={str(p.resolve()):sha(p)for p in (Path(__file__),Path(previous.__file__),out/'report.json',folder/'stderr.log')},
        newNativeBoots=0,newRawMedia=0,fullPortAcceptance=False),indent=2)+'\n')
    state['contract'].DEPENDENCIES.extend([Path(__file__),proof/'report.json'])
    qualified=state['qualify'](out,text,images,report,'kano',2,'sonya')
    pixels=state['pixel_check'](out,text,images,'kano',2,'sonya')
    controls=state['control_check'](out,text,'kano',2,'sonya')
    state['COMPLETED'].append(key)
    print(json.dumps(dict(passed=True,key=key,stateRasterFaults=len(qualified['actualFaultsRejected']),
        controlFaults=len(controls['actualControlFaultsRejected']),extraPixelFaults=len(pixels['additionalActualImageFaultsRejected']),
        nativeReplay=False,fullPortAcceptance=False)),flush=True)
    return dict(folder=out,text=text,images=images,report=report,qualified=qualified,pixels=pixels,controls=controls)
