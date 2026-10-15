"""Read six dedicated sample channels across earned action and rejoin."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_friendly_rejoin_both_selectors_preparation'
out=sync.ROOT/'audit_bounded_friendship_channel_retirement_preparation'
assert not out.exists()
out.mkdir()
base=old/'friendship.lua'
source=base.read_text()+'''
local observed_channels={}
emu.register_frame(function()
 if frame==1 then
  for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
   local channel,field=name:match('^(%x+)/chan%.(.+)$')
   if channel then
    channel=tonumber(channel,16)
    if channel>=4 and channel<=9 then
     observed_channels[channel]=observed_channels[channel]or{}
     observed_channels[channel][field]=emu.item(index)
    end
   end
  end
  for channel=4,9 do
   local c=assert(observed_channels[channel]);assert(c.source_len and c.pos and c.source_num and c.loop and c.paused)
  end
 end
 if action and frame%8==0 then
  for channel=4,9 do
   local c=observed_channels[channel]
   local pos=string.unpack('<d',c.pos:read_block(0,8))
   log('SAMPLE_CHANNEL',string.format('channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d rejoined=%s',channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0),tostring(rejoin_live~=nil)))
  end
 end
end)
'''
lua=out/'channels.lua'
lua.write_text(source)
assert 'get_samples(' not in source and ':snapshot(' not in source and ':write_' not in source
for fighter in ('kano','sonya'):
    for side in (1,2):
        runner=(old/f'run_friendship_{fighter}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/friendship.lua',out.name+'/channels.lua').replace(sync.sha(base),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_rejoin_both_selectors_friendship_{fighter}_p{side}_runtime',f'audit_bounded_friendship_channel_retirement_{fighter}_p{side}_runtime')
        (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared four bounded channel-state observers; no PCM collection')
