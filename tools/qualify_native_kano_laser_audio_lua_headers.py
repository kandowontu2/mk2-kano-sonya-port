"""Retain the first parser compile failure; supply its missing C++ header."""
from pathlib import Path
import qualify_native_kano_laser_audio_lua as failed

source=Path(failed.__file__).read_text()
changes=[("OUT=ROOT/'audit_native_kano_laser_audio_lua_source'",
          "OUT=ROOT/'audit_native_kano_laser_audio_lua_headers_source'"),
         ("cpp=ROOT/'tools/validate_native_kano_laser_audio_lua.cpp'",
          "cpp=ROOT/'tools/validate_native_kano_laser_audio_lua_headers.cpp'"),
         ('files=[Path(__file__),cpp,lua,',
          'files=[Path(__file__),ROOT/"tools/qualify_native_kano_laser_audio_lua.py",'
          'ROOT/"tools/validate_native_kano_laser_audio_lua.cpp",'
          'ROOT/"audit_native_kano_laser_audio_lua_source/compiler.log",cpp,lua,')]
for old,new in changes:
    failed.need(source.count(old)==1,'Exact retained parser-source boundary')
    source=source.replace(old,new)
exec(compile(source,str(Path(__file__).resolve()),'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
