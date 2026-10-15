"""Full-scope handoff for the authoritative live native sound-guard build."""
import json
import subprocess
from pathlib import Path
import verify_native_sound_packet_guard_v3669 as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
PREVIOUS=ROOT/'audit_v3672_native_sound_packet_full_scope_checkpoint/checkpoint.json'
OUT=ROOT/'audit_v3686_native_sound_build_wait_full_scope_checkpoint'

def main():
    need(not OUT.exists(),'New live build checkpoint')
    command="Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('gmake.exe','cc1plus.exe') } | Select-Object ProcessId,ParentProcessId,Name,CreationDate | ConvertTo-Json -Compress"
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True,text=True,check=True)
    processes=json.loads(result.stdout)
    if isinstance(processes,dict):processes=[processes]
    need(processes and any(p['Name']=='gmake.exe'for p in processes),'Specific build/compile processes confirmed live now')
    state=json.loads(PREVIOUS.read_text());remaining=list(state['remaining'])
    need(state['goalStatus']=='active'and len(remaining)==5 and not state['fullPortAcceptance']and not state['finishedRelease'],'Full objective intact')
    pins={str(PREVIOUS):sha(PREVIOUS),str(Path(__file__).resolve()):sha(__file__)}
    attempts=[]
    for version in(3674,3676,3678):
        leaf=ROOT/f'diagnostic_v{version}_native_sound_packet_guard'
        log=(leaf/'build.log').read_text(encoding='utf-8-sig')
        restore=json.loads((leaf/'restoration.json').read_text(encoding='utf-8-sig'))
        need(restore['passed']and 'Error' in log and not(leaf/'mkport_candidate.exe').exists(),'Failed terminal build retained, exact restoration recorded, no candidate promoted')
        cause='new GCC warnings promoted to errors'if version in(3674,3676)else'missing old custom target definition; source-selected generation replaces it'
        attempts.append(dict(candidate=leaf.name,terminalExitCode=1,restorationReport=str(leaf/'restoration.json'),cause=cause,
          temporaryExecutableBackupRemoved=not(leaf/'restoration_backups/mkport.exe').exists()))
        for file in leaf.rglob('*'):
            if file.is_file():pins[str(file)]=sha(file)
    active=ROOT/'diagnostic_v3680_native_sound_packet_guard'
    log=(active/'build.log').read_text(encoding='utf-8-sig')
    need('Compiling src/mame/midway/midtunit_m.cpp...'in log and not any(s in log for s in('error:','fatal error',' Error ')),
         'Actual guarded machine compilation observed, no reported compile error so far')
    need(not(active/'restoration.json').exists()and not(active/'build-info.json').exists(),'Active build not mislabeled terminal')
    for file in active.joinpath('input_sources').rglob('*'):
        if file.is_file():pins[str(file)]=sha(file)
    for file in('tools/build_native_sound_packet_guard_v3673.ps1','tools/build_native_sound_packet_guard_v3675.ps1',
                 'tools/build_native_sound_packet_guard_v3677.ps1','tools/build_native_sound_packet_guard_v3679.ps1',
                 'tools/run_native_sound_delivery_ram_v3682.py','mk2ks_native_sound_delivery_ram_v3681.lua'):
        pins[str(ROOT/file)]=sha(ROOT/file)
    state.update(previousCheckpoint=str(PREVIOUS),inputHashes=pins,
      inputHashInheritance=dict(schema=1,parentCheckpoint=str(PREVIOUS),parentSHA256=sha(PREVIOUS),
        mergeRule='Resolve parent recursively preserving retired/deleted exclusions. Do not flatten historical map.'),
      previousGoalTurnClassification=state['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress and verified wait: staged packet guard/source3670/current3672 inspected. Three fresh builds terminal1 fail newGCC Werror/vendor and missing custom definition; each actual original user-file/executable restoration recorded and only created transient backup removed. Fresh3679builder uses supportedSOURCES/REGENIE/NOWERROR, no thirdparty source mutation or retired data restoration; current3680 rebuild is confirmed live by specific gmake/compiler PIDs and exec session56841. Actual guarded machine cpp compiled without errors so far, but final link/executable/runtime acceptance unproven. New3681read-only actualADSP-latch observer and3682RAM samples-on/off pipeline ready: source-qualified38/39female packed range, actual delivery, full original16k winner waveform via retained unchanged MAME interpolation, proper source_num idle semantics. No execution of new runtime gate yet; all5groups retained.',
      failedBuildAttempts=attempts,
      pendingNativeSoundBuild=dict(candidate=active.name,execSessionId=56841,processesConfirmedLive=processes,
        compilerScript=str(ROOT/'tools/build_native_sound_packet_guard_v3679.ps1'),
        buildLog=str(active/'build.log'),workingFilesTemporarilyStaged=True,
        exactRestorationInBuilderFinally=True,finalLinkAndExecutableUnproven=True),
      preparedNativeSoundRuntimeRegression=dict(script=str(ROOT/'tools/run_native_sound_delivery_ram_v3682.py'),
        executed=False,rawAudioFiles=0),
      nextAction='Poll authoritative exec session56841/current gmake processes; never restart merely due observation timeout. If terminal0 inspect3680build-info/restoration and exact source/EXE/payload/wholeguest, then run3682RAM actualADSP delivery/full16k winner waveform/trueownedvictim gender gate. If terminal1 inspect exact failure and ensure actual user-file/executable restoration before fresh repair; never overwrite failed build/evidence. No public promotion until full shared selection/direct cue/state/audio regressions, remaining5groups and release refreshed. No retired graph/data restoration. Current source-selected target replaces missing old definition and NOWERROR warnings retained; built machine code/sourcefix is not finished executable/audio acceptance yet. Keep exact restored public/current/user work; payload may share immutable hardlink only after successful link. Compress sealed logs and avoid raw audio/raster/VRAM copies.')
    need(state['remaining']==remaining and not state['fullPortAcceptance']and not state['finishedRelease'],'No scope shrinking')
    OUT.mkdir();file=OUT/'checkpoint.json';file.write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(dict(checkpoint=str(file),liveBuildSession=56841,liveBuildProcesses=len(processes),
      freshPins=len(pins),fullPortAcceptance=False),indent=2))

if __name__=='__main__':main()
