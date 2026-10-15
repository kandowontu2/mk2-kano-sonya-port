"""Exact observer key correction; preserve executed6667 selector failure.

Native choice records publish actor/main, not register aliases a8/a13. No
source waveform, clock, route, packet, EOF or output comparison is changed.
"""
import inspect
import kano_cpu_launch_audio_model_v6667 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
source=inspect.getsource(original.sources)
for before,after in [("route[0]['a8']","route[0]['actor']"),("route[0]['a13']","route[0]['main']")]:
 need(source.count(before)==1,'Exact native choice observer key correction')
 source=source.replace(before,after,1)
scope=dict(original.__dict__)
exec(compile(source,__file__+'::actual_choice_observer_keys','exec'),scope)
for function in(original.predict,original.channels,original.packet_gate):
 exec(compile(inspect.getsource(function),__file__+'::whole_original_'+function.__name__,'exec'),scope)
sources,predict,channels,packet_gate=(scope[n]for n in('sources','predict','channels','packet_gate'))
