"""Validate preserved attempts and reclaim bounded diagnostic storage/RAM."""
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT = Path(__file__).resolve().parents[1]
FOLDERS = ('audit_natural_smoke_route_kano_p2',
           'audit_natural_smoke_route_kano_p2_portal_entry_correction',
           'audit_natural_smoke_route_sonya_p1_deliberate_uppercuts')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest().upper()


def main():
    out = ROOT/'audit_natural_smoke_rotation_progress_storage'
    assert not out.exists() and not native.census()
    files, cases = set(), []
    for name in FOLDERS:
        folder = ROOT/name
        report = json.loads((folder/'report.json').read_text())
        terminal = report['nativeTerminal']
        assert terminal['nativeExit'] == 0 and not terminal['hostDecodeErrors']
        handle = native.k.OpenProcess(0x1000, False, terminal['actualWindowsIdentity']['ParentProcessId'])
        if handle:
            native.k.CloseHandle(handle)
            raise ValueError('Actual retained RAM collector still live')
        with gzip.open(folder/'executed_sources.json.gz', 'rt', encoding='utf-8') as f:
            sources = json.load(f)
        for path, wanted in report['inputHashes'].items():
            if path in sources:
                assert sources[path]['sha256'] == wanted == hashlib.sha256(sources[path]['text'].encode()).hexdigest().upper()
            else:
                assert sha(path) == wanted
        preserved = json.loads((folder/'preserved_failure.json').read_text())
        assert preserved['preservedFailedAttempt'] and not preserved['secretRouteAccepted'] and not preserved['gameSideSecretFailureEstablished']
        contract = folder/'arena_rotation_contract.json'
        if contract.exists():
            case = json.loads(contract.read_text())
            assert case['passed'] and not case['actualSecretFightAccepted'] and not case['fullPortAcceptance']
            assert len(case['actualFaultsRejected']) == 7 and case['nativeMatches'] == 13
            assert case['captureLogSHA256'] == sha(folder/'run.log.gz')
            assert case['originalTransportReportSHA256'] == sha(folder/'report.json')
            assert all(sha(p) == h for p,h in case['sourceHashes'].items())
            cases.append(case)
        files.update(p for p in folder.rglob('*') if p.is_file())
    assert len(cases) == 2 and sum(c['earnedTwoWinWindows'] for c in cases) == 25
    files.update(ROOT/'tools'/name for name in ('capture_natural_smoke_route.py', 'check_natural_smoke_route.py',
                  'preserve_natural_smoke_attempt.py', 'seal_natural_smoke_rotation.py',
                  'inspect_natural_smoke_route.py', 'inspect_native_smoke_callers.py', Path(__file__).name))
    files.add(ROOT/'mk2ks_natural_smoke_route.lua')
    targets = []
    for path in sorted(files):
        assert path.resolve().is_relative_to(ROOT) and not path.is_symlink()
        assert path.suffix.lower() not in ('.exe', '.mdata', '.zip', '.wav', '.png', '.bin', '.pcm', '.rgb')
        before, wanted = allocated(path), sha(path)
        subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)], capture_output=True, check=True)
        assert sha(path) == wanted
        targets.append(dict(path=str(path), sha256=wanted, beforeAllocatedBytes=before, allocatedBytes=allocated(path)))
    parent = ROOT/'audit_launch_stage_advance_progress_storage/report.json'
    prior = json.loads(parent.read_text())
    assert prior['passed'] and len(prior['remaining']) == 6
    assert len([p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]) == 16
    assert not (ROOT/'mame-mkp/build/mingw-gcc').exists()
    assert 'PLAY_CURRENT_V6508_CHECKED.cmd' in (ROOT/'PLAY_MK2_KANO_SONYA.cmd').read_text()
    report = dict(passed=True, objective=prior['objective'] if 'objective' in prior else 'Kano and Sonya appear as a natural part of the game in all aspects',
                  goalStatus='active', candidate='diagnostic_v6640_kano_ball_launch',
                  previousGoalTurnClassification='no progress: acknowledgement only; live RAM carrier and native terminal revalidated',
                  thisGoalTurnClassification='progress: corrected physical Portal entry, two complete earned arena-rotation/health/ownership gates and fourteen actual record faults; secret attempts remain unaccepted',
                  actualNativeMatches=26, actualEarnedTwoWinWindows=25, actualPortalMatches=2,
                  continuousPhysicalFields=sum(c['wholePhysicalAndHealthLedger']['continuousPhysicalFields'] for c in cases),
                  actualNativeHealthWrites=sum(c['wholePhysicalAndHealthLedger']['allNativeHealthWrites'] for c in cases),
                  actualFaultsRejected=14, originalControllerFailuresPreserved=True,
                  originalCheckerRejectionsPreserved=4, actualSecretFightAccepted=False,
                  fullSecretAudioAccepted=False, allRAMHostsReleased=True, fullPortAcceptance=False,
                  originalRemainingScope=prior['remaining'],
                  nextAction='Use the revised native uppercut/Toasty task/RNG-branch recorder in a new physical-slot route. Distinguish missing native popup from test recognition; prove original Down+Start secret entry and true added-human versus Smoke14 CPU controls without writes or forced RNG. Then resolve the concrete remaining finisher/cinematic source exposure and final matching CMD/ZIP.',
                  currentControllerPreflightOnly=True, latestControllerRuntimeAccepted=False,
                  selectedFiles=len(files), allocatedBytes=sum(v['allocatedBytes'] for v in targets),
                  exactCompressedTargets=targets, parentReportSHA256=sha(parent),
                  retainedCompiledCandidates=16, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  publicPlayableChanged=False, rootDocumentsChanged=False)
    out.mkdir()
    path = out/'report.json'
    path.write_text(json.dumps(report, indent=2)+'\n')
    wanted = sha(path)
    subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)], capture_output=True, check=True)
    assert sha(path) == wanted and not native.census()
    print(json.dumps({k: report[k] for k in ('passed', 'actualNativeMatches', 'actualEarnedTwoWinWindows',
          'continuousPhysicalFields', 'actualNativeHealthWrites', 'actualFaultsRejected', 'allocatedBytes', 'allRAMHostsReleased', 'actualSecretFightAccepted')}))


if __name__ == '__main__':
    main()
