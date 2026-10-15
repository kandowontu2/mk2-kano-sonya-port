"""Check native stomp wait/return/control, not a tower clear or visual fidelity."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDS = {'liu_kang': 1, 'kano': 17, 'sonya': 18}
ASSIST = 'single_preconstruction_stage_index'
HEX = {'own', 'main', 'attacker', 'attacker_main', 'action', 'pc', 'entry',
       'a8', 'a13', 'a0', 'a1', 'sp', 'actor', 'owner', 'flags', 'pose',
       'vx', 'vy', 'field', 'at', 'schedule'}
EXE = 'AD98FE42383F776BBD49BA4298EFD1F9F021FD2988C6B0A3956EE64316B44E82'
PAYLOAD = '1367D5A0D42C661CF555F42231A20A650C28E107AB9C80BD821C0BEA7EB4D5EF'
ORIGINAL = '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23'
GUEST = '8395DD271BA3A8B8FABED892E9C3E14E2BA51EC8D952A041BA667AFB8015010D'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest().upper()


def parse(text):
    rows = []
    for match in re.finditer(r'^MK2_NAT_CAMPAIGN_(\w+) (.*)$', text, re.M):
        row = dict(re.findall(r'(\w+)=([^\s]+)', match[2]))
        row.update(tag=match[1], event=match.start())
        for key, value in tuple(row.items()):
            if key in HEX and re.fullmatch(r'[0-9A-Fa-f]+', str(value)):
                row[key] = int(value, 16)
            elif re.fullmatch(r'-?\d+', str(value)):
                row[key] = int(value)
        if row['tag'] == 'BOSS_FIELD':
            row['task'] = {int(k, 16): int(v, 16) for k, v in
                           (part.split(':') for part in row['task'].split(','))}
        rows.append(row)
    return rows


def verify(folder, check_hashes=True, text_override=None, source_override=None):
    result = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
    text = text_override if text_override is not None else (folder / 'run.log').read_text(encoding='utf-8-sig')
    source = source_override if source_override is not None else (folder / 'input_sources/mk2ks_native_boss_recovery_v680_v3.lua').read_text()
    errors = []
    def need(ok, label):
        if not ok and label not in errors:
            errors.append(label)
    side = result['human_slot']; identity = IDS[result['player']]
    release = 148 + side
    need(side in (1, 2) and result['cpu_slot'] == 3 - side, 'Actual physical slots')
    need(result['exit_code'] == 0 and result['assistance'] == ASSIST and
         result['unassisted_clear_proven'] is False, 'Terminal explicitly staged diagnostic')
    need(result['candidate'] == 'diagnostic_v680_native_pit_initial_cache' and
         result['executable_sha256'] == EXE and result['payload_sha256'] == PAYLOAD,
         'Unchanged matched current candidate')
    if check_hashes:
        for name, sha in result['input_hashes'].items():
            need(Path(name).is_file() and digest(Path(name)) == sha, 'Frozen input changed: ' + name)
        for name in ('mk2ks_native_boss_recovery_v680_v3.lua', 'run_native_boss_recovery_v680_v3.ps1'):
            frozen = folder / 'input_sources' / name
            original = ROOT / (('tools/' if name.endswith('.ps1') else '') + name)
            need(digest(frozen) == digest(original), 'Retained runner/observer source matches executed input')
    writes = re.findall(r'\bp:write_\w+\([^\n]*\)', source)
    need(writes == ['p:write_u16(0x01061b30,15)'] and
         not re.search(r'\bload\s*\(|\bdofile\s*\(|\beval\b', source), 'Only one declared stage fixture; no health/actor/delegated writes')
    runner = (folder / 'input_sources/run_native_boss_recovery_v680_v3.ps1').read_text(encoding='utf-8-sig')
    need('-nocheat' in runner and '-noautoframeskip -frameskip 0' in runner and
         'input_hashes=$hashes' in runner, 'Frozen isolated no-cheat runner with input guards')
    need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at', text, re.I), 'No observer/native runtime errors')
    rows = parse(text)
    need(all(r.get('observer_writes') == 0 and r.get('setup_assistance') == ASSIST and
             r.get('human_slot') == side and r.get('fighter') == result['player'] for r in rows), 'Every record declares actual staged scope')
    tags = lambda tag: [r for r in rows if r['tag'] == tag]
    boot, setup, begin, stomp, terminal = (tags(t) for t in ('BOOT', 'BOSS_SETUP', 'BOSS_BEGIN', 'BOSS_STOMP', 'BOSS_RESULT'))
    need(len(boot) == len(setup) == len(begin) == len(stomp) == len(terminal) == 1, 'Exactly one setup/first stomp/terminal result')
    if not (len(setup) == len(begin) == len(stomp) == len(terminal) == 1):
        return dict(passed=False, errors=errors, unassisted_clear_proven=False, fullPortAcceptance=False)
    setup, begin, stomp, terminal = setup[0], begin[0], stomp[0], terminal[0]
    need(setup['stage_before'] == 0 and setup['stage_after'] == 15 and setup['mode'] == 4 and
         setup['state'] == 4 and setup['own_roster'] == identity and setup['cpu_roster'] == 65535 and
         setup['field'] == 0x01061b30 and setup['event'] < begin['event'], 'Single preconstruction fixture after genuine locked selection')
    selected = [r for r in tags('SELECT_ID') if r['event'] < setup['event']]
    need(len(selected) == 2 and all(r['roster'] == identity and r['state'] == 3 for r in selected), 'Actual true-ID native selection before fixture')
    need(begin['own_id'] == identity and begin['cpu_id'] == 12 and begin['health'] == '161,161' and
         begin['last_prep'] == setup['frame'] and begin['prep_writes'] == 1 and begin['health_writes'] == 0,
         'Native construction of full-health true character and Kintaro')
    need(terminal['begin'] == begin['frame'] and terminal['stomp'] == stomp['frame'] and
         terminal['prep_writes'] == 1 and terminal['last_prep'] == setup['frame'] and terminal['boss_writes'] == 0 and
         terminal['unassisted_clear_proven'] == 'false', 'No writes during boss; never classified as a natural tower')
    need(stomp['id'] == identity and stomp['pc'] == 0xff836700 and stomp['action'] == 0x407 and
         stomp['before'] - stomp['after'] == 56 and stomp['after'] > 0 and
         stomp['attacker'] == stomp['own'], 'Original native stomp store with A8 victim, not purported attacker')
    matching = [r for r in tags('HEALTH') if r['frame'] == stomp['frame'] and r['slot'] == side and
                r['before'] == stomp['before'] and r['after'] == stomp['after'] and r['pc'] == stomp['pc'] and
                r['a8'] == stomp['own'] and r['a13'] == stomp['attacker_main']]
    need(len(matching) == 1, 'Actual owned native HP store underlying first stomp')
    fields = tags('BOSS_FIELD'); own = {}; boss = {}
    for row in fields:
        target = own if row['slot'] == side else boss
        need(row['age'] not in target, 'No duplicate actual field/physical slot')
        target[row['age']] = row
    ages = range(release + 3)
    need(all(age in own and age in boss for age in ages), 'Continuous same-episode victim and boss fields through first control movement')
    if not all(age in own and age in boss for age in ages):
        return dict(passed=False, errors=errors, unassisted_clear_proven=False, fullPortAcceptance=False)
    first = own[0]; bfirst = boss[0]
    for age in ages:
        row, other = own[age], boss[age]
        need(row['frame'] == other['frame'] == stomp['frame'] + age, 'Actual field age/frame binding')
        need(row['actor'] == row['owner'] == stomp['own'] and row['main'] == stomp['main'] and
             row['id'] == row['roster'] == identity and row['state'] == 1 and
             other['actor'] == other['owner'] == bfirst['actor'] and other['main'] == stomp['attacker_main'] and
             other['id'] == other['roster'] == 12 and other['state'] == 0, 'Stable true-ID actor/Main physical ownership, not a new-round actor')
        need(row['hp'] == stomp['after'] and row['y'] == row['floor'] == first['floor'], 'Same live victim HP and ground interval without reset')
        task = row['task']
        # Both slots observe boss action clear at age 149. P2's native victim
        # cooperative task sees that change on its next scheduler field.
        need(other['action'] == (0x407 if age < 149 else 0), 'Native boss action clears at age 149 in both physical slots')
        need(set(task) == set(range(0, 0x451, 0x10)) and task[0xc0] == row['actor'] and
             task[0x1f0] & 0xffff == row['action'] and task[0x200] & 0xffff == row['floor'] and
             task[0x210] & 0xffff == row['flags'], 'Full native task words bind independently sampled owner/action/floor/flags')
        if age < release:
            need(row['flags'] == 5 and row['action'] == 0 and row['x'] == first['x'] and row['vx'] == row['vy'] == 0 and
                 task[0xe0] == 0xff8392b0 and task[0x60] == 0x407 and task[0x170] == other['main'],
                 'Original cooperative wait through native per-slot scheduling')
        else:
            need(row['flags'] == 1 and other['action'] != 0x407, 'Native release only after waited boss action changes')
    need(own[release]['action'] == 0x303 and own[release]['task'][0xe0] == 0xff82f270 and
         own[release]['x'] == first['x'] and own[release + 1]['action'] == 0 and
         own[release + 1]['task'][0xe0] == 0xff830d00 and own[release + 1]['x'] == first['x'] and
         own[release + 2]['task'][0xe0] == 0xff830d00 and own[release + 2]['x'] == first['x'] + 2 and
         own[release + 2]['pose'] != first['pose'], 'Original human control return followed by actual native Right movement')
    entries = [r for r in tags('BOSS_ENTRY') if r['age'] <= release]
    need(len(entries) == 1 and entries[0]['age'] == release and entries[0]['frame'] == stomp['frame'] + release and
         entries[0]['entry'] == 0xff861350 and entries[0]['pc'] == 0xff861360 and
         entries[0]['a8'] == first['actor'] and entries[0]['a13'] == first['main'], 'Actual original victim recovery-entry call on owned Main')
    inputs = [r for r in tags('INPUT') if stomp['frame'] < r['frame'] <= stomp['frame'] + release + 2]
    need(len(inputs) == release + 2 and all(r['button'] == 'Right' for r in inputs) and
         [r['frame'] for r in inputs] == list(range(stomp['frame'] + 1, stomp['frame'] + release + 3)), 'Continuous ordinary Right input; no artificial controller release')
    original_path = ROOT / 'mk2/mk2-maincpu.bin'
    guest_path = ROOT / 'audit_v684_pit_guest_rom_integrity/diagnostic_v680_native_pit_initial_cache/guest_maincpu.bin'
    need(digest(original_path) == ORIGINAL and digest(guest_path) == GUEST, 'Authoritative original and current guest program identities')
    original = original_path.read_bytes(); guest = guest_path.read_bytes()
    # Compare entire native cooperative wait, return and input continuation ranges.
    ranges = ((0xff839260, 0xff839370), (0xff861350, 0xff861550),
              (0xff82efa0, 0xff82f2a0), (0xff830cd0, 0xff830d80), (0xff8366c0, 0xff836710))
    for start, end in ranges:
        need(original[(start - 0xff800000) // 8:(end - 0xff800000) // 8] ==
             guest[(start - 0xff800000) // 8:(end - 0xff800000) // 8], 'Native instruction range unchanged: %08X' % start)
    return dict(passed=not errors, errors=errors, player=result['player'], human_slot=side,
                stomp_damage=56, native_held_fields=release, first_movement_age=release + 2,
                verified_episode_fields=release + 3, total_captured_own_fields=len(own),
                legacy_attacker_label_means='actual A8 victim actor; attacker_main is actual execution boss Main',
                setup_assistance=ASSIST, unassisted_clear_proven=False, fullPortAcceptance=False,
                scope='First native Kintaro stomp wait, recovery and ordinary input return; no tower, all-boss, render or audio acceptance')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('folder', type=Path); parser.add_argument('--output', type=Path)
    args = parser.parse_args(); report = verify(args.folder)
    if args.output:
        if args.output.exists(): raise ValueError('Do not overwrite evidence')
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(not report['passed'])
