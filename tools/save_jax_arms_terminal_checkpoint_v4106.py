"""Close the exact pending qualifier without losing full scope or cleanup history."""
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'audit_v4103_jax_arms_scene_state_stock_live_fifo_full_scope_checkpoint/checkpoint.json'
REPORT = ROOT / 'audit_v4087_jax_arms_native_fifo_checked/report.json'
OUT = ROOT / 'audit_v4107_jax_arms_terminal_full_scope_checkpoint'


def need(value, message):
    if not value:
        raise AssertionError(message)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest().upper()


def main():
    need(not OUT.exists(), 'Fresh immutable checkpoint output')
    state = json.loads(PARENT.read_text())
    remaining = list(state['remaining'])
    need(state['goalStatus'] == 'active' and len(remaining) == 5 and
         not state['fullPortAcceptance'] and not state['finishedRelease'],
         'Original full objective stays active')
    pending = state['pendingJaxArmsQualification']
    need(pending['execSession'] == 1558 and pending['pid'] == 137548 and
         pending['result'] == str(REPORT) and not pending['completed'],
         'Close only the exact saved pending qualifier')
    pins = {}

    def pin(path, expected=None):
        path = Path(path).resolve()
        key, digest = str(path), sha(path)
        need(expected is None or digest == expected, 'Immutable evidence unchanged: ' + key)
        need(key not in pins or pins[key] == digest, 'Consistent shared pin: ' + key)
        need(key not in state['inputHashes'] or state['inputHashes'][key] == digest,
             'Inherited shared evidence unchanged: ' + key)
        pins[key] = digest

    # Recheck all fresh live parent pins. Its recursive ancestry and exclusions remain inherited.
    for path, digest in state['inputHashes'].items():
        pin(path, digest)
    pin(PARENT)
    fifo = json.loads(REPORT.read_text())
    need(fifo['passed'] and fifo['actualContexts'] == 4 and
         fifo['actualRowFaultsRejected'] == 60 and
         not fifo['allArenaFloorShadowsAccepted'] and not fifo['fullPortAcceptance'],
         'Actual terminal four-context/60-fault bounded proof')
    pin(REPORT)
    for path, digest in fifo['inputHashes'].items():
        pin(path, digest)
    need({(c['fighter'], c['side']) for c in fifo['cases']} ==
         {('kano', 1), ('kano', 2), ('sonya', 1), ('sonya', 2)}, 'Every intended context')
    projections = sum(c['nativeFIFO']['sourceBoundProjections'] for c in fifo['cases'])
    floors = sum(c['nativeFIFO']['floorShadowCopyCommands'] for c in fifo['cases'])
    shadows = sum(c['nativeFIFO']['actualOwnedCompressedShadowRows']['copies'] for c in fifo['cases'])
    props = sum(c['nativeDetachedProps']['originalPropDMAs'] for c in fifo['cases'])
    need((projections, floors, shadows, props) == (13000, 43549, 2429, 3912),
         'Actual terminal report counts, not assumed preflight counts')
    for case in fifo['cases']:
        prop = case['nativeDetachedProps']
        need(prop['sourceBoundPropFIFO'] == 978 and prop['originalPropDMAs'] == 978 and
             prop['nativeFourFieldCadenceAccepted'] and
             not prop['separatePropWorldCameraProjectionAccepted'],
             'Actual prop source/cadence/DMA proof; no unlogged world-transform claim')
    q = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
                        'Get-CimInstance Win32_Process -Filter "ProcessId=137548" | Select-Object -ExpandProperty ProcessId'],
                       capture_output=True, text=True)
    need(q.returncode == 0 and not q.stdout.strip(), 'Exact saved qualifier PID terminal/missing')
    pin(Path(__file__))
    state.update(
        inputHashes=pins,
        inputHashInheritance=dict(schema=1, parentCheckpoint=str(PARENT),
                                  parentCheckpointSHA256=sha(PARENT),
                                  mergeRule='Resolve parent recursively; preserve retired/deleted exclusions and agree on shared pins.'),
        previousCheckpoint=str(PARENT),
        previousGoalTurnClassification=state['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: saved exact pending FIFO qualifier exec1558/PID137548 consumed terminal exit0. Actual4087 passes four own victim/slot contexts and60 faults:13000 physical projections,43549 floor/shadow copy commands,2429 actual own compressed-shadow copies,3912 actual detached-prop draws. All4103 scene/state/stock/failed-proof/storage history retained and fresh hashes rechecked. No additional compression reclamation, deletion, build or playable change.',
        currentDevelopmentNativeJaxArmsFIFOReport=str(REPORT),
        currentDevelopmentNativeJaxArmsQualified=dict(
            ownVictimContexts=4, actualContinuousNativeRGBFields=2432, exactNativeRGBPixels=247091200,
            originalEarnedStateAndPropFaults=52, actualFIFOPropFloorFaults=60,
            sourceBoundPhysicalProjections=projections, actualDetachedPropDraws=props,
            floorShadowCopyCommands=floors, actualOwnCompressedShadowCopies=shadows,
            allTenBodyArmSourcePhasesPresented=True, essentialNativeContactSheets=4,
            all44PanelsNativeBound=True, mainAgentViewedAllFour=True,
            scope='Normal Dead Pool Jax arm-rip, true own17/18 victims in both slots. No independent prop world/camera transform, universal art/position, alternate costume, audio, all-arena, ending or full-port acceptance.'),
        completedJaxArmsQualification=dict(priorPending=pending, completed=True, terminalExitCode=0,
                                            source=str(ROOT / 'tools/verify_jax_arms_native_fifo_v4086.py'),
                                            result=str(REPORT), actualContexts=4, actualFaultsRejected=60),
        pendingJaxArmsQualification=None,
        additionalAllocatedBytesReclaimedAtTerminalCheckpoint=0,
        cleanupAccounting='4101/4105 reclaimed54194176bytes once, inherited from4103; no additional reclaim at this checkpoint.',
        nextImplementationAction='Continue original arm-rip victim/effect/audio and relevant stock-profile/center/edge/facing comparisons. Normal standing armless victim/held WIN is stock behavior; own placement is not broadly accepted. Preserve all five remaining groups: stage/victim audio and broader native stage branches; complete multi-arena move-phase art/ground/shadows/cleanup; remaining finishers/victims/morphs/secrets/cinematics; natural SonyaP2 full tower/own endings/attract; final combined UI/ladder/names/audio, dependency-aware obsolete-folder cleanup and refreshed ZIP. No controlled-alt guest writes, retired evidence resurrection, repeat identical failing campaign policy, or narrow-proof release promotion.',
        gameSourceAndPlayableBytesChangedThisTurn=False, fullPortAcceptance=False,
        finishedRelease=False, goalStatus='active')
    need(state['remaining'] == remaining and state['currentTurnReclaimedAllocatedBytes'] == 54194176,
         'Full scope and exact single-count cleanup accounting preserved')
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)],
                        capture_output=True).returncode == 0, 'Compress checkpoint directory before writes')
    (OUT / 'checkpoint.json').write_text(json.dumps(state, indent=2) + '\n')
    print(json.dumps(dict(checkpoint=str(OUT / 'checkpoint.json'), freshPins=len(pins),
                          contexts=4, faultsRejected=60, floorCopies=floors, ownShadowCopies=shadows,
                          additionalReclaimedBytes=0, goalStatus='active', fullPortAcceptance=False)), flush=True)


if __name__ == '__main__':
    main()
