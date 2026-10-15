"""Two fresh natural P2 Sonya CPU contacts and ordinary continuations.
Original paired poses/offsets/health/fling/gravity/ready/flag-store contracts
unchanged, with every actual guest byte independently reconstructed. This is
not every CPU slot/move/victim/arena, raster/audio or whole-port acceptance.
"""
import json, re, sys, traceback
from pathlib import Path
import verify_native_friendship_palette_assembly_v2750 as assembly
import verify_current_physical_p2_cpu_v1916 as contract

ROOT=assembly.ROOT
OUT=ROOT/'audit_v2866_native_physical_p2_cpu_checked'
CASES={name:f'audit_v2864_native_sonya_p2_cpu_human_{name}' for name in ('kano','sonya')}
def verify():
    pins=assembly.source_check();guest,_,payload,_,_=assembly.expected()
    def pin(path,wanted=None):
        path=Path(path);path=path if path.is_absolute() else ROOT/path
        key=str(path.absolute());actual=assembly.sha(path)
        assembly.need(wanted is None or actual==wanted,'Immutable actual CPU dependency '+key)
        assembly.need(key not in pins or pins[key]==actual,'Consistent CPU dependency '+key);pins[key]=actual
    build_path=ROOT/assembly.NAME/'build-info.json';build=json.loads(build_path.read_text(encoding='utf-8-sig'));pin(build_path)
    pin(ROOT/assembly.NAME/'mkport_candidate.exe',build['executable_sha256'])
    pin(ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata',build['payload_sha256'])
    assembly.need((ROOT/assembly.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Actual native donor payload independently reconstructed')
    for file,wanted in build['input_hashes'].items():pin(file,wanted)
    runner=ROOT/'tools/run_native_physical_p2_cpu_v2863.ps1';old_runner=ROOT/'tools/run_current_physical_p2_cpu_v1913.ps1';pin(old_runner)
    expected=old_runner.read_text().replace('$root/mk2ks_cpu_recovery_probe_v1438.lua")',
        '$root/mk2ks_cpu_recovery_probe_v1438.lua","$root/mk2ks_native_cpu_guest_v2862.lua","$root/mk2/mk2-maincpu.bin")').replace(
        '-autoboot_script "$root/mk2ks_cpu_recovery_probe_v1438.lua"','-autoboot_script "$root/mk2ks_native_cpu_guest_v2862.lua"')
    assembly.need(expected.rstrip()==runner.read_text().rstrip(),'Entire actual CPU runner unchanged except read-only whole-guest observer/pins')
    accepted_path=ROOT/'audit_v1916_current_physical_p2_cpu_checked/report.json';accepted=json.loads(accepted_path.read_text());pin(accepted_path)
    assembly.need(accepted['passed'] and accepted['candidate']==assembly.prior.NAME,'Original physical-slot CPU baseline accepted')
    historical={str((Path(p) if Path(p).is_absolute() else ROOT/p).absolute()):h for p,h in accepted['inputHashes'].items()}
    cases={}
    for player,leaf in CASES.items():
        folder=ROOT/leaf;meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'))
        before=json.loads((folder/'input_hashes_before.json').read_text(encoding='utf-8-sig'))
        assembly.need(meta['exit_code']==0 and meta['candidate']==assembly.NAME and meta['player']==player and
            meta['boot_frame']==604 and meta['confirm_age']==264 and meta['approach']=='guard_until_close' and
            (meta['cpu_slot'],meta['human_slot'])==(2,1) and meta['assistance']=='none' and not meta['cheats_enabled'] and
            before==meta['input_hashes'],'Actual terminal natural selected human/native CPU fixture')
        assembly.need(meta['executable_sha256']==build['executable_sha256'] and meta['payload_sha256']==build['payload_sha256'] and
            all(before.get(p)==h for p,h in build['input_hashes'].items()),'Every actual CPU launch/compiled input pinned')
        for file,wanted in before.items():
            pin(file,wanted);path=Path(file)
            if path.suffix in ('.lua','.json','.ps1'):pin(folder/'input_sources'/path.name,wanted)
            if path.suffix=='.lua':
                assembly.need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',path.read_text()),
                              'Actual CPU driver never supplies ID/health/stage/position/RNG/AI/register state')
        assembly.need((folder/'guest_maincpu.bin').read_bytes()==guest,'Every actual CPU guest byte matches independent assembly')
        log=(folder/'run.log').read_text(encoding='utf-8-sig')
        assembly.need('MK2_NATIVE_CPU_GUEST bytes=1048576 writes=0 assistance=none' in log,'Actual whole-guest capture observer executed')
        result=contract.verify_log(log,player,guest)
        assembly.need(result['originalContract']['target']=='sonya' and result['originalContract']['CPU_slot']==2,
                      'Actual naturally selected true Sonya CPU owns the entire complete pair/ordinary continuation')
        old_path=ROOT/f'audit_v1914_current_sonya_p2_cpu_human_kano/run.log' if player=='kano' else ROOT/'audit_v1915_current_sonya_p2_cpu_human_sonya/run.log'
        pin(old_path,historical[str(old_path.absolute())]);old=old_path.read_text(encoding='utf-8-sig')
        events=lambda text:[line for line in text.splitlines() if line.startswith(('MK2_CPU_PAIR_','MK2_P2CPU_'))]
        result.update(case=leaf,wholeActualGuestReconstructed=True,exactCheckedBuildNativeChronology=events(log)==events(old))
        cases[player]=result
        for file in folder.rglob('*'):
            if file.is_file():pin(file)
        print(player+': complete original native Sonya CPU leg/ordinary handoffs and every floor/store passed',flush=True)
    for module in tuple(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file:
            path=Path(file).absolute()
            if path.is_relative_to(ROOT/'tools') and path.suffix=='.py':pin(path)
    return dict(passed=True,candidate=assembly.NAME,cases=cases,inputHashes=pins,originalTypedContractUnchanged=True,
                wholeActualGuestCapturedAndReconstructed=True,naturalCPUChoiceNotPrescribed=True,
                everyFloorAnchorAndNativeFlagStoreChecked=True,allCPUAccepted=False,fullRasterErasureAccepted=False,
                audioAccepted=False,fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    assembly.need(not OUT.exists(),'Immutable native CPU verification')
    try:report=verify()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','cases')},indent=2),flush=True)
    if report['passed']:
        print(json.dumps({p:{k:r['originalContract'].get(k) for k in ('start','release','complete','paired_fields','held_fields','damage','observed_cycles','own_handoff','victim_handoff','native_followup')}
              for p,r in report['cases'].items()},indent=2),flush=True)
    raise SystemExit(0 if report['passed'] else 1)
