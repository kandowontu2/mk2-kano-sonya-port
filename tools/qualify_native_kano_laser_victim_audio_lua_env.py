"""Retain failed native parser diagnostic; fix wrapper's explicitnil _ENV."""
from pathlib import Path
import qualify_native_kano_laser_victim_audio_lua as failed

source=Path(failed.__file__).read_text()
changes=[("OUT=ROOT/'audit_native_kano_laser_victim_audio_lua_source'",
          "OUT=ROOT/'audit_native_kano_laser_victim_audio_lua_env_source'"),
         ("'-autoboot_script',str(ROOT/'mk2ks_native_kano_laser_victim_parse.lua')",
          "'-autoboot_script',str(ROOT/'mk2ks_native_kano_laser_victim_parse_env.lua')"),
         ('paths=[Path(__file__),',
          'paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_victim_audio_lua.py",'
          'ROOT/"mk2ks_native_kano_laser_victim_audio_env.lua",ROOT/"mk2ks_native_kano_laser_victim_parse_env.lua",'
          'ROOT/"audit_native_kano_laser_victim_audio_lua_source/victim4/native_exit.json",')]
for old,new in changes:
    failed.need(source.count(old)==1,'Exact retained native parser correction boundary')
    source=source.replace(old,new)
exec(compile(source,str(Path(__file__).resolve()),'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
