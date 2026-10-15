-- Preserve the real6081 controller, hash transport and all original taps.
-- Take bounded native pictures at each actual owned stream phase, not a
-- guessed fatality age that only captures Mileena's long preparatory poses.
local root=assert(os.getenv('MK2KS_CURRENT_ROOT'))
local path=root..'/mk2ks_current_mileena_native_v6081.lua'
local file=assert(io.open(path,'r'));local source=file:read('*a');file:close()
local function replace(before,after)
 local a,b=source:find(before,1,true);assert(a and not source:find(before,b+1,true))
 source=source:sub(1,a-1)..after..source:sub(b+1)
end
replace('local current_shots={[0]=true,[8]=true,[16]=true,[24]=true,[32]=true,[64]=true,[128]=true,[600]=true}',
        'local current_shots={[0]=true,[600]=true}')
replace('emu.register_frame_done(function()',[=[
local current_lookup=nil
local current_lookup_address=0xffd61800+identity*32
local current_lookup_tap=p:install_read_tap(current_lookup_address,current_lookup_address+15,'actual true victim stream phase origin',function(at,data,mask)
 if action and not current_lookup and at==current_lookup_address and cpu.PC.value==0xff83b850 then
  current_lookup=frame
  print(string.format('MK2_CURRENT_MILEENA_LOOKUP frame=%d action=%d id=%d pc=%08X mask=%04X writes=0 assistance=none',frame,action,identity,cpu.PC.value,mask))
 end
end)
emu.register_stop(function()current_lookup_tap:remove()end)
emu.register_frame_done(function()
]=])
replace('if action and current_shots[frame-action]then',
        'if action and(current_shots[frame-action]or current_lookup and frame>=current_lookup and frame<current_lookup+(identity==17 and 7 or 8)*4 and(frame-current_lookup)%4==0)then')
assert(load(source,'@'..path..'::actual_native_stream_phase_screens_v6090','t',_ENV))()
