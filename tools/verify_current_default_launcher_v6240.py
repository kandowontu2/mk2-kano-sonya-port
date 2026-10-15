"""Verify the ordinary default CMD with actual executable identity and terminal.

Retain the full checker, denial, ROM, input and isolated-settings checks from
5976. Its command-line absolute-path assumption is not valid for a CMD that
changes directory and starts a relative executable. Never abandon a child
because an observation/check fails: collect its natural terminal first.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_playtest_launcher_v5976 as prior
import verify_current_default_launcher_v6238 as default
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6241_current_default_launcher_checked'

def run():
 need(sha(default.HISTORY)=='631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
      'Exact previous default retained')
 old=default.HISTORY.read_text()
 expected=old.replace('rem Keep the normal launcher on the current checked build, not the v277 prototype.',
                      'rem Use the current tested build; the older v1836 launcher remains available.',1).replace(
                      'PLAY_CURRENT_V1836_CHECKED.cmd','PLAY_CURRENT_V5219_CHECKED.cmd',1)
 need(default.FORWARD.read_text()==expected,'Only intended two-line default launcher change')
 code=inspect.getsource(prior.run)
 before='for p in(CHECKER,LAUNCHER,FORWARD,Path(__file__).resolve(),'
 need(code.count(before)==1,'Full original source pins retained')
 code=code.replace(before,'for p in(CHECKER,LAUNCHER,FORWARD,HISTORY,Path(prior.__file__),Path(default.__file__),Path(__file__).resolve(),',1)
 start=code.index(' time.sleep(3)\n')
 end=code.index(" need(process.returncode==0",start)
 original=code[start:end]
 need('Exactly one actual live cold boot from forwarding CMD' in original and 'process.communicate()' in original,
      'Replace only live observation and terminal persistence, not acceptance gates')
 replacement=''' observation_error=None;native=None
 try:
  time.sleep(3)
  census=powershell("Get-CimInstance Win32_Process -Filter \\\"Name='mkport_candidate.exe'\\\" | Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress")
  (OUT/'live_census.json').write_text(json.dumps(dict(exitCode=census.returncode,stdout=census.stdout,stderr=census.stderr),indent=2)+'\\n')
  need(census.returncode==0,'Read actual live native executable identity')
  jobs=json.loads(census.stdout)if census.stdout.strip()else[]
  if isinstance(jobs,dict):jobs=[jobs]
  live=[j for j in jobs if j['ExecutablePath'] and Path(j['ExecutablePath']).resolve()==executable.resolve()
        and str(boot)in(j['CommandLine']or'')and j['createdUnix']>=started and j['ParentProcessId']==process.pid]
  need(len(live)==1 and process.poll()is None,'Exactly one actual checked executable child of forwarding CMD')
  native=live[0]
  need('-autoboot_script'not in native['CommandLine']and '-nocheat'in native['CommandLine']and '-samples'in native['CommandLine'],
       'Actual ordinary command, no diagnostic controls')
  (OUT/'native_identity.json').write_text(json.dumps(native,indent=2)+'\\n')
 except Exception as error:
  observation_error=error
 finally:
  stdout,stderr=process.communicate()
  with gzip.open(OUT/'boot.log.gz','wt')as writer:writer.write(stdout)
  (OUT/'stderr.log').write_text(stderr)
  (OUT/'native_terminal.json').write_text(json.dumps(dict(cmdPID=process.pid,exitCode=process.returncode,
       observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),naturalTerminal=True,
       observationError=repr(observation_error)if observation_error else None),indent=2)+'\\n')
 if observation_error:raise observation_error
'''
 code=code[:start]+replacement+code[end:]
 # Terminal check uses the same full identity schema as the live capture.
 previous="Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix'"
 need(code.count(previous)==1,'Exactly one original terminal census')
 code=code.replace(previous,"Select-Object ProcessId,ParentProcessId,Name,ExecutablePath,CommandLine,@{Name='createdUnix'",1)
 scope=dict(prior.run.__globals__,__file__=__file__,prior=prior,default=default,OUT=OUT,
            PARENT=default.PARENT,FORWARD=default.FORWARD,HISTORY=default.HISTORY)
 exec(compile(code,__file__+'::full_original_checks_actual_identity','exec'),scope)
 report=scope['run']()
 report.update(defaultNowUsesCurrentV5219=True,legacyDefaultWrapperHistory=str(default.HISTORY),
               oldPublicLauncherAndZIPUnchanged=False,oldVersionedLauncherBuildZIPAndUserSettingsUnchanged=True,
               defaultLauncherChanged=True,finishedReleasePromotion=False,
               previousAttemptReport=str(default.OUT/'report.json'),
               previousAttemptNativeExitCodeUnknown=True)
 return report

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  OUT.mkdir(exist_ok=True)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
