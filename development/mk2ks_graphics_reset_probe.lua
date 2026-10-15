-- Same physical secret/return/attract policy, with bounded passive decoder
-- provenance. No guest, CPU, health, RNG, graphics or sound-state writes.
dofile('mk2ks_natural_smoke_route.lua')
local machine=manager.machine
local cpu=machine.devices[':maincpu'].state
local p=machine.devices[':maincpu'].spaces.program
local taps,ring,last={}, {}, {}
local captured=false
local last_lookup,last_header
local observing=false
local function readable(a)
 return a>=0 and a<=0x003ffe00 or a>=0x01000000 and a<=0x013ffe00 or
        a>=0x02000000 and a<=0x07fffe00 or a>=0xff800000 and a<=0xfffffe00
end
local function words(a)
 if not readable(a)then return 'unreadable' end
 local out={}
 for i=0,15 do out[#out+1]=string.format('%04X',p:read_u16(a+i*16))end
 return table.concat(out)
end
local function snapshot(tag,at,data,mask)
 observing=true
 local out={string.format('MK2_GRAPHICS_%s frame=%d seconds=%.12f writes=0 assistance=none at=%08X pc=%08X mode=%d arena=%d data=%08X mask=%08X',
  tag,rawget(_G,'MK2_SECRET_FRAME')or 0,emu.time(),at,cpu.PC.value,p:read_u16(0x010601d0),p:read_u16(0x01061ac0),data or 0,mask or 0)}
 for _,bank in ipairs({'A','B'})do
  for n=0,14 do local name=bank..n;out[#out+1]=string.format('%s=%08X',name,cpu[name].value)end
 end
 out[#out+1]=string.format('SP=%08X stack=%s A8words=%s A1words=%s B3words=%s',
  cpu.SP.value,words(cpu.SP.value),words(cpu.A8.value),words(cpu.A1.value),words(cpu.B3.value))
 local result=table.concat(out,' ')
 observing=false
 return result
end
local table_base=0xff800000+0xf4900*8
taps[#taps+1]=p:install_read_tap(table_base,table_base+54*32-1,'last native slideshow lookup',function(at,data,mask)
 if observing then return end
 if cpu.PC.value==0xff8447e0 and (at-table_base)%32==0 then
  last_lookup=snapshot('PICTURE_LOOKUP',at,data,mask)
 end
end)
taps[#taps+1]=p:install_read_tap(0xff903640,0xff90364f,'last native picture decoder header',function(at)
 if observing then return end
 if at==0xff903640 then last_header=snapshot('PICTURE_HEADER',at)end
end)
-- One record per decoder entry per video field, twelve most recent records
-- only. A malformed row loop cannot produce an unbounded instruction trace.
for _,entry in ipairs({0xff903280,0xff9037d0,0xff904ee0})do
 taps[#taps+1]=p:install_read_tap(entry,entry+15,'bounded graphics-copy ancestry',function(at)
  if observing then return end
  local f=rawget(_G,'MK2_SECRET_FRAME')or 0
  if at~=entry or last[entry]==f then return end
  last[entry]=f
  ring[#ring+1]=snapshot('ANCESTRY',at)
  if #ring>12 then table.remove(ring,1)end
 end)
end
taps[#taps+1]=p:install_write_tap(0x01d81060,0x01d8107f,'first native copy watchdog pointer provenance',function(at,data,mask)
 if observing then return end
 if captured or cpu.PC.value~=0xff904f80 then return end
 captured=true
 if last_lookup then print(last_lookup)end
 if last_header then print(last_header)end
 for _,row in ipairs(ring)do print(row)end
 print(snapshot('WATCHDOG',at,data,mask))
 local raw,w,h=machine.screens[':screen']:pixels()
 assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_HPHASE_RGB frame=%d move=ball side=%s attempt=1 stage=graphics_watchdog.png width=%d height=%d bytes=%d hex=%s',
  rawget(_G,'MK2_SECRET_FRAME')or 0,os.getenv('MK2KS_STAGE_SIDE'),w,h,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end)
emu.register_stop(function()for _,tap in ipairs(taps)do tap:remove()end end)
