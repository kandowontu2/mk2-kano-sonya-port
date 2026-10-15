"""Earn original laser with preserved physical inputs; whole RGB stays in RAM."""
import code
import inspect
import json
import re
from pathlib import Path
import capture_native_secondary_kano_source_distance as distance
from capture_native_sonya_orb_worker_wall import serve

reference=distance.reference
ROOT=reference.ROOT
LUA=ROOT/'mk3_native_kano_laser_burst_pipeline.lua'


def transformed():
    reference.LUA=ROOT/'mk3_native_secondary_kano_source_distance.lua'
    baseline=distance.transformed()
    wrapper=LUA.read_text()
    opening='local additions={'
    start=wrapper.index(opening)+len(opening)
    end=wrapper.index('\n}\nfor _,pair',start)
    block=wrapper[start:end]
    pairs=re.findall(r'\{"([^"\n]+)",\s*\[=\[(.*?)\]=\]\}',block,re.S)
    pairs+=re.findall(r"\{'([^'\n]+)',\s*'([^'\n]+)'\}",block)
    reference.need(len(pairs)==3,'Exactly three passive original observer boundaries')
    result=baseline
    for old,new in pairs:
        reference.need(result.count(old)==1,'Unique unchanged physical controller boundary')
        result=result.replace(old,new)
    restored=result
    for old,new in reversed(pairs):
        reference.need(restored.count(new)==1,'Exact reversible passive observer boundary')
        restored=restored.replace(new,old)
    reference.need(restored==baseline,'Whole physical selection/combat/command callback unchanged')
    reference.LUA=LUA
    return result


def run():
    previous=ROOT/'audit_native_secondary_kano_source_distance/report.json'
    record=json.loads(previous.read_text())
    reference.need(record['passed'] and record['nativeExit']==0 and
        all(reference.sha(p)==h for p,h in record['inputHashes'].items()),
        'Original earned source-distance reference terminal and conserved')
    reference.OUT=ROOT/'audit_native_kano_laser_original_burst_pipeline'
    transformed()
    source=inspect.getsource(reference.run)
    old='source=LUA.read_text()'
    reference.need(source.count(old)==1,'Exact original native controller guard')
    source=source.replace(old,'source=transformed()')
    old="ROOT/'audit_native_secondary_finisher_reference/report.json']"
    new="ROOT/'audit_native_secondary_finisher_reference/report.json', ROOT/'mk3_native_secondary_kano_reference.lua', ROOT/'mk3_native_secondary_kano_source_distance.lua', ROOT/'tools/capture_native_secondary_kano_reference.py', ROOT/'tools/capture_native_secondary_kano_source_distance.py', ROOT/'tools/capture_native_sonya_orb_worker_wall.py', ROOT/'audit_native_secondary_kano_source_distance/report.json']"
    reference.need(source.count(old)==1,'Complete immutable original input provenance')
    source=source.replace(old,new)
    scope=dict(vars(reference),transformed=transformed,__file__=__file__)
    exec(compile(source,__file__+'::original_burst_pipeline','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    capture=run();server=serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Same original game terminal; whole original burst rasters in RAM.',local=dict(capture=capture,server=server))
