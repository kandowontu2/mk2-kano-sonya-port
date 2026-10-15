"""Native sound packets/voice branches during an actually earned finisher."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local finisher_audio_taps={}
for _,entry in ipairs({{0xffa122d0,'male'},{0xffa123b0,'female'}})do
 local address,route=entry[1],entry[2]
 finisher_audio_taps[#finisher_audio_taps+1]=p:install_read_tap(address,address+15,'earned finisher voice branch',function(at)
  if not action_start or at~=address or cpu.PC.value~=address+16 then return end
  local victim=sample(side)
  print(string.format('MK2_FINISHER_AUDIO_BRANCH frame=%d age=%d route=%s pc=%08X a2=%08X a8=%08X a13=%08X victim_actor=%08X victim_main=%08X victim_id=%d hp=%d writes=0 assistance=none',frame,frame-action_start,route,cpu.PC.value,cpu.A2.value,cpu.A8.value,cpu.A13.value,victim.actor,victim.main,victim.id,victim.hp))
 end)
end
finisher_audio_taps[#finisher_audio_taps+1]=p:install_write_tap(0x01d01030,0x01d0103f,'earned finisher actual sound packets',function(at,data,mask)
 if not action_start or at~=0x01d01030 then return end
 print(string.format('MK2_FINISHER_AUDIO_PACKET frame=%d age=%d data=%04X mask=%04X pc=%08X a0=%08X a8=%08X a13=%08X writes=0 assistance=none',frame,frame-action_start,data&65535,mask,cpu.PC.value,cpu.A0.value,cpu.A8.value,cpu.A13.value))
end)
emu.register_stop(function()assert(#finisher_audio_taps==3)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_finisher_preparation'
    out=sync.ROOT/'audit_bounded_stock_head_audio_route_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_finisher_runtime',
                              f'audit_bounded_{fighter}_stock_head_audio_route_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
