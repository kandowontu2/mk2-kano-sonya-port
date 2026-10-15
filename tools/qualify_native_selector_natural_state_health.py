"""Whole original native health/state ledgers for actual Kano17/Sonya18 games.

Prove the selected schedule against all six source-derived native ROM lists,
then change only the old ledger's fixed schedule context. No CPU choice claim:
the retained observer was filtered to Kano17, while the actual CPU is Sonya18.
Historical rejection and source pins are preserved with explicit source sync.
"""
import hashlib
import inspect
import json
import re
import struct
from pathlib import Path
import psutil
import verify_native_extended_cpu_v2946 as original
import verify_native_source_sync as migration

ROOT, need = migration.ROOT, original.need
OUT = ROOT / 'audit_native_selector_natural_state_health_checked'


def rows(text, tag):
    answer = []
    for line in text.splitlines():
        if line.startswith(tag + ' '):
            fields = re.findall(r'(\w+)=([^\s]+)', line)
            need(len(fields) == len(dict(fields)), 'Unambiguous actual native fields')
            answer.append(dict(fields))
    return answer


def bind_health(schedule):
    source = inspect.getsource(original.health_ledger)
    before = "row['schedule']==0xfffa3180"
    need(source.count(before) == 1, 'Only old fixed schedule context differs')
    source = source.replace(before, "row['schedule']==schedule", 1)
    scope = dict(original.health_ledger.__globals__, schedule=schedule)
    exec(compile(source, __file__ + '::whole_original_health_actual_schedule', 'exec'), scope)
    return scope['health_ledger']


def gate(text, guest):
    need(not re.search(r'LUA ERROR|stack traceback|fatal error|access violation', text, re.I),
         'No actual native/observer runtime error')
    pair = original.pair
    cold = pair.rows_prefix(text, 'MK2_P2CPU_COLD_LIVE ')
    selected = pair.rows_prefix(text, 'MK2_P2CPU_SELECT_RESULT ')
    need(len(cold) == len(selected) == 1, 'One real cold physical selection')
    c, s = cold[0], selected[0]
    need(c['human'] == s['human'] == 'kano' and
         c['human_id'] == s['human_id'] == 17 and c['cpu_id'] == s['initial_cpu'] == 18 and
         c['stage'] == 0 and c['frame'] == s['live'] == 1818 and
         s['checks'] == 50 and s['errors'] == 0 and 700 < s['css'] < s['exit'] < s['live'] and
         all(r['writes'] == 0 and r['assistance'] == 'none' for r in (c, s)),
         'Actual selected Kano17 enters naturally chosen Sonya18 without proxies')
    table = struct.unpack_from('<I', guest, (0xff8a11f0 - 0xff800000) // 8)[0]
    expected = pair.expected_orders()
    rom = pair.rows(text, 'ROM')
    need(table == 0xfffa2c00 and len(rom) == 6 and
         [r['order'] for r in rom] == list(range(6)), 'Entire native ladder inventory')
    for i, row in enumerate(rom):
        pointer = struct.unpack_from('<I', guest, (table + i * 32 - 0xff800000) // 8)[0]
        ids = struct.unpack_from('<17H', guest, (pointer - 0xff800000) // 8)
        need(row['table'] == table and row['list'] == pointer == 0xfffa3000 + i * 0x180 and
             tuple(map(int, row['ids'].split(','))) == ids == expected[i] and
             row['writes'] == 0 and row['assistance'] == 'none',
             'Every whole actual list matches independent source-derived native order')
    orders = [r['order'] for r in rom if r['list'] == c['schedule']]
    need(len(orders) == 1 and expected[orders[0]][0] == c['cpu_id'],
         'Actual schedule selects real Sonya at stage zero, not supplied CPU ID')
    hp, by = bind_health(c['schedule'])(text, guest, 'kano')
    state = original.state_ledgers(text, guest, 'kano', by)
    need(hp['first'] == 1818 and hp['last'] == 3618 and hp['allModePhysicalFields'] == 3602,
         'Whole original 1800-field window includes every round/transition callback')
    # Keep the raw choice coverage gap visible. CODE is not an executing event.
    choice = rows(text, 'MK2_CPU_CHOICE_EVENT')
    result = rows(text, 'MK2_CPU_CHOICE_RESULT')
    need(not choice and len(result) == 1 and result[0]['choices'] == '0',
         'Kano-only observer genuinely recorded zero CPU choice events')
    for row in rows(text, 'MK2_CPU_CHOICE_CODE'):
        start, stop = (int(row[k], 16) for k in ('start', 'stop'))
        words = [int(word, 16) for word in row['words'].split(',')]
        need(struct.pack('<' + 'H' * len(words), *words) ==
             guest[(start - 0xff800000) // 8:(stop - 0xff800000) // 8],
             'Whole observed choice code is source-bound, not choice execution')
    return dict(passed=True, actualNativeTower=orders[0], schedule=c['schedule'],
                trueHumanID=17, trueCPUID=18, wholeNativeHealthLedger=hp,
                wholeUnchangedNativeStateLedger=state,
                actualCPUChoiceEvents=0, fullNaturalCPUChoiceAcceptance=False,
                completedGrabAcceptance=False, wholeRasterAudioAcceptance=False,
                allModesAllOpponentsAccepted=False, fullPortAcceptance=False)


def execute(state, cases):
    need(not OUT.exists(), 'Fresh immutable whole native state/health qualification')
    host = psutil.Process()
    need(host.pid == 38752 and host.ppid() == 40316 and
         host.create_time() == 1791734919.6266766 and
         host.cmdline()[1:] == ['-B', 'tools/capture_native_selector_special_shadow.py'],
         'Original exact live native capture host, not a timeout replay')
    migrated = migration.verify()
    need(migrated['passed'] and migrated['trackedCanonicalCompileInputs'] == 15,
         'Whole independently synchronized compiled/current/historical source provenance')
    pins = {str(Path(migration.__file__).resolve()): migration.sha(migration.__file__),
            str(Path(__file__).resolve()): migration.sha(__file__),
            str(ROOT / 'audit_native_source_sync/report.json'):
                migration.sha(ROOT / 'audit_native_source_sync/report.json')}
    old_paths = {str((ROOT / 'mame-mkp/src/mame/midway' / name).resolve()):
                 (migration.BACKUP / ('canonical_' + Path(name).stem + '_before_sync' + Path(name).suffix), digest)
                 for name, digest in migration.OLD.items()}
    def pin(path, digest):
        key = str(Path(path).resolve())
        if key in old_paths and digest == old_paths[key][1]:
            path = old_paths[key][0]
            key = str(path.resolve())
        need(migration.sha(path) == digest, 'Whole immutable original input or explicit preserved source: ' + key)
        need(key not in pins or pins[key] == digest, 'No conflicting source pin')
        pins[key] = digest
    compiled = json.loads((migration.BUILD / 'build-info.json').read_text())
    for path, digest in compiled['canonical_source_hashes_at_compile'].items():
        pin(path, digest)
    qualifications, faults = [], []
    for capture, expected_pid, expected_birth in cases:
        folder, text, images = capture.RAM_CASES[capture.KEY]
        meta = json.loads((folder / 'result.json').read_text())
        receipt = json.loads((capture.OUT / 'report.json').read_text())
        held = capture.NATIVE_HANDLES[capture.KEY]
        identity = held['identity']
        need(meta['passed'] and receipt['passed'] and held['process'].poll() == meta['nativeExit'] == 0 and
             identity == receipt['actualNativeIdentity'] == meta['nativeTerminal']['actualWindowsIdentity'] and
             (identity['ProcessId'], identity['ParentProcessId'], identity['createdUnix']) ==
             (expected_pid, host.pid, expected_birth) and not meta['nativeTerminal']['hostDecodeErrors'],
             'Same exact original terminal native game and full transport, no replay')
        need(not receipt['originalNativeStateContract']['wholeOriginalNativeStateHPAndChoices']['passed'],
             'Original mirror-specific rejection remains false and preserved separately')
        windows = {'cold_high': state['WINDOWS']['high'], 'cold_owned': state['WINDOWS']['owned'],
                   'cold_graphics': state['WINDOWS']['graphics'], 'guest': state['guest'], 'gfx': state['gfx']}
        need(set(meta['proofs']) == set(windows), 'All five full actual cold/runtime windows')
        for key, raw in windows.items():
            need(meta['proofs'][key] == dict(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest().upper(),
                 everyActualByteComparedInRAM=True), 'Every actual cold byte independently compared: ' + key)
        positive = gate(text, state['guest'])
        def change(tag, key, value, **where):
            line = next(line for line in text.splitlines() if line.startswith(tag + ' ') and
                        all(dict(re.findall(r'(\w+)=([^\s]+)', line)).get(k) == str(v)
                            for k, v in where.items()))
            altered, count = re.subn(r'\b' + key + r'=\S+', key + '=' + value, line, count=1)
            need(count == 1 and altered != line, 'Effective mutation of a real actual field')
            return text.replace(line, altered, 1)
        # Test every core inventory and ledger boundary. Choose actual store rows
        # dynamically, not assumptions about an opponent's prescribed trajectory.
        health = rows(text, 'MK2_CPU_ROUND_HEALTH')
        flags = rows(text, 'MK2_CPU_PAIR_FLAG')
        field = rows(text, 'MK2_CPU_PAIR_FIELD')[0]
        need(health and flags, 'Actual health and action/body/flag store histories observed')
        trials = [
            ('tower_pointer', change('MK2_CPU_PAIR_ROM', 'list', 'FFFA0000', order=positive['actualNativeTower'])),
            ('cold_proxy', change('MK2_P2CPU_COLD_LIVE', 'cpu_id', '17')),
            ('wrong_actual_schedule', change('MK2_CPU_ROUND_FIELD', 'schedule', 'FFFA3180', frame=1818, slot=2)),
            ('missing_all_mode_callback', text.replace(next(line + '\n' for line in text.splitlines()
                if line.startswith('MK2_CPU_ROUND_FIELD ')), '', 1)),
            ('health_unexplained', change('MK2_CPU_ROUND_FIELD', 'hp', '160', frame=1818, slot=1)),
            ('health_store_instruction', change('MK2_CPU_ROUND_HEALTH', 'op0', 'FFFF', frame=health[0]['frame'], slot=health[0]['slot'])),
            ('health_store_mask', change('MK2_CPU_ROUND_HEALTH', 'mask', 'FFFE', frame=health[0]['frame'], slot=health[0]['slot'])),
            ('state_store_instruction', change('MK2_CPU_PAIR_FLAG', 'op0', 'FFFF', frame=flags[0]['frame'], slot=flags[0]['slot'])),
            ('state_store_target', change('MK2_CPU_PAIR_FLAG', 'at', '01000000', frame=flags[0]['frame'], slot=flags[0]['slot'])),
            ('live_owner', change('MK2_CPU_PAIR_FIELD', 'owner', '01000000', frame=field['frame'])),
            ('human_proxy', change('MK2_CPU_PAIR_FIELD', 'vid', '1', frame=field['frame'])),
            ('live_floor', change('MK2_CPU_PAIR_FIELD', 'floor', '80', frame=field['frame'])),
            ('false_choice_coverage', change('MK2_CPU_CHOICE_RESULT', 'choices', '1')),
        ]
        for label, bad in trials:
            need(bad != text, 'Effective native state/health counterexample')
            try:
                gate(bad, state['guest'])
            except (AssertionError, ValueError, KeyError, IndexError) as error:
                faults.append(dict(nativePID=expected_pid, fault=label, rejectedBy=str(error)))
            else:
                raise ValueError('Actual native ledger corruption accepted: ' + label)
        need(gate(text, state['guest']) == positive, 'Whole untouched native ledger restored after faults')
        qualifications.append(dict(nativePID=expected_pid, actualNativeIdentity=identity,
                                   qualification=positive, originalMirrorRejectionPreserved=True,
                                   originalRGBCallbacks=len(images), RGBReviewedInThisQualification=False))
        for path, digest in receipt['inputHashes'].items():
            pin(path, digest)
        for path in (capture.OUT / 'report.json', *(p for p in folder.rglob('*') if p.is_file())):
            pin(path, migration.sha(path))
    for module in (original, original.pair, original.rounds, original.overlap):
        pin(module.__file__, migration.sha(module.__file__))
    need(all(migration.sha(path) == digest for path, digest in pins.items()),
         'Fresh final whole immutable qualification inventory')
    report = dict(passed=True, goalStatus='active', qualifications=qualifications,
                  wholeAllModePhysicalFields=sum(r['qualification']['wholeNativeHealthLedger']['allModePhysicalFields']
                                                for r in qualifications),
                  originalHealthAndStateRulesRetained=True,
                  actualFaultsRejected=faults, inputHashes=pins,
                  originalSourceMigrationReceipt=str(ROOT / 'audit_native_source_sync/report.json'),
                  fullNaturalCPUChoiceAcceptance=False, fullPortAcceptance=False,
                  requirements=receipt['requirements'], remainingGroups=receipt['remainingGroups'],
                  newNativeGames=0, newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0)
    OUT.mkdir()
    # Artifact output, not a source edit; original capture helper's JSON saver.
    capture.prior.current.prior.save(OUT / 'report.json', report)
    print('PASS both whole actual17/18 native state/health ledgers; natural Sonya AI choice coverage remains open', flush=True)
    return report
