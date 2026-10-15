"""Confirm actual real-ID fatality lookup before staging any game correction."""
import json
import capture_native_cpu_kano_cache_cause as previous
base=previous.base
base.OUT=base.ROOT/'audit_native_cpu_kano_finish_lookup_cause'
base.LUA='mk2ks_native_cpu_kano_finish_lookup_cause.lua'
base.CONTROLLERS=[base.LUA,*base.CONTROLLERS]
if __name__=='__main__':
    capture=base.run()
    print(json.dumps(dict(nativeExit=capture['result']['nativeExit'],
        confirmedCorruption=capture['result']['nativeCacheOverrunObserved'],
        diagnosticOnly=True,fullPortAcceptance=False)),flush=True)
