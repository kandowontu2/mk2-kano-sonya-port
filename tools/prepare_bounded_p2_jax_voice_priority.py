"""Scalar true-victim selector and priority taps; no media or guest writes."""
import json
import verify_native_source_sync as sync
from prepare_bounded_p2_voice_selector import TAIL

QUEUE = r'''
local voice_priority_taps={}
for _,address in ipairs({0xffa12a10,0xffa12a80,0xffa12b00})do
 voice_priority_taps[#voice_priority_taps+1]=p:install_read_tap(address,address+15,'native victim voice priority',function(at)
  if not action_start or at~=address or cpu.PC.value~=address+16 then return end
  local victim=sample(side);if cpu.A8.value~=victim.actor then return end
  print(string.format('MK2_VOICE_PRIORITY_QUEUE frame=%d age=%d entry=%08X a1=%08X a3=%08X a4=%08X a8=%08X a13=%08X writes=0 assistance=none',frame,frame-action_start,address,cpu.A1.value,cpu.A3.value,cpu.A4.value,cpu.A8.value,cpu.A13.value))
 end)
end
emu.register_stop(function()assert(#voice_priority_taps==3)end)
'''

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_p2_jax_clap_audio_route_preparation'
    out=sync.ROOT/'audit_bounded_p2_jax_voice_priority_preparation'
    assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL+QUEUE
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('): assert banned not in text
    out.mkdir(); target=out/'prepared_observer.lua'; target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_p2_{fighter}_jax_clap_audio_route_runtime',f'audit_bounded_p2_{fighter}_jax_voice_priority_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
