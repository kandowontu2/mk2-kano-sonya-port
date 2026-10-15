"""Current finite Ring native branches plus saved display/complete source audio.

All original scope remains active. Different record schemas are not absent
native branch execution: accept the actual ungated entries/registers while
retaining the rejected older full phase/port/startup checker explicitly.
"""
import json
from pathlib import Path
import seal_native_selector_cpu_rings_snapshot as display
import qualify_native_selector_cpu_rings_native_branches as branches

ROOT,need,sha=display.ROOT,display.need,display.sha
OUT=ROOT/'audit_native_selector_cpu_rings_current_evidence_sealed'


def execute(state):
    need(not OUT.exists(),'Fresh finite current Ring combined evidence')
    paths=[m.OUT/'report.json'for m in (display,branches)]
    rendering,mechanics=(json.loads(p.read_text())for p in paths)
    held=display.capture.NATIVE_HANDLES[display.capture.KEY]
    need(rendering['passed']and mechanics['passed']and held['process'].poll()==0 and
         held['identity']==rendering['actualNativeIdentity']==mechanics['actualNativeIdentity'],
         'Both whole current evidence sets belong to the same retained terminal0 native')
    pins={}
    for proof in (rendering,mechanics):
        need(proof['requirements']==rendering['requirements']and proof['remainingGroups']==rendering['remainingGroups']and
             len(proof['requirements'])==14 and len(proof['remainingGroups'])==6,
             'Complete original fourteen requirements and six groups retained')
        for p,h in proof['inputHashes'].items():
            need(p not in pins or pins[p]==h,'Whole source/evidence pins agree without waivers');pins[p]=h
    need(mechanics['threeSourceExecutedBlockHitContactsAccepted']and
         [(r['contact'],r['blocked'],r['damage'])for r in mechanics['actualNativeBranchContacts']]==
         [(1841,True,6),(2196,False,22),(3051,False,22)]and
         len(mechanics['effectiveSourceBranchFaultsRejected'])==24 and
         mechanics['originalLegacyMechanicsRejectionPreserved']and
         not mechanics['completeLegacyPhysicalControlPortContractAccepted'],
         'Three actual source-bound native decisions and twenty-four effective faults; older port gate not accepted')
    need(rendering['actualRGBFrames']==319 and rendering['actualViewedFrames']==18 and
         rendering['completeStereoFrames']==1580160 and rendering['differentChannelSamples']==0 and
         rendering['finiteThreeCPURingSavedDisplayAndWholeRecordedAudioAccepted'],
         'Full saved rendering/actual views/entire sound stream accepted, not a subset')
    for p in (*paths,Path(__file__)):
        key=str(p.resolve());h=sha(p);need(key not in pins or pins[key]==h,'No mutable executed sources or saved results');pins[key]=h
    need(all(sha(p)==h for p,h in pins.items()),'All whole current source/native/media/evidence input hashes revalidated')
    value=dict(passed=True,goalStatus='active',actualNativeIdentity=held['identity'],nativeExit=0,
        completeFiniteDisplayAudioReportSHA256=sha(paths[0]),nativeBranchesReportSHA256=sha(paths[1]),
        actualRGBFrames=319,actualViewedFrames=18,exactWholeDisplayedPixels=32410400,
        exactWholeVRAMWords=83623936,completePCMCallbacks=1646,completeStereoFrames=1580160,
        actualNativeBranchContacts=mechanics['actualNativeBranchContacts'],
        effectiveDisplayOwnershipFaults=24,effectiveSourceAudioFaults=30,effectiveSourceBranchFaults=24,
        inputHashes=pins,requirements=rendering['requirements'],remainingGroups=rendering['remainingGroups'],
        finiteNativeRingBranchesSavedDisplayWholeSourceAudioAccepted=True,
        legacyNativeBlockSchemaMissing=True,actualUngatedNativeBranchExecutionMissing=False,
        firstCompleteStartupParentContractAccepted=False,completeLegacyPhysicalControlPortContractAccepted=False,
        wholeOriginalPhaseContractAccepted=False,allArenaCPUContextsAccepted=False,
        interPassEraseAccepted=False,heardAudioQualityAccepted=False,fullPortAcceptance=False,
        publicPlayableChanged=False,newNativeGames=0,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(value,indent=2)+'\n')
    print('PASS finite current Ring native contacts +319 displayed passes +18 views +whole source sound; all scope active',flush=True)
    return value
