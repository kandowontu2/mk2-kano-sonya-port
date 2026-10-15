"""Current native Tomb via physical paid rematches; no dumps or snapshots."""
import re
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_native_tomb_preparation';assert not out.exists()
source=(sync.ROOT/'mk2ks_current_stage_ram_driver_v3594.lua').read_text()
dump="  local raw=p:read_range(0xff800000,0xffffffff,8,8);assert(#raw==1048576)\n  local f=assert(io.open(assert(os.getenv('MK2KS_STAGE_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()"
assert source.count(dump)==1;source=source.replace(dump,'  -- No raw guest capture.')
needle='if at~=entry or not window then return end';assert source.count(needle)==1
source=source.replace(needle,'if at~=entry or cpu.PC.value~=at+16 or not window then return end')
needle=' frame=frame+1\n';assert source.count(needle)==1
source=source.replace(needle,needle+" if frame>=12000 then log('HOST_BOUND','maximum_fields=12000');manager.machine:exit();return end\n")
assert ':write_' not in source and 'read_range' not in source and 'snapshot(' not in source and 'io.open' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
base=sync.ROOT/'audit_current_kano_native_winner_preparation'
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/stage.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua))
runner=runner.replace('audit_current_kano_native_winner_runtime','audit_current_native_tomb_kano_p1_runtime')
runner=re.sub(r'^\$env:.*\n','',runner,flags=re.M)
needle='$taskArgs=@(';assert runner.count(needle)==1
runner=runner.replace(needle,"$env:MK2KS_STAGE_WINNER='kano'\n$env:MK2KS_STAGE_SIDE='1'\n$env:MK2KS_STAGE_ARENA='1'\n$env:MK2KS_STAGE_CASE='positive'\n"+needle)
(out/'run_kano_p1.ps1').write_text(runner)
print('Prepared natural current Tomb: earned two-KO matches/paid rematch, passive scene fields; no media')
