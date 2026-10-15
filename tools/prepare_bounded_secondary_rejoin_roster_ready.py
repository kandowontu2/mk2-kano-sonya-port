"""Wait for a valid native CSS roster before host route search; no new PNGs."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_rejoin_delayed_preparation'
out=sync.ROOT/'audit_bounded_secondary_rejoin_roster_ready_preparation'
assert not out.exists()
out.mkdir()
source=(old/'rejoin.lua').read_text()
marker="if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and not css[n]then"
assert source.count(marker)==1
source=source.replace(marker,"if mode==4 and frame>700 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].id)<=18 and not css[n]then")
marker=" screen:snapshot('rejoin_'..label..'.png');log('REJOIN_VISUAL','sample='..label..' count='..visual_count)"
assert source.count(marker)==1
source=source.replace(marker," log('REJOIN_MARKER','sample='..label..' count='..visual_count..' media=none')")
lua=out/'rejoin.lua'
lua.write_text(source)
assert ':snapshot(' not in source
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text()
    runner=runner.replace(old.name+'/rejoin.lua',out.name+'/rejoin.lua').replace(sync.sha(old/'rejoin.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_secondary_rejoin_delayed_{fighter}_p1_runtime',f'audit_bounded_secondary_rejoin_roster_ready_{fighter}_p1_runtime')
    runner=runner.replace("rawMedia='bounded_two_png'","rawMedia='none'")
    (out/f'run_{fighter}.ps1').write_text(runner)
