"""Release grounded blocks; count a jump only after actual native acceptance."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_mirror_jump_action_trace_preparation'
out=sync.ROOT/'audit_current_mirror_confirmed_jump_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
first=source.index('   if leg_tactic and other.roster==18 then\n')
last=source.index('   elseif leg_tactic and other.roster==0 then',first)
branch=r'''   if leg_tactic and other.roster==18 then
    local forward=human.x<other.x and 'Right' or 'Left'
    local height=human.floor-human.y
    if not cj_last or frame-cj_last~=1 then cj_request=nil;cj_seen=false;cj_accepted=-1000 end
    cj_last=frame
    local jumping=human.action==512 or human.action==779 or human.action==776
    if cj_request and not cj_seen and jumping then
     cj_seen=true;cj_accepted=frame
     log('MIRROR_JUMP_ACCEPTED',string.format('action=%d height=%d gap=%d request=%d',human.action,height,gap,cj_request))
    end
    if height>8 then
     if jumping and height>20 and frame%6<3 then press('High Kick')end
    elseif cj_request and frame-cj_request<6 then
     press('Up');if gap>90 then press(forward)end
    elseif human.flags&0x1c==0 and (human.action==0 or human.action==771 or human.action==772) then
     if frame-cj_accepted>=28 then
      cj_request=frame;cj_seen=false;press('Up');if gap>90 then press(forward)end
      log('MIRROR_CONFIRMED_JUMP_ATTEMPT',string.format('stage=%d gap=%d human_action=%d cpu_action=%d',stage,gap,human.action,other.action))
     end
    else
     -- Neutral release lets native block/crouch recovery settle. Never restart
     -- Down/Block here; rejected jump requests do not start a32field cooldown.
    end
'''
source='local cj_last,cj_request,cj_seen,cj_accepted=nil,nil,false,-1000\n'+source[:first]+branch+source[last:]
source=source.replace('frame>=18500','frame>=21000').replace('maximum_fields=18500','maximum_fields=21000')
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_mirror_jump_action_trace_runtime','audit_current_mirror_confirmed_jump_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared confirmed neutral-jump controller,21000fields,no media,90sec/320MiB')
