"""Retire diagnostic-only boss instruction taps; preserve actual physical inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_liukang_short_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p1_boss_light_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index('    if not boss_action_taps[human.main] then')
end=source.index("    local forward=human.x<other.x and'Right'or'Left'",start)
diagnostic=source[start:end]
assert 'boss_action_taps.native_handlers' in diagnostic and "log('BOSS_ACTION'" in diagnostic and "log('BOSS_HANDLER'" in diagnostic
assert all(token not in diagnostic for token in ['press(', 'boss_last_jump=', 'boss_walk_counter=', 'projectile_start='])
source=source[:start]+"    -- Diagnostic-only instruction/action taps retired; native state unmodified.\n"+source[end:]
old="    log('BOSS_FIELD',string.format("
assert source.count(old)==1
source=source.replace(old,"    if frame%120==0 then log('BOSS_FIELD',string.format(")
old='p:read_u32(human.actor+0x60),p:read_u32(other.actor+0x60),human.hp,other.hp))\n'
assert source.count(old)==1
source=source.replace(old,old.rstrip('\n')+' end\n')
assert source.count('maximum_fields=120000')==1
source=source.replace('frame>=120000','frame>=140000').replace('maximum_fields=120000','maximum_fields=140000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_liukang_short_leg_runtime','audit_current_sonya_p1_boss_light_runtime')
(out/'run.ps1').write_text(runner)
print('Samephysicalcontroller; diagnostic-only boss taps retired/BOSS_FIELD120;140000ceiling/180sec/320MiB/10MiB/no media')
