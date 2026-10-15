"""Actual timestamped native writes and ADSP input-latch reads, scalar only."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local split_dcs=assert(manager.machine.devices[':dcs:dcs'])
local split_dcs_read=split_dcs.spaces.data:install_read_tap(0x3400,0x37ff,'actual split ADSP delivery',function(at,value,mask)
 if not action_start then return end
 print(string.format('MK2_SPLIT_DCS_READ frame=%d seconds=%.12f at=%04X word=%04X mask=%04X dsp_pc=%04X writes=0 assistance=none',frame,emu.time(),at,value,mask,split_dcs.state.PC.value))
end)
local split_dcs_write=p:install_write_tap(0x01d01030,0x01d0103f,'timestamp actual split port bytes',function(at,data,mask)
 if not action_start or at~=0x01d01030 then return end
 print(string.format('MK2_SPLIT_DCS_WRITE frame=%d seconds=%.12f word=%04X mask=%04X pc=%08X a8=%08X a13=%08X writes=0 assistance=none',frame,emu.time(),data&65535,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
emu.register_stop(function()assert(split_dcs_read and split_dcs_write)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_kung_lao_split_voice_preparation'
    out=sync.ROOT/'audit_bounded_kung_lao_split_dcs_delivery_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for side in (1,2):
        for fighter in ('sonya','kano'):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text().replace(old.name,out.name)
            runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
            runner=runner.replace('kung_lao_split_voice_runtime','kung_lao_split_dcs_delivery_runtime')
            (out/f'run_{fighter}_p{side}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
