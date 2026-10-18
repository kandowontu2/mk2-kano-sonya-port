-- Loaded-state planning ONLY. Reset Lua controller bookkeeping, never guest data.
;(function()
 local planning={}
 local path=assert(os.getenv('KS_PLANNING_STATE'))
 local events=assert(io.open('planning_state_load.csv','w'))
 events:write('event,restoredControllerField,attempt,mode,map\n')
 planning.subscription=emu.add_machine_post_load_notifier(function()
  -- These are Lua locals, not emulated registers/health/positions/results.
  n=129988;previousMode=7;selection=180;locked=true;enteredCombat=true
  combat=0;plan=nil;planAge=0;continuing=false;continuesUsed=25;lastHealth=91
  events:write(string.format('loaded,%d,%d,%d,%d\n',n,continuesUsed,u16(0x010601d0),u16(0x01061b30)))
  events:close()
 end)
 m:load(path)
end)()
