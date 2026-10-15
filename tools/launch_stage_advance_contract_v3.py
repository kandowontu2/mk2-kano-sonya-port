"""Retain native lethal provenance across the game's full finish sequence.

The executed v2 imposed an unsupported 100-field winner delay. Actual native
finish sequences last 249/170 fields. Require the real current-round lethal
store, continuous zero loser HP, and no intervening reset/selection instead.
"""
import inspect
import launch_stage_advance_contract_v2 as previous
import launch_stage_advance_contract as original

ROOT, need, sha, rows = previous.ROOT, previous.need, previous.sha, previous.rows
inventory = previous.inventory
source = inspect.getsource(original.gate)
before = "        need(lethal and int(win['frame'])-int(lethal[-1]['frame']) < 100, 'Each winning round follows real native lethal collision')"
after = """        need(lethal, 'Each winning round has an actual native lethal collision')
        death, victory = int(lethal[-1]['frame']), int(win['frame'])
        earlier = [int(v['frame']) for v in wins if int(v['frame']) < victory]
        need(death > max(earlier, default=first-1), 'Lethal belongs to this round, never reused from an earlier win')
        need(all(by[f, 3-side]['hp'] == '0' and by[f, 3-side]['mode'] == '2'
                 for f in range(death+1, victory+1)), 'Whole native finish sequence retains zero loser HP')
        need(not any(death < int(r['frame']) <= victory and r['pc'] != 'FF836700' for r in health) and
             not any(death < int(r['frame']) <= victory for r in actual('MK2_NAT_CAMPAIGN_SELECT')),
             'No health reset/refill or selection between actual lethal and winner')"""
need(source.count(before) == 1, 'Only unsupported KO-to-winner timing bound changes')
scope = dict(vars(original), inventory=inventory)
exec(compile(source.replace(before, after, 1), __file__+'::whole_native_finish_sequence_gate', 'exec'), scope)
gate = scope['gate']
