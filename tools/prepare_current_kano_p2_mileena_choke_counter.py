"""Verified physical D/F/LP command; own readiness only, actual CPU5."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_ready_escape_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_choke_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   if fighter=='kano' and side==2 and other.roster==5 then")
end=source.index("   elseif fighter=='kano' and side==2 and (other.roster==18",start)
branch=source[start:end]
policy=branch.index("    local back=human.x<other.x and 'Left' or 'Right'")
branch=branch[:policy]+"""    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not mc_last or frame-mc_last~=1 then mc_start=nil;mc_retry=-1000 end
    mc_last=frame
    local ready=height<=8 and human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772 or human.action==770 or human.action==1792 or human.action==1793 or human.action==3)
    if mc_start and frame-mc_start<12 then
     local age=frame-mc_start
     if age<3 then press('Down')end
     if age>=5 and age<8 then press(mc_direction)end
     if age>=6 and age<9 then
      press('Low Punch')
      log('MILEENA_CHOKE_LP_INPUT',string.format('age=%d gap=%d action=%d flags=%04X health=%d,%d',age,gap,human.action,human.flags,human.hp,other.hp))
     end
    elseif ready and other.floor-other.y<=8 and gap<100 and frame-mc_retry>=64 then
     mc_start=frame;mc_retry=frame;mc_direction=forward;press('Down')
     log('MILEENA_CHOKE_PLAN',string.format('gap=%d action=%d cpu_action=%d flags=%04X cpu_flags=%04X health=%d,%d',gap,human.action,other.action,human.flags,other.flags,human.hp,other.hp))
    elseif ready and gap>=100 then press(forward)
    end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_ready_escape_runtime','audit_current_kano_p2_mileena_choke_counter_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only ownready D/F/LP/100gap attempt;native entries and actual LP fields;90sec/320MiB/10MiB/no media')
