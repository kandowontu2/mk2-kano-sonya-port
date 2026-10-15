"""Actual native both-Down true mirror Tomb drop and complete paired RAM audio.

Entire4350 earned/action/audio/winner/DCS/finite-cleanup gates retained.
The separate4375 pressed branch is source/IO/task/phase qualified; existing
unpressed/RNG proofs are not altered or relabelled. No full-port acceptance.
"""
import hashlib,inspect,json,subprocess,traceback
from pathlib import Path
import run_tomb_mirror_audio_ram_v4350 as runtime
import verify_pressed_tomb_mirror_contract_v4375 as state
ROOT,need,sha=runtime.ROOT,runtime.need,runtime.sha
OUT=ROOT/'audit_v4384_pressed_kano_p1_tomb_mirror_audio_checked'

def collector():
    source=inspect.getsource(runtime.old.capture)
    changes={
      "audit_v4213_jax_arms_{fighter}_p{side}_audio_queue_{suffix}":"audit_v4383_pressed_tomb_mirror_{fighter}_p{side}_{suffix}",
      'mk2ks_jax_arms_audio_routes_ram_v4210.lua':'mk2ks_tomb_mirror_pressed_audio_ram_v4380.lua',
      'mk2ks_stock_extended_earned_ram_v3958.lua':'mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua',
      "ROOT/'mk2ks_stock_fatality_v1021.lua',ROOT/'mk2ks_arm_palette_trace_v1073.lua',\n        ROOT/'mk2ks_jax_arms_native_scene_ram_v4073.lua',ROOT/'mk2ks_jax_clap_audio_routes_ram_v4057.lua',\n        Path(state.old.__file__),Path(state.scene_state.__file__),":
        "ROOT/'mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua',ROOT/'mk2ks_tomb_mirror_audio_ram_v4342.lua',\n        ROOT/'mk2ks_tomb_mirror_provenance_ram_v4341.lua',ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',\n        ROOT/'mk2ks_current_stage_provenance_v3595.lua',ROOT/'mk2ks_jax_arms_audio_routes_ram_v4210.lua',\n        Path(runtime.__file__),Path(runtime.old.__file__),Path(state.old.__file__),Path(state.native.__file__),\n        Path(state.native.legacy.__file__),ROOT/'tools/verify_current_tomb_drop_physics_v3618.py',ROOT/'tools/verify_native_friendship_audio_v791.py',",
      "env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',\n        MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0',\n        MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='bbbb_lp',MK2KS_STOCK_GAP='96',\n        MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_OUT=str(folder))":
        "env.update(MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter,MK2KS_STAGE_ARENA='1',MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(folder))",
      "'-str','150'":"'-str','900'"}
    for before,after in changes.items():
        need(source.count(before)==1,'Exact entire RAM collector adaptation: '+before)
        source=source.replace(before,after)
    scope=dict(runtime.old.__dict__);scope.update(__file__=__file__,runtime=runtime,state=state)
    exec(compile(source,'<entire4212_collector_true_mirror_pressed_branch_4376>','exec'),scope)
    return scope['capture'],hashlib.sha256(source.encode()).hexdigest().upper()

pair_source=inspect.getsource(runtime.pair)
scope=dict(runtime.__dict__);scope.update(state=state)
exec(compile(pair_source,'<entire4350_pair_with_original1731_and_exact_pressed_branch>','exec'),scope)
pair=scope['pair']

def preflight():
    capture,digest=collector()
    need(pair_source==inspect.getsource(runtime.pair),'Entire original audio/delivery/winner/mix/channel-cleanup contract retained')
    need(state.contract_source==state.old.contract_source.replace(
      'qualify_drop(log,fighter,side,arena,case,guest)','qualify_pressed_drop(log,fighter,side,arena,case,guest)'),
      'All original complete1731 gates retained, only separate native pressed branch qualification')
    for name in ('mk2ks_tomb_mirror_pressed_provenance_ram_v4379.lua','mk2ks_tomb_mirror_pressed_audio_ram_v4380.lua'):
        text=(ROOT/name).read_text();need('set_value'not in text.replace("source:find('set_value(',1,true)",'')and ':write_u'not in text,
          'Read-only observer wrappers, no controls or game writes')
    driver=(ROOT/'mk2ks_tomb_mirror_pressed_driver_ram_v4372.lua').read_text()
    need("press(1,'Down');press(2,'Down')"in driver and 'frame-action>=32 and frame-action<64'in driver and
      'manager.machine:exit'not in driver and ':write_u'not in driver,'Only declared ordinary Down fields, original host exit unchanged')
    return capture,dict(collectorSHA256=digest,pairSHA256=hashlib.sha256(pair_source.encode()).hexdigest().upper(),
      fullEarnedPressedContractSHA256=state.CONTRACT_SHA256)

def main():
    need(not OUT.exists(),'Fresh immutable native pressed branch proof')
    capture,proof=preflight();guest=runtime.old.expected()
    print(json.dumps(dict(preflight=proof)),flush=True)
    case=pair('kano',1,guest,capture)
    text=(ROOT/case['capture']/'run.log').read_text()
    pressed=state.qualify_pressed_drop(text,'kano',1,1,'positive',guest)
    need(case['lateOwnedMirrorVictimScreams']==1,'Actual native pressed drop produces one owned mirror victim late scream')
    case['nativePressedBranch']=pressed;case['actualNativePhaseFaultsRejected']=state.pressed_phase_faults(text,'kano',1,guest)
    pins={str(Path(__file__).resolve()):sha(__file__)}
    for name in (case['capture'],case['baseline']):
        leaf=ROOT/name;meta=json.loads((leaf/'result.json').read_text())
        for p,h in meta['input_hashes'].items():need(p not in pins or pins[p]==h,'Consistent actual paired source bytes');pins[p]=h
        for p in leaf.rglob('*'):
            if p.is_file():pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every executed source/native text/result byte unchanged')
    return dict(passed=True,candidate=runtime.old.NAME,case=case,inputHashes=pins,sourcePreflight=proof,
      actualNativeBothDownMirrorDropContexts=1,allMirrorPressedDropSlotsAccepted=False,
      nativeDCSStageVictimFullWaveformAccepted=False,fullTombRasterAndFloorShadowAccepted=False,
      fullPortAcceptance=False,scope=__doc__)

if __name__=='__main__':
    try:report=main()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    need(not OUT.exists(),'Never overwrite native context/report');OUT.mkdir()
    need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k not in('case','inputHashes')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
