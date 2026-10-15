"""Ordinary crouching low kick, preserving prior executed observers."""
import json
import verify_native_source_sync as sync

def main():
    root = sync.ROOT
    sync.verify()
    old = root/'audit_bounded_native_pain_voice_preparation'
    out = root/'audit_bounded_crouch_kick_pain_preparation'
    assert not out.exists()
    lua = (old/'prepared_observer.lua').read_text()
    needle = "if age>=112 and age<116 then input(2,'High Punch')end"
    assert lua.count(needle) == 1
    lua = lua.replace(needle, "if age>=112 and age<116 then input(2,'Low Kick')end")
    lua = lua.replace('physical_settled_uppercut_recovery', 'physical_crouch_lowkick_reaction')
    assert ':write_' not in lua and 'snapshot_pixels' not in lua
    out.mkdir()
    target = out/'prepared_observer.lua'
    target.write_text(lua)
    for fighter in ('sonya', 'kano'):
        runner = (old/f'run_{fighter}.ps1').read_text()
        runner = runner.replace(old.name, out.name).replace(
            sync.sha(old/'prepared_observer.lua'), sync.sha(target)).replace(
            f'audit_bounded_{fighter}_native_pain_voice_runtime',
            f'audit_bounded_{fighter}_crouch_kick_pain_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True, acceptance=False,
                                                observerSha=sync.sha(target))))

if __name__ == '__main__':
    main()
