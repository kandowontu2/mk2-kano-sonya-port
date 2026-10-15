-- Exact whole deferred observer; restore only original physical P2 admission.
local path='mk2ks_p1_ending_deferred_display_ram_v5257.lua'
local file=assert(io.open(path,'rb'));local source=file:read('a');file:close()
local before='assert(side==1)'
local a,b=source:find(before,1,true)
assert(a and not source:find(before,b+1,true),'One original physical admission')
source=source:sub(1,a-1)..'assert(side==2)'..source:sub(b+1)
local first=assert(source:find('local winner_entry=',1,true))
local last=assert(source:find('\n]])',first,true))
local addresses={['0x01060280']='0x01060e50',['0x01060e50']='0x01060280',
 ['0x010602f0']='0x01060ec0',['0x01060ec0']='0x010602f0',
 ['0x010602ff']='0x01060ecf',['0x01060ecf']='0x010602ff',
 ['0x010601f0']='0x01060dc0',['0x01060dc0']='0x010601f0',
 ['0x01060220']='0x01060df0',['0x01060df0']='0x01060220'}
local admission=source:sub(first,last-1)
admission=admission:gsub('0x010[0-9a-f]+',function(address)return addresses[address]or address end)
local old='mode,roster,p:read_u16(0x01060280)'
local new='mode,p:read_u16(0x01060280),roster'
local oa,ob=admission:find(old,1,true)
assert(oa and not admission:find(old,ob+1,true),'One physical attract-roster output order')
admission=admission:sub(1,oa-1)..new..admission:sub(ob+1)
source=source:sub(1,first-1)..admission..source:sub(last)
assert(load(source,'@'..path..'::whole_deferred_original_P2_admission_only','t',_ENV))()
