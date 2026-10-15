"""Fresh controller-only readiness-triggered backjump trial; preserve prior route."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_native_jumpkick_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_ready_backjump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source='local bj_start,bj_retry,bj_direction,bj_air=nil,-1000,nil,false\n'+source
start=source.index("   elseif fighter=='sonya' and side==2 and other.roster==3 then\n")
end=source.index('   elseif leg_tactic',start)
branch="""   elseif fighter=='sonya' and side==2 and other.roster==3 then
    local height=human.floor-human.y
    local forward=human.x<other.x and 'Right' or 'Left'
    local back=human.x<other.x and 'Left' or 'Right'
    local blocking=human.action==1792 or human.action==1793
    local ready=height==0 and p:read_u32(human.actor+0x60)==0 and human.flags&0x1c==0 and
     (blocking or human.action==0 or human.action==771 or human.action==770 or human.action==772)
    if height>8 and not bj_air then
     log('BARAKA_ACTUAL_AIR',string.format('actor=%08X main=%08X id=%d height=%d action=%d gap=%d',human.actor,human.main,human.id,height,human.action,gap))
    end
    bj_air=height>8
    if bj_start and frame-bj_start<4 then press('Up');press(bj_direction)
    elseif height>8 then
     if gap<190 and frame%6<3 then press('High Kick')end
    elseif ready and gap<190 and frame-bj_retry>=48 then
     bj_start=frame;bj_retry=frame;bj_direction=back
     press('Up');press(back)
    elseif ready and gap>=190 then press(forward)
    else press('Down');press('Block')end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_native_jumpkick_runtime','audit_current_sonya_p2_baraka_ready_backjump_runtime')
(out/'run.ps1').write_text(runner)
print('Ready-ground backjump trial:90sec/320MiB/10MiB/no media, actual-air observations not activation count')
