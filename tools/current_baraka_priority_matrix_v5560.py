"""Actual current original priority decisions, both victims and native slots.

Reuse qualified Kano-P1; three physical cold boots, no builds or game edits.
Whole original capture, exact pixel gate and independently inventoried priority
gate retained; adapt only actual victim voice selectors in the full fault suite.
"""
import concurrent.futures, datetime, inspect, json, re, subprocess, traceback
from pathlib import Path
from PIL import Image
import qualify_current_baraka_priority_v5558 as qualified

prior = qualified.prior
capture = prior.capture
ROOT, need, sha = prior.ROOT, prior.need, prior.sha
PARENT = qualified.OUT / 'progress.json'
BASE = ROOT / 'audit_v5561_current_baraka_priority_matrix_ram'
OUT = ROOT / 'audit_v5562_current_baraka_priority_matrix_progress'
COMPLETED = []
capture.capture.__globals__.update(BASE=BASE, LUA=prior.LUA, COMPLETED=COMPLETED)

source = inspect.getsource(qualified.faults)
edits = {
    'def faults(log, guest):': 'def faults(log, guest, fighter, side):',
    "    call = next(s for s in lines if s.startswith('MK2_BPRIO_CALL ') and 'command=00000045 ' in s)":
    "    voice = '00000048' if fighter == 'sonya' else ('00000045' if side == 1 else '00000046')\n"
    "    call = next(s for s in lines if s.startswith('MK2_BPRIO_CALL ') and 'command=' + voice + ' ' in s)",
    "    busy = next(s for s in lines if s.startswith('MK2_BPRIO_CALL ') and 'command=0000001F ' in s\n"
    "                and 'priority0=0060 priority1=0050 priority2=0050 ' in s)":
    "    blocked = next(r['actualCall'] for r in gate(log, guest)['calls']\n"
    "                   if r['expectedOriginalDecision']['kind'] == 'all native slots higher priority'\n"
    "                   and r['actualCall']['command'] == '0000001F')\n"
    "    busy = next(s for s in lines if s.startswith('MK2_BPRIO_CALL ')\n"
    "                and 'serial=' + blocked['serial'] + ' ' in s)",
    "    owner_end = next(s for s in lines if s.startswith('MK2_BPRIO_END ') and 'serial=2 ' in s)":
    "    voice_serial = re.search(r' serial=(\\d+) ', call).group(1)\n"
    "    owner_end = next(s for s in lines if s.startswith('MK2_BPRIO_END ') and 'serial=' + voice_serial + ' ' in s)",
    "    change('actual command header corrupted', call, 'header', '6039')":
    "    header = int(re.search(r' header=([0-9A-F]+) ', call).group(1), 16)\n"
    "    change('actual command header corrupted', call, 'header', f'{header ^ 1:04X}')",
}
for before, after in edits.items():
    need(source.count(before) == 1, 'Only actual voice/blocked-call selectors adapted, entire original fault suite retained')
    source = source.replace(before, after, 1)
scope = dict(qualified.__dict__, gate=qualified.gate)
exec(compile(source, __file__ + '.entire5558_actual_priority_faults_true_victim_slot_selectors', 'exec'), scope)
faults = scope['faults']


def case(spec, guest, payload, gfx, reference, pins, image):
    fighter, side = spec
    record = capture.capture(spec, guest, payload, gfx, reference, pins, image, True)
    meta, log, folder = record['final'], record['log'], record['folder']
    priority = qualified.gate(log, guest)
    rejected = faults(log, guest, fighter, side)
    need(len(rejected) == 22, 'All actual original priority/inventory/owner/branch faults retained')
    coverage = prior.phase.coverage(log, meta)
    routes = prior.routes.gate(log, guest, fighter, side)
    old_path = ROOT / 'audit_v5547_current_baraka_audio_matrix_ram' / f'{fighter}_p{side}_samples/result.json'
    old = json.loads(old_path.read_text())
    need(meta['actualDisplayHeaders'] == old['actualDisplayHeaders']
         and meta['actualMixedPCMSHA256'] == old['actualMixedPCMSHA256']
         and meta['actualPCMUpdates'] == old['actualPCMUpdates'] and meta['actualPCMBytes'] == old['actualPCMBytes'],
         'Every actual whole display and native joined PCM unchanged by additional passive priority snapshots')
    need(meta['passed'] and meta['process']['exit_code'] == 0
         and meta['process']['player'] == fighter and meta['process']['victim_slot'] == side
         and meta['actualNativeHeadBodyPixelsAndScanout']['passed']
         and meta['actualNativeHeadBodyPixelsAndScanout']['everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact']
         and len(meta['actualNativeHeadBodyPixelsAndScanout']['parts']) == 14
         and len(meta['effectiveActualNativeRecordFaults']) == 15,
         'Whole original current physical and exact14 native owned head/body scanout gates passed in the actual context')
    result = dict(passed=True, fighter=fighter, side=side, nativeResult=str(folder / 'result.json'),
        nativePID=meta['process']['nativePID'], nativeExit=0, priority=priority,
        effectiveActualPriorityFaults=rejected, audioTimerCoverage=coverage, sourceVoiceEffectRoutes=routes,
        priorUnperturbedNativeResult=str(old_path), wholeDisplayedFrames=125,
        exactOwnedPhaseScanoutPixels=1422400, entireOriginalPhysicalAndPixelGatesRetained=True,
        fullPortAcceptance=False)
    capture.save(BASE / f'{fighter}_p{side}_qualified.json', result)
    print(f'{fighter} P{side} actual native priority/complete inventory/22faults and original physical/raster/audio gates passed', flush=True)
    return result


def run():
    guest = capture.original.model.current.expected()
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active'
         and len(parent['effectiveActualPriorityRecordFaults']) == 22,
         'Qualified actual current Kano-P1 priority and complete remaining scope retained')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT, Path(__file__), Path(qualified.__file__), Path(prior.__file__), prior.LUA):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'All authoritative current/public/source/retained evidence stable before native runs')
    payload = (ROOT / capture.original.model.current.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference, gfx = capture.original.model.source_art(guest, payload, pins)
    image = capture.original.transport.source_graphics(payload, pins)
    cases, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        jobs = {pool.submit(case, spec, guest, payload, gfx, reference, pins, image): spec
                for spec in [('kano', 2), ('sonya', 1), ('sonya', 2)]}
        for future in concurrent.futures.as_completed(jobs):
            try:
                cases.append(future.result())
            except Exception as error:
                errors.append(dict(context=jobs[future], error=repr(error), traceback=''.join(traceback.format_exception(error))))
    need(not errors, 'Actual priority matrix errors: ' + json.dumps(errors))
    cases.sort(key=lambda c: (c['fighter'], c['side']))
    pngs, compacted = [], []
    for p in sorted(BASE.rglob('*')):
        if not p.is_file():
            continue
        need(p.suffix.lower() not in ('.bin', '.wav', '.rgb', '.pcm'), 'No requested raw guest/audio/raster buffers persisted')
        if p.suffix.lower() == '.png':
            with Image.open(p) as im:
                need(p.name == '0000.png' and p.parent.name == 'mk2ks' and p.parent.parent.name == 'snap'
                     and im.size == (400, 254), 'Only actual native automatic timed-exit PNGs')
            pngs.append(dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p)))
        if p.suffix.lower() in ('.log', '.json', '.cfg', '.txt'):
            before = sha(p)
            cp = subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/I', '/Q', str(p)], capture_output=True)
            need(cp.returncode == 0 and sha(p) == before, 'Retained terminal text losslessly compacted')
            compacted.append(str(p))
        pins[str(p.resolve())] = sha(p)
    need(len(cases) == len(pngs) == len(COMPLETED) == 3
         and all(sha(p) == h for p, h in pins.items()), 'Three actual completed captures/PNG records and unchanged pinned inputs')
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
        remaining=parent['remaining'], parentAdditiveJournal=str(PARENT),
        previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual original dispatcher priority snapshots both true victims/both native slots; reuse qualified Kano-P1 and three new complete physical/exact art/PCM captures with all native dispatcher and queue records independently inventoried;66new actual priority faults rejected, original raster and joined audio unchanged, timed PNGs accounted and retained logs compacted',
        retainedKanoP1Evidence=str(PARENT), cases=cases, newNativeBoots=3, reusedPriorQualifiedNativeBoots=1,
        effectiveNewActualPriorityRecordFaults=66, effectiveAllFourContextActualPriorityRecordFaults=88,
        normalBothVictimsAndSlotsObservedOriginalDispatcherDecisionsAccepted=True,
        persistentNewNativeAutomaticExitPNGs=pngs, persistentNewNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs),
        terminalTextFilesLosslesslyCompacted=len(compacted), newBuilds=0, newDeletedFiles=0,
        publicPlayableChanged=False, refreshedReleaseZIP=False, requestedRawGuestGFXVRAMRGBPCMFilesWritten=0,
        allNativeQueueSuppressionCausesAccepted=False, sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False, fullPortAcceptance=False, newInputHashes=pins,
        nextAction='Independently bind native direct/complex dispatch and full original DCS waveform; retain all four-context physical/art/audio/priority evidence while continuing every remaining original requirement group.')


if __name__ == '__main__':
    need(not OUT.exists() and not BASE.exists(), 'Fresh immutable actual native priority matrix')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), completedNativeCaptures=COMPLETED,
                      goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir()
    capture.save(OUT / 'progress.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('remaining', 'newInputHashes', 'cases', 'completedNativeCaptures')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
