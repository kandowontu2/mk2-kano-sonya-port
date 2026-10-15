"""Physical ring/guard trial against native CPU0 projectile exposure."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_contact_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_grounded_ring_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2 or other.roster==0) then"
assert source.count(marker)==1
branch="""   elseif fighter=='sonya' and side==2 and other.roster==0 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local backward=human.x<other.x and 'Left' or 'Right'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local ready=height<=8 and human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793 or human.action==3)
    local safe=other.flags&0x1c==0 and cpu_height<=8 and (other.action==0 or other.action==771 or other.action==772 or other.action==770)
    if not kr_last or frame-kr_last~=1 then kr_start=nil;kr_guard=-1000;kr_retry=-1000 end
    kr_last=frame
    if other.action==1540 then kr_guard=frame+50 end
    if kr_start and frame-kr_start<52 then
     local age=frame-kr_start
     if age<3 then press('Down')end
     if age>=5 and age<8 then press(kr_forward)end
     if age>=6 and age<9 then press('Low Punch')end
     if age>=12 then press('Down');press('Block')end
    elseif ready and gap<130 then kr_start=nil;press(backward)
    elseif frame<kr_guard or other.flags&0x10~=0 then kr_start=nil;press('Down');press('Block')
    elseif ready and safe and gap>=130 and gap<=350 and frame-kr_retry>=52 then
     kr_start=frame;kr_retry=frame;kr_forward=forward;press('Down')
     log('KUNGLAO_RING_PLAN',string.format('gap=%d health=%d,%d',gap,human.hp,other.hp))
    elseif ready and safe and gap>350 then kr_start=nil;press(forward)
    else kr_start=nil;press('Down');press('Block')end
"""
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_contact_trace_runtime','audit_current_sonya_p2_kunglao_grounded_ring_runtime')
(out/'run.ps1').write_text(runner)
print('CPU0-only grounded physical ring+observed1540 guard delay;60k/90sec/320MiB/10MiB/no media')
