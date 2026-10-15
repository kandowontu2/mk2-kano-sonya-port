"""Bound real later Liu losses without discarding the earned SubZero clear.

Keep original30+ failed-attempt/rare-round/five-later-loss stop protection,
actual birth/path/parent/command checks, full transport and RAM preservation.
"""
import inspect
import json
from pathlib import Path
import retire_native_sonya_subzero_ring_policy as original
import run_native_sonya_subzero_guard_pressure_campaign as capture

ROOT, need, sha = capture.ROOT,capture.need,capture.sha
GAME,PARENT = 7268,21628
OUT = ROOT/'audit_native_sonya_liu_original_policy_preserved'
RETIRED = ROOT/'audit_native_sonya_liu_original_policy_retirement'


def scope():
    return dict(vars(original),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)


def stop():
    body=inspect.getsource(original.stop)
    for before,after in (("identity['createdUnix'] == 1791703089.4675903","identity['createdUnix'] == 1791708051.8534794"),
        ('("\'3\'", "\'11\'")','("\'3\'", "\'12\'")'),
        ('(\'30549\', \'304271\')','(\'30549\', \'391498\')'),
        ('("\'4:4\'", "\'8:8\'")','("\'4:4\'", "\'1:1\'")'),
        ('("\'4\'", "\'12\'")','("\'4\'", "\'13\'")')):
        body=original.once(body,before,after)
    body=body.replace('Sonya Ring','Sonya inherited guard/leg').replace('SubZero','LiuKang')
    bound=scope()
    exec(compile(body,__file__+'::whole_original_protected_actual_Liu_losing_stop','exec'),bound)
    return bound['stop']()


def prepare(ram):
    clear_path=ROOT/'audit_native_subzero_guard_pressure_earned_clear_phase_bound_checked/report.json'
    clear=json.loads(clear_path.read_text())
    need(clear['passed'] and clear['finiteNativeSonyaSubZeroClearAccepted'] and
         clear['actualObservedNextStage']['frame']=='391498' and
         clear['accepted']['ownSuccessfulRoundFrames']==[388387,390990] and
         all(sha(path)==digest for path,digest in clear['inputHashes'].items()),
         'Entire native SubZero clear/whole HP/all original callback phases remain qualified')
    body=inspect.getsource(original.prepare)
    body=original.once(body,'audit_native_subzero_ring_preceding_campaign_checked/report.json',
                      'audit_native_subzero_guard_pressure_preceding_campaign_checked/report.json')
    body=original.once(body,"body = body.replace(\"'9'\", \"'11'\").replace('range(9)', 'range(11)')",
        """body = once(body,"stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0",
                         "stats['lossesByStage']['12']>=30 and stats['latestNativeField']['stage']=='12'")
    body = body.replace('range(9)', 'range(12)')""")
    body=original.once(body,
        "OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)\")",
        "clear_path,OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)\")")
    body=body.replace('failed SubZero Ring policy','failed Liu guard/leg policy').replace('earlier eleven-fight','earlier twelve-fight')
    bound=dict(scope(),clear_path=clear_path)
    exec(compile(body,__file__+'::whole_original_failed_transport_preservation_and_earned_SubZero','exec'),bound)
    return bound['prepare'](ram)


def retire():
    bound=scope()
    exec(compile(inspect.getsource(original.retire),__file__+'::whole_original_exact_identity_retirement','exec'),bound)
    return bound['retire']()


if __name__=='__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
