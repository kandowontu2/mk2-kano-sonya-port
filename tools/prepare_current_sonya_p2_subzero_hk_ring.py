"""Physical native-ready HK and low-health ring; mirror18 unchanged."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_mirror_guard_preparation'
out=sync.ROOT/'audit_current_sonya_p2_subzero_hk_ring_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker="   elseif (leg_tactic or strategy=='lowkick'or strategy=='throw') and other.roster~=12 and other.roster~=13 then"
assert source.count(marker)==1
branch="""   elseif fighter=='sonya' and side==2 and other.roster==8 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    local ready=height<=8 and human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772)
    local safe=(other.action==0 or other.action==771 or other.action==772 or other.action==770) and other.flags&0x1c==0
    if not sh_last or frame-sh_last~=1 then sh_start=nil;sh_retry=-1000;sr_start=nil end
    sh_last=frame
    if sr_start and frame-sr_start<64 then
     local age=frame-sr_start
     if age>=2 and age<5 then press('Down')end
     if age>=7 and age<10 then press(sr_direction)end
     if age>=8 and age<12 then press('Low Punch')end
     if age>=15 then press('Down');press('Block')end
    elseif other.hp<=33 and ready and safe and cpu_height<=8 then
     sr_start=frame;sr_direction=forward;sh_start=nil
     log('SONYA_SUBZERO_RING_PLAN',string.format('gap=%d health=%d,%d',gap,human.hp,other.hp))
    elseif other.flags&0x10~=0 then sh_start=nil;press('Down');press('Block')
    elseif sh_start and frame-sh_start<32 then
     local age=frame-sh_start
     if age>=2 and age<6 then press('High Kick')end
     if age>=10 and (ready or not safe)then press('Down');press('Block')end
    elseif ready and safe and cpu_height<=8 and gap<105 and frame-sh_retry>=32 then
     sh_start=frame;sh_retry=frame
     log('SONYA_SUBZERO_HK_PLAN',string.format('gap=%d health=%d,%d',gap,human.hp,other.hp))
    elseif ready and safe and cpu_height<=8 and gap>=105 then sh_start=nil;press(forward)
    elseif not ready and safe then sh_start=nil
    else sh_start=nil;press('Down');press('Block')end
"""
source=source.replace(marker,branch+marker)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_p2_mirror_guard_runtime','audit_current_sonya_p2_subzero_hk_ring_runtime')
(out/'run.ps1').write_text(runner)
print('SonyaP2 CPU8-only native-ready HK/low33ring;mirrorunchanged;30k/90sec/320MiB/10MiB/no media')
