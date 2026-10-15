"""Source bytes and actual packed-role/RNG/cue selection, scalar only."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local selector_taps={}
for _,address in ipairs({0xffa12220,0xffa123d0,0xffa12400,0xffa12530})do
 selector_taps[#selector_taps+1]=p:install_read_tap(address,address+15,'actual finisher packed voice selector',function(at)
  if not action_start or at~=address or cpu.PC.value~=address+16 then return end
  local victim=sample(side);if cpu.A8.value~=victim.actor then return end
  print(string.format('MK2_VOICE_SELECTOR_STEP frame=%d age=%d entry=%08X a0=%08X a1=%08X a2=%08X a8=%08X a13=%08X role=%d victim_id=%d writes=0 assistance=none',frame,frame-action_start,address,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A13.value+0x20),victim.id))
  if address==0xffa12530 then
   local cue=cpu.A0.value;assert(cue<254)
   print(string.format('MK2_VOICE_SELECTOR_CUE frame=%d cue=%02X header=%04X packet=%04X writes=0 assistance=none',frame,cue,p:read_u16(0xffa0ef20+cue*32),p:read_u16(0xffa0ef20+cue*32+16)))
  end
 end)
end
emu.register_frame(function()
 if frame~=1 then return end
 local bytes={};for address=0xffa122d0,0xffa12430-8,8 do bytes[#bytes+1]=string.format('%02X',p:read_u8(address))end
 print('MK2_VOICE_SELECTOR_SOURCE first=FFA122D0 end_pc=FFA12430 hex='..table.concat(bytes)..' writes=0 assistance=none')
end)
emu.register_stop(function()assert(#selector_taps==4)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_p2_stock_head_finisher_preparation'
    out=sync.ROOT/'audit_bounded_p2_voice_selector_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_p2_{fighter}_stock_head_finisher_runtime',f'audit_bounded_p2_{fighter}_voice_selector_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
