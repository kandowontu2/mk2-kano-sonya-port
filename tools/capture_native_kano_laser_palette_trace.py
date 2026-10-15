"""Original laser: unchanged earned inputs, continuous palette lifecycle.

Freeze every previous controller and preserve this successor on execution.
Actual whole program/RGB retained in RAM; native handle observed to terminal.
"""
import code
import inspect
import json
from pathlib import Path
import capture_native_secondary_kano_source_distance as distance
from capture_native_sonya_orb_worker_wall import serve

reference=distance.reference
ROOT=reference.ROOT
LUA=ROOT/'mk3_native_kano_laser_palette_trace.lua'


def transformed():
    # Same preserved source-distance transform, with only passive observers.
    reference.LUA=ROOT/'mk3_native_secondary_kano_source_distance.lua'
    baseline=distance.transformed()
    wrapper=LUA.read_text()
    # Read the exact literal additions that the actual Lua wrapper applies.
    opening='local additions={'
    start=wrapper.index(opening)+len(opening)
    end=wrapper.index('\n}\nfor _,pair',start)
    import re
    block=wrapper[start:end]
    pairs=re.findall(r'\{"([^"\n]+)",\s*\[=\[(.*?)\]=\]\}',block,re.S)
    pairs+=re.findall(r"\{'([^'\n]+)', '([^'\n]+)'\}",block)
    reference.need(len(pairs)==3,'Exactly three literal passive instrumentation boundaries')
    for old,new in pairs:
        reference.need(baseline.count(old)==1,'Unique frozen original passive observer boundary')
        baseline=baseline.replace(old,new)
    reference.LUA=LUA
    return baseline


def run():
    previous=ROOT/'audit_native_secondary_kano_source_distance/report.json'
    report=json.loads(previous.read_text())
    reference.need(report['passed'] and report['nativeExit']==0 and
                   all(reference.sha(p)==h for p,h in report['inputHashes'].items()),
                   'Previous actual original reference remains terminal and byte-exact')
    reference.OUT=ROOT/'audit_native_kano_laser_palette_trace'
    transformed()
    source=inspect.getsource(reference.run)
    old='source=LUA.read_text()';reference.need(source.count(old)==1,'Exact original host boundary')
    source=source.replace(old,'source=transformed()')
    old="ROOT/'audit_native_secondary_finisher_reference/report.json']"
    new="ROOT/'audit_native_secondary_finisher_reference/report.json', ROOT/'mk3_native_secondary_kano_reference.lua', ROOT/'mk3_native_secondary_kano_source_distance.lua', ROOT/'tools/capture_native_secondary_kano_reference.py', ROOT/'tools/capture_native_secondary_kano_source_distance.py', ROOT/'tools/capture_native_sonya_orb_worker_wall.py', ROOT/'audit_native_secondary_kano_source_distance/report.json']"
    reference.need(source.count(old)==1,'Exact complete provenance boundary')
    source=source.replace(old,new)
    scope=dict(vars(reference),transformed=transformed,__file__=__file__)
    exec(compile(source,__file__+'::laser_palette_trace','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    capture=run();server=serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Original laser reference terminal; actual full rasters retained in RAM.',local=dict(capture=capture,server=server))
