"""Preserve failed shallow matcher; demand the actual complete controller."""
from pathlib import Path
import qualify_native_kano_laser_cpu_audio_lua as prior
wrapper=(prior.ROOT/'tools/qualify_native_kano_laser_cpu_motion_audio_lua.py').read_text()
changes=[
    ("audit_native_kano_laser_cpu_motion_audio_lua_source","audit_native_kano_laser_cpu_motion_audio_lua_full_source"),
    ("str(ROOT/'mk2ks_native_kano_laser_cpu_motion_parse.lua')","str(ROOT/'mk2ks_native_kano_laser_cpu_motion_parse_full.lua')"),
    ('paths=[Path(__file__),ROOT/', 'paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_cpu_motion_audio_lua.py",ROOT/"mk2ks_native_kano_laser_cpu_motion_parse_full.lua",ROOT/"audit_native_kano_laser_cpu_motion_audio_lua_source/native_exit.json",ROOT/'),
    ("'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO']",
     "len(parts['MK2_CPU_PARSE_CAMPAIGN'])>30000 and 'if mode==2 and state==1 and p:read_u16(slots[opponent].state)==0 and human and other and human.owner==human.actor and other.owner==other.actor then' in parts['MK2_CPU_PARSE_CAMPAIGN'] and 'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO']")]
for old,new in changes:
    prior.need(wrapper.count(old)==1,'Exact retained shallow-source matcher correction');wrapper=wrapper.replace(old,new)
exec(compile(wrapper,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
