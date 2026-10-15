"""Observe natural CPU Kano ball cue/owner/channel progression without input changes."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_compact_kano_campaign_preparation'
out=sync.ROOT/'audit_current_cpu_kano_ball_audio_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
assert 'frame>=18000' in source
source=source.replace('frame>=18000','frame>=4000').replace('maximum_fields=18000','maximum_fields=4000')
source+='''
local audio_items,audio_channels,audio_launch,audio_signature={},{},nil,nil
emu.register_frame(function()
 if frame~=1 then return end
 for name,index in pairs(manager.machine.devices[':'].items)do
  for _,field in ipairs({'actor','main','health','id','mode'})do
   if name:match('/m_mk2ks_battle_'..field..'$')then audio_items[field]=emu.item(index)end
  end
 end
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local n,field=name:match('^(%x+)/chan%.(.+)$')
  if n and tonumber(n,16)>=12 and tonumber(n,16)<=13 then
   n=tonumber(n,16);audio_channels[n]=audio_channels[n]or{};audio_channels[n][field]=emu.item(index)
  end
 end
 assert(audio_items.actor and audio_items.main and audio_channels[12])
end)
taps[#taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'natural CPU Kano ball voice',function(at,data,mask)
 if at~=0x01d01030 or mask~=0xffff or data~=0x6b03 then return end
 local actual=sample(2)
 if not actual or actual.id~=17 or actual.roster~=17 or actual.state~=0 or actual.owner~=actual.actor or cpu.A8.value~=actual.actor or cpu.A13.value~=actual.main then return end
 audio_launch=frame;audio_signature=nil
 log('CPU_BALL_CUE',string.format('cue=%04X pc=%08X actor=%08X main=%08X id=%d action=%d health=%d',data,cpu.PC.value,actual.actor,actual.main,actual.id,actual.action,actual.hp))
end)
emu.register_frame_done(function()
 if not audio_launch or frame-audio_launch>120 then return end
 local age=frame-audio_launch
 local c=audio_channels[12]
 local signature=string.format('%08X:%08X:%d:%d:%d',audio_items.actor:read(1),audio_items.main:read(1),c.source_num:read(0),c.source_len:read(0),c.paused:read(0))
 if signature==audio_signature and age>3 and age~=20 and age~=60 and age~=120 then return end
 audio_signature=signature
 local actual=sample(2)
 log('CPU_BALL_OWNER',string.format('launch=%d age=%d actor=%08X main=%08X id=%d stored_health=%d mode=%d guest_actor=%08X guest_main=%08X guest_id=%d guest_hp=%d',audio_launch,age,audio_items.actor:read(1),audio_items.main:read(1),audio_items.id:read(1),audio_items.health:read(1),p:read_u16(0x010601d0),actual and actual.actor or 0,actual and actual.main or 0,actual and actual.id or 0,actual and actual.hp or 0))
 for n=12,13 do
  local channel=audio_channels[n]
  log('CPU_BALL_CHANNEL',string.format('launch=%d age=%d channel=%d sample=%d length=%d pos=%.8f paused=%d loop=%d',audio_launch,age,n,channel.source_num:read(0),channel.source_len:read(0),string.unpack('<d',channel.pos:read_block(0,8)),channel.paused:read(0),channel.loop:read(0)))
 end
end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_bounded_compact_kano_campaign_p1_runtime','audit_current_cpu_kano_ball_audio_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared4000fields; natural CPU Kano cue/owner/passive scalars; no media')
