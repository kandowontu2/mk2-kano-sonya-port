"""Preserve full port scope, actual new controller evidence, failures and exact live handle."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
import compact_current_tomb_logs_v3654 as storage
import run_sonya_guard_punish_campaign_v4119 as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
PARENT = ROOT / 'audit_v4107_jax_arms_terminal_full_scope_checkpoint/checkpoint.json'
OUT = ROOT / 'audit_v4133_guard_punish_live_full_scope_checkpoint'
FOLDER = ROOT / 'audit_v4120_sonya_guard_punish_p2_campaign'


def main():
    need(not OUT.exists(), 'Fresh immutable active-goal checkpoint')
    state = json.loads(PARENT.read_text())
    remaining = list(state['remaining'])
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         not state['fullPortAcceptance'] and not state['finishedRelease'], 'Original full goal remains incomplete')
    pins = {}

    def pin(path, wanted=None):
        path = Path(path).resolve()
        key, digest = str(path), sha(path)
        need(wanted is None or digest == wanted, 'Actual immutable evidence unchanged: ' + key)
        need(key not in pins or pins[key] == digest, 'Consistent shared evidence')
        need(key not in state['inputHashes'] or state['inputHashes'][key] == digest, 'Shared parent input unchanged')
        pins[key] = digest

    pin(PARENT)
    for path, digest in state['inputHashes'].items():
        pin(path, digest)
    reports = {}
    for leaf in ('audit_v4117_guard_punish_source_preflight',
                 'audit_v4123_guard_punish_block_readiness_source_preflight',
                 'audit_v4127_guard_punish_actual_prefix_checked',
                 'audit_v4131_stopped_campaign_evidence_compression'):
        path = ROOT / leaf / 'report.json'
        report = json.loads(path.read_text())
        need(report['passed'] and not report['fullPortAcceptance'], 'Actual bounded completed proof: ' + leaf)
        reports[leaf] = report
        pin(path)
        for path, digest in report['inputHashes'].items():
            pin(path, digest)
    prefix = reports['audit_v4127_guard_punish_actual_prefix_checked']
    observed = prefix['actualCapturedPrefix']
    need(observed['actualCompleteGuardFields'] == 16336 and observed['actualNativeLegActivations'] == 30 and
         observed['stages'] == list(range(10)) and observed['actualOwnNativeRoundWins'] == 20 and
         len(prefix['actualRowFaultsRejected']) == 10 and prefix['prefixProofOnly'] and
         not prefix['completedWholeCampaignAccepted'] and not prefix['campaignClearAccepted'],
         'Real guard input replay/activation prefix; not a whole campaign or ending proof')
    with (FOLDER / 'run.log').open('rb') as stream:
        raw = stream.read(prefix['nativeLogPrefixBytes'])
    need(len(raw) == prefix['nativeLogPrefixBytes'] and hashlib.sha256(raw).hexdigest().upper() ==
         prefix['nativeLogPrefixSHA256'], 'Exact accepted live prefix still retained in growing log')
    q = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        'Get-CimInstance Win32_Process | Where-Object { $_.ProcessId -in @(133776,37824) } | '
        'Select-Object ProcessId,ParentProcessId,Name,CommandLine | ConvertTo-Json -Compress'], capture_output=True, text=True)
    need(q.returncode == 0 and q.stdout.strip(), 'Exact current native campaign and collector live now')
    processes = json.loads(q.stdout)
    need(isinstance(processes, list) and len(processes) == 2, 'Both actual live process records')
    by_pid = {p['ProcessId']: p for p in processes}
    native, collector = by_pid[133776], by_pid[37824]
    need(native['Name'] == 'mkport_candidate.exe' and native['ParentProcessId'] == 37824 and
         capture.LUA in native['CommandLine'] and FOLDER.name in native['CommandLine'] and
         collector['Name'] == 'python.exe' and 'tools/run_sonya_guard_punish_campaign_v4119.py' in collector['CommandLine'],
         'Exact experiment identities, not stale handles or unrelated game jobs')
    need(not (FOLDER / 'result.json').exists(), 'Current capture not terminal yet')
    for name in ('input_hashes_before.json', 'source_snapshot_paths.json', 'guest_memory_proof.json', 'process.json'):
        pin(FOLDER / name)
    need(not any(p.suffix in ('.bin', '.png', '.wav') for p in FOLDER.rglob('*') if p.is_file()),
         'No new ordinary native guest/raster/audio dump copies')
    for version in (4111, 4115):
        path = ROOT / f'audit_v{version}_sonya_guard_punish_campaign_observed/report.json'
        need(json.loads(path.read_text())['passed'] is False, 'Original failed source matcher/stopped guard deadlock stays false')
        pin(path)
    for name in ('mk2ks_guard_punish_campaign_ram_v4108.lua', 'mk2ks_guard_punish_campaign_ram_v4112.lua',
                 'mk2ks_guard_punish_campaign_ram_v4118.lua', 'tools/run_sonya_guard_punish_campaign_v4109.py',
                 'tools/run_sonya_guard_punish_campaign_v4113.py', 'tools/run_sonya_guard_punish_campaign_v4119.py',
                 'tools/qualify_guard_punish_source_v4116.py', 'tools/qualify_guard_punish_source_v4122.py',
                 'tools/verify_guard_punish_prefix_v4124.py', 'tools/verify_guard_punish_prefix_v4126.py',
                 'tools/verify_guard_punish_whole_campaign_v4128.py', 'tools/compact_stopped_campaign_evidence_v4130.py',
                 'tools/save_guard_punish_live_checkpoint_v4132.py'):
        pin(ROOT / name)
    failed_source = (ROOT / 'tools/verify_guard_punish_prefix_v4124.py').read_text()
    current_source = (ROOT / 'tools/verify_guard_punish_prefix_v4126.py').read_text()
    need(failed_source.replace("OUT = ROOT / 'audit_v4125_guard_punish_actual_prefix_checked'",
                              "OUT = ROOT / 'audit_v4127_guard_punish_actual_prefix_checked'")
         .replace("r['pc'] == 'FFF80820'", "r['pc'] == 'FFF80830'") == current_source,
         'Prefix correction only actual three-word native instruction PC and fresh leaf; all replay/fault algorithm unchanged')
    text = (FOLDER / 'run.log').read_text()
    lines = text.splitlines()
    last_rows = [dict(re.findall(r'(\w+)=([^\s]+)', line)) for line in lines
                 if line.startswith(('MK2_NAT_CAMPAIGN_LOSS ', 'MK2_NAT_CAMPAIGN_STAGE '))]
    cleanup = reports['audit_v4131_stopped_campaign_evidence_compression']
    need(cleanup['reclaimedAllocatedBytes'] == 720896 and cleanup['deletedFiles'] == 0,
         'New single-count failed-log reclamation, never repeat parent savings')
    state.update(
        inputHashes=pins,
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PARENT), parentCheckpointSHA256=sha(PARENT),
                                  mergeRule='Resolve parent recursively; retain all exclusions and agree on shared immutable pins.'),
        previousCheckpoint=str(PARENT), previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: new genuine cold SonyaP2 grounded guard/punish physical policy, game/public unchanged. Initial ambiguous source matcher failed before boot; fresh unique boundary preserved failure. Native3267field experiment showed3157 actual701/005A blocking fields prevented readiness; stopped exact owned test and kept its false terminal. Fresh readiness admits original700/701 guard state, still no health/AI/RNG/schedule/register writes. Actual prefix passes16336 fields,30 native LegGrab tasks,20 own native round wins/stages0..9 and10 real row faults; not full clear. Opening mirror clears without old39loss streak, but current Mileena9 encounter repeatedly loses; no promotion. Full exact campaign PID133776/collector37824/exec42915 confirmed live; continue same handle. Draft4128 retains whole original campaign/health/schedule/morph/paid-continue/ending/boss-input algorithm plus new independent complete physical replay, unexecuted until real terminal. Two failed log leaves losslessly compacted720896bytes,0deleted/new builds or native dump copies.',
        currentDevelopmentSonyaP2GuardPrefixReport=str(ROOT / 'audit_v4127_guard_punish_actual_prefix_checked/report.json'),
        currentDevelopmentSonyaP2GuardPrefixQualified=observed,
        currentDevelopmentSonyaP2GuardPrefixLimits=dict(actualFaultsRejected=10, prefixOnly=True, towerClearAccepted=False,
                                                       endingPixelsAccepted=False, completeCampaignAudioAccepted=False),
        pendingSonyaP2GuardCampaign=dict(execSession=42915, nativePID=133776, collectorPID=37824,
            liveProcesses=processes, capture=str(FOLDER), runner=str(ROOT / 'tools/run_sonya_guard_punish_campaign_v4119.py'),
            result=str(FOLDER / 'result.json'), observationReport=str(ROOT / 'audit_v4121_sonya_guard_punish_campaign_observed/report.json'),
            completed=False, lastNativeStageOrLoss=last_rows[-1],
            currentGrowingLogLogicalBytes=(FOLDER / 'run.log').stat().st_size,
            currentGrowingLogAllocatedBytes=storage.allocated(FOLDER / 'run.log')),
        currentSonyaGuardFailuresPreserved=[str(ROOT / f'audit_v{v}_sonya_guard_punish_campaign_observed/report.json') for v in (4111,4115)],
        currentSonyaGuardPrefixPreflightFailure=dict(source=str(ROOT / 'tools/verify_guard_punish_prefix_v4124.py'),
            terminalExitCode=1, reason='Mistaken PC=entry+32; actual native LegGrab instruction fetch PC=entry+48, original whole native campaign grammar and real SPECIAL rows confirm it.',
            outputLeafNeverCreated='audit_v4125_guard_punish_actual_prefix_checked'),
        currentTurnReclaimedAllocatedBytes=720896, currentTurnDeletedFiles=0, currentTurnNewBuilds=0,
        currentTurnNewNativeAudioRasterROMCopies=0,
        cleanupAccounting='Only720896bytes reclaimed in this goal turn. Parent54194176byte scene seal was already counted; never add it again.',
        nextImplementationAction='Poll exact exec42915/nativePID133776/collector37824. They are confirmed live, not stopped by observation timeout. Native guarded SonyaP2 run currently repeatedly loses against Mileena9; do not claim clear from earlier0..9/20wins prefix and do not restart identical policy. On real terminal consume handle and inspect actual4120/result.json plus4121 observation; only then execute fresh unexecuted4128 complete native campaign qualifier to4129. If qualifier needs repair preserve failure and use fresh version/leaf. Its factory retains all original campaign and boss-input algorithms, plus independent new guard physical replay; verify every invoked source adaptation, current terminal fields, true IDs, actual health/KO/paid continues, native special tasks and own ending/attract before broad acceptance. Then losslessly seal only terminal current logs. Diagnose actual per-frame Mileena failed leg attempts/uppercut507/crouch303/roll20E and native LP+Block readiness, not sparse30field guesses; guard policy reduced mirror losses but is not a universal strategy or game fix. Remaining five groups remain unchanged, including all original arm-rip effect/audio, stock profile/edge/facing art comparisons, other finishers/victims/morphs/secrets, all arenas/move phases/shadows, actual natural SonyaP2 full tower/own endings/audio/attract, final combined UI/ladder/names/audio and dependency-aware cleanup/refreshed ZIP. No guest assistance, retired evidence resurrection, broad cleanup retry or narrow-proof promotion.',
        gameSourceAndPlayableBytesChangedThisTurn=False, fullPortAcceptance=False,
        finishedRelease=False, goalStatus='active')
    need(state['remaining'] == remaining and state['currentCandidate'] == 'diagnostic_v1836_ball_register_boundary',
         'Original full scope and public playable preserved')
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Checkpoint compressed before writes')
    (OUT / 'checkpoint.json').write_text(json.dumps(state, indent=2) + '\n')
    print(json.dumps(dict(checkpoint=str(OUT / 'checkpoint.json'), freshPins=len(pins),
        actualPrefixFields=16336, nativeLegTasks=30, actualFaultsRejected=10, currentNativePID=133776,
        liveExecSession=42915, reclaimedAllocatedBytes=720896, goalStatus='active', fullPortAcceptance=False)), flush=True)


if __name__ == '__main__':
    main()
