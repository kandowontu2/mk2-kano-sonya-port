"""Keep the entire natural-character goal active after a reproduced real defect."""
import json,subprocess
from pathlib import Path
import run_native_sound_delivery_ram_v3682 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
PARENT=ROOT/'audit_v3763_guarded_p2_campaign_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3798_mileena_cache_full_scope_checkpoint'
def main():
    need(not OUT.exists(),'Fresh full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins={}
    need(len(remaining)==5 and state['goalStatus']=='active'and not state['fullPortAcceptance']and not state['finishedRelease'],'Original complete objective remains open')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);digest=sha(path)
        need(wanted is None or digest==wanted,'Immutable input '+key)
        need(key not in pins or pins[key]==digest,'Consistent fresh pin')
        need(key not in state['inputHashes']or state['inputHashes'][key]==digest,'Inherited evidence not relabelled')
        pins[key]=digest
    proof_path=ROOT/'audit_v3794_mileena_cache_cause_checked/report.json';proof=json.loads(proof_path.read_text());pin(proof_path)
    need(proof['passed']and len(proof['cases'])==4 and not proof['stabilityFixAccepted']and not proof['gameSourceOrPlayableBytesChanged'],'Real cause proof, never a completed fix')
    for path,h in proof['inputHashes'].items():pin(path,h)
    need(sum(len(case['actualRowFaultsRejected'])for case in proof['cases'])==44,'Forty-four actual-row faults rejected')
    storage_path=ROOT/'audit_v3796_mileena_cache_log_compression/report.json';storage=json.loads(storage_path.read_text());pin(storage_path)
    need(storage['passed']and storage['deletedFiles']==0 and storage['reclaimedAllocatedBytes']==10149888,'Exact lossless storage outcome')
    for path,h in storage['inputHashes'].items():pin(path,h)
    failed=ROOT/'audit_v3775_guarded_sonya_p2_extended_state_checked/report.json';pin(failed)
    need(not json.loads(failed.read_text())['passed'],'Strong original native-state failure preserved')
    for leaf in ('audit_v3768_guarded_sonya_extended_p2_campaign','audit_v3778_campaign_cache_provenance','audit_v3783_mileena_earned_cache'):
        folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text())
        need(meta.get('exit_code',meta.get('terminalExitCode'))==0,'Stopped diagnostic, not emulator exit alone as success')
        for path in folder.rglob('*'):
            if path.is_file():pin(path)
    no_action=(ROOT/'audit_v3783_mileena_earned_cache/run.log').read_text()
    need('action=-1'in no_action and 'frame=7000'in no_action,'Failed short-controller approach preserved, not a finisher acceptance')
    for source in ('tools/verify_mileena_cache_cause_v3791.py','tools/verify_mileena_cache_cause_v3793.py',
      'tools/run_mileena_earned_cache_matrix_v3789.py','mk2ks_mileena_earned_guest_v3787.lua',
      'mk2ks_mileena_earned_victim_v3781.lua','mk2ks_mileena_earned_victim_v3784.lua',
      'mk2ks_cache_provenance_retained_v3780.lua','tools/save_mileena_cache_checkpoint_v3797.py'):
        pin(ROOT/source)
    public={
      'diagnostic_v1836_ball_register_boundary/mkport_candidate.exe':'34D427A8FB152E89F4B5FDA5CCE7A8BDB2CC3020CD66C42979B53ED1BA15263E',
      'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata':'5646E839C73C4DB89BCF7CC87ECADBDA94B1E0D30EB1C0D2ED50A21A5524E23D',
      'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip':'994AC5535CD65EA92B7BCD19E12EC6669F4527796CD0CA8C7CA28E708A6897EA',
      'mame-mkp/mkport.exe':'413855890FCE3BECAC9B24E11699FAD1CE465ACCBE4B27A93F2DD5819D13A891',
      'mame-mkp/src/mame/midway/midtunit_m.cpp':'EE48F2FBD72749354A44F3B6574D00EB5DD879EC368A73FBDD57540A4F351D34',
      'mame-mkp/src/mame/midway/midtunit.cpp':'07C1FA27AAA0B1C836E462BC6EC13D62DFF405FA2B7F1358D7BB34B51731DA85',
      'mame-mkp/src/mame/midway/midtunit.h':'256577139683DE7226D3EC0966CAC9B44C9C01C96ED561D236112B2DBADC7644'}
    for path,h in public.items():pin(ROOT/path,h)
    pin(ROOT/state['currentCMD']);pin(PARENT)
    # Old 31936 and every newly captured child are authoritatively missing now.
    ids=[31936,34364,119256,116172,126200,52648,112736]
    check=subprocess.run(['powershell.exe','-NoProfile','-Command',
      'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @('+','.join(map(str,ids))+') } | Select-Object -ExpandProperty ProcessId'],capture_output=True,text=True)
    need(check.returncode==0 and not check.stdout.strip(),'All recorded capture children stopped; no stale live handles')
    state['inputHashes']=pins
    state.update(inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=pins[str(PARENT)],
      mergeRule='Resolve parent recursively, preserving retired/deleted exclusions. Fresh pins agree with inherited keys; do not flatten historical map.'),
      previousCheckpoint=str(PARENT),previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: extended3680SonyaP2 stopped; strict3775native-state gate rejected real cache corruption at223502, no tower clear. New unmodified cold replay3778 reproduces byte-identical controller/combat prefix and same corrupting frame; added trace handles were unretained and collected, honestly not accepted. Source/table analysis corrects CPU5 toMileena, notReptile9. Source-derived native HK charge>=128/gap<=69 enables a genuine two-human short reproduction: both trueKano17/Sonya18 victims in both slots earn322original collision damage across two full rounds, actualFF8D2410fatality, nativeFF9E7D70victim task, exactFF83B850ID-indexed reads, followed byFF838860global cache overrun.3794independent wholeguest/source/table/state qualification and44actual-row faults accepted for defect cause only, NOT stability or art. Three added initialized1MiBguests equal independentexpected bytes. No new EXE/payload/ROM/audio/raster or game edits.3796lossless stopped-log compression reclaims10149888allocatedbytes,0deletions. All five remaining groups and public/dirty user checkout preserved.',
      pendingSonyaP2ExtendedCampaign=None,pendingSonyaP2ZoningQualificationExecSession=None,
      current3680SonyaP2ExtendedCampaignStateAccepted=False,
      current3680SonyaP2ExtendedCampaignRejectedReport=str(failed),
      current3680MileenaEatenVictimCacheCauseAccepted=True,
      current3680MileenaEatenVictimCacheCauseReport=str(proof_path),
      current3680MileenaEatenVictimSafeOrArtAccepted=False,
      current3680MileenaEatenVictimActualContexts=[dict(fighter=c['fighter'],victimSlot=c['victimSlot'],capture=c['capture'],cause=c['cause'])for c in proof['cases']],
      current3680MileenaCauseActualRowFaultsRejected=44,
      current3680StockCpuIdentityCorrection='Mileena=5, Reptile=9; preserve diagnostic history, do not reinterpret previous narrow tests as this branch coverage.',
      current3680ColdCacheReproductionObserverAccepted=False,
      current3680ColdCacheReproductionOriginalControllerPrefixMatched=True,
      current3680ColdCacheReproductionObserverFailure='3776tap userdata not held in registered closure; MAME tap_helper destructor removes handlers.3780register_frame explicitly retains all five taps and actual callbacks verified in four contexts. Keep original3778records0/bad_frame-1; not a pointer-provenance proof.',
      currentTurnSourceSyntaxFailure=dict(path=str(ROOT/'tools/verify_mileena_cache_cause_v3791.py'),error='SyntaxError: else18/else0/else1; preserved. Fresh3793 source passes3794.'),
      currentTurnFailedShortController=dict(capture='audit_v3783_mileena_earned_cache',nativeFatalityActivated=False,reason='Requested gap<=58 is below actual native body separation near60; approached forever. Fresh3784 uses exact native<=69 gate and early blocked HK charge; actual native fatality proved.'),
      currentTurnSealedDiagnosticCompression=dict(report=str(storage_path),allocatedBytesFreed=10149888,deletedFiles=0),
      gameSourceAndPlayableBytesChangedThisTurn=False,developmentCandidate=current.NAME,
      nextAction='Implement proper native Mileena eaten-victim data/art, not a proxy, a cache clamp, NULL skip, AI disable or changed bot/health. Missing original consumer operandFF9E7EA0->FF9E9140: trueKano17 readsFF9E9520 (group, not stream); trueSonya18 reads0, causing native cache overflow. Need independent own body-consumption poses/terminated streams/19-ID table with original rows and scheduler/palette/retirement preserved. Inspect exact stock grammar and art first; existing generated-death/inflation/torso pipeline uses character-owned raster assets, cannot stand-in Kitana/Liu. imagegen skill main inspected completely but not used this turn; read applicable shared prompt references and view actual local references before any new raster generation. Original input-only shorter controller3784 plus retained observer3780 now offers reproducible all4contexts; use new immutable leaves for fixes/verification. Full native stage/victim audio, movephase/art/ground/floorshadow/erase arenas CPU/repeat/KO/overlap, otherfinishers/victims/morphs/secrets/cinematics, actual guardedSonyaP2remainingtower/bosses/ownending/attract and P2endingpixels/audio, final combined regression/cleanup/refreshedpublicZIP remain. Keep accepted earlier scoped proofs and recursive retired exclusions. No current live capture handles.')
    need(state['remaining']==remaining and state['goalStatus']=='active'and not state['fullPortAcceptance']and not state['finishedRelease'],'Original broad scope intact')
    OUT.mkdir();path=OUT/'checkpoint.json';path.write_text(json.dumps(state,indent=2)+'\n')
    digest=sha(path);compact=subprocess.run(['compact.exe','/C','/I','/Q',str(path)],capture_output=True)
    need(compact.returncode==0 and sha(path)==digest,'Every checkpoint byte preserved')
    print(json.dumps(dict(checkpoint=str(path),causeContexts=4,actualRowFaultsRejected=44,allocatedBytesFreed=10149888,
      freshPins=len(pins),fullPortAcceptance=False,stabilityFixAccepted=False,pendingProcesses=None),indent=2),flush=True)
if __name__=='__main__':main()
