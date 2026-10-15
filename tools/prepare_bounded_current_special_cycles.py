"""Original physical two-cycle controller; remove raw guest/GFX/RGB sinks."""
import json
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_current_special_cycles_preparation';assert not out.exists();out.mkdir()
original=sync.ROOT/'mk2ks_special_repeat_v5099.lua'
lua=original.read_text()
start=lua.index(' if frame==1 then\n');end=lua.index(' if ready then\n',start)
lua=lua[:start]+" if frame==1 then phase_log('NO_RAW_DUMPS','bounded_scalar_only=true')end\n"+lua[end:]
start=lua.index(' local raw,width,height=screen:pixels();');end=lua.index(" phase_log('SNAP'",start)
lua=lua[:start]+" phase_snaps=phase_snaps+1\n"+lua[end:]
assert 'hex=' not in lua and 'read_range' not in lua and ':snapshot(' not in lua
target=out/'cycles.lua';target.write_text(lua)
old=sync.ROOT/'audit_bounded_jump_presented_points_preparation'
for move in ('knife','ball','blade','choke','ring','square','bicycle','leg'):
    fighter='kano' if move in ('knife','ball','blade','choke') else 'sonya'
    for side in (1,2):
        runner=(old/f'run_{fighter}.ps1').read_text()
        runner=runner.replace(old.name+'/prepared_observer.lua',out.name+'/cycles.lua').replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        prior='knife' if fighter=='kano' else 'ring'
        runner=runner.replace(f"$env:MK2KS_HUMAN_SPECIAL_MOVE='{prior}'",f"$env:MK2KS_HUMAN_SPECIAL_MOVE='{move}'")
        runner=runner.replace("$env:MK2KS_HUMAN_SPECIAL_SIDE='1'",f"$env:MK2KS_HUMAN_SPECIAL_SIDE='{side}'")
        runner=runner.replace(f'audit_bounded_{fighter}_jump_presented_points_runtime',f'audit_bounded_current_special_cycles_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,originalPhysicalControllerSHA256=sync.sha(original),observerSHA256=sync.sha(target),rawMedia=False,fullGoalComplete=False)))
