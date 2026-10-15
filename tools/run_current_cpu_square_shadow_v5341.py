"""Natural CPU Sonya Square, original physical chain with native RAM body/shadow observation."""
import inspect,json,re,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_current_cpu_choke_shadow_v5328 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_cpu_square_shadow_v5341.lua'
OUT=ROOT/'audit_v5343_current_cpu_sonya_square_observed'
CHAIN=('mk2ks_physical_p2_cpu_continuation_v1997.lua','mk2ks_physical_p2_cpu_round_trace_v1998.lua',
 'mk2ks_physical_p2_cpu_overlap_trace_v1999.lua','mk2ks_physical_p2_cpu_choice_trace_v2035.lua',
 'mk2ks_physical_p2_cpu_square_trace_v2038.lua','mk2ks_native_cpu_square_boundary_v2993.lua','mk2ks_native_cpu_square_locks_v3000.lua')
def run():
 current.expected()
 baseline_path=ROOT/'audit_v3282_current_cpu_square_render_erase_checked/report.json'
 baseline=json.loads(baseline_path.read_text());need(baseline['passed'],'Original actual natural CPU Square context accepted')
 paths=[*(ROOT/name for name in CHAIN),ROOT/'mk2ks_cpu_choke_shadow_v5328.lua',ROOT/'mk2ks_special_shadow_v5131.lua',
  LUA,Path(__file__),Path(original.__file__),baseline_path]
 for name in CHAIN:
  path=ROOT/name
  need(sha(path)==baseline['inputHashes'][str(path.resolve())],'Entire original physical/provenance source unchanged: '+name)
  need(not re.search(r':write_|write_u\d+|\.value\s*=(?!=)|load_?state|:reset\(',path.read_text()),'No injected CPU/state/health/RNG/position')
 pins={str(p.resolve()):sha(p)for p in paths}
 source=inspect.getsource(original.collector)
 changes={
  'audit_v5329_current_cpu_kano_choke_human_{victim}':'audit_v5342_current_cpu_sonya_square_human_{victim}',
  "env.update(MK2KS_TEST_FIGHTER=victim,MK2KS_TEST_BOOT_FRAME='605'if victim=='kano'else'606',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_PAIR_CONFIRM_AGE='264')":
   "env.update(MK2KS_TEST_FIGHTER=victim,MK2KS_TEST_BOOT_FRAME='613',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_PAIR_CONFIRM_AGE='264',MK2KS_CPU_CONTINUATION_POLICY='jump_guard')",
  "ROOT/'mk2ks_cpu_recovery_probe_v1438.lua',Path(original.__file__)":
   "ROOT/'mk2ks_cpu_recovery_probe_v1438.lua',*(ROOT/n for n in CHAIN),ROOT/'mk2ks_cpu_choke_shadow_v5328.lua',Path(original.__file__)"}
 for before,after in changes.items():
  need(source.count(before)==1,'Single exact collector adaptation: '+before[:100]);source=source.replace(before,after,1)
 namespace=dict(original.collector.__globals__,LUA=LUA,__file__=__file__,CHAIN=CHAIN)
 exec(compile(source,__file__+'::original_full_RAM_transport_collector','exec'),namespace)
 report=namespace['collector']()('square',2,'kano')
 folder=ROOT/'audit_v5342_current_cpu_sonya_square_human_kano'
 need((folder/'stderr.log').read_text()=='','Native warning-free current ROM metadata')
 log=(folder/'run.log').read_text()
 choices=[s for s in log.splitlines()if s.startswith('MK2_CPU_CHOICE_EVENT ')and 'kind=square 'in s]
 contacts=[s for s in log.splitlines()if s.startswith('MK2_SQUARE_BOUNDARY_EVENT ')and 'kind=hit_entry 'in s]
 need(len(choices)==len(contacts)==1,'Actual natural CPU Square and native hit branch, not activation alone')
 prefixes=('MK2_CPU_PAIR_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_CPU_CHOICE_','MK2_SQUARE_NATIVE_','MK2_P2CPU_','MK2_SQUARE_BOUNDARY_','MK2_SQUARE_LOCK_')
 old=ROOT/'audit_v3269_current_native_cpu_square_hit/run.log'
 actual=[s for s in log.splitlines()if s.startswith(prefixes)]
 prior=[s for s in old.read_text(encoding='utf-8-sig').splitlines()if s.startswith(prefixes)]
 trajectory=actual==prior
 for p,h in pins.items():need(sha(p)==h,'All selected source/evidence unchanged');report['inputHashes'][p]=h
 report['inputHashes'][str(old)]=sha(old)
 report.update(observerOnlyAdaptation=True,actualCPUNotPrescribed=True,actualCPUPhysicalSlot=2,actualHumanPhysicalSlot=1,
  actualNaturalSquareHits=1,originalWholePhysicalTrajectoryUnchanged=trajectory,actualPhysicalEvents=len(actual),
  previousPhysicalEvents=len(prior),nativeStderrEmpty=True,fullCPUPhaseBodyShadowVerificationPending=True,
  previousFileWritingDisplayObserverNotLoaded=True,currentFullEraseAcceptance=False,
  observationScope='Complete original physical/choice/entry/collision/lock chain; replace old file-writing display observer with native full body/shadow RAM observer. Full erase requires separate RAM proof.')
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable CPU Square capture')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
