"""Real cold inputs: repeated CPU, voice channels, interruptions and full matrix."""
import concurrent.futures,json,subprocess
from pathlib import Path
import run_launch_audio_regression_v1498 as matrix
ROOT=matrix.ROOT;NAME='diagnostic_v1517_active_launch_timer'
OUT=ROOT/'audit_v1518_active_launch_timer_dispatch'
def fixtures():
 jobs=[('audit_v1519_cpu_repeated_p1_human_kano','tools/run_current_cpu_pair_display_v1459.ps1',['-Player','kano','-BootFrame','605'])]
 for name,runner,player,boot in [
  ('p2_human_kano','1438','kano',604),('p2_human_sonya','1438','sonya',604),('p1_human_sonya','1399','sonya',605)]:
  jobs.append(('audit_v1519_cpu_'+name,'tools/run_current_cpu_pair_display_v'+runner+'.ps1',['-Player',player,'-BootFrame',str(boot)]))
 for move in ('square','bicycle'):
  for side in (1,2):
   params=['-Move',move,'-Side',str(side)]
   jobs.append((f'audit_v1519_channels_{move}_p{side}','tools/run_sonya_launch_channels_v1483.ps1',params))
   # Wider original Baraka uppercut is a genuine physical P2-square attempt,
   # not acceptance unless an incoming native damage store actually occurs.
   opponent='baraka' if (move,side)==('square',2) else 'sub_zero'
   jobs.append((f'audit_v1519_interruption_{move}_p{side}','tools/run_sonya_launch_interruption_v1510.ps1',params+['-Victim',opponent]))
 for case,runner,params in matrix.fixtures():
  case=case.replace('audit_v1499_human','audit_v1519_human').replace('audit_v1500_ui','audit_v1519_ui').replace('audit_v1501_ground_shadow','audit_v1519_ground_shadow')
  jobs.append((case,runner,params))
 return jobs
def run(job):
 case,runner,params=job
 r=subprocess.run([matrix.PWSh,'-NoProfile','-File',str(ROOT/runner),'-CaseName',case,'-CandidateName',NAME]+params,cwd=ROOT,capture_output=True,text=True)
 print(case+' terminal runner='+str(r.returncode)+' '+r.stdout.strip()+' '+r.stderr.strip(),flush=True)
 return dict(case=case,runner=runner,runnerExit=r.returncode,stdout=r.stdout,stderr=r.stderr)
if __name__=='__main__':
 jobs=fixtures();assert len(jobs)==72 and not OUT.exists() and all(not(ROOT/c).exists()for c,r,p in jobs)
 OUT.mkdir();before=matrix.source.prior.digest(__file__)
 (OUT/Path(__file__).name).write_bytes(Path(__file__).read_bytes())
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:cases=list(pool.map(run,jobs))
 assert matrix.source.prior.digest(__file__)==before
 (OUT/'report.json').write_text(json.dumps(dict(candidate=NAME,cases=cases,sourceSHA256=before,allRunnersTerminal=True,allRunnerExitsZero=all(c['runnerExit']==0 for c in cases),independentVerificationPending=True,fullPortAccepted=False),indent=2)+'\n')
 raise SystemExit(0 if all(c['runnerExit']==0 for c in cases)else 1)
