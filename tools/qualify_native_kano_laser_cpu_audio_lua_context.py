"""Retain failed diagnostic; original Sonya fixture requires limit18000."""
from pathlib import Path
import qualify_native_kano_laser_cpu_audio_lua as prior
source=Path(prior.__file__).read_text()
for old,new in [
    ("OUT=ROOT/'audit_native_kano_laser_cpu_audio_lua_source'","OUT=ROOT/'audit_native_kano_laser_cpu_audio_lua_context_source'"),
    ("MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'","MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'"),
    ("str(ROOT/'mk2ks_native_kano_laser_cpu_parse.lua')","str(ROOT/'mk2ks_native_kano_laser_cpu_parse_context.lua')"),
    ('paths=[Path(__file__),','paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_cpu_audio_lua.py",ROOT/"mk2ks_native_kano_laser_cpu_parse_context.lua",ROOT/"audit_native_kano_laser_cpu_audio_lua_source/native_exit.json",')]:
    prior.need(source.count(old)==1,'Exact retained parser/context successor boundary');source=source.replace(old,new)
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
