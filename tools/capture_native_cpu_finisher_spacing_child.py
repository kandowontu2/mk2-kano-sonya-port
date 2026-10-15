"""Same game and physical replay; independently read attached skeleton ownership."""
import code,json
import capture_native_cpu_finisher_spacing as previous
base=previous.base
base.OUT=base.ROOT/'audit_native_cpu_finisher_spacing_child'
base.LUA='mk2ks_native_cpu_finisher_spacing_child.lua'
base.CONTROLLERS=[base.LUA,*base.CONTROLLERS]
if __name__=='__main__':
    capture=base.run()
    print(json.dumps(dict(nativeExit=capture['result']['nativeExit'],
        cacheOverrun=capture['result']['nativeCacheOverrunObserved'],transportOnly=True,
        fullPortAcceptance=False)),flush=True)
    code.interact(banner='Actual independent finisher child-link replay; native images retained in RAM.',
                 local=dict(capture=capture))
