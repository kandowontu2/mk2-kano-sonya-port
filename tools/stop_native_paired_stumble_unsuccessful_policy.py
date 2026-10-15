"""Explicitly retire a losing physical policy, not an observation timeout."""
import hashlib
import json
import subprocess
from pathlib import Path
import inspect_native_paired_stumble_live_prefix as inspect

ROOT, need, sha = inspect.ROOT, inspect.need, inspect.sha


def run():
    path = inspect.capture.OUT / 'explicit_unsuccessful_physical_policy_stop.json'
    need(not path.exists(), 'Preserve this actual policy outcome exactly once')
    text, report = inspect.inspect_prefix()
    need(report['observedLossesByStage']['2'] >= 30 and report['ownNativeWinReadsByStage']['2'] == 0 and
         report['latestNativeField']['stage'] == '2' and
         report['latestNativeField']['human'] == '18:18' and report['latestNativeField']['cpu'] == '7:7' and
         int(report['latestNativeField']['frame']) > 54865 + 50000,
         'Repeated real paid Raiden losses without any own round win, not expired observation')
    actual = next((p for p in inspect.capture.base.census.census() if p['ProcessId'] == inspect.GAME), None)
    need(actual == report['actualNativeIdentity'], 'Same exact observed process still live before explicit stop')
    record = dict(report, passed=False, physicalPolicyUnsuccessful=True,
        stopReason='At least30 collision-earned Raiden losses and zero own round wins; change ordinary test tactics after reviewing the actual repaired handoff.',
        engineDefectNotInferredFromControllerLosses=True, oldExactCorruptingHandoffNowReturnsNormally=True,
        actualObservedPrefixSHA256=hashlib.sha256(text.encode()).hexdigest().upper(),
        actualObservedPrefixBytes=len(text.encode()), nativeCacheFailureObserved=False,
        stoppedSolelyForObservationTimeout=False, exactNativePID=inspect.GAME, exactRAMParent=inspect.PARENT,
        inputHashes={str(Path(__file__).resolve()): sha(__file__), str(Path(inspect.__file__).resolve()): sha(inspect.__file__)},
        fullPortAcceptance=False, goalStatus='active')
    path.write_text(json.dumps(record, indent=2) + '\n')
    result = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
        f'Stop-Process -Id {inspect.GAME} -ErrorAction Stop'], capture_output=True, text=True)
    need(result.returncode == 0 and not result.stderr.strip(), 'Only exact original losing-policy native stopped')
    print(json.dumps(dict(explicitStop=True, exactNativePID=inspect.GAME,
        actualRaidenLosses=report['observedLossesByStage']['2'], nativeCacheStoresObserved=0,
        fullCampaignAccepted=False)), flush=True)


if __name__ == '__main__':
    run()
