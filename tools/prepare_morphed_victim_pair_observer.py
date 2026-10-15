"""Independent full-field publication ledger, no ownership-gated omissions."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_morphed_victim_finishers_preparation'
out=sync.ROOT/'audit_morphed_victim_pair_observer_preparation';assert not out.exists()
source=(old/'finishers.lua').read_text()
source+='''
emu.register_frame_done(function()
 if not action_start then return end
 for n=1,2 do
  local current=sample(n)
  if current then
   log('PEER',string.format('slot=%d actor=%08X main=%08X owner=%08X character_id=%d roster=%d hp=%d pose=%08X attached=%08X y=%d floor=%d flags=%04X',
    n,current.actor,current.main,current.owner,current.id,current.roster,current.hp,current.pose,
    p:read_u32(current.main+0x190),current.y,p:read_i16(current.main+0x200),current.flags))
  else log('PEER_MISSING','slot='..n)end
 end
end)
'''
out.mkdir();lua=out/'finishers.lua';lua.write_text(source)
for target in('kano','sonya'):
    for side in(1,2):
        runner=(old/f'run_{target}_p{side}.ps1').read_text()
        runner=runner.replace(old.name+'/finishers.lua',out.name+'/finishers.lua').replace(sync.sha(old/'finishers.lua'),sync.sha(lua))
        runner=runner.replace(f'audit_bounded_morphed_victim_finisher_{target}_p{side}_runtime',f'audit_morphed_victim_pair_{target}_p{side}_runtime')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared exact physical replay with independent paired publications every action field')
