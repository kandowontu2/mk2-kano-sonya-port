"""60 isolated current native fixtures: full move matrix, UI, ground/shadows."""
import concurrent.futures,json,subprocess
from pathlib import Path
import verify_native_grab_audio_v1415 as source
ROOT=source.ROOT;NAME='diagnostic_v1473_sonya_launch_audio';OUT=ROOT/'audit_v1498_launch_audio_regression_dispatch'
MOVES=('knife','ball','blade','choke','ring','square','bicycle','leg')
MOVESPECS=[(m,s,None,False)for m in MOVES for s in(1,2)]+[('square',s,None,True)for s in(1,2)]+[(m,s,k,False)for m in MOVES for s in(1,2)for k in('block','miss')]+[('leg',s,'duck_block',False)for s in(1,2)]
PWSh=r'C:\Users\kando\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\powershell\pwsh.exe'

def fixtures():
 jobs=[]
 for move,side,scenario,air in MOVESPECS:
  suffix=move+('_air'if air else '_'+scenario if scenario else '')
  case=f'audit_v1499_human_{suffix}_p{side}'
  runner='tools/run_current_human_negative_v1240.ps1'if scenario else'tools/run_current_human_special_v820.ps1'
  params=['-Move',move,'-Side',str(side)]
  if scenario:params+=['-Scenario',scenario]
  if air:params+=['-Air']
  jobs.append((case,runner,params))
 for fighter in ('kano','sonya'):
  for side in(1,2):
   jobs.append((f'audit_v1500_ui_{fighter}_p{side}','tools/run_native_ui_flow_v813.ps1',['-Fighter',fighter,'-Side',str(side)]))
   jobs.append((f'audit_v1501_ground_shadow_{fighter}_p{side}','tools/run_ground_shadow_v815_probe.ps1',['-Fighter',fighter,'-Side',str(side)]))
 return jobs

def run(job):
 case,runner,params=job
 command=[PWSh,'-NoProfile','-File',str(ROOT/runner),'-CaseName',case,'-CandidateName',NAME]+params
 result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
 print(case+' runner exit='+str(result.returncode)+' '+result.stdout.strip()+' '+result.stderr.strip(),flush=True)
 return dict(case=case,runner=runner,runnerExit=result.returncode,stdout=result.stdout,stderr=result.stderr)

if __name__=='__main__':
 jobs=fixtures();assert len(jobs)==60 and not OUT.exists() and all(not(ROOT/c).exists()for c,r,p in jobs)
 OUT.mkdir();before=source.prior.digest(__file__);(OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:cases=list(pool.map(run,jobs))
 assert source.prior.digest(__file__)==before
 (OUT/'report.json').write_text(json.dumps(dict(candidate=NAME,cases=cases,sourceSHA256=before,allRunnersTerminal=True,allRunnerExitsZero=all(c['runnerExit']==0 for c in cases),independentVerificationPending=True,fullPortAccepted=False),indent=2)+'\n')
 raise SystemExit(0 if all(c['runnerExit']==0 for c in cases)else 1)
