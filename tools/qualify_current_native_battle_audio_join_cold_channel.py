"""Account for samples_device cold source_num ordering, require actual clip progression."""
from pathlib import Path
source=Path(__file__).with_name('qualify_current_native_battle_audio_join_selection.py').read_text()
source=source.replace('import copy\n','import copy\nimport wave\n')
old="assert len(first)==1 and int(first[0]['length'])>0 and int(first[0]['sample'])==14"
assert source.count(old)==1
new='''assert len(first)==1 and int(first[0]['sample']) in (14,4294967295)
 clip=sync.ROOT/'diagnostic_native_selector_layers_long/samples/mk2ks/sonya_bicycle_launch.wav'
 if not clip.exists():clip=sync.ROOT/'samples/mk2ks/sonya_bicycle_launch.wav'
 with wave.open(str(clip)) as wav:clip_length=wav.getnframes()
 assert int(first[0]['length'])==clip_length
 early=[r for r in rows['JOIN_CHANNEL'] if r['channel']=='10' and int(r['age'])<=2]
 assert len(early)==3 and all(r['paused']==r['loop']=='0' for r in early)
 assert all(float(b['pos'])>float(a['pos']) for a,b in zip(early,early[1:]))
 implementation=(sync.ROOT/'mame-mkp/src/devices/sound/samples.cpp').read_text()
 assert 'chan.source_num = (chan.source_len > 0) ? samplenum : -1;' in implementation'''
source=source.replace(old,new)
source=source.replace('audit_current_native_battle_audio_join_selection_checked','audit_current_native_battle_audio_join_cold_channel_checked')
exec(compile(source,__file__+'::cold loader bookkeeping','exec'),{'__name__':'__main__'})
