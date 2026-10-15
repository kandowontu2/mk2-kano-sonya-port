"""Full original goal retained after actual compiled/native corruption repair."""
import json, subprocess
from pathlib import Path
import save_subzero_native_root_cause_progress_v4847 as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
PARENT=previous.OUT/'progress.json'
OUT=ROOT/'audit_v4869_native_subzero_repair_progress'

def main():
    need(not OUT.exists(),'Fresh full-scope additive journal')
    parent=json.loads(PARENT.read_text())
    need(parent['goalStatus']=='active' and len(parent['remaining'])==5,'All five original unfinished requirements retained')
    inherited={}
    base=json.loads(previous.BASE.read_text());inherited.update(base['inputHashes'])
    parents=previous.PARENTS+[PARENT]
    for path in parents:
        for p,h in json.loads(path.read_text())['newInputHashes'].items():
            need(p not in inherited or inherited[p]==h,'Consistent inherited immutable evidence');inherited[p]=h
    pins={}
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Exact actual current evidence byte')
        need(key not in inherited or inherited[key]==digest,'No inherited evidence/source overwritten')
        need(key not in pins or pins[key]==digest,'Consistent actual new evidence')
        if key not in inherited:pins[key]=digest
    for path in [previous.BASE,*parents,Path(__file__).resolve(),Path(previous.__file__).resolve()]:pin(path)
    checked_path=ROOT/'audit_v4867_native_subzero_offset_regression_checked/report.json'
    checked=json.loads(checked_path.read_text());pin(checked_path)
    need(checked['passed'] and checked['actualNativeRecordsBound']==877 and checked['actualPostDefectFields']==361 and
         checked['nativeGlobalCacheOverrunRows']==0 and checked['nativeVictimTaskAdvanced'] and
         len(checked['actualRowAndFieldFaultsRejected'])==9 and not checked['fullPortAcceptance'],
         'Actual new binary exact native route/whole fields/source-bound records, not a source-only claim')
    for p,h in checked['inputHashes'].items():pin(p,h)
    candidate=ROOT/'diagnostic_v4850_native_subzero_victim_offset'
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    restored=json.loads((candidate/'restoration.json').read_text(encoding='utf-8-sig'))
    need(restored['passed'] and all(sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items()),
         'Exact preexisting driver/header/machine and installed executable restored')
    need(build['initialized_guest_byte_delta']==39 and not build['public_build_promoted'],
         'Native candidate only; original public release untouched')
    for p in candidate.rglob('*'):
        if p.is_file():pin(p)
    for relative in (
        'tools/run_native_subzero_offset_regression_v4852.py',
        'tools/run_native_subzero_offset_regression_v4856.py',
        'tools/prepare_native_subzero_shatter_references_v4860.py',
        'tools/prepare_native_subzero_shatter_references_v4862.py',
        'tools/prepare_native_subzero_shatter_references_v4864.py',
    ):pin(ROOT/relative)
    for leaf in ('art_reference_subzero_shatter_v4863','art_reference_subzero_shatter_v4865'):
        for p in (ROOT/leaf).rglob('*'):
            if p.is_file():pin(p)
    report=dict(schema=1,baseFullScopeCheckpoint=str(previous.BASE),parentAdditiveJournals=[str(p)for p in parents],
        mergeRule='Additive full original scope: retain4557 and every parent, finite original successes and exclusions. New real native corruption repair applies to observed Sonya P1 action0616 only; no full-port or own-body art acceptance.',
        remaining=parent['remaining'],newInputHashes=pins,goalStatus='active',fullPortAcceptance=False,finishedRelease=False,
        previousGoalTurnClassification='progress: fresh source gate4845/4846 rejected6 actual staged-source faults; confirmed whole repaired guest33018F and actual compiled3836 baseline; saved full-scope4848 journal. Existing32.49GiB cleanup verified, no further deletions.',
        thisGoalTurnClassification='progress: compiled isolated native candidate4850 from actual3836 frozen driver/header and source4844, not dirty baseline. All preexisting source/installed executable bytes restored. Exact old physical Sonya inputs cold-booted new binary; full1MB initialized guest compared inRAM to independent39-byte table-only delta. Original failure108255 now reads dedicated row zero and own FF0320C0 dizzy group; native victim advances to body lookup108311 and native death050A with zero global cache stores through108600. Independent checker4866 binds877 actual opcodes/ROM peeks and361 consecutive native fields and rejects9 real row/field faults. Decoded original3-component frozen bodies and actualFFB06AE0 palette as small references; own new body art still needed.',
        actualNativeRepair=dict(candidate=str(candidate),executableSHA256=build['executable_sha256'],payloadSHA256=build['payload_sha256'],
            expectedAndActualInitializedGuestSHA256=build['expected_guest_sha256'],initializedGuestByteDelta=39,
            nativeTerminalExit=0,nativeStopFrame=108600,actualNativeRecords=877,actualConsecutivePostDefectFields=361,
            originalDefectFrame=108255,nativeLaterBodyLookupFrame=108311,subsequentNativeDeathAction='050A',
            realVictimIdentity=18,originalPhysicalInputsUnchanged=True,nativeGlobalCacheOverrunRows=0,
            independentRuntimeProof=str(checked_path),nativeSonyaOverreadRepairAccepted=True,trueKanoNativeRegressionPending=True),
        remainingSubzeroFinisher=dict(ownBodyArtAccepted=False,actualLaterLookupStillClamps17And18To11=True,
            sourceReference=str(ROOT/'art_reference_subzero_shatter_v4865/reference.json'),
            nativeBodyPalette='FFB06AE0',nativeCompositeComponents=3,
            next='Author dedicated own Kano/Sonya frozen bodies, encode native3-component zero-terminated groups and extend real-ID lookup while retaining original stock/secret/boss semantics. Verify actual native shatter rendering/parts/cleanup/audio in both slots, and regression of trueKano offset branch. No Jax proxy, native cache cap, action/state restoration or health/AI/RNG assistance.'),
        preservedFailures=dict(regression4852='Host generated collector lacked separator between EXE_SHA and and; failed before native launch; immutable original retained. Fresh4856 corrected.',
            reference4860='Normal-palette reference decoder incorrectly treated16-bit count plus color0 as32-bit count forLiu; failed before outputs.4863 normal costume comparison retained;4865 actual final native body palette is authoritative.'),
        currentDirtyCheckoutRestored=True,installedHistoricalExecutableRestored=True,publicCMDExecutableAndZIPChanged=False,
        newBuilds=1,payloadCopies=0,payloadUsesImmutableHardlink=True,rawMediaGuestOrROMFilesWritten=0,
        removedOnlyTransientExecutableBackupAfterVerifiedRestoration=True,oldUserBuildsNewlyDeleted=0,
        cleanupAccounting='One required compressed native candidate and compressed source/log/digest evidence; immutable payload hardlink. No WAV/PNG game captures/guest dumps/recovery archive. Two tiny decoded original reference atlases only. Public release unchanged; prior user-requested cleanup remains authoritative.',
        nextAction='Complete character-owned frozen-body native art/data route and trueKano action0616 runtime regression, then continue every original Pit/Tomb/audio/art/grounding/floor-shadow/CPU/KO/overlap/finishers/victims/morphs/secrets/cinematics/natural endings/selection/ladder/names/release requirement. Do not mark complete on a bounded corruption regression.')
    need(len(report['remaining'])==5 and all(sha(p)==h for p,h in pins.items()),'Original full scope and newly pinned actual evidence retained')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before checkpoint')
    (OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(journal=str(OUT/'progress.json'),newPins=len(pins),newBuilds=1,
        actualNativeSonyaOverreadRepairAccepted=True,trueKanoNativeRegressionPending=True,
        ownFrozenBodyArtPending=True,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
