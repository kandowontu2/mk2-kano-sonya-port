"""Observe original announcer dispatcher without replacing old priority gates.

One true native Kano-P1 Baraka run; independently bound original announcer
table/slot/packet/port/ADSP, whole physical/raster/PCM checks and real faults.
Full waveform, direct packet programs and other contexts remain pending.
"""
import collections, datetime, inspect, json, re, struct, subprocess, traceback
from pathlib import Path
from PIL import Image
import qualify_current_baraka_priority_v5558 as qualified

prior = qualified.prior
capture = prior.capture
ROOT, need, sha = prior.ROOT, prior.need, prior.sha
PARENT = ROOT / 'audit_v5564_current_baraka_priority_storage_progress/progress.json'
BASE = ROOT / 'audit_v5567_current_baraka_announcer_ram'
OUT = ROOT / 'audit_v5568_current_baraka_announcer_progress'
LUA = ROOT / 'mk2ks_current_baraka_announcer_ram_v5565.lua'
COMPLETED = []
capture.capture.__globals__.update(BASE=BASE, LUA=LUA, COMPLETED=COMPLETED)


def rows(log, tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)', s)) for s in log.splitlines() if s.startswith('MK2_APRIO_' + tag + ' ')]


source = inspect.getsource(prior.decision)
edits = {
    "    code=int(call['command'],16);table=(0xffa0ef20+((code<<5)&0xffffffff))&0xffffffff":
    "    first,limit=(0xffa10ee0,0xffa11a40)if call['entry']=='FFA12430'else(0xffa0ef20,0xffa10ee0)\n"
    "    code=int(call['command'],16);table=(first+((code<<5)&0xffffffff))&0xffffffff",
    "need(call['entry']=='FFA12530'and": "need(call['entry']in('FFA12530','FFA12430')and",
    'if table>=0xffa10ee0:': 'if table>=limit:',
    "need(table>=0xffa0ef20,": "need(table>=first,",
}
for before, after in edits.items():
    need(source.count(before) == 1, 'Entire original priority predictor; only actual dispatcher/table base and limit extended')
    source = source.replace(before, after, 1)
scope = dict(prior.__dict__)
exec(compile(source, __file__ + '.whole5555_native_priority_predictor_original_announcer_table', 'exec'), scope)
decision = scope['decision']
source = inspect.getsource(prior.gate)
before = 'for first,last in((0xffa0ef20,0xffa10ee0),(0xffa12530,0xffa12bd0)):'
need(source.count(before) == 1, 'Whole original command table/dispatcher code equality expanded, never weakened')
source = source.replace(before, 'for first,last in((0xffa0ef20,0xffa11a40),(0xffa12430,0xffa12bd0)):', 1)
scope = dict(prior.__dict__, rows=rows, decision=decision)
exec(compile(source, __file__ + '.whole5555_all_observed_native_announcer_and_fighter_decisions', 'exec'), scope)
whole_priority_gate = scope['gate']


def gate(log, guest):
    old = qualified.gate(log, guest)
    positive = whole_priority_gate(log, guest)
    calls = rows(log, 'CALL')
    fighters = [c for c in calls if c['entry'] == 'FFA12530']
    announcers = [c for c in calls if c['entry'] == 'FFA12430']
    routes = [dict(re.findall(r'(\w+)=([^\s]+)', s)) for s in log.splitlines() if s.startswith('MK2_AROUTE_CALL ')]
    keys = ('frame', 'seconds', 'entry', 'a0', 'a1', 'a8', 'a13')
    tuples = lambda rs: [tuple(r[k] for k in keys) for r in rs]
    need(tuples(fighters) == tuples(prior.rows(log, 'CALL')),
         'Every original fighter call cross-bound to the unchanged independent BPRIO observer')
    need(tuples(announcers) == tuples(routes) and len(announcers) >= 7
         and all(c['caller'] == r['return_pc'] for c, r in zip(announcers, routes)),
         'Every actual announcer call independently route-inventoried, caller exact')
    ar_end = [dict(re.findall(r'(\w+)=([^\s]+)', s)) for s in log.splitlines() if s.startswith('MK2_AROUTE_RESULT ')]
    need(len(ar_end) == 1 and ar_end[0]['frame'] == '5198' and ar_end[0]['calls'] == str(len(announcers)),
         'Independent announcer route count retires at real native terminal')
    keys = ('frame', 'seconds', 'entry', 'a1', 'a3', 'a4', 'a8', 'a13')
    queues = rows(log, 'QUEUE')
    need(not rows(log, 'UNBOUND_QUEUE') and tuples(queues) == tuples(capture.rows(log, 'QUEUE')),
         'Every original native priority queue now bound to exactly one actual dispatcher, none guessed or dropped')
    need(all(r.get('writes') == '0' and r.get('assistance') == 'none'
             for tag in ('CALL', 'QUEUE', 'END', 'RESULT') for r in rows(log, tag))
         and all(r.get('writes') == '0' and r.get('assistance') == 'none' for r in routes + ar_end),
         'All additional original dispatcher observations passive and unassisted')
    stock = (ROOT / 'mk2/mk2-maincpu.bin').read_bytes()
    packets, writes, delivery = (capture.rows(log, tag) for tag in ('PACKET', 'SOUND', 'DELIVERY'))
    accepted = []
    for item in positive['calls']:
        call, end, expected = item['actualCall'], item['actualCompletion'], item['expectedOriginalDecision']
        need(call['frame'] == end['frame'] and float(call['seconds']) < float(end['seconds']),
             'Actual original call completes later in its own native field')
        if call['entry'] == 'FFA12430':
            for name in ('a8', 'caller'):
                address = int(call[name], 16)
                need(0xff800000 <= address <= 0xfffffe00
                     and guest[prior.off(address):prior.off(address)+16] == stock[prior.off(address):prior.off(address)+16],
                     'Actual native announcer script/caller remains original source bytes')
        serial_queues = [q for q in queues if q['serial'] == call['serial']]
        if expected['slot'] is None:
            continue
        need(len(serial_queues) == 1, 'One actual queue descendant per selected call')
        queue = serial_queues[0]
        need(float(call['seconds']) < float(queue['seconds']) < float(end['seconds']),
             'Actual queue occurs after entry and before native completion')
        matched = [p for p in packets if float(queue['seconds']) < float(p['seconds']) < float(end['seconds'])
                   and all(p[k] == call[k] for k in ('frame', 'a8', 'a13'))]
        need(len(matched) == 1 and int(matched[0]['a3'], 16) == expected['packet'],
             'Actual dispatcher-selected original table base plus slot reaches exact native packet')
        packet = matched[0]
        ports = [w for w in writes if float(packet['seconds']) < float(w['seconds']) < float(end['seconds'])
                 and all(w[k] == call[k] for k in ('frame', 'a8', 'a13'))]
        need(len(ports) == 2 and [w['pc'] for w in ports] == ['FFA13C90', 'FFA13D60']
             and all(w['mask'] == 'FFFF' for w in ports)
             and [int(w['word'], 16) & 255 for w in ports] == [expected['packet'] >> 8, expected['packet'] & 255],
             'Original exact packet high/low bytes, writers and masks reach native DCS port')
        dsps = []
        for w in ports:
            index = writes.index(w)
            deadline = float(writes[index+1]['seconds']) if index+1 < len(writes) else float(w['seconds']) + .1
            hits = [d for d in delivery if float(w['seconds']) <= float(d['seconds']) < deadline
                    and int(d['word'], 16) == int(w['word'], 16) & 255]
            need(hits, 'Every actual selected dispatcher byte consumed by ADSP before the next native port write')
            dsps.append(hits[0])
        accepted.append(dict(call=call, nativeDecision=expected, queue=queue, packet=packet, ports=ports, dspReads=dsps))
    need(len(accepted) == len(queues), 'All original priority queues delivered; no surviving unqualified queue')
    ann = [a for a in accepted if a['call']['entry'] == 'FFA12430']
    keys = ('frame', 'seconds', 'entry', 'a1', 'a3', 'a4', 'a8', 'a13')
    need(tuples([a['queue'] for a in ann]) == tuples(prior.rows(log, 'UNBOUND_QUEUE')),
         'All previously unbound native queues are precisely the actual announcer descendants, not inferred from sound')
    return dict(passed=True, actualCalls=len(calls), actualAnnouncerCalls=len(announcers), actualFighterCalls=len(fighters),
        actualDeliveredPriorityQueues=len(queues), actualAnnouncerDeliveredQueues=len(ann), delivered=accepted,
        allObservedPriorityQueuesBoundToSourceDispatcher=True, originalFighterPriorityGate=old,
        completeObservedDualDispatcherPriority=positive,
        directPacketProgramsOutsidePriorityPath=len(packets)-len(accepted),
        fullOriginalWaveformAccepted=False, allVictimSlotsAccepted=False, allComplexDispatchAccepted=False,
        fullPortAcceptance=False)


def faults(log, guest):
    positive = gate(log, guest)
    row = positive['delivered'][next(i for i, r in enumerate(positive['delivered']) if r['call']['entry'] == 'FFA12430')]
    cases = []

    def change(label, tag, record, key, value):
        line = next(s for s in log.splitlines() if s.startswith(tag + ' ') and all(re.search(r'(?<!\w)' + k + '=' + re.escape(v) + r'(?:\s|$)', s) for k, v in record.items()))
        damaged, n = re.subn(r'(?<!\w)' + key + r'=[^\s]+', key + '=' + value, line)
        need(n == 1 and damaged != line and log.count(line) == 1, 'Effective actual announcer record fault')
        cases.append((label, log.replace(line, damaged, 1)))

    c, q = row['call'], row['queue']
    change('wrong announcer source table header', 'MK2_APRIO_CALL', c, 'header', f"{int(c['header'],16)^1:04X}")
    change('wrong announcer source base packet', 'MK2_APRIO_CALL', c, 'base', '0000')
    change('wrong announcer table address', 'MK2_APRIO_CALL', c, 'table', 'FFA0EF20')
    change('announcer mislabeled as fighter dispatch', 'MK2_APRIO_CALL', c, 'entry', 'FFA12530')
    change('wrong independently recorded announcer caller', 'MK2_APRIO_CALL', c, 'caller', '00000000')
    change('false announcer mute snapshot', 'MK2_APRIO_CALL', c, 'mute', '0001')
    change('wrong announcer queue slot', 'MK2_APRIO_QUEUE', q, 'entry', 'FFA12B00')
    change('wrong announcer queue duration', 'MK2_APRIO_QUEUE', q, 'a4', '00000000')
    change('wrong announcer packet word', 'MK2_MAUDIO_PACKET', row['packet'], 'a3', '00000000')
    change('wrong announcer port byte', 'MK2_MAUDIO_SOUND', row['ports'][0], 'word', '0000')
    change('foreign announcer packet task', 'MK2_MAUDIO_PACKET', row['packet'], 'a13', '01000000')
    route = next(s for s in log.splitlines() if s.startswith('MK2_AROUTE_CALL '))
    cases.append(('one actual independent announcer route omitted', log.replace(route+'\n', '', 1)))
    rejected = []
    for label, bad in cases:
        need(bad != log, 'Actual announcer record really mutated')
        try:
            gate(bad, guest)
        except ValueError as error:
            rejected.append(dict(label=label, rejectedBy=str(error)))
        else:
            raise ValueError('Accepted effective actual announcer fault: ' + label)
    need(gate(log, guest) == positive, 'Entire positive original dual-dispatcher gate restored after actual faults')
    return rejected


def run():
    guest = capture.original.model.current.expected()
    parent = json.loads(PARENT.read_text())
    need(parent['passed'] and parent['goalStatus'] == 'active', 'Completed both-victim/slot priority evidence and full remaining scope retained')
    pins = dict(parent['newInputHashes'])
    for p in (PARENT, Path(__file__), LUA, Path(qualified.__file__), Path(prior.__file__)):
        pins[str(p.resolve())] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'All current/public/source/retained evidence unchanged before actual physical boot')
    payload = (ROOT / capture.original.model.current.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes()
    reference, gfx = capture.original.model.source_art(guest, payload, pins)
    image = capture.original.transport.source_graphics(payload, pins)
    record = capture.capture(('kano', 1), guest, payload, gfx, reference, pins, image, True)
    meta, log, folder = record['final'], record['log'], record['folder']
    positive = gate(log, guest)
    rejected = faults(log, guest)
    old_faults = qualified.faults(log, guest)
    coverage = prior.phase.coverage(log, meta)
    voice = prior.routes.gate(log, guest, 'kano', 1)
    old = json.loads((ROOT / 'audit_v5556_current_baraka_priority_ram/kano_p1_samples/result.json').read_text())
    need(meta['actualDisplayHeaders'] == old['actualDisplayHeaders']
         and meta['actualMixedPCMSHA256'] == old['actualMixedPCMSHA256']
         and meta['actualPCMUpdates'] == old['actualPCMUpdates'] and meta['actualPCMBytes'] == old['actualPCMBytes'],
         'Every actual whole display and joined native PCM unchanged by additional passive announcer observers')
    pngs, compacted = [], []
    for p in sorted(folder.rglob('*')):
        if not p.is_file(): continue
        need(p.suffix.lower() not in ('.bin', '.wav', '.rgb', '.pcm'), 'No requested raw guest/media buffers persisted')
        if p.suffix.lower() == '.png':
            with Image.open(p) as im:
                need(p == folder / 'snap/mk2ks/0000.png' and im.size == (400,254), 'Only actual automatic timed-exit PNG')
            pngs.append(dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p)))
        if p.suffix.lower() in ('.log', '.json', '.cfg', '.txt'):
            before = sha(p)
            cp = subprocess.run(['compact.exe','/C','/F','/EXE:LZX','/Q',str(p)], capture_output=True)
            need(cp.returncode == 0 and sha(p) == before, 'Force-LZX really processes already-compressed retained text without changing bytes')
            compacted.append(str(p))
        pins[str(p.resolve())] = sha(p)
    need(len(pngs) == 1 and all(sha(p) == h for p,h in pins.items()), 'One accounted native PNG and exact current/public/source/evidence hashes')
    return dict(passed=True, observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(), goalStatus='active',
        remaining=parent['remaining'], parentAdditiveJournal=str(PARENT), previousGoalTurnClassification=parent['thisGoalTurnClassification'],
        thisGoalTurnClassification='progress: actual original announcer and fighter dispatchers independently observed; all native priority queues source-table/branch/packet/port/ADSP bound, previous unbound queues precisely resolved;12announcer and22original priority faults rejected; entire original physical/raster/source voice/timer and whole RGB/PCM nonperturbance retained',
        actualDualDispatcher=positive, effectiveActualAnnouncerFaults=rejected, retainedOriginalPriorityFaults=old_faults,
        actualTimerCoverage=coverage, actualSourceVoiceEffectRoutes=voice, nativeCaptureResult=str(folder/'result.json'),
        persistentNativeAutomaticExitPNGs=pngs, persistentNativeAutomaticPNGBytes=sum(p['bytes'] for p in pngs),
        terminalTextFilesForceLZXCompacted=len(compacted), newNativeBoots=1, newBuilds=0, newDeletedFiles=0,
        requestedRawGuestGFXVRAMRGBPCMFilesWritten=0, publicPlayableChanged=False, refreshedReleaseZIP=False,
        allNativeQueueSuppressionCausesAccepted=False, sourceQualifiedNativeDCSWaveformAccepted=False,
        completeBarakaFinisherAudioAccepted=False, fullPortAcceptance=False, newInputHashes=pins,
        nextAction='Extend actual announcer proof to both victims/slots; source-qualify direct packet programs and full original DCS waveform, then continue every original remaining requirement group.')


if __name__ == '__main__':
    need(not OUT.exists() and not BASE.exists(), 'Fresh immutable actual announcer capture')
    try:
        report = run()
    except Exception as error:
        report = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), completedNativeCaptures=COMPLETED,
                      goalStatus='active', fullPortAcceptance=False)
    OUT.mkdir()
    capture.save(OUT / 'progress.json', report)
    print(json.dumps({k:v for k,v in report.items() if k not in ('remaining','newInputHashes','actualDualDispatcher',
        'effectiveActualAnnouncerFaults','retainedOriginalPriorityFaults','actualTimerCoverage','actualSourceVoiceEffectRoutes','completedNativeCaptures')}, indent=2), flush=True)
    raise SystemExit(0 if report['passed'] else 1)
