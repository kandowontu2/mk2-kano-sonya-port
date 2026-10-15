"""Approach before morph, within the real pre-announcement finisher window."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_actor_tap_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_window_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
source = source.replace('  if wins<2 or mode~=5 then return end\n', '')
start = source.index('  if own.id==6 and age>=65 and age<85 then')
end = source.index('   local command_age=frame-approach_done', start)
source = source[:start]+'''  if not approach_done then
   if gap<target_gap-4 then press(winner_side,back)
   elseif gap>target_gap+4 then press(winner_side,forward)
   else approach_done=frame;log('APPROACH','gap='..gap)end
  end
  if approach_done and own.id==6 then
   local morph_age=frame-approach_done
   if killer=='kano' then
    if morph_age<2 or(morph_age>=8 and morph_age<10)then press(winner_side,back)end
    if morph_age>=4 and morph_age<6 then press(winner_side,'Down')end
    if morph_age>=8 and morph_age<10 then press(winner_side,'Low Kick')end
   elseif killer=='sonya'and morph_age<8 then
    press(winner_side,'Down');press(winner_side,'Low Punch');press(winner_side,'Block')
   end
  end
  if approach_done and own.id==killer_id then
'''+source[end:]
source = source.replace('local command_age=frame-approach_done', 'local command_age=frame-approach_done-40')
source = source.replace(' elseif frame>=5800 then', ''' elseif first_live and wins>=2 and p:read_u16(0x010601d0)==3 and not action_start then
  log('BOUNDED_FAILED','reason=native_window_ended_without_finisher raw_media=none')
  manager.machine:exit()
 elseif frame>=5800 then''')
assert all(banned not in source for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('))
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_morphed_finisher_actor_tap_', 'audit_bounded_morphed_finisher_window_')
        runner = runner.replace("'-str','100'", "'-str','120'")
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared actual native finisher-window physical positioning/morph/command sequence')
