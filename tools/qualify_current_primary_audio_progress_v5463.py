"""Qualify the completed current primary-fatality matrix and compact its text.

No new native boots, build, game edit, media dump, deletion or promotion.
Whole five-function host-audio continuity is source evidence, not universal
DCS-waveform or finisher-art acceptance. RAM-only logical palette filenames
inside the original physical model never become filesystem input pins.
"""
import ctypes, datetime, json, subprocess, traceback
from pathlib import Path
import current_primary_audio_ram_v5460 as captured

ROOT, need, sha = captured.ROOT, captured.need, captured.sha
PARENT = ROOT / 'audit_v5462_current_primary_audio_progress/progress.json'
OUT = ROOT / 'audit_v5464_current_primary_audio_qualified_progress'
OLD_REPORT = ROOT / 'audit_v3717_natural_mirror_complete_audio_checked/report.json'
OLD_SOURCE = ROOT / 'diagnostic_v3680_native_sound_packet_guard/input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
CURRENT_SOURCE = ROOT / captured.current.NAME / 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
HEADERS = (
 'void midtunit_state::mk2ks_battle_audio_stop(unsigned slot, const char *reason)',
 'TIMER_CALLBACK_MEMBER(midtunit_state::mk2ks_battle_audio_tick)',
 'uint16_t midtunit_state::midtunit_sound_state_r()',
 'uint16_t midtunit_state::midtunit_sound_r()',
 'void midtunit_state::midtunit_sound_w(offs_t offset, uint16_t data, uint16_t mem_mask)',
)


def source_blocks(text):
    need(all(text.count(header) == 1 for header in HEADERS), 'Exact whole native host-audio function boundaries')
    starts = [text.index(header) for header in HEADERS]
    need(starts == sorted(starts), 'Original contiguous native host-audio function order')
    ends = starts[1:] + [len(text)]
    return [text[first:last] for first, last in zip(starts, ends)]


def source_contract(text, original):
    actual = source_blocks(text)
    need(actual == original, 'Entire stop/tick/status/read/write host-audio functions source-exact against qualified3680')
    return [dict(function=header, utf8Bytes=len(block.encode()), sha256=captured.digest(block.encode()))
            for header, block in zip(HEADERS, actual)]


def run():
    captured.current.expected()
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active' and
         parent['currentBothSlotNaturalPrimaryMirrorsStateAndCompleteImportedAudioAccepted'],
         'Completed actual current both-slot primary-fatality and full imported-audio matrix')
    pins = dict(parent['newInputHashes'])
    pins[str(PARENT)] = sha(PARENT)
    need(all(sha(p) == h for p, h in pins.items()), 'All executed actual filesystem inputs and retained evidence stable')
    old = json.loads(OLD_REPORT.read_text())
    need(old['passed'] and old['inputHashes'].get(str(OLD_SOURCE)) == sha(OLD_SOURCE),
         'Exact previously runtime-qualified native host-audio source pinned to original3717')
    need(pins.get(str(CURRENT_SOURCE)) == sha(CURRENT_SOURCE), 'Actual current compiled native host-audio source bound')
    original = source_blocks(OLD_SOURCE.read_text())
    source = CURRENT_SOURCE.read_text()
    functions = source_contract(source, original)
    faults = []
    mutations = (
      ('wrong second owned stop channel', 'm_mk2ks_voices->stop(11 + slot * 2);', 'm_mk2ks_voices->stop(10 + slot * 2);'),
      ('wrong native actor identity', 'space.read_word(actor + 0x1f0) != 18)', 'space.read_word(actor + 0x1f0) != 17)'),
      ('wrong original DCS status shift', 'return m_dcs->control_r() >> 4;', 'return m_dcs->control_r() >> 5;'),
      ('wrong original DCS data read mask', 'return m_dcs->data_r() & 0xff;', 'return m_dcs->data_r() & 0xfe;'),
      ('wrong original packet-store PC guard', 'm_maincpu->pc() == 0xffa13c90U', 'm_maincpu->pc() == 0xffa13c91U'),
      ('wrong imported name volume', 'm_mk2ks_voices->set_volume(0, 0.30f);', 'm_mk2ks_voices->set_volume(0, 0.31f);'),
      ('wrong original DCS byte write mask', 'm_dcs->data_w(data & 0xff);', 'm_dcs->data_w(data & 0xfe);'),
    )
    for label, before, after in mutations:
        need(source.count(before) == 1 and before != after, 'One effective selected host-source counterexample: ' + label)
        changed = source.replace(before, after)
        need(changed != source, 'Actual source mutation differs')
        try:
            source_contract(changed, original)
        except ValueError as error:
            faults.append(dict(label=label, rejectedBy=str(error), sourceContinuityOnly=True))
        else:
            raise ValueError('Actual host-source counterexample accepted: ' + label)
        need(source_contract(source, original) == functions, 'Same positive whole source restored')

    census = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
      "Get-CimInstance Win32_Process -Filter \"Name = 'mkport_candidate.exe'\" | Select-Object ProcessId,CommandLine | ConvertTo-Json -Compress"],
      capture_output=True, text=True)
    need(census.returncode == 0, 'Actual native process census')
    live = json.loads(census.stdout) if census.stdout.strip() else []
    if isinstance(live, dict):
        live = [live]
    need(not live, 'All actual native writers terminal before scoped text compaction')

    base = captured.BASE.resolve(strict=True)
    need(base.parent == ROOT.resolve() and not captured.BASE.is_symlink(), 'Exact scoped retained native capture root')
    expected = {f'{fighter}_p{side}_{setting}' for fighter in ('kano', 'sonya')
                for side in (1, 2) for setting in ('samples', 'nosamples')}
    need({p.name for p in base.iterdir()} == expected, 'Exactly eight actual current cold-boot contexts')
    contract, contract_sha = captured.original.physical_contract()
    need(parent['newNativeBoots'] == 8 and parent['effectiveOriginalActualStateFaults'] == 40 and
         parent['effectiveActualMixedAudioFaults'] == 16 and len(parent['cases']) == 4,
         'Complete actual matrix and original state/audio counterexample counts')
    cases, runs, files = [], [], []
    for case in parent['cases']:
        fighter, side = case['fighter'], case['side']
        need((fighter, side) in ((f, s) for f in ('kano', 'sonya') for s in (1, 2)), 'Exact native case identity')
        need(case['audio']['passed'] and case['pairedEntireDisplayedFramesByteExact'] and
             len(case['actualOriginalNativeStatePaletteFaults']) == 10 and len(case['actualMixedAudioFaults']) == 4,
             'Whole actual paired physical/display/audio acceptance and effective faults')
        fit = case['audio']['mixedOriginalCueFidelity']
        need(all(.98 < gain < 1.02 for gain in fit['gains']) and fit['residualRMS'] < 2 and
             fit['correlation'] > .9995 and all(abs(n) <= 4 for n in fit['offsetOutputSamples']) and
             fit['rawAudioFilesWritten'] == 0, 'Unchanged original complete mixed-cue tolerances')
        for key, setting in (('actual', 'samples'), ('baseline', 'nosamples')):
            folder = base / f'{fighter}_p{side}_{setting}'
            need(folder.is_dir() and not folder.is_symlink() and folder.resolve().parent == base,
                 'Exact unlinked native capture leaf')
            result = json.loads((folder / 'result.json').read_text())
            process = json.loads((folder / 'process.json').read_text())
            need(result == case[key] and result['passed'] and result['nativeExit'] == 0 and
                 result['nativePID'] == process['pid'] and result['candidate'] == captured.current.NAME and
                 result['samplesEnabled'] == (setting == 'samples') and result['physical']['passed'] and
                 result['physicalContractSHA256'] == contract_sha and result['wholeActualGuestSourceExact'] and
                 result['allGuestPalettesImagesPCMOnlyInRAM'] and result['guestWrites'] == 0 and
                 result['assistance'] == 'none' and not result['cheatsEnabled'], 'Exact current native terminal fixture')
            need(result['inputHashes'] == json.loads((folder / 'input_hashes_before.json').read_text()) and
                 all(pins.get(p) == h for p, h in result['inputHashes'].items()), 'Actual preboot inputs bound to accepted matrix')
            need((folder / 'stderr.log').stat().st_size == 0 and result['physical']['terminalFrame'] >= 5199,
                 'Actual warning-free full-length native terminal')
            runs.append((str(folder), process['pid']))
            for p in folder.rglob('*'):
                need(not p.is_symlink(), 'No linked retained evidence target')
                if p.is_file():
                    need(p.suffix.lower() not in ('.bin', '.png', '.wav', '.rgb'), 'No raw guest/display/audio media persisted')
                    files.append(p)
        cases.append(dict(fighter=fighter, side=side, nativeExit=0, baselineExit=0,
          completeOriginalMixedCueFit=fit, subsequentOwnedLaunchCues=case['audio']['subsequentOwnedLaunchCues'],
          nativeDamage=case['actual']['physical']['nativeDamage'], nativeKOs=case['actual']['physical']['nativeKOs'],
          actualDisplayedFrameCallbacks=case['actual']['actualDisplayedFrameCallbacks'] + case['baseline']['actualDisplayedFrameCallbacks'],
          originalStateFaults=10, actualMixedAudioFaults=4))
    need(len(runs) == len(set(runs)) == 8 and len({(c['fighter'], c['side']) for c in cases}) == 4,
         'Every actual boot and both-character/both-slot pair accounted without PID-only assumptions')

    measure = ctypes.WinDLL('kernel32', use_last_error=True).GetCompressedFileSizeW
    measure.argtypes = (ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulong))
    measure.restype = ctypes.c_ulong
    def allocated(p):
        high = ctypes.c_ulong()
        ctypes.set_last_error(0)
        low = measure(str(p), ctypes.byref(high))
        need(low != 0xffffffff or ctypes.get_last_error() == 0, 'Actual NTFS file allocation')
        return (high.value << 32) | low

    files.append(PARENT)
    before_total = sum(allocated(p) for p in files)
    compacted = []
    for p in files:
        if p.suffix.lower() not in ('.json', '.log') or not p.stat().st_size:
            continue
        resolved = p.resolve(strict=True)
        need((resolved.is_relative_to(base) or resolved == PARENT.resolve()) and not p.is_symlink(),
             'Exact terminal text target in retained capture scope')
        before, digest = allocated(p), sha(p)
        cp = subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/I', '/Q', str(resolved)], capture_output=True, text=True)
        need(cp.returncode == 0 and sha(p) == digest, 'Lossless terminal text compression; authoritative bytes unchanged')
        compacted.append(dict(file=str(p), logicalBytes=p.stat().st_size, beforeAllocatedBytes=before,
                              afterAllocatedBytes=allocated(p), sha256=digest))
    after_total = sum(allocated(p) for p in files)
    for p in (Path(__file__).resolve(), OLD_SOURCE, CURRENT_SOURCE, OLD_REPORT, *files):
        if str(p) in pins:
            need(pins[str(p)] == sha(p), 'Original filesystem pin stable after scoped compression')
        pins[str(p)] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'All current/source/public/evidence bytes unchanged')
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
      remaining=parent['remaining'], parentAdditiveJournal=str(PARENT),
      previousGoalTurnClassification=parent['previousGoalTurnClassification'],
      thisGoalTurnClassification=parent['thisGoalTurnClassification'] + '; entire current host-audio functions source-bound to qualified3680; seven effective source-continuity counterexamples; all eight native runs terminal; full retained text losslessly compacted',
      currentBothSlotNaturalPrimaryMirrorsStateAndCompleteImportedAudioAccepted=True,
      cases=cases, wholeSourceExactNativeAudioFunctions=functions, effectiveHostSourceContinuityFaults=faults,
      effectiveOriginalActualStateFaults=40, effectiveActualMixedAudioFaults=16,
      actualPairedDisplayedFrameCallbacks=parent['actualPairedDisplayedFrameCallbacks'], retainedActualNativeBoots=8,
      retainedEvidenceLogicalBytes=sum(p.stat().st_size for p in files), retainedEvidenceAllocatedBytes=after_total,
      additionalAllocatedBytesReclaimed=before_total-after_total, terminalTextCompaction=compacted,
      nativeProcessCensus=live, noNativeProcessStillLive=True, newNativeBoots=0, newBuilds=0, newDeletedFiles=0,
      rawGuestRGBPCMOrWAVFilesWritten=0, publicPlayableChanged=False, refreshedReleaseZIP=False,
      sourceContinuityIsNotUniversalRuntimeAcceptance=True, allFinisherContextsAccepted=False,
      allArenasAccepted=False, allNativeDCSWaveformsAccepted=False, fullPortAcceptance=False,
      newInputHashes=pins, nextAction=parent['nextAction'])


if __name__ == '__main__':
    need(not OUT.exists(), 'Fresh immutable completed primary-audio qualification checkpoint')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir()
    captured.save(OUT / 'progress.json', report)
    print(json.dumps({k:v for k,v in report.items() if k not in
                     ('cases', 'newInputHashes', 'remaining', 'terminalTextCompaction')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
