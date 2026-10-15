"""Stage6-only physical short leg chord; preserve all earlier controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_baraka_ring_finish20_preparation'
out=sync.ROOT/'audit_current_sonya_p2_baraka_short_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif fighter=='sonya' and side==2 and (other.roster==8 or other.roster==2 or other.roster==0 or other.roster==9 or other.roster==3) then"
assert source.count(marker)==1
branch="""   elseif fighter=='sonya' and side==2 and other.roster==3 and stage==6 then
    if not bl_last or frame-bl_last>1 then bl_pulse=nil end
    bl_last=frame
    local grounded=human.y==human.floor
    local ready=grounded and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)
    local forward=human.x<other.x and'Right'or'Left'
    if bl_pulse and frame-bl_pulse<12 then
     local age=frame-bl_pulse
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif ready and other.floor-other.y<=8 and gap<110 and(not bl_pulse or frame-bl_pulse>=48)then
     bl_pulse=frame;press('Down')
     log('SONYA_BARAKA_SHORT_LEG_PLAN',string.format('stage=%d actor=%08X main=%08X id=18 action=%d gap=%d health=%d,%d',stage,human.actor,human.main,human.action,gap,human.hp,other.hp))
    elseif ready and gap>100 and other.floor-other.y<=8 then
     press(forward)
    else press('Down');press('Block')end
"""
source='local bl_last,bl_pulse=nil,nil\n'+source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_baraka_ring_finish20_runtime','audit_current_sonya_p2_baraka_short_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Stage6 Baraka shortphysicalleg retry48; unchangedearlierroute;180sec/320MiB/10MiB/no media')
