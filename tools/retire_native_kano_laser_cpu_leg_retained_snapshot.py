"""Exact session retirement with the policy-blocked automatic snapshot retained.

Do not retry or bypass the rejected deletion. Preserve the actual exception
and report one remaining 51,674-byte generated screenshot, never zero media.
"""
import inspect
import json
import retire_native_kano_laser_cpu_leg_ram as prior


def run():
    source=inspect.getsource(prior.run)
    def once(before,after):
        nonlocal source
        prior.need(source.count(before)==1,'Exact retained-screenshot outcome adaptation: '+before[:90])
        source=source.replace(before,after,1)
    once("need(before['sha256']==SCREEN_SHA and not SCREEN.exists(),'Only exact generated timeout screenshot removed')",
         "need(before['sha256']==SCREEN_SHA and SCREEN.exists() and sha(SCREEN)==SCREEN_SHA,'Exact generated screenshot retained unchanged after policy-rejected deletion')")
    once("need(not any(p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')for p in files),\n         'No raw media/ROM/build/archive remains in this pass evidence')",
         "need([p for p in files if p.suffix.lower()in('.png','.wav','.bin','.exe','.zip')]==[SCREEN],\n         'Only exact policy-retained timeout screenshot remains; no raw ROM/audio/build/archive')")
    once("oneGeneratedNativeTimeoutScreenshotRemoved=True,removedSnapshotSHA256=SCREEN_SHA,removedSnapshotBytes=51674,",
         "oneGeneratedNativeTimeoutScreenshotRemoved=False,generatedScreenshotRetainedDueToPolicy=True,retainedTimeoutScreenshotSHA256=SCREEN_SHA,retainedTimeoutScreenshotBytes=51674,")
    once("removalRecovery='Discarded generated diagnostic screenshot; hash/provenance retained, no user source or ROM removed',",
         "cleanupOutcome='Deletion command rejected by tool policy; no alternate deletion attempted. Exact generated screenshot retained; no user source or ROM removed.',")
    once('rawMediaFilesRemaining=0,generatedBuildCachePresent=False',
         'rawMediaFilesRemaining=1,generatedBuildCachePresent=False')
    once('generatedTimeoutScreenshotRemoved=True,publicPlayableChanged=False',
         'generatedTimeoutScreenshotRemoved=False,generatedTimeoutScreenshotRetainedDueToPolicy=True,publicPlayableChanged=False')
    once("pins={str(p.resolve()):sha(p)for p in (Path(__file__),diagnostic,first,compiler,OUT/'timeout_snapshot_before_cleanup.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd')}",
         "pins={str(p.resolve()):sha(p)for p in (Path(__file__),Path(prior_source_file),SCREEN,diagnostic,first,compiler,OUT/'timeout_snapshot_before_cleanup.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd')}")
    scope=dict(vars(prior),__file__=__file__,prior_source_file=prior.__file__)
    exec(compile(source,__file__+'::whole_exact_session_retirement_with_retained_policy_exception','exec'),scope)
    scope['run']()


if __name__=='__main__':run()
