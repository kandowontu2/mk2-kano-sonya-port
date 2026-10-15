"""Same native whole audio carrier; source-qualified Kitana/Kano opponents."""
import argparse
import code
import inspect
import json
from pathlib import Path
import capture_native_kano_laser_audio as original

ROOT,need,sha=original.ROOT,original.need,original.sha


def run(side,victim):
    need(victim in (4,17),'Only the actually source-qualified opponent variants')
    guard_path=ROOT/'audit_native_kano_laser_victim_audio_lua_env_source/report.json'
    guard=json.loads(guard_path.read_text())
    need(guard['passed'] and guard['actualNativeLuaParserAccepted'] and not guard['nativeGameplayAccepted'] and
         any(r['victimID']==victim and r['physicalChangedIdentityConstantsOnly'] and r['audioByteIdentical'] for r in guard['cases']),
         'Actual native parser and exact physical-constant conservation, not gameplay proof')
    pins=dict(guard['inputHashes'])
    for path in (guard_path,Path(__file__),Path(original.__file__)):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Every qualified actual controller/native candidate input unchanged')
    source=inspect.getsource(original.functions)
    changes=[('def functions():','def functions(victim):'),
             ('audit_native_kano_laser_audio_p{side}','audit_native_kano_laser_audio_p{side}_victim{victim}'),
             ('scope=dict(vars(transport),','scope=dict(vars(transport),victim=victim,'),
             ("(\"env['MK2KS_ORB_SIDE']\",\"env['MK2KS_LASER_SIDE']\"),",
              "(\"env['MK2KS_ORB_SIDE']=str(side)\",\"env['MK2KS_LASER_SIDE']=str(side);env['MK2KS_LASER_VICTIM']=str(victim)\"),")]
    for old,new in changes:
        need(source.count(old)==1,'Exact original immutable whole transport adaptation');source=source.replace(old,new)
    scope=dict(vars(original),__file__=__file__,LUA=ROOT/'mk2ks_native_kano_laser_victim_audio_env.lua')
    exec(compile(source,__file__+'::whole_native_victim_transport','exec'),scope)
    capture=scope['functions'](victim)(side);capture['victimID']=victim
    need(all(sha(p)==h for p,h in pins.items()),'Complete actual observers/candidate conserved through same native terminal')
    (capture['folder']/'checked_observer_sources.json').write_text(json.dumps(dict(passed=True,sourceOnlyGuard=True,
        nativeAudioAccepted=False,inputHashes=pins,totalSampleChannels=19,victimID=victim,goalStatus='active',latestPlayableChanged=False),indent=2)+'\n')
    return capture


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True)
    parser.add_argument('--victim',type=int,choices=(4,17),required=True);args=parser.parse_args()
    capture=run(args.side,args.victim);server=original.transport.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']),pcmCallbacks=len(capture['pcm']),victimID=args.victim)),flush=True)
    code.interact(banner='Same actual victim trial terminal; whole rasters/PCM/DAC remain in RAM.',local=dict(capture=capture,server=server))
