"""Reject weaker physical strategy, reclaim retained evidence space, preserve full goal."""
import json,subprocess
from pathlib import Path
import verify_current_kintaro_direction_comparison_v4336 as comparison
ROOT,need,sha=comparison.ROOT,comparison.need,comparison.sha
PARENT=ROOT/'audit_v4313_scorpion_clear_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4339_kintaro_rejection_cleanup_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable complete-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    for p,h in pins.items():need(sha(p)==h,'All inherited logical bytes unchanged, including compacted old audio')
    def pin(path,wanted=None):
        path=Path(path).resolve();key=str(path);h=sha(path)
        need(key not in pins or pins[key]==h,'Shared/inherited evidence unchanged')
        need(wanted is None or h==wanted,'Exact new executed input/report pin');pins[key]=h
    pin(PARENT);pin(__file__)
    names=('audit_v4317_current_kintaro_damage_windows','audit_v4322_kintaro_backward_escape_source_preflight',
      'audit_v4325_kintaro_backward_escape_campaign_observed','audit_v4327_kintaro_backward_escape_actual_prefix_checked',
      'audit_v4329_kintaro_backward_escape_whole_campaign_checked','audit_v4337_current_kintaro_direction_comparison',
      'audit_v4333_frozen_boss_audio_compaction','audit_v4335_frozen_kintaro_audio_compaction')
    reports={}
    for name in names:
        path=ROOT/name/'report.json';r=json.loads(path.read_text())
        need(r['passed'] and not r.get('fullPortAcceptance',False),'Actual bounded qualified evidence only')
        pin(path);reports[name]=r
        for p,h in r.get('inputHashes',r.get('case',{}).get('inputHashes',{})).items():pin(p,h)
    c=reports[names[4]]['case'];v=reports[names[5]];a=reports[names[0]]['actualKintaroTiming']
    need(c['passed'] and c['actualWholeCampaignGrammarRetained'] and
      c['actual3836P2WholeCampaignAlgorithmRetained'] and c['actualKintaroPhysicalDirectionIndependentlyReplayed'],
      'Complete actual native grammar and independently replayed declared backward inputs')
    need(c['native_own_round_wins']==30 and c['paid_continue_losses']==10 and
      c['stages_reached']==list(range(13))+[14,15] and c['ending_starts']==c['ending_completions']==0 and
      not c['unassisted_clear_proven'],'Actual finite native negative outcome, not tower/ending clear')
    need(v['identicalNativePrefixRows']==113060 and v['actualNativeControls']['actualBackwardPressurePlans']==125 and
      v['actualNativeControls']['firstActualDirectionChangeFrame']==61841 and not v['backwardPolicyPromoted'],
      'Actual identical native campaign prefix and exact new inputs; reject weaker experiment')
    need(v['oldForwardPressureOutcome']['actualOwnKintaroRoundWins']==2 and
      v['oldForwardPressureOutcome']['actualKintaroPaidLosses']==3 and
      v['newBackwardPressureOutcome']['actualOwnKintaroRoundWins']==0 and
      v['newBackwardPressureOutcome']['actualKintaroPaidLosses']==5,'Exact bounded old/new Kintaro outcomes')
    need(a['actualNativeJumps']==96 and a['actualNativeAirKicks']==94 and
      a['actualTaskStoresWithDifferentWriterMain']==14 and a['sampledActionNotAttackCausality'],
      'Native jump/kick dispatches; other writer contexts and sampled health state never promoted to activation/attack causality')
    cleanup=[reports[names[6]],reports[names[7]]]
    done=[row for report in cleanup for row in report['verifiedFiles']]
    need(len(done)==8 and len({row['path'] for row in done})==8 and
      all(report['deletedFiles']==0 and report['originalPathsBytesSizesTimestampsPreserved'] for report in cleanup),
      'Eight disjoint original files remain byte/size/timestamp exact, zero deletion')
    reclaimed=sum(report['reclaimedAllocatedBytes'] for report in cleanup)
    need(reclaimed==1582383104 and reclaimed==sum(row['reclaimed'] for row in done),
      'Only actual new allocated savings counted once; no historical4207 savings added')
    for report in cleanup:
        for row in report['targets']:pin(row['path'],row['sha256'])
    for name in ('tools/analyze_current_kintaro_damage_windows_v4314.py',
      'tools/analyze_current_kintaro_damage_windows_v4316.py','mk2ks_kintaro_backward_escape_campaign_ram_v4320.lua',
      'tools/qualify_kintaro_backward_escape_source_v4321.py','tools/run_kintaro_backward_escape_campaign_v4323.py',
      'tools/verify_kintaro_backward_escape_prefix_v4326.py','tools/verify_kintaro_backward_escape_whole_campaign_v4328.py',
      'tools/compact_frozen_boss_audio_sample_v4332.py','tools/compact_frozen_kintaro_audio_sample_v4334.py',
      'tools/verify_current_kintaro_direction_comparison_v4336.py'):pin(ROOT/name)
    need(not (ROOT/'audit_v4315_current_kintaro_damage_windows').exists(),
      'Failed initial analysis source preserved; no invented passing report')
    for name in ('audit_v4333_frozen_boss_audio_compaction','audit_v4335_frozen_kintaro_audio_compaction'):
        pin(ROOT/name/'plan.json')
    q=subprocess.run(['powershell.exe','-NoProfile','-Command',
      "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.ProcessId -eq 133572 -or $_.CommandLine -match 'run_kintaro_backward_escape_campaign_v4323.py|verify_kintaro_backward_escape_prefix_v4326.py|verify_kintaro_backward_escape_whole_campaign_v4328.py|compact_frozen_boss_audio_sample_v4332.py|compact_frozen_kintaro_audio_sample_v4334.py|verify_current_kintaro_direction_comparison_v4336.py' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],capture_output=True,text=True)
    need(q.returncode==0 and not q.stdout.strip(),'Actual specific native/collector/prefix/whole/comparison/compaction jobs terminal; handles consumed')
    next_action=('Do not promote/repeat Kintaro backward-pressure4320: verified0own Kintaro rounds/5paid Kintaro losses '
      'versus2own rounds/3losses with forward pressure4300, with113060identical native campaign records before first input '
      'change61841 and125actual backward plans. Preferred baseline4300/4309 remains unchanged; no tower/ending clear. '
      'Original Kintaro inputs really produced96native jumps/94airkicks: ignoredUp is not the main demonstrated cause. '
      'Same-frame damage partitions are observations, not causal attack credit. Native Main byte-clear stores with another '
      'A13 were incorrectly rejected by4314;4316 excludes them from activation counts while retaining exact setter PCs/regs '
      'for actual jumps/kicks. Continue a distinct open native fidelity group, e.g. broader Pit/Tomb branch/victim/mirror and '
      'stage/victim audio, instead of repeated rejected direction variations; inspect its latest accepted scope and gaps before '
      'new immutable capture. Full five-group goal remains: stage/finisher fidelity, all move art/ground/floor shadows/erase '
      'across arenas/CPU/repeat/KO/overlap, other finishers/victims/morphs/secrets/cinematics, actual complete towers/own endings/'
      'attract, final combined UI/names/audio/dependency cleanup/refreshed release. Public1836 remains unchanged playtest. '
      'Eight old retained wave files now losslessly LZX-compressed with1582383104Bnew allocated savings; original paths/bytes/'
      'sizes/timestamps retained, no deletion, no historical savings recounted.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every full-goal requirement/exclusion and inherited logical byte retained; NTFS storage changes only.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: actual Kintaro timing and one-direction physical experiment qualified; weaker backward variant rejected after same113060record prefix, so baseline retained. Eight retained original wave files losslessly compacted,1582383104Bnew allocated savings, no deletion or game/public changes.',
      currentKintaroNativeTimingReport=str(ROOT/names[0]/'report.json'),
      currentKintaroDirectionComparisonReport=str(ROOT/names[5]/'report.json'),
      currentRejectedKintaroBackwardExperiment=dict(capture=str(comparison.NEW),nativePID=133572,
        captureExecHandle=4897,prefixExecHandle=48487,wholeExecHandle=94020,comparisonExecHandle=66870,
        allExitCodes=0,collectorPIDNotRecorded=True,actualOwnRoundWins=30,totalPaidLosses=10,
        actualOwnKintaroRoundWins=0,actualKintaroPaidLosses=5,endingStarts=0,endingCompletions=0,
        independentlyReplayedNativeCampaignAndNewPhysicalInputs=True,controllerPromoted=False,
        gameSourceChanged=False,fullPortAcceptance=False),
      preferredNativeSonyaP2Controller=str(ROOT/'mk2ks_shang_jump_retry_campaign_ram_v4300.lua'),
      preferredControllerNativeReport=str(ROOT/'audit_v4309_shang_jump_retry_whole_campaign_checked/report.json'),
      preservedCurrentKintaroAnalyzerFailure=dict(source=str(ROOT/'tools/analyze_current_kintaro_damage_windows_v4314.py'),
        error='Assumed every BOSS_ACTION writer A13 equals own Main; actual native byte clear may write it using another Main context.',
        nativeExampleFrame=63873,nativeExamplePC='FF83A100',correctedObservationalReport=str(ROOT/names[0]/'report.json'),
        actualNonActorWriterContexts=14,moveActivationsRequireExactNativeSetterPCAndOwnedRegisters=True,
        failedSourceNotEdited=True,noMissingEventsRecreated=True),
      currentLosslessFrozenBossAudioCleanupReports=[str(ROOT/names[6]/'report.json'),str(ROOT/names[7]/'report.json')],
      currentLosslessFrozenBossAudioCleanupExecHandles=[12995,30638],
      currentTurnReclaimedAllocatedBytes=reclaimed,currentTurnDeletedFiles=0,currentTurnNewBuilds=0,
      currentTurnNewNativeAudioRasterROMCopies=0,
      cleanupAccounting='1582383104B measured new savings across8disjoint old wave files; SHA256/size/mtime/path exact, no deletion. Prior4207savings3392749568B and older deletions not counted again.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All five original requirements retained exactly')
    for p,h in pins.items():need(sha(p)==h,'All new/inherited original logical bytes exact')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compress checkpoint before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),pins=len(pins),
      backwardPressurePromoted=False,preferredForwardPressureRetained=True,actualNewAllocatedBytesReclaimed=reclaimed,
      deletedFiles=0,allOriginalRemainingGroups=5,fullPortAcceptance=False),indent=2),flush=True)

if __name__=='__main__':main()
