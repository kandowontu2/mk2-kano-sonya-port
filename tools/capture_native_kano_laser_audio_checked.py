"""Require actual Lua-parser/physical-callback evidence before native capture."""
import argparse
import code
import json
from pathlib import Path
import capture_native_kano_laser_audio as original

ROOT,need,sha=original.ROOT,original.need,original.sha


def run(side):
    guard_path=ROOT/'audit_native_kano_laser_audio_lua_headers_source/report.json'
    guard=json.loads(guard_path.read_text())
    need(guard['passed'] and guard['actualNativeLuaParserAccepted'] and guard['wholePhysicalCallbackByteIdentical'] and
         guard['totalSampleChannels']==19 and not guard['nativeGameplayAccepted'],
         'Actual native Lua source qualification, not fabricated gameplay evidence')
    pins=dict(guard['inputHashes'])
    for path in (guard_path,Path(__file__),Path(original.__file__)):
        pins[str(path.resolve())]=sha(path)
    need(all(sha(p)==h for p,h in pins.items()),'Entire executed audio/physical observer sources immutable')
    runner=original.functions()
    runner.__globals__['__file__']=__file__
    capture=runner(side)
    need(all(sha(p)==h for p,h in pins.items()),'Same complete observer sources conserved through actual native terminal')
    (capture['folder']/'checked_observer_sources.json').write_text(json.dumps(dict(passed=True,sourceOnlyGuard=True,
        nativeAudioAccepted=False,inputHashes=pins,totalSampleChannels=19,goalStatus='active',latestPlayableChanged=False),indent=2)+'\n')
    return capture


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    capture=run(args.side);server=original.transport.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']),pcmCallbacks=len(capture['pcm']))),flush=True)
    code.interact(banner='Same native trial terminal; whole rasters/PCM/DAC retained in RAM.',local=dict(capture=capture,server=server))
