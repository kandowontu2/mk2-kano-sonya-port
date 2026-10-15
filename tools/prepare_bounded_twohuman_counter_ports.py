"""Passive actual port-read provenance around the physical counter command."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_bicycle_uppercut_counter_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_counter_ports_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()+r'''
local counter_port_tap=p:install_read_tap(0x01600000,0x0160000f,'actual native input admission',function(at,value,mask)
 if not command or frame-command<0 or frame-command>40 then return end
 log('PORT_READ',string.format('at=%08X value=%04X mask=%04X pc=%08X age=%d',at,value,mask,regs.PC.value,frame-command))
end)
emu.register_frame_done(function()
 if command and frame-command<=40 then
  log('PHYSICAL_PORT',string.format('age=%d in0=%04X in2=%04X',frame-command,manager.machine.ioport.ports[':IN0']:read(),manager.machine.ioport.ports[':IN2']:read()))
 end
end)
emu.register_stop(function()assert(counter_port_tap)end)
'''
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_bicycle_uppercut_counter_runtime':'audit_bounded_twohuman_counter_ports_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer)}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False)))

if __name__=='__main__':main()
