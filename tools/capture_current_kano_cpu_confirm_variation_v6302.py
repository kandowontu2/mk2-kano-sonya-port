"""Bounded genuine selection-confirm timing variations; no RNG/state fixture.

Up to three actual current cold matches, stopping at the first knife/blade
choice. Different stock opponents are retained as scenario misses. Never
restart a live job or hide a semantic rejection under a different fixture.
"""
import gzip,inspect,json,re
from pathlib import Path
import capture_current_kano_cpu_extended_v6292 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha


def capture(age):
 need(age in(265,266,267),'Finite normal button-confirm timing variations only')
 source=inspect.getsource(prior.capture)
 before='changes={'
 need(source.count(before)==1,'Single explicit input timing override')
 source=source.replace(before,'changes={\n  "MK2KS_CPU_PAIR_CONFIRM_AGE=\'264\'":"MK2KS_CPU_PAIR_CONFIRM_AGE=\''+str(age)+'\'",',1)
 before='audit_v6293_current_kano_cpu_extended_ram'
 need(source.count(before)==1,'Fresh actual native capture, never overwrite old job')
 source=source.replace(before,f'audit_v6303_current_kano_cpu_confirm{age}_ram',1)
 before='Path(model.__file__).resolve(),'
 need(source.count(before)==1,'Retain entire executed original capture source')
 source=source.replace(before,'ROOT/"tools/capture_current_kano_cpu_extended_v6292.py",Path(model.__file__).resolve(),',1)
 namespace=dict(prior.capture.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::whole_current_collector_physical_confirm'+str(age),'exec'),namespace)
 return namespace['capture']()


def main():
 records=[]
 for age in(265,266,267):
  folder=ROOT/f'audit_v6303_current_kano_cpu_confirm{age}_ram'
  try:report=capture(age)
  except Exception:
   need((folder/'result.json').exists(),'Unexpected prelaunch/collector error; no substitute launch')
   report=json.loads((folder/'result.json').read_text())
   need(report['nativeExit']==0 and report['nativeIdentity'] and not prior.prior.process_tools.census(),
        'Same actual job naturally terminal before any new input variation')
   with gzip.open(folder/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
   cold=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_P2CPU_COLD_LIVE ')]
   need(len(cold)==1 and cold[0]['cpu_id']!='17','Do not hide actual Kano semantic failures by changing inputs')
   records.append(dict(confirmAge=age,folder=str(folder),nativeCPU=int(cold[0]['cpu_id']),scenarioAccepted=False))
   print(json.dumps(records[-1]),flush=True);continue
  choices=report['independentSemantics']['nativeChoices']
  records.append(dict(confirmAge=age,folder=str(folder),nativeCPU=17,choices=choices,movePhaseAcceptance=False))
  print(json.dumps(records[-1]),flush=True)
  if any(r['move']in('knife','blade')for r in choices):break
 print(json.dumps(dict(actualTerminalCases=records,fullPortAcceptance=False,newBuilds=0)),flush=True)


if __name__=='__main__':main()
