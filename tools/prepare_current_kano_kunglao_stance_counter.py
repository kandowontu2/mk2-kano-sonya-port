"""Transfer finite KungLao guard spacing, own Kano standing-HK inputs only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_standing_counter_long_preparation'
out=sync.ROOT/'audit_current_kano_kunglao_stance_counter_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
marker='   if identity==17 and other.roster==4 then'
assert source.count(marker)==1
branch=r'''   if identity==17 and other.roster==0 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height,cpu_height=human.floor-human.y,other.floor-other.y
    if not kl_last or frame-kl_last~=1 then kl_start=nil;kl_retry=-1000;kl_guard=-1000 end
    kl_last=frame
    local blocking=human.action==1792 or human.action==1793
    local ready=height<=8 and (blocking or human.action==0 or human.action==771 or human.action==770 or human.action==772)
      and human.flags&0x1c==0 and (blocking or human.body&0x0c==0)
    local safe=(other.action==0 or other.action==771 or other.action==770 or other.action==772 or other.action==1792 or other.action==1793)
      and other.flags&0x0c==0
    if other.action==4 or other.action==10 or other.action==16 then kl_guard=frame+40 end
    if kl_start and frame-kl_start<32 then
     local age=frame-kl_start
     if age>=6 and age<10 then press('High Kick')end
     if age>=10 then press('Down');press('Block')end
    elseif height>8 then
     press('Block');if gap<105 and frame%6<3 then press('High Kick')end
    elseif frame<kl_guard or not safe or cpu_height>8 then
     press('Down');press('Block')
    elseif ready and gap<105 and frame-kl_retry>=32 then
     kl_start=frame;kl_retry=frame
     log('KANO_KUNGLAO_COUNTER',string.format('stage=%d gap=%d human_action=%d cpu_action=%d health=%d,%d',stage,gap,human.action,other.action,human.hp,other.hp))
    elseif ready and gap>=105 then
     kl_start=nil;press(forward)
    else
     kl_start=nil;press('Down');press('Block')
    end
'''
source='local kl_last,kl_start,kl_retry,kl_guard=nil,nil,-1000,-1000\n'+source.replace(marker,branch+marker.replace('   if ','   elseif ',1))
source=source.replace('frame>=21000','frame>=24000').replace('maximum_fields=21000','maximum_fields=24000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_standing_counter_long_runtime','audit_current_kano_kunglao_stance_counter_runtime')
assert runner.count("'-str','400'")==1
runner=runner.replace("'-str','400'","'-str','450'")
(out/'run.ps1').write_text(runner)
print('Prepared24000fields,KungLao-only physical guard/HK,90sec/320MiB,no media')
