"""Actual normal CMD cold boot outside workspace; no Lua or game-state assistance."""
import gzip,json,os,subprocess,time
from pathlib import Path
import native_cpu_finisher_spacing_context as native
import native_process_census_v6647 as census
ROOT,need,sha=native.ROOT,native.need,native.sha
OUT=ROOT/'audit_latest_native_launcher'
OUTSIDE=Path('C:/Users/kando/Documents/Codex/2026-08-30/continue-the-mk2-kano-sonya-port')

if __name__=='__main__':
    need(not OUT.exists() and not census.census(),'Fresh normal-launch verification; no live native job restart')
    native.expected()
    launcher=ROOT/'PLAY_LATEST_KANO_SONYA.cmd';checker=ROOT/'tools/check_latest_native_playtest.ps1'
    old=ROOT/'PLAY_MK2_KANO_SONYA.cmd'
    need(sha(old)=='90BD99EC729C956A1414D9A544DBA537597A828AE382D323579DF266FB053ACE',
         'Historical canonical launcher and every prior dependency remain intact')
    source=launcher.read_text()
    need('-autoboot_script' not in source and '-nocheat' in source and
         'diagnostic_native_cpu_finisher_spacing\\samples;samples' in source and
         'diagnostic_native_cpu_finisher_spacing\\roms;roms' in source,
         'Ordinary current matched native command, with correct waveform overlay and no scripted controller')
    settings=[p for leaf in ('cfg','nvram') for p in (ROOT/'play_v5219_checked'/leaf).rglob('*') if p.is_file()]
    setting_pins={str(p):sha(p) for p in settings}
    pins={str(p.resolve()):sha(p) for p in (launcher,checker,old,Path(__file__),
        ROOT/'LATEST_PLAYTEST.txt',ROOT/native.NAME/'mkport_candidate.exe',ROOT/native.NAME/'build-info.json')}
    OUT.mkdir()
    command=[os.environ.get('COMSPEC','C:/Windows/System32/cmd.exe'),'/d','/c',str(launcher),
        '-video','none','-sound','none','-str','15','-inipath',str(OUT),
        '-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap')]
    started=time.time();job=subprocess.Popen(command,cwd=OUTSIDE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
    (OUT/'process.json').write_text(json.dumps(dict(cmdPID=job.pid,command=command,cwd=str(OUTSIDE)),indent=2)+'\n')
    observation_error=None;actual=None
    try:
        for _ in range(200):
            actual=next((r for r in census.census() if r['ParentProcessId']==job.pid and
                Path(r['ExecutablePath']).resolve()==(ROOT/native.NAME/'mkport_candidate.exe').resolve() and
                r['createdUnix']>=started-1),None)
            if actual or job.poll() is not None:break
            time.sleep(.05)
        need(actual and job.poll() is None,'Actual current EXE child of this normal CMD, not inferred from launch intent')
        native_command=actual['CommandLine']
        need('-autoboot_script' not in native_command and '-nocheat' in native_command and
             '-samples' in native_command and 'play_v5219_checked' in native_command and str(OUT) in native_command,
             'Actual native command forwards arguments and contains no automated selection/physical controller')
        (OUT/'native_identity.json').write_text(json.dumps(actual,indent=2)+'\n')
        print(json.dumps(dict(actualNativePID=actual['ProcessId'],actualCMDParent=job.pid,normalCMD=True)),flush=True)
    except Exception as e:observation_error=e
    finally:
        # Natural -str termination only. A timeout or failed observation never
        # kills/restarts the actual game, and the original handle is retained.
        stdout,stderr=job.communicate()
        with gzip.open(OUT/'boot.log.gz','wt',encoding='utf-8') as f:f.write(stdout)
        (OUT/'stderr.log').write_text(stderr)
        (OUT/'native_terminal.json').write_text(json.dumps(dict(cmdExit=job.returncode,actualNativeIdentity=actual,
            naturalPlannedExit=True,observationError=repr(observation_error) if observation_error else None),indent=2)+'\n')
    if observation_error:raise observation_error
    need(job.returncode==0 and not census.census() and 'all seventeen waveforms match' in stdout and
         not any(s in stderr.lower() for s in ('fatal error','unable to','error:','lua error')),
         'Actual normal CMD/EXE cold boot exits naturally0 with matching assets and no startup errors')
    check=subprocess.run([os.environ.get('COMSPEC','C:/Windows/System32/cmd.exe'),'/d','/c',str(launcher),'--check'],
        cwd=OUTSIDE,capture_output=True,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
    need(check.returncode==0 and 'all seventeen waveforms match' in check.stdout and not census.census(),
         'Actual check-only CMD outside workspace succeeds without starting a game')
    need(all(sha(p)==h for p,h in {**pins,**setting_pins}.items()),
         'Old launchers, actual inputs and every existing player settings byte preserved')
    report=dict(passed=True,fullPortAcceptance=False,actualNativeIdentity=actual,nativeCMDExit=job.returncode,
        actualNormalCMDOutsideWorkspaceBootAccepted=True,checkOnlyOutsideWorkspaceAccepted=True,
        candidate=native.NAME,executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,
        forwardedVideoAudioObservationLimitSeconds=15,noScriptedInputs=True,noCheats=True,
        historicalCanonicalLauncherUnchanged=True,existingSettingsPreserved=setting_pins,
        inputHashes=pins,stdoutCheckOnly=check.stdout,
        latestPlaytestLauncher=str(launcher),finishedReleasePromoted=False,newBuilds=0,newROMCopies=0,
        goalStatus='active',allOriginalGoalRequirementsStillActive=True)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    for p in OUT.iterdir():
        if p.is_file():subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(p)],check=True,capture_output=True)
    print(json.dumps(dict(passed=True,actualNormalCMDNativeBoot=True,actualNativePID=actual['ProcessId'],
        oldLauncherAndSettingsUnchanged=True,finishedRelease=False)),flush=True)
