"""Read-only native action-store provenance during forty command fields."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_counter_ports_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_counter_action_writes_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+r'''
local action_write_tap=p:install_write_tap(0x01000000,0x010fffff,'actual counter action store',function(at,value,mask)
 if not command or frame-command<0 or frame-command>40 then return end
 local own=sample(3-side)
 if own and at==own.main+0x1f0 then
  log('ACTION_WRITE',string.format('age=%d seconds=%.12f slot=%d main=%08X at=%08X before=%04X value=%04X mask=%04X pc=%08X a8=%08X a13=%08X',frame-command,emu.time(),3-side,own.main,at,own.action,value&65535,mask,regs.PC.value,regs.A8.value,regs.A13.value))
 end
end)
emu.register_stop(function()assert(action_write_tap)end)
'''
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_counter_ports_runtime':'audit_bounded_twohuman_counter_action_writes_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
