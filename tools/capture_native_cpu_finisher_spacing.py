"""One cold unchanged physical replay; actual gap/owned finish/native RGB in RAM."""
import code,json
import capture_native_cpu_finisher_repair_regression_checked as previous
import native_cpu_finisher_spacing_context as fixed
base=previous.base
base.native=fixed
base.OUT=base.ROOT/'audit_native_cpu_finisher_spacing'
base.LUA='mk2ks_native_cpu_finisher_spacing.lua'
base.CONTROLLERS=[base.LUA,*base.CONTROLLERS]
def metadata_clean(errors,proof):
    fixed.need(errors=='' and proof and proof['sha256']==fixed.GUEST_SHA and
        proof['executableSHA256']==fixed.EXE_SHA and proof['payloadSHA256']==fixed.PAYLOAD_SHA and
        proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten']==0,
        'Actual spacing-only compiled executable/payload/whole guest and empty native error stream')
    return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,releaseMetadataCorrectionStillRequired=False)
base.metadata_clean=metadata_clean
if __name__=='__main__':
    capture=base.run()
    print(json.dumps(dict(nativeExit=capture['result']['nativeExit'],
        cacheOverrun=capture['result']['nativeCacheOverrunObserved'],transportOnly=True,
        fullPortAcceptance=False)),flush=True)
    code.interact(banner='Actual dedicated-distance CPU finisher replay ended; native images retained in RAM.',
                 local=dict(capture=capture))
