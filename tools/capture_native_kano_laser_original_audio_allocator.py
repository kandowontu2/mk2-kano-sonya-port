"""Same actual original game; passive whole five-slot sound state only."""
import code
import inspect
import json
import re
import capture_native_kano_laser_original_burst_pipeline as prior

ROOT=prior.ROOT
reference=prior.reference
LUA=ROOT/'mk3_native_kano_laser_audio_allocator.lua'


def transformed():
    source=prior.transformed()
    opening='local additions={'
    wrapper=LUA.read_text();start=wrapper.index(opening)+len(opening)
    end=wrapper.index('\n}\nfor _,pair',start)
    pairs=re.findall(r'\{"([^"\n]+)",\s*\[=\[(.*?)\]=\]\}',wrapper[start:end],re.S)
    reference.need(len(pairs)==1,'One passive sound-allocator observer insertion')
    before=source
    for old,new in pairs:
        reference.need(source.count(old)==1,'Unique existing passive source-code tap boundary')
        source=source.replace(old,new)
    reference.need(source.replace(pairs[0][1],pairs[0][0])==before,
                   'Whole selection/combat/command and raster callback byte-identical')
    reference.LUA=LUA
    return source


def run():
    receipt=ROOT/'audit_native_kano_laser_original_burst_pipeline/report.json'
    record=json.loads(receipt.read_text())
    reference.need(record['passed'] and record['nativeExit']==0 and
        all(reference.sha(p)==h for p,h in record['inputHashes'].items()),
        'Actual original burst reference terminal and conserved')
    source=inspect.getsource(prior.run)
    old="reference.OUT=ROOT/'audit_native_kano_laser_original_burst_pipeline'"
    reference.need(source.count(old)==1,'Fresh actual native original allocator audit')
    source=source.replace(old,"reference.OUT=ROOT/'audit_native_kano_laser_original_audio_allocator'")
    old="ROOT/'audit_native_secondary_kano_source_distance/report.json']"
    new="ROOT/'audit_native_secondary_kano_source_distance/report.json', ROOT/'tools/capture_native_kano_laser_original_burst_pipeline.py', ROOT/'mk3_native_kano_laser_burst_pipeline.lua', ROOT/'audit_native_kano_laser_original_burst_pipeline/report.json']"
    reference.need(source.count(old)==1,'All original physical and nested observer provenance')
    source=source.replace(old,new)
    scope=dict(vars(prior),LUA=LUA,transformed=transformed,__file__=__file__)
    exec(compile(source,__file__+'::original_native_allocator_run','exec'),scope)
    return scope['run']()


if __name__=='__main__':
    capture=run();server=prior.serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Same original audio allocator test terminal; full actual rasters retained in RAM.',local=dict(capture=capture,server=server))
