"""Preserve the full natural-character objective with actual P2 campaign work."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha,NAME=current.ROOT,current.need,current.sha,current.NAME
PREVIOUS=ROOT/'audit_v3741_guarded_friendship_ui_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3763_guarded_p2_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh full-objective checkpoint')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],
      'Full original objective, not campaigns-only or tests-only completion')
    def pin(file,wanted=None):
        path=Path(file).resolve();key=str(path);digest=sha(path)
        need(wanted is None or wanted==digest,'Actual relevant evidence changed '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh pins')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Never relabel inherited evidence')
        pins[key]=digest
    def checked(relative):
        path=ROOT/relative;report=json.loads(path.read_text());need(report['passed'],'Actual completed bounded proof')
        pin(path)
        for p,h in report.get('inputHashes',{}).items():pin(p,h)
        for case in report.get('cases',[]):
            for p,h in case.get('inputHashes',{}).items():pin(p,h)
        return report
    kano=checked('audit_v3748_guarded_p2_campaign_state_checked/report.json')
    need(len(kano['cases'])==1,'One actual verified Kano context')
    k=kano['cases'][0]
    need(k['passed']and k['unassisted_clear_proven']and k['human_slot']==2 and k['player']=='kano'and
      k['stages_reached']==list(range(13))+[14,15,16]and k['native_own_round_wins']==33 and k['paid_continue_losses']==3 and
      k['ending_starts']==k['ending_completions']==1 and len(k['actualRowCounterexamplesRejected'])==12 and
      not k['endingPixelsAccepted']and not k['completeCampaignAudioAccepted'],
      'Actual real-credit full P2 true17 campaign, original damage/win/progression/own pages/attract, not all ending pixels/audio')
    sonya=checked('audit_v3765_guarded_sonya_p2_capture_accounting_checked/report.json')
    s=sonya['cases'][0]
    need(s['passed']and not s['unassisted_clear_proven']and s['human_slot']==2 and s['player']=='sonya'and
      s['stages_reached']==[0]and s['paid_continue_losses']==83 and s['native_owned_special_entries']==729 and
      len(s['actualRowCounterexamplesRejected'])==9 and not s['captureMemoryOnlyResourceContractAccepted'],
      'Actual stable true18 mirror/paid-continue state only; no false clear or zero-raster accounting')
    storage=checked('audit_v3760_guarded_p2_campaign_log_compression/report.json')
    accounting=checked('audit_v3773_campaign_timeout_raster_accounting/report.json')
    need(storage['deletedFiles']==0 and storage['reclaimedAllocatedBytes']==8466432 and
      accounting['nativeTimeoutAutomaticRasterFiles']==3 and not accounting['historicalResultsChanged'],
      'Lossless sealed-log space reclaimed, exposed native timeout PNGs honestly accounted for')
    failed=ROOT/'audit_v3759_guarded_sonya_p2_bounded_campaign_checked/report.json'
    need(not json.loads(failed.read_text())['passed'],'Original strict raster-accounting failure retained');pin(failed)
    for leaf in('audit_v3751_guarded_sonya_zoning_p2_campaign','audit_v3756_guarded_sonya_throw_p2_campaign'):
        folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
        need(meta['exit_code']==0 and meta['candidate']==NAME,'Stopped actual diagnostic, never claim a clear')
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    zoned=ROOT/'audit_v3771_guarded_sonya_p2_zoning_state_checked/report.json'
    zoned_state=None
    if zoned.exists():
        z=checked(str(zoned.relative_to(ROOT)));need(len(z['cases'])==1,'One actual zoning context')
        zoned_state={k:v for k,v in z['cases'][0].items()if k not in('inputHashes','uppercutAssignmentFrames')}
        need(zoned_state['stages_reached']==list(range(10))and not zoned_state['unassisted_clear_proven'],
          'Successful earned mirror advance to9, never a full tower clear')
    public={
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}
    for file,h in public.items():pin(ROOT/file,h)
    pin(ROOT/state['currentCMD']);pin(PREVIOUS);pin(__file__)
    for file in('mk2ks_guarded_campaign_finite_ram_v3766.lua','tools/run_guarded_sonya_p2_extended_ram_v3767.py'):
        pin(ROOT/file)
    # Check the actual child, not merely a manifest or intended run.
    live=subprocess.run(['powershell.exe','-NoProfile','-Command',
      '(Get-Process -Id 31936 -ErrorAction Stop).Id'],capture_output=True,text=True)
    need(live.returncode==0 and live.stdout.strip()=='31936','Longer actual Sonya cold-campaign child confirmed live now')
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentCheckpointSHA256=pins[str(PREVIOUS)],
      mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Fresh pins agree with inherited keys; never flatten/copy historical map.'),
      previousCheckpoint=str(PREVIOUS),previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: revalidate3741/current3680/unchanged user checkout. Actual original input-only P2 cold campaigns, six raster sinks streamed inRAM, no game/build changes. Kano59336fields terminal0 clears all16actual stages incl Kintaro/Shao,33ownwins3paidcontinues,318trueKnifeentries,own picture/text dispatch and native attract;3748whole original campaign algorithm/physical boss replay and12actual-row faults accepted. Sonya213357fields terminal0 defensive_leg staysstage0 after83paidlosses,729actuallegentries;3765whole native bounded state and9faults accepted but never a clear. Strict3759resource gate correctly catches one automatic MAME -str PNG, preserved.3773actual inventory accounts three timeout PNGs across stoppedSonya leaves; originalzero-raster metadata never promoted. Separate originalSonya zoning controls naturally clear mirror and reachstage9 before3900s limit; independent3770qualification may remain live. Throw strategy staysstage0, stopped; not a clear. Longer originalSonya zoning cold run3767/3768 actually live46156child31936,6000hostlimit and5900finiteobserverexit prevents native timeout screenshot in future, no forced inputs/state/AI/wins.3760lossless sealed-log compression preserves everybyte and reclaims8466432allocatedbytes. Full five groups/publicZIP/currentgame untouched; no broad completion.',
      developmentCandidate=NAME,gameSourceAndPlayableBytesChangedThisTurn=False,
      current3680KanoP2NaturalFullCampaignClearAccepted=True,
      current3680KanoP2NaturalCampaignReport=str(ROOT/'audit_v3748_guarded_p2_campaign_state_checked/report.json'),
      current3680KanoP2OwnEndingDispatchAndNativeAttractAccepted=True,
      current3680KanoP2EndingPixelOrFullAudioFidelityAccepted=False,
      current3680KanoP2NativeOwnRoundWins=33,current3680KanoP2PaidContinueLosses=3,
      current3680KanoP2ActualRowFaultsRejected=12,
      current3680SonyaP2NaturalFullCampaignClearAccepted=False,
      current3680SonyaP2BoundedMirrorContinueStateReport=str(ROOT/'audit_v3765_guarded_sonya_p2_capture_accounting_checked/report.json'),
      current3680SonyaP2ZoningStateReport=str(zoned)if zoned_state else None,
      current3680SonyaP2ZoningState=zoned_state,
      preservedStrictCampaignRasterAccountingFailure=str(failed),
      campaignTimeoutRasterAccountingReport=str(ROOT/'audit_v3773_campaign_timeout_raster_accounting/report.json'),
      originalCampaignCaptureZeroRasterClaimsAccepted=False,
      pendingSonyaP2ExtendedCampaign=dict(execSession=46156,childPID=31936,capture='audit_v3768_guarded_sonya_extended_p2_campaign',
        runner='tools/run_guarded_sonya_p2_extended_ram_v3767.py',actualChildConfirmedLive=True,
        independentVerificationPending=True,actualFiniteHostExitNotYetProven=True),
      pendingSonyaP2ZoningQualificationExecSession=None if zoned_state else 60004,
      currentTurnSealedDiagnosticCompression=dict(report=str(ROOT/'audit_v3760_guarded_p2_campaign_log_compression/report.json'),
        allocatedBytesFreed=8466432,deletedFiles=0),
      nextAction='Resume authoritative live46156 first; never restart3768becausepolltimedout. Originalzoning reachesstage9 before oldlimit; longer currentrun must earn remainingstages/Kintaro/Shao/ownending/attract, not forcedclear. If60004remainslive, pollthat exact qualifier; native state beyondoldlimit and full original guest/compiled inputs/input replay must be verified. Do not rerun accepted3680KanoP2clear/UI/Friendship/mirror/Tomb merelymetadata. Original3759 automaticPNG gate failure retained; threeactual timeoutPNGs recorded3773; oldzero-raster manifests unaccepted. Longer3766observerexit must itself be observed; do not claimRAM-onlywithoutoutput inventory. Remaining broaderstage/victim/DCSwaveforms, movephase/art/ground/shadow/erase arenas CPU/repeat/KO/overlap, otherfinishers/victims/morph/secrets/cinematics, P2endingpixel/audio and finalcombinedregression/obsoletecleanup/newpublicZIPallremain. PreserveallpriorP1naturalclear proofs andrecursive retired exclusions. Public1836CMD/ZIPanddirtyworkinggamefilesunchanged.')
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],'All five original groups retained')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n')
    digest=sha(path);sealed=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True,text=True)
    need(sealed.returncode==0 and sha(path)==digest,'Lossless checkpoint compression')
    print(json.dumps(dict(checkpoint=str(path),kanoP2FullNaturalClear=True,sonyaP2FullNaturalClear=False,
      zonedBoundedStateAccepted=bool(zoned_state),pendingExtendedExec=46156,pendingChildPID=31936,
      freshRelevantPins=len(pins),allocatedBytesFreed=8466432,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
