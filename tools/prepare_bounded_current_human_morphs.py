"""Original native physical morph/return controller, no snapshot sink."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_current_human_morphs_preparation'
assert not out.exists()
original=sync.ROOT/'mk2ks_human_shang_probe.lua'
source=original.read_text()
before="    for _,s in ipairs(pending) do if s.at==frame then manager.machine.screens[':screen']:snapshot(string.format('human_shang_%s_%s_p%d_%d.png',target,s.kind,side,frame))end end"
assert source.count(before)==1
source=source.replace(before,"    -- Snapshot sink omitted; native physical inputs and reads unchanged.")
assert all(t not in source for t in (':snapshot(',':pixels(','read_range','hex=','dofile('))
out.mkdir()
target=out/'morph.lua'
target.write_text(source)
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
runner=(old/'run_knife_p1.ps1').read_text()
runner=runner.replace(old.name+'/cycles.lua',out.name+'/morph.lua').replace(sync.sha(old/'cycles.lua'),sync.sha(target))
for fighter in ('kano','sonya'):
    for side in (1,2):
        case=runner.replace('audit_bounded_current_special_cycles_knife_p1_runtime',f'audit_bounded_current_human_morph_{fighter}_p{side}_runtime')
        case=case.replace("$env:MK2KS_HUMAN_SPECIAL_MOVE='knife'",f"$env:MK2KS_HUMAN_SHANG_SIDE='{side}'\n$env:MK2KS_HUMAN_SHANG_TARGET='{fighter}'\n$env:MK2KS_HUMAN_SHANG_PROFILE='native'\n$env:MK2KS_HUMAN_SPECIAL_MOVE='knife'")
        (out/f'run_{fighter}_p{side}.ps1').write_text(case)
print('Prepared4 bounded native morph/return runs, no screenshots')
