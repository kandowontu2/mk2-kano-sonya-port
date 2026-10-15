-- Genuine CPU-earned loss/paid continue followed by the whole original native
-- UI navigation/stock-border/blink/pose/fade/ladder/first-match controller.
-- Release the startup P1 punch on BOTH slots. No state/HP/RNG/CPU writes.
local f=assert(io.open('mk2ks_single_continue_v6567.lua','rb'))
local source=f:read('*a');f:close()
local function edit(before,after)
 local first,last=assert(source:find(before,1,true))
 assert(not source:find(before,last+1,true),'One exact presentation adaptation')
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
edit('for _,field in pairs(buttons)do field:clear_value()end',
 "for _,field in pairs(buttons)do field:clear_value()end\n high['P1 High Punch']:clear_value()")
edit("local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Start',age,80,5)",
 "local age=frame-continueAt;pulse('Coin',age,20,5);pulse('Coin',age,270,5);pulse('Start',age,310,5)")
edit("continueAt=frame;log('CONTINUE'","continueAt=frame;_MK2_UI_CONTINUE_ARMED=true;log('CONTINUE'")
edit('if mode==4 and state==3 then reselect=frame;',
 'if mode==4 and state==3 and _MK2_UI_CSS_FRAME then reselect=frame;')
edit('if mode==4 then select_inputs(reselect,rePlan,ids[target])',
 'if mode==4 then -- the complete original UI controller owns continued selection')
local fixed=[[ if reReady then
  local age=frame-reReady
  local away=own and enemy and own.x<enemy.x and 'Left' or 'Right'
  pulse(away,age,12,24);pulse('Up',age,64,3);pulse('High Punch',age,128,3)
  if age==38 or age==80 or age==145 or age==180 then snap('continued_control')end
  if age>=180 then manager.machine:exit()end
 end]]
edit(fixed,' -- Native UI driver owns its full180-field post-selection Block window.')
edit('a8=%08X a13=%08X',
 'a8=%08X a13=%08X ctxOwner=%08X parent=%08X ctxID=%d pairActor=%08X pairMain=%08X pairAction=%d caller=%08X')
edit('cpu.A8.value,cpu.A13.value))',
 [[cpu.A8.value,cpu.A13.value,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0xc0)or 0,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x230)or 0,
 valid(cpu.A8.value)and p:read_u16(cpu.A8.value+0x1f0)or -1,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x140)or 0,
 valid(cpu.A13.value)and p:read_u32(cpu.A13.value+0x170)or 0,
 valid(cpu.A13.value)and valid(p:read_u32(cpu.A13.value+0x170))and p:read_u16(p:read_u32(cpu.A13.value+0x170)+0x1f0)or -1,
 p:read_u32(cpu.SP.value)))]])
edit('emu.register_frame_done(function()',[[emu.register_frame_done(function()
 log('IO',string.format('in0=%04X',manager.machine.ioport.ports[':IN0']:read()))]])
assert(load(source,'@mk2ks_single_continue_v6567.lua::released_startup_native_continue_UI'))()

f=assert(io.open('mk2ks_native_ui_flow_v2_probe.lua','rb'));source=f:read('*a');f:close()
edit("os.getenv('MK2KS_UI_FIGHTER')","os.getenv('MK2PORT_SINGLE_CONTINUE_TARGET')")
edit("os.getenv('MK2KS_UI_SIDE')","os.getenv('MK2PORT_SINGLE_CONTINUE_SIDE')")
edit('frame=frame+1;for _,field in pairs(fields)do field:clear_value()end',
 'frame=frame+1;if css_at then for _,field in pairs(fields)do field:clear_value()end end')
edit("if frame>=300 and frame<304 then fields['High Punch']:set_value(1)end",'-- Startup input belongs exclusively to the released base controller.')
edit("if not css_at and frame>=boot then local age=(frame-boot)%300;pulse('Coin',age,0);pulse('Start',age,20)end",'-- Only the base controller supplies genuine paid continue input.')
edit('if not css_at and frame>700 and css then css_at=frame;',
 'if not css_at and _MK2_UI_CONTINUE_ARMED and frame>700 and css then css_at=frame;_MK2_UI_CSS_FRAME=frame;')
edit('screen:snapshot(name)','_ui_emit(name,frame)')
local helper=[[
local function _ui_emit(label,frame)
 local raw=manager.machine.video:snapshot_pixels()
 local width,height=manager.machine.video:snapshot_size()
 assert(width==400 and height==254 and #raw==406400)
 print(string.format('MK2_SC_RGB frame=%d label=%s bytes=%d width=%d height=%d hex=%s',frame,label,#raw,width,height,
 raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(helper..source,'@mk2ks_native_ui_flow_v2_probe.lua::real_paid_continue_full_native_UI'))()
