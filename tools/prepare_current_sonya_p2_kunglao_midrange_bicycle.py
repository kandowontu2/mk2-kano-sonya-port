"""Physical verified B,B,D+HK command from native grounded midrange."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_kunglao_contact_trace_preparation'
out=sync.ROOT/'audit_current_sonya_p2_kunglao_midrange_bicycle_preparation'
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
    if not kb_last or frame-kb_last~=1 then kb_start=nil;kb_retry=-1000 end
    kb_last=frame
    if kb_start and frame-kb_start<90 then
     local age=frame-kb_start
     if age<3 or (age>=6 and age<9)then press(kb_backward)end
     if age>=12 and age<15 then press('Down')end
     if age>=13 and age<16 then press('High Kick')end
     if age>=20 then press('Down');press('Block')end
    elseif ready and safe and gap>=120 and gap<=260 and frame-kb_retry>=90 then
     kb_start=frame;kb_retry=frame;kb_backward=backward;press(backward)
     log('KUNGLAO_BICYCLE_PLAN',string.format('gap=%d health=%d,%d',gap,human.hp,other.hp))
    elseif ready and safe and gap<120 then kb_start=nil;press(backward)
    elseif ready and safe and gap>260 then kb_start=nil;press(forward)
    else kb_start=nil;press('Down');press('Block')end
"""
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_kunglao_contact_trace_runtime','audit_current_sonya_p2_kunglao_midrange_bicycle_runtime')
(out/'run.ps1').write_text(runner)
print('CPU0-only midrange physical bicycle;60k/90sec/320MiB/10MiB/no media')
