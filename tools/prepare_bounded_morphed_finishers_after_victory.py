"""Wait for real second victory; retain failed early-morph test unchanged."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_after_victory_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
before = '  finish_start=finish_start or frame'
assert source.count(before) == 1
source = source.replace(before, '  if wins<2 or mode~=5 then return end\n'+before)
before = " local own=sample(winner_side)\n if not first_live or not own or at~=own.actor+0x1f0"
assert source.count(before) == 1
source = source.replace(before, " if not first_live or(cpu.PC.value~=0xff86e670 and cpu.PC.value~=0xffa16700)then return end\n local own=sample(winner_side)\n if not own or at~=own.actor+0x1f0")
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_morphed_finisher_', 'audit_bounded_morphed_finisher_after_victory_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared after-victory genuine morph test; native stores remain passive')
