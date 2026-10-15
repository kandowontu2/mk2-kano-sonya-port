"""True-ID native pain voice routes/packets; no renderer or audio recorder."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify();old=root/'audit_bounded_settled_uppercut_recovery_preparation'
    original=(old/'prepared_observer.lua').read_text()
    marker='local actual_dma={}';assert original.count(marker)==1
    lua=original.split(marker,1)[0]
    marker='local contact_health_taps={}';assert original.count(marker)==1
    lua+=original[original.index(marker):]
    lua+=r'''
local pain_taps={}
for _,entry in ipairs({{0xffa122d0,'male'},{0xffa123b0,'female'}})do
 local address,route=entry[1],entry[2]
 pain_taps[#pain_taps+1]=p:install_read_tap(address,address+15,'actual true-ID native pain branch',function(at,data,mask)
  if not ready or at~=address or regs.PC.value~=address+16 then return end
  local a,b=sample(1),sample(2)
  log('PAIN_BRANCH',string.format('route=%s entry=%08X pc=%08X a2=%08X a8=%08X a10=%08X a13=%08X actor1=%08X main1=%08X id1=%d hp1=%d actor2=%08X main2=%08X id2=%d hp2=%d',
   route,address,regs.PC.value,regs.A2.value,regs.A8.value,regs.A10.value,regs.A13.value,a.actor,a.main,a.id,a.hp,b.actor,b.main,b.id,b.hp))
 end)
end
pain_taps[#pain_taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual native pain-window sound packets',function(at,data,mask)
 if not ready or at~=0x01d01030 then return end
 log('PAIN_SOUND',string.format('data=%04X mask=%04X pc=%08X a0=%08X a2=%08X a8=%08X a10=%08X a13=%08X',
  data&65535,mask,regs.PC.value,regs.A0.value,regs.A2.value,regs.A8.value,regs.A10.value,regs.A13.value))
end)
local pain_channels={}
local function bind_pain_channels()
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local channel,field=name:match('^(%x+)/chan%.(.+)$')
  if channel then
   channel=tonumber(channel,16)
   if channel>=10 and channel<=13 then pain_channels[channel]=pain_channels[channel]or{};pain_channels[channel][field]=emu.item(index)end
  end
 end
 for channel=10,13 do for _,field in ipairs({'source_len','pos','loop','paused'})do assert(pain_channels[channel][field])end end
end
emu.register_frame(function()if frame==1 then bind_pain_channels()end end)
emu.register_frame_done(function()
 if not ready or frame<1408 or frame>1480 or frame%2~=0 then return end
 for channel=10,13 do
  local c=pain_channels[channel];local pos=string.unpack('<d',c.pos:read_block(0,8))
  log('PAIN_CHANNEL',string.format('channel=%d length=%d pos=%.8f loop=%d paused=%d',channel,c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
 end
end)
emu.register_stop(function()assert(#pain_taps==3 and pain_channels[13])end)
'''
    for banned in (':write_', ':snapshot(', ':pixels(', 'snapshot_pixels', 'read_block(0,512'):
        assert banned not in lua,banned
    out=root/'audit_bounded_native_pain_voice_preparation';out.mkdir(exist_ok=False)
    target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_settled_uppercut_recovery_runtime',f'audit_bounded_{fighter}_native_pain_voice_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target),rawMedia='none')))

if __name__=='__main__':main()
