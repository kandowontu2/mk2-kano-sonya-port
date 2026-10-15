"""Same full carrier; normal first-loss Kano reselect, never forced CPU choice."""
from pathlib import Path
import capture_native_kano_laser_cpu_audio as prior
source=Path(prior.__file__).read_text()
changes=[
    ("LUA=ROOT/'mk2ks_native_kano_laser_cpu_audio.lua'","LUA=ROOT/'mk2ks_native_kano_laser_cpu_continue_audio.lua'"),
    ("CONTROLLERS=[LUA,","CONTROLLERS=[LUA,ROOT/'mk2ks_native_kano_laser_cpu_continue.lua',"),
    ("audit_native_kano_laser_cpu_audio_lua_source/report.json","audit_native_kano_laser_cpu_continue_audio_lua_source/report.json"),
    ("out=ROOT/'audit_native_kano_laser_cpu_audio'","out=ROOT/'audit_native_kano_laser_cpu_continue_audio'"),
    ("MK2KS_CAMPAIGN_OBSERVER_LIMIT='5900'","MK2KS_CAMPAIGN_OBSERVER_LIMIT='18000'"),
    ('    runner=original.functions()\n    source=inspect.getsource(runner)',
     '''    factory=inspect.getsource(original.functions)
    need(factory.count("return scope['run']")==1,'Whole generated native carrier boundary')
    factory=factory.replace("return scope['run']","return run,scope")
    generated=dict(vars(original),__file__=__file__)
    exec(compile(factory,__file__+'::generated_full_audio_carrier','exec'),generated)
    source,runner_scope=generated['functions']()'''),
    ('scope=dict(runner.__globals__,__file__=__file__,LUA=LUA)','scope=dict(runner_scope,__file__=__file__,LUA=LUA)')]
for old,new in changes:
    prior.need(source.count(old)==1,'Exact whole passive audio and physical-first-loss carrier');source=source.replace(old,new)
exec(compile(source,__file__,'exec'),dict(__name__='__main__',__file__=str(Path(__file__).resolve())))
