"""Entire5976 current checker/ROM audit/default CMD cold boot qualification.

Canonical user-facing CMD now chooses tested5219, not obsolete1836. Preserve
old wrapper bytes separately; old versioned launcher/build/settings remain.
No new build, raw media, ZIP or unverified final-release promotion.
"""
import inspect,json,traceback
from pathlib import Path
import verify_current_playtest_launcher_v5976 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_v6239_current_default_launcher_checked'
PARENT=ROOT/'audit_v6236_current_mileena_source_audio_progress/progress.json'
FORWARD=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
HISTORY=ROOT/'launcher_history_v6237/PLAY_MK2_KANO_SONYA_v1836.cmd'

def run():
 need(sha(HISTORY)=='631DDB18A2F740F102E5D4167B18269DE848A1E9936FE54DD8D8DD54C55ACAE7',
      'Exact original1836 default-wrapper bytes retained')
 new=FORWARD.read_text();old=HISTORY.read_text()
 expected=old.replace('rem Keep the normal launcher on the current checked build, not the v277 prototype.',
                      'rem Use the current tested build; the older v1836 launcher remains available.',1).replace(
                      'PLAY_CURRENT_V1836_CHECKED.cmd','PLAY_CURRENT_V5219_CHECKED.cmd',1)
 need(new==expected,'Only exact default candidate and explanatory comment change')
 code=inspect.getsource(prior.run)
 before='for p in(CHECKER,LAUNCHER,FORWARD,Path(__file__).resolve(),'
 need(code.count(before)==1,'Only add actual historical/default verification inputs')
 code=code.replace(before,'for p in(CHECKER,LAUNCHER,FORWARD,HISTORY,Path(prior.__file__),Path(__file__).resolve(),',1)
 scope=dict(prior.run.__globals__,__file__=__file__,prior=prior,OUT=OUT,PARENT=PARENT,FORWARD=FORWARD,HISTORY=HISTORY)
 exec(compile(code,__file__+'::entire5976_actual_default_CMD_boot','exec'),scope)
 report=scope['run']()
 report.update(currentDefaultCMD=str(FORWARD),defaultNowUsesCurrentV5219=True,
               legacyDefaultWrapperHistory=str(HISTORY),oldPublicLauncherAndZIPUnchanged=False,
               oldVersionedLauncherBuildZIPAndUserSettingsUnchanged=True,
               defaultLauncherChanged=True,finishedReleasePromotion=False)
 return report

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  OUT.mkdir(exist_ok=True)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
