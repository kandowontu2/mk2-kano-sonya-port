"""Read nine specific VRAM coordinates before each subsequent native DMA."""
import json
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_jump_presented_points_preparation'
out=sync.ROOT/'audit_bounded_shadow_writer_trace_preparation';assert not out.exists();out.mkdir()
lua=(old/'prepared_observer.lua').read_text()
lua+=r'''
local trace_targets={
 kano={[1424]={{244,190},{248,201},{250,202},{250,203}},[1496]={{245,197},{245,198}}},
 sonya={[1424]={{246,185}},[1432]={{248,201},{245,202}}}
}
local trace_fighter=os.getenv('MK2KS_TEST_FIGHTER')
local writer_trace=p:install_write_tap(0x01a80010,0x01a8001f,'nine passive native VRAM writer traces',function(at,data)
 if at~=0x01a80010 or not trace_targets[trace_fighter]then return end
 local targets=trace_targets[trace_fighter][frame];if not targets then return end
 local function reg(n)return p:read_u16(0x01a80000+n*16)end
 for _,q in ipairs(targets)do
  log('SHADOW_WRITER',string.format('x=%d y=%d before=%d pc=%08X source=%08X command=%04X start_x=%d start_y=%d width=%d height=%d palette=%04X color=%04X',
   q[1],q[2],point_vram:read(q[2]*512+q[1])&0x7fff,regs.PC.value,reg(2)|(reg(3)<<16),data&65535,reg(4)&1023,reg(5)&511,reg(6)&1023,reg(7)&1023,reg(8),reg(9)))
 end
end)
emu.register_stop(function()assert(writer_trace)end)
'''
target=out/'prepared_observer.lua';target.write_text(lua)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}.ps1').read_text().replace(old.name,out.name)
    runner=runner.replace(sync.sha(old/'prepared_observer.lua'),sync.sha(target))
    runner=runner.replace(f'audit_bounded_{fighter}_jump_presented_points_runtime',f'audit_bounded_{fighter}_shadow_writer_trace_runtime')
    (out/f'run_{fighter}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True,passiveTargetCoordinates=9,rawMedia=False,observerSHA256=sync.sha(target))))
