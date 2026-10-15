"""Full ordinary checked-CMD audit, denials, identity and protected settings.

Reuse entire5976 checker/ROM/denial/coldboot criteria and6240 terminal-first
actual Windows identity observation. Preserve historical launcher byte copies;
record deliberate route changes separately, never rewrite prior acceptance.
"""
import inspect,json,subprocess,traceback
from pathlib import Path
from types import SimpleNamespace
import verify_current_playtest_launcher_v5976 as original
import verify_current_default_launcher_v6240 as transport
import native_projectile_identifiers_context_v6509 as candidate
ROOT,need,sha=candidate.ROOT,candidate.need,candidate.sha
TASK=original.TASK
OUT=ROOT/'audit_v6554_repaired_default_launcher_checked'
CHECKER=ROOT/'tools/check_repaired_playtest_v6552.ps1'
LAUNCHER=ROOT/'PLAY_CURRENT_V6508_CHECKED.cmd'
HISTORY=ROOT/'launcher_history_v6552/PLAY_MK2_KANO_SONYA.cmd'
PARENT=ROOT/'audit_v6558_repaired_projectile_storage/report.json'

def prepare_original():
 source=inspect.getsource(original.run)
 changes={
  "len(parent['remaining'])==5":"len(parent['remaining'])==6",
  'diagnostic_v5219_current_payload_rom_metadata\\\\mkport_candidate.exe':'diagnostic_v6508_native_projectile_identifiers\\\\mkport_candidate.exe',
  'check_current_playtest_v5975.ps1':'check_repaired_playtest_v6552.ps1',
  "'PLAY_CURRENT_V5219_CHECKED.cmd'in forward":"'PLAY_MK2_KANO_SONYA.cmd'in forward",
  "'Checked v5219'in stdout":"'Checked v6508'in stdout",
  "('voice','sonya_wins.wav'))":"('voice','sonya_wins.wav'),('runtime qualification','report.json'))",
 }
 for a,b in changes.items():need(source.count(a)==1,'Only actual new candidate/route metadata or additional denial '+a);source=source.replace(a,b,1)
 return source

def run():
 need(sha(HISTORY)=='C3E5553075F2977EFD36F6C4CF4D37726A29386F4718F4254242E7808FD6B3F1','Exact original root default preserved')
 need((ROOT/'PLAY_MK2_KANO_SONYA.cmd').read_text()==HISTORY.read_text().replace('PLAY_CURRENT_V5219_CHECKED.cmd','PLAY_CURRENT_V6508_CHECKED.cmd',1),'Only intended current default version pointer change')
 task_history=ROOT/'launcher_history_v6552/TASK_PLAY_LATEST_MK2_KANO_SONYA.cmd'
 need(sha(task_history)=='7B853BFA38DBF7738E93AE16C401F55D7F708077CB829F4F19AD1D812A8AA150','Exact old task direct-v5219 alias preserved')
 factory=inspect.getsource(transport.run)
 start=factory.index(' code=inspect.getsource(prior.run)');end=factory.index(' report.update(defaultNowUsesCurrentV5219')
 factory='def run():\n'+factory[start:end]+' return report\n'
 factory=factory.replace('code=inspect.getsource(prior.run)','code=prepare_original()',1)
 before='PARENT=default.PARENT,FORWARD=default.FORWARD,HISTORY=default.HISTORY)'
 after='PARENT=default.PARENT,FORWARD=default.FORWARD,HISTORY=default.HISTORY,current=candidate,CHECKER=CHECKER,LAUNCHER=LAUNCHER)'
 need(factory.count(before)==1,'Full original terminal-first actual native identity patch retained')
 factory=factory.replace(before,after,1)
 default=SimpleNamespace(PARENT=PARENT,FORWARD=TASK/'PLAY_LATEST_MK2_KANO_SONYA.cmd',HISTORY=HISTORY,__file__=transport.__file__)
 scope=dict(transport.__dict__,__file__=__file__,OUT=OUT,prior=original,default=default,candidate=candidate,
            CHECKER=CHECKER,LAUNCHER=LAUNCHER,prepare_original=prepare_original)
 exec(compile(factory,__file__+'::whole_original_checked_native_launcher','exec'),scope)
 report=scope['run']()
 for p in (Path(__file__),Path(transport.__file__),Path(original.__file__),task_history,
           ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd',ROOT/'tools/check_current_playtest_v5975.ps1',
           ROOT/candidate.old.NAME/'mkport_candidate.exe',ROOT/candidate.old.NAME/'build-info.json',
           ROOT/'release_v5986_current_playtest/MK2_Kano_Sonya_v5219_CURRENT_PLAYTEST.zip'):
  report['inputHashes'][str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Current verified routing and protected fallback pins intact')
 report.update(defaultNowUsesCurrentV6508=True,checkedWIPPromotion=True,finishedReleasePromotion=False,
               oldPublicLauncherAndZIPUnchanged=False,oldVersionedLauncherBuildZIPAndUserSettingsUnchanged=True,
               originalCanonicalLauncherRecoverableAt=str(HISTORY),oldTaskAliasRecoverableAt=str(task_history),
               intentionalHistoricalRoutingPinDrift=['PLAY_MK2_KANO_SONYA.cmd',str(TASK/'PLAY_LATEST_MK2_KANO_SONYA.cmd')],
               historicalReportsRemainUnchanged=True,goalStatus='active',newBuilds=0,newZIPs=0)
 return report

if __name__=='__main__':
 try:report=run()
 except Exception as e:
  report=dict(passed=False,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
  OUT.mkdir(exist_ok=True)
 p=OUT/'report.json';p.write_text(json.dumps(report,indent=2)+'\n');h=sha(p)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],capture_output=True).returncode==0 and sha(p)==h,'Exact launcher proof compression')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
