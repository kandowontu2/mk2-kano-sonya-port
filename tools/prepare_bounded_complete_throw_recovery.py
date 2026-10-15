"""Last actual non-idle fields through the first persistent paired idle."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    proofpath=root/'audit_bounded_cross_throw_recovery_end/report.json'
    proof=json.loads(proofpath.read_text());assert proof['passed']
    assert all(r['firstPersistentPairedIdleAge']==183 for r in proof['results'].values())
    old=root/'audit_bounded_viewport_throw_footprint_preparation'
    out=root/'audit_bounded_complete_throw_recovery_preparation';assert not out.exists()
    lua=(old/'landing_observer.lua').read_text()
    needle='frame-ready>=145 and frame-ready<=176';assert lua.count(needle)==2
    lua=lua.replace(needle,'frame-ready>=177 and frame-ready<=183')
    out.mkdir();target=out/'recovery_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}_landing.ps1').read_text()
        runner=runner.replace(old.name+'/landing_observer.lua',out.name+'/'+target.name)
        runner=runner.replace(sync.sha(old/'landing_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_viewport_throw_landing_runtime',
                              f'audit_bounded_{fighter}_complete_throw_recovery_runtime')
        (out/f'run_{fighter}_recovery.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,
        captureAges=[177,183],recoveryEndProofSha256=sync.sha(proofpath),observerSha=sync.sha(target))))

if __name__=='__main__':main()
