"""Four explicitly bounded first-cycle screenshots per cross-grab case."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
runners=sync.ROOT/'audit_bounded_current_cross_grabs_preparation'
out=sync.ROOT/'audit_bounded_cross_grab_visuals_preparation';assert not out.exists();out.mkdir()
lua=(old/'cycles.lua').read_text()
marker=" phase_log('SNAP','stage='..marks[frame])"
assert lua.count(marker)==1
lua=lua.replace('local phase_snaps=0','local phase_snaps=0\nlocal visual_snaps=0',1)
lua=lua.replace(marker,""" if attempt==1 and ({entry=true,phase_24=true,phase_64=true,special_recovered=true})[marks[frame]]then
  visual_snaps=visual_snaps+1;assert(visual_snaps<=4,'Four-shot bound')
  screen:snapshot('grab_'..marks[frame]..'.png')
  phase_log('VISUAL_SAVED','stage='..marks[frame]..' count='..visual_snaps)
 end
"""+marker)
target=out/'visuals.lua';target.write_text(lua)
for move in ('choke','leg'):
    runner=(runners/f'run_{move}_p1.ps1').read_text()
    runner=runner.replace(old.name+'/cycles.lua',out.name+'/visuals.lua').replace(sync.sha(old/'cycles.lua'),sync.sha(target))
    runner=runner.replace(f'audit_bounded_current_cross_grab_{move}_p1_runtime',f'audit_bounded_cross_grab_visual_{move}_p1_runtime')
    runner=runner.replace("rawMedia='none'","rawMedia='bounded_four_png'")
    (out/f'run_{move}.ps1').write_text(runner)
