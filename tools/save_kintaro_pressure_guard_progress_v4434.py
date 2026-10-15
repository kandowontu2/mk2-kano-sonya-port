"""Actual SonyaP2 Kintaro match clear; full original port goal remains open."""
import ctypes,json,subprocess
from pathlib import Path
import compare_kintaro_pressure_guard_v4432 as comparison
ROOT,need,sha=comparison.ROOT,comparison.need,comparison.sha
PARENT=ROOT/'audit_v4421_kintaro_early_airkick_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v4435_kintaro_pressure_guard_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'Fresh immutable full-scope checkpoint')
    state=json.loads(PARENT.read_text());remaining=list(state['remaining']);pins=dict(state['inputHashes'])
    need(all(sha(p)==h for p,h in pins.items()),'All inherited original evidence/source/public bytes unchanged')
    def pin(p,wanted=None):
        p=Path(p).resolve();h=sha(p);key=str(p)
        need(key not in pins or pins[key]==h,'Exact shared original bytes')
        need(wanted is None or wanted==h,'Exact actual manifest bytes');pins[key]=h
    pin(PARENT);pin(__file__)
    path=ROOT/'audit_v4433_kintaro_pressure_guard_native_comparison/report.json';report=json.loads(path.read_text());pin(path)
    need(report['passed'] and report['pressureGuardPolicyPromoted'] and
      report['pressureGuardOutcome']['actualShaoStageEntered'] and not report['naturalTowerClearAccepted'] and
      not report['fullPortAcceptance'],'Actual Kintaro progression accepted, not Shao/tower/ending/full-port completion')
    for p,h in report['inputHashes'].items():pin(p,h)
    proofpath=ROOT/'audit_v4431_kintaro_pressure_guard_whole_campaign_checked/report.json'
    proof=json.loads(proofpath.read_text());pin(proofpath)
    need(proof['passed'] and proof['case']['passed'] and proof['case']['actualWholeCampaignGrammarRetained'] and
      proof['case']['onlyKintaroPhysicalPressureGuardChanged'] and not proof['actualNaturalSonyaP2TowerClearAccepted'],
      'All full native schedule/health/KO/paid continue/selection/ID/morph/boss/ending gates retained')
    folder=comparison.NEW;meta=json.loads((folder/'result.json').read_text());process=json.loads((folder/'process.json').read_text())
    need(meta['exit_code']==0 and meta['assistance']=='none' and not meta['cheats_enabled'] and
      meta['player']=='sonya' and meta['human_slot']==2 and meta['ramGuestSHA256']==
      '938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821' and
      meta['rawRasterFilesWritten']==meta['raw_audio_files_written']==meta['new_builds_or_rom_copies']==meta['guestDumpFilesWritten']==0,
      'Actual terminal native3836 whole guest/RAM frames, no assistance or copies')
    rows=comparison.current.spacing.parse((folder/'run.log').read_text())
    shao=next(r for r in rows if r['tag']=='STAGE' and r['stage']=='16')
    losses=[r for r in rows if r['tag']=='LOSS' and r['stage']=='15' and r['frame']<shao['frame']]
    lastloss=losses[-1]['frame'];wins=[r for r in rows if r['tag']=='WIN' and r['stage']=='15' and
      lastloss<r['frame']<shao['frame']]
    need(len(wins)==2 and all(r['slot']=='2' and r['id']=='18' and r['pc']=='FF8296B0' and
      int(r['health'].split(',')[0])==0 and int(r['health'].split(',')[1])>0 for r in wins),
      'Two consecutive actual owned Sonya Kintaro KO wins after last paid loss, not isolated wins from different matches')
    need(not any(r['tag'] in ('SELECT','LOSS') and wins[0]['frame']<r['frame']<wins[1]['frame'] for r in rows),
      'No paid restart/selection/loss between final two Kintaro wins')
    fights=[r for r in rows if r['tag']=='FIGHT' and r['stage']=='15' and lastloss<r['frame']<shao['frame']]
    need(fights and len({r['selection'] for r in fights})==1 and
      all(r['human']=='18:18' and r['cpu']=='12:12' for r in fights),
      'One genuine paid match selection, real Sonya18/Kintaro12 throughout native rounds')
    for win in wins:
        ko=[r for r in rows if r['tag']=='HEALTH' and r['slot']=='1' and r['after']=='0' and
          lastloss<r['frame']<win['frame']]
        need(ko and ko[-1]['pc']=='FF836700' and int(ko[-1]['before'])>0,
          'Actual original native collision health subtract reaches Kintaro zero before each winner read')
    for p in folder.rglob('*'):
        if p.is_file():pin(p)
    for name in ('mk2ks_kintaro_pressure_guard_campaign_ram_v4424.lua',
      'tools/qualify_kintaro_pressure_guard_source_v4425.py','tools/run_kintaro_pressure_guard_campaign_v4427.py',
      'tools/verify_kintaro_pressure_guard_whole_campaign_v4430.py','tools/compare_kintaro_pressure_guard_v4432.py',
      'audit_v4426_kintaro_pressure_guard_source_preflight/report.json','audit_v4429_kintaro_pressure_guard_campaign_observed/report.json'):
        pin(ROOT/name)
    query="Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='mkport_candidate.exe'\" | Where-Object { $_.CommandLine -match 'run_kintaro_pressure_guard_campaign_v4427.py|verify_kintaro_pressure_guard_whole_campaign_v4430.py|compare_kintaro_pressure_guard_v4432.py|audit_v4428_' } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"
    observed=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(observed.returncode==0 and not observed.stdout.strip(),'Actual native/collector/verifier jobs terminal, no expired observation restart')
    get=ctypes.windll.kernel32.GetCompressedFileSizeW
    get.argtypes=[ctypes.c_wchar_p,ctypes.POINTER(ctypes.c_uint32)];get.restype=ctypes.c_uint32
    files=[p for p in folder.rglob('*') if p.is_file()];allocated=0
    for p in files:
        high=ctypes.c_uint32();low=get(str(p),ctypes.byref(high));need(low!=0xffffffff,'Exact allocated capture bytes')
        allocated+=(high.value<<32)|low
    next_action=('Actual3836 SonyaP2 has now earned a full native Kintaro match clear in one paid selection: '
      'two consecutive own KO winner reads with Kintaro HP0/Sonya HPpositive, original collision subtracts, '
      'true IDs18/12, no loss/reselection between wins, and natural Shao stage16 entry. Full native campaign '
      'grammar and complete independent physical-input replay pass; actual guarded pressure waiting and '
      'block-to-forward-jump attempts/native jump/airkick writers qualify separately. Prefer4424pressure-guard '
      'controller over4300for the unfinished SonyaP2 tower, but do not change game source, difficulty, AI, '
      'health, identity, flags, positions, RNG or schedule. Stomp HP/forward jump/descending kick/Shao inputs '
      'remain original. Earlier4410kick and4320backward trials stay rejected. The1500second native observation '
      'is actually terminal0 and reachedShao only at81677; it is not a complete Shao clear or own ending. '
      'Next use a fresh declared longer host-only observation of the same cold ordinary campaign to cover '
      'Shao and own ending/return-to-attract, preserving all complete native input/health/KO/selection/morph/'
      'ending gates and comparing the bounded4431native prefix byte-for-byte. Do not restart any live job '
      'because an observation call expires, do not shorten/native-assist the tower, and do not force ending '
      'markers. RAM-only guest/raster/PCM sinks and compressed text remain mandatory. True Shao/full tower/'
      'ending art/audio/attract acceptance stays open. All five original full-goal groups remain required, '
      'including broader Pit/Tomb victims/unpressed RNG/native full waveform, full move art/ground/shadows '
      'across arenas/CPU/repeat/KO/overlap, other finishers/victims/morphs/secrets/cinematics, final combined '
      'selection/ladder/names/audio/dependency cleanup/refreshed release. Completed held/pressed Tomb mirror '
      'cases must not be replayed. Public1836 remains unchanged playtest, not a finished release.')
    state.update(previousCheckpoint=str(PARENT),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PARENT),parentCheckpointSHA256=sha(PARENT),
        mergeRule='Every original full-goal group/inherited evidence/strict exclusion retained; actual native SonyaP2 Kintaro match clear added.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: native cold SonyaP2 pressure guard/release trial earns two consecutive full Kintaro KO wins in one selection and advances naturally to Shao. Full original campaign grammar and actual input/state/writer counterexamples retained; Shao/own endings/full-port remain open.',
      current3836SonyaP2KintaroMatchClearAccepted=True,current3836SonyaP2KintaroConsecutiveOwnWins=wins,
      current3836SonyaP2NativeShaoEntry=shao,current3836SonyaP2PressureGuardComparison=str(path),
      current3836SonyaP2PressureGuardWholeProof=str(proofpath),current3836SonyaP2PressureGuardCapture=str(folder),
      current3836SonyaP2PressureGuardActualControls=report['actualNativeControls'],
      current3836PreferredSonyaP2PhysicalController='mk2ks_kintaro_pressure_guard_campaign_ram_v4424.lua',
      current3836SonyaP2FullShaoClearAccepted=False,current3836SonyaP2OwnEndingAttractAccepted=False,
      current3836PressureGuardNativePID=process['pid'],current3836PressureGuardExecHandles=dict(capture=18872,wholeVerifier=97516),
      currentTurnDiagnosticLogicalBytes=sum(p.stat().st_size for p in files),currentTurnDiagnosticAllocatedBytes=allocated,
      currentTurnNewBuilds=0,currentTurnRawAudioRasterVRAMROMCopies=0,currentTurnDeletedFiles=0,currentTurnReclaimedAllocatedBytes=0,
      cleanupAccounting='Compressed text/source/digest evidence only;50native frames/full guest verified in RAM, no new media/ROM/build copies or repeated historical savings.',
      gameSourceAndPlayableBytesChangedThisTurn=False,publicLauncherChangedThisTurn=False,publicReleaseZIPChangedThisTurn=False,
      nextAction=next_action,nextImplementationAction=next_action,goalStatus='active',fullPortAcceptance=False,finishedRelease=False)
    need(state['remaining']==remaining and len(remaining)==5,'All original full-goal requirements intact')
    need(all(sha(p)==h for p,h in pins.items()),'Every inherited/current source/evidence/public pinned byte unchanged')
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Checkpoint compressed before writes')
    (OUT/'checkpoint.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(OUT/'checkpoint.json'),inputPins=len(pins),actualKintaroMatchClearAccepted=True,
      fullShaoClearAccepted=False,fullPortAcceptance=False,originalRemainingGroups=5,diagnosticAllocatedBytes=allocated),indent=2),flush=True)

if __name__=='__main__':main()
