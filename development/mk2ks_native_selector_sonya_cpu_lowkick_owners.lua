-- One ordinary physical controller; native CPU decisions/outcomes unchanged.
-- Preserve the executed pressure source and its corrected string boundary.
local f=assert(io.open('mk2ks_native_selector_sonya_cpu_pressure.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(before,after)
 local first,last=source:find(before,1,true);assert(first,before)
 assert(not source:find(before,last+1,true),'Unique actual source boundary')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
once("\n print('MK2_SONYA_OBSERVER_LOAD\n]====])",
     "\n]====]..\" print('MK2_SONYA_OBSERVER_LOAD\")")
once("or approach=='pressure_hp'","or approach=='air_approach'")
once("if approach=='pressure_hp' then","if approach=='air_approach' then")
once('local toward=eligible and gap>76','local toward=eligible and gap>70')
once('local punch=eligible and (frame-first_live)%24<4','local kicking=eligible and (frame-first_live)%18<3')
once("if punch then fields['P1 High Punch']:set_value(1)end",
     "if kicking then fields['P1 Low Kick']:set_value(1)end")
once("log('PRESSURE_INPUT',string.format('policy=pressure_hp eligible=%d gap=%d toward=%d punch=%d',\n            eligible and 1 or 0,gap,toward and 1 or 0,punch and 1 or 0))",
     "log('LOWKICK_INPUT',string.format('policy=walk_lowkick eligible=%d gap=%d toward=%d kicking=%d',\n            eligible and 1 or 0,gap,toward and 1 or 0,kicking and 1 or 0))")
once('MK2_PRESSURE_BIND count=1 controller=original_physical_P1 inputs=walk_high_punch',
     'MK2_LOWKICK_BIND count=1 controller=original_physical_P1 inputs=walk_lowkick')
assert(not source:match(':write_[ui]%d+') and not source:match('%.value%s*=[^=]'))
assert(load(source,'@one_ordinary_Kano_lowkick_controller','t',_G))()

-- Retain the complete original display collector, without a second controller.
f=assert(io.open('mk2ks_native_selector_sonya_pressure_snapshot.lua','rb'))
source=f:read('a'):gsub('\r\n','\n');f:close()
once("dofile('mk2ks_native_selector_sonya_cpu_pressure_bound.lua')",
     '-- One physical controller already loaded above.')
assert(load(source,'@whole_original_dense_display_lowkick_trial','t',_G))()

-- Read actual saved driver arrays through MAME's read-only item interface.
-- No inferred owner lifetime from intended routes or audible sample numbers.
local owner_frame,owner_serial=0,0
local saved={}
local sizes={actor=4,main=4,health=2,id=2,mode=2}
local names={'actor','main','health','id','mode'}
local function bind()
 local device=assert(manager.machine.devices[':'],'Actual root driver')
 for name,index in pairs(device.items)do
  for _,field in ipairs(names)do
   if name:match('/m_mk2ks_battle_'..field..'$')then
    assert(not saved[field],'Unique actual saved battle field')
    local item=emu.item(index)
    assert(item.size==sizes[field] and item.count==2,'Actual two-player saved field layout')
    saved[field]=item
    print(string.format('MK2_VOICE_OWNER_ITEM field=%s name=%s bytes=%d count=%d writes=0 assistance=none',
     field,name,item.size,item.count))
   end
  end
 end
 for _,field in ipairs(names)do assert(saved[field],'Actual saved field '..field)end
end
local function observe(phase)
 if not saved.actor then return end
 owner_serial=owner_serial+1
 for slot=0,1 do
  print(string.format('MK2_VOICE_OWNER frame=%d seconds=%.12f serial=%d phase=%s slot=%d actor=%08X main=%08X health=%d id=%d mode=%d writes=0 assistance=none',
   owner_frame,emu.time(),owner_serial,phase,slot+1,saved.actor:read(slot),saved.main:read(slot),
   saved.health:read(slot),saved.id:read(slot),saved.mode:read(slot)))
 end
end
emu.register_frame(function()
 owner_frame=owner_frame+1
 if owner_frame==1 then bind()end
 observe('frame')
end)
emu.register_sound_update(function()observe('sound')end)
emu.register_stop(function()observe('stop')end)
