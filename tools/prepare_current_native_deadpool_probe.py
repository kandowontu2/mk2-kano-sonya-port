"""Physical held-LP/LK crouch-uppercut probe; actual outcome not assumed."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_native_tomb_preparation'
out=sync.ROOT/'audit_current_native_deadpool_probe_preparation';assert not out.exists()
source=(base/'stage.lua').read_text()
start=source.index("     if winner=='kano'then\n");end=source.index('     end\n    end\n',start)+len('     end\n')
source=source[:start]+'''     if age>=5 and age<44 then press(side,'Low Punch');press(side,'Low Kick')end
     if age>=16 and age<44 then press(side,'Down')end
     if age>=32 and age<36 then press(side,'High Punch')end
'''+source[end:]
source+='''
taps[#taps+1]=p:install_read_tap(0xff870dc0,0xff870dcf,'actual earned uppercut',function(at)
 if at~=0xff870dc0 or cpu.PC.value~=at+16 or not command or p:read_u16(0x01061ac0)~=0 then return end
 local own=sample(side)
 if not own or own.id~=id or cpu.A8.value~=own.actor then return end
 action=action or frame;action_arena=0
 log('ACID_UPPERCUT_ENTRY',string.format('entry=%08X pc=%08X actor=%08X main=%08X a8=%08X a13=%08X id=%d',at,cpu.PC.value,own.actor,own.main,cpu.A8.value,cpu.A13.value,own.id))
end)
'''
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run_kano_p1.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua))
runner=runner.replace('audit_current_native_tomb_kano_p1_runtime','audit_current_native_deadpool_probe_kano_p1_runtime').replace("MK2KS_STAGE_ARENA='1'","MK2KS_STAGE_ARENA='0'")
(out/'run.ps1').write_text(runner)
print('Prepared held LP/LK plus settled crouch HP after earned KOs; native outcome observed/no media')
