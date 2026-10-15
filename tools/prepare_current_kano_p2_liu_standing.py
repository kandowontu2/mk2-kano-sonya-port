"""Keep two earned match clears; only use standing counter against real Liu2."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_subzero_low_knife_preparation'
out=sync.ROOT/'audit_current_kano_p2_liu_standing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old='(other.roster==18 or other.roster==8)';assert source.count(old)==1
source=source.replace(old,'(other.roster==18 or other.roster==8 or other.roster==2)')
old="other.roster==18 and 'KANO_P2_SONYA_COUNTER' or 'KANO_P2_SUBZERO_STANDING'"
assert source.count(old)==1
source=source.replace(old,"other.roster==18 and 'KANO_P2_SONYA_COUNTER' or other.roster==8 and 'KANO_P2_SUBZERO_STANDING' or 'KANO_P2_LIU_STANDING'")
needle="   log('HEALTH',string.format(";assert source.count(needle)==1
source=source.replace(needle,"""   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==2 then
    local a,b=sample(1),sample(2);local before,after=p:read_u16(at),data&0xffff
    if a and b and a.id==2 and b.id==17 and after<before and before<=161 then
     log('KANO_P2_LIU_DAMAGE',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d',n,before,after,cpu.A8.value,cpu.A13.value,a.actor,a.main,b.actor,b.main,a.id,b.id,a.action,b.action))
    end
   end
"""+needle)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_subzero_low_knife_runtime','audit_current_kano_p2_liu_standing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared actual Liu2 physical standing counter only;20000fields/90sec/320MiB/no media')
