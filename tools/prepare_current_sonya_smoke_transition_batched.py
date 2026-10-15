"""Identical physical/observer records, batched bounded text transport only."""
import verify_native_source_sync as sync
sync.verify()
base=sync.ROOT/'audit_current_sonya_smoke_transition_preparation'
out=sync.ROOT/'audit_current_sonya_smoke_transition_batched_preparation'
assert not out.exists()
source=(base/'stage.lua').read_text()
old="local function log(tag,s)print(string.format('MK2_STAGE_%s frame=%d match=%d side=%d winner=%s writes=0 assistance=none %s',tag,frame,match,side,winner,s or''))end"
assert source.count(old)==1
source=source.replace(old,"""local logbuffer={}
local function flush_log()if #logbuffer>0 then print(table.concat(logbuffer,'\\n'));logbuffer={}end end
local function log(tag,s)
 logbuffer[#logbuffer+1]=string.format('MK2_STAGE_%s frame=%d match=%d side=%d winner=%s writes=0 assistance=none %s',tag,frame,match,side,winner,s or'')
 if #logbuffer>=64 then flush_log()end
end""")
old=' for _,tap in ipairs(taps)do tap:remove()end\nend)'
assert source.count(old)==1
source=source.replace(old,' flush_log()\n'+old)
assert ':write_' not in source and ':snapshot(' not in source
out.mkdir();lua=out/'stage.lua';lua.write_text(source)
runner=(base/'run.ps1').read_text().replace(base.name+'/stage.lua',out.name+'/stage.lua').replace(sync.sha(base/'stage.lua'),sync.sha(lua)).replace('audit_current_sonya_smoke_transition_runtime','audit_current_sonya_smoke_transition_batched_runtime')
(out/'run.ps1').write_text(runner)
print('Prepared only64-record text batching; same inputs/180-field return target/90sec/no media')
