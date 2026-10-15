"""Full-scope checkpoint: actual Jax scenes, terminal RAM campaign, live state QA."""
import hashlib,json,subprocess
from pathlib import Path
from PIL import Image
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v4018_split_audio_ram_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4047_jax_scene_ram_campaign_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Whole natural-character objective retained')
    def pin(p,wanted=None):
        p=Path(p).resolve();key=str(p);digest=sha(p)
        need(wanted is None or digest==wanted,'Exact actual evidence/source unchanged '+key)
        need(key not in pins or pins[key]==digest,'Consistent new evidence pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Shared inherited bytes unchanged')
        pins[key]=digest
    pin(PARENT);reports={}
    for leaf in('audit_v4010_sonya_zoning700_campaign_observed','audit_v4016_sonya_zoning700_campaign_checked','audit_v4030_jax_clap_native_scene_observed','audit_v4043_jax_campaign_terminal_compression','audit_v4045_retained_build_binary_compression'):
        p=ROOT/leaf/'report.json';r=json.loads(p.read_text());need(r['passed']and not r['fullPortAcceptance'],'Completed bounded evidence '+leaf);reports[leaf]=r;pin(p)
        for f,h in r.get('inputHashes',{}).items():pin(f,h)
        for c in r.get('cases',[]):
            for f,h in c.get('inputHashes',{}).items():pin(f,h)
    campaign=reports['audit_v4016_sonya_zoning700_campaign_checked']['cases'][0]
    need(campaign['bounded_campaign_evidence_proven']and not campaign['unassisted_clear_proven']and campaign['stages_reached']==[0,1,2]and campaign['native_own_round_wins']==16 and campaign['paid_continue_losses']==106 and campaign['native_special_moves']=={'ring':1408}and campaign['native_combat_damage_stores']==3234 and campaign['actualNativeSwallowingSequences']==6 and campaign['globalCacheOverruns']==0 and len(campaign['actualRowCounterexamplesRejected'])==9 and len(campaign['actualRAMGuestFaultsRejected'])==8 and campaign['actualGuestDumpFilesWritten']==0,'Actual bounded campaign and full-byte RAM proof, never a clear')
    reviews=[];pids=[]
    matrix=reports['audit_v4030_jax_clap_native_scene_observed'];need(len(matrix['cases'])==4,'Four true own victim/slot scenes')
    for c in matrix['cases']:
        fighter,side=c['fighter'],c['side'];folder=ROOT/f'audit_v4029_jax_clap_{fighter}_p{side}_native_scene_ram'
        meta=json.loads((folder/'result.json').read_text());need(meta['exit_code']==0 and meta['observedRGBFields']==meta['modelExactFields']==c['exactFields']==649 and not meta['modelErrors']and not c['stockReferenceOnly'],'Actual terminal continuous exact native scene')
        visible=json.loads((folder/'visible_digests.json').read_text());digests={int(r['file'].rsplit('_',1)[1].split('.')[0]):r['rgbSHA256']for r in visible}
        frames=[frame for _,frame in sorted(c['actualPhaseFrames'].items())]+[max(digests)]
        path=ROOT/'art_review_jax_clap_v4031'/f'{fighter}-p{side}-native-clap-review.png';im=Image.open(path).convert('RGB')
        need(im.size==(800,1112)and len(frames)==8,'Seven actual native headless groups and final native page')
        for index,frame in enumerate(frames):
            x,y=(index%2)*400,(index//2)*278
            need(hashlib.sha256(im.crop((x,y+24,x+400,y+278)).tobytes()).hexdigest().upper()==digests[frame],'Every main-agent-reviewed panel equals actual native RGB')
        pin(path);reviews.append(dict(fighter=fighter,side=side,path=str(path),sha256=sha(path),actualNativePanels=8,everyPanelEqualsActualRGB=True))
        pids.append(json.loads((folder/'process.json').read_text())['pid'])
        for p in folder.rglob('*'):
            if p.is_file():pin(p)
    failed=ROOT/'audit_v4022_jax_clap_native_scene_observed/report.json';need(not json.loads(failed.read_text())['passed'],'Original descriptor-as-pose assertion failure retained false');pin(failed)
    for leaf in('audit_v4009_sonya_zoning700_p2_campaign','audit_v4021_jax_clap_kano_p1_native_scene_ram'):
        for p in (ROOT/leaf).rglob('*'):
            if p.is_file():pin(p)
    for name in('mk2ks_jax_clap_native_scene_ram_v4019.lua','tools/run_jax_clap_native_scene_v4020.py','tools/verify_jax_clap_earned_v4024.py','tools/verify_jax_clap_earned_v4026.py','tools/run_jax_clap_native_scene_v4028.py','tools/verify_jax_clap_earned_v4032.py','tools/verify_jax_clap_native_fifo_v4034.py','tools/verify_jax_clap_native_fifo_v4036.py','tools/verify_jax_clap_earned_v4038.py','tools/verify_jax_clap_native_fifo_v4040.py','tools/compact_jax_campaign_terminal_v4042.py','tools/compact_retained_build_binaries_v4044.py','tools/save_jax_scene_ram_campaign_checkpoint_v4046.py'):pin(ROOT/name)
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId = 40096" | Select-Object ProcessId,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress'],capture_output=True,text=True)
    need(q.returncode==0 and q.stdout.strip(),'Exact state qualifier handle live now, not a stale lock')
    live=json.loads(q.stdout);need(live['ProcessId']==40096 and 'verify_jax_clap_earned_v4038.py'in live['CommandLine'],'Actual original state/fault verifier still running')
    missing=pids+reports['audit_v4043_jax_campaign_terminal_compression']['captureChildrenMissing']
    q=subprocess.run(['powershell.exe','-NoProfile','-Command','Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,missing))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'All six exact native captures terminal/missing now; no child restart')
    for relative,wanted in {
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}.items():pin(ROOT/relative,wanted)
    pin(ROOT/state['currentCMD'])
    reclaimed=reports['audit_v4043_jax_campaign_terminal_compression']['reclaimedAllocatedBytes']+reports['audit_v4045_retained_build_binary_compression']['reclaimedAllocatedBytes']
    state.update(inputHashes=pins,inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared fresh pins; do not flatten.'),previousCheckpoint=str(PARENT),
      previousGoalTurnClassification='progress:4018 full native split audio/80 actual faults, lossless2.7MiB seal and confirmed live actual SonyaP2 RAM-only original zoning Start700 campaign.',
      thisGoalTurnClassification='progress: reused exact57976 campaign and31154 qualifier handles to terminal. Actual322771-field campaign reaches0/1/2,16 own rounds,106 paid losses,1408 native Rings and3234 collision damage stores; six actual own Sonya swallowing removals/no cache overrun. Whole original campaign gate plus nine native-state and eight RAM-transport faults passed; not a tower clear. New original Jax head-clap actual earned two-player controls/true17/18 victims in both slots; four full649-field CPU/DMA/shift/scanout scenes,2596fields/263753600RGBpixels exact. Preserved initial descriptor-address-as-pose failure; corrected expectations use source-bound original mapped animation groups, each pointing to its actual own native descriptor and sentinel. Four essential eight-panel native review sheets viewed and all32 panels bound to actual RGB. Current original earned-state/fault qualifier is confirmed live; independent complete generic FIFO/projection/floor/811 compressed shadow contracts preflight passed actual K1/K2/S1. Terminal campaign/initialfailed-scene leaves sealed,20443136bytes reclaimed. Nine retained EXEs are already compressed; no extra reclaim or deletion claimed. No game/build/playable byte changes; all five remaining groups and public1836 retained.',
      pendingSonyaCampaign=None,
      completedSonyaZoning700P2Campaign=dict(terminalFrame=322771,stagesReached=[0,1,2],nativeRoundWins=16,paidContinues=106,trueNativeRingEntries=1408,nativeCollisionDamageStores=3234,actualSwallowingSequences=6,globalCacheOverruns=0,stateFaultsRejected=9,ramProofFaultsRejected=8,towerClear=False,report=str(ROOT/'audit_v4016_sonya_zoning700_campaign_checked/report.json')),
      currentDevelopmentNativeJaxClapScene=dict(ownVictimContexts=4,exactFields=2596,exactRGBPixels=263753600,exactFieldsPerContext=649,allSevenSourceBoundHeadlessGroupsVisible=True,scope='Normal Dead Pool, both physical victim slots. No all-finisher/audio/arena/alternate-costume or full-port claim.',report=str(ROOT/'audit_v4030_jax_clap_native_scene_observed/report.json')),
      currentDevelopmentNativeJaxClapHumanReview=dict(allFourSheetsViewed=True,actualNativePanels=32,everyPanelEqualsActualRGB=True,panels=reviews),
      pendingJaxClapQualification=dict(stateSource=str(ROOT/'tools/verify_jax_clap_earned_v4038.py'),stateExecSession=52768,statePID=40096,liveProcess=live,stateFaultMatrixTerminalPending=True,fifoSource=str(ROOT/'tools/verify_jax_clap_native_fifo_v4040.py'),fifoFullMatrixNotStarted=True,preflightActualFIFOContextsPassed=['kanoP1','kanoP2','sonyaP1'],allFourStateAndFIFOFaultMatricesAccepted=False),
      preservedJaxSceneCheckerFailure='4020 assumed the physical pose field held guest descriptor addresses. Native original own main60 keeps mapped animation-group pointers FF0137E0..FF013A20/FF0339A0..FF033BE0. Its actual renderer was exact649fields. Fresh4028 checks each whole original group points to the exact own descriptor plus sentinel; all four fresh full scenes passed. Original4022 failure remains false.',
      gameSourceAndPlayableBytesChangedThisTurn=False,currentTurnReclaimedAllocatedBytes=reclaimed,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,currentTurnActualCaptureRasterFiles=0,currentTurnActualCaptureAudioFiles=0,currentTurnNativeGuestMemoryDumpFiles=0,currentTurnEssentialNativeQAReviewPNGs=4,confirmedMissingThisTurnCapturePIDs=missing,
      retainedBuildBinaryCompression=dict(report=str(ROOT/'audit_v4045_retained_build_binary_compression/report.json'),inspectedExactExecutables=9,reclaimedAllocatedBytes=0,everyLogicalByteAndLaunchPathUnchanged=True),
      nextImplementationAction='Poll the same confirmed-live52768/PID40096 Jax original earned-state/fault qualifier to its actual terminal; do not restart on timeout. After actual state acceptance run4040 whole retained FIFO/camera/native-ground/811 compressed-shadow matrix and actual faults, then losslessly seal four terminal scene leaves and bind all proof sources. Continue native Jax victim/effect full audio and other original finisher/victim/morph/secret/cinematic contexts. Original SonyaP2 zoning Start700 has16 rounds/106losses and no clear; next physical control plan must respond to actual failing Mileena encounter evidence rather than repeat an identical boot/strategy or change health/AI/schedule. Full multi-arena move/ground/shadow/cleanup and final combined UI/ladder/names/audio, own endings, dependency-aware old-folder cleanup and refreshed ZIP remain required.',
      fullPortAcceptance=False,finishedRelease=False,goalStatus='active')
    need(state['remaining']==remaining and state['currentCandidate']=='diagnostic_v1836_ball_register_boundary','No scope shrink or release promotion')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),freshPins=len(pins),exactJaxFields=2596,reclaimedAllocatedBytes=reclaimed,liveStateQualifierPID=40096,goalStatus='active',fullPortAcceptance=False)),flush=True)

if __name__=='__main__':main()
