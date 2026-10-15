"""Physical close-range escape only; preserve the earned route before stage five."""
import verify_native_source_sync as sync

sync.verify()
base = sync.ROOT/'audit_current_sonya_mirror_stance_guard_preparation'
out = sync.ROOT/'audit_current_sonya_mirror_throw_escape_preparation'
assert not out.exists()
source = (base/'campaign.lua').read_text()
start = source.index('   if leg_tactic and other.roster==18 then\n')
end = source.index('   elseif leg_tactic and other.roster==0 then', start)
branch = source[start:end]
needle = "    elseif frame<mg_guard or (not safe and gap<125) then\n"
assert branch.count(needle) == 1
branch = branch.replace(needle,
    "    elseif ready and gap<65 then\n"
    "     press(forward=='Right' and 'Left' or 'Right');press('Up')\n"
    "     log('MIRROR_THROW_ESCAPE',string.format('stage=%d gap=%d human_action=%d cpu_action=%d',stage,gap,human.action,other.action))\n" + needle)
source = source[:start]+branch+source[end:]
source = source.replace('frame>=30000','frame>=24000').replace('maximum_fields=30000','maximum_fields=24000')
out.mkdir()
lua = out/'campaign.lua'
lua.write_text(source)
runner = (base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner = runner.replace('audit_current_sonya_mirror_stance_guard_runtime','audit_current_sonya_mirror_throw_escape_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared: physical mirror throw escape, 24000 fields, 90sec/320MiB/10MiB, no media')
