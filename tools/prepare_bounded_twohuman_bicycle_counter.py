"""Physical two-player command and counter; scalar-only natural collision."""
import json
import verify_native_source_sync as sync

def main():
    sync.verify()
    old=sync.ROOT/'audit_bounded_twohuman_idle_preparation'
    out=sync.ROOT/'audit_bounded_twohuman_bicycle_counter_preparation';assert not out.exists()
    source=(old/'prepared_observer.lua').read_text()
    start=source.index(' if frame>=3000 then')
    source=source[:start]+r'''
 if frame>=3500 then log('FAILED','reason=bounded_timeout');manager.machine:exit();return end
 if ready then
  assert(pair_live(a,b),'True selected two-human pair')
  part(1,a);part(2,b)
  local own,victim=side==1 and a or b,side==1 and b or a
  if frame-ready>=420 then log('COUNTER_TERMINAL');manager.machine:exit();return end
  if not command then
   if math.abs(own.x-victim.x)>80 then input(side,own.x<victim.x and 'Right' or 'Left');settle=nil
   elseif clean(own) and clean(victim) then
    settle=settle or frame
    if frame-settle>=20 then
     command=frame;attempt=1;forward=own.x<victim.x and 'Right' or 'Left';backward=forward=='Right' and 'Left' or 'Right'
     log('COMMAND','gap='..math.abs(own.x-victim.x))
    end
   end
  end
  if command then
   local age=frame-command
   pulse(side,backward,age,0,3);pulse(side,backward,age,6,3);pulse(side,'Down',age,12,3);pulse(side,'High Kick',age,13,3)
   if age>=18 and age<100 and age%12<3 then input(3-side,'High Kick')end
  end
 end
end)
local counter_taps={}
counter_taps[1]=p:install_write_tap(0x01d01030,0x01d0103f,'actual private cue',function(at,value,mask)
 if at==0x01d01030 and value>=0x6b00 and value<=0x6b03 then log('CUE',string.format('seconds=%.12f value=%04X',emu.time(),value))end
end)
for slot,address in ipairs({0x010602f0,0x01060ec0})do
 counter_taps[#counter_taps+1]=p:install_write_tap(address,address+15,'actual counter health',function(at,value,mask)
  if ready then log('HEALTH',string.format('seconds=%.12f slot=%d before=%d after=%d pc=%08X',emu.time(),slot,p:read_u16(address),value&65535,regs.PC.value))end
 end)
end
emu.register_stop(function()assert(#counter_taps==3);log('STOP','raw_media=none')end)
'''
    assert ':write_' not in source and ':snapshot(' not in source and ':pixels(' not in source
    out.mkdir();observer=out/'prepared_observer.lua';observer.write_text(source)
    runner=(old/'run.ps1').read_text()
    for before,after in {old.name:out.name,
        'audit_bounded_twohuman_sonya_kitana_idle_runtime':'audit_bounded_twohuman_bicycle_counter_runtime',
        sync.sha(old/'prepared_observer.lua'):sync.sha(observer),
        "MK2KS_HUMAN_SPECIAL_MOVE='ring'":"MK2KS_HUMAN_SPECIAL_MOVE='bicycle'",
        "MK2KS_HUMAN_SPECIAL_VICTIM='kitana'":"MK2KS_HUMAN_SPECIAL_VICTIM='kano'"}.items():
        assert runner.count(before)==1;runner=runner.replace(before,after)
    (out/'run.ps1').write_text(runner)
    (out/'report.json').write_text(json.dumps(dict(prepared=True,observerSHA256=sync.sha(observer),rawMedia=False,assistance='none')))

if __name__=='__main__':main()
