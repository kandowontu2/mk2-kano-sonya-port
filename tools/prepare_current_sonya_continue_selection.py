"""Plan physical continue cursor after native initialization; insist on true identity."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_p2_native_start_preparation'
out=sync.ROOT/'audit_current_sonya_continue_selection_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='css=frame;selections=selections+1;plan=route(p:read_u16(slots[side].roster))'
assert source.count(old)==1
source=source.replace(old,'css=frame;selections=selections+1;plan={}')
old='  local age=frame-css\n  for index,direction in ipairs(plan)do'
assert source.count(old)==1
source=source.replace(old,'''  local age=frame-css
  if age==56 then
   local initialized=p:read_u16(slots[side].roster)
   plan=route(initialized)
   log('SELECT_INITIALIZED',string.format('number=%d roster=%d target=%d path=%s',selections,initialized,identity,table.concat(plan,',')))
  end
  if age==146 then assert(p:read_u16(slots[side].roster)==identity,'Native cursor did not reach requested fighter')end
  for index,direction in ipairs(plan)do''')
source=source.replace('frame>=30000','frame>=12000').replace('maximum_fields=30000','maximum_fields=12000')
source+='''
local continued_fight=nil
emu.register_frame_done(function()
 if selections<2 or p:read_u16(0x010601d0)~=2 then return end
 local own=sample(side)
 if not own or own.state~=1 then return end
 assert(own.roster==18 and own.id==18 and own.owner==own.actor)
 continued_fight=continued_fight or frame
 local age=frame-continued_fight
 if age<=160 then
  log('CONTINUE_PAIR',string.format('age=%d actor=%08X main=%08X owner=%08X id=%d roster=%d state=%d hp=%d',
   age,own.actor,own.main,own.owner,own.id,own.roster,own.state,own.hp))
 end
 if age==160 then log('CONTINUE_COMPLETE','fields=161');manager.machine:exit()end
end)
'''
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_sonya_p2_native_start_runtime','audit_current_sonya_continue_selection_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared delayed native cursor planning, real Sonya confirmation/161continued match fields,no media')
