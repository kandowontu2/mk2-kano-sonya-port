"""One genuine earned laser trial; actual guest/RGB kept in RAM.

Reuse immutable actual-PID/terminal/whole-buffer transport, never save states
or guest assistance. A transport pass does not accept activation/art/audio.
"""
import argparse
import code
import inspect
import json
from types import SimpleNamespace
import capture_native_sonya_orb_worker_lifetime as transport
import qualify_native_kano_laser_action_routes as qualified

ROOT=qualified.ROOT
NAME='diagnostic_native_kano_laser_action'
LUA=ROOT/'mk2ks_native_kano_laser_action.lua'
need,sha=qualified.initial.need,qualified.initial.sha


def providers():
    g=qualified.initial.gate
    base=g.prior.phases.palette.prior.prior.prior.prior.prior.prior.visual.prior.expected()
    payload=g.prior.phases.palette.prior.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
    return base,payload


def functions():
    expected=inspect.getsource(transport.expected)
    old='base=source.prior.prior.prior.prior.prior.visual.prior.expected();payload=source.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()'
    need(expected.count(old)==1,'Exact shared source/payload provider boundary')
    expected=expected.replace(old,'base,payload=providers()')
    run=inspect.getsource(transport.run)
    changes=[('audit_native_sonya_orb_worker_lifetime_p{side}','audit_native_kano_laser_action_p{side}'),
             ("env['MK2KS_ORB_SIDE']","env['MK2KS_LASER_SIDE']")]
    for old,new in changes:
        need(run.count(old)==1,'Exact finite physical-controller/candidate transport boundary');run=run.replace(old,new)
    run=run.replace('MK2_ORB_','MK2_LASER_')
    scope=dict(vars(transport),ROOT=ROOT,NAME=NAME,LUA=LUA,need=need,sha=sha,providers=providers,
        __file__=__file__,source=SimpleNamespace(OUT=qualified.OUT,__file__=qualified.__file__))
    exec(compile(expected,__file__+'::whole_actual_guest_expectation','exec'),scope)
    exec(compile(run,__file__+'::same_native_handle_transport','exec'),scope)
    return scope['run']


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    capture=functions()(args.side);server=transport.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Same native trial terminal; complete actual rasters retained in RAM.',local=dict(capture=capture,server=server))
