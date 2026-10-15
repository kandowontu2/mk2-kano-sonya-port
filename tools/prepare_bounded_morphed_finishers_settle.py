"""Release combat inputs and let the real uppercut recover before morphing."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_combat_form_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_settle_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
assert source.count("combat_morph=frame;log('COMBAT_MORPH_BEGIN'") == 1
source = source.replace("combat_morph=frame;log('COMBAT_MORPH_BEGIN'", "combat_morph=frame+80;log('COMBAT_MORPH_BEGIN'")
source = source.replace('if morph_age<2 or(morph_age>=8 and morph_age<10)then',
    'if morph_age>=0 and(morph_age<2 or(morph_age>=8 and morph_age<10))then')
source = source.replace("elseif killer=='sonya'and morph_age<8 then", "elseif killer=='sonya'and morph_age>=0 and morph_age<8 then")
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_morphed_finisher_combat_form_', 'audit_bounded_morphed_finisher_settle_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared real release/recovery before combat morph, no state assistance')
