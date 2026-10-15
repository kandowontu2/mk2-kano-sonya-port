"""Correct the matcher on the actual assembled qualifier, retain first attempt."""
from pathlib import Path
import qualify_native_kano_laser_cpu_audio_lua as prior
wrapper=(prior.ROOT/'tools/qualify_native_kano_laser_cpu_motion_audio_lua.py').read_text()
boundary="exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))"
prior.need(wrapper.count(boundary)==1,'Exact earlier assembled qualifier execution boundary')
scope=dict(__file__=str(Path(__file__).resolve()))
exec(compile(wrapper.replace(boundary,'assembled_qualifier_source=source'),__file__+'::exact_old_qualifier_assembly','exec'),scope)
source=scope['assembled_qualifier_source']
changes=[
    ("OUT=ROOT/'audit_native_kano_laser_cpu_motion_audio_lua_source'","OUT=ROOT/'audit_native_kano_laser_cpu_motion_audio_lua_full_source'"),
    ("str(ROOT/'mk2ks_native_kano_laser_cpu_motion_parse.lua')","str(ROOT/'mk2ks_native_kano_laser_cpu_motion_parse_full.lua')"),
    ('paths=[Path(__file__),','paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_cpu_motion_audio_lua.py",ROOT/"tools/qualify_native_kano_laser_cpu_motion_audio_lua_full.py",ROOT/"mk2ks_native_kano_laser_cpu_motion_parse_full.lua",ROOT/"audit_native_kano_laser_cpu_motion_audio_lua_source/native_exit.json",'),
    ("'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO']",
     "len(parts['MK2_CPU_PARSE_CAMPAIGN'])>30000 and 'if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then' in parts['MK2_CPU_PARSE_CAMPAIGN'] and 'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO']")]
for old,new in changes:
    prior.need(source.count(old)==1,'Exact assembled full-source predicate correction');source=source.replace(old,new)
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
