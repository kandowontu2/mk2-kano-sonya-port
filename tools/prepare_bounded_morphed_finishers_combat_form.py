"""Genuine second-round morph before final KO; finish in the actual form."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_window_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_combat_form_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
source = source.replace('local join_at=nil', 'local join_at=nil\nlocal combat_morph=nil')
before = '   if gap>80 then press(winner_side,forward)'
assert source.count(before) == 1
source = source.replace(before, '''   if wins==1 and victim.hp<=41 and own.id==6 and not combat_morph then
    combat_morph=frame;log('COMBAT_MORPH_BEGIN','victim_hp='..victim.hp)
   end
   if combat_morph and frame-combat_morph<40 then
    local morph_age=frame-combat_morph
    if killer=='kano' then
     if morph_age<2 or(morph_age>=8 and morph_age<10)then press(winner_side,back)end
     if morph_age>=4 and morph_age<6 then press(winner_side,'Down')end
     if morph_age>=8 and morph_age<10 then press(winner_side,'Low Kick')end
    elseif killer=='sonya'and morph_age<8 then
     press(winner_side,'Down');press(winner_side,'Low Punch');press(winner_side,'Block')
    end
   elseif gap>80 then press(winner_side,forward)''')
source = source.replace('local command_age=frame-approach_done-40', 'local command_age=frame-approach_done')
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_morphed_finisher_window_', 'audit_bounded_morphed_finisher_combat_form_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared genuine combat morph before last KO; native finish timing retained')
