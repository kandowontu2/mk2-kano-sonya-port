"""Two true current Kitana stock corner controls; six native panels, RAM only."""
import argparse,inspect,json,sys,traceback
from pathlib import Path
import run_jax_arms_stock_corner_v4091 as prior
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha

def run(side):
 prior.NAME=current.NAME
 prior.REVIEW=ROOT/f'audit_v6147_current_jax_arms_stock_kitana_p{side}_corner_ram/review'
 source=inspect.getsource(prior.run)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'One exact current stock provenance/storage adaptation')
  source=source.replace(before,after,1)
 replace('audit_v4092_jax_arms_stock_kitana_p{side}_corner_ram','audit_v6147_current_jax_arms_stock_kitana_p{side}_corner_ram')
 replace("'36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'",'(current.EXE_SHA)')
 replace("'91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24'",'(current.PAYLOAD_SHA)')
 replace("    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}",
         "    files.add(Path(prior.__file__).resolve())\n    for module in list(sys.modules.values()):\n        path=getattr(module,'__file__',None)\n        if path and Path(path).resolve().is_relative_to(ROOT/'tools'):files.add(Path(path).resolve())\n    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}")
 replace("    for p in files:\n        if p.suffix in('.py','.lua','.ps1'):\n            target=folder/'input_sources'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);need(sha(target)==pins[str(p)],'Exact original stock control hierarchy snapshot')",
         '    REVIEW.mkdir() # All original files pinned; no duplicate source tree.')
 replace("        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\\n');print(f'Actual stock KitanaP{side} corner control pid={process.pid}',flush=True)",
         "        query=\"Get-CimInstance Win32_Process -Filter 'ProcessId=\"+str(process.pid)+\"' | Select-Object ProcessId,Name,CreationDate,ExecutablePath,CommandLine | ConvertTo-Json -Compress\"\n        census=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)\n        wi=json.loads(census.stdout)if census.returncode==0 and census.stdout.strip()else None\n        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,actualWindowsIdentity=wi),indent=2)+'\\n')\n        print(f'Actual current stock KitanaP{side} corner PID={process.pid}',flush=True)")
 replace("    text=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()",
         "    (folder/'native_terminal.json').write_text(json.dumps(dict(pid=process.pid,nativeExit=code,actualWindowsIdentity=wi),indent=2)+'\\n')\n    need(wi and wi['ProcessId']==process.pid and wi['CreationDate']and wi['Name']=='mkport_candidate.exe'and Path(wi['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve()and str(folder)in wi['CommandLine'],'Actual native creation/executable/full-command terminal identity')\n    text=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()")
 scope=dict(prior.run.__globals__,current=current,sys=sys,prior=prior,__file__=__file__)
 exec(compile(source,__file__+'::whole_original_six_native_stock_control','exec'),scope)
 return scope['run'](side,current.expected())

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--side',type=int,choices=(1,2),required=True);a=p.parse_args()
 out=ROOT/f'audit_v6148_current_jax_arms_stock_kitana_p{a.side}_corner_observed';need(not out.exists(),'Fresh stock control report')
 try:report=run(a.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','frames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
