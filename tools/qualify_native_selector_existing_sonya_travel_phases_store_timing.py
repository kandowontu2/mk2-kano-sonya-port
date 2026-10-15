"""Bind actual store fields2035/2046, preceding sampled HP2036/2047.

Preserve original rejected checker and report. No new gameplay, gate invariant
waiver, or modified guest data; whole motion/state/health source gates retained.
"""
import inspect
import qualify_native_selector_existing_sonya_travel_phases as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_existing_sonya_travel_phases_store_timing_checked'
need(sha(original.__file__)=='D42D7D3983C1342DBE4BDDA510CC2513E41193F82D13F19C786D16E346F893CD' and
     sha(original.OUT/'failure.json')=='4B1E317DD83F2262CB028BDAF2FFB1B3E0D602F1880268E3929A17AB4E8536D3',
     'Exact original source/timing rejection remains unchanged')
scope=dict(vars(original),OUT=OUT,original=original,__file__=__file__)
for function in (original.square_followup,original.square_gate,original.bicycle_gate,original.gate,original.execute):
    source=inspect.getsource(function)
    if function is original.square_followup:
        source=original.replace(source,'[(2036,2),(2047,2)]','[(2035,2),(2046,2)]')
    if function is original.execute:
        source=original.replace(source,'paths=[Path(__file__),PARENT,',
                                "paths=[Path(__file__),Path(original.__file__),original.OUT/'failure.json',PARENT,")
    exec(compile(source,__file__+'::whole_original_'+function.__name__,'exec'),scope)
execute=scope['execute']
gate=scope['gate']
