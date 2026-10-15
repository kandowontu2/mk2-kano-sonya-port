"""Qualify actual native priority snapshots against the complete older observer.

No new boot, guest edits, builds, or persistent raw buffers. Faults modify
copies of actual sealed records, never the game. Preserve full remaining scope.
"""
import collections, datetime, json, re, subprocess, traceback
from pathlib import Path
from PIL import Image
import current_baraka_priority_capture_v5555 as prior

ROOT, need, sha = prior.ROOT, prior.need, prior.sha
PARENT = prior.OUT / 'progress.json'
FOLDER = prior.BASE / 'kano_p1_samples'
OUT = ROOT / 'audit_v5559_current_baraka_priority_qualified'


def gate(log, guest):
    positive = prior.gate(log, guest)
    calls = prior.rows(log, 'CALL')
    original = [r for r in prior.capture.rows(log, 'ROUTE') if r['entry'] == 'FFA12530']
    keys = ('frame', 'seconds', 'entry', 'a0', 'a1', 'a8', 'a13')
    inventory = lambda rs: [tuple(r[k] for k in keys) for r in rs]
    need(inventory(calls) == inventory(original),
         'Every original dispatcher observation has exactly one identical priority snapshot, in order')
    need(all(c['caller'] == o['return_pc'] for c, o in zip(calls, original)),
         'Every actual dispatcher caller matches the original independently retained route')
    keys = ('frame', 'seconds', 'entry', 'a1', 'a3', 'a4', 'a8', 'a13')
    all_new = [dict(re.findall(r'(\w+)=([^\s]+)', s)) for s in log.splitlines()
               if s.startswith(('MK2_BPRIO_QUEUE ', 'MK2_BPRIO_UNBOUND_QUEUE '))]
    old_queues = prior.capture.rows(log, 'QUEUE')
    need(inventory(all_new) == inventory(old_queues),
         'All native queues, including explicit direct/unbound queues, independently inventoried one to one')
    need(all(r['serial'] == '0' for r in prior.rows(log, 'UNBOUND_QUEUE')),
         'Unbound native direct queues are not fabricated dispatcher descendants')
    need(all(r.get('writes') == '0' and r.get('assistance') == 'none'
             for tag in ('CALL', 'QUEUE', 'UNBOUND_QUEUE', 'END', 'UNBOUND_END', 'RESULT')
             for r in prior.rows(log, tag)), 'Actual passive observer provenance retained')
    ends = prior.rows(log, 'END')
    queues = prior.rows(log, 'QUEUE')
    need(all(q['serial'] in {c['serial'] for c in calls} for q in queues),
         'No orphan priority queues hidden outside the call inventory')
    for c in calls:
        e = next(r for r in ends if r['serial'] == c['serial'])
        need(e['frame'] == c['frame'] and float(c['seconds']) < float(e['seconds']),
             'Actual completion is after its call in the same native field')
        q = [r for r in queues if r['serial'] == c['serial']]
        if q:
            need(float(c['seconds']) < float(q[0]['seconds']) < float(e['seconds']),
                 'Actual queue is between its original dispatcher entry and native completion')
        later = [r for r in calls if r['a13'] == c['a13'] and int(r['serial']) > int(c['serial'])]
        if later:
            need(float(e['seconds']) < float(later[0]['seconds']),
                 'Actual task retires each decision before its next dispatcher call')
    counts = dict(collections.Counter(r['expectedOriginalDecision']['kind'] for r in positive['calls']))
    return dict(positive, completeIndependentDispatcherInventory=len(calls),
                completeIndependentNativeQueueInventory=len(old_queues), actualDecisionKinds=counts,
                nativeQueueChronologyAndTaskRetirementAccepted=True)


def faults(log, guest):
    lines = log.splitlines()
    call = next(s for s in lines if s.startswith('MK2_BPRIO_CALL ') and 'command=00000045 ' in s)
    busy = next(s for s in lines if s.startswith('MK2_BPRIO_CALL ') and 'command=0000001F ' in s
                and 'priority0=0060 priority1=0050 priority2=0050 ' in s)
    queue = next(s for s in lines if s.startswith('MK2_BPRIO_QUEUE '))
    owner_end = next(s for s in lines if s.startswith('MK2_BPRIO_END ') and 'serial=2 ' in s)
    busy_serial = re.search(r' serial=(\d+) ', busy).group(1)
    busy_end = next(s for s in lines if s.startswith('MK2_BPRIO_END ') and f'serial={busy_serial} ' in s)
    terminal = next(s for s in lines if s.startswith('MK2_BPRIO_RESULT '))
    original = next(s for s in lines if s.startswith('MK2_MAUDIO_ROUTE ') and 'entry=FFA12530 ' in s)
    cases = []

    def change(label, line, key, value):
        damaged, count = re.subn(r'(?<!\w)' + key + r'=[^\s]+', key + '=' + value, line)
        need(count == 1 and damaged != line and log.count(line) == 1, 'Effective actual record fault: ' + label)
        cases.append((label, log.replace(line, damaged, 1)))

    change('busy slot falsified as free', busy, 'priority0', '0000')
    change('actual command header corrupted', call, 'header', '6039')
    change('actual command base packet corrupted', call, 'base', '0000')
    change('actual command table arithmetic corrupted', call, 'table', 'FFA0EF20')
    change('actual command register corrupted', call, 'command', '00000044')
    change('wrong original stack caller', call, 'caller', '00000000')
    change('false mute snapshot', call, 'mute', '0001')
    change('wrong native selected queue', queue, 'entry', 'FFA12A80')
    change('wrong selected duration register', queue, 'a4', '00000000')
    change('wrong queue source base', queue, 'a3', '00000000')
    change('wrong selected priority register', queue, 'a1', '00000000')
    change('wrong completion branch for suppressed call', busy_end, 'entry', 'FFA12B90')
    change('foreign completion actor', owner_end, 'a8', '01000000')
    change('foreign completion task', owner_end, 'a13', '01000000')
    change('completion before actual call', owner_end, 'seconds', '0')
    change('actual queue orphaned', queue, 'serial', '999999')
    change('actual terminal pending command', terminal, 'pending', '1')
    change('false passive provenance', call, 'writes', '1')
    for label, line in (('missing actual dispatcher snapshot', call),
                        ('missing actual completion', owner_end),
                        ('missing independently retained dispatcher route', original),
                        ('missing actual selected queue', queue)):
        need(log.count(line) == 1, 'Unique actual omitted record')
        cases.append((label, log.replace(line + '\n', '', 1)))
    accepted = gate(log, guest)
    rejected = []
    for label, bad in cases:
        need(bad != log, 'Actual mutation changes retained records')
        try:
            gate(bad, guest)
        except (ValueError, StopIteration) as error:
            rejected.append(dict(label=label, rejectedBy=str(error)))
        else:
            raise ValueError('Accepted effective actual priority fault: ' + label)
    need(gate(log, guest) == accepted, 'Entire positive priority/inventory gate restored after actual faults')
    return rejected


def run():
    guest = prior.capture.original.model.current.expected()
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active' and parent['newNativeBoots'] == 1,
         'Retain real completed native capture and unchanged full objective')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT, Path(__file__), Path(prior.__file__), prior.LUA):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'Authoritative current/public/source/evidence hashes stable')
    meta = json.loads((FOLDER / 'result.json').read_text())
    terminal = json.loads((FOLDER / 'terminal.json').read_text())
    process = json.loads((FOLDER / 'process.json').read_text())
    log = (FOLDER / 'run.log').read_text()
    need(meta['passed'] and meta['samplesEnabled'] and terminal == meta['process']
         and terminal['exit_code'] == 0 and terminal['nativePID'] == process['pid']
         and terminal['player'] == 'kano' and terminal['victim_slot'] == 1
         and terminal['killer'] == 'baraka' and terminal['command'] == 'bbbb_hp'
         and terminal['entireOriginal921PhysicalControllerRetained'] and terminal['assistance'] == 'none'
         and not terminal['cheats_enabled'] and 'MK2_STOCK_HEAD_V921_RESULT frame=5198' in log
         and 'Average speed:' in log and not (FOLDER / 'stderr.log').read_text(),
         'Real native controller capture finished5198, terminal0 and empty stderr')
    need(terminal['candidate'] == prior.capture.original.model.current.NAME
         and terminal['executable_sha256'] == prior.capture.original.model.current.EXE_SHA
         and terminal['payload_sha256'] == prior.capture.original.model.current.PAYLOAD_SHA,
         'Exact current executable/payload context')
    pins.update(terminal['input_hashes'])
    state, visual = meta['actualNativeContract'], meta['actualNativeHeadBodyPixelsAndScanout']
    need(state['damage'] == 322 and state['nativeWrapAge'] == 174
         and state['headPoses'] == state['bodyPoses'] == list(range(7))
         and state['groundedBodyDMAs'] > 100 and state['hardwarePaletteDumps'] == 14
         and len(meta['effectiveActualNativeRecordFaults']) == 15 and visual['passed']
         and visual['everyEmittedOwnedHeadBodyAndLegitimateForegroundPixelExact']
         and len(visual['parts']) == 14 and visual['wholeNativeScanoutPixels'] == 1422400
         and len(meta['actualDisplayHeaders']) == 125, 'Entire original physical and exact native rendered ownership gates retained')
    positive = gate(log, guest)
    rejected = faults(log, guest)
    coverage = prior.phase.coverage(log, meta)
    routes = prior.routes.gate(log, guest, 'kano', 1)
    need(positive['calls'] == parent['actualPriority']['calls'], 'Actual independently qualified decisions match sealed native observations')
    old = json.loads((ROOT / 'audit_v5538_current_baraka_audio_ram/kano_p1_samples/result.json').read_text())
    need(meta['actualDisplayHeaders'] == old['actualDisplayHeaders']
         and meta['actualMixedPCMSHA256'] == old['actualMixedPCMSHA256']
         and meta['actualPCMUpdates'] == old['actualPCMUpdates'] and meta['actualPCMBytes'] == old['actualPCMBytes'],
         'Every actual whole RGB callback and full joined PCM unchanged by additional passive taps')
    pngs, compacted = [], []
    for p in sorted(FOLDER.rglob('*')):
        if not p.is_file():
            continue
        need(p.suffix.lower() not in ('.bin', '.wav', '.rgb', '.pcm'), 'No requested raw game/media buffers persisted')
        if p.suffix.lower() == '.png':
            with Image.open(p) as im:
                need(p == FOLDER / 'snap/mk2ks/0000.png' and im.size == (400, 254), 'Only actual native timed-exit PNG')
            pngs.append(dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p)))
        if p.suffix.lower() in ('.log', '.json', '.cfg', '.txt'):
            before = sha(p)
            cp = subprocess.run(['compact.exe', '/C', '/EXE:LZX', '/I', '/Q', str(p)], capture_output=True)
            need(cp.returncode == 0 and sha(p) == before, 'Retained native text losslessly compacted')
            compacted.append(str(p))
        pins[str(p.resolve())] = sha(p)
    need(len(pngs) == 1 and pngs == meta['nativeAutomaticTerminalPNGs']
         and all(sha(p) == h for p, h in pins.items()), 'One automatic native PNG accurately accounted; all hashes unchanged')
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
        remaining=parent['remaining'], parentAdditiveJournal=str(PARENT),
        previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: sealed actual native priority decisions independently cross-bound one-to-one to every original dispatcher and queue record;22effective actual snapshot/inventory/owner/branch faults rejected; full physical/raster/source voice/timer gates retained; one native exit PNG accounted and sealed text compacted without another boot',
        actualPriority=positive, effectiveActualPriorityRecordFaults=rejected, actualAudioTimerCoverage=coverage,
        actualSourceVoiceEffectRoutes=routes, actualNativeTerminal=dict(nativePID=process['pid'], nativeExit=0, terminalField=5198),
        persistentNativeAutomaticExitPNGs=pngs, persistentNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs),
        terminalTextFilesLosslesslyCompacted=len(compacted), newNativeBoots=0, reusedAcceptedNativeBoots=1,
        newBuilds=0, newDeletedFiles=0, publicPlayableChanged=False, refreshedReleaseZIP=False,
        requestedRawGuestGFXVRAMRGBPCMFilesWritten=0, allNativeQueueSuppressionCausesAccepted=False,
        sourceQualifiedNativeDCSWaveformAccepted=False, completeBarakaFinisherAudioAccepted=False,
        fullPortAcceptance=False, newInputHashes=pins,
        nextAction='Extend actual priority snapshots to both victims and slots; independently qualify direct/complex native dispatch and original DCS waveform, then continue every remaining stage/move/finisher/CPU/campaign/UI/release requirement.')


if __name__ == '__main__':
    need(not OUT.exists(), 'Fresh immutable actual priority qualification')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir()
    prior.capture.save(OUT / 'progress.json', report)
    print(json.dumps({k: v for k, v in report.items() if k not in ('remaining', 'newInputHashes', 'actualPriority',
        'effectiveActualPriorityRecordFaults', 'actualAudioTimerCoverage', 'actualSourceVoiceEffectRoutes')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
