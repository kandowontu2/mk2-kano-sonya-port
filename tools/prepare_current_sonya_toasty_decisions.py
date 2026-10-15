"""Same physical policy, new sparse native Toasty/RNG call-chain observer."""
import struct
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_natural_smoke_close_preparation'
out=sync.ROOT/'audit_current_sonya_toasty_decisions_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
source+='''
for _,entry in ipairs({0xff8debf0,0xff8def20,0xff8df070,0xff8df0f0,0xff8df120,0xffa0ba10})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'native Toasty decision chain',function(at)
  if at==entry and p:read_u16(0x01061ac0)==7 then
   local h,v=sample(side),sample(3-side)
   if h and v then log('TOASTY_DECISION',string.format('entry=%08X pc=%08X a0=%08X a1=%08X actor=%08X task=%08X own=%08X victim=%08X ids=%d,%d states=%d,%d',
    entry,cpu.PC.value,cpu.A0.value,cpu.A1.value,cpu.A8.value,cpu.A13.value,h.actor,v.actor,h.id,v.id,h.state,v.state))end
  end
 end)
end
emu.register_frame_done(function()
 if frame~=600 then return end
'''
stock_path=sync.ROOT/'mk2/mk2-maincpu.bin'
stock=stock_path.read_bytes()
for lo,hi in ((0xff8de9f0,0xff8df2b0),(0xff81e740,0xff81e820),(0xff80e980,0xff80ecf0)):
    raw=stock[(lo-0xff800000)//8:(hi-0xff800000)//8]
    words=struct.unpack('<'+'H'*(len(raw)//2),raw)
    source+=' do local at=0x%08x;local words={%s};local mismatches=0\n'%(lo,','.join('0x%04x'%w for w in words))
    source+=''' for i,w in ipairs(words)do if p:read_u16(at+(i-1)*16)~=w then mismatches=mismatches+1 end end
 log('TOASTY_STOCK_CODE',string.format('at=%08X words=%d mismatches=%d',at,#words,mismatches));assert(mismatches==0)
 end
'''
source+='end)\n'
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_natural_smoke_close_runtime','audit_current_sonya_toasty_decisions_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared unchanged physical route; sparse original Toasty/RNG taps;28000fields/90sec/320MiB/no media')
