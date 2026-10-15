"""Scalar native arena6 transition diagnosis, unchanged controller inputs."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_stock_pit_direct_rematch_preparation'
out=sync.ROOT/'audit_current_stock_pit_transition_trace_preparation'
assert not out.exists()
source=(base/'sonya_p1_kitana.lua').read_text()
source+=r'''
local transition_key=nil
emu.register_frame_done(function()
 if frame>=19500 then log('TRANSITION_BOUND','maximum_fields=19500 completed_scene=false');manager.machine:exit();return end
 local arena=p:read_u16(0x01061ac0)
 if arena~=6 then return end
 local mode=p:read_u16(0x010601d0)
 local own,other=sample(side),sample(3-side)
 local key=string.format('%d:%d:%d:%d:%d',mode,p:read_u16(0x01061b00),p:read_u16(slots[1].state),p:read_u16(slots[2].state),pending and 1 or 0)
 if key~=transition_key or frame%120==0 then
  transition_key=key
  log('TRANSITION_SCALAR',string.format('mode=%d arena=%d finish=%d states=%d,%d pending=%d kos=%d window=%d valid=%d,%d health=%d,%d ids=%d,%d owners=%08X,%08X actors=%08X,%08X',mode,arena,p:read_u16(0x01061b00),p:read_u16(slots[1].state),p:read_u16(slots[2].state),pending and 1 or 0,kos,window or -1,own and 1 or 0,other and 1 or 0,own and own.hp or -1,other and other.hp or -1,own and own.id or -1,other and other.id or -1,own and own.owner or 0,other and other.owner or 0,own and own.actor or 0,other and other.actor or 0))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'sonya_p1_kitana.ps1').read_text().replace(base.name+'/sonya_p1_kitana.lua',out.name+'/stage.lua').replace(sync.sha(base/'sonya_p1_kitana.lua'),sync.sha(lua)).replace('audit_current_stock_pit_direct_rematch_sonya_p1_kitana_runtime','audit_current_stock_pit_transition_trace_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared19500field scalartransition only,no media,90sec/320MiB')
