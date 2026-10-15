"""Preserve first diagnostic; isolate all explicit_G loaded parser callbacks."""
from pathlib import Path
import qualify_native_kano_laser_ui_lua as prior
source=Path(prior.__file__).read_text()
changes=[
    ("OUT=ROOT/'audit_native_kano_laser_ui_lua_source'","OUT=ROOT/'audit_native_kano_laser_ui_lua_globals_source'"),
    ("str(ROOT/'mk2ks_native_kano_laser_ui_parse.lua')","str(ROOT/'mk2ks_native_kano_laser_ui_parse_globals.lua')"),
    ('paths=[Path(__file__),','paths=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_ui_lua.py",ROOT/"mk2ks_native_kano_laser_ui_parse_globals.lua",ROOT/"audit_native_kano_laser_ui_lua_source/native_exit.json",')]
for old,new in changes:
    prior.need(source.count(old)==1,'Exact retained diagnostic/global namespace correction');source=source.replace(old,new)
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
