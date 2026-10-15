"""Source-bound inventory of sixteen physical-start CPU fixtures on v2753.

Cold selection, actual whole guest, six unmodified-derived orders, ownership,
floors and store opcodes are checked for each terminal fixture. Completed CPU
pairs are accepted ONLY by the unchanged original typed v1941/v1916 contracts.
Unexpected opponents are scenario misses. Rejected follow-ups remain rejected,
not relabeled or counted as gameplay passes. This is not all CPU acceptance.
"""
import hashlib
import json
import re
import struct
import sys
import traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_current_kano_physical_p2_cpu_v1941 as kano_contract
import verify_current_physical_p2_cpu_v1916 as sonya_contract
import run_native_cpu_start_sweep_v2871 as first_dispatch
import run_native_cpu_adjacent_start_v2874 as second_dispatch

ROOT = assembly.ROOT
OUT = ROOT / 'audit_v2878_native_cpu_start_inventory_checked'
MODEL = kano_contract.original


def typed_pair(log, player, guest, target):
    assembly.need(target in (17, 18), 'Only actual Kano/Sonya native CPU contact contracts')
    model = kano_contract if target == 17 else sonya_contract
    return model.verify_log(log, player, guest)


def inventory():
    pins = assembly.source_check()

    def pin(path, wanted=None):
        path = Path(path)
        path = path if path.is_absolute() else ROOT / path
        key = str(path.absolute())
        actual = assembly.sha(path)
        assembly.need(wanted is None or actual == wanted, 'Immutable CPU fixture dependency ' + key)
        assembly.need(key not in pins or pins[key] == actual, 'Consistent CPU dependency ' + key)
        pins[key] = actual

    guest, _, payload, _, _ = assembly.expected()
    build_path = ROOT / assembly.NAME / 'build-info.json'
    build = json.loads(build_path.read_text(encoding='utf-8-sig'))
    pin(build_path)
    assembly.need(build['name'] == assembly.NAME and hashlib.sha256(guest).hexdigest().upper() == build['expected_guest_sha256'],
                  'Whole compiled guest independently reconstructed')
    pin(ROOT / assembly.NAME / 'mkport_candidate.exe', build['executable_sha256'])
    pin(ROOT / assembly.NAME / 'roms/mk2ks/mk2ks.mdata', build['payload_sha256'])
    assembly.need((ROOT / assembly.NAME / 'roms/mk2ks/mk2ks.mdata').read_bytes() == payload,
                  'Entire unchanged native donor payload')
    for file, wanted in build['input_hashes'].items():
        pin(file, wanted)
    pin(ROOT / assembly.NAME / 'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp', assembly.SOURCE_SHA)

    runner = ROOT / 'tools/run_native_physical_p2_cpu_v2863.ps1'
    old_runner = ROOT / 'tools/run_current_physical_p2_cpu_v1913.ps1'
    expected_runner = old_runner.read_text().replace('$root/mk2ks_cpu_recovery_probe_v1438.lua")',
        '$root/mk2ks_cpu_recovery_probe_v1438.lua","$root/mk2ks_native_cpu_guest_v2862.lua","$root/mk2/mk2-maincpu.bin")').replace(
        '-autoboot_script "$root/mk2ks_cpu_recovery_probe_v1438.lua"', '-autoboot_script "$root/mk2ks_native_cpu_guest_v2862.lua"')
    assembly.need(runner.read_text().rstrip() == expected_runner.rstrip(),
                  'Entire physical driver runner unchanged except read-only guest observer and pins')
    pin(runner)
    pin(old_runner)
    cases = []
    orders = MODEL.expected_orders()
    for dispatch, version in ((first_dispatch, 2873), (second_dispatch, 2876)):
        ran_path = dispatch.OUT / 'report.json'
        ran = json.loads(ran_path.read_text())
        pin(ran_path)
        assembly.need(ran['candidate'] == assembly.NAME and ran['allRunnersTerminal'] and ran['allRunnerExitsZero'] and
                      len(ran['cases']) == len(dispatch.CASES) == 8 and not ran['CPUChoicesPrescribed'] and
                      ran['naturalCoinStartAndSelectionInputsOnly'], 'Entire actual eight-case physical input dispatch completed')
        pin(dispatch.__file__, ran['sourceSHA256'])
        pin(dispatch.OUT / Path(dispatch.__file__).name, ran['sourceSHA256'])
        assembly.need([(r['player'], r['bootFrame']) for r in ran['cases']] == dispatch.CASES,
                      'Every declared physical start timing has its actual terminal launch')
        for player, boot in dispatch.CASES:
            folder = ROOT / f'audit_v{version}_native_cpu_human_{player}_boot{boot}'
            meta = json.loads((folder / 'result.json').read_text(encoding='utf-8-sig'))
            before = json.loads((folder / 'input_hashes_before.json').read_text(encoding='utf-8-sig'))
            assembly.need(meta['exit_code'] == 0 and meta['candidate'] == assembly.NAME and meta['player'] == player and
                          meta['boot_frame'] == boot and meta['confirm_age'] == 264 and meta['approach'] == 'guard_until_close' and
                          (meta['cpu_slot'], meta['human_slot']) == (2, 1) and meta['assistance'] == 'none' and
                          not meta['cheats_enabled'] and before == meta['input_hashes'], 'Actual natural terminal physical input fixture')
            assembly.need(meta['executable_sha256'] == build['executable_sha256'] and meta['payload_sha256'] == build['payload_sha256'] and
                          all(before.get(file) == wanted for file, wanted in build['input_hashes'].items()),
                          'All actual matched compiled and launch dependencies captured')
            assembly.need({'mk2ks_cpu_recovery_probe_v1438.lua', 'mk2ks_native_cpu_guest_v2862.lua',
                           'run_native_physical_p2_cpu_v2863.ps1', 'mk2-maincpu.bin'} <= {Path(file).name for file in before},
                          'Original input/CPU observer and entire guest/source capture dependencies required')
            for file, wanted in before.items():
                pin(file, wanted)
                path = Path(file)
                if path.suffix in ('.lua', '.ps1', '.json'):
                    pin(folder / 'input_sources' / path.name, wanted)
                if path.suffix == '.lua':
                    assembly.need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(', path.read_text()),
                                  'Inputs only; no guest ID, health, position, AI, stage, RNG, register or state injection')
            assembly.need((folder / 'guest_maincpu.bin').read_bytes() == guest, 'Entire actually executed guest equals independent assembly')
            log = (folder / 'run.log').read_text(encoding='utf-8-sig')
            assembly.need('MK2_NATIVE_CPU_GUEST bytes=1048576 writes=0 assistance=none' in log and
                          not re.search(r'LUA ERROR|fatal error|access violation|stack traceback|WRONG CHECKSUMS', log, re.I),
                          'Actual observer ran without emulator or Lua errors')
            cold = MODEL.rows_prefix(log, 'MK2_P2CPU_COLD_LIVE ')
            selection = MODEL.rows_prefix(log, 'MK2_P2CPU_SELECT_RESULT ')
            assembly.need(len(cold) == len(selection) == 1, 'One genuine cold selection and native live match')
            c, s = cold[0], selection[0]
            assembly.need(s['human'] == c['human'] == player and s['human_id'] == c['human_id'] == MODEL.HUMANS[player] and
                          700 < s['css'] < s['exit'] < s['live'] == c['frame'] and s['checks'] == 50 and s['errors'] == 0 and
                          s['initial_cpu'] == c['cpu_id'] and c['stage'] == 0 and
                          s['writes'] == c['writes'] == 0 and s['assistance'] == c['assistance'] == 'none',
                          'Real new human identity survives selection teardown into a naturally chosen native CPU match')
            order = (c['schedule'] - 0xfffa3000) // 0x180
            assembly.need(order in range(6) and c['schedule'] == 0xfffa3000 + order * 0x180 and c['cpu_id'] == orders[order][0],
                          'Actual random choice follows original-derived stage-zero tower')
            roms = MODEL.rows(log, 'ROM')
            assembly.need(len(roms) == 6 and [r['order'] for r in roms] == list(range(6)) and
                          all(r['table'] == 0xfffa2c00 and r['list'] == 0xfffa3000 + i * 0x180 and
                              tuple(map(int, r['ids'].split(','))) == orders[i] and r['writes'] == 0 and
                              r['assistance'] == 'none' for i, r in enumerate(roms)),
                          'All six original-derived native extended ladders captured, not prescribed')
            fields = MODEL.rows(log, 'FIELD')
            flags = MODEL.flag_rows(log)
            for r in fields:
                assembly.need(r['id'] == r['roster'] == c['cpu_id'] and r['vid'] == r['vroster'] == MODEL.HUMANS[player] and
                              r['state'] == 0 and r['vstate'] == 1 and r['owner'] == r['actor'] and r['vowner'] == r['vactor'] and
                              (r['cpu_slot'], r['human_slot']) == (2, 1) and r['writes'] == 0 and r['assistance'] == 'none',
                              'Every recorded CPU field retains actual physical roles, identities and Main ownership')
                assembly.need(r['id'] in (17, 18) and r['floor'] == r['stage_floor'] - (134 if r['id'] == 17 else 135) and
                              r['vfloor'] == r['stage_floor'] - (134 if player == 'kano' else 135),
                              'Every actual new CPU/human floor anchor')
            for r in flags:
                offset = (r['pc'] - 32 - 0xff800000) // 8
                assembly.need(0 <= offset <= len(guest) - 4 and struct.unpack_from('<HH', guest, offset) == (r['op0'], r['op1']),
                              'Every observed physical flag/action/body store matches the actual independently assembled native code')
                assembly.need(r['at'] == (r['actor'] + 0x160 if r['kind'] == 'body' else r['main'] + (0x1f0 if r['kind'] == 'action' else 0x210)),
                              'Every observed store targets its real current actor/Main')
            original = MODEL.verify_log(log, player)
            if c['cpu_id'] not in (17, 18):
                assembly.need(not fields and not original['passed'], 'Stock-opponent timing is a scenario miss, not a new CPU proof')
                status, typed = 'scenario_miss', None
            elif original['passed']:
                typed = typed_pair(log, player, guest, c['cpu_id'])
                status = 'accepted_original_pair_and_ordinary_followup'
            else:
                status, typed = 'original_contract_rejected', None
            result = dict(case=folder.name, player=player, bootFrame=boot, actualCPU=c['cpu_id'],
                          actualNativeOrder=order, actualColdSelection=selection[0], status=status,
                          originalContract=original, typedContract=typed, allRecordedFields=len(fields),
                          sourceBoundStores=len(flags), wholeActualGuestReconstructed=True,
                          floorAnchorsChecked=True, noGuestStateInjection=True, allCPUAccepted=False)
            cases.append(result)
            for file in folder.rglob('*'):
                if file.is_file():
                    pin(file)
            print(folder.name + ': CPU=' + str(c['cpu_id']) + ' ' + status, flush=True)
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file:
            path = Path(file).absolute()
            if path.is_relative_to(ROOT / 'tools') and path.suffix == '.py':
                pin(path)
    accepted = [r for r in cases if r['status'] == 'accepted_original_pair_and_ordinary_followup']
    assembly.need(len(cases) == 16 and accepted, 'All sixteen actual fixtures inventoried and at least one unchanged native CPU pair accepted')
    return dict(passed=True, diagnosticInventoryOnly=True, candidate=assembly.NAME, cases=cases,
                acceptedPairFixtures=len(accepted), scenarioMisses=sum(r['status'] == 'scenario_miss' for r in cases),
                originalContractRejectedFixtures=sum(r['status'] == 'original_contract_rejected' for r in cases),
                allFixturesGameplayAccepted=False, allCPUAccepted=False, fullRasterErasureAccepted=False,
                audioAccepted=False, fullPortAcceptance=False, publicPromotionAccepted=False,
                originalTypedContractsUnchanged=True, scope=__doc__, inputHashes=pins)


if __name__ == '__main__':
    assembly.need(not OUT.exists(), 'Immutable native CPU inventory')
    try:
        result = inventory()
    except Exception as error:
        result = dict(passed=False, error=repr(error), traceback=traceback.format_exc(), fullPortAcceptance=False)
    OUT.mkdir()
    (OUT / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('inputHashes', 'cases')}, indent=2), flush=True)
    raise SystemExit(0 if result['passed'] else 1)
