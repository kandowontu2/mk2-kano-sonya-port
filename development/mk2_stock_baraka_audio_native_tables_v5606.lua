-- Preserve5602's real stock-selection failure. Use original ROM navigation
-- and round-win tables; retain the complete physical controller and audio.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2_stock_baraka_audio_reference_v5602.lua','rb'))
local source=f:read('*a');f:close();source=source:gsub('\r\n','\n')
local before="execute(s,'921_original_roster_physical_controller_without_snapshot_sink')"
local first,last=source:find(before,1,true)
assert(first and not source:find(before,last+1,true),'One whole-controller native table correction')
local after=[[s=replace(s,'local tables={Left=0xffff1400,Right=0xffff1600,Down=0xffff1200}',
 'local tables={Left=0xff898000,Right=0xff8980c0,Down=0xff897f40}')
s=replace(s,"taps[#taps+1]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,'actual native round wins',function(at)",
 "taps[#taps+1]=p:install_read_tap(0xff822280,0xff822280+17*32-1,'actual native round wins',function(at)")
s=replace(s,'at==0xfffef800+killer_id*32','at==0xff822280+killer_id*32')
execute(s,'921_original_roster_and_native_navigation_win_tables_physical_controller')]]
source=source:sub(1,first-1)..after..source:sub(last+1)
assert(load(source,'@entire5602_stock_reference_only_native_navigation_win_tables_corrected','t',_ENV))()
