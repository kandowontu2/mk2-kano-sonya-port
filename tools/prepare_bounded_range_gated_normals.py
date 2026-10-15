"""Range- and recovery-gated physical normal contacts after specials."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_current_special_cycles_preparation'
out=sync.ROOT/'audit_bounded_range_gated_normals_preparation'
assert not out.exists()
out.mkdir()
source=(old/'cycles.lua').read_text()
marker=' if followup then\n'
start=source.index(marker)
end=source.index("   elseif age>=400 then",start)
source=source[:start]+''' if followup then
    normal_index=normal_index or 1
    local buttons={'High Punch','Low Punch','High Kick','Low Kick'}
    if normal_index<=4 then
     if not normal_start then
      if clean(own)and clean(victim)then
       if math.abs(own.x-victim.x)>48 then input(side,own.x<victim.x and'Right'or'Left');normal_settle=nil
       else normal_settle=normal_settle or frame
        if frame-normal_settle>=12 then normal_start=frame;log('NORMAL_COMMAND',string.format('index=%d button=%s gap=%d',normal_index,buttons[normal_index],math.abs(own.x-victim.x)))end
       end
      else normal_settle=nil end
     end
     if normal_start then
      pulse(side,buttons[normal_index],frame-normal_start,0,3)
      if frame-normal_start>=100 and clean(own)and clean(victim)then log('NORMAL_RECOVERED','index='..normal_index);normal_index=normal_index+1;normal_start=nil;normal_settle=nil end
     end
    elseif clean(own)and clean(victim)then completed=2;log('FINAL');rawset(_G,'MK2_SPECIAL_EXIT_PENDING',true)end
''' + source[end:]
lua=out/'normals.lua'
lua.write_text(source)
for move in ('knife','ring'):
    for side in (1,2):
        runner=(old/f'run_{move}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/cycles.lua',out.name+'/normals.lua').replace(sync.sha(old/'cycles.lua'),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_current_special_cycles_{move}_p{side}_runtime',f'audit_bounded_range_gated_normals_{move}_p{side}_runtime')
        (out/f'run_{move}_p{side}.ps1').write_text(runner)
