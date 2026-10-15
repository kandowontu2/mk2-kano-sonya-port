"""Passive original gate/counter evidence; identical physical Sonya controls."""
import verify_native_source_sync as sync

sync.verify()
old=sync.ROOT/'audit_bounded_morphed_friendship_followthrough_preparation'
out=sync.ROOT/'audit_morphed_friendship_eligibility_reads_preparation'
assert not out.exists()
source=(old/'friendships.lua').read_text()
marker='emu.register_frame(function()\n frame=frame+1'
assert source.count(marker)==1
source=source.replace(marker,'''taps[#taps+1]=p:install_read_tap(0x01061e40,0x01061e7f,'native original eligibility counter read',function(at,data,mask)
 if not window or cpu.PC.value<0xff880770 or cpu.PC.value>=0xff880a70 then return end
 log('ELIGIBILITY_READ',string.format('at=%08X data=%04X mask=%08X pc=%08X a8=%08X a13=%08X',at,data&0xffff,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value))
end)
'''+marker)
marker="  log('BOOT','own_id='..id..' victim_id='..victim_id..' guest_writes=0')"
assert source.count(marker)==1
source=source.replace(marker,marker+'''
  for at=0xff880770,0xff880890,16 do
   log('ORIGINAL_GATE_WORD',string.format('at=%08X word=%04X',at,p:read_u16(at)))
  end''')
out.mkdir()
lua=out/'friendships.lua'
lua.write_text(source)
for side in(1,2):
    runner=(old/f'run_sonya_p{side}_path_checked.ps1').read_text()
    runner=runner.replace(old.name+'/friendships.lua',out.name+'/friendships.lua')
    runner=runner.replace(sync.sha(old/'friendships.lua'),sync.sha(lua))
    runner=runner.replace(f'audit_bounded_morphed_friendship_followthrough_sonya_p{side}_runtime',f'audit_morphed_friendship_eligibility_sonya_p{side}_runtime')
    (out/f'run_sonya_p{side}.ps1').write_text(runner)
print('Prepared two passive native eligibility-read observations, unchanged actual controls')
