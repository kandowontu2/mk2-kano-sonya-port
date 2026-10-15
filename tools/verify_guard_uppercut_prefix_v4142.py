"""Independent physical-input replay of a captured, explicitly incomplete live prefix."""
import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path
import qualify_guard_uppercut_source_v4140 as source
import run_sonya_guard_uppercut_campaign_v4135 as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
FOLDER = ROOT / 'audit_v4138_sonya_guard_uppercut_p2_campaign'
OUT = ROOT / 'audit_v4143_guard_uppercut_actual_prefix_checked'


def parse(text):
    rows = []
    for line in text.splitlines():
        if not line.startswith('MK2_NAT_CAMPAIGN_'):
            continue
        r = dict(re.findall(r'(\w+)=([^\s]+)', line))
        r['tag'] = line.split()[0][len('MK2_NAT_CAMPAIGN_'):]
        r['frame'] = int(r['frame'])
        rows.append(r)
    return rows


def replay(text):
    rows = parse(text)
    decisions = {r['frame']: r for r in rows if r['tag'] == 'GUARD_DECISION'}
    inputs = collections.defaultdict(list)
    for r in rows:
        if r['tag'] == 'INPUT':
            inputs[r['frame']].append(r['button'])
    fields = [r for r in rows if r['tag'] == 'GUARD_FIELD' and r['frame'] in decisions]
    need(fields, 'Actual complete guard fields, not a fixture-only gate')
    previous, leg, last_leg, upper, guard, move = None, None, -1000, -1000, -1000, None
    reasons = collections.Counter()
    live = {r['frame']: r for r in rows if r['tag'] == 'LIVE'}
    for f in fields:
        frame = f['frame']
        need(f['human_slot'] == '2' and f['fighter'] == 'sonya' and
             f['human_id'] == f['human_roster'] == '18', 'Actual true Sonya P2 identity')
        need(f['cpu_id'] == f['cpu_roster'] and int(f['cpu_roster']) in (5, 10, 18),
             'Actual true target roster, never a proxy or Shang morph substitute')
        for who in ('human', 'cpu'):
            actor, main = int(f[who + '_actor'], 16), int(f[who + '_main'], 16)
            need(0x01000000 <= actor < 0x01100000 and 0x01000000 <= main < 0x01100000 and
                 f[who + '_owner'] == f[who + '_actor'], 'Actual actor/Main ownership')
        need(all(0 < int(hp) <= 161 for hp in f['health'].split(',')), 'Actual live positive health, not injected victory')
        reset = previous is None or frame - previous != 1
        need(int(f['reset']) == int(reset), 'Independent contiguous-field controller reset')
        if reset:
            leg, last_leg, upper, guard, move = None, -1000, -1000, -1000, None
        previous = frame
        hx, cx = int(f['h_x']), int(f['c_x'])
        height = int(f['h_floor']) - int(f['h_y'])
        cpu_height = int(f['c_floor']) - int(f['c_y'])
        gap = abs(hx - cx)
        action, ca = int(f['human_action']), int(f['cpu_action'])
        flags, body = int(f['flags'], 16), int(f['body'], 16)
        blocking = action in (0x700, 0x701)
        ready = height <= 8 and (blocking or action in (0, 0x303, 0x302, 0x304, 0x107)) and not flags & 0x18 and (blocking or not body & 0x0c)
        safe = ca in (0, 0x303, 0x302, 0x304, 0x107) or 0x600 <= ca <= 0x60f
        if ca in (4, 0xa, 0x10):
            guard = frame + 40
        expected = []
        if leg is not None and frame - leg < 12:
            reason, age = move + '_sequence', frame - leg
            if age < 7:
                expected.append('Down')
            if 3 <= age < 7:
                expected += ['Low_Punch', 'Block'] if move == 'leg' else ['High_Punch']
        elif height > 8:
            reason, expected = 'actual_air_recovery', ['Block']
            if gap < 105 and frame % 6 < 3:
                expected.append('High_Kick')
        elif cpu_height > 15 and gap < 100:
            reason, expected = 'anti_air_guard', ['Down']
            if ready and gap < 78 and frame - upper >= 26:
                reason, upper = 'anti_air_attempt', frame
                expected.append('High_Punch')
            else:
                expected.append('Block')
        elif frame < guard:
            reason, expected = 'projectile_guard', ['Down', 'Block']
        elif not safe and gap < 125:
            reason, expected = 'active_guard', ['Down', 'Block']
        elif ready and safe and gap < (85 if f['cpu_roster'] == '18' else 63) and frame - last_leg >= 32:
            move = 'leg' if f['cpu_roster'] == '18' else 'uppercut'
            reason, leg, last_leg = move + '_attempt', frame, frame
            expected = ['Down']
        elif ready and safe and gap > (75 if f['cpu_roster'] == '18' else 58) and cpu_height <= 8:
            reason, leg = 'grounded_approach', None
            expected = ['Right' if hx < cx else 'Left']
        else:
            reason, expected = 'stance_guard', ['Down', 'Block']
        need(decisions[frame]['reason'] == reason, 'Independently replayed physical decision at ' + str(frame))
        need(inputs[frame] == expected, 'Independently replayed exact physical button edges at ' + str(frame))
        reasons[reason] += 1
        if frame in live:
            old = live[frame]
            mapping = dict(human_actor=f['human_actor'], human_main=f['human_main'], cpu_actor=f['cpu_actor'], cpu_main=f['cpu_main'],
                           human='18:18', cpu=f['cpu_roster'] + ':' + f['cpu_id'],
                           hpos=f['h_x'] + ',' + f['h_y'], cpos=f['c_x'] + ',' + f['c_y'],
                           hfloor=f['h_floor'], cfloor=f['c_floor'], actions=f['human_action'] + ',' + f['cpu_action'],
                           flags=f['flags'] + ',' + f['cpu_flags'], poses=f['human_pose'] + ',' + f['cpu_pose'], health=f['health'])
            need(all(old[k] == v for k, v in mapping.items()), 'Complete original LIVE state cross-check')
    specials = [r for r in rows if r['tag'] == 'SPECIAL' and r['move'] == 'leg']
    for r in specials:
        need(r['id'] == r['roster'] == '18' and r['actor'] == r['a8'] and r['main'] == r['a13'] and
             r['entry'] == 'FFF80800' and r['at'] == 'FFF80810' and r['pc'] == 'FFF80830',
             'Actual own native leg task activation, not planned inputs credited as success')
    actions = [r for r in rows if r['tag'] == 'GUARD_ACTION']
    fields_by = {r['frame']: r for r in fields}
    for r in actions:
        need(r['id'] == r['roster'] == '18' and r['actor'] == r['owner'] == r['a8'] and r['main'] == r['a13'],
             'Actual native guarded action true Sonya owner/registers')
        need(int(r['at'], 16) == int(r['main'], 16) + 0x1f0 and r['mask'] == 'FFFF' and
             0 <= int(r['before']) <= 65535 and 0 <= int(r['after']) <= 65535 and
             0 < int(r['health'].split(',')[0]) <= 161, 'Actual native Main action address/mask/live health')
        if r['frame'] in fields_by:
            field = fields_by[r['frame']]
            need(r['actor'] == field['human_actor'] and r['main'] == field['human_main'],
                 'Same-field native action belongs to physical human')
        if int(r['after']) == 0x107:
            need(r['pc'] == 'FF83C340' and int(r['a1'], 16) & 0xffff == 0x107,
                 'Original HUMAN107 uppercut store/PC/operand, not CPU106 or a planned button credited')
    return dict(actualCompleteGuardFields=len(fields), firstFrame=fields[0]['frame'], lastFrame=fields[-1]['frame'],
                reasons=dict(reasons), actualNativeLegActivations=len(specials),
                actualNativeGuardedActionStores=len(actions),actualNativeHumanUppercut107Stores=sum(int(r['after'])==0x107 for r in actions),
                stages=[int(r['stage']) for r in rows if r['tag'] == 'STAGE'],
                actualOwnNativeRoundWins=sum(r['tag'] == 'WIN' and r['slot'] == '2' for r in rows),
                actualPaidLosses=sum(r['tag'] == 'LOSS' for r in rows))


def change(text, tag, frame, key, value):
    pattern = rf'^(MK2_NAT_CAMPAIGN_{tag} frame={frame} [^\r\n]*?\b{key}=)([^\s]+)'
    damaged, count = re.subn(pattern, lambda m: m[1] + str(value), text, count=1, flags=re.M)
    need(count == 1 and damaged != text, 'Actual non-vacuous row fault')
    return damaged


def main():
    need(not OUT.exists(), 'Fresh immutable prefix qualifier')
    source.source_boundary()
    raw = (FOLDER / 'run.log').read_bytes()
    # Drop the single partially flushed line; never mutate the growing native log.
    raw = raw[:raw.rfind(b'\n') + 1]
    text = raw.decode('utf-8')
    positive = replay(text)
    need(positive['reasons'].get('uppercut_attempt', 0) > 0 and positive['actualNativeHumanUppercut107Stores'] > 0 and
         positive['actualNativeLegActivations'] > 0, 'Closer buffered uppercut must activate original HUMAN107, mirror native leg retained')
    rows = parse(text)
    target = next(r for r in rows if r['tag'] == 'GUARD_DECISION' and r['reason'] == 'leg_attempt')['frame']
    field = next(r for r in rows if r['tag'] == 'GUARD_FIELD' and r['frame'] == target)
    trials = []
    faults = [('human_id', '0'), ('human_roster', '0'), ('cpu_id', '0'), ('human_owner', '01000000'),
              ('health', '0,161'), ('reset', 1 - int(field['reset'])), ('human_action', 0x500), ('cpu_action', 0x507)]
    for key, value in faults:
        try:
            replay(change(text, 'GUARD_FIELD', target, key, value))
        except ValueError as error:
            trials.append(dict(key=key, rejectedBy=str(error)))
        else:
            raise ValueError('Actual row fault accepted: ' + key)
        need(replay(text) == positive, 'Exact positive restored after every state fault')
    for tag, key, value in [('GUARD_DECISION', 'reason', 'stance_guard'), ('INPUT', 'button', 'Up')]:
        try:
            replay(change(text, tag, target, key, value))
        except ValueError as error:
            trials.append(dict(key=tag + ':' + key, rejectedBy=str(error)))
        else:
            raise ValueError('Actual physical decision/input fault accepted')
        need(replay(text) == positive, 'Exact positive restored after physical edge fault')
    action = next(r for r in rows if r['tag'] == 'GUARD_ACTION' and int(r['after']) == 0x107)
    for key, value in [('pc', 'FFF00000'), ('a1', '00000106'), ('a8', '01000000'), ('mask', '00FF')]:
        try:
            replay(change(text, 'GUARD_ACTION', action['frame'], key, value))
        except ValueError as error:
            trials.append(dict(key='GUARD_ACTION:' + key, rejectedBy=str(error)))
        else:
            raise ValueError('Actual original human uppercut store fault accepted')
        need(replay(text) == positive, 'Exact positive restored after native uppercut store fault')
    proof_path = FOLDER / 'guest_memory_proof.json'
    proof = json.loads(proof_path.read_text())
    expected = capture.expected()
    need(hashlib.sha256(expected).hexdigest().upper() == proof['sha256'] ==
         '938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821' and
         proof['bytes'] == 1048576 and proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten'] == 0 and
         proof['captureSourceSHA256'] == sha(capture.__file__) and
         proof['transportSourceSHA256'] == sha(ROOT / capture.LUA), 'Full actual RAM guest/source provenance')
    before = json.loads((FOLDER / 'input_hashes_before.json').read_text())
    need(all(sha(path) == digest for path, digest in before.items()), 'All actual executed sources unchanged')
    pins = dict(before)
    for path in (Path(__file__), Path(source.__file__), proof_path, FOLDER / 'input_hashes_before.json',
                 ROOT / 'audit_v4141_guard_uppercut_source_preflight/report.json'):
        pins[str(path.resolve())] = sha(path)
    report = dict(passed=True, actualCapturedPrefix=positive, actualRowFaultsRejected=trials,
                  inputHashes=pins, nativeLogPrefixBytes=len(raw), nativeLogPrefixSHA256=hashlib.sha256(raw).hexdigest().upper(),
                  prefixProofOnly=True, completedWholeCampaignAccepted=False, campaignClearAccepted=False,
                  endingPixelsAccepted=False, completeCampaignAudioAccepted=False, fullPortAcceptance=False)
    OUT.mkdir()
    need(subprocess.run(['compact.exe', '/C', '/I', '/Q', '/S:' + str(OUT)], capture_output=True).returncode == 0,
         'Compress report directory before writes')
    (OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(passed=True, prefix=positive, actualFaultsRejected=len(trials), fullPortAcceptance=False), indent=2))


if __name__ == '__main__':
    main()
