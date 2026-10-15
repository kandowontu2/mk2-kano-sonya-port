"""Retain exact finite earned-stage evidence; reclaim its RAM and compression."""
import json
import subprocess
from pathlib import Path
import audit_campaign_source_conservation as source
import native_process_census_v6647 as native
from inventory_current_port_storage_v4200 import allocated

ROOT, need, sha = source.ROOT, source.need, source.sha


def main():
    out = ROOT/'audit_launch_stage_advance_progress_storage'
    proofpath = ROOT/'audit_launch_stage_advance_checked_kano_p2/report.json'
    need(not out.exists() and not native.census(), 'Fresh journal and actual native terminal')
    proof = json.loads(proofpath.read_text())
    need(proof['passed'] and proof['nativeTerminal']['nativeExit'] == 0 and
         proof['nativeTerminal']['pid'] == 39428 and not proof['fullPortAcceptance'] and
         proof['completeSourceWaveform']['differentChannelSamples'] == 0,
         'Actual finite native earned advance plus complete source audio is sealed')
    # The preview daemon belongs to the capture collector, not a separate job.
    pid = proof['nativeTerminal']['actualWindowsIdentity']['ParentProcessId']
    handle = native.k.OpenProcess(0x1000, False, pid)
    if handle:
        native.k.CloseHandle(handle)
        raise ValueError('Retained RAM collector has not yet exited')
    need(len(proof['remaining']) == 6 and not proof['allCurrentCampaignStagesAccepted'] and
         not proof['partialLaunchInterruptedAtStageBoundaryAccepted'],
         'Do not turn one clean earned transition into all-stage or live-interruption acceptance')
    pins = dict(proof['inputHashes'])
    pins[str(proofpath)] = sha(proofpath)
    need(all(sha(p) == h for p, h in pins.items()), 'All executed prior/current evidence and original failures remain exact')
    files = {ROOT/'mk2ks_launch_stage_advance.lua', Path(__file__).resolve()}
    files.update((ROOT/'tools').glob('*launch_stage_advance*.py'))
    files.update(p for name in ('audit_launch_stage_advance_ball_p2_delay1', 'audit_launch_stage_advance_checked_kano_p2')
                 for p in (ROOT/name).rglob('*') if p.is_file())
    storage, seen, total = [], set(), 0
    for path in sorted(files):
        need(path.resolve().is_relative_to(ROOT) and not path.is_symlink() and
             path.suffix.lower() not in ('.exe', '.zip', '.wav', '.png', '.bin', '.mdata'),
             'Only exact bounded source/compressed-log/proof/configuration leaves')
        digest, before = sha(path), allocated(path)
        subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/F', '/I', '/Q', str(path)], capture_output=True, check=True)
        need(sha(path) == digest, 'Exact lossless retained evidence bytes')
        stat, amount = path.stat(), allocated(path)
        key = stat.st_dev, stat.st_ino
        if key not in seen:
            seen.add(key)
            total += amount
        pins[str(path.resolve())] = digest
        storage.append(dict(path=str(path.resolve()), sha256=digest, beforeAllocatedBytes=before, allocatedBytes=amount))
    need(all(sha(p) == h for p, h in pins.items()) and not native.census() and
         len([p for p in ROOT.iterdir() if p.is_dir() and (p/'mkport_candidate.exe').is_file()]) == 16,
         'All final source/proof pins intact; existing compiled folders unchanged')
    faults = sum(len(proof[key]['actualFaultsRejected']) for key in
                 ('actualSemanticFaults', 'actualSourceChannelFaults', 'actualSourceOwnershipFaults'))
    faults += len(proof['completeSourceWaveform']['actualWaveformFaultsRejected'])+len(proof['sourceDAC']['faults'])+len(proof['wholeSoundROM']['faults'])
    need(faults == 66, 'Complete actually executed counterexample inventory')
    report = dict(passed=True, candidate=proof['candidate'], nativePID=39428, nativeExit=0,
                  earnedNextLadderIndex=1, nextNativeOpponent=7, nextArenaId=2,
                  continuousPhysicalFields=13086, completeBattleChannelFields=26172,
                  completeSourceCallbackFields=83706, comparedStereoFrames=5739840,
                  differentChannelSamples=0, actualFaultsRejected=faults, actualViewedNativeFrames=3,
                  originalCheckerFailuresPreserved=3, allRAMHostsReleased=True,
                  wholeCurrentCampaignAcceptance=False, partialLaunchInterruptedAtStageBoundaryAcceptance=False,
                  fullPortAcceptance=False, goalStatus='active', remaining=proof['remaining'],
                  nextAction=proof['nextAction'], previousGoalTurnClassification=proof['previousGoalTurnClassification'],
                  thisGoalTurnClassification=proof['thisGoalTurnClassification'],
                  selectedFileCount=len(files), uniqueSelectedAllocatedBytes=total,
                  retainedCompiledCandidates=16, publicPlayableChanged=False, rootDocumentsChanged=False,
                  newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0,
                  inputHashes=pins, exactCompressedTargets=storage)
    out.mkdir()
    source.seal(out/'report.json', report)
    print(json.dumps({k: report[k] for k in ('passed', 'earnedNextLadderIndex', 'comparedStereoFrames',
                                           'actualFaultsRejected', 'selectedFileCount', 'uniqueSelectedAllocatedBytes', 'allRAMHostsReleased')}), flush=True)


if __name__ == '__main__':
    main()
