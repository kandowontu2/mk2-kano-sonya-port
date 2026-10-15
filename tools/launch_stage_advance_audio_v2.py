"""Separate sample streams honor the native short-circuited playing query.

Each samples_device channel has its own stream. While main is still playing,
the && guard never queries auxiliary. The last auxiliary stream update is the
last PCM callback; main additionally updates at the previous 60 Hz guard tick.
Do not fit either cutoff to the recorded waveform or channel positions.
"""
import inspect
from pathlib import Path
import launch_stage_advance_audio as previous

ROOT, need, sha = previous.ROOT, previous.need, previous.sha
samples = ROOT/'mame-mkp/src/devices/sound/samples.cpp'
need(sha(samples) == '8BF4BB350F40B309A5CECB4591DF8EE32A3563C3E061F2D2338C8CBA76B5353F',
     'Whole exact native separate-stream sample implementation')
text = samples.read_text()
need('chan.stream = stream_alloc(0, 1, SAMPLE_RATE_OUTPUT_ADAPTIVE);' in text and
     'chan.stream->update();\n\treturn (chan.source != nullptr);' in text,
     'Playing updates only the requested channel stream')
driver = ROOT/'source_v6636_kano_ball_launch/midtunit_m.cpp'
need('!m_mk2ks_voices->playing(10 + slot * 2) && !m_mk2ks_voices->playing(11 + slot * 2)' in driver.read_text(),
     'Original shared owner timer short-circuits auxiliary while main is playing')
source = inspect.getsource(previous.source_events)
before = '            update = max(max(updates), stop-period)'
after = """            update = max(updates) if sid == 15 else max(max(updates), stop-period)
            if sid == 15:
                main_start = clock.sample_clock(main['seconds'], True)
                previous_main = clock.sample_clock(str(Decimal(stop-period)/clock.ATTO), True)-main_start
                need(0 < previous_main < 40720, 'Main is still playing; actual source guard skips auxiliary update')"""
need(source.count(before) == 1, 'Only original auxiliary stream update selection changes')
scope = dict(vars(previous))
exec(compile(source.replace(before, after, 1), __file__+'::whole_separate_stream_source_clocks', 'exec'), scope)
exec(compile(inspect.getsource(previous.predict), __file__+'::whole_unchanged_native_waveform', 'exec'), scope)
predict, source_events, packet_gate = scope['predict'], scope['source_events'], previous.packet_gate
