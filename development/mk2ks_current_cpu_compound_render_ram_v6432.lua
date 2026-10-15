-- Original physical5324 input stream; continuous third leg/Square/ordinary scene.
local function read(name)
 local file=assert(io.open(name,'rb'));local source=file:read('a'):gsub('\r\n','\n');file:close();return source
end
local function change(source,before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 return source:sub(1,first-1)..after..source:sub(last+1)
end
--6422's qualified physical transport prefix routes every legacy snapshot to RAM.
local physical=read('mk2ks_current_cpu_ring_miss_audio_v6422.lua')
local stop=assert(physical:find("local source=read('mk2ks_current_cpu_ring_audio_v6383.lua')",1,true))
assert(load(physical:sub(1,stop-1),'@whole_original5324_physical_RAM_driver','t',_G))()
local source=read('mk2ks_physical_p2_cpu_ring_display_v2014.lua')
source=change(source,"dofile('mk2ks_physical_p2_cpu_ring_trace_v2013.lua')",'-- Original physical chain already installed.')
source=change(source,"local output=assert(os.getenv('MK2KS_FLOOR_OUT'))","local output='RAM_ONLY'")
source=change(source,"local move='ring'","local move='leg'")
source=change(source,"local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)')
source=change(source,'screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')
source=change(source,'if not origin then','if not origin and #shots==3 then')
--204 fields is the existing actual third-leg entry2920 through ordinary tail3124.
--No state is written; host acceptance independently requires the same actual chain.
source=change(source,'if observed_recovery and child.retired then return math.max(observed_recovery,child.retired)+30 end\n return command and command+480',
 'return command and command+204')
source=change(source,'scope=continuous_actual_P2_CPU_ring_scene_diagnostic_not_full_port',
 'scope=continuous_actual_P2_CPU_leg_square_ordinary_scene_not_full_port')
--Keep5131's native eligibility/projection/DMA observations, without its driver
--or duplicate raw stream transport:2014 already observes every used GFX byte.
local shadows=read('mk2ks_special_shadow_v5131.lua')
local first=assert(shadows:find('-- Observe every real owned shadow call',1,true))
local last=assert(shadows:find('local function snapshot_ram',first,true))
shadows=shadows:sub(first,last-1)
local raw_first=assert(shadows:find('    local key=string.format',1,true))
local raw_last=assert(shadows:find('    end\n   end\n  end\n end\nend)',raw_first,true))
shadows=shadows:sub(1,raw_first-1)..shadows:sub(raw_last+8)
shadows=shadows:gsub('if not ready or','if not active()or')
shadows=shadows:gsub('for slot in ipairs%(slots%)do','for slot=1,2 do')
shadows=shadows:gsub('local a=sample%(slot%)','local a=actor(slot)')
shadows=shadows:gsub('regs%.','cpu.')
shadows=shadows:gsub('phase_log%(','compound_shadow_log(')
assert(not shadows:find('hex=',1,true)and not shadows:find('native_gfx',1,true))
shadows=[[local function compound_shadow_log(tag,value)
 print(string.format('MK2_HPHASE_%s frame=%d move=leg side=2 attempt=3 writes=0 assistance=none %s',tag,frame,value or''))
end
]]..shadows
source=change(source,"emu.register_stop(function()\n log('FLOOR_RESULT'",shadows.."\nemu.register_stop(function()\n log('FLOOR_RESULT'")
assert(not source:find('io.open',1,true)and not source:find(':snapshot',1,true))
assert(load(source,'@whole_original2014_raster_third_leg_through_ordinary_tail_RAM','t',_G))()
