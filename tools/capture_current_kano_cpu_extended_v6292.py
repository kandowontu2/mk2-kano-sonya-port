"""One current native long match with qualified physical continuation.

Retain actual Baraka outcome, use current proven605 input timing, then native
Kano AI chooses freely. Same robust terminal-first RAM-only collector.
"""
import inspect,json
from pathlib import Path
import capture_current_cpu_knife_v6285 as prior
import current_kano_cpu_extended_contract_v6291 as model
ROOT,need,sha=prior.ROOT,prior.need,prior.sha


def capture():
 rejected=ROOT/'audit_v6288_current_native_cpu_knife_ram/result.json'
 r=json.loads(rejected.read_text());need(r['nativeExit']==0 and not r['passed'],'Retain actual natural different-CPU scenario')
 qualified=ROOT/'audit_v5325_current_cpu_bicycle_ram_checked/report.json';p=json.loads(qualified.read_text())
 need(p['passed'],'Original full physical extended continuation and native RNG source qualified')
 names=('mk2ks_physical_p2_cpu_continuation_v3300.lua','mk2ks_physical_p2_cpu_choice_trace_v3303.lua')
 for name in names:
  file=ROOT/name;need(sha(file)==p['inputHashes'][str(file)],'Entire qualified original extended control/observer unchanged')
 source=inspect.getsource(prior.capture)
 changes={
  "prior=json.loads(prior_path.read_text())":"prior=json.loads(prior_path.read_text());prior['inputHashes']={str(Path(k).resolve()):v for k,v in prior['inputHashes'].items()}",
  "MK2KS_TEST_BOOT_FRAME='960'":"MK2KS_TEST_BOOT_FRAME='605',MK2KS_CPU_CONTINUATION_POLICY='retreat'",
  'for p in (LUA,Path(__file__).resolve(),':'for p in (rejected,qualified,Path(prior_module.__file__).resolve(),Path(model.__file__).resolve(),*(ROOT/n for n in names),LUA,Path(__file__).resolve(),',
  "report['independentSemantics']=original.verify(text,guest)":"report['independentSemantics']=model.verify(text,guest);report['fullKnifeScenarioAcceptance']=report['independentSemantics']['originalKnifeScenario']['passed']",
 }
 for before,after in changes.items():
  need(source.count(before)==1,'Explicit finite current physical continuation context: '+before[:100]);source=source.replace(before,after,1)
 namespace=dict(prior.capture.__globals__,__file__=__file__,prior_module=prior,model=model,names=names,
                rejected=rejected,qualified=qualified,FOLDER=ROOT/'audit_v6293_current_kano_cpu_extended_ram',
                LUA=ROOT/'mk2ks_current_kano_cpu_extended_ram_v6290.lua')
 exec(compile(source,__file__+'::whole_original_terminal_first_collector_current_physical_long_match','exec'),namespace)
 return namespace['capture']()


if __name__=='__main__':capture()
