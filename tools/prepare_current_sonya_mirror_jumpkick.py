"""New physical mirror spacing tactic; retain all prior earned campaign inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_kunglao_guard_preparation'
out=sync.ROOT/'audit_current_sonya_mirror_jumpkick_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
first=source.index('   if leg_tactic and other.roster==18 then\n')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
branch=r'''   if leg_tactic and other.roster==18 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local back=human.x<other.x and 'Left' or 'Right'
    local height=human.floor-human.y
    if not mj_last or frame-mj_last~=1 then mj_jump=-1000 end
    mj_last=frame
    if height>8 then
     if gap<130 and height>20 and frame%6<3 then press('High Kick')end
    elseif human.flags&0x1c~=0 then
     press('Down');press('Block')
    elseif frame-mj_jump<4 then
     press('Up');if gap>90 then press(forward)end
    elseif frame-mj_jump>=32 then
     mj_jump=frame;press('Up');if gap>90 then press(forward)end
     log('MIRROR_JUMPKICK_ATTEMPT',string.format('stage=%d gap=%d human_action=%d cpu_action=%d',stage,gap,human.action,other.action))
    else
     press('Block');if gap<60 then press(back)end
    end
'''
source='local mj_last,mj_jump=nil,-1000\n'+source[:first]+branch+source[last:]
source=source.replace('frame>=18000','frame>=21000').replace('maximum_fields=18000','maximum_fields=21000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_kunglao_guard_runtime','audit_current_sonya_mirror_jumpkick_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared21000field physical jumpkick mirror test,no media,90sec/320MiB')
