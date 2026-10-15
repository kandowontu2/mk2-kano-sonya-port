"""Required native replay of the real failing campaign on the table repair.

All prior physical inputs/limits remain intact. New taps and four RAM-only
victim rasters observe the handoff, not alter it. Terminal transport alone is
not full-campaign, artwork, sound or whole-port acceptance.
"""
import code
import hashlib
import inspect
import json
import re
import struct
import traceback
from pathlib import Path
from types import SimpleNamespace

import capture_native_sonya_raiden_cache_cause as cause

base = cause.prior.prior.prior
ROOT, need, sha = base.ROOT, base.need, base.sha
NAME = 'diagnostic_native_paired_stumble_table_ps7'
OUT = ROOT / 'audit_native_paired_stumble_campaign'
OLD_INIT = ROOT / 'audit_native_paired_stumble_campaign_previous_initializer'
INIT = ROOT / 'audit_native_paired_stumble_campaign_initializer'
SOURCE = ROOT / 'audit_native_paired_stumble_campaign_source'
LUA = 'mk2ks_native_paired_stumble_campaign.lua'
CONTROLLERS = [LUA, *cause.prior.CONTROLLERS]
GUARD = ROOT / 'audit_native_paired_stumble_table_bounded_source/report.json'
RAM = {}


def expectation():
    need(not OLD_INIT.exists() and not INIT.exists(), 'Fresh independent full source initializer')
    scope = dict(vars(base), __file__=__file__, INIT=OLD_INIT)
    exec(compile(inspect.getsource(base.expectation), __file__ + '::whole_original_source_initializer', 'exec'), scope)
    previous, gfx, original, _ = scope['expectation']()
    guard = json.loads(GUARD.read_text())
    guest = bytearray(previous)
    at = (0xff875bd0 - 0xff800000) // 8
    need(guest[(0xff8752a0 - 0xff800000) // 8: (0xff8752a0 - 0xff800000) // 8 + 4] == struct.pack('<I', 0xff875bd0) and
         all(v == 255 for v in guest[0xfd7a0:0xfd7f0]), 'Actual old operand and unused independent source storage')
    guest[0xfd7a0:0xfd7a0 + 68] = previous[at:at + 68]
    struct.pack_into('<II', guest, 0xfd7a0 + 68, 0x2303bce0, 0x2303bce0)
    struct.pack_into('<I', guest, (0xff8752a0 - 0xff800000) // 8, 0xfffebd00)
    build = json.loads((ROOT / NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    actual_sha = hashlib.sha256(guest).hexdigest().upper()
    need(actual_sha == guard['proposedGuestSHA256'] == build['expected_guest_sha256'] and
         original['payload_sha256'] == build['payload_sha256'] and
         sha(ROOT / NAME / 'mkport_candidate.exe') == build['executable_sha256'] and
         all(sha(p) == h for p, h in build['input_hashes'].items()), 'Actual new executable and full independent guest')
    for name, digest in guard['stagedSourceHashes'].items():
        need(sha(ROOT / NAME / 'input_sources/mame-mkp/src/mame/midway' / name) == digest,
             'Actual compiled source equals whole qualified repair')
    provider = SimpleNamespace(ROOT=ROOT, NAME=NAME, EXE_SHA=build['executable_sha256'],
        GUEST_SHA=actual_sha, PAYLOAD_SHA=build['payload_sha256'], __file__=__file__,
        expected=lambda: bytes(guest), expected_gfx=lambda: gfx)
    INIT.mkdir()
    (INIT / 'report.json').write_text(json.dumps(dict(passed=True, sourceOnlyAccepted=True,
        wholeExpectedGuestSHA256=actual_sha, wholeExpectedGuestBytes=len(guest),
        entireOldInitializerRetained=True, initializedGuestByteDelta=79,
        inputHashes={str(Path(__file__).resolve()): sha(__file__), str(GUARD): sha(GUARD),
                     str(ROOT / NAME / 'build-info.json'): sha(ROOT / NAME / 'build-info.json')},
        nativeGameplayAccepted=False, fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
    return bytes(guest), gfx, build, provider


def source_guard():
    need(not SOURCE.exists(), 'Fresh immutable physical-input/passive source proof')
    guard = json.loads(GUARD.read_text())
    retirement = ROOT / 'audit_native_sonya_raiden_cache_cause_retirement/report.json'
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeRuntimeAccepted'] and
         json.loads(retirement.read_text())['passed'] and
         all(sha(p) == h for p, h in guard['inputHashes'].items()), 'Failed original retired and complete repair source intact')
    for name in CONTROLLERS:
        text = (ROOT / name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data', text),
             'Every transitive controller uses only physical inputs and passive observers')
    observer = (ROOT / LUA).read_text()
    need(observer.count("dofile('mk2ks_native_kano_laser_sonya_postending_leg_guard_late.lua')") == 1 and
         ':set_value(' not in observer and ':clear_value(' not in observer and
         'manager.machine:exit()' not in observer and 'assert(#taps==3' in observer,
         'Three passive native helper reads and four native raster observations only')
    SOURCE.mkdir()
    paths = [Path(__file__), GUARD, retirement, *[ROOT / n for n in CONTROLLERS]]
    (SOURCE / 'report.json').write_text(json.dumps(dict(passed=True, sourceOnlyAccepted=True,
        wholePreviousPhysicalPolicyByteIdentical=True, originalObservationDeadlineSeconds=18000,
        passiveHandoffReadLocations=3, newNativeVictimRasterObservations=4,
        inputHashes={str(p.resolve()): sha(p) for p in paths},
        originalNaturalIntegrationRequirements=guard['originalNaturalIntegrationRequirements'],
        originalRemainingWorkGroups=guard['originalRemainingWorkGroups'],
        nativeGameplayAccepted=False, fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')


def run():
    need(not OUT.exists() and not base.census.census() and not (ROOT / 'mame-mkp/build/mingw-gcc').exists(),
         'One fresh required native replay after actual compiler terminal/cache retirement')
    source_guard()
    guest, gfx, build, provider = expectation()
    scope, host = base.functions(provider)
    old = "name.startswith('ending_page') or name.startswith('postjoin_')"
    new = "name.startswith('paired_stumble_victim_') or " + old
    need(host.count(old) == 1, 'Exact critical RAM retention addition, not changed game inputs')
    host = host.replace(old, new)
    old = "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_'))"
    new = "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_','MK2_PAIRED_STUMBLE_'))"
    need(host.count(old) == 1, 'Live actual native handoff observation added to unchanged complete chronology')
    host = host.replace(old, new)
    scope.update(__file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(host, __file__ + '::whole_original_physical_host_plus_passive_handoffs', 'exec'), scope)
    RAM.update(scope=scope, guest=guest, gfx=gfx, build=build, executedHost=host)
    captured = scope['capture']()
    RAM['capture'] = captured
    return captured


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        if folder.exists():
            path = folder / 'current_capture_failure.json'
            need(not path.exists(), 'Never overwrite original actual failure')
            path.write_text(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc(),
                fullPortAcceptance=False, goalStatus='active'), indent=2) + '\n')
        print(json.dumps(dict(passed=False, error=repr(error), traceback=traceback.format_exc())), flush=True)
    code.interact(banner='Same actual repaired paired-victim campaign; full goal remains open.', local=dict(RAM=RAM))
