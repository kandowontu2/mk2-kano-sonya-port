"""A controller-only close-range short leg chord; never writes native state."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p1_subzero_guard_release_leg_preparation'
out=sync.ROOT/'audit_current_sonya_p1_subzero_short_leg_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   elseif fighter=='sonya' and side==1 and other.roster==8 and stage==11 then")
end=source.index("   elseif fighter=='sonya' and side==1 and (other.roster==8",start+1)
branch="""   elseif fighter=='sonya' and side==1 and other.roster==8 and stage==11 then
    if not sl_last or frame-sl_last>1 then sl_pulse=nil end
    sl_last=frame
    local grounded=human.y==human.floor
    local ready=grounded and(human.action==0 or human.action==771 or human.action==770 or human.action==772 or human.action==1792 or human.action==1793)
    local forward=human.x<other.x and'Right'or'Left'
    if sl_pulse and frame-sl_pulse<12 then
     local age=frame-sl_pulse
     if age<7 then press('Down')end
     if age>=3 and age<7 then press('Low Punch');press('Block')end
    elseif ready and other.floor-other.y<=8 and gap<110 and(not sl_pulse or frame-sl_pulse>=48)then
     sl_pulse=frame;press('Down')
     log('SONYA_SETTLED_LEG_PLAN',string.format('actor=%08X main=%08X id=18 action=%d gap=%d loop=-1 health=%d,%d',human.actor,human.main,human.action,gap,human.hp,other.hp))
    elseif ready and gap>100 and other.floor-other.y<=8 then
     press(forward)
    else press('Down');press('Block')end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p1_subzero_guard_release_leg_runtime','audit_current_sonya_p1_subzero_short_leg_runtime')
(out/'run.ps1').write_text(runner)
print('Stage11 physical Down7 LP+Block3..7 retry48; unchanged earlier route; 180sec/320MiB/10MiB/no media')
