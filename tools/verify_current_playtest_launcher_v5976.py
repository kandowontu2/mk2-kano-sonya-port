"""Actual checked v5219 launcher/ROM audit/cold boot, no new build copies.

Keep old public launcher/ZIP and all user settings unchanged. Cold boot uses
isolated settings and no diagnostic autoboot; it is not interactive audio or
whole-port acceptance. Checker-denial tests simulate digest mismatches in
RAM, without damaging or copying actual protected executable/ROM/voice files.
"""
import base64,datetime,gzip,hashlib,json,os,re,subprocess,time,traceback
from pathlib import Path
import current_payload_metadata_context_v5229 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
TASK=Path(r'C:\Users\kando\Documents\Codex\2026-08-30\continue-the-mk2-kano-sonya-port')
OUT=ROOT/'audit_v5977_current_checked_launcher'
CHECKER=ROOT/'tools/check_current_playtest_v5975.ps1'
LAUNCHER=ROOT/'PLAY_CURRENT_V5219_CHECKED.cmd'
FORWARD=TASK/'PLAY_LATEST_MK2_KANO_SONYA.cmd'
PARENT=ROOT/'audit_v5974_current_pit_queue_rng_progress/progress.json'

def powershell(code):
 encoded=base64.b64encode(code.encode('utf-16le')).decode()
 return subprocess.run(['powershell.exe','-NoProfile','-EncodedCommand',encoded],capture_output=True,text=True)

def settings():
 paths=[ROOT/'diagnostic_v1836_ball_register_boundary/play',ROOT/'mame-mkp/cfg',ROOT/'mame-mkp/nvram',
        ROOT/'play_v5219_checked',ROOT/'cfg',ROOT/'nvram']
 return {str(p.resolve()):sha(p)for folder in paths if folder.exists()for p in folder.rglob('*')if p.is_file()}

def run():
 need(not OUT.exists(),'Fresh immutable actual current launcher qualification')
 current.expected();parent=json.loads(PARENT.read_text())
 need(parent['passed']and parent['goalStatus']=='active'and len(parent['remaining'])==5,'Previous native queue/RNG progress and whole objective intact')
 pins={str(PARENT):sha(PARENT)}
 for p in(CHECKER,LAUNCHER,FORWARD,Path(__file__).resolve(),
          ROOT/'PLAY_MK2_KANO_SONYA.cmd',ROOT/'PLAY_CURRENT_V1836_CHECKED.cmd',TASK/'PLAY_MK2_KANO_SONYA.cmd',
          ROOT/'release_v1863_current_playtest/MK2_Kano_Sonya_v1836_CURRENT_PLAYTEST.zip',
          ROOT/current.NAME/'build-info.json',ROOT/current.NAME/'mkport_candidate.exe',ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata'):
  pins[str(p)]=sha(p)
 build=json.loads((ROOT/current.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
 for p,h in build['input_hashes'].items():pins[p]=h
 source=CHECKER.read_text();cmd=LAUNCHER.read_text();forward=FORWARD.read_text()
 need('diagnostic_v5219_current_payload_rom_metadata\\mkport_candidate.exe'in cmd and '-samples -samplerate 48000'in cmd and
      '-nocheat %*'in cmd and 'check_current_playtest_v5975.ps1'in cmd and
      all(s not in cmd for s in('-autoboot_script','-skip_gameinfo','-nosamples','-cheat '))and
      'play_v5219_checked'in cmd and 'PLAY_CURRENT_V5219_CHECKED.cmd'in forward,
      'Actual matched candidate/default48k enabled voices/fresh settings/no cheats/no scripted input/no hidden warnings')
 ast=powershell("$taskErrors=$null; [void][System.Management.Automation.Language.Parser]::ParseFile('"+str(CHECKER)+"',[ref]$null,[ref]$taskErrors); if($taskErrors.Count){$taskErrors|Out-String;exit 1}")
 need(ast.returncode==0,'Actual Windows PowerShell parses checker without module assumptions')
 before=settings();OUT.mkdir();(OUT/'settings_before.json').write_text(json.dumps(before,indent=2)+'\n')
 check=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(CHECKER)],cwd=str(TASK),capture_output=True,text=True)
 need(check.returncode==0 and 'all sixteen voice assets'in check.stdout,'Actual untouched installed checker accepts exact matched build/voices from different cwd')
 (OUT/'checker.log').write_text(check.stdout+check.stderr)
 # Same checker source/branches in RAM, only root routing for ScriptBlock.
 root_line='$taskRoot = Split-Path $PSScriptRoot -Parent'
 need(source.count(root_line)==1,'One ScriptBlock-only root routing substitution')
 direct=source.replace(root_line,"$taskRoot = '"+str(ROOT)+"'",1)
 wrapper=lambda s:'try { & {\n'+s+'\n}; exit 0 } catch { Write-Output $_.Exception.Message; exit 1 }'
 baseline=powershell(wrapper(direct));need(baseline.returncode==0,'Whole RAM denial-test positive checker restored')
 old_return="return [BitConverter]::ToString($taskHash.ComputeHash($taskStream)).Replace('-', '')"
 need(direct.count(old_return)==1,'One full actual hash calculation')
 denials=[]
 for label,predicate in(('manifest','build-info.json'),('executable','mkport_candidate.exe'),('payload','mk2ks.mdata'),('voice','sonya_wins.wav')):
  alternative="$taskDigest = [BitConverter]::ToString($taskHash.ComputeHash($taskStream)).Replace('-', ''); if ([IO.Path]::GetFileName($Path) -eq '"+predicate+"') { return ('0' * 64) }; return $taskDigest"
  denied=powershell(wrapper(direct.replace(old_return,alternative,1)))
  need(denied.returncode==1 and denied.stdout.strip(),'Whole actual checker rejects simulated '+label+' digest mismatch')
  restored=powershell(wrapper(direct));need(restored.returncode==0,'Whole real-file positive checker restored after each denial')
  denials.append(dict(kind=label+' digest mismatch simulation',rejectedBy=denied.stdout.strip(),actualFilesChanged=False))
 executable=ROOT/current.NAME/'mkport_candidate.exe'
 audit_cmd=[str(executable),'mk2ks','-rompath',str(ROOT/current.NAME/'roms')+';'+str(ROOT/'roms'),'-verifyroms']
 audit=subprocess.run(audit_cmd,cwd=str(TASK),capture_output=True,text=True)
 (OUT/'rom_audit.log').write_text(audit.stdout+audit.stderr)
 need(audit.returncode==0 and 'is good'in audit.stdout and not re.search(r'WRONG CHECKSUMS|NOT FOUND|INCORRECT|BAD DUMP',audit.stdout+audit.stderr,re.I),
      'Actual current ROM audit passes all declared dependencies without mismatched checksum warnings')
 boot=OUT/'boot';boot.mkdir()
 boot_args=['-inipath',str(boot),'-cfg_directory',str(boot/'cfg'),'-nvram_directory',str(boot/'nvram'),
            '-snapshot_directory',str(boot/'snap'),'-video','none','-sound','none','-str','12']
 command=[os.environ['ComSpec'],'/d','/c',str(FORWARD),*boot_args]
 started=time.time();process=subprocess.Popen(command,cwd=str(TASK),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 identity=dict(hostPID=os.getpid(),pid=process.pid,command=command,startedUnix=started,hostSource=str(Path(__file__).resolve()))
 (OUT/'process.json').write_text(json.dumps(identity,indent=2)+'\n')
 time.sleep(3)
 census=powershell("Get-CimInstance Win32_Process -Filter \"Name='mkport_candidate.exe'\" | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress")
 need(census.returncode==0,'Read actual live cold-boot native identity')
 jobs=json.loads(census.stdout)if census.stdout.strip()else[]
 if isinstance(jobs,dict):jobs=[jobs]
 live=[j for j in jobs if str(executable)in(j['CommandLine']or'')and str(boot)in(j['CommandLine']or'')and j['createdUnix']>=started]
 need(len(live)==1 and process.poll()is None,'Exactly one actual live cold boot from forwarding CMD')
 native=live[0];need('-autoboot_script'not in native['CommandLine']and '-nocheat'in native['CommandLine']and '-samples'in native['CommandLine'],
                       'Actual native command is ordinary checked launcher, no diagnostic controls')
 (OUT/'native_identity.json').write_text(json.dumps(native,indent=2)+'\n')
 stdout,stderr=process.communicate()
 with gzip.open(OUT/'boot.log.gz','wt')as writer:writer.write(stdout)
 (OUT/'stderr.log').write_text(stderr)
 need(process.returncode==0 and stderr==''and 'Checked v5219'in stdout and not re.search(
      r'WRONG CHECKSUMS|might not run correctly|LUA ERROR|Lua error|fatal error|stack traceback|access violation',stdout,re.I),
      'Actual ordinary12second forwarding-CMD cold boot terminal0, checked bytes, no ROM/runtime warnings')
 need(settings()==before,'All pre-existing user/old/default play settings unchanged; isolated boot writes only')
 exact=powershell("Get-CimInstance Win32_Process -Filter 'ProcessId="+str(native['ProcessId'])+"' | Select-Object ProcessId,Name,CommandLine,@{Name='createdUnix';Expression={([DateTimeOffset]$_.CreationDate).ToUnixTimeMilliseconds()/1000}} | ConvertTo-Json -Compress")
 need(exact.returncode==0,'Actual captured native terminal rechecked')
 later=json.loads(exact.stdout)if exact.stdout.strip()else[]
 if isinstance(later,dict):later=[later]
 need(not any(j==native for j in later),'Exact captured PID/name/creation/full command terminal, not an observation timeout')
 current.expected();need(all(sha(p)==h for p,h in pins.items()),'Every protected compiled/user-dirty/old public/new launcher/native input byte unchanged')
 for p in OUT.rglob('*'):
  if p.is_file():pins[str(p)]=sha(p)
 return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=current.NAME,inputHashes=pins,
             matchedCurrentLauncher=str(LAUNCHER),userTaskLauncher=str(FORWARD),actualROMAuditExitCode=audit.returncode,
             actualForwardingCMDBootExitCode=process.returncode,actualNativeColdBootIdentity=native,
             actualSourceCheckerDenialSimulations=denials,actualProtectedFilesModifiedForTests=False,
             currentExePayloadAndAll16VoicesChecked=True,ordinaryNoAutobootColdStartupAccepted=True,
             preExistingUserSettingsUnchanged=True,oldPublicLauncherAndZIPUnchanged=True,
             interactiveVideoAndPhysicalAudioDeviceAcceptance=False,fullPortAcceptance=False,
             newBuilds=0,newRawRecordings=0,newZIPs=0)

if __name__=='__main__':
 try:report=run()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  OUT.mkdir(exist_ok=True)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes',)},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
