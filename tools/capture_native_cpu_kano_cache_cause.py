"""Cold replay original buttons; stop only after actual corruption is observed."""
import json
import capture_native_sonya_p1_postending_kano as base
base.OUT=base.ROOT/'audit_native_cpu_kano_cache_cause'
base.LUA='mk2ks_native_cpu_kano_cache_cause.lua'
base.CONTROLLERS=[base.LUA,*base.CONTROLLERS]
original_source=base.capture_source
def diagnostic_source():
    source=original_source()
    before=" need(not overruns,'No original cache writes into global state')"
    after=" need(overruns and 'MK2_KANO_CACHE_CAUSE_STOP ' in chronology,'Actual original corrupting chain and finite native exit; diagnostic only')"
    base.need(source.count(before)==1,'Exact transport-only diagnostic boundary')
    return source.replace(before,after,1)
base.capture_source=diagnostic_source
if __name__=='__main__':
    capture=base.run()
    print(json.dumps(dict(nativeExit=capture['result']['nativeExit'],
        confirmedCorruption=capture['result']['nativeCacheOverrunObserved'],
        diagnosticOnly=True,fullPortAcceptance=False)),flush=True)
