"""Release block before physical Up; bounded native flight-action observation."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_air_timing_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_release_jump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source=source.replace('local guard_until=-1000','local guard_until=-1000\nlocal launch_start,launch_last=nil,nil',1)
start=source.index('   elseif leg_tactic and other.roster==8 then\n')
end=source.index("   elseif (leg_tactic or strategy=='lowkick'",start)
branch='''   elseif leg_tactic and other.roster==8 then
    local forward=human.x<other.x and'Right'or'Left'
    local height=human.floor-human.y
    if not launch_last or frame-launch_last~=1 then launch_start=nil end
    launch_last=frame
    if height>8 then
     if frame%6<3 then press('High Kick')end
    elseif launch_start and frame-launch_start<20 then
     local age=frame-launch_start
     -- First8 fields neutral; no Block or Down reapplied during launch.
     if age>=8 and age<16 then press('Up');press(forward)end
    elseif launch_start and frame-launch_start<38 then
     -- Neutral recovery; do not replace a delayed jump with crouch block.
    else
     launch_start=frame
     log('RELEASE_JUMP',string.format('gap=%d action=%d height=%d',gap,human.action,height))
    end
'''
source=source[:start]+branch+source[end:]
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_subzero_air_timing_runtime','audit_current_sonya_p2_subzero_release_jump_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared9000fields neutral8/Up8/native-flightHK; first1000stage fields,no media')
