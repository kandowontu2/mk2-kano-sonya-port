"""Prove original split grammar from cold real-input controls, not new art.

The main0 stream seeds a temporary actor; both split actors subsequently use
the SAME seven-frame half stream. Never replace main0 with cut-body animation.
"""
import hashlib
import json
import re
import struct
from pathlib import Path
import verify_native_split_v1115 as current

ROOT = current.ROOT
OUT = ROOT / 'audit_v1118_original_split_controls_checked'
CASES = (('liu_kang', 1, 2, 167), ('kitana', 4, 1, 166))
HEX = {'at','pc','actor','other','a0','a9','a11','main','sp','st','flags','other_flags'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def records(text, prefix):
    result = []
    for line in text.splitlines():
        if not line.startswith(prefix + ' '):
            continue
        row = dict(re.findall(r'(\w+)=([^\s]+)', line))
        for key in HEX & row.keys():
            row[key] = int(row[key], 16)
        for key in ('frame','age','id','other_id','writes','damage','wins','action','wrap'):
            if key in row:
                row[key] = int(row[key])
        result.append(row)
    return result


def verify():
    errors, pins, summaries = [], {}, {}
    def need(ok, message):
        if not ok:
            errors.append(message)
    guest, _, _, _ = current.reconstruct()
    original_path = ROOT / 'mk2/mk2-maincpu.bin'
    original = original_path.read_bytes()
    need(digest(original_path) == '45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23', 'Exact original ROM')
    pins[str(original_path)] = digest(original_path)
    def offset(address):
        return (address - 0xff800000) // 8
    def read32(address):
        return struct.unpack_from('<I', original, offset(address))[0]
    def read16(address):
        return struct.unpack_from('<H', original, offset(address))[0]
    # Original instruction words and unmodified whole native split task.
    split_task = bytearray(original[offset(0xff8ce9f0):offset(0xff8cf110)])
    struct.pack_into('<I', split_task, offset(0xff8cea70)-offset(0xff8ce9f0), current.native(0xfbf40))
    need(guest[offset(0xff8ce9f0):offset(0xff8cf110)] == split_task, 'Native split task unchanged except validated table operand')
    need(guest[0xfbf40:0xfbf40+68] == original[offset(0xff8cf110):offset(0xff8cf110)+68], 'Every original split victim table row preserved')
    need(guest[offset(0xff842590):offset(0xff842710)] == original[offset(0xff842590):offset(0xff842710)], 'Native dual animation unchanged')
    need(read16(0xff8ceca0) == 0x5729 and read32(0xff8cecc0) == 0xff906090, 'Original main0 seed lookup')
    need(read16(0xff8cefd0) == 0x4d2b, 'Original A11=A9 after restoring split stream')
    need(read16(0xff842680) == 0x4d69 and read16(0xff8426c0) == 0x4d2b, 'Original second actor cursor swap and advance')
    info = json.loads((ROOT/current.CANDIDATE/'build-info.json').read_text(encoding='utf-8-sig'))
    for name, identity, side, first_age in CASES:
        case = ROOT / f'audit_v1114_kung_lao_{name}_p{side}_stock_control'
        result = json.loads((case/'result.json').read_text(encoding='utf-8-sig'))
        need(result['exit_code'] == 0 and result['candidate'] == current.CANDIDATE and result['executable_sha256'] == info['executable_sha256'] and result['payload_sha256'] == info['payload_sha256'], 'Exact terminal matched build '+case.name)
        need(result['player'] == name and result['victim_slot'] == side and result['winner_slot'] == 3-side and result['killer'] == 'kung_lao' and result['command'] == 'fff_lk' and result['target_gap'] == 112 and result['assistance'] == 'none' and result['cheats_enabled'] is False, 'Real physical control '+case.name)
        for filename, wanted in result['input_hashes'].items():
            path = Path(filename)
            need(path.is_file() and digest(path) == wanted, 'Build input '+filename)
            pins[filename] = wanted
        need((case/'guest_maincpu.bin').read_bytes() == guest, 'Exact reconstructed whole guest '+case.name)
        text = (case/'run.log').read_text(encoding='utf-8-sig')
        historical = ROOT / f'audit_v1098_kung_lao_{name}_p{side}_split_native_trace'
        previous_text = (historical/'run.log').read_text(encoding='utf-8-sig')
        for prefix in ('MK2_STOCK_HEAD_V921_', 'MK2_ROLLING_HEAD_V1003_', 'MK2_SPLIT_V1098_'):
            before = [line for line in previous_text.splitlines() if line.startswith(prefix)]
            after = [line for line in text.splitlines() if line.startswith(prefix)]
            need(bool(before) and after == before, 'Every original native observation unchanged '+case.name+' '+prefix)
        old_pictures = {p.name:p for p in (historical/'snap').rglob('*.png')}
        new_pictures = {p.name:p for p in (case/'snap').rglob('*.png')}
        need(old_pictures.keys() == new_pictures.keys(), 'Every original capture retained '+case.name)
        for filename,path in new_pictures.items():
            need(filename in old_pictures and path.read_bytes() == old_pictures[filename].read_bytes(), 'Actual original scene PNG unchanged '+case.name+' '+filename)
            pins[str(path)] = digest(path)
            if filename in old_pictures:
                pins[str(old_pictures[filename])] = digest(old_pictures[filename])
        pins[str(historical/'run.log')] = digest(historical/'run.log')
        need(not re.search(r'\[LUA ERROR\]|fatal error|access violation|exception at', text, re.I), 'No runtime errors '+case.name)
        actions = records(text, 'MK2_STOCK_HEAD_V921_ACTION')
        need(len(actions) == 1 and actions[0]['damage'] == 322 and actions[0]['address'] == 'FF8C6040', 'Native original two KOs and split activation '+case.name)
        terminal = records(text, 'MK2_STOCK_HEAD_V921_RESULT')
        wraps = records(text, 'MK2_STOCK_HEAD_V921_WRAP')
        need(len(terminal) == 1 and terminal[0]['frame'] == 5198 and terminal[0]['damage'] == 322 and terminal[0]['wins'] == 2 and len(wraps) == 1 and wraps[0]['age'] == 179, 'Original completion and terminal state '+case.name)
        state = [r for r in records(text, 'MK2_SPLIT_V1098_STATE') if r['id'] == identity]
        need(bool(state) and all(r['pc'] == r['at']+16 and r['writes'] == 0 and r['assistance'] == 'none' for r in state), 'Actual original instruction fetches '+case.name)
        by_at = {at: [r for r in state if r['at'] == at] for at in (0xff8cecb0,0xff8cece0,0xff8cede0,0xff8cef00,0xff8cefb0,0xff8cf030,0xff842630,0xff842650,0xff842690,0xff8426b0)}
        need(all(len(by_at[at]) == 1 for at in by_at if at < 0xff842630 or at > 0xff8426b0), 'Exactly one native constructor '+case.name)
        # Bound subsequent indexing; report a failed/incomplete trace, never guess.
        if not all(by_at[at] for at in by_at):
            continue
        entry, lookup, seed = (by_at[at][0] for at in (0xff8cecb0,0xff8cece0,0xff8cede0))
        stance = read32(read32(0xff906150+identity*32))
        selected = stance
        selectors = []
        while read32(selected) == 8:
            wanted, target = read16(selected+32), read32(selected+48)
            selectors.append({'idWord': wanted, 'target': f'{target:08X}'})
            selected += 48
            if wanted == identity:
                selected = target
                break
            selected += 32
        need(entry['a9'] == 0 and lookup['a9'] == stance and seed['a9'] == selected, 'MAIN0 only seeds original second actor '+case.name)
        native_stream = read32(0xff8cf110+identity*32)
        words = [read32(native_stream+32*n) for n in range(12)]
        need(words[3] == 0 and words[11] == 0 and all(words[n] >= 0xff800000 for n in (*range(3),*range(4,11))), 'Original three-plus-seven terminated grammar '+case.name)
        half = native_stream+128
        restored = by_at[0xff8cf030][0]
        physical, other, main = restored['actor'], restored['other'], restored['main']
        need(physical != other and restored['other_id'] == identity and restored['a9'] == half and restored['a11'] == half, 'Both actors start the SAME split half stream '+case.name)
        before, after = by_at[0xff8cef00][0], by_at[0xff8cefb0][0]
        need(before['other'] == other and after['actor'] == other and (before['other_flags'] ^ after['flags']) == 0x10, 'Native constructor toggles only X mirror bit '+case.name)
        steps = [by_at[at] for at in (0xff842630,0xff842650,0xff842690,0xff8426b0)]
        need([len(rows) for rows in steps] == [8,8,8,8], 'Seven half poses plus paired zero sentinel '+case.name)
        for n, rows in enumerate(zip(*steps)):
            a,b,c,d = rows
            cursor = half+n*32
            label = f' paired half step {n} '+case.name
            need(a['actor'] == physical and a['other'] == other and c['actor'] == other and d['actor'] == other and all(r['main'] == main and r['id'] == identity for r in rows), 'True actors'+label)
            need(a['a9'] == cursor and a['a11'] == cursor and b['a9'] == cursor+32 and b['a11'] == cursor and c['a9'] == cursor and d['a9'] == cursor+32 and d['a11'] == cursor, 'Same original stream independently advanced'+label)
            need(a['age'] == first_age+6*n and all(r['frame'] == a['frame'] for r in rows), 'Original six-field timing'+label)
            need((a['flags'] ^ a['other_flags']) & 0x10 == 0x10, 'Opposite native X flip'+label)
            need(a['words9'] == a['words11'] and a['words9'].split(',')[0] == f'{words[n+4]:08X}', 'Original group including final zero'+label)
            need(d['sp'] == a['sp']-64 and d['st'] == b['st'], 'Native saved registers and second status'+label)
        summaries[case.name] = {'victimID': identity, 'victimSlot': side, 'stanceSeed': f'{stance:08X}', 'selectedSeed': f'{selected:08X}', 'originalSelectors': selectors, 'splitStream': f'{native_stream:08X}', 'halfStream': f'{half:08X}', 'sameMirroredHalfPoses': 7, 'pairedZeroSentinel': True, 'firstHalfAge': first_age, 'nativeWrapAge': 179, 'traceRecords': len(state), 'physicalActor': f'{physical:08X}', 'secondActor': f'{other:08X}'}
        for filename in ('run.log','result.json','guest_maincpu.bin'):
            path = case/filename
            pins[str(path)] = digest(path)
        for path in (case/'snap').rglob('*.png'):
            pins[str(path)] = digest(path)
    need(len(summaries) == 2, 'Both genuine original victim controls')
    return {'passed': not errors, 'errors': errors, 'scope': 'original split regression only; genuine Liu P2 and Kitana P1 on v1110, original observations and actual PNGs unchanged', 'cases': summaries, 'main0IsConstructorSeedNotSplitAnimation': True, 'sameHalfStreamMirroredByNativeActor': True, 'replacementMain0Required': False, 'kanoSonyaSplitAccepted': False, 'replacementArtAccepted': False, 'allStockFatalitiesAccepted': False, 'fullPortAccepted': False, 'inputHashes': pins}


if __name__ == '__main__':
    if OUT.exists():
        raise ValueError('Preserve verification evidence')
    report = verify()
    OUT.mkdir()
    (OUT/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'inputHashes'}, indent=2))
    raise SystemExit(0 if report['passed'] else 1)
