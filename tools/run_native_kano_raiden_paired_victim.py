"""True Kano/Raiden native victim, clearing and ordinary paid reselect trial.

Original cold campaign first two opponents and controls stay unchanged. Only
ordinary attacks stop at Raiden until the actual target handoff; subsequent
native selection/recovery is observed, not assigned. No full-tower inference.
"""
import code
import inspect
import json
import re
import traceback
from pathlib import Path
import prepare_native_kano_paired_stumble_host_checked as prepared

ROOT, need, sha = prepared.ROOT, prepared.need, prepared.sha
OUT = ROOT / 'audit_native_kano_raiden_paired_victim_ram'
SOURCE = ROOT / 'audit_native_kano_raiden_paired_victim_source'
INIT = ROOT / 'audit_native_kano_raiden_paired_victim_initializer'
OLD_INIT = ROOT / 'audit_native_kano_raiden_paired_victim_previous_initializer'
LUA = 'mk2ks_native_kano_raiden_victim_provenance.lua'
NEW = (LUA, 'mk2ks_native_kano_raiden_victim_cache.lua', 'mk2ks_native_kano_raiden_victim_driver.lua')
CONTROLLERS = list(dict.fromkeys((*NEW, *prepared.previous.CONTROLLERS)))
RAM = {}


def once(source, before, after):
    need(source.count(before) == 1, 'Whole original boundary occurs exactly once: ' + before[:100])
    return source.replace(before, after, 1)


def functions(provider):
    factory = inspect.getsource(prepared.functions)
    factory = once(factory, 'scope = dict(vars(previous),__file__=__file__,OUT=OUT,RAM=RAM)',
                   'scope = dict(vars(previous),__file__=__file__,OUT=OUT,RAM=RAM,LUA=LUA,CONTROLLERS=CONTROLLERS)')
    namespace = dict(vars(prepared), __file__=__file__, OUT=OUT, RAM=RAM, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(factory, __file__ + '::whole_original_corrected_host_factory_new_controller_vector', 'exec'), namespace)
    scope, host = namespace['functions'](provider)
    host = once(host, "name.startswith('paired_stumble_victim_') or name.startswith('ending_page')",
                "name.startswith(('paired_stumble_victim_','kano_raiden_paired_')) or name.startswith('ending_page')")
    host = once(host, 'preview_seen.add(fields[\'sha256\']);images[name]=image;raw_images[name]=raw',
                'preview_seen.add(fields[\'sha256\']);images[name]=image;raw_images[name]=raw;need(len(images)<=64,\'Bounded original native RGB held only in RAM\')')
    host = once(host, "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_','MK2_PAIRED_STUMBLE_'))",
                "or line.startswith(('MK2_CAMPAIGN_HOST_DEADLINE ','MK2_CURRENT_CAMPAIGN_CACHE_','MK2_PAIRED_STUMBLE_','MK2_KANO_RAIDEN_VICTIM_READMITTED ','MK2_KANO_RAIDEN_VICTIM_COMPLETE ','MK2_KANO_RAIDEN_VICTIM_NO_HANDOFF '))")
    scope.update(__file__=__file__, OUT=OUT, LUA=LUA, CONTROLLERS=CONTROLLERS)
    exec(compile(host, __file__ + '::entire_original_native_capture_bounded_extra_phase_rasters', 'exec'), scope)
    return scope, host


def source_guard():
    need(not SOURCE.exists() and not OUT.exists() and not prepared.previous.census.census(),
         'One fresh actual victim trial, no existing native process')
    old = prepared.source_guard()
    prefix_path = ROOT / 'audit_native_kano_prefix_complete_move_inventory_checked/report.json'
    pit_path = ROOT / 'audit_native_pit_transition_matrix_checked/report.json'
    victim_path = ROOT / 'audit_native_paired_stumble_handoff_checked/report.json'
    prefix, pit, victim = (json.loads(path.read_text()) for path in (prefix_path, pit_path, victim_path))
    need(prefix['passed'] and prefix['finiteCurrentKanoFirstThreeLadderAdvancesAccepted'] and
         not prefix['KanoPairedVictimAccepted'] and pit['passed'] and
         pit['finiteBothCharactersBothSlotsOppositeVictimPitTransitionAccepted'] and
         victim['passed'] and victim['finiteNativeSonyaRaidenHandoffAccepted'] and
         not victim['KanoVictimRuntimeAccepted'], 'Actual outstanding Kano victim gap; no accepted case replay')
    pins = {}
    for proof in (old, prefix, pit, victim):
        need(not proof['fullPortAcceptance'], 'Finite prior evidence stays limited')
        for path, digest in proof['inputHashes'].items():
            need(sha(path) == digest and (path not in pins or pins[path] == digest), 'Frozen source/native input ' + path)
            pins[path] = digest
    for name in CONTROLLERS:
        text = (ROOT / name).read_text()
        need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat|return\s+data', text),
             'All loaded controller layers use normal buttons and passive observations only')
    driver, cache, provenance = ((ROOT / name).read_text() for name in (NEW[2], NEW[1], NEW[0]))
    need("not(stage==2 and other.roster==7 and not rawget(_G,\\'MK2KS_KANO_PAIRED_CALLBACK\\'))" in driver and
         'if age==56 then plan=route' in driver and 'losses>=8' in driver and 'frame-admitted>=500' in driver and
         'a.hp==161 and b.hp==161' in driver and 'kano_raiden_paired_frame%d.png' in driver and
         ':set_value(' not in driver and ':clear_value(' not in driver and ':snapshot(' not in driver,
         'Only original attack predicate/settled native cursor input planning; passive admission/loss limits')
    need('mk2ks_native_kano_laser_sonya_postending.lua' in cache and
         "dofile('mk2ks_native_kano_raiden_victim_driver.lua')" in cache and
         ':set_value(' not in cache and 'manager.machine:exit()' not in cache,
         'Whole existing native cache observer, one driver leaf only')
    need(provenance.count('once(') == 4 and "id==17 and p:read_u16(owner+0x1f0)==7" in provenance and
         'pending={frame=frame};MK2KS_KANO_PAIRED_CALLBACK=frame' in provenance and
         ':set_value(' not in provenance and ':clear_value(' not in provenance and
         'manager.machine:exit()' not in provenance,
         'All original paired native reads and four victim rasters, true Kano target and passive Lua signal only')
    metadata = json.loads((ROOT / prepared.previous.repaired.NAME / 'build-info.json').read_text(encoding='utf-8-sig'))
    provider = prepared.SimpleNamespace(GUEST_SHA=metadata['expected_guest_sha256'],
                                        EXE_SHA=metadata['executable_sha256'], PAYLOAD_SHA=metadata['payload_sha256'])
    _, host = functions(provider)
    need("MK2KS_TEST_FIGHTER='kano',MK2KS_CAMPAIGN_SIDE='1'" in host and
         "MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'" in host and "'-str','6000'" in host and
         "'-nocheat'" in host and "'-wavwrite','NUL'" in host and
         len(old['originalNaturalIntegrationRequirements']) == 14 and len(old['originalRemainingWorkGroups']) == 6,
         'Whole original compiled native host/deadline/guest proof, samples/NUL and full objective retained')
    for path in (Path(__file__).resolve(), Path(prepared.__file__), prefix_path, pit_path, victim_path,
                 prepared.SOURCE / 'report.json', *(ROOT / name for name in CONTROLLERS)):
        pins[str(path)] = sha(path)
    report = dict(passed=True, sourceOnlyAccepted=True, nativeGameplayAccepted=False,
                  physicalInputPolicy='Original first two earned opponents; no attacks against native Raiden until actual Kano handoff, then original controls resume. Cursor route reread before first physical direction.',
                  guestStateWrites=0, healthOrRNGAssistance=False, boundedRAMRasters=64,
                  originalObservationDeadlineSeconds=5900, realLossBoundWithoutHandoff=8,
                  postPaidReadmissionNativeFields=500, fullTowerAccepted=False, audioAccepted=False,
                  fullPortAcceptance=False, originalNaturalIntegrationRequirements=old['originalNaturalIntegrationRequirements'],
                  originalRemainingWorkGroups=old['originalRemainingWorkGroups'], inputHashes=pins,
                  newBuilds=0, newROMCopies=0, newRawMedia=0, newZIPs=0, goalStatus='active')
    SOURCE.mkdir()
    (SOURCE / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def run():
    need(not INIT.exists() and not OLD_INIT.exists(), 'Fresh whole independent initializer')
    guard = source_guard()
    repaired = prepared.previous.repaired
    namespace = dict(vars(repaired), __file__=__file__, INIT=INIT, OLD_INIT=OLD_INIT)
    exec(compile(inspect.getsource(repaired.expectation), __file__ + '::whole_original79_byte_independent_initializer', 'exec'), namespace)
    guest, gfx, build, provider = namespace['expectation']()
    scope, host = functions(provider)
    RAM.update(scope=scope, guest=guest, gfx=gfx, build=build, executedHost=host)
    captured = scope['capture']()
    RAM['capture'] = captured
    need(not prepared.previous.census.census() and all(sha(path) == digest for path, digest in guard['inputHashes'].items()),
         'Original native actually terminal; all executed controls and frozen prerequisites unchanged')
    return captured


if __name__ == '__main__':
    try:
        captured = run()
    except Exception as error:
        folder = OUT if OUT.exists() else (INIT if INIT.exists() else SOURCE)
        failure = dict(passed=False, error=repr(error)[:4096], traceback=traceback.format_exc(),
                       fullPortAcceptance=False, goalStatus='active')
        if folder.exists():
            path = folder / 'current_capture_failure.json'
            need(not path.exists(), 'Preserve actual original trial failure')
            path.write_text(json.dumps(failure, indent=2) + '\n')
        print(json.dumps(failure, indent=2), flush=True)
    code.interact(banner='Original Kano/Raiden victim trial; held buffers only in RAM, full goal remains open.', local=dict(RAM=RAM))
