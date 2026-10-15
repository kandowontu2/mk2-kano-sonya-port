"""Physical coin-to-start delay, observe accepted P1 state rather than inferred join."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_battle_audio_join_selection_preparation'
out=sync.ROOT/'audit_current_native_challenger_join_delay_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="if age>=8 and age<12 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end"
assert source.count(old)==1
source=source.replace(old,"if age>=24 and age<28 then join_button:set_value(1);log('JOIN_INPUT','button=Start_1 age='..age)end")
source+='''
emu.register_frame_done(function()
 if not join_start then return end
 local age=frame-join_start
 if age<=300 or (join_selection and frame-join_selection<=160) then
  log('JOIN_PLAYER_STATE',string.format('age=%d mode=%d p1=%d p2=%d credits=%d',age,p:read_u16(0x010601d0),
   p:read_u16(slots[1].state),p:read_u16(slots[2].state),manager.machine.ioport.ports[':IN1']:read()))
 end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_battle_audio_join_selection_runtime','audit_current_native_challenger_join_delay_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared normal Coin1 ages1..4/Start1 ages24..27 and actual player-state readings,no media')
