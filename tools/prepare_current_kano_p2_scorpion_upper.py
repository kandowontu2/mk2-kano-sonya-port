"""Grounded physical crouch uppercut instead of repeated pressured jumps."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_scorpion_release_air_preparation'
out=sync.ROOT/'audit_current_kano_p2_scorpion_upper_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("    local forward=human.x<other.x and 'Right' or 'Left'",source.index("elseif fighter=='kano' and side==2 and other.roster==3 then"))
end=source.index('   elseif (leg_tactic',start)
branch="""    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not sc_last or frame-sc_last~=1 then sc_upper=-1000 end
    sc_last=frame
    local ready=height<=8 and human.flags&0x18==0 and
     (human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1793 or human.action==1792)
    if gap>100 and height<=8 and other.flags&0x10==0 then press(forward)
    else
     press('Down')
     if ready and gap<105 and frame-sc_upper>=24 then
      sc_upper=frame;press('High Punch')
     elseif frame-sc_upper>=4 then press('Block')end
    end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_scorpion_release_air_runtime','audit_current_kano_p2_scorpion_upper_runtime')
(out/'run.ps1').write_text(runner)
print('Physical grounded Scorpion uppercut response;32000fields/90sec/320MiB/10MiB/no media')
