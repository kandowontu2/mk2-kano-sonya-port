"""Actual forward jump-kick inputs against Scorpion only; passive diagnostics."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_damage_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_jump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw')"
assert source.count(marker)==1
branch="""   elseif fighter=='kano' and side==2 and other.roster==3 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if gap>70 then press(forward)end
    if frame%56<4 then press('Up');press(forward)end
    if height>8 and frame%56>=12 and frame%56<20 then press('High Kick')end
"""
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_damage_runtime','audit_current_kano_p2_scorpion_jump_runtime')
(out/'run.ps1').write_text(runner)
print('Scorpion-only physical forward jump kick;32000fields/90sec/320MiB/10MiB/no media')
