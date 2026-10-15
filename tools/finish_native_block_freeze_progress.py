"""Seal same-RAM visual review and finite guard progress without promotion."""
import datetime,hashlib,json,subprocess
from pathlib import Path
import qualify_native_block_freeze_observed as gate
import native_process_census_v6647 as census
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=gate.ROOT,gate.need,gate.sha

def finish(captures):
    checked=ROOT/'audit_native_block_freeze_observed_checked/report.json'
    result=json.loads(checked.read_text())
    out=ROOT/'audit_native_block_freeze_progress'
    need(not out.exists() and not census.census(),'All six native games terminal; fresh immutable progress receipt')
    need(result['passed'] and len(result['cases'])==len(captures)==6 and len(result['effectiveFaults'])==108,
         'Actual complete six-case guard/recovery positive and negative checks')
    need(all(sha(p)==h for p,h in result['inputHashes'].items()),'Every checked source and native proof still unchanged')
    reviews=[]
    for (key,c),case in zip(captures.items(),result['cases']):
        hashes=[hashlib.sha256(i.tobytes()).hexdigest().upper() for i in c['images']]
        need(hashes==case['ramRGBHashes'] and len(hashes)==4,'Same original native RAM pixels visually reviewed')
        reviews.append(dict(case=key,actualScreens=4,screenPixels=406400,RGBHashes=hashes,
                            observation='Own true fighter and native name remain; actual blue unblocked Kano ice or ordinary own guard with visible native impact; guard releases and own stance returns.'))
    core=json.loads((ROOT/'audit_native_current_regression_progress_storage/report.json').read_text())
    trials=[]
    for name in ('join','reactive','defensive'):
        folder=ROOT/f'audit_native_postending_kano_p2_sonya_{name}'
        stopped=json.loads((folder/'explicit_unsuccessful_controller_stop.json').read_text())
        preserved=json.loads((folder/'stopped_controller_trial_preserved.json').read_text())
        need(stopped['testIntentionallyStopped'] and stopped['nativeExit']==4294967295 and preserved['failedNativeTrialPreserved'],
             'Earlier unsuccessful campaign trials are actual terminal failures, not still-live progress')
        trials.append(dict(controller=name,nativeExit=stopped['nativeExit'],paidContinueLosses=stopped['observedPaidContinueLosses'],
                           postEndingJoinAccepted=False,softlockClaim=False,gameBugClaim=False))
    launcher=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(launcher)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE','Public launcher unchanged')
    folders=[ROOT/'audit_native_block_freeze_observed_checked',*[
        ROOT/f'audit_native_block_freeze_observed_{case["policy"]}_{case["fighter"]}_p{case["physicalSlot"]}' for case in result['cases']]]
    storage=[]
    for folder in folders:
        for p in folder.rglob('*'):
            if not p.is_file():continue
            need(p.resolve().is_relative_to(ROOT.resolve()) and not p.is_symlink(),'Bounded exact evidence compression path')
            digest=sha(p)
            subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
            need(sha(p)==digest,'Every original source/evidence byte preserved')
            storage.append(dict(path=str(p),sha256=digest,allocatedBytes=allocated(p)))
    out.mkdir()
    previous_source=ROOT/'tools/qualify_native_block_freeze_before_exception_type_fix.py'
    failure=dict(passed=False,nativeFailure=False,nativeReruns=0,
                 originalError='ValueError: Actual independent stable native human actor/main/roster ownership',
                 cause='Negative tests raised the intended need() ValueError, but the verifier caught only AssertionError/RuntimeError.',
                 originalSourceSHA256=sha(previous_source),correctedSourceSHA256=sha(gate.__file__))
    (out/'initial_verifier_exception_failure.json').write_text(json.dumps(failure,indent=2)+'\n')
    report=dict(passed=True,goalStatus='active',fullPortAcceptance=False,fullGoalComplete=False,
                observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                previousGoalTurnClassification='no progress: status-only response; retained RAM host revalidated before action',
                thisGoalTurnClassification='progress: stale Freeze launch taps diagnosed and corrected, six current native Freeze/Block/recovery comparisons qualified, 24 actual screens reviewed, three unsuccessful campaign-controller trials preserved as failures',
                originalNaturalIntegrationRequirements=core['originalNaturalIntegrationRequirements'],
                originalRemainingWorkGroups=core['originalRemainingWorkGroups'],
                acceptedPriorWorkNotReset=core['acceptedPriorWorkNotReset'],
                nativeGuardCases=result['cases'],nativeFields=4206,effectiveFaults=108,visualReview=reviews,
                finiteP2HumanFreezeBlockRecoveryAccepted=True,
                unsuccessfulCampaignControllers=trials,postEndingFreshJoinAccepted=False,
                audibleNativeKanoAttractAccepted=False,publicBuildPromoted=False,
                nextAction='Complete opposite-slot guard comparison; continue native CPU/projectile/audio and post-ending fresh-join integration. Do not infer a game blocking defect from poor automated-player wins or stale observer hooks. Original full integration/combined release scope remains open.',
                newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
                compressedEvidenceAllocatedBytes=sum(r['allocatedBytes'] for r in storage),storage=storage,
                inputHashes={str(p):sha(p) for p in (checked,Path(__file__).resolve(),previous_source,launcher,
                    ROOT/'audit_native_current_regression_progress_storage/report.json')})
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return dict(passed=True,nativeGames=6,nativeFields=4206,actualScreensReviewed=24,effectiveFaults=108,
                allocatedEvidenceBytes=report['compressedEvidenceAllocatedBytes'],publicBuildPromoted=False)
