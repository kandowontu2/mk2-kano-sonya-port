"""Successor unassisted wall test, before the real finish deadline expires."""
import argparse
import code
import inspect
import json
from pathlib import Path
import capture_native_sonya_orb_worker_wall as prior

ROOT=prior.ROOT
LUA=ROOT/'mk2ks_native_sonya_orb_worker_wall_earlier.lua'

def transformed():
    text=prior.LUA.read_text();wrapper=LUA.read_text()
    prior.need(text.count('frame-finish>=65')==1 and 'frame-finish>=45' in wrapper,
               'Only physical retreat starts20fields earlier')
    return text.replace('frame-finish>=65','frame-finish>=45')

def run(side):
    preserved=ROOT/'audit_native_sonya_orb_worker_wall_fixture_review/report.json'
    report=json.loads(preserved.read_text())
    prior.need(report['passed'] and report['fixtureFailurePreserved'] and not report['gameplayAccepted'] and
               all(prior.sha(p)==h for p,h in report['inputHashes'].items()),'Real expired finish fixture preserved')
    text=inspect.getsource(prior.run)
    swaps=[("out=ROOT/f'audit_native_sonya_orb_worker_wall_p{side}'", "out=ROOT/f'audit_native_sonya_orb_worker_wall_earlier_p{side}'"),
           ('controller=LUA.read_text()','controller=transformed()'),
           ("ROOT/'roms/mk2.zip',ROOT/'roms/mk2ks.zip',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']",
            "ROOT/'roms/mk2.zip',ROOT/'roms/mk2ks.zip',ROOT/'PLAY_LATEST_KANO_SONYA.cmd', ROOT/'mk2ks_native_sonya_orb_worker_wall.lua', ROOT/'tools/capture_native_sonya_orb_worker_wall.py', ROOT/'audit_native_sonya_orb_worker_wall_fixture_review/report.json']")]
    for old,new in swaps:
        prior.need(text.count(old)==1,'Exact physical/provenance successor boundary')
        text=text.replace(old,new)
    scope=dict(vars(prior),LUA=LUA,transformed=transformed,__file__=__file__)
    exec(compile(text,__file__+'::earlier_physical_retreat','exec'),scope)
    return scope['run'](side)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True)
    capture=run(parser.parse_args().side);server=prior.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Earlier physical wall test terminal; actual full rasters retained in RAM.',local=dict(capture=capture,server=server))
