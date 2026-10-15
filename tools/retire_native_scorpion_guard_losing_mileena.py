"""Retire only the exact repeatedly unsuccessful Mileena input-policy trial.

Preserve every actual input/result and native buffer inventory. PID checks
always bind original birth/path/parent/command, never a reused PID alone.
"""
import inspect
import json
import subprocess
from pathlib import Path
import retire_native_regular_guard_losing_scorpion as previous
import capture_native_paired_stumble_scorpion_guard as capture
import confirm_native_scorpion_policy_identity_retirement as identity_retirement

ROOT, need, sha, progress = previous.ROOT, previous.need, previous.sha, previous.progress
GAME, PARENT = 180088, 173328
OUT = ROOT/'audit_native_scorpion_guard_losing_mileena_preserved'
RETIRED = ROOT/'audit_native_scorpion_guard_losing_mileena_retirement'


def stop():
    path = capture.OUT/'explicit_unsuccessful_physical_policy_stop.json'
    need(not path.exists(), 'Fresh exact unsuccessful Mileena policy stop')
    stats = progress.inspect(capture.OUT.name)
    identity = json.loads((capture.OUT/'native_identity.json').read_text())
    need(stats['originalNativeStillLive'] and stats['exactOriginalNativePID']==GAME and
         identity['ParentProcessId']==PARENT and stats['lossesByStage']['10']>=30 and
         stats['ownWinReadsByStage']['10']==0 and stats['nativeLegActivationsByStage']['10']==0 and
         stats['latestNativeField']['stage']=='10' and stats['latestNativeField']['human']=='18:18' and
         stats['latestNativeField']['cpu']=='5:5' and stats['nativeGlobalCacheFailureRows']==0 and
         identity in progress.census.census(),
         'Same exact actual game, 30+ paid Mileena losses and no owned round wins or leg activations')
    path.write_text(json.dumps(dict(stats,passed=False,physicalPolicyUnsuccessful=True,
        exactNativeIdentity=identity,exactRAMParent=PARENT,
        stopReason='30+ genuine paid Mileena losses without own wins; original ranged test branch still prevents the regular guard/leg fallback.',
        stoppedSolelyForObservationTimeout=False,engineDefectNotInferredFromControllerLosses=True,
        inputHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(progress.__file__).resolve()):sha(progress.__file__)},
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False),indent=2)+'\n')
    need(identity in progress.census.census(), 'Exact birth/path/command/parent rechecked immediately before owned stop')
    answer = subprocess.run(['powershell.exe','-NoProfile','-Command',f'Stop-Process -Id {GAME} -ErrorAction Stop'],capture_output=True,text=True)
    need(answer.returncode==0 and not answer.stderr.strip(), 'Only exact losing-policy native stopped')
    print(json.dumps(dict(explicitStop=True,nativePID=GAME,actualMileenaLosses=stats['lossesByStage']['10'])),flush=True)


def prepare(ram):
    scope = dict(vars(previous),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)
    source = inspect.getsource(previous.prepare)
    before = "stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0"
    after = "stats['lossesByStage']['10']>=30 and stats['ownWinReadsByStage']['10']==0"
    need(source.count(before)==1, 'Exact original failed-policy preservation boundary')
    source = source.replace(before, after).replace('range(9)', 'range(10)').replace('failed Scorpion policy', 'failed Mileena policy')
    exec(compile(source,__file__+'::whole_original_failed_trial_preservation','exec'),scope)
    return scope['prepare'](ram)


def retire():
    prior_scope = dict(vars(previous),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)
    from types import SimpleNamespace
    scope = dict(vars(identity_retirement),__file__=__file__,prior=SimpleNamespace(**prior_scope))
    exec(compile(inspect.getsource(identity_retirement.run),__file__+'::whole_PID_reuse_safe_retirement','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
