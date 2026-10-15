"""Passive scalar action changes only; retain existing physical input sequence."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_mirror_jumpkick_preparation'
out=sync.ROOT/'audit_current_mirror_jump_action_trace_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text().replace('frame>=21000','frame>=18500').replace('maximum_fields=21000','maximum_fields=18500')
source+=r'''
local trace_last={}
emu.register_frame_done(function()
 if p:read_u16(0x010601d0)~=2 or p:read_u16(0x01061b30)~=5 then return end
 for slot=1,2 do
  local actor=sample(slot)
  if actor and actor.id==18 and actor.roster==18 and actor.owner==actor.actor then
   local key=string.format('%08X:%08X:%d',actor.actor,actor.main,actor.action)
   if trace_last[slot]~=key then
    trace_last[slot]=key
    local other=sample(3-slot)
    log('MIRROR_ACTION_CHANGE',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d action=%d x=%d y=%d floor=%d height=%d gap=%d health=%d flags=%04X',slot,actor.actor,actor.main,actor.owner,actor.id,actor.roster,actor.action,actor.x,actor.y,actor.floor,actor.floor-actor.y,other and math.abs(actor.x-other.x) or -1,actor.hp,actor.flags))
   end
  end
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_sonya_mirror_jumpkick_runtime','audit_current_mirror_jump_action_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared18500fields action-change trace only,no media,90sec/320MiB')
