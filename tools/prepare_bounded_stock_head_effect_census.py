"""Scalar census of all native finisher FIFO actors; no artwork dumps."""
import json
import verify_native_source_sync as sync

TAIL=r'''
local effect_fifo=p:install_read_tap(0xff804410,0xff80441f,'bounded all finisher FIFO actors',function(at)
 if not action_start or frame-action_start>174 or at~=0xff804410 or cpu.PC.value~=0xff804420 then return end
 local actor=cpu.A0.value
 if actor<0x01000000 or actor>=0x01100000 then return end
 local first=p:read_u32(0x01060220);local second=p:read_u32(0x01060df0)
 print(string.format('MK2_EFFECT_CENSUS_FIFO frame=%d age=%d actor=%08X physical=%d id=%d pose=%08X source=%08X size=%08X xy=%08X command=%08X writes=0 assistance=none',
 frame,frame-action_start,actor,(actor==first and 1 or actor==second and 2 or 0),p:read_u16(actor+0x1f0),p:read_u32(actor+0x1d0),cpu.A11.value,cpu.A9.value,cpu.A10.value,cpu.A12.value))
end)
emu.register_stop(function()assert(effect_fifo)end)
'''

def main():
    sync.verify();old=sync.ROOT/'audit_bounded_stock_head_finisher_preparation'
    out=sync.ROOT/'audit_bounded_stock_head_effect_census_preparation';assert not out.exists()
    text=(old/'prepared_observer.lua').read_text()+TAIL
    for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('):assert banned not in text
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(text)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_stock_head_finisher_runtime',
                              f'audit_bounded_{fighter}_stock_head_effect_census_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSha256=sync.sha(target),acceptance=False)))

if __name__=='__main__':main()
