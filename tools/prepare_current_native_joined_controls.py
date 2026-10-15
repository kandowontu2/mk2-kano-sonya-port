"""Successor joined match: release both selectors, exercise physical controls."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_joined_matches_preparation'
out=sync.ROOT/'audit_current_native_joined_controls_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
source=source.replace("{'Left','Right','Down','High Punch'}","{'Left','Right','Down','Up','High Punch','High Kick'}")
needle="emu.register_frame(function()\n if not join_selection then return end"
assert source.count(needle)==1
source=source.replace(needle,"""emu.register_frame(function()
 for n=1,2 do for _,field in pairs(joined_buttons[n])do field:clear_value()end end
 if joined_live then
  local age=frame-joined_live
  local side=(math.floor(age/180)%2)+1
  local phase=age%180
  local key=nil
  if phase>=10 and phase<28 then key=side==1 and 'Right' or 'Left'
  elseif phase>=50 and phase<54 then key='High Punch'
  elseif phase>=90 and phase<94 then key='High Kick'
  elseif phase>=130 and phase<138 then key='Up' end
  if key then joined_buttons[side][key]:set_value(1)
   log('JOINED_CONTROL',string.format('age=%d slot=%d button=%s',age,side,key:gsub(' ','_')))
  end
  return
 end
 if not join_selection then return end""")
old="age,n,row.actor,row.main,row.owner,row.id,row.roster,row.state,row.hp))"
assert source.count(old)==1
source=source.replace("state=%d hp=%d',age,n", "state=%d hp=%d action=%d x=%d y=%d',age,n")
source=source.replace(old,"age,n,row.actor,row.main,row.owner,row.id,row.roster,row.state,row.hp,row.action,row.x,row.y))")
source=source.replace("if age==160 then log('JOINED_MATCH_COMPLETE','fields=161')","if age==1599 then log('JOINED_MATCH_COMPLETE','fields=1600')")
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
for p1,p2 in [(17,18),(18,17)]:
 runner=(base/f'run_{p1}_{p2}.ps1').read_text()
 runner=runner.replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
 runner=runner.replace(f'audit_current_native_joined_{p1}_{p2}_runtime',f'audit_current_native_joined_controls_{p1}_{p2}_runtime')
 (out/f'run_{p1}_{p2}.ps1').write_text(runner)
print('Prepared bounded joined physical controls, both selector inputs explicitly released')
