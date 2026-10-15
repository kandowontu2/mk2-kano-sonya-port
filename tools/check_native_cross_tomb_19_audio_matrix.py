"""Whole original four-case Tomb sound/window/cue fault suite, current19.

Run inside the final terminal capture with the independently initialized guest
still in RAM. Keep every original case, fault and native cue/branch/role gate.
No native boot, source copies, raw media or claim of complete stage artwork.
"""
import hashlib
import gzip
import inspect
import json
import re
import traceback
from pathlib import Path
from types import SimpleNamespace
import prepare_native_cross_tomb_19_audio_manifest_checked as prepared
import qualify_native_cross_tomb_19_audio_voice_context as analysis
import retire_native_cross_tomb_19_audio_ram as retirement

ROOT, need, sha = prepared.ROOT, prepared.need, prepared.sha
OUT = ROOT / 'audit_native_cross_tomb_19_audio_matrix_checked'


def terminal_gate(text):
    records = prepared.original.verification.inventory(text)
    end = records['MK2_MAUDIO_RESULT']
    channels = records.get('MK2_CROSS_TOMB_AUDIO_TERMINAL', [])
    pool = records.get('MK2_CROSS_TOMB_AUDIO_POOL', [])
    need(len(end) == 1 and len(channels) == 19 and
         {int(r['channel']) for r in channels} == set(range(19)) and
         all(r['frame'] == end[0]['frame'] and r['sample'] == '4294967295' and
             r['writes'] == '0' and r['assistance'] == 'none' for r in channels),
         'All19 actual terminal channels complete, unique, idle and passive')
    need(len(pool) == 1 and pool[0]['frame'] == end[0]['frame'] and
         pool[0]['actor'] == pool[0]['main'] == '00000000' and
         pool[0]['slots'] == '0000,0;0000,0;0000,0;0000,0;0000,0' and
         pool[0]['writes'] == '0' and pool[0]['assistance'] == 'none',
         'All five actual priority/remaining slots and native owner references clear')
    return dict(passed=True, terminalFrame=int(end[0]['frame']), channels=19, prioritySlots=5)


def terminal_faults(text):
    positive = terminal_gate(text)
    channel = next(s for s in text.splitlines() if s.startswith('MK2_CROSS_TOMB_AUDIO_TERMINAL ') and 'channel=18 ' in s)
    pool = next(s for s in text.splitlines() if s.startswith('MK2_CROSS_TOMB_AUDIO_POOL '))
    def replace(line, key, value):
        bad, count = re.subn(r'\b' + key + r'=\S+', key + '=' + value, line, count=1)
        need(count == 1 and bad != line, 'Nonvacuous actual terminal mutation')
        return text.replace(line, bad, 1)
    faults = []
    for label, bad in (
        ('added channel18 stale clip', replace(channel, 'sample', '3')),
        ('added channel18 absent', text.replace(channel + '\n', '', 1)),
        ('added channel18 duplicate', text.replace(channel, channel + '\n' + channel, 1)),
        ('wrong native terminal frame', replace(channel, 'frame', '0')),
        ('stale priority actor', replace(pool, 'actor', '01036960')),
        ('stale priority main', replace(pool, 'main', '01069590')),
        ('uncleared fifth priority lifetime', replace(pool, 'slots', '0000,0;0000,0;0000,0;0000,0;0001,1')),
        ('missing terminal priority pool', text.replace(pool + '\n', '', 1)),
    ):
        need(bad != text, 'Actual terminal counterexample changes evidence')
        try:
            terminal_gate(bad)
        except (ValueError, KeyError) as error:
            faults.append(dict(kind=label, rejectedBy=str(error)))
        else:
            raise ValueError('Corrupted actual terminal admitted: ' + label)
        need(terminal_gate(text) == positive, 'Whole actual terminal positive restored')
    return positive, faults


def check(ram):
    need(not OUT.exists(), 'Fresh immutable complete current matrix proof')
    scope = prepared.functions()
    original = prepared.original
    verification = original.verification
    current = scope['context']()
    guest = bytes(ram['guest'])
    need(len(guest) == 1048576 and hashlib.sha256(guest).hexdigest().upper() == current.GUEST_SHA and
         ram['report']['guestSHA256'] == current.GUEST_SHA and not original.census.census(),
         'Same final normal terminal and independently initialized whole current guest')
    current.expected = lambda: guest
    observed = scope['observed']
    observed.current = current
    observed.model = original.previous.model
    observed.pressed = original.previous.state
    observed.random_phase_faults = verification.phase_faults
    observed.source = verification.observed.source
    observed.voice_models = lambda: scope['voice_models'](current)
    branches = scope['branch_models'](current)
    observed.random_branch = branches.branch
    fn = scope['collector'](current)
    observed.collector = lambda: (fn, hashlib.sha256(fn.source.encode()).hexdigest().upper())
    _, (held, dropped) = scope['channel_models']()
    namespace = dict(vars(verification), __file__=__file__, OUT=OUT,
                     observed=observed, branches=branches, held_gate=held, drop_gate=dropped)
    exec(compile(inspect.getsource(verification.gate), __file__ + '::whole_four_PCM_fault_wrapper', 'exec'), namespace)
    body = verification.run.source
    first = body.index(' prepath=observed.source.OUT')
    last = body.index(' for p,h in pre[', first)
    body = body[:first] + (
        " prepath=prepared.SOURCE/'report.json';pre=json.loads(prepath.read_text())\n"
        " prior=json.loads((observed.source.previous.held.previous.OUT/'report.json').read_text())\n"
        " fn,digest=observed.collector()\n"
        " need(pre==prepared.functions()['source_guard']() and pre['passed'] and prior['passed'] and "
        "len(prior['actualSourceFaultsRejected'])==8 and pre['transportSourceSHA256']==digest and "
        "fn.__globals__['model']is observed.model and fn.__globals__['state']is observed.pressed,"
        "'Entire current19 immutable source/transport/model/earned state and all eight original observer faults')\n"
    ) + body[last:]
    body = original.once(body, 'audit_v5841_current_cross_tomb_winner_mix_', prepared.PREFIX)
    body = original.once(body, "live=json.loads((folder/'audio_live_source_model.json').read_text())",
        "live=json.loads((folder/'current_19_audio_report.json').read_text())\n"
        "   for p,h in live.get('additionalAnalysisInputHashes',{}).items():"
        "need(sha(p)==h,'Actual complete drop-analysis source frozen');pins[p]=h\n"
        "   live=dict(live,sourceQualifiedNativeLateVictimVoice=live['actualLateVictimVoice'])")
    namespace.update(prepared=prepared)
    exec(compile(body, __file__ + '::whole_four_case_current19_window_cue_fault_matrix', 'exec'), namespace)
    report = namespace['run']()
    for case in report['cases']:
        with gzip.open(Path(case['capture']) / 'run.log.gz', 'rt') as reader:
            text = reader.read()
        case['actual19ChannelTerminalProof'], case['actualTerminalFaultsRejected'] = terminal_faults(text)
    report['actual19ChannelTerminalFaultsRejected'] = sum(len(c['actualTerminalFaultsRejected']) for c in report['cases'])
    pre = json.loads((prepared.SOURCE / 'report.json').read_text())
    report.update(guestSHA256=current.GUEST_SHA, totalSampleChannels=19,
                  originalNaturalIntegrationRequirements=pre['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=pre['originalRemainingWorkGroups'], goalStatus='active',
                  fullStageArtAccepted=False, allStageFinishersAccepted=False, fullPortAcceptance=False)
    for path in (Path(__file__), Path(analysis.__file__), Path(retirement.__file__),
                 Path(prepared.__file__), Path(verification.__file__)):
        report['inputHashes'][str(path.resolve())] = sha(path)
    need(all(sha(p) == h for p, h in report['inputHashes'].items()), 'Entire final matrix evidence frozen')
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in
                      ('cases', 'inputHashes', 'originalNaturalIntegrationRequirements', 'originalRemainingWorkGroups')},
                     indent=2), flush=True)
    return report


def verify(ram):
    try:
        return check(ram)
    except Exception as error:
        if not OUT.exists():
            OUT.mkdir()
            (OUT / 'failure.json').write_text(json.dumps(dict(passed=False, error=repr(error),
                traceback=traceback.format_exc(), inputHashes={str(Path(__file__)): sha(__file__)},
                fullPortAcceptance=False), indent=2) + '\n')
        raise
