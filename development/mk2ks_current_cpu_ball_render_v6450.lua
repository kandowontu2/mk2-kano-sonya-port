-- Whole original6293 controls; source body/raster/shadow observation only.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local sink=read('mk2ks_native_tomb_ram_v3624.lua')
local stop=assert(sink:find("local handle=assert(io.open('mk2ks_native_tomb_display_v2062.lua'",1,true))
assert(load(sink:sub(1,stop-1),'@whole_original_RAM_renderer_transport','t',_G))()
assert(load(read('mk2ks_current_kano_cpu_extended_ram_v6290.lua'),'@whole_original6293_physical_inputs','t',_G))()
local source=read('mk2ks_physical_p2_cpu_ring_display_v2014.lua')
local function change(before,after)
 local a,b=assert(source:find(before,1,true));assert(not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
change("dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')",'-- Qualified original physical chain already loaded.')
change('local frame,command=0,nil','local frame,command=0,1813')
change("local move='ring'","local move='ball'")
change("local output=assert(os.getenv('MK2KS_FLOOR_OUT'))","local output='RAM_ONLY'")
change("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)')
change('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')
change('origin=frame;command=frame','origin=frame;-- Keep passive pre-entry observation bound unchanged.')
change('if observed_recovery and child.retired then return math.max(observed_recovery,child.retired)+30 end\n return command and command+480',
 'return command and 1918')
-- Ball is selected before the first legacy live-pair callback. Keep a second
-- full read-only physical binding for EVERY observation callback, including
-- that pre-entry gap. This adds no controls and replaces no original rows.
change('-- The original helper allocates A10;',[[emu.register_frame(function()
 if frame<1813 or frame>1919 then return end
 for slot=1,2 do
  local a=assert(actor(slot))
  log('BALL_BINDING',string.format('slot=%d actor=%08X main=%08X owner=%08X id=%d roster=%d floor=%d',
   slot,a.actor,a.main,a.owner,a.id,a.roster,a.floor))
 end
end)
-- The original helper allocates A10;]])
local shadows=read('mk2ks_special_shadow_v5131.lua')
local a=assert(shadows:find('-- Observe every real owned shadow call',1,true))
local b=assert(shadows:find('local function snapshot_ram',a,true));shadows=shadows:sub(a,b-1)
local first=assert(shadows:find('    local key=string.format',1,true))
local last=assert(shadows:find('    end\n   end\n  end\n end\nend)',first,true))
shadows=shadows:sub(1,first-1)..shadows:sub(last+8)
shadows=shadows:gsub('if not ready or','if not active()or')
shadows=shadows:gsub('for slot in ipairs%(slots%)do','for slot=1,2 do')
shadows=shadows:gsub('local a=sample%(slot%)','local a=actor(slot)')
-- Original5131 uses regs and phase_log;2014 exposes cpu and log instead.
shadows=shadows:gsub('regs%.','cpu.'):gsub('phase_log%(','ball_shadow_log(')
shadows=[[
local function ball_shadow_log(tag,value)
 print(string.format('MK2_HPHASE_%s frame=%d writes=0 assistance=none %s',tag,frame,value or''))
end
]]..shadows
assert(not shadows:find('hex=',1,true)and not shadows:find('native_gfx',1,true))
change("emu.register_stop(function()\n log('FLOOR_RESULT'",shadows.."\nemu.register_stop(function()\n log('FLOOR_RESULT'")
assert(not source:find('io.open',1,true)and not source:find('screen:snapshot',1,true))
assert(load(source,'@whole_original2014_and5131_ball_render_and_shadow','t',_G))()
