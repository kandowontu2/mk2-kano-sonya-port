-- Actual native fracture, original parked legs and natural screen transition.
local file=assert(io.open('mk2ks_native_subzero_shatter_probe_v4939.lua','rb'))
local source=file:read('a');file:close()
local function replace(before,after)
 local first,last=source:find(before,1,true)
 assert(first and not source:find(before,last+1,true),'Unique shatter lifecycle anchor')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace('local jump_start,close_start,ground_y,previous_gap,stalled=nil,nil,nil,nil,0',
 'local jump_start,close_start,ground_y,previous_gap,stalled=nil,nil,nil,nil,0\nlocal fracture,wrap,natural=nil,nil,nil')
replace("{0xff8c2e90,'FRACTURE_ENTRY'},{0xff8c3080,'LEGS_LOOKUP'}",[[{0xff8c2e90,'FRACTURE_ENTRY'},{0xff8c3080,'LEGS_LOOKUP'},
 {0xffa12530,'SOUND_CALL'},{0xff9e1290,'ICE_EMITTER'},{0xff80e280,'EFFECT_SPAWN'},
 {0xff841ec0,'NATIVE_PARK'},{0xff8cdc40,'WIN_WRAP'}]])
replace("log(tag,string.format('entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X a0=%08X a1=%08X a9=%08X pose=%08X',",[[
  if tag=='FRACTURE_ENTRY'then fracture=fracture or frame end
  if tag=='WIN_WRAP'and p:read_u16(actor+0x1f0)==8 then wrap=wrap or frame end
  if tag=='SOUND_CALL'and cpu.A0.value~=0xd8 then return end
  if tag=='ICE_EMITTER'and p:read_u16(actor+0x1f0)~=identity then return end
  if tag=='EFFECT_SPAWN'and cpu.A7.value~=0xff9ee3a0 then return end
  if tag=='NATIVE_PARK'and (p:read_u16(actor+0x1f0)~=identity or p:read_u16(main+0x1f0)~=0x0408)then return end
  log(tag,string.format('entry=%08X pc=%08X value=%04X mask=%04X actor=%08X main=%08X owner=%08X id=%d action=%04X a0=%08X a1=%08X a9=%08X pose=%08X',]])
replace('cpu.A0.value,cpu.A1.value,cpu.A9.value,p:read_u32(actor+0x1d0)))',
 'cpu.A0.value,cpu.A1.value,cpu.A9.value,p:read_u32(actor+0x1d0)))\n  log(tag..\'_EXTRA\',string.format(\'a7=%08X a11=%08X palette=%04X mode=%d\',cpu.A7.value,cpu.A11.value,p:read_u16(actor+0x140),p:read_u16(0x010601d0)))')
-- Preserve valid physical observations through the natural post-finisher transition.
replace("log('NATURAL_TRANSITION','id='..tostring(id));manager.machine:exit();return",[[
   log('NATURAL_TRANSITION','id='..tostring(id))
   natural=natural or frame
   if frame-natural==60 then
    local raw,width,height=screen:pixels();assert(width==400 and height==254 and #raw==400*254*4)
    print(string.format('MK2_EARNED_SUBZERO_RGB frame=%d width=%d height=%d bytes=%d hex=%s',frame,width,height,#raw,raw:gsub('.',function(c)return string.format('%02x',c:byte())end)))
    log('LIFECYCLE_END',string.format('fracture=%d wrap=%d natural=%d mode=%d',fracture or-1,wrap or-1,natural,p:read_u16(0x010601d0)))
    manager.machine:exit()
   end
   return]])
replace("replace('frame-deep>=400','frame-deep>=500')",[[
replace('frame-deep>=400','frame-deep>=1200')
replace('if deep and frame-deep==100 then',"if deep and (frame-deep==100 or (fracture and frame-fracture==20)or (wrap and frame-wrap==150))then")
]])
assert(load(source,'@native_shatter_lifecycle_v4943','t',_ENV))()
