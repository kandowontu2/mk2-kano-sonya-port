"""Normal credits/Start after friendly finishers, no state fixtures/media."""
import verify_native_source_sync as sync

sync.verify()
out=sync.ROOT/'audit_bounded_friendly_rejoin_preparation'
assert not out.exists()
out.mkdir()
for kind,folder,own in (('friendship','friendships','id'),('babality','babalities','winner_id')):
    old=sync.ROOT/f'audit_bounded_current_{folder}_preparation'
    original=old/(folder+'.lua')
    source=original.read_text()
    assert source.count('if age>=720 then manager.machine:exit()end')==1
    source=source.replace('if age>=720 then manager.machine:exit()end','-- extended through physical rejoin')
    source=source.replace('frame>=5500','frame>=6500').replace('limit=5500','limit=6500')
    source+='''
local rejoin_request,rejoin_css,rejoin_live=nil,nil,nil
local victim_side=3-side
emu.register_frame(function()
 if not action then return end
 local mode=p:read_u16(0x010601d0)
 if mode==3 and p:read_u16(slots[victim_side].state)==2 and not rejoin_request then
  rejoin_request=frame;log('REJOIN_REQUEST','mode=3 loser_state=2')
 end
 if not rejoin_request then return end
 local age=frame-rejoin_request
 if (age>=20 and age<25)or(age>=270 and age<275)then press(victim_side,'Coin')end
 if age>=310 and age<315 then
  if age==310 then css[victim_side]=nil;exits[victim_side]=nil;plans[victim_side]=nil end
  press(victim_side,'Start')
 end
 if mode==4 and not rejoin_css then rejoin_css=frame;log('REJOIN_CSS','mode=4')end
 local h,v=sample(side),sample(victim_side)
 if rejoin_css and mode==2 and h and v and h.id==OWN_ID and v.id==victim_id and h.hp==161 and v.hp==161 and h.owner==h.actor and v.owner==v.actor and not rejoin_live then
  rejoin_live=frame;log('REJOIN_LIVE',string.format('own_id=%d victim_id=%d own_actor=%08X own_owner=%08X victim_actor=%08X victim_owner=%08X',h.id,v.id,h.actor,h.owner,v.actor,v.owner))
 end
 if rejoin_live and frame-rejoin_live>=60 then log('REJOIN_TERMINAL','next_match_survival=60');manager.machine:exit()end
 if age>=2000 then log('REJOIN_FAILED','reason=no_rejoined_match');manager.machine:exit()end
end)
'''.replace('OWN_ID',own)
    lua=out/(kind+'.lua')
    lua.write_text(source)
    assert ':snapshot(' not in source and ':write_' not in source
    for fighter in ('kano','sonya'):
        for side in (1,2):
            runner=(old/f'run_{fighter}_p{side}.ps1').read_text()
            runner=runner.replace(old.name+'/'+original.name,out.name+'/'+lua.name).replace(sync.sha(original),sync.sha(lua))
            runner=runner.replace(f'audit_bounded_current_{kind}_{fighter}_p{side}_runtime',f'audit_bounded_rejoin_{kind}_{fighter}_p{side}_runtime')
            runner=runner.replace("'-str','100'","'-str','130'")
            (out/f'run_{kind}_{fighter}_p{side}.ps1').write_text(runner)
print('Prepared eight bounded text-only friendly-finisher paid rejoin cases')
