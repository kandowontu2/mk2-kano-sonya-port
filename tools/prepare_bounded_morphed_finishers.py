"""Earn as Shang, then command a real added-form morph and its finisher."""
import json
import verify_native_source_sync as sync

sync.verify()
old = sync.ROOT/'audit_bounded_own_finishers_dispatch_preparation'
out = sync.ROOT/'audit_bounded_morphed_finishers_preparation'
assert not out.exists()
source = (old/'finishers.lua').read_text()
def once(before, after):
    global source
    assert source.count(before) == 1, before
    source = source.replace(before, after)

once('n==side and identity or killer_id)', 'n==side and identity or 6)')
once('n==side and identity or killer_id,table.concat', 'n==side and identity or 6,table.concat')
once('at==0xfffef800+killer_id*32', 'at==0xfffef800+6*32')
once('own.id~=killer_id or victim.id~=identity or own.owner~=own.actor',
     '(own.id~=6 and own.id~=killer_id)or own.roster~=6 or victim.id~=identity or own.owner~=own.actor')
once('if age>=65 and not approach_done then', '''if own.id==6 and age>=65 and age<85 then
   local morph_age=age-65
   if killer=='kano' then
    if morph_age<2 or(morph_age>=8 and morph_age<10)then press(winner_side,back)end
    if morph_age>=4 and morph_age<6 then press(winner_side,'Down')end
    if morph_age>=8 and morph_age<10 then press(winner_side,'Low Kick')end
   elseif killer=='sonya'and morph_age<8 then
    press(winner_side,'Down');press(winner_side,'Low Punch');press(winner_side,'Block')
   end
  end
  if own.id==killer_id and age>=125 and not approach_done then''')
once("assert(#taps==20,'Retain both original action variants and native table lookup observers')",
     "assert(#taps==21,'Retain original finisher observers plus passive native morph store')")
marker='emu.register_frame(function()\n assert(#taps==21'
once(marker, '''taps[#taps+1]=p:install_write_tap(0x01000000,0x010fffff,'actual winner native ID',function(at,data,mask)
 local own=sample(winner_side)
 if not first_live or not own or at~=own.actor+0x1f0 or mask&0xffff~=0xffff then return end
 log('MORPH_STORE',string.format('old=%d id=%d actor=%08X main=%08X roster=%d pc=%08X a9=%08X a0=%08X',
  own.id,data&0xffff,own.actor,own.main,own.roster,cpu.PC.value,cpu.A9.value,cpu.A0.value))
end)
emu.register_frame(function()
 assert(#taps==21''')
assert all(banned not in source for banned in (':write_', ':snapshot(', ':pixels(', 'io.open('))
out.mkdir()
lua = out/'finishers.lua'
lua.write_text(source)
for target in ('kano', 'sonya'):
    for side in (1, 2):
        runner = (old/f'run_{target}_p{side}.ps1').read_text()
        runner = runner.replace(old.name+'/finishers.lua', out.name+'/finishers.lua')
        runner = runner.replace(sync.sha(old/'finishers.lua'), sync.sha(lua))
        runner = runner.replace('audit_bounded_own_finisher_dispatch_', 'audit_bounded_morphed_finisher_')
        (out/f'run_{target}_p{side}.ps1').write_text(runner)
(out/'report.json').write_text(json.dumps(dict(prepared=True, sourceSHA256=sync.sha(old/'finishers.lua'),
    observerSHA256=sync.sha(lua), acceptance=False, rawMedia='none')))
print('Prepared physical Shang selection, earned rounds, genuine morph and own finisher commands')
