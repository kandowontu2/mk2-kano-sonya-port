"""Frozen selection; compatible raster ABI and attainable input spacing."""
import code
import inspect
import json
import capture_native_secondary_kano_reference as previous

previous.OUT=previous.ROOT/'audit_native_secondary_kano_raster_checked'
previous.LUA=previous.ROOT/'mk3_native_secondary_kano_raster_checked.lua'

def run():
    root=previous.ROOT
    preserved=json.loads((root/'audit_native_secondary_kano_reference/raster_observer_failure.json').read_text())
    previous.need(preserved['passed']and not preserved['failedNativeRunAccepted']and
                  all(previous.sha(p)==h for p,h in preserved['inputHashes'].items()),'Actual failed executed controller frozen before repair')
    original=root/'mk3_native_secondary_kano_reference.lua'
    baseline=original.read_text()
    failure=json.loads((root/'audit_native_secondary_kano_reference/report.json').read_text())
    previous.need(not failure['passed'] and failure['nativeExit']==0 and failure['originalWholeGuestMatched'] and
                  all(previous.sha(p)==h for p,h in failure['inputHashes'].items()),
                  'Original failed observation/physical input run terminal0, original program and source conserved')
    before="local raw,w,h=machine.screens[':screen']:pixels()"
    after="local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"
    previous.need(baseline.count(before)==1,'Only one actual old raster ABI boundary')
    close_before='if gap>45 then press(forward)'
    close_after='if gap>65 then press(forward)'
    previous.need(baseline.count(close_before)==1,'Only ordinary combat approach threshold, not finisher range or guest state')
    wrapper=previous.LUA.read_text()
    previous.need("local filename='mk3_native_secondary_kano_reference.lua'"in wrapper and
                  'local before='+json.dumps(before)in wrapper and 'local after='+json.dumps(after)in wrapper,
                  'Exact frozen input script, explicit single raster-only source replacement')
    previous.need("local close_before='"+close_before+"'"in wrapper and
                  "local close_after='"+close_after+"'"in wrapper,
                  'Exact physical attack spacing correction after actual59..63pixel native collision stall')
    source=inspect.getsource(previous.run)
    changes=(('source=LUA.read_text()',"source=(ROOT/'mk3_native_secondary_kano_reference.lua').read_text().replace("+repr(before)+','+repr(after)+').replace('+repr(close_before)+','+repr(close_after)+')'),
             ("ROOT/'audit_native_secondary_finisher_reference/report.json']",
              "ROOT/'audit_native_secondary_finisher_reference/report.json', ROOT/'mk3_native_secondary_kano_reference.lua', ROOT/'tools/capture_native_secondary_kano_reference.py', ROOT/'audit_native_secondary_kano_reference/report.json']"))
    for old,new in changes:
        previous.need(source.count(old)==1,'Unique source transformation/provenance location')
        source=source.replace(old,new)
    scope=dict(vars(previous),__file__=__file__)
    exec(compile(source,__file__+'::only_screen_dimensions','exec'),scope)
    return scope['run']()

if __name__=='__main__':
    capture=run()
    code.interact(banner='Original native reference terminal; compatible whole raster buffers in RAM.',local=dict(capture=capture))
