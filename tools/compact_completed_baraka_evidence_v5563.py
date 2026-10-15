"""Force LZX on sealed, already-compressed native evidence; never delete it.

compact skips compressed files without /F. Measure actual allocated bytes via
Windows, bind every target to passed terminal evidence and immutable hashes,
retain all media/sources/configs and the complete original remaining scope.
"""
import ctypes, datetime, json, subprocess, traceback
from pathlib import Path
import current_baraka_priority_capture_v5555 as prior

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
PARENT = ROOT / 'audit_v5562_current_baraka_priority_matrix_progress/progress.json'
OUT = ROOT / 'audit_v5564_current_baraka_priority_storage_progress'
kernel = ctypes.WinDLL('kernel32', use_last_error=True)
kernel.GetCompressedFileSizeW.argtypes = (ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32))
kernel.GetCompressedFileSizeW.restype = ctypes.c_uint32


def allocated(path):
    high = ctypes.c_uint32()
    ctypes.set_last_error(0)
    low = kernel.GetCompressedFileSizeW(str(path), ctypes.byref(high))
    need(low != 0xffffffff or ctypes.get_last_error() == 0, 'Actual Windows allocated size available')
    return (high.value << 32) | low


def run():
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active'
         and parent['normalBothVictimsAndSlotsObservedOriginalDispatcherDecisionsAccepted'],
         'Retain completed four-context native priority proof and full remaining objective')
    pins = dict(parent['newInputHashes'])
    pins[str(PARENT)] = sha(PARENT)
    pins[str(Path(__file__).resolve())] = sha(__file__)
    need(all(sha(p) == h for p, h in pins.items()), 'Exact current/public/source/evidence bytes before lossless storage operation')
    folders = [ROOT / 'audit_v5556_current_baraka_priority_ram/kano_p1_samples']
    for fighter in ('kano', 'sonya'):
        for side in (1, 2):
            base = ROOT / ('audit_v5538_current_baraka_audio_ram' if (fighter, side) == ('kano', 1)
                           else 'audit_v5547_current_baraka_audio_matrix_ram')
            folders.extend(base / f'{fighter}_p{side}_{suffix}' for suffix in ('samples', 'nosamples'))
    folders.extend(ROOT / 'audit_v5561_current_baraka_priority_matrix_ram' / f'{fighter}_p{side}_samples'
                   for fighter, side in [('kano', 2), ('sonya', 1), ('sonya', 2)])
    targets, records = [], []
    for folder in folders:
        folder = folder.resolve()
        need(folder.is_relative_to(ROOT.resolve()) and folder.is_dir(), 'Explicit completed capture folder remains within workspace')
        meta = json.loads((folder / 'result.json').read_text())
        terminal = json.loads((folder / 'terminal.json').read_text())
        need(meta['passed'] and terminal == meta['process'] and terminal['exit_code'] == 0
             and terminal['candidate'] == prior.capture.original.model.current.NAME
             and terminal['killer'] == 'baraka' and terminal['command'] == 'bbbb_hp'
             and meta['actualNativeHeadBodyPixelsAndScanout']['passed'], 'Only sealed passed original native terminal captures')
        for p in sorted(folder.rglob('*')):
            if p.is_file() and p.suffix.lower() in ('.log', '.json', '.cfg', '.txt'):
                need(p.resolve().is_relative_to(folder) and not p.is_symlink()
                     and str(p.resolve()) in pins and sha(p) == pins[str(p.resolve())],
                     'Each exact non-symlink sealed text target independently pinned to executed capture evidence')
                targets.append(p.resolve())
    need(len(folders) == 12 and len(targets) == len(set(targets)), 'Twelve distinct finished captures; no duplicate compression targets')
    for p in targets:
        before_hash, before_bytes = sha(p), allocated(p)
        cp = subprocess.run(['compact.exe', '/C', '/F', '/EXE:LZX', '/Q', str(p)], capture_output=True)
        after_bytes = allocated(p)
        need(cp.returncode == 0 and sha(p) == before_hash, 'Force compression preserves every evidence/config byte')
        records.append(dict(path=str(p), sha256=before_hash, logicalBytes=p.stat().st_size,
                            allocatedBefore=before_bytes, allocatedAfter=after_bytes,
                            measuredReclaimedBytes=before_bytes-after_bytes,
                            compactOutput=cp.stdout.decode(errors='replace')))
    need(all(sha(p) == h for p, h in pins.items()), 'All current/public/source/physical/visual/audio evidence unchanged after compression')
    recovered = sum(r['measuredReclaimedBytes'] for r in records)
    need(recovered > 0, 'Actual additional allocated disk space recovered, not logical-size or skipped-file claims')
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
        remaining=parent['remaining'], parentAdditiveJournal=str(PARENT),
        previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: completed normal Baraka priority proof both victims/both slots retained; corrected skipped already-compressed-file storage handling with explicit force-LZX on hashed terminal evidence only; actual allocated-byte recovery measured for12finished captures with all hashes unchanged',
        preservedFourContextPriorityEvidence=str(PARENT), actualFilesForceCompacted=len(records), completedNativeCaptureFolders=12,
        measuredAllocatedBytesReclaimed=recovered, perFileMeasurements=records,
        inheritedCompressionSkippedWithoutForce=True,
        priorSingleLogProbeExcludedFromMeasuredRecovery=True,
        newNativeBoots=0, newBuilds=0, newDeletedFiles=0,
        publicPlayableChanged=False, refreshedReleaseZIP=False,
        allNativeQueueSuppressionCausesAccepted=False, sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False, fullPortAcceptance=False, newInputHashes=pins,
        nextAction='Native announcer dispatcher starts at originalFFA12430 with command tableFFA10EE0..FFA11A40, sharing the same priority selector; capture and source-qualify its actual calls rather than guessing unbound queues. Continue original DCS waveform and every remaining original requirement group; use force-LZX for already-compressed sealed evidence.')


if __name__ == '__main__':
    need(not OUT.exists(), 'Fresh immutable measured evidence storage qualification')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir()
    prior.capture.save(OUT / 'progress.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('remaining', 'newInputHashes', 'perFileMeasurements')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
