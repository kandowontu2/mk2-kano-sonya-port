"""Physical knife recovery escape, CPU5-only, no combat/AI state writes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_mileena_early_airkick_preparation'
out=sync.ROOT/'audit_current_kano_p2_mileena_knife_escape_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
start=source.index("   if fighter=='kano' and side==2 and other.roster==5 then")
end=source.index("   elseif fighter=='kano' and side==2 and (other.roster==18",start)
branch=source[start:end]
policy=branch.index("    local forward=human.x<other.x and 'Right' or 'Left'")
branch=branch[:policy]+"""    local back=human.x<other.x and 'Left' or 'Right'
    local height=human.floor-human.y
    if not mj_last or frame-mj_last~=1 then mj_start=nil;mj_jump=-1000 end
    mj_last=frame
    if mj_start and frame-mj_start<64 then
     local age=frame-mj_start
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(mj_back)end
     if age>=8 and age<12 then press('High Punch')end
     if age>=15 and age<24 then press('Down');press('Block')end
     if age>=24 and age<28 then press('Up');press(mj_back)end
     if age>=28 then
      press(mj_back)
      if height>8 and gap<120 and frame%6<3 then press('High Kick')end
     end
    elseif height>8 then
     if gap<120 and frame%6<3 then press('High Kick')end
    elseif gap<80 then
     mj_start=nil
     if frame-mj_jump>=40 then mj_jump=frame end
     if frame-mj_jump<4 then press('Up');press(back)end
    else
     mj_start=frame;mj_back=back
     log('MILEENA_KNIFE_ESCAPE_PLAN',string.format('gap=%d action=%d flags=%04X health=%d,%d',gap,human.action,human.flags,human.hp,other.hp))
    end
"""
source=source[:start]+branch+source[end:]
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_mileena_early_airkick_runtime','audit_current_kano_p2_mileena_knife_escape_runtime')
(out/'run.ps1').write_text(runner)
print('CPU5-only physical knife+recovery backjump;native command/air observers;90sec/320MiB/10MiB/no media')
