"""Keep cold selection intact; scope physical input release to accepted join."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_joined_controls_preparation'
out=sync.ROOT/'audit_current_native_joined_controls_scoped_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old=" for n=1,2 do for _,field in pairs(joined_buttons[n])do field:clear_value()end end\n if joined_live then"
assert source.count(old)==1
source=source.replace(old," if not join_selection then return end\n for n=1,2 do for _,field in pairs(joined_buttons[n])do field:clear_value()end end\n if joined_live then")
source+='''
emu.register_frame_done(function()
 if joined_live and frame-joined_live>=1599 then
  log('JOINED_CONTROL_WINDOW_END','elapsed_fields=1600 mode='..p:read_u16(0x010601d0))
  manager.machine:exit()
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
for p1,p2 in [(17,18),(18,17)]:
 runner=(base/f'run_{p1}_{p2}.ps1').read_text()
 runner=runner.replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_current_native_joined_controls_{p1}_{p2}_runtime',f'audit_current_native_joined_controls_scoped_{p1}_{p2}_runtime')
 (out/f'run_{p1}_{p2}.ps1').write_text(runner)
print('Prepared scoped joined controls; finite window ends even on native round transition')
