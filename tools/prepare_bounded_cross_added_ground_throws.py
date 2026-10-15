"""Both true added fighters selected normally; ordinary close LowPunch."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_ground_throw_dispatch_preparation'
    out=root/'audit_bounded_cross_added_ground_throw_preparation';assert not out.exists()
    out.mkdir();target=out/'prepared_observer.lua'
    target.write_text((old/'prepared_observer.lua').read_text())
    for fighter,victim in (('sonya','kano'),('kano','sonya')):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        needle="$env:MK2KS_HUMAN_SPECIAL_VICTIM='kitana'"
        assert runner.count(needle)==1
        runner=runner.replace(needle,f"$env:MK2KS_HUMAN_SPECIAL_VICTIM='{victim}'")
        runner=runner.replace(f'audit_bounded_{fighter}_ground_throw_dispatch_runtime',
                              f'audit_bounded_{fighter}_cross_added_ground_throw_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
