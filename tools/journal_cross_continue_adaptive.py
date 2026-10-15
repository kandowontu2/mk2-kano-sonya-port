"""Four current true cross-continues; preserve rejected attempts and full scope."""
import gzip,json,subprocess
from pathlib import Path
import cross_continue_adaptive_contract as contract
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT,need,sha=contract.ROOT,contract.need,contract.sha


def main():
    out=ROOT/'audit_cross_continue_adaptive_progress_storage'
    need(not out.exists()and not native.census(),'Fresh complete journal; authoritative native jobs terminal')
    parentpath=ROOT/'audit_challenger_precombat_count_correction/report.json';parent=json.loads(parentpath.read_text())
    need(parent['passed']and len(parent['remaining'])==6,'Full original natural-integration scope retained')
    pins={str(parentpath):sha(parentpath)};migrations=[]
    for p,h in parent['inputHashes'].items():
        path=Path(p).resolve()
        if path.parent==ROOT and path.name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'):
            old=ROOT/'status_history_cross_continue_adaptive'/path.name
            need(sha(old)==h,'Exact previous root document retained')
            migrations.append(dict(priorLogicalPath=str(path),priorSHA256=h,historicalBytes=str(old),currentSHA256=sha(path)));path=old
        need(sha(path)==h,'Every original source/evidence pin preserved');pins[str(path)]=h
    cases=[];fields=faults=shadow_checks=views=0;pids=[]
    for fighter,side,target in(('kano',1,'sonya'),('kano',2,'sonya'),('sonya',1,'kano'),('sonya',2,'kano')):
        folder=ROOT/f'audit_cross_continue_adaptive_{fighter}_p{side}_to_{target}'
        terminal=json.loads((folder/'native_terminal.json').read_text());capture=json.loads((folder/'report.json').read_text())
        report_paths=[ROOT/f'{prefix}_{fighter}_p{side}_to_{target}/report.json'for prefix in('audit_cross_continue_adaptive_checked','audit_cross_continue_adaptive_pixels','audit_cross_continue_adaptive_control_faults','audit_cross_continue_adaptive_visual')]
        proof,pixel,control,visual=(json.loads(p.read_text())for p in report_paths)
        need(capture['passed']and all(r['passed']for r in(proof,pixel,control,visual))and terminal['exitCode']==0 and not terminal['observationErrors']and not(folder/'stderr.log').read_text().strip(),'Actual normal current capture and all four independent finite receipts')
        need(capture['candidate']==contract.current.NAME and capture['guestSHA256']==contract.current.GUEST_SHA and capture['executableSHA256']==contract.current.EXE_SHA,'Actual current candidate, not transferred old runtime result')
        with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
        actual=contract.gate(text,fighter,side,target)
        need(actual==proof['actualSinglePlayerContinue']and actual['actualWalkJumpPunchAccepted']and actual['actualOtherPlayerStartupKeyReleased']and actual['collisionEarnedLosses']==2,'Whole original real loss/payment/ID/actual-response/UI gate reruns from exact retained native log')
        need(len(proof['actualFaultsRejected'])==18 and len(control['actualControlFaultsRejected'])==9 and len(visual['viewedFrameHeaders'])==3,'All actual state/raster/control faults and finite visual frames')
        need(proof['actualUIPixels']['blink_colors']>=2 and proof['actualUIPixels']['native_name_shadow_checks']>=4 and pixel['selectedPlayerLadderIcon']['fullSourceRasterMatches']>=3,'Original complete blink/name/selected-player native pixel contracts')
        for path,report in zip(report_paths,(proof,pixel,control,visual),strict=True):
            pins[str(path)]=sha(path)
            for p,h in report['inputHashes'].items():need(sha(p)==h,'Every current actually executed input/proof remains intact');pins[p]=h
        pids.append(terminal['nativePID']);fields+=actual['continuedActorFields'];shadow_checks+=proof['actualUIPixels']['native_name_shadow_checks'];views+=3
        case_faults=18+9+len(pixel['additionalActualImageFaultsRejected']);faults+=case_faults
        cases.append(dict(fighter=fighter,side=side,target=target,nativePID=terminal['nativePID'],nativeTerminal=terminal,events=actual['events'],continuedActorFields=actual['continuedActorFields'],actualResponseAccepted=True,selectedPlayerLadderSourceMatches=pixel['selectedPlayerLadderIcon']['fullSourceRasterMatches'],nativeNameShadowChecks=proof['actualUIPixels']['native_name_shadow_checks'],actualFaultsRejected=case_faults,proofs=[str(p)for p in report_paths]))
    need(len(set(pids))==4 and fields==2432 and faults==117 and shadow_checks==53 and views==12,'Complete actual four-route counts, no renamed native games')
    rejected=[]
    for name,expected in(('audit_cross_continue_kano_p1_to_sonya',3),('audit_cross_continue_v3_kano_p1_to_sonya',0),('audit_cross_continue_ordinary_kano_p1_to_sonya',0)):
        folder=ROOT/name;capture=json.loads((folder/'report.json').read_text());terminal=json.loads((folder/'native_terminal.json').read_text())
        need(not capture['passed']and terminal['exitCode']==expected,'Original actual native/host rejected attempt kept false')
        rejected.append(dict(capture=str(folder),nativeTerminal=terminal,originalError=capture['error'],wholeRouteAccepted=False))
        pins[str(folder/'report.json')]=sha(folder/'report.json')
    folders=[p for p in ROOT.iterdir()if p.is_dir()and p.name.startswith('audit_cross_continue')]+[ROOT/'status_history_cross_continue_adaptive']
    files={p for folder in folders for p in folder.rglob('*')if p.is_file()}
    files.update(ROOT.glob('mk2ks_cross_continue*.lua'));files.update((ROOT/'tools').glob('*cross_continue*.py'))
    files.update(ROOT/name for name in('CURRENT_PLAYTEST_STATUS.md','WORKSPACE_CLEANUP_CURRENT.md'))
    need(all(p.resolve().is_relative_to(ROOT)and not p.is_symlink()for p in files)and not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),'Exact bounded source/gzip/digest/proof/history compression targets; no raw media or build')
    storage=[];total=0;seen=set()
    for p in sorted(files):
        h=sha(p);st=p.stat();before=allocated(p)
        need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact lossless retained source/evidence compression')
        after=allocated(p);key=st.st_dev,st.st_ino
        if key not in seen:total+=after;seen.add(key)
        pins[str(p)]=h;storage.append(dict(path=str(p),sha256=h,beforeAllocatedBytes=before,allocatedBytes=after))
    contract.current.expected();builds=[p for p in ROOT.iterdir()if p.is_dir()and(p/'mkport_candidate.exe').is_file()]
    need(len(builds)==16 and not(ROOT/'mame-mkp/build/mingw-gcc').exists()and not native.census()and all(sha(p)==h for p,h in pins.items()),'All actual sources/candidate/public launcher preserved, no new build/cache/live game')
    report=dict(passed=True,candidate=contract.current.NAME,goalStatus='active',fullPortAcceptance=False,
        previousGoalTurnClassification='progress: actual CPU audio carry-in source-clock gap closed on retained native run, exact mixed audio and cleanup qualified',
        thisGoalTurnClassification='progress: four genuine released-input cross-character continues, complete original native UI pixels and actual-response controls/survival, source/identity/fault checks and twelve actual frames',
        cases=cases,actualNativePIDs=pids,collisionEarnedLosses=8,continuedActorFields=fields,originalUIStateRasterFaultsRejected=72,additionalImageFaultsRejected=9,actualControlResponseFaultsRejected=36,totalActualFaultsRejected=faults,actualNativeNameShadowChecks=shadow_checks,actualViewedFrames=views,
        completedReleasedCrossCharacterStageZeroRoutes=4,allContinueStagesOrAudioAccepted=False,allPostEndingFreshJoinsAccepted=False,
        originalRejectedAttempts=rejected,
        preservedPostCaptureCheckerFailures=[dict(error='Actually jumps after cross-character continue',nativeGameFailure=False,scope='Fixed-time extended control attempt, real incoming-hit recovery; not an accepted jump'),dict(error="module 'continue_viewport_contract_v6610' has no attribute 'prior'",nativeGameFailure=False,scope='Original CPU fault predicate namespace before same-terminal qualification'),dict(error='StopIteration',nativeGameFailure=False,scope='Sparse delayed neutral-air raster preview absent after original CPU interrupts jump; appearance review makes no airborne-raster acceptance')],
        remaining=parent['remaining'],nextAction='Audit exact unchanged-source conservation and actual outstanding post-ending/continued-stage/audio/stock-victim/secret/cinematic gates against the full14 original requirements, then final combined current acceptance and matching public CMD/release; do not replay these four routes merely for a new label.',
        allRAMHostsReleased=True,publicPlayableChanged=False,newNativeBoots=7,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,retainedCompiledCandidates=16,selectedFileCount=len(files),uniqueSelectedAllocatedBytes=total,inputHashes=pins,intentionalDocumentationPinMigrations=migrations,exactCompressedTargets=storage)
    out.mkdir();path=out/'report.json';path.write_text(json.dumps(report,indent=2)+'\n');h=sha(path)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Lossless authoritative actual progress checkpoint')
    print(json.dumps({k:report[k]for k in('passed','completedReleasedCrossCharacterStageZeroRoutes','continuedActorFields','totalActualFaultsRejected','actualNativeNameShadowChecks','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds')}),flush=True)


if __name__=='__main__':main()
