"""Four bounded P1 PNG samples per cross-victim primary/secondary action."""
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_bounded_cross_finisher_visuals_preparation'
assert not out.exists()
out.mkdir()
for kind,base_folder in (('primary','audit_bounded_own_finishers_dispatch_preparation'),('secondary','audit_bounded_secondary_finishers_preparation')):
    base=sync.ROOT/base_folder/'finishers.lua'
    source=base.read_text()+'''
local bounded_visual_count=0
emu.register_frame_done(function()
 if not action_start then return end
 local label=({[30]='early',[100]='active',[180]='late'})[frame-action_start]
 if wrap and frame-wrap==100 then label='completed' end
 if label then
  bounded_visual_count=bounded_visual_count+1;assert(bounded_visual_count<=4)
  screen:snapshot('cross_'..label..'.png')
  log('VISUAL_SAVED','sample='..label..' count='..bounded_visual_count)
 end
end)
'''
    lua=out/(kind+'.lua')
    lua.write_text(source)
    old=sync.ROOT/f'audit_bounded_cross_{kind}_finishers_preparation'
    for fighter in ('kano','sonya'):
        runner=(old/f'run_{fighter}_p1.ps1').read_text()
        runner=runner.replace(base_folder+'/finishers.lua',out.name+'/'+lua.name).replace(sync.sha(base),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_cross_{kind}_finisher_{fighter}_p1_runtime',f'audit_bounded_cross_visual_{kind}_{fighter}_p1_runtime')
        runner=runner.replace("rawMedia='none'","rawMedia='bounded_four_png'")
        (out/f'run_{kind}_{fighter}.ps1').write_text(runner)
print('Prepared four cases, four PNG cap each, sixteen total')
