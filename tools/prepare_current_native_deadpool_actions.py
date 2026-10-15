"""Same physical command with finite read-only actual action fields."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_deadpool_probe_preparation'
out=sync.ROOT/'audit_current_native_deadpool_actions_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
source+='''
emu.register_frame_done(function()
 if not command or frame-command>200 then return end
 for n=1,2 do
  local row=sample(n)
  if row then
   log('ACID_ACTION_FIELD',string.format('age=%d slot=%d actor=%08X main=%08X owner=%08X id=%d native_action=%d flags=%04X body=%04X x=%d y=%d floor=%d hp=%d mode=%d finish=%d',
    frame-command,n,row.actor,row.main,row.owner,row.id,p:read_u16(row.main+0x1f0),row.flags,p:read_u16(row.actor+0x160),row.x,row.y,p:read_i16(row.main+0x200),row.hp,p:read_u16(0x010601d0),p:read_u16(0x01061b00)))
  end
 end
end)
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_deadpool_probe_kano_p1_runtime','audit_current_native_deadpool_actions_kano_p1_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared201paired scalar action fields; physical failed probe unchanged/no media')
