"""Normal vertical/forward jump and landing presentation extension."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_ground_motion_preparation'
    lua=(old/'prepared_observer.lua').read_text()
    oldpolicy="""  if age>=8 and age<24 then input(1,'Right')end
  if age>=32 and age<48 then input(1,'Left')end
  if age>=64 and age<80 then input(1,'Down')end
  if age>=96 and age<100 then input(1,'High Kick')end"""
    assert lua.count(oldpolicy)==1
    lua=lua.replace(oldpolicy,"  if age>=8 and age<12 then input(1,'Up')end\n  if age>=72 and age<76 then input(1,'Up');input(1,'Right')end",1)
    lua=lua.replace('policy=physical_ground_motion','policy=physical_aerial_motion',1)
    out=root/'audit_bounded_aerial_motion_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_ground_motion_points_runtime',f'audit_bounded_{fighter}_aerial_motion_points_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target),maximumReadyFields=180)))

if __name__=='__main__':main()
