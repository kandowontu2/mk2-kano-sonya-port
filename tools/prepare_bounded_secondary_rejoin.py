"""Physical challenger rejoin after secondary completion, bounded scene samples."""
import verify_native_source_sync as sync
sync.verify()
old=sync.ROOT/'audit_bounded_secondary_finishers_preparation'
out=sync.ROOT/'audit_bounded_secondary_rejoin_preparation'
assert not out.exists()
out.mkdir()
source=(old/'finishers.lua').read_text()
marker=' if action_start and wrap and frame-wrap>=120 then'
assert source.count(marker)==1
source=source.replace(marker,' if false then -- original early stop replaced by bounded physical rejoin')
source+='''
local rejoin_css,rejoin_live,visual_count=nil,nil,0
local function rejoin_snap(label)
 visual_count=visual_count+1;assert(visual_count<=3)
 screen:snapshot('rejoin_'..label..'.png');log('REJOIN_VISUAL','sample='..label..' count='..visual_count)
end
emu.register_frame(function()
 if not wrap then return end
 local age=frame-wrap
 if age>=350 and age<354 then press(side,'Coin')end
 if age>=368 and age<372 then press(side,'Start')end
 local mode=p:read_u16(0x010601d0)
 if age>120 and mode==4 and not rejoin_css then rejoin_css=frame;log('REJOIN_CSS','mode=4')end
 local own,victim=sample(winner_side),sample(side)
 if rejoin_css and mode==2 and own and victim and own.id==killer_id and victim.id==identity and own.hp==161 and victim.hp==161 and not rejoin_live then
  rejoin_live=frame;log('REJOIN_LIVE',string.format('own_id=%d victim_id=%d own_owner=%08X own_actor=%08X victim_owner=%08X victim_actor=%08X',own.id,victim.id,own.owner,own.actor,victim.owner,victim.actor))
 end
 if rejoin_live and frame-rejoin_live>=60 then log('REJOIN_TERMINAL','next_match_survival=60');manager.machine:exit()end
 if age>=1600 then log('REJOIN_FAILED','reason=no_rejoined_match');manager.machine:exit()end
end)
emu.register_frame_done(function()
 if not wrap then return end
 if frame-wrap==300 then rejoin_snap('completed_scene')end
 if rejoin_css and frame-rejoin_css==30 then rejoin_snap('selection')end
 if rejoin_live and frame-rejoin_live==30 then rejoin_snap('next_match')end
end)
'''
lua=out/'rejoin.lua'
lua.write_text(source)
for fighter in ('kano','sonya'):
    runner=(old/f'run_{fighter}_p1.ps1').read_text()
    runner=runner.replace(old.name+'/finishers.lua',out.name+'/rejoin.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_secondary_finisher_{fighter}_p1_runtime',f'audit_bounded_secondary_rejoin_{fighter}_p1_runtime')
    runner=runner.replace("rawMedia='none'","rawMedia='bounded_three_png'")
    (out/f'run_{fighter}.ps1').write_text(runner)
