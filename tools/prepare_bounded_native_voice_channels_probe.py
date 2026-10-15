"""Read actual per-channel saved playback state in a bounded target window."""
import prepare_bounded_native_close_counter_probe as old
scope=dict(old.scope)
scope['OUT']=old.old.old.old.old.prior.ROOT/'audit_bounded_native_voice_channels_preparation'
scope['TAIL']+=r'''
local voice_channels={}
local function bind_voice_channels()
    for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items) do
        local channel,field=name:match('^(%x+)/chan%.(.+)$')
        if channel then
            channel=tonumber(channel,16)
            if channel>=10 and channel<=13 then
                voice_channels[channel]=voice_channels[channel] or {}
                assert(not voice_channels[channel][field],'Unique channel field')
                voice_channels[channel][field]=emu.item(index)
            end
        end
    end
    for channel=10,13 do
        local c=assert(voice_channels[channel])
        for _,field in ipairs({'source_num','source_len','pos','loop','paused'}) do
            assert(c[field],'Actual saved channel field '..field)
        end
    end
end
local function observe_voice_channels(phase)
    if selection_frame<2500 or selection_frame>2700 then return end
    for channel=10,13 do
        local c=voice_channels[channel]
        local pos=string.unpack('<d',c.pos:read_block(0,8))
        print(string.format('MK2_BOUNDED_CHANNEL frame=%d seconds=%.12f phase=%s channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
            selection_frame,emu.time(),phase,channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
    end
end
emu.register_frame(function()
    if selection_frame==1 then bind_voice_channels() end
    observe_voice_channels('frame')
end)
emu.register_sound_update(function()observe_voice_channels('sound')end)
emu.register_stop(function()
    assert(voice_channels[10] and voice_channels[13],'Channel observers completed')
    print('MK2_BOUNDED_CHANNEL_TERMINAL channels=4 writes=0 raw_media=none')
end)
'''
exec(compile(old.old.old.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
