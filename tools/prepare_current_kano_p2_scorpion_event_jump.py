"""Jump-relative physical kick pulses, not global-clock pulses."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_jump_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_event_jump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='kano' and side==2 and other.roster==3 then")
end=source.index("   elseif (leg_tactic",start)
branch="""   elseif fighter=='kano' and side==2 and other.roster==3 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not sc_last or frame-sc_last~=1 then sc_jump=nil;sc_retry=-1000 end
    sc_last=frame
    local ready=height<=8 and human.flags&0x1c==0 and
     (human.action==0 or human.action==771 or human.action==772)
    if ready and (not sc_jump or frame-sc_jump>=40) and frame-sc_retry>=48 then
     sc_jump=frame;sc_retry=frame;sc_direction=forward
    end
    local age=sc_jump and frame-sc_jump or 1000
    if age<4 then press('Up');press(sc_direction)
    elseif height>8 then
     if age<40 then press(sc_direction)end
     if age>=8 and age<42 and age%6<3 then press('High Kick')end
    elseif ready and gap>70 then press(forward)
    else press('Down');press('Block')end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_jump_runtime','audit_current_kano_p2_scorpion_event_jump_runtime')
(out/'run.ps1').write_text(runner)
print('Physical jump-relative Scorpion response;32000fields/90sec/320MiB/10MiB/no media')
