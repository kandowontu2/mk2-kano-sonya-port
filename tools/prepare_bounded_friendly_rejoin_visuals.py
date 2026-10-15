"""Two transition PNGs per P1 case; unchanged earned/rejoin controller."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_friendly_rejoin_both_selectors_preparation'
out=sync.ROOT/'audit_bounded_friendly_rejoin_visuals_preparation'
assert not out.exists()
out.mkdir()
for kind in ('friendship','babality'):
    original=old/(kind+'.lua')
    source=original.read_text()+'''
local rejoin_visual_count=0
emu.register_frame_done(function()
 local label=nil
 if rejoin_css and frame-rejoin_css==30 then label='selection' end
 if rejoin_live and frame-rejoin_live==30 then label='new_match' end
 if label then
  rejoin_visual_count=rejoin_visual_count+1;assert(rejoin_visual_count<=2)
  screen:snapshot('rejoin_'..label..'.png')
  log('REJOIN_VISUAL_SAVED','sample='..label..' count='..rejoin_visual_count)
 end
end)
'''
    lua=out/original.name
    lua.write_text(source)
    for fighter in ('kano','sonya'):
        runner=(old/f'run_{kind}_{fighter}_p1.ps1').read_text()
        runner=runner.replace(old.name+'/'+original.name,out.name+'/'+lua.name).replace(sync.sha(original),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_rejoin_both_selectors_{kind}_{fighter}_p1_runtime',f'audit_bounded_rejoin_visual_{kind}_{fighter}_p1_runtime')
        runner=runner.replace("rawMedia='none'","rawMedia='bounded_two_png'")
        (out/f'run_{kind}_{fighter}.ps1').write_text(runner)
print('Prepared four cases, two PNGs each, eight total')
