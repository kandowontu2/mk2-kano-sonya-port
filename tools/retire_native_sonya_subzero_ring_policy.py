"""Bound the actually unsuccessful Sub-Zero Ring tactic, not elapsed waiting.

Keep the whole original30+ failed-attempt/rare-round/five-later-loss and exact
native identity stop contract. Preserve the full failed transport, source
inventory and preceding eleven earned fights. No game defect is inferred.
"""
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
import retire_native_kano_zoning_losing_kitana as stop_model
import retire_native_kano_kitana_single_snapshot as single
import retire_native_regular_guard_losing_scorpion as preservation
import confirm_native_scorpion_policy_identity_retirement as identity_retirement
import run_native_sonya_subzero_ring_campaign as capture

ROOT, need, sha = capture.ROOT, capture.need, capture.sha
GAME, PARENT = 30832, 14408
OUT = ROOT / 'audit_native_sonya_subzero_ring_policy_preserved'
RETIRED = ROOT / 'audit_native_sonya_subzero_ring_policy_retirement'


def once(source, before, after):
    need(source.count(before) == 1, 'Entire original protective contract: ' + before[:100])
    return source.replace(before, after, 1)


def stop():
    identity = json.loads((capture.OUT / 'native_identity.json').read_text())
    need(identity['createdUnix'] == 1791703089.4675903 and identity['ProcessId'] == GAME and
         identity['ParentProcessId'] == PARENT and identity in preservation.progress.census.census(),
         'Same actual original native birth/path/parent/full command before stop preflight')
    body = inspect.getsource(stop_model.stop)
    body = once(body,
        "    stats=progress.inspect(capture.OUT.name)\n    identity=json.loads((capture.OUT/'native_identity.json').read_text())\n    lines=reader.complete_lines(capture.OUT/'run.log.gz')",
        "    identity=json.loads((capture.OUT/'native_identity.json').read_text())\n    lines=reader.complete_lines(capture.OUT/'run.log.gz')\n    stats=single.single_stats(lines,identity)")
    for before, after in [("'3'", "'11'"), ('30549', '304271'), ("'17:17'", "'18:18'"),
                          ("'4:4'", "'8:8'"), ("'4'", "'12'")]:
        need(before in body, 'Actual target/opponent boundary present')
        body = body.replace(before, after)
    body = body.replace('Kano/Kitana', 'Sonya/SubZero').replace('Kitana', 'SubZero').replace('Kano zoning', 'Sonya Ring')
    scope = dict(vars(stop_model), __file__=__file__, capture=capture, GAME=GAME, PARENT=PARENT,
                 OUT=OUT, RETIRED=RETIRED, single=single)
    exec(compile(body, __file__ + '::whole_original_single_snapshot_losing_policy_stop', 'exec'), scope)
    return scope['stop']()


def prepare(ram):
    preceding_path = ROOT / 'audit_native_subzero_ring_preceding_campaign_checked/report.json'
    preceding = json.loads(preceding_path.read_text())
    need(preceding['passed'] and preceding['finiteCurrentFirstElevenEarnedFightsByExactConservationAccepted'] and
         preceding['accepted']['completedOpponents'] == 11 and
         preceding['accepted']['completeOriginalRows'] == 785698 and
         len(preceding['allObservedCategoryFaultsRejected']) == 48 and
         all(sha(path) == digest for path, digest in preceding['inputHashes'].items()),
         'Entire actual earlier eleven earned fights and48 real category faults still frozen')
    body = inspect.getsource(preservation.prepare)
    body = body.replace("'9'", "'11'").replace('range(9)', 'range(11)')
    body = body.replace('failed Scorpion policy', 'failed SubZero Ring policy').replace('earlier nine-fight', 'earlier eleven-fight')
    body = once(body,
        "for p in (OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)",
        "for p in (preceding_path,Path(preservation_file),Path(stop_file),Path(single_file),OUT/'original_executed_sources.json.gz',Path(__file__).resolve()):bound[str(p)]=sha(p)")
    scope = dict(vars(preservation), __file__=__file__, capture=capture, GAME=GAME, PARENT=PARENT,
                 OUT=OUT, RETIRED=RETIRED, preceding_path=preceding_path, preservation_file=preservation.__file__,
                 stop_file=stop_model.__file__, single_file=single.__file__)
    exec(compile(body, __file__ + '::whole_original_failed_transport_and_sources_preservation', 'exec'), scope)
    return scope['prepare'](ram)


def retire():
    prior_scope = dict(vars(preservation), __file__=__file__, capture=capture, GAME=GAME, PARENT=PARENT,
                       OUT=OUT, RETIRED=RETIRED)
    scope = dict(vars(identity_retirement), __file__=__file__, prior=SimpleNamespace(**prior_scope))
    exec(compile(inspect.getsource(identity_retirement.run),
                 __file__ + '::whole_original_identity_safe_retirement', 'exec'), scope)
    return scope['run']()


if __name__ == '__main__':
    import sys
    {'stop':stop, 'retire':retire}[sys.argv[1]]()
