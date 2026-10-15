"""Correct the host parser's missing re import; retain every original gate."""
import inspect
import re
import launch_stage_advance_contract as previous

ROOT, need, sha, rows = previous.ROOT, previous.need, previous.sha, previous.rows
source = inspect.getsource(previous.inventory)
need(source.count('physical.re.findall') == 1, 'Only missing host parser namespace is corrected')
scope = dict(vars(previous), re=re)
exec(compile(source.replace('physical.re.findall', 're.findall', 1), __file__+'::whole_inventory_import_fix', 'exec'), scope)
exec(compile(inspect.getsource(previous.gate), __file__+'::whole_unchanged_stage_gate', 'exec'), scope)
gate, inventory = scope['gate'], scope['inventory']
