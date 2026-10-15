"""Actual new binary, original physical inputs; RAM-only bounded regression.

This validates the native table-overread repair, not own shatter art/full port.
"""
import ast, hashlib, json, re, struct, subprocess, sys, traceback, types
from pathlib import Path
import run_current_p1_campaign_ram_v4772 as base
import run_kintaro_pressure_guard_long_campaign_v4439 as transport
import qualify_sonya_subzero_cache_trace_source_v4833 as old_source
import qualify_native_subzero_victim_offset_v4838 as cause
import qualify_native_subzero_offset_staged_source_v4845 as stage

ROOT, need, sha = transport.ROOT, transport.need, transport.sha
NAME = 'diagnostic_v4850_native_subzero_victim_offset'
LUA = 'mk2ks_sonya_subzero_offset_regression_v4851.lua'
PREFLIGHT = ROOT / 'audit_v4853_native_subzero_offset_regression_source/report.json'
FOLDER = ROOT / 'audit_v4854_sonya_native_subzero_offset_regression_ram'
OUT = ROOT / 'audit_v4855_sonya_native_subzero_offset_regression_observed'
EXE_SHA = '61D78B83EAB18AED229C60618037DFFF6577A0DBD4F248F6B9C719D927C4474F'
GUEST_SHA = '33018F4325B689210C8DA4FB329E28AFDB693EEAB7D5124875D8D05A3E56BEE7'
TRANSITIVE_LUA = tuple(dict.fromkeys((LUA, *old_source.TRANSITIVE_LUA)))

def expected():
    original = transport.expected()
    need(hashlib.sha256(original).hexdigest().upper() == '938D380B3E2CE8DF6A688E2DC64C576CC7A1E554AE341E7B42463129FA5CA821',
         'Independent full3836 initialized guest reconstruction')
    repaired = bytearray(original)
    need(repaired[cause.DEST:cause.DEST+64] == b'\xff'*64, 'Unused native storage')
    repaired[cause.DEST:cause.DEST+34] = original[cause.off(0xff8c27d0):cause.off(0xff8c27d0)+34]
    struct.pack_into('<2H', repaired, cause.DEST+34, 0, 0)
    struct.pack_into('<I', repaired, cause.off(0xff8c23a0), 0xff800000+cause.DEST*8)
    need(sum(a != b for a,b in zip(original,repaired)) == 39, 'Only qualified initialized table/operand bytes change')
    need(hashlib.sha256(repaired).hexdigest().upper() == GUEST_SHA, 'Independent qualified whole repaired guest')
    need(stage.source_gate(stage.SOURCE.read_text(), stage.BASE.read_text(), original) == GUEST_SHA,
         'Actual compiled initializer and independent RAM reconstruction agree')
    return repaired

def collector_source():
    text = base.collector_source()
    for before, after in (
        ('audit_v4775_{fighter}_current_p1_campaign_ram', 'audit_v4854_{fighter}_native_subzero_offset_regression_ram'),
        ("need(fighter in('kano','sonya'),'Only actual true17/18 player-one campaigns')",
         "need(fighter=='sonya','Exact native action0616 Sonya counterexample regression')"),
        ("sha(candidate/'mkport_candidate.exe')=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'",
         "sha(candidate/'mkport_candidate.exe')==EXE_SHA"),
    ):
        need(text.count(before) == 1, 'Unique complete original collector adaptation')
        text = text.replace(before, after, 1)
    ast.parse(text)
    return text

def source_boundary():
    old_source.source_boundary()
    original = (ROOT / 'mk2ks_sonya_subzero_cache_trace_ram_v4831.lua').read_text()
    text = (ROOT / LUA).read_text()
    old_source.previous.observer_readonly(text)
    changes = (
        ('-- Readonly root/cursor/group provenance; corrected native SP state name.',
         '-- Readonly regression of built native victim-offset fix; no guest assistance.'),
        ('frame>108270', 'frame>108600'),
        ("{0xff838a30,'cache_end'}", "{0xff838a30,'cache_end'},{0xff8c26b0,'shatter_body_lookup'}"),
        ('frame>=108270', 'frame>=108600'),
    )
    for before, after in changes:
        need(original.count(before) == 1, 'Exact prior observer anchor')
        original = original.replace(before, after, 1)
    first = text.index(' if frame>=108240 and frame<=108600 then\n')
    last = text.index(' if (bad_frame and frame>=bad_frame+2)', first)
    fields = text[first:last]
    need(text[:first] + text[last:] == original, 'Every prior read-only observer byte outside explicit field extension retained')
    need('p:read_u16(0x0106c810)' in fields and 'MK2_SUBZERO_REPAIR_FIELD' in fields and
         'writes=0 assistance=none' in fields, 'Read-only actual physical/native victim fields')
    code = collector_source()
    for token in ('raw==guest', 'Never persist encoded raster', "MK2KS_CAMPAIGN_SIDE='1'",
                  "MK2KS_TWO_PLAYER='0'", 'human_slot=1,cpu_slot=2', 'rawRasterFilesWritten=0', 'raw_audio_files_written=0'):
        need(token in code, 'Complete original RAM/physical transport retained')
    return dict(passed=True, readOnlyObserver=True, physicalInputsUnchanged=True,
                boundedStopFrame=108600, expectedGuestSHA256=GUEST_SHA, fullPortAcceptance=False)

def preflight():
    need(not PREFLIGHT.parent.exists(), 'Fresh regression source proof')
    positive = source_boundary(); expected()
    build_path = ROOT / NAME / 'build-info.json'
    build = json.loads(build_path.read_text(encoding='utf-8-sig'))
    need(build['executable_sha256'] == EXE_SHA and build['expected_guest_sha256'] == GUEST_SHA,
         'Actual consumed successful new build')
    restored = json.loads((ROOT/NAME/'restoration.json').read_text(encoding='utf-8-sig'))
    need(restored['passed'] and all(sha(p)==h for p,h in restored['restored_actual_preexisting_files'].items()),
         'Exact working checkout and historical executable restored')
    pins = dict(build['input_hashes'])
    for path in (build_path, ROOT/NAME/'mkport_candidate.exe', ROOT/NAME/'restoration.json',
                 Path(__file__).resolve(), ROOT/LUA, stage.OUT/'report.json', cause.OUT/'report.json'):
        pins[str(path.resolve())] = sha(path)
    for relative in TRANSITIVE_LUA:
        path = ROOT/relative; pins[str(path.resolve())] = sha(path)
    need(all(sha(p)==h for p,h in pins.items()), 'Every actual native compiled source and unchanged physical policy bound')
    PREFLIGHT.parent.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(PREFLIGHT.parent)],capture_output=True).returncode==0, 'Compressed before source proof')
    PREFLIGHT.write_text(json.dumps(dict(positive,inputHashes=pins),indent=2)+'\n')

def capture():
    proof = json.loads(PREFLIGHT.read_text())
    need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()), 'Preflight actual bytes before boot')
    source = types.SimpleNamespace(source_boundary=source_boundary, TRANSITIVE_LUA=TRANSITIVE_LUA)
    scope = dict(vars(transport), __file__=__file__, NAME=NAME, LUA=LUA, PREFLIGHT=PREFLIGHT,
                 source=source, expected=expected, EXE_SHA=EXE_SHA)
    exec(compile(collector_source(), __file__+'::original_native_RAM_collector', 'exec'), scope)
    return scope['capture']('sonya')

def main():
    need(not OUT.exists() and not FOLDER.exists(), 'Fresh actual native run, never restart an executed leaf')
    preflight()
    try:
        folder, headers, images = capture()
        log = (folder/'run.log').read_text()
        need('MK2_SUBZERO_CACHE_TRACE frame=' in log, 'Actual nonempty opcode trace')
        stop = re.findall(r'MK2_SUBZERO_CACHE_TRACE_STOP frame=(\d+) first_bad=(-?\d+) records=(\d+)', log)
        need(stop == [('108600','-1',stop[0][2])] and int(stop[0][2]) > 1, 'Actual normal bounded stop; no global-cache write')
        meta = json.loads((folder/'result.json').read_text())
        need(meta['exit_code']==0 and meta['ramGuestSHA256']==GUEST_SHA and meta['nativeGuestBytesVerifiedInRAM']==1048576,
             'Actual successful new native whole-byte guest transport')
        need('MK2_MILEENA_CAMPAIGN_OVERRUN ' not in log, 'No original group cache writes into physical globals')
        rows = [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in log.splitlines()
                if line.startswith('MK2_SUBZERO_CACHE_TRACE ')]
        at = [r for r in rows if r['frame']=='108255' and r['action']=='0616']
        entry = next(r for r in at if r['kind']=='main_lookup')
        need(entry['id']==entry['roster']=='18' and entry['health']=='0,105' and entry['cpu_roster']=='8' and
             entry['a0']=='00000000' and entry['a1']=='FFFD4620', 'Same genuine native victim context now reads dedicated zero offset')
        cache = next(r for r in at if r['kind']=='cache_begin')
        need(cache['a0']=='FF0320C0' and cache['a9']=='FF0248F0', 'Actual own Sonya dizzy group replaces invalid FFFFFFFF')
        need(any(r['kind']=='shatter_body_lookup' and r['action']=='0616' for r in rows),
             'Native victim task actually advances to later shatter-body lookup')
        pins = dict(meta['input_hashes'])
        for path in folder.rglob('*'):
            if path.is_file(): pins[str(path.resolve())]=sha(path)
        pins[str(PREFLIGHT.resolve())]=sha(PREFLIGHT)
        need(all(sha(p)==h for p,h in pins.items()), 'Actual executed native regression evidence unchanged')
        report = dict(passed=True, candidate=NAME, actualNativeExit=0, actualStopFrame=108600,
            originalDefectFrame=108255, actualTraceRows=len(rows), actualRGBFrames=len(headers),
            initializedGuestEveryByteComparedInRAM=True, ownSonyaDizzyGroupObserved=True,
            nativeVictimTaskAdvances=True, nativeGlobalCacheOverrunRows=0,
            ownShatterBodyArtAccepted=False, fullPortAcceptance=False, publicBuildPromoted=False,
            rawMediaGuestFilesWritten=0, inputHashes=pins)
    except Exception as error:
        report = dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                      fullPortAcceptance=False,publicBuildPromoted=False)
    OUT.mkdir(); need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compressed before terminal proof')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

if __name__=='__main__':
    main()
