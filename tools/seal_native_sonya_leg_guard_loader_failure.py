"""Exact naturally terminal pre-frame loader failure, never gameplay evidence."""
import json
import subprocess
from pathlib import Path
import capture_native_kano_laser_sonya_postending_leg_guard as prior

ROOT,need,sha=prior.ROOT,prior.need,prior.sha
OUT=ROOT/'audit_native_kano_laser_sonya_leg_guard_loader_failure'


def run():
    need(not OUT.exists(),'Fresh immutable actual loader failure preservation')
    terminal=json.loads((prior.OUT/'native_terminal.json').read_text())
    error=(prior.OUT/'stderr.log').read_text()
    failure=json.loads((prior.OUT/'current_capture_failure.json').read_text())
    need(terminal['nativeExit']==3 and terminal['identity']['ProcessId']==180976 and
         terminal['identity']['ParentProcessId']==191132 and not failure['passed'] and
         'Jax_physical_pound_jump_guard_only_4807:14: assertion failed!' in error and
         not (prior.OUT/'guest_memory_proof.json').exists(),
         'Actual exact native loader assertion before any guest/gameplay callback')
    pins=json.loads((prior.OUT/'input_hashes_before.json').read_text())
    need(all(sha(p)==h for p,h in pins.items()),'All failed executed inputs preserved unchanged')
    query='Get-CimInstance Win32_Process -Filter "ProcessId=180976 OR ProcessId=191132" | Select-Object ProcessId | ConvertTo-Json -Compress'
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',query],capture_output=True,text=True)
    need(result.returncode==0 and not result.stdout.strip() and not result.stderr.strip(),
         'Exact native child and its zero-raster RAM parent authoritatively absent')
    files=[p for d in (prior.OUT,prior.INIT,prior.SOURCE) for p in d.rglob('*') if p.is_file()]
    need(not any(p.suffix.lower() in ('.png','.wav','.bin','.exe','.zip') for p in files),
         'No raw media/build/ROM/archive left by exact pre-frame failure')
    OUT.mkdir()
    report=dict(passed=True,failedLoaderPreserved=True,nativeExit=3,exactNativeGameRetired=180976,
        exactRAMParentRetired=191132,actualGuestAccepted=False,nativeGameplayAccepted=False,
        sourceOnlyInitializerNotRuntimeAcceptance=True,originalFailure=failure,
        cause='The mirror branch was altered before the original Kitana/Jax/Subzero loaders copied it; their exact original source marker no longer matched.',
        correctionRequired='Delay only CPU Kano mirror guard/leg substitution until original opponent-specific branches have already been assembled.',
        inputHashes={str(p.resolve()):sha(p) for p in [Path(__file__),*files]},originalFailedInputHashes=pins,
        rawNativeBuffersReleased=0,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,
        fullPortAcceptance=False,goalStatus='active')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(preserved=True,actualNativeExit=3,actualGameplayAccepted=False,exactRAMParentRetired=191132)),flush=True)


if __name__=='__main__': run()
