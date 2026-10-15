"""Observe only the real spawned actor ID, preserving after-victory inputs."""
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_morphed_finishers_after_victory_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_actor_tap_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
begin = "taps[#taps+1]=p:install_write_tap(0x01000000,0x010fffff,'actual winner native ID',function(at,data,mask)"
start = source.index(begin)
end = source.index('emu.register_frame(function()', start)
block = source[start:end]
source = source[:start]+source[end:]
block = block.replace("0x01000000,0x010fffff,'actual winner native ID'", "own.actor+0x1f0,own.actor+0x1ff,'actual winner native ID'")
before = "assert(#taps==21,'Retain original finisher observers plus passive native morph store')"
assert source.count(before) == 1
source = source.replace(before, "assert(#taps==(first_live and 21 or 20),'Retain original observers plus spawned actor ID tap')")
before = "  if not first_live then first_live=frame;log('FIRST_LIVE',string.format('own=%08X victim=%08X ids=%d,%d',own.actor,victim.actor,own.id,victim.id))end"
assert source.count(before) == 1
source = source.replace(before, "  if not first_live then\n   first_live=frame\n   "+block+"   log('FIRST_LIVE',string.format('own=%08X victim=%08X ids=%d,%d',own.actor,victim.actor,own.id,victim.id))\n  end")
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_morphed_finisher_after_victory_', 'audit_bounded_morphed_finisher_actor_tap_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
print('Prepared one-actor ID observer; physical inputs and caps unchanged')
