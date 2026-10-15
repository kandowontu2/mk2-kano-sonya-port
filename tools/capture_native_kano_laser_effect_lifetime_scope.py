"""Correct only passive Lua lexical scope; preserve failed native evidence.

Actual physical controller unchanged. Use a real interactive terminal for
RAM visual review, never -i on a pipe. Original game must exit naturally.
"""
import code
import inspect
import json
from pathlib import Path

import capture_native_kano_laser_effect_lifetime as prior

ROOT=prior.ROOT
LUA=ROOT/'mk3_native_kano_laser_effect_lifetime_scope.lua'
reference=prior.reference


def transformed():
    source=prior.transformed()
    edits=[('local laser_effect_jobs,laser_effect_objects,laser_effect_serial={},{},0',
            'local valid,log\nlocal laser_effect_jobs,laser_effect_objects,laser_effect_serial={},{},0'),
           ('local function valid(a)','function valid(a)'),
           ('local function log(tag,content)','function log(tag,content)')]
    for old,new in edits:
        reference.need(source.count(old)==1,'Only exact passive lexical binding changes')
        source=source.replace(old,new)
    reference.LUA=LUA
    return source


def run():
    failed=ROOT/'audit_native_kano_laser_effect_lifetime/report.json'
    report=json.loads(failed.read_text())
    reference.need(not report['passed'] and report['nativeExit']==0 and
        all(reference.sha(p)==h for p,h in report['inputHashes'].items()) and
        "global 'valid'" in (failed.parent/'stderr.log').read_text(),
        'Actual failed observer/native exit0 and all executed inputs preserved')
    source=inspect.getsource(prior.run)
    source=source.replace("reference.OUT=ROOT/'audit_native_kano_laser_effect_lifetime'",
                          "reference.OUT=ROOT/'audit_native_kano_laser_effect_lifetime_scope'")
    old="ROOT/'audit_native_kano_laser_palette_trace/report.json']"
    new="ROOT/'audit_native_kano_laser_palette_trace/report.json',ROOT/'mk3_native_kano_laser_effect_lifetime.lua',ROOT/'tools/capture_native_kano_laser_effect_lifetime.py',ROOT/'audit_native_kano_laser_effect_lifetime/report.json',ROOT/'audit_native_kano_laser_effect_lifetime/stderr.log',ROOT/'audit_native_kano_laser_effect_lifetime/run.log.gz',ROOT/'audit_native_kano_laser_effect_lifetime/executed_sources.json.gz']"
    reference.need(source.count(old)==1,'Complete failed original controller provenance')
    source=source.replace(old,new)
    scope=dict(vars(prior),LUA=LUA,transformed=transformed,__file__=__file__)
    exec(compile(source,__file__+'::scoped_original_run','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    capture=run();server=prior.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Actual original effect reference terminal; full native rasters retained in RAM.',local=dict(capture=capture,server=server))
