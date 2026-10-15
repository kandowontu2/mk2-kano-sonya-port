"""Retain earned opener; test physical standing HK rather than crouch HP."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_kano_p2_sonya_standing_counter_preparation'
out=sync.ROOT/'audit_current_kano_p2_subzero_standing_preparation'
assert not out.exists()
source=(base/'campaign.lua').read_text()
old="fighter=='kano' and side==2 and other.roster==18 then"
assert source.count(old)==1
source=source.replace(old,"fighter=='kano' and side==2 and (other.roster==18 or other.roster==8) then")
source=source.replace("log('KANO_P2_SONYA_COUNTER',", "log(other.roster==18 and 'KANO_P2_SONYA_COUNTER' or 'KANO_P2_SUBZERO_STANDING',")
needle="   log('HEALTH',string.format(";assert source.count(needle)==1
source=source.replace(needle,"""   if cpu.PC.value==0xff836700 and p:read_u16(0x01061b30)==1 then
    local a,b=sample(1),sample(2);local before,after=p:read_u16(at),data&0xffff
    if a and b and a.id==8 and b.id==17 and after<before and before<=161 then
     log('KANO_P2_SUBZERO_DAMAGE',string.format('victim_slot=%d before=%d after=%d a8=%08X a13=%08X p1_actor=%08X p1_main=%08X p2_actor=%08X p2_main=%08X ids=%d,%d actions=%d,%d',n,before,after,cpu.A8.value,cpu.A13.value,a.actor,a.main,b.actor,b.main,a.id,b.id,a.action,b.action))
    end
   end
"""+needle)
old="""local function log(tag,value)
 print(string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,value or''))
end"""
assert source.count(old)==1
source=source.replace(old,"""local logbuffer={}
local function flush_log()if #logbuffer>0 then print(table.concat(logbuffer,'\\n'));logbuffer={}end end
local function log(tag,value)
 logbuffer[#logbuffer+1]=string.format('MK2_NAT_CAMPAIGN_%s frame=%d human_slot=%d fighter=%s writes=0 assistance=none %s',tag,frame,side,fighter,value or'')
 if #logbuffer>=64 then flush_log()end
end""")
old=' for _,tap in ipairs(taps)do tap:remove()end\nend)';assert source.count(old)==1
source=source.replace(old,' flush_log()\n'+old)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'campaign.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/campaign.lua',out.name+'/campaign.lua').replace(sync.sha(base/'campaign.lua'),sync.sha(lua)).replace('audit_current_kano_p2_sonya_standing_counter_runtime','audit_current_kano_p2_subzero_standing_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared only standingHK response toSubZero and bounded text batching;20000fields/90sec/no media')
