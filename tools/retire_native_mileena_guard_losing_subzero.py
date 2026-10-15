"""Preserve the current failed Sub-Zero policy, including rare earned rounds.

Never stop on an observation timeout or a reused PID. Require 30+ genuinely
failed attempts and five losses after the latest own round, without a clear.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import retire_native_kano_kitana_single_snapshot as single
import retire_native_kano_zoning_losing_kitana as stop_model
import retire_native_regular_guard_losing_scorpion as preservation
import confirm_native_scorpion_policy_identity_retirement as identity_retirement
import prepare_native_mileena_guard_campaign as capture

ROOT,need,sha,progress=preservation.ROOT,preservation.need,preservation.sha,preservation.progress
GAME,PARENT=125856,181552
OUT=ROOT/'audit_native_mileena_guard_losing_subzero_preserved'
RETIRED=ROOT/'audit_native_mileena_guard_losing_subzero_retirement'


def stop():
    body=inspect.getsource(stop_model.stop)
    body=single.previous.need and body
    before="    stats=progress.inspect(capture.OUT.name)\n    identity=json.loads((capture.OUT/'native_identity.json').read_text())\n    lines=reader.complete_lines(capture.OUT/'run.log.gz')"
    after="    identity=json.loads((capture.OUT/'native_identity.json').read_text())\n    lines=reader.complete_lines(capture.OUT/'run.log.gz')\n    stats=single.single_stats(lines,identity)"
    need(body.count(before)==1,'Whole safe stop from one exact captured snapshot')
    body=body.replace(before,after).replace("'3'","'11'").replace('30549','304271')
    body=body.replace("'17:17'","'18:18'").replace("'4:4'","'8:8'").replace("'4'","'12'")
    body=body.replace('Kitana','Subzero').replace('Kano zoning','Sonya guard/leg')
    scope=dict(vars(stop_model),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,
        single=single,OUT=OUT,RETIRED=RETIRED)
    exec(compile(body,__file__+'::whole_safe_rare_round_failed_policy_stop','exec'),scope)
    return scope['stop']()


def prepare(ram):
    proof_path=ROOT/'audit_native_mileena_guard_earned_clear_checked/report.json'
    proof=json.loads(proof_path.read_text())
    need(proof['passed']and proof['finiteNativeSonyaMileenaClearAccepted']and
         all(sha(p)==h for p,h in proof['inputHashes'].items()),
         'Actual earlier native Mileena clear and entire preceding chronology preserved')
    body=inspect.getsource(preservation.prepare)
    before="stats['lossesByStage']['9']>=30 and stats['ownWinReadsByStage']['9']==0"
    after="stats['lossesByStage']['11']>=30 and stats['latestNativeField']['stage']=='11'"
    need(body.count(before)==1,'Whole original unsuccessful policy preservation condition')
    body=body.replace(before,after).replace('range(9)','range(11)')
    body=body.replace('failed Scorpion policy','failed Subzero policy').replace('earlier nine-fight','earlier eleven-fight')
    before="for p in (OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)"
    after="for p in (proof_path,Path(preservation_file),Path(single_file),OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)"
    need(body.count(before)==1,'Whole preservation plus qualified advance and exact executed source pins')
    scope=dict(vars(preservation),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED,
        proof_path=proof_path,preservation_file=preservation.__file__,single_file=single.__file__)
    exec(compile(body.replace(before,after),__file__+'::whole_failed_campaign_preservation','exec'),scope)
    return scope['prepare'](ram)


def retire():
    prior_scope=dict(vars(preservation),__file__=__file__,capture=capture,GAME=GAME,PARENT=PARENT,OUT=OUT,RETIRED=RETIRED)
    scope=dict(vars(identity_retirement),__file__=__file__,prior=SimpleNamespace(**prior_scope))
    exec(compile(inspect.getsource(identity_retirement.run),__file__+'::whole_actual_identity_retirement','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    import sys
    {'stop':stop,'retire':retire}[sys.argv[1]]()
