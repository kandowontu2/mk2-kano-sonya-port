local frame,pulses=0,{}
local function pulse(field,first,duration) pulses[#pulses+1]={field=field,first=first,last=first+duration-1} end
local function chord(first,block,button)
 pulse(block,first,6); pulse(button,first+1,3)
end
emu.register_frame(function()
 frame=frame+1
 if frame==1 then
  local p=manager.machine.ioport.ports; local hi,sys,lo=p[":IN0"].fields,p[":IN1"].fields,p[":IN2"].fields
  pulse(hi["P1 High Punch"],300,4); pulse(sys["Coin 1"],600,4); pulse(sys["Coin 2"],615,4); pulse(sys["2 Players Start"],640,4)
  pulse(hi["P1 Left"],780,4); pulse(hi["P1 High Punch"],850,4); pulse(hi["P2 High Punch"],880,4); pulse(hi["P2 Block"],1500,1500)
  chord(1600,hi["P1 Block"],hi["P1 High Punch"])
  chord(1930,hi["P1 Block"],lo["P1 Low Punch"])
  chord(2180,hi["P1 Block"],hi["P1 High Kick"])
  pulse(lo["P1 Low Kick"],2400,190)
 end
 for _,item in ipairs(pulses) do if frame==item.first then item.field:set_value(1) end; if frame==item.last+1 then item.field:clear_value() end end
 if frame>=1580 and frame<=2780 and frame%10==0 then manager.machine.video:snapshot() end
end)
