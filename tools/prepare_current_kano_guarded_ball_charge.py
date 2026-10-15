"""Physical crouch-block+LK charge compatibility, not CPU/campaign success."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_bounded_kano_ball_guard_counter_preparation'
out=sync.ROOT/'audit_current_kano_guarded_ball_charge_preparation'
assert not out.exists()
source=(base/'prepared_observer.lua').read_text()
before="   pulse(side,'Low Kick',age,0,84)"
assert source.count(before)==1
source=source.replace(before,before+"\n   if age<84 then input(side,'Down');input(side,'Block')end")
before="input(3-side,'Down');if age>=80 and age<84 then input(3-side,'High Punch')end"
assert source.count(before)==1
source=source.replace(before,"input(3-side,'Down')")
before='  part(1,a);part(2,b)'
assert source.count(before)==1
source=source.replace(before,'  if frame%5==0 then part(1,a);part(2,b)end')
source+=r'''
local guarded_ball_tap=p:install_read_tap(0xffffde00,0xffffde0f,'owned guarded-charge ball entry',function(at)
 if at~=0xffffde00 then return end
 local own=sample(side)
 if own and own.id==17 and own.roster==17 and own.owner==own.actor and regs.A8.value==own.actor and regs.A13.value==own.main then
  log('GUARDED_BALL_ENTRY',string.format('actor=%08X main=%08X owner=%08X id=%d pc=%08X charge_age=%d',own.actor,own.main,own.owner,own.id,regs.PC.value,command and frame-command or -1))
 end
end)
emu.register_stop(function()assert(guarded_ball_tap)end)
'''
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'charge.lua';lua.write_text(source)
runner=(base/'run_p1.ps1').read_text().replace(base.name+'/prepared_observer.lua',out.name+'/charge.lua').replace(sync.sha(base/'prepared_observer.lua'),sync.sha(lua)).replace('audit_bounded_kano_ball_p1_guard_counter_runtime','audit_current_kano_guarded_ball_charge_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared3500field cap physical guarded charge,no media,90sec/320MiB')
