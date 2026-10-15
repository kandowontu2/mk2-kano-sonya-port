"""Current integration evidence and bounded storage; keep the full goal open."""
import json
import subprocess
from pathlib import Path
import native_ai_response_full_context as current
import native_process_census_v6647 as native
import audit_current_natural_integration_v6476 as requirements
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=current.ROOT,current.need,current.sha

def main():
    out=ROOT/'audit_native_current_regression_progress_storage'
    need(not out.exists() and not native.census(), 'Fresh current regression journal, all native jobs terminal')
    current.expected()
    ui_path=ROOT/'audit_native_current_ui_owned_checked/report.json'
    visual_path=ui_path.parent/'actual_native_visual_review.json'
    matrix_path=ROOT/'audit_native_current_special_matrix_checked/report.json'
    lookup_path=ROOT/'audit_native_current_lookup_inventory/report.json'
    ui=json.loads(ui_path.read_text());visual=json.loads(visual_path.read_text())
    matrix=json.loads(matrix_path.read_text());lookup=json.loads(lookup_path.read_text())
    original_groups_path=ROOT/'audit_native_dual_roll_progress_storage/report.json'
    original_groups=json.loads(original_groups_path.read_text())
    need(original_groups['passed'] and len(original_groups['remaining'])==6,
        'Full original remaining work groups retained, not replaced by the current finite matrix')
    need(ui['passed'] and ui['candidate']==current.NAME and len(ui['cases'])==4 and
        ui['originalStatePixelFaultMethods']==46 and len(ui['actualOwnerFaultsRejected'])==32 and
        ui['currentBothSlotSelectionLadderFirstMatchPixelsAccepted'] and ui['completeColdOwnershipClear'] and
        ui['allCombatOwnersSourceBound'] and visual['passed'] and len(visual['reviewedOriginalNativeFrames'])==12,
        'Actual complete current four-case UI/state/render/owner gates and inspected native images')
    need(matrix['passed'] and matrix['candidate']==current.NAME and matrix['actualCases']==16 and
        matrix['actualVerifiedSpecialCycles']==32 and len(matrix['actualSemanticFaultsRejected'])==194 and
        matrix['allEightMovesBothPlayerSlotsRepeatTwiceAndRecoverVerified'] and not matrix['canonicalUserCMDUsed'],
        'All current native cold boots and the entire original human special semantic/fault matrix')
    need(lookup['passed'] and lookup['staticInventoryOnly'] and not lookup['runtimeAcceptance'],
        'Static source inventory stays distinct from actual runtime coverage')
    pins={str(Path(__file__).resolve()):sha(__file__)}
    pins[str(original_groups_path)]=sha(original_groups_path)
    pins[str(Path(requirements.__file__).resolve())]=sha(requirements.__file__)
    for path,report in ((ui_path,ui),(visual_path,visual),(matrix_path,matrix),(lookup_path,lookup)):
        pins[str(path)]=sha(path)
        for source,digest in report['inputHashes'].items():
            need(sha(source)==digest and (source not in pins or pins[source]==digest),
                'Every current actual proof/executable/controller/source pin intact: '+source)
            pins[source]=digest
    public=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(public)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE',
        'Public checked playtest launcher unchanged; no premature promotion')
    pins[str(public)]=sha(public)
    leaves=[ROOT/'audit_native_current_ui_ram',ROOT/'audit_native_current_ui_checked',ui_path.parent,
        lookup_path.parent,matrix_path.parent]
    leaves.extend(ROOT/f'audit_native_current_special_{move}_p{side}'
        for move in ('knife','ball','blade','choke','ring','square','bicycle','leg') for side in (1,2))
    files={p for leaf in leaves for p in leaf.rglob('*') if p.is_file()}
    files.update([Path(__file__),ROOT/'TEST_NATIVE_CURRENT_SPECIALS.cmd',
        *(ROOT/'tools'/name for name in ('capture_native_current_specials.py','verify_native_current_special_matrix.py',
          'inspect_current_native_lookup_tables.py','seal_current_native_lookup_inventory.py',
          'finish_native_current_ui_review.py','serve_native_current_ui_ram.py'))])
    storage=[];seen=set();total=0
    for path in sorted(files):
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink() and
            path.suffix.lower() not in ('.exe','.mdata','.zip','.wav','.png','.bin','.pcm','.rgb'),
            'Exact proof/source leaves only; no build, ROM or raw media copies')
        digest=sha(path);before=allocated(path)
        subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
        need(sha(path)==digest,'Exact evidence unchanged by lossless compression')
        stat=path.stat();key=(stat.st_dev,stat.st_ino);after=allocated(path)
        if key not in seen:total+=after;seen.add(key)
        storage.append(dict(path=str(path.resolve()),sha256=digest,beforeAllocatedBytes=before,allocatedBytes=after))
        pins[str(path.resolve())]=digest
    builds=[p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]
    need(len(builds)==19 and not (ROOT/'mame-mkp/build/mingw-gcc').exists() and not native.census(),
        'Same nineteen retained compiled candidates, no generated compiler cache or live game')
    report=dict(passed=True,candidate=current.NAME,goalStatus='active',
        objective='Kano and Sonya appear as a natural part of the game in all aspects',
        previousGoalTurnClassification=visual['previousGoalTurnClassification'],
        thisGoalTurnClassification='progress: current four-case selection/ladder/true match state and pixels, actual CPU startup ownership, twelve reviewed images, sixteen current cold special runs and all original 194 semantic fault tests',
        currentSelectionCases=4,currentUIStatePixelFaultMethods=46,currentAudioOwnerFaults=32,
        actualReviewedNativeFrames=12,currentHumanSpecialColdBoots=16,currentHumanSpecialCycles=32,
        currentSpecialFaults=194,currentSpecialPostFields=matrix['actualContiguousPostFields'],
        originalNaturalIntegrationRequirements={key:value[0] for key,value in requirements.SPECS.items()},
        originalRemainingWorkGroups=original_groups['remaining'],
        staticImmediateLiveIDLookupSites=28,sourceInventoryIsNotRuntimeAcceptance=True,
        originalFailedUIAssumptionPreserved=str(ROOT/'audit_native_current_ui_checked/failure.json'),
        acceptedPriorWorkNotReset=['All four retained campaigns and complete endings/art/audio.',
          'Native stock-victim finishers, Pit/Tomb voice queue equivalence, and the repaired successful Sonya/Smoke route.',
          'Owned launch interruptions, KO, overlap, challenger, morph/return and released cross-continues.',
          'Current native AI attract repertoire and exact audible Sonya Square/Bicycle compound audio.'],
        remaining='Full original natural-integration requirements remain open until applicable source conservation, changed-source runtime and final combined gameplay/visual/audio/release evidence establish them. This journal does not narrow the objective or grant complete coverage to a finite test.',
        nextConcreteAction='Check the still-unverified audible native Kano attract roll, then reconcile scene-boundary/post-ending-join and remaining stage/victim/cinematic evidence for final combined acceptance; only then promote the matching public CMD and portable ZIP.',
        fullPortAcceptance=False,fullGoalComplete=False,publicPlayableChanged=False,
        selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,retainedCompiledCandidates=19,
        compilerCacheAbsent=True,retainedActualCurrentUIBoots=4,newNativeBoots=16,
        totalActualCurrentBootsInTheseProofs=20,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        inputHashes=pins,exactCompressedTargets=storage)
    need(all(sha(path)==digest for path,digest in pins.items()),'All final actual evidence inputs intact')
    out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n')
    digest=sha(path)
    subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True,check=True)
    need(sha(path)==digest,'Exact final journal losslessly retained')
    print(json.dumps({key:report[key] for key in ('passed','currentSelectionCases','currentHumanSpecialCycles',
        'currentSpecialFaults','uniqueSelectedAllocatedBytes','newBuilds','newRawMedia','publicPlayableChanged')}),flush=True)

if __name__=='__main__':
    main()
