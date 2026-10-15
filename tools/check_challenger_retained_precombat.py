"""Actual both-slot source-state faults on the same completed RAM carrier."""
import json
from pathlib import Path
import qualify_challenger_retained_precombat as model
import qualify_challenger_retained_precombat_v2 as adapter
from check_launch_ko_round_faults import change
ROOT, need, sha = model.ROOT, model.need, model.sha


def continuous(c):
    first = int(model.original.prior.one(c['text'], 'MK2_MAUDIO_BEGIN')['frame'])
    last = int(model.original.prior.one(c['text'], 'MK2_JR_RESULT')['frame'])
    for tag, key, ids in (('MK2_INTERRUPT_OWNER', 'slot', (1, 2)), ('MK2_INTERRUPT_CHANNEL', 'channel', (10, 11, 12, 13))):
        records = model.rows(c['text'], tag)
        need(len(records) == (last-first+1)*len(ids) and {(int(r['frame']), int(r[key])) for r in records} == {(f, i) for f in range(first, last+1) for i in ids}, 'Every exact native field and physical channel, no relabelled gap')
    return True


def check(c):
    out = ROOT/'audit_challenger_retained_precombat_faults'; need(not out.exists(), 'Fresh actual same-run fault proof')
    path = ROOT/'audit_challenger_retained_precombat_checked/report.json'; proof = json.loads(path.read_text())
    need(proof['passed'] and proof['nativeTerminal'] == c['terminal'], 'Actual exact completed interval proof')
    scoped, admission = model.interval(c)
    physical, by = model.health.physical_inventory(scoped); pins = dict(proof['inputHashes'])
    events = model.source_events(scoped, pins, by); owned = model.owners(scoped, events, by); continuous(scoped)
    rejected = []
    def reject(label, fn):
        try: fn()
        except (ValueError, KeyError, StopIteration) as error: rejected.append(dict(kind=label, rejectedBy=str(error)))
        else: raise ValueError('Actual false evidence admitted: '+label)
    for slot, frame in ((1, 1494), (2, 2298)):
        for key, value in (('actor', '01000000'), ('main', '01000000'), ('id', '1'), ('health', '160')):
            bad = change(scoped['text'], 'MK2_INTERRUPT_OWNER', lambda r: r['frame']==str(frame) and r['slot']==str(slot), key, value)
            reject('actual active slot'+str(slot)+' '+key, lambda t=bad: model.owners(dict(scoped, text=t), events, by))
    for slot, frame in ((1, 1570), (2, 2302)):
        bad = change(scoped['text'], 'MK2_INTERRUPT_OWNER', lambda r: r['frame']==str(frame) and r['slot']==str(slot), 'actor', '01000000')
        reject('actual stale retired slot'+str(slot), lambda t=bad: model.owners(dict(scoped, text=t), events, by))
    for channel, frame in ((10, 1570), (11, 1570), (12, 2302)):
        row = next(r for r in model.rows(scoped['text'], 'MK2_INTERRUPT_CHANNEL') if r['frame']==str(frame) and r['channel']==str(channel))
        bad = change(scoped['text'], 'MK2_INTERRUPT_CHANNEL', lambda r: r==row, 'position', str(float(row['position'])-1))
        reject('actual frozen source position channel'+str(channel), lambda t=bad: model.owners(dict(scoped, text=t), events, by))
    bad = change(scoped['text'], 'MK2_MAUDIO_SOUND', lambda r: r['word']=='6B01', 'word', '6B00')
    reject('missing actual CPU Bicycle launch marker', lambda: model.source_events(dict(scoped, text=bad), {}, by))
    for tag, key in (('MK2_INTERRUPT_OWNER', 'slot'), ('MK2_INTERRUPT_CHANNEL', 'channel')):
        row = model.rows(scoped['text'], tag)[0]
        bad = change(scoped['text'], tag, lambda r: r==row, 'frame', '1')
        reject('relabelled native field '+tag, lambda t=bad: continuous(dict(scoped, text=t)))
    need(model.owners(scoped, events, by) == owned and model.health.physical_inventory(scoped)[0] == physical and continuous(scoped), 'Complete positives restored after all actual faults')
    for p in (Path(__file__), Path(model.__file__), Path(adapter.__file__), ROOT/'tools/check_launch_ko_round_faults.py', path): pins[str(p)] = sha(p)
    need(all(sha(p) == h for p, h in pins.items()), 'All executed source and original evidence pins unchanged')
    report = dict(passed=True, nativeTerminal=c['terminal'], actualFaultsRejected=rejected, completePhysicalFields=physical['continuousPhysicalFields'], continuousBattleChannels=owned['continuousChannelFields'], inputHashes=pins, newNativeBoots=0, newBuilds=0, fullPortAcceptance=False)
    out.mkdir(); (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(passed=True, actualFaultsRejected=len(rejected))), flush=True)
    return report
