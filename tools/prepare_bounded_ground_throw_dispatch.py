"""Observe executed native ground-throw victim animation router."""
import json
import verify_native_source_sync as sync

def main():
    root=sync.ROOT;sync.verify()
    old=root/'audit_bounded_added_ground_throw_preparation'
    out=root/'audit_bounded_ground_throw_dispatch_preparation';assert not out.exists()
    lua=(old/'prepared_observer.lua').read_text()+r'''
local throw_dispatch_taps={}
for _,address in ipairs({0xff8b6e30,0xfffe1140,0xff8b6e80})do
 throw_dispatch_taps[#throw_dispatch_taps+1]=p:install_read_tap(address,address+15,'actual native ground throw dispatch',function(at,data,mask)
  if not ready or at~=address or regs.PC.value~=address+16 then return end
  local a,b=sample(1),sample(2)
  log('THROW_DISPATCH',string.format('entry=%08X pc=%08X op=%04X a0=%08X a1=%08X a8=%08X a9=%08X a10=%08X a13=%08X actor1=%08X main1=%08X id1=%d actor2=%08X main2=%08X id2=%d',
   address,regs.PC.value,data&65535,regs.A0.value,regs.A1.value,regs.A8.value,regs.A9.value,regs.A10.value,regs.A13.value,a.actor,a.main,a.id,b.actor,b.main,b.id))
 end)
end
emu.register_stop(function()assert(#throw_dispatch_taps==3)end)
'''
    assert ':write_' not in lua
    out.mkdir();target=out/'prepared_observer.lua';target.write_text(lua)
    for fighter in ('sonya','kano'):
        runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
        runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
        runner=runner.replace(f'audit_bounded_{fighter}_added_ground_throw_runtime',
                              f'audit_bounded_{fighter}_ground_throw_dispatch_runtime')
        (out/f'run_{fighter}.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,acceptance=False,observerSha=sync.sha(target))))

if __name__=='__main__':main()
