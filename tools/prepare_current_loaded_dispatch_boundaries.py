"""Small input-free initialized-ROM table read; no RAM/media/state dumps."""
import json,struct
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_subzero_contact_trace_preparation'
out=sync.ROOT/'audit_current_loaded_dispatch_boundaries_preparation'
assert not out.exists()
stock=sync.ROOT/'mk2/mk2-maincpu.bin';data=stock.read_bytes()
def rows(at,count):return list(struct.unpack_from('<'+'I'*count,data,(at-0xff800000)//8))
tables={
 'decision':dict(at=0xfffa2000,values=rows(0xff9b1db0,17)+[0xff9b20d0]*2),
 'round':dict(at=0xfffa2800,values=rows(0xff9b2210,17)+[0xff9b91b0]*2),
 'followup':dict(at=0xfffa4000,values=rows(0xff9b76d0,17)+[0xff9b91b0]*7),
 'special':dict(at=0xfffa2400,values=rows(0xff8a5960,22)+[0xfffbc000,0xfffbc200]),
 'reaction':dict(at=0xfffe4800,values=rows(0xff8d2bd0,17)+[0xfffe5000,0xfffe5800])}
operands={0xff9b1d60:0xfffa2000,0xff9b21c0:0xfffa2800,0xff9b7680:0xfffa4000,0xff8a5920:0xfffa2400,0xff835de0:0xfffe4800}
expected=dict(stockSHA256=sync.sha(stock),tables=tables,operands={f'{k:08X}':v for k,v in operands.items()},closeFallback=dict(at=0xfffbc700,words=[0x09c0,7,0xc080,0x9470,0xff9b]))
lines=['local p=manager.machine.devices[":maincpu"].spaces.program','local frame=0','emu.register_frame_done(function()',' frame=frame+1',' if frame~=3 then return end']
for name,t in tables.items():
    lines.append(f" for i=0,{len(t['values'])-1} do print(string.format('MK2_DISPATCH_ROW table={name} index=%d value=%08X writes=0 assistance=none',i,p:read_u32(0x{t['at']:08x}+i*32)))end")
for at in operands:
    lines.append(f" print(string.format('MK2_DISPATCH_OPERAND at={at:08X} value=%08X writes=0 assistance=none',p:read_u32(0x{at:08x})))")
lines.append(" for i=0,4 do print(string.format('MK2_DISPATCH_FALLBACK index=%d value=%04X writes=0 assistance=none',i,p:read_u16(0xfffbc700+i*16)))end")
lines.extend([' manager.machine:exit()','end)'])
lua='\n'.join(lines)+'\n';assert ':write_' not in lua and ':snapshot(' not in lua and ':set_value(' not in lua
out.mkdir();(out/'expected.json').write_text(json.dumps(expected,indent=2)+'\n');path=out/'tables.lua';path.write_text(lua)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/tables.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(path)).replace('audit_current_sonya_p2_subzero_contact_trace_runtime','audit_current_loaded_dispatch_boundaries_runtime').replace("'-str','900'","'-str','2'")
(out/'run.ps1').write_text(runner)
print('105 table rows/5 operands/5 fallback words;3 input-free fields;90sec/320MiB/10MiB/no media')
