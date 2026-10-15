"""Actual natural CPU Kano choke, full original read-only body/shadow RAM transport."""
import argparse,inspect,json,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import run_special_shadow_v5133 as original
ROOT,need,sha=current.ROOT,current.need,current.sha
LUA=ROOT/'mk2ks_cpu_choke_shadow_v5328.lua'

def collector():
 source=inspect.getsource(original.capture)
 start=source.index(" results=[dict(re.findall");end=source.index(" sheet=Image.new",start)
 old_tail=source[start:end]
 cpu_tail=""" results=[dict(re.findall(r'(\\w+)=([^\\s]+)',line))for line in log.splitlines()if line.startswith('MK2_CPU_PAIR_RESULT ')]
 need(len(results)==1 and int(results[0]['complete'])>0 and int(results[0]['follow_regain'])>0,'Actual complete native pair and follow-up, not activation only')
 need(len(scenes)>=5 and all(any(s['stage']==stage for s in scenes)for stage in('p1_cold_cpu_fight','cpu_pair_complete','cpu_followup_regain')),'Original before/paired/recovery native RGB transported')
 preview=[preview[i]for i in sorted(set((0,1,3,len(preview)//3,len(preview)//2,2*len(preview)//3,len(preview)-2,len(preview)-1)))if i<len(preview)]
"""
 changes={
  "audit_v5134_special_repeat_{move}_p{side}_{victim}":"audit_v5329_current_cpu_kano_choke_human_{victim}",
  "for p in(LUA,Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):":
   "for p in(LUA,ROOT/'mk2ks_special_shadow_v5131.lua',ROOT/'mk2ks_cpu_recovery_probe_v1438.lua',Path(original.__file__),Path(__file__),Path(native.__file__),build/'mkport_candidate.exe',build/'build-info.json',build/'roms/mk2ks/mk2ks.mdata'):",
  "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM=victim)":
   "env.update(MK2KS_TEST_FIGHTER=victim,MK2KS_TEST_BOOT_FRAME='605'if victim=='kano'else'606',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_PAIR_CONFIRM_AGE='264')",
  old_tail:cpu_tail,
  "bothPhysicalSpecialCyclesTransportPassed=True":"originalPhysicalCPUPairTransportPassed=True"}
 for before,after in changes.items():
  need(source.count(before)==1,'Single exact native collector adaptation: '+before[:75]);source=source.replace(before,after,1)
 namespace=dict(original.capture.__globals__,native=current,LUA=LUA,__file__=__file__,original=original)
 exec(compile(source,__file__+'::entire_RAM_only_native_collector','exec'),namespace)
 return namespace['capture']

def run(human):
 # Before execution, bind entire unchanged selected sources to actual earlier acceptance.
 body=json.loads((ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json').read_text())
 cpu=json.loads((ROOT/'audit_v2880_native_cpu_start_inventory_checked/report.json').read_text())
 need(body['passed']and cpu['passed'],'Original full body/shadow and actual CPU physical sources qualified')
 for name,proof in [('mk2ks_special_shadow_v5131.lua',body),('tools/run_special_shadow_v5133.py',body),('mk2ks_cpu_recovery_probe_v1438.lua',cpu)]:
  path=ROOT/name;need(sha(path)==proof['inputHashes'][str(path.resolve())],'Entire original source unchanged: '+name)
 report=collector()('choke',2,human)
 folder=ROOT/f'audit_v5329_current_cpu_kano_choke_human_{human}'
 need((folder/'stderr.log').read_text()=='','Native warning-free current build')
 for p in(ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json',ROOT/'audit_v2880_native_cpu_start_inventory_checked/report.json'):
  report['inputHashes'][str(p)]=sha(p)
 report.update(nativeStderrEmpty=True,actualCPUNotPrescribed=True,fullCPUChokeBodyShadowVerificationPending=True,
  observerOnlyAdaptation=True,physicalHumanSlot=1,actualCPUPhysicalSlot=2)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--human',choices=('kano','sonya'),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v5330_current_cpu_kano_choke_human_{a.human}_observed';need(not out.exists(),'Fresh immutable current CPU terminal')
 try:report=run(a.human)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualScenes')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
