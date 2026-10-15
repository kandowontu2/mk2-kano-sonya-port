"""Fresh original per-field interruption/retry and KO/next-round contracts.
Twenty cold unassisted native fixtures bound to the actual v2753 guest and
compiled inputs. No claim covers every move/interrupt point/victim/arena,
CPU/morph/overlap, whole raster erasure, audio, full campaign or final release.
"""
import hashlib, json, re, sys, traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_current_interrupt_and_ko_v824 as interrupt
import verify_current_lifecycle_v2 as lifecycle
import run_native_combat_dispatch_v2851 as dispatch

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2855_native_combat_regression_checked'

def verify():
    pins=assembly.source_check()
    def pin(path,wanted=None):
        path=Path(path)
        if not path.is_absolute():path=ROOT/path
        key=str(path.absolute());actual=assembly.sha(path)
        assembly.need(wanted is None or actual==wanted,'Immutable actual dependency '+key)
        assembly.need(key not in pins or pins[key]==actual,'Consistent actual dependency '+key);pins[key]=actual
    guest,prior,payload,_,_=assembly.expected()
    build_path=ROOT/assembly.NAME/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
    assembly.need(build['name']==assembly.NAME and hashlib.sha256(guest).hexdigest().upper()==build['expected_guest_sha256'],
                  'Whole candidate guest independently assembled')
    pin(ROOT/assembly.NAME/'mkport_candidate.exe',build['executable_sha256'])
    pin(ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
    assembly.need(hashlib.sha256(payload).hexdigest().upper()==build['payload_sha256'],'Independent unchanged donor payload')
    for file,wanted in build['input_hashes'].items():pin(file,wanted)
    frozen=ROOT/assembly.NAME/'input_sources/mame-mkp/src/mame/midway/midtunit_m.cpp'
    pin(frozen,assembly.SOURCE_SHA)
    ran_path=dispatch.OUT/'report.json';ran=json.loads(ran_path.read_text());pin(ran_path)
    assembly.need(ran['candidate']==assembly.NAME and ran['allRunnersTerminal'] and ran['allRunnerExitsZero'] and
                  len(ran['cases'])==len(dispatch.FIXTURES)==20,'All twenty actual runners terminal and inventory complete')
    pin(Path(dispatch.__file__),ran['sourceSHA256']);pin(dispatch.OUT/Path(dispatch.__file__).name,ran['sourceSHA256'])
    historical={}
    for leaf in ('audit_v1870_current_interrupt_checked','audit_v1872_current_ko_checked'):
        path=ROOT/leaf/'report.json';value=json.loads(path.read_text());pin(path)
        assembly.need(value['passed'] and value['candidate']==assembly.prior.NAME,'Checked-build original contract baseline')
        for file,wanted in value['inputHashes'].items():
            pathkey=Path(file);pathkey=pathkey if pathkey.is_absolute() else ROOT/pathkey
            historical[str(pathkey.absolute())]=wanted
    cases=[]
    for kind,move,side,victim in dispatch.FIXTURES:
        folder=ROOT/f'audit_v2853_{kind}_{move}_p{side}_{victim}'
        meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        assembly.need(meta['observer_passed'] and meta['exit_code']==0 and meta['candidate']==assembly.NAME and
                      (meta['kind'],meta['move'],meta['side'],meta['victim'])==(kind,move,side,victim) and
                      not meta['cheats'] and not meta['cheats_enabled'] and meta['guest_writes']==meta['emulator_resets']==0 and
                      not meta['saved_states_used'] and meta['assistance']==meta['memory_assistance']=='none',
                      'Actual unassisted completed native fixture '+folder.name)
        assembly.need(meta['executable_sha256']==meta['candidate_executable_sha256']==build['executable_sha256'] and
                      meta['payload_sha256']==build['payload_sha256'] and before==meta['input_hashes'] and
                      all(before.get(file)==wanted for file,wanted in build['input_hashes'].items()),
                      'Every actually executed compiled/launch input pinned before and after')
        driver=f'mk2ks_{move}_interrupt_v4.lua' if kind=='interrupt' else f'mk2ks_{move}_lifecycle_test.lua'
        required={driver,'mk2ks_native_combat_regression_v2849.lua','mk2ks_selector_exit_test.lua',
                  'mk2ks_native_shang_morph.lua','mk2ks_interrupt_trace_v3.lua','mk2ks_lifecycle_trace.lua'}
        assembly.need(required<={Path(file).name for file in before},'Every physical/transitive observer captured')
        for file,wanted in before.items():
            pin(file,wanted);path=Path(file)
            if path.suffix in ('.lua','.ps1','.json'):pin(folder/'input_sources'/path.name,wanted)
            if path.suffix=='.lua':
                assembly.need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|:reset\(',path.read_text()),
                              'No emulated state/register/health/ID injection or emulator resets')
        assembly.need((folder/'guest_maincpu.bin').read_bytes()==guest,'Whole actually executed guest matches independent assembly')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        assembly.need(not re.search(r'LUA ERROR|fatal error|access violation|stack traceback|WRONG CHECKSUMS',log,re.I),
                      'No actual runtime or observer errors')
        baseline=ROOT/(f'audit_v1869_interrupt_{move}_p{side}_{victim}' if kind=='interrupt' else f'audit_v1871_ko_{move}_p{side}_{victim}')/'run.log'
        assembly.need(str(baseline.absolute()) in historical,'Baseline source-bound to checked accepted contract')
        pin(baseline,historical[str(baseline.absolute())]);old=baseline.read_text(encoding='utf-8-sig')
        if kind=='interrupt':
            result=interrupt.verify_interrupt(log,move,side,victim)
            prefix='MK2_INTERRUPT_';field_prefix=prefix+'FIELD '
        else:
            result=lifecycle.verify(log,move,side,victim)
            assembly.need(result['passed'],'Entire unchanged original KO contract '+str(result['errors']))
            assembly.need(all(e['pc']==0xff835480 for e in lifecycle.rows(log,'EVENT') if e['kind']=='strike'),
                          'Actual original native collision descriptor reader')
            prefix='MK2_LIFE_TRACE_';field_prefix=prefix+'FIELD '
        actual_lines=[line for line in log.splitlines() if line.startswith(prefix)]
        old_lines=[line for line in old.splitlines() if line.startswith(prefix)]
        actual_fields=[line for line in actual_lines if line.startswith(field_prefix)]
        old_fields=[line for line in old_lines if line.startswith(field_prefix)]
        result.update(case=folder.name,kind=kind,wholeActualGuestReconstructed=True,
                      actualNativeTraceRecords=len(actual_lines),checkedBuildTraceRecords=len(old_lines),
                      exactCheckedBuildNativeTrace=actual_lines==old_lines,
                      exactCheckedBuildParticipantFields=actual_fields==old_fields,
                      fullPortAcceptance=False)
        cases.append(result)
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
        print(folder.name+' original full native identity/health/physics/effect/recovery contract passed',flush=True)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).absolute()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':pin(path)
    interruptions=[r for r in cases if r['kind']=='interrupt'];knockouts=[r for r in cases if r['kind']=='ko']
    assembly.need(len(interruptions)==len(knockouts)==10,'Complete both original native fixture matrices')
    return dict(passed=True,candidate=assembly.NAME,cases=cases,
                interruptionPairedFields=sum(r['pairedFields'] for r in interruptions),
                knockoutPairedFields=sum(r['actual_fields'] for r in knockouts),
                exactCheckedBuildParticipantCases=sum(r['exactCheckedBuildParticipantFields'] for r in cases),
                exactCheckedBuildNativeTraceCases=sum(r['exactCheckedBuildNativeTrace'] for r in cases),
                originalPerFieldAcceptanceUnchanged=True,wholeActualGuestCapturedAndReconstructedForEveryFixture=True,
                noEmulatedStateInjectionOrReset=True,allInterruptionsAccepted=False,allKOPathsAccepted=False,
                fullRasterErasureAccepted=False,audioAccepted=False,CPUAccepted=False,fullPortAcceptance=False,
                scope=__doc__,inputHashes=pins)

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable native combat verification')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','cases')},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
