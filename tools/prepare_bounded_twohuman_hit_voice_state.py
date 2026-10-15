"""Observe saved ownership/channel positions around the real human hit."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_crouched_early_punch_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_hit_voice_state_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+r'''
local hit_saved,hit_channels={},{}
local function bind_hit_voice()
 for name,index in pairs(manager.machine.devices[':'].items)do
  for _,field in ipairs({'actor','main','health','id','mode'})do
   if name:match('/m_mk2ks_battle_'..field..'$')then assert(not hit_saved[field]);hit_saved[field]=emu.item(index)end
  end
 end
 for _,field in ipairs({'actor','main','health','id','mode'})do assert(hit_saved[field])end
 for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items)do
  local n,field=name:match('^(%x+)/chan%.(.+)$')
  if n then n=tonumber(n,16);if n>=10 and n<=13 then hit_channels[n]=hit_channels[n]or{};hit_channels[n][field]=emu.item(index)end end
 end
 for n=10,13 do for _,field in ipairs({'source_len','pos','paused','loop'})do assert(hit_channels[n][field])end end
end
local function hit_voice_observe(phase)
 if not command or frame-command>160 then return end
 for n=0,1 do
  log('VOICE_OWNER',string.format('seconds=%.12f phase=%s slot=%d actor=%08X main=%08X health=%d id=%d mode=%d',emu.time(),phase,n+1,hit_saved.actor:read(n),hit_saved.main:read(n),hit_saved.health:read(n),hit_saved.id:read(n),hit_saved.mode:read(n)))
 end
 for n=10,13 do
  local c=hit_channels[n]
  log('VOICE_CHANNEL',string.format('seconds=%.12f phase=%s channel=%d length=%d pos=%.8f paused=%d loop=%d',emu.time(),phase,n,c.source_len:read(0),string.unpack('<d',c.pos:read_block(0,8)),c.paused:read(0),c.loop:read(0)))
 end
end
emu.register_frame(function()if frame==1 then bind_hit_voice()end;hit_voice_observe('frame')end)
emu.register_sound_update(function()hit_voice_observe('sound')end)
emu.register_stop(function()assert(hit_saved.actor and hit_channels[10]);log('VOICE_STOP','raw_media=none')end)
'''
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_crouched_early_punch_runtime':'audit_bounded_twohuman_hit_voice_state_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
