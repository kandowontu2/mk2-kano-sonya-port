"""Retained native CPU cue gap closure; bounded storage and exact doc history."""
import json, subprocess
from pathlib import Path
import kano_ball_launch_context_v6642 as current
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated
ROOT, need, sha = current.ROOT, current.need, current.sha


def main():
    out = ROOT/'audit_challenger_retained_precombat_progress_storage'
    need(not out.exists() and not native.census(), 'Fresh journal, original native execution terminal')
    parentpath = ROOT/'audit_morph_startup_return_progress_storage/report.json'
    parent = json.loads(parentpath.read_text()); need(parent['passed'] and len(parent['remaining'])==6, 'Full original scope retained')
    pins = {str(parentpath): sha(parentpath)}; migrations = []
    for p, h in parent['inputHashes'].items():
        path = Path(p).resolve()
        if path.parent == ROOT and path.name in ('CURRENT_PLAYTEST_STATUS.md', 'WORKSPACE_CLEANUP_CURRENT.md'):
            old = ROOT/'status_history_challenger_retained_precombat'/path.name
            need(sha(old)==h, 'Exact previous root-document bytes retained')
            migrations.append(dict(priorLogicalPath=str(path), priorSHA256=h, historicalBytes=str(old), currentSHA256=sha(path)))
            path = old
        need(sha(path)==h, 'Every retained original source/evidence pin intact')
        pins[str(path)] = h
    proofpath = ROOT/'audit_challenger_retained_precombat_checked/report.json'
    faultpath = ROOT/'audit_challenger_retained_precombat_faults/report.json'
    proof, faults = (json.loads(p.read_text()) for p in (proofpath, faultpath))
    need(proof['passed'] and faults['passed'] and proof['nativeTerminal']['pid']==69532 and proof['nativeTerminal']['nativeExit']==0, 'Actual same-terminal checked route')
    need(proof['completeSourceWaveform']['comparedStereoFrames']==1986240 and proof['completeSourceWaveform']['differentChannelSamples']==0 and len(faults['actualFaultsRejected'])==16, 'Entire finite source match and actual semantic counterexamples')
    need(proof['originalColdRecorderStillRejected'] and not proof['bootAudioAccepted'] and proof['newNativeBoots']==0, 'Original boot failure preserved, same execution never replayed')
    folders = [ROOT/name for name in ('audit_launch_challenger_fullcold_ball_p2_delay1', 'audit_challenger_retained_precombat_checked', 'audit_challenger_retained_precombat_faults', 'audit_challenger_precombat_DAC_ordinal_rejection', 'status_history_challenger_retained_precombat')]
    files = {p for folder in folders for p in folder.rglob('*') if p.is_file()}
    files.update(ROOT/name for name in ('mk2ks_launch_challenger_fullcold.lua', 'tools/capture_launch_challenger_fullcold.py', 'tools/qualify_challenger_retained_precombat.py', 'tools/qualify_challenger_retained_precombat_v2.py', 'tools/check_challenger_retained_precombat.py', 'tools/journal_challenger_retained_precombat.py', 'CURRENT_PLAYTEST_STATUS.md', 'WORKSPACE_CLEANUP_CURRENT.md'))
    for path, report in ((proofpath, proof), (faultpath, faults)):
        pins[str(path)] = sha(path)
        for p, h in report['inputHashes'].items(): need(sha(p)==h, 'Whole executed current proof sources intact'); pins[p]=h
    need(all(p.resolve().is_relative_to(ROOT) and not p.is_symlink() for p in files) and not any(p.suffix.lower() in ('.png', '.wav', '.bin', '.exe', '.zip') for p in files), 'Bounded source/evidence targets only; no raw media or candidate payload')
    storage = []; seen = set(); total = 0
    for p in sorted(files):
        h = sha(p); st = p.stat(); before = allocated(p)
        need(subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(p)], capture_output=True).returncode==0 and sha(p)==h, 'Exact lossless evidence compression')
        after = allocated(p); key = st.st_dev, st.st_ino
        if key not in seen: total += after; seen.add(key)
        pins[str(p)] = h; storage.append(dict(path=str(p), sha256=h, beforeAllocatedBytes=before, allocatedBytes=after))
    current.expected()
    builds = [p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]
    need(len(builds)==16 and not (ROOT/'mame-mkp/build/mingw-gcc').exists() and not native.census() and all(sha(p)==h for p,h in pins.items()), 'All actual source/launcher pins stable, no new build/cache/live game')
    report = dict(passed=True, candidate=current.NAME, goalStatus='active', fullPortAcceptance=False,
        previousGoalTurnClassification='no progress: acknowledgement only; all1531 parent pins and the retained authoritative native terminal revalidated before qualification',
        thisGoalTurnClassification='progress: intact precombat interval closes actual CPU source-clock gap on same terminal run, whole waveform/owner/health/gameplay/DAC/ROM qualified, actual faults rejected and bounded evidence compressed',
        actualNativePID=69532, continuousPhysicalFields=4528, continuousBattleChannels=9056,
        comparedStereoFrames=1986240, differentChannelSamples=0, semanticFaultsRejected=16,
        waveformDACROMFaultsRejected=len(proof['completeSourceWaveform']['actualFaultsRejected'])+len(proof['sourceDAC']['faults'])+len(proof['wholeSoundROM']['faults']),
        completeKanoP2ChallengerMixedAudioAccepted=True, wholeColdBootAudioAccepted=False,
        remaining=parent['remaining'], nextAction='Released-input cross-character continues and ordinary post-continue controls on current v6640; inspect full v6621/6614 gates and adapt only actual current source provenance. Then remaining integration and final matching public launcher/release.',
        originalExpandedRecorderReportStillFalse=True, allRAMHostsReleased=True, publicPlayableChanged=False,
        newNativeBoots=0, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
        retainedCompiledCandidates=16, selectedFileCount=len(files), uniqueSelectedAllocatedBytes=total,
        inputHashes=pins, intentionalDocumentationPinMigrations=migrations, exactCompressedTargets=storage)
    out.mkdir(); path = out/'report.json'; path.write_text(json.dumps(report, indent=2)+'\n'); h=sha(path)
    need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h, 'Lossless progress checkpoint')
    print(json.dumps({k: report[k] for k in ('passed','comparedStereoFrames','semanticFaultsRejected','waveformDACROMFaultsRejected','selectedFileCount','uniqueSelectedAllocatedBytes','newBuilds')}), flush=True)


if __name__=='__main__': main()
