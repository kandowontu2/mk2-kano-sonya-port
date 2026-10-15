"""Only the actually fully expanded/compiled normal-motion source guard."""
from pathlib import Path
import capture_native_kano_laser_cpu_audio as prior
source=(prior.ROOT/'tools/capture_native_kano_laser_cpu_motion_audio.py').read_text()
old='audit_native_kano_laser_cpu_motion_audio_lua_source/report.json'
prior.need(source.count(old)==1,'Exact full-source guard successor')
source=source.replace(old,'audit_native_kano_laser_cpu_motion_audio_lua_full_source/report.json')
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
