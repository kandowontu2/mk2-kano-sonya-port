"""Review the last actual captured walk field, age456, not terminal age480.

Original controller exits before its terminal frame_done callback. Its full
37 real snapshots and 480-field state window remain unchanged.
"""
import inspect
import review_launch_ground_ram as original
source=inspect.getsource(original.serve)
before='for age in(16,128,248,368,432,480):'
original.need(source.count(before)==1,'Exact host-only attempted terminal image selection')
source=source.replace(before,'for age in(16,128,248,368,432,456):')
scope=dict(vars(original));exec(compile(source,__file__+'::last_actual_walk_snapshot','exec'),scope)
serve=scope['serve']
receipt=original.receipt
