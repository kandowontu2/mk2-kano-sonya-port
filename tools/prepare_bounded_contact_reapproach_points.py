"""Return through ordinary walking after real punch knockback before counter."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_contact_reaction_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    marker="  if age>=152 and age<156 then input(1,'High Punch')end";assert lua.count(marker)==1
    lua=lua.replace(marker,"  if age>=144 and age<200 and math.abs(a.x-b.x)>45 then input(1,a.x<b.x and 'Right' or 'Left')end\n  if age>=200 and age<204 then input(1,'High Punch')end",1)
    lua=lua.replace('policy=physical_contact_reaction','policy=physical_contact_reapproach',1)
    out=root/'audit_bounded_contact_reapproach_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_contact_reaction_runtime',f'audit_bounded_{fighter}_contact_reapproach_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
