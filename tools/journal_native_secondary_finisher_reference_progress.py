"""Preserve full goal scope after two genuinely executed original variants.

No promotion, guest/source edit, build, ROM duplication or raw-media output.
Strict filler census is planning evidence, not allocated implementation space.
"""
import ctypes
import gzip
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
import audit_native_secondary_finisher_reference as reference
import capture_native_secondary_kano_reference as transport

ROOT=reference.ROOT
OUT=ROOT/'audit_native_secondary_finisher_reference_progress'


def allocation(path):
    kernel=ctypes.WinDLL('kernel32',use_last_error=True)
    call=kernel.GetCompressedFileSizeW
    call.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_ulong)]
    call.restype=ctypes.c_ulong
    high=ctypes.c_ulong();low=call(str(path.resolve()),ctypes.byref(high))
    if low==0xffffffff and ctypes.get_last_error():raise ctypes.WinError(ctypes.get_last_error())
    return(high.value<<32)|low


def main():
    reference.need(not OUT.exists()and not transport.census()and not reference.native.census(),
                   'Fresh journal after actual native terminal states, no games live')
    names=['audit_native_secondary_finisher_reference','audit_native_kano_secondary_input',
           'audit_native_secondary_kano_reference','audit_native_secondary_kano_raster_checked',
           'audit_native_secondary_kano_command_checked','audit_native_secondary_kano_guarded_command',
           'audit_native_secondary_guard_preflight_failure','audit_native_secondary_kano_source_distance',
           'audit_native_kano_laser_checker_failure','audit_native_kano_laser_checker_failure_2',
           'audit_native_kano_laser_reference_checked','audit_native_sonya_secondary_input',
           'audit_native_secondary_sonya_source_distance','audit_native_sonya_orb_reference_checked',
           'audit_native_secondary_reference_journal_failure']
    paths=[ROOT/name/'report.json'for name in names]
    records={name:json.loads(path.read_text())for name,path in zip(names,paths)}
    for name in ('audit_native_kano_secondary_input','audit_native_sonya_secondary_input',
                 'audit_native_kano_laser_reference_checked','audit_native_sonya_orb_reference_checked'):
        record=records[name]
        reference.need(record['passed']and all(reference.sha(p)==h for p,h in record['inputHashes'].items()),
                       'Actually checked source/runtime provenance remains frozen: '+name)
    for name in ('audit_native_kano_laser_reference_checked','audit_native_sonya_orb_reference_checked'):
        record=records[name]
        reference.need(record['originalFiniteActionReferenceAccepted']and
                       not record['portSecondFatalityImplemented']and not record['fullPortAcceptance']and
                       record['nativeExit']==0 and record['actualFrameReview']['all15WholeFramesActuallyViewed'],
                       'Both original finite action receipts, not port acceptance')
    guest=reference.current.expected()
    source=reference.MK2.read_bytes()
    dispatch=reference.inspect_dispatch(guest,source)
    free=[]
    for match in re.finditer(b'\xff{256,}',guest[0xf0000:]):
        start=(0xf0000+match.start()+3)&~3
        end=(0xf0000+match.end())&~3
        if end-start>=256 and source[start:end]==b'\xff'*(end-start):
            free.append(dict(byteStart=f'{start:05X}',byteEndExclusive=f'{end:05X}',
                             bytes=end-start,bitAddress=f'{0xff800000+start*8:08X}'))
    free.sort(key=lambda r:r['bytes'],reverse=True)
    scope=records['audit_native_secondary_finisher_reference']
    evidence=[p for name in names for p in(ROOT/name).rglob('*')if p.is_file()]
    raw=[p for p in evidence if p.suffix.lower()in('.png','.bmp','.wav','.avi','.mp4','.bin','.exe','.zip')]
    snapshots=records['audit_native_secondary_reference_journal_failure']['olderActualNativeAutomaticSnapshots']
    reference.need({str(p.resolve())for p in raw}=={r['path']for r in snapshots}and
                   all(reference.sha(r['path'])==r['sha256']for r in snapshots),
                   'Only four preserved older native str180 terminal snapshots; no new ROM/build or this-continuation media files')
    paths.extend([Path(__file__),reference.SOURCE,reference.PAYLOAD,
                  ROOT/reference.current.NAME/'mkport_candidate.exe',
                  ROOT/reference.current.NAME/'build-info.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd',
                  ROOT/'audit_latest_native_launcher/report.json',*[Path(r['path'])for r in snapshots]])
    pins={str(p.resolve()):reference.sha(p)for p in paths}
    report=dict(passed=True,observedUTC=datetime.now(timezone.utc).isoformat(),
        previousGoalTurnClassification='no progress: user-requested status restatement only',
        thisGoalTurnClassification='progress: actual original Kano eye laser and Sonya magenta orb physically earned/activated at independently source-verified ranges; two451field traces and all30 actual frames checked; both port variants remain unimplemented',
        fullGoalComplete=False,fullPortAcceptance=False,goalStatus='active',
        originalNaturalIntegrationRequirements=scope['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=scope['originalRemainingWorkGroups'],
        acceptedPriorWorkNotReset=['Current selection/ladder/identity/names/grounding/shadow finite proofs.',
                                  'Current human-special matrix and earlier native CPU/ordinary/guard/mirror/campaign/stage/secret proofs.',
                                  'Recent CPU finisher table and approach repairs, current Sonya attract audio and latest runnable CMD.'],
        candidate=reference.current.NAME,
        candidateGuestSHA256=hashlib.sha256(guest).hexdigest().upper(),
        currentAddedFatalityChoicesStillAliased=dispatch['added'],
        originalKanoLaserReference=records['audit_native_kano_laser_reference_checked']['accepted'],
        originalSonyaOrbReference=records['audit_native_sonya_orb_reference_checked']['accepted'],
        originalRuntimeChecksFaultRejections=30,originalInputFaultRejections=18,
        actualNativeOriginalGamesThisContinuation=2,actualNativeOriginalFramesReviewed=30,
        bothOriginalNativeProcessesTerminal0=True,noNativeGamesStillRunning=True,
        allExecutedFailuresAndSourceVersionsPreserved=True,
        secondPortFatalitiesImplemented=False,
        originalSourceSpaceCensus=dict(largestStrictFillerRanges=free[:12],
            allocationAccepted=False,limitation='Actual original and current FF filler only. Must still qualify source reservations, pointers and opcode/storage boundaries before allocating a finisher.'),
        currentPlayableChanged=False,gameSourceChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        oldBuildsDeleted=0,compilerCacheAbsent=not(ROOT/'mame-mkp/build/mingw-gcc').exists(),
        evidenceStorage=dict(files=len(evidence),logicalBytes=sum(p.stat().st_size for p in evidence),
                             allocatedBytes=sum(allocation(p)for p in evidence),
                             completeNativeRGBReviewedInRAMAndReleased=True,
                             thisContinuationRawRGBROMAndGameCopiesWritten=False,
                             olderNativeAutomaticTerminalSnapshotsConserved=snapshots),
        inputHashes=pins,
        nextAction='Implement genuine distinct Kano eye-laser and Sonya magenta-orb native MKII finishers from the proven original choreography. Use own typed attacker/effect/victim streams and MKII process/cleanup/input rules; conserve all stock and installed first choices and separately qualify CPU per-variant approach and dispatch. Then complete remaining full-scope audio/stage/secret/post-ending checks, combined current regression and matching finished ZIP.',
        limitations=['Original finite references are not implemented MKII variants.',
                     'Complete new finisher PCM/audio and following rematch cleanup remain unproved.',
                     'Kano victim palette was sampled at pose changes; Sonya both actor banks were continuous.',
                     'MKII has no Run button: Sonya input must be adapted deliberately, not copied as unusable donor grammar.',
                     'No finished release or broad universal completion claim.'])
    reference.need(len(report['originalNaturalIntegrationRequirements'])==14 and
                   len(report['originalRemainingWorkGroups'])==6,'Full original14+6 scope intact')
    reference.need(all(reference.sha(p)==h for p,h in pins.items()),'All current source/receipts/assets conserved')
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(OUT/'executed_journal_source.json.gz','wt',encoding='utf-8')as stream:
        json.dump(dict(path=str(Path(__file__).resolve()),sha256=reference.sha(__file__),source=Path(__file__).read_text()),stream)
    print(json.dumps(dict(passed=True,originalNativeFramesReviewed=30,originalRuntimeFaults=30,
                          currentPlayableChanged=False,newBuilds=0,newROMCopies=0,
                          evidenceStorage=report['evidenceStorage'],largestFillerRanges=free[:5],
                          goalStatus='active',secondPortFatalitiesImplemented=False)))


if __name__=='__main__':main()
