"""Full-goal checkpoint: real early-kick trial, never promote failed controls."""
import ctypes,json,subprocess
from pathlib import Path
import compare_kintaro_early_airkick_v4418 as comparison
ROOT,need,sha=comparison.ROOT,comparison.need,comparison.sha
PARENT=ROOT/'audit_v4405_pressed_mirror_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4421_kintaro_early_airkick_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable original full-goal checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'All inherited source/evidence/playable bytes unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();h=sha(p);key=str(p)
        need(key not in pins or pins[key]==h,'Exact shared/inherited input bytes')
        need(wanted is None or wanted==h,'Exact executed source/report manifest');pins[key]=h
    pin(PARENT);pin(__file__)
    path=ROOT/'audit_v4419_kintaro_early_airkick_native_comparison/report.json'
    compared=json.loads(path.read_text());pin(path)
    need(compared['passed'] and not compared['earlierKickPolicyPromoted'] and
      not compared['naturalTowerClearAccepted'] and not compared['fullPortAcceptance'],
      'Actual failed trial is rejected; no imaginary Kintaro/tower clear')
    need(compared['originalForwardOutcome']['actualOwnKintaroRoundWins']==2 and
      compared['earlierKickOutcome']['actualOwnKintaroRoundWins']==0 and
      compared['earlierKickOutcome']['actualKintaroPaidLosses']==5,
      'Exact actual native outcome, not inferred from input count or sampled animation')
    for p,h in compared['inputHashes'].items():pin(p,h)
    proofpath=ROOT/'audit_v4417_kintaro_early_airkick_whole_campaign_checked/report.json'
    proof=json.loads(proofpath.read_text());pin(proofpath)
    need(proof['passed'] and proof['case']['passed'] and proof['case']['actualWholeCampaignGrammarRetained'] and
      proof['case']['onlyKintaroPhysicalKickWindowChanged'] and not proof['actualNaturalSonyaP2TowerClearAccepted'],
      'Original complete native schedule/health/KO/paid continue/true ID/morph/ending/input gates retained')
    folder=ROOT/'audit_v4414_sonya_kintaro_early_airkick_p2_campaign'
    meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
    need(meta['exit_code']==0 and meta['assistance']=='none' and not meta['cheats_enabled'] and
      meta['human_slot']==2 and meta['player']=='sonya' and meta['ramGuestSHA256']==
      '938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821' and
      meta['rawRasterFilesWritten']==meta['raw_audio_files_written']==meta['new_builds_or_rom_copies']==meta['guestDumpFilesWritten']==0,
      'Actual terminal3836 cold native SonyaP2, RAM-only guest/frames; no assistance or copies')
    for p in folder.rglob('*'):
        if p.is_file():pin(p)
    for name in ('mk2ks_kintaro_early_airkick_campaign_ram_v4410.lua',
      'tools/qualify_kintaro_early_airkick_source_v4411.py','tools/run_kintaro_early_airkick_campaign_v4413.py',
      'tools/verify_kintaro_early_airkick_whole_campaign_v4416.py','tools/compare_kintaro_early_airkick_v4418.py',
      'audit_v4412_kintaro_early_airkick_source_preflight/report.json','audit_v4415_kintaro_early_airkick_campaign_observed/report.json',
      'tools/inspect_sonya_kintaro_ground_damage_v4422.py','audit_v4423_sonya_kintaro_ground_damage/report.json'):
        pin(ROOT/name)
    groundpath=ROOT/'audit_v4423_sonya_kintaro_ground_damage/report.json';ground=json.loads(groundpath.read_text())
    need(ground['passed'] and ground['sampledGroundedDamage']==1246 and ground['sampledAirborneDamage']==40 and
      ground['groundDamageByActualSameFieldInput'].get('Down')==966 and ground['sampledNativeBlockBodies']=={'0012':2617} and
      ground['inputAndSampledActionsNotCausalAttackAttribution'] and not ground['alternativeGuardPolicyExercised'],
      'Actual baseline damage/input partitions, not inferred attack causality or a tested guard fix')
    for p,h in ground['inputHashes'].items():pin(p,h)
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_kintaro_early_airkick_campaign_v4413.py|verify_kintaro_early_airkick_whole_campaign_v4416.py|compare_kintaro_early_airkick_v4418.py|audit_v4414_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    observed=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(observed.returncode==0 and not observed.stdout.strip(),'Actual native/capture/verifier jobs terminal, no elapsed-time restart')
    get=ctypes.windll.kernel32.GetCompressedFileSizeW
    get.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];get.restype=ctypes.c_uint32
    files=[p for p in folder.rglob('*') if p.is_file()];allocated=0
    for p in files:
        high=ctypes.c_uint32();low=get(str(p),ctypes.byref(high));need(low!=0xffffffff,'Actual allocated diagnostic bytes')
        allocated+=(high.value<<32)|low
    next_action=('All five original full-goal groups remain. Held and pressed Tomb mirror scenes are already independently '
      'qualified for both added characters and both physical slots; do not rerun completed scenes. This turn prioritized '
      'actual missing SonyaP2 natural Kintaro/Shao clear. One genuine physical Kintaro kick-window experiment changed '
      'only descending-only HK to actual airborne height<90/gap<100 HK edges; native game/AI/health/difficulty/IDs/'
      'schedule/morphs/Shao/ending code stayed identical. Complete cold native prefix before changed inputs matches '
      'the4300baseline and whole campaign/physical grammar passes. Actual earlier kicks produce zero Kintaro round '
      'wins and five paid losses, versus original two isolated wins/three losses. Reject4410policy; retain4300preferred '
      'controller and earlier4320backward rejection. Actual native activations/PCs/actor/Main/inputs are separately '
      'qualified, never credited from plans. Next concrete campaign work: inspect original baseline ground/crouch '
      'damage windows and native stomp407/uppercut107 response. Original107 sampled-state damage partition725 is '
      'not causal attack attribution; own0/303 ground damage is substantial. Evaluate ordinary Block/release/crouch '
      'preparation using actual native block700/701 fields (2617observed block fields have body0012, not a presumed08), '
      'flags and observed crouch-exit/Up/native jump timing '
      '(first original attempt reaches the native jump writer after9fields), '
      'without granting actions, immunity, boss health, AI states, positions, RNG, roster or victories. Any change '
      'requires fresh source/capture leaves and complete original native campaign/input/KO/ending gates. True full '
      'Kintaro match/Shao clear/own endings/attract remain unproved. Broader Pit/Tomb victims/unpressed RNG branches/'
      'whole native stage-victim waveforms, full move art/ground/shadows across arenas/CPU/repeat/KO/overlap, other '
      'finishers/victims/morphs/secrets/cinematics, final combined selection/ladder/names/audio/dependency cleanup/'
      'refreshed release remain required. Public1836 remains unchanged playtest, not finished release.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='All original full-goal groups and inherited held/pressed mirror/campaign/strict-failure evidence retained; actual failed early-kick trial added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: fresh native cold campaign and full independent grammar/input verification; source-only early-kick trial activates genuine moves but worsens actual Kintaro outcome, so reject policy and preserve preferred baseline. Tower/ending scope remains required.',
      current3836KintaroEarlierAirKickCapture=str(folder),current3836KintaroEarlierAirKickWholeProof=str(proofpath),
      current3836KintaroEarlierAirKickComparison=str(path),current3836KintaroEarlierAirKickPolicyPromoted=False,
      current3836KintaroEarlierAirKickOutcome=compared['earlierKickOutcome'],
      current3836KintaroEarlierAirKickActualControls=compared['actualNativeControls'],
      current3836SonyaKintaroGroundDamageReport=str(groundpath),
      current3836SonyaKintaroActualGroundDamage=1246,current3836SonyaKintaroActualAirDamage=40,
      current3836SonyaKintaroGroundDamageWithActualDownOnlyFields=966,
      current3836PreferredSonyaP2PhysicalController='mk2ks_shang_jump_retry_campaign_ram_v4300.lua',
      current3836EarlierAirKickNativePID=process['pid'],current3836EarlierAirKickExecHandles=dict(capture=60850,wholeVerifier=81333),
      currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='Compressed native text/source/digest evidence only; all54native frames and full guest verified in RAM, no persisted raster/audio/ROM copies or repeated historical savings.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All original full-goal groups intact, not narrowed to this experiment')
    need(all(sha(p)==h for p,h in pins.items()),'Every current/inherited actual source/evidence/public byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),actualKintaroRoundWins=0,
      actualKintaroLosses=5,earlierKickPolicyPromoted=False,originalRemainingGroups=5,fullPortAcceptance=False,
      diagnosticAllocatedBytes=allocated),indent=2),flush=True)

if __name__=='__main__':main()
