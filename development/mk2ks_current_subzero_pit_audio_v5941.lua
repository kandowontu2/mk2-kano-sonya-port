-- Whole5779 native DAC/ROM/PCM/14 precise channel observer, Pit origin.
-- Added metadata reads both native Main ownership namespaces; no new writes.
local f=assert(io.open('mk2ks_current_tomb_winner_mix_observer_v5779.lua','rb'))
local source=f:read('a');f:close();source=source:gsub('\r\n','\n')
local function replace(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
replace("0xff8bdfe0,0xff8bdfef,'actual native Tomb mirror audio origin'","0xff8bdde0,0xff8bddef,'actual native Pit audio origin'")
replace('at~=0xff8bdfe0','at~=0xff8bdde0')
replace('id=%d owner=%08X return_pc=%08X',
 'id=%d owner=%08X return_pc=%08X owner140=%08X owner290=%08X mode=%d')
replace('valid(m)and p:read_u32(m+0xc0)or 0,p:read_u32(cpu.SP.value)))',
 'valid(m)and p:read_u32(m+0xc0)or 0,p:read_u32(cpu.SP.value),valid(m)and p:read_u32(m+0x140)or 0,valid(m)and p:read_u32(m+0x290)or 0,p:read_u16(0x010601d0)))')
replace('word=%04X mask=%04X pc=%08X a8=%08X a13=%08X',
 'word=%04X mask=%04X pc=%08X a8=%08X a13=%08X owner140=%08X ownerC0=%08X mode=%d')
replace('data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))',
 'data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x140)or 0,valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0xc0)or 0,p:read_u16(0x010601d0)))')
assert(not source:find(':write_',1,true)and not source:find('set_value',1,true))
assert(load(source,'@whole5779_Pit_native_DAC_ROM_PCM_precise_mix_and_both_Main_owners','t',_ENV))()

do
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local frame,origin,cine=0,nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,value)
 print(string.format('MK2_PIT140_%s frame=%d seconds=%.12f writes=0 assistance=none %s',tag,frame,emu.time(),value))
end
local function active()return origin and frame<=origin+1100 end
emu.register_frame(function()frame=frame+1 end)
taps[#taps+1]=p:install_read_tap(0xff8bdde0,0xff8bddef,'actual own current stage action',function(at)
 if at~=0xff8bdde0 or cpu.PC.value~=at+16 then return end
 assert(not origin and p:read_u16(0x01061ac0)==6)
 origin=frame;log('BEGIN',string.format('actor=%08X main=%08X id=%d arena=6',cpu.A8.value,cpu.A13.value,p:read_u16(cpu.A8.value+0x1f0)))
end)
taps[#taps+1]=p:install_read_tap(0xff906ef0,0xff906eff,'original real-stock Pit constructor ancestry',function(at)
 if active()and at==0xff906ef0 and cpu.PC.value==at+16 then
  log('CONSTRUCTOR',string.format('a0=%08X a8=%08X a11=%08X a13=%08X mode=%d',cpu.A0.value,cpu.A8.value,cpu.A11.value,cpu.A13.value,p:read_u16(0x010601d0)))
 end
end)
taps[#taps+1]=p:install_read_tap(0xff180800,0xff180800+19*32-1,'actual extended native Pit movie lookup, original stock row',function(at,data,mask)
 if not active()or(at-0xff180800)%32~=0 or cpu.PC.value~=0xff83b850 or p:read_u16(0x010601d0)~=9 then return end
 local a,m=cpu.A8.value,cpu.A13.value
 log('LOOKUP',string.format('at=%08X low=%04X high=%04X mask=%04X pc=%08X actor=%08X main=%08X owner140=%08X id=%d',
  at,data,p:read_u16(at+16),mask,cpu.PC.value,a,m,valid(m)and p:read_u32(m+0x140)or 0,valid(a)and p:read_u16(a+0x1f0)or -1))
end)
taps[#taps+1]=p:install_read_tap(0xff838790,0xff83879f,'actual original Sub-Zero movie draw groups',function(at)
 if not active()or at~=0xff838790 or cpu.PC.value~=at+16 or p:read_u16(0x010601d0)~=9 then return end
 local a,m=cpu.A8.value,cpu.A13.value
 assert(valid(a)and valid(m)and p:read_u16(a+0x1f0)==8 and p:read_u32(m+0x140)==a)
 cine={actor=a,main=m}
 log('DRAW',string.format('group=%08X actor=%08X main=%08X owner140=%08X id=8 body=%04X bank=%04X pose=%08X cache=%08X x=%d y=%d',
  cpu.A0.value,a,m,p:read_u32(m+0x140),p:read_u16(a+0x160),p:read_u16(a+0x140),p:read_u32(a+0x1d0),p:read_u32(a+0x1a0),p:read_i16(a+0x90),p:read_i16(a+0xb0)))
end)
emu.register_frame_done(function()
 if not active()then return end
 log('FIELD',string.format('age=%d mode=%d arena=%d p1=%08X p2=%08X cine_actor=%08X cine_main=%08X owner140=%08X id=%d body=%04X',
  frame-origin,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),p:read_u32(0x01060220),p:read_u32(0x01060df0),
  cine and cine.actor or 0,cine and cine.main or 0,cine and p:read_u32(cine.main+0x140)or 0,
  cine and p:read_u16(cine.actor+0x1f0)or -1,cine and p:read_u16(cine.actor+0x160)or 0))
end)
emu.register_stop(function()
 log('RESULT','origin='..(origin or -1)..' raw_files=0')
 for _,tap in ipairs(taps)do tap:remove()end
end)
end
