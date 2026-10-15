"""Same compiled game/controller; bind the metadata oracle to the actual new guest."""
import code,json
import capture_native_cpu_finisher_repair_regression as previous
base,fixed=previous.base,previous.fixed
base.OUT=base.ROOT/'audit_native_cpu_finisher_repair_regression_current_oracle'
def metadata_clean(errors,proof):
    fixed.need(errors=='' and proof and proof['sha256']==fixed.GUEST_SHA and
        proof['executableSHA256']==fixed.EXE_SHA and proof['payloadSHA256']==fixed.PAYLOAD_SHA and
        proof['everyActualByteComparedInRAM'] and proof['guestDumpFilesWritten']==0,
        'Actual current compiled executable/payload/whole guest and empty native error stream')
    return dict(metadataMatchesPayload=True,nativeStderrEmpty=True,releaseMetadataCorrectionStillRequired=False)
base.metadata_clean=metadata_clean
if __name__=='__main__':
    capture=base.run()
    print(json.dumps(dict(nativeExit=capture['result']['nativeExit'],
        cacheOverrun=capture['result']['nativeCacheOverrunObserved'],
        transportOnly=True,fullPortAcceptance=False)),flush=True)
    code.interact(banner='Actual same-game replay with current guest oracle; real native images retained in RAM.',local=dict(capture=capture))
