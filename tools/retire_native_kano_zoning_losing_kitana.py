"""Preserve and retire exact repeated Kitana losses, not a timeout restart.

Rare won rounds in failed attempts remain real wins, never a match clear.
The failed physical policy, full sources and original buffers stay recorded.
"""
import inspect
import json
import re
import subprocess
from pathlib import Path
from types import SimpleNamespace
import retire_native_regular_guard_losing_scorpion as previous
import confirm_native_scorpion_policy_identity_retirement as identity_retirement
import prepare_native_kano_paired_stumble_host_checked as capture
import check_native_scorpion_guard_first_five_prefix as reader

ROOT,need,sha,progress=previous.ROOT,previous.need,previous.sha,previous.progress
GAME,PARENT=156972,123368
OUT=ROOT/'audit_native_kano_zoning_losing_kitana_preserved'
RETIRED=ROOT/'audit_native_kano_zoning_losing_kitana_retirement'


def stop():
    path=capture.OUT/'explicit_unsuccessful_physical_policy_stop.json'
    need(not path.exists(),'Fresh exact repeatedly unsuccessful Kano/Kitana policy stop')
    stats=progress.inspect(capture.OUT.name)
    identity=json.loads((capture.OUT/'native_identity.json').read_text())
    lines=reader.complete_lines(capture.OUT/'run.log.gz')
    parse=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',l)) for l in lines if l.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
    losses=[q for q in parse('LOSS') if q['stage']=='3']
    own=[q for q in parse('WIN') if q['stage']=='3' and q['slot']=='1']
    boundaries=[30549,*[int(q['frame']) for q in losses]]
    need(stats['originalNativeStillLive'] and stats['exactOriginalNativePID']==GAME and identity['ParentProcessId']==PARENT and
         stats['latestNativeField']['stage']=='3' and stats['latestNativeField']['human']=='17:17' and stats['latestNativeField']['cpu']=='4:4' and
         stats['lossesByStage']['3']==len(losses)>=30 and stats['nativeGlobalCacheFailureRows']==0 and
         all(sum(a<int(q['frame'])<b for q in own)<=1 for a,b in zip(boundaries,boundaries[1:])) and
         not any(int(q['frame'])>boundaries[-1] for q in own) and
         sum(int(q['frame'])>max([int(w['frame']) for w in own]+[30549]) for q in losses)>=5 and
         not any(q['stage']=='4' for q in parse('STAGE')) and identity in progress.census.census(),
         'Same exact live game,30+ failed paid attempts, no two owned wins in any one attempt and five further losses since latest real own round')
    path.write_text(json.dumps(dict(stats,passed=False,physicalPolicyUnsuccessful=True,exactNativeIdentity=identity,exactRAMParent=PARENT,
        actualUnsuccessfulKitanaAttempts=len(losses),actualOwnedKitanaRoundsPreserved=own,
        stopReason='Repeated original Kano zoning policy losses against true Kitana; rare single-round wins never form a successful match.',
        stoppedSolelyForObservationTimeout=False,engineDefectNotInferredFromControllerLosses=True,
        inputHashes={str(Path(__file__).resolve()):sha(__file__),str(Path(progress.__file__).resolve()):sha(progress.__file__),
                     str(Path(reader.__file__).resolve()):sha(reader.__file__)},
        fullTowerAccepted=False,endingAccepted=False,freshJoinAccepted=False),indent=2)+'\n')
    need(identity in progress.census.census(),'Exact native birth/path/parent/command rechecked immediately before owned stop')
    result=subprocess.run(['powershell.exe','-NoProfile','-Command',f'Stop-Process -Id {GAME} -ErrorAction Stop'],capture_output=True,text=True)
    need(result.returncode==0 and not result.stderr.strip(),'Only exact native losing-policy process stopped')
    print(json.dumps(dict(explicitStop=True,nativePID=GAME,failedKitanaAttempts=len(losses),actualOwnKitanaRounds=len(own))),flush=True)


def prepare(ram):
    scope=dict(vars(previous),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)
    source=inspect.getsource(previous.prepare)
    before="stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0"
    after="stats['lossesByStage']['3']>=30 and stats['latestNativeField']['stage']=='3'"
    need(source.count(before)==1,'Entire original unsuccessful policy preservation boundary')
    source=source.replace(before,after).replace('range(9)','range(3)').replace('failed Scorpion policy','failed Kitana policy').replace('earlier nine-fight','earlier three-fight')
    exec(compile(source,__file__+'::entire_original_failed_run_sources_and_buffers_preservation','exec'),scope)
    return scope['prepare'](ram)


def retire():
    prior_scope=dict(vars(previous),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)
    scope=dict(vars(identity_retirement),__file__=__file__,prior=SimpleNamespace(**prior_scope))
    exec(compile(inspect.getsource(identity_retirement.run),__file__+'::entire_original_PID_reuse_safe_retirement','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
