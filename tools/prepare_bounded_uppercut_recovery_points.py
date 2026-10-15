"""Normal stock-human crouch+HP knockdown against the added fighter."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_contact_reaction_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker="  if age>=112 and age<116 then input(2,'High Punch')end\n  if age>=152 and age<156 then input(1,'High Punch')end"
    assert lua.count(marker)==1
    lua=lua.replace(marker,"  if age>=108 and age<116 then input(2,'Down')end\n  if age>=112 and age<116 then input(2,'High Punch')end",1)
    lua=lua.replace('policy=physical_contact_reaction','policy=physical_uppercut_recovery',1)
    out=root/'audit_bounded_uppercut_recovery_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_contact_reaction_runtime',f'audit_bounded_{fighter}_uppercut_recovery_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
