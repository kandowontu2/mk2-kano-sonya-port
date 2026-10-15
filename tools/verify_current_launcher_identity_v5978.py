"""Whole5976 successor: resolve relative CMD executable through OS identity.

Always settle/store this finite boot before a live-identity assertion. Retain
the terminal failed identity-filter attempt and all original checker/audit/
settings/source checks. No executable/ROM/source copies or guest assistance.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_playtest_launcher_v5976 as original_boot
ROOT,need,sha=original_boot.ROOT,original_boot.need,original_boot.sha
OUT=ROOT/'audit_v5979_current_launcher_identity_checked'
run_source=inspect.getsource(original_boot.run)
before='Select-Object ProcessId,Name,CommandLine,'
need(run_source.count(before)==2,'Both actual live/terminal identity queries')
run_source=run_source.replace(before,'Select-Object ProcessId,Name,ExecutablePath,CommandLine,')
before="str(executable)in(j['CommandLine']or'')and str(boot)in(j['CommandLine']or'')and j['createdUnix']>=started"
after="j['ExecutablePath']and os.path.normcase(j['ExecutablePath'])==os.path.normcase(str(executable))and str(boot)in(j['CommandLine']or'')and j['createdUnix']>=started"
need(run_source.count(before)==1,'One relative-command executable identity correction')
run_source=run_source.replace(before,after,1)
before=" need(len(live)==1 and process.poll()is None,'Exactly one actual live cold boot from forwarding CMD')"
after=""" running_at_census=process.poll() is None
 stdout,stderr=process.communicate()
 with gzip.open(OUT/'boot.log.gz','wt')as writer:writer.write(stdout)
 (OUT/'stderr.log').write_text(stderr)
 (OUT/'live_census.json').write_text(json.dumps(jobs,indent=2)+'\\n')
 need(len(live)==1 and running_at_census,'Exactly one actual live cold boot from forwarding CMD')"""
need(run_source.count(before)==1,'One actual finite-boot settlement before identity assertion')
run_source=run_source.replace(before,after,1)
before=" stdout,stderr=process.communicate()\n with gzip.open(OUT/'boot.log.gz','wt')as writer:writer.write(stdout)\n (OUT/'stderr.log').write_text(stderr)\n need(process.returncode==0"
need(run_source.count(before)==1,'Remove only duplicate late finite-boot settlement')
run_source=run_source.replace(before,' need(process.returncode==0',1)
scope=dict(original_boot.run.__globals__,__file__=__file__,__doc__=__doc__,OUT=OUT)
exec(compile(run_source,__file__+'::entire5976_OS_executable_identity','exec'),scope)
run=scope['run'];run.source=run_source

if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable OS-resolved checked launcher test')
 try:
  report=run();failed=original_boot.OUT/'report.json';prior=json.loads(failed.read_text())
  need(not prior['passed']and 'Exactly one actual live cold boot from forwarding CMD'in prior['error'],
       'Actual failed relative-command identity filter preserved, no runtime acceptance transferred')
  for p in original_boot.OUT.rglob('*'):
   if p.is_file():report['inputHashes'][str(p)]=sha(p)
  report['inputHashes'][str(Path(original_boot.__file__).resolve())]=sha(original_boot.__file__)
  need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Every actual current/source/old/failed/native/settings evidence byte intact')
  report.update(actualOSExecutablePathBound=True,retainedFailedIdentityFilter=str(failed),fullPortAcceptance=False)
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  OUT.mkdir(exist_ok=True)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
