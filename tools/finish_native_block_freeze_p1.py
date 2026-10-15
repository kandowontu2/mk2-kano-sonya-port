"""Seal real P1 pixel review and preserve original full integration scope."""
import datetime,hashlib,json,subprocess
from pathlib import Path
import qualify_native_block_freeze_observed as gate
import native_process_census_v6647 as census
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=gate.ROOT,gate.need,gate.sha

def finish(captures):
    checked=ROOT/'audit_native_block_freeze_p1_checked/report.json'
    previous=ROOT/'audit_native_block_freeze_progress/report.json'
    a=json.loads(checked.read_text());b=json.loads(previous.read_text())
    out=ROOT/'audit_native_block_freeze_both_slots_progress'
    need(not out.exists() and not census.census(),'Fresh review receipt after actual native terminal')
    need(a['passed'] and len(a['cases'])==len(captures)==7 and len(a['effectiveFaults'])==140 and
         b['passed'] and len(b['nativeGuardCases'])==6,'Actual P1 seven cases and prior P2 six cases, never inferred from labels')
    need(all(sha(p)==h for r in (a,b) for p,h in r['inputHashes'].items()),'All actually checked old and new inputs unchanged')
    reviews=[]
    for (key,c),case in zip(captures.items(),a['cases']):
        hashes=[hashlib.sha256(i.tobytes()).hexdigest().upper() for i in c['images']]
        need(hashes==case['ramRGBHashes'] and len(hashes)==4,'Same four original native RAM event screens reviewed')
        reviews.append(dict(case=key,actualScreens=4,RGBHashes=hashes,
                            observation='Native own Kano/Sonya or stock Liu body/name; blue unblocked ice or native own guard and visible ice impact; original palette and standing pose restored after release/thaw.'))
    folders=[checked.parent,*[ROOT/f'audit_native_block_freeze_observed_{r["policy"]}_{r["fighter"]}_p1' for r in a['cases']]]
    storage=[]
    for folder in folders:
        for p in folder.rglob('*'):
            if not p.is_file():continue
            need(p.resolve().is_relative_to(ROOT.resolve()) and not p.is_symlink(),'Exact bounded proof compression')
            digest=sha(p)
            subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
            need(sha(p)==digest,'No original evidence byte changed')
            storage.append(dict(path=str(p),sha256=digest,allocatedBytes=allocated(p)))
    out.mkdir()
    report=dict(passed=True,goalStatus='active',fullGoalComplete=False,fullPortAcceptance=False,
                observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                previousGoalTurnClassification='progress: original completed six-case P2 guard comparison and 24 reviewed native screens saved before interruption',
                thisGoalTurnClassification='progress: seven current opposite-slot human Freeze/block/release comparisons qualified with 140 effective faults and 28 original native event screens reviewed',
                originalNaturalIntegrationRequirements=b['originalNaturalIntegrationRequirements'],
                originalRemainingWorkGroups=b['originalRemainingWorkGroups'],acceptedPriorWorkNotReset=b['acceptedPriorWorkNotReset'],
                finiteHumanFreezeBlockRecoveryBothSlotsAccepted=True,combinedNativeGames=13,combinedNativeFields=9113,
                combinedEffectiveFaults=248,combinedReviewedNativeScreens=52,newCases=a['cases'],newVisualReview=reviews,
                unsuccessfulCampaignControllers=b['unsuccessfulCampaignControllers'],postEndingFreshJoinAccepted=False,
                audibleNativeKanoAttractAccepted=False,publicBuildPromoted=False,
                limitation='Finite Dead Pool human Freeze/block/control sequences. No continuous whole-scene shadow/audio, CPU/arena or full-port completion claim.',
                nextAction='Use a passive native CPU projectile-creation event to drive only ordinary Block buttons in a bounded fresh earned campaign/post-ending-join attempt. Do not modify game balance without a reproduced game defect.',
                newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,
                allocatedEvidenceBytes=sum(r['allocatedBytes'] for r in storage),storage=storage,
                inputHashes={str(p):sha(p) for p in (checked,previous,Path(__file__).resolve(),
                    ROOT/'tools/qualify_native_block_freeze_p1.py',ROOT/'tools/capture_native_block_freeze_p1.py',ROOT/'PLAY_MK2_KANO_SONYA.cmd')})
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return dict(passed=True,combinedNativeGames=13,combinedNativeFields=9113,combinedEffectiveFaults=248,
                combinedReviewedNativeScreens=52,allocatedEvidenceBytes=report['allocatedEvidenceBytes'])
