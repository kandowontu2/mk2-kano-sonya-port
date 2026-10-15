"""Whole original physical replay against the independently qualified compiled fix."""
import code,json
import capture_native_sonya_p1_postending_kano as base
import native_cpu_finisher_dispatch_context as fixed
base.native=fixed
base.OUT=base.ROOT/'audit_native_cpu_finisher_repair_regression'
base.LUA='mk2ks_native_cpu_finisher_repair_regression.lua'
base.CONTROLLERS=[base.LUA,'mk2ks_native_cpu_kano_finish_lookup_cause.lua',
                  'mk2ks_native_cpu_kano_cache_cause.lua',*base.CONTROLLERS]
if __name__=='__main__':
    capture=base.run()
    print(json.dumps(dict(nativeExit=capture['result']['nativeExit'],
        cacheOverrun=capture['result']['nativeCacheOverrunObserved'],
        transportOnly=True,fullPortAcceptance=False)),flush=True)
    code.interact(banner='Actual compiled repair replay ended; native images remain in RAM for independent review.',local=dict(capture=capture))
