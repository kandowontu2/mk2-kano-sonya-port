"""Use physically verified D/F/LP choke sequence against real campaign CPU3."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_close_upper_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_choke_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("    local forward=human.x<other.x and 'Right' or 'Left'",source.index("elseif fighter=='kano' and side==2 and other.roster==3 then"))
end=source.index('   elseif (leg_tactic',start)
branch="""    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not sc_last or frame-sc_last~=1 then sc_choke=nil;sc_retry=-1000 end
    sc_last=frame
    local ready=height<=8 and human.flags&0x1c==0 and
     (human.action==0 or human.action==771 or human.action==772)
    local safe=other.flags&0x1c==0 and other.floor-other.y<=8
    if sc_choke and frame-sc_choke<12 then
     local age=frame-sc_choke
     if age<3 then press('Down')end
     if age>=5 and age<8 then press(sc_direction)end
     if age>=6 and age<9 then press('Low Punch')end
    elseif ready and safe and gap<64 and frame-sc_retry>=64 then
     sc_choke=frame;sc_retry=frame;sc_direction=forward;press('Down')
    elseif ready and safe and gap>=64 then press(forward)
    elseif height<=8 and (human.action==770 or human.action==769 or human.action==1792 or human.action==1793) then
     -- Release crouch/guard physically so fresh command can follow.
    elseif ready then press('Down');press('Block')end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_close_upper_runtime','audit_current_kano_p2_scorpion_choke_runtime')
(out/'run.ps1').write_text(runner)
print('Physical close D/F/LP choke;32000fields/90sec/320MiB/10MiB/no media')
