"""Use real source-qualified Sonya controller limit; preserve first sources."""
from pathlib import Path
import capture_native_kano_laser_cpu_audio as prior
source=Path(prior.__file__).read_text()
for old,new in [
    ("audit_native_kano_laser_cpu_audio_lua_source/report.json","audit_native_kano_laser_cpu_audio_lua_context_source/report.json"),
    ("MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'","MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'")]:
    prior.need(source.count(old)==1,'Exact qualified CPU host context');source=source.replace(old,new)
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
