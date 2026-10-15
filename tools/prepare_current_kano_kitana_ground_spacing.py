"""Ground retreat and actual-ready native knife inputs, no forced gameplay state."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_current_kano_kitana_ground_spacing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   if (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(marker)==1
branch=r'''   if identity==17 and other.roster==4 then
    local back=human.x<other.x and 'Left' or 'Right'
    local ready=human.floor-human.y<=8 and human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772)
    if not ks_last or frame-ks_last~=1 then ks_start=nil end
    ks_last=frame
    if ks_start and frame-ks_start<12 then
     local age=frame-ks_start
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(ks_direction)end
     if age>=8 and age<12 then press('High Punch')end
    elseif human.floor-human.y>8 then
     if human.action==512 or human.action==779 then press('High Kick')end
    elseif gap<170 or other.action==300 then
     ks_start=nil;press(back)
    elseif ks_start and frame-ks_start<52 then
     if gap<230 then press(back)end
    elseif ready then
     ks_start=frame;ks_direction=back
     log('KANO_KITANA_SPACING_KNIFE',string.format('gap=%d action=%d cpu_action=%d',gap,human.action,other.action))
    else
     -- Release buttons to recover; don't keep Block asserted across startup.
    end
'''
source='local ks_last,ks_start,ks_direction=nil,nil,nil\n'+source.replace(marker,branch+marker.replace('   if ','   elseif ',1))
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_bounded_compact_kano_campaign_p1_runtime','audit_current_kano_kitana_ground_spacing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18000field groundspacing nativeknife physical tactic,no media')
