"""Real installed parser for native first-loss continue and own CPU origin."""
from pathlib import Path
import qualify_native_kano_laser_cpu_audio_lua as prior
source=Path(prior.__file__).read_text()
changes=[
    ("OUT=ROOT/'audit_native_kano_laser_cpu_audio_lua_source'","OUT=ROOT/'audit_native_kano_laser_cpu_continue_audio_lua_source'"),
    ("MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'","MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'"),
    ("str(ROOT/'mk2ks_native_kano_laser_cpu_parse.lua')","str(ROOT/'mk2ks_native_kano_laser_cpu_continue_parse.lua')"),
    ('paths=[Path(__file__),','paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_cpu_audio_lua.py",ROOT/"mk2ks_native_kano_laser_cpu_continue_parse.lua",ROOT/"mk2ks_native_kano_laser_cpu_continue.lua",ROOT/"mk2ks_native_kano_laser_cpu_continue_audio.lua",'),
    ("'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO']", "'frame==origin+751' in parts['MK2_CPU_PARSE_AUDIO'] and '_mk2_cpu_laser_started then return end' in parts['MK2_CPU_PARSE_AUDIO'] and '_mk2_cpu_after_first_loss then _cpu_laser_followup(frame)' in parts['MK2_CPU_PARSE_CAMPAIGN']")]
for old,new in changes:
    prior.need(source.count(old)==1,'Exact installed-parser successor for normal continues');source=source.replace(old,new)
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
