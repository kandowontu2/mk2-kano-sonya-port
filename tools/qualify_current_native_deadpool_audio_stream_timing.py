"""Successor: stream positions may repeat between 50Hz sound flushes.

samples.cpp318..365 advances position only in sound_stream_update.
sound.h758 fixes streams update frequency at50Hz; sound.cpp1118..1120
creates that separate timer. Video frame observations are not sound flushes.
Keep the failed original checker intact; require monotonic progression,
short plateaus, near-complete traversal and actual termination instead.
"""
from pathlib import Path

source=(Path(__file__).parent/'qualify_current_native_deadpool_audio.py').read_text()
old='assert all(b>a for a,b in zip(positions,positions[1:]))'
assert source.count(old)==1
new='''assert all(b>=a for a,b in zip(positions,positions[1:]))
 assert positions[-1]-positions[0]>30000
 plateau=0
 max_plateau=0
 for a,b in zip(positions,positions[1:]):
  plateau=plateau+1 if b==a else 0
  max_plateau=max(max_plateau,plateau)
 assert max_plateau<=2
 case['maximumRepeatedPositionIntervals']=max_plateau'''
source=source.replace(old,new)
source=source.replace("'audit_current_native_deadpool_audio_checked'","'audit_current_native_deadpool_audio_stream_timing_checked'")
exec(compile(source,str(Path(__file__).parent/'qualify_current_native_deadpool_audio.py'),'exec'))
