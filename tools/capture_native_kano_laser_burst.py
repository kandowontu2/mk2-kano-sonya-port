"""Same physical controller; new private source-timed burst candidate."""
import argparse
import code
import inspect
import json
from types import SimpleNamespace
import capture_native_sonya_orb_worker_lifetime as transport
import capture_native_kano_laser_action as prior
import qualify_native_kano_laser_burst as qualified

ROOT=qualified.ROOT
NAME='diagnostic_native_kano_laser_burst'
LUA=ROOT/'mk2ks_native_kano_laser_burst.lua'
need,sha=qualified.need,qualified.sha
providers=prior.providers

def functions():
    need(sha(ROOT/'mk2ks_native_kano_laser_action.lua')=='87EFC01B55588A8F8FFC3BA9BE67B1AE57086BF97858FB4BB18F29C5E2A272DA',
         'Frozen actual physical controller conserved')
    parser_receipt=ROOT/'audit_native_kano_laser_burst_lua_env_source/report.json'
    parsed=json.loads(parser_receipt.read_text())
    need(parsed['passed'] and parsed['actualNativeLuaParserAccepted'] and parsed['wholePhysicalCallbackByteIdentical'] and
         all(sha(p)==h for p,h in parsed['inputHashes'].items()),'Actual full nested Lua expansion parsed, complete physical callback conserved')
    expected=inspect.getsource(transport.expected)
    old='base=source.prior.prior.prior.prior.prior.visual.prior.expected();payload=source.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()'
    need(expected.count(old)==1,'Exact expected source boundary');expected=expected.replace(old,'base,payload=providers()')
    run=inspect.getsource(transport.run)
    for old,new in [('audit_native_sonya_orb_worker_lifetime_p{side}','audit_native_kano_laser_burst_p{side}'),
                    ("env['MK2KS_ORB_SIDE']","env['MK2KS_LASER_SIDE']"),
                    ('paths=[Path(__file__),LUA,','paths=[Path(__file__),LUA,ROOT/\'mk2ks_native_kano_laser_action.lua\',ROOT/\'mk2ks_native_kano_laser_typed_epochs.lua\',ROOT/\'audit_native_kano_laser_burst_lua_env_source/report.json\',Path(prior.__file__),')]:
        need(run.count(old)==1,'Exact burst successor transport boundary');run=run.replace(old,new)
    run=run.replace('MK2_ORB_','MK2_LASER_')
    scope=dict(vars(transport),ROOT=ROOT,NAME=NAME,LUA=LUA,need=need,sha=sha,providers=providers,prior=prior,
        __file__=__file__,source=SimpleNamespace(OUT=qualified.OUT,__file__=qualified.__file__))
    exec(compile(expected,__file__+'::whole_actual_guest_expectation','exec'),scope)
    exec(compile(run,__file__+'::same_native_handle_transport','exec'),scope)
    return scope['run']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    capture=functions()(args.side);server=transport.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Same native trial terminal; complete actual rasters retained in RAM.',local=dict(capture=capture,server=server))
