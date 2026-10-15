-- Original whole Kano campaign; clone its existing physical reactive routine
-- only ahead of zoning against true Kitana4. No guest or game-state writes.
local path='mk2ks_kano_current_p2_campaign_ram_v4472.lua'
local file=assert(io.open(path,'rb'));local adapted=file:read('a');file:close()
local function once(before,after)
 local first,last=adapted:find(before,1,true)
 assert(first and not adapted:find(before,last+1,true),'One exact original assembly boundary')
 adapted=adapted:sub(1,first-1)..after..adapted:sub(last+1)
end
once("assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='2')",
     "assert(os.getenv('MK2KS_CAMPAIGN_SIDE')=='1')")
once("local adapted,count=source:gsub('screen:snapshot%(', '_campaign_emit(')",[=[
local zoning="   elseif strategy=='zoning' then\n"
local zfirst,zlast=source:find(zoning,1,true)
assert(zfirst and not source:find(zoning,zlast+1,true),'One original regular zoning branch')
local tail="   else\n    -- Read-only feedback: jump from actual grounded state"
local first,last=source:find(tail,zlast+1,true)
assert(first and not source:find(tail,last+1,true),'Whole original reactive input routine')
local bodyfirst=first+#"   else\n"
local final="    previous_y=human.y\n"
local finalfirst,finallast=source:find(final,last+1,true)
assert(finalfirst and not source:find(final,finallast+1,true),'Exact complete reactive routine tail')
local body=source:sub(bodyfirst,finallast)
source=source:sub(1,zfirst-1).."   elseif strategy=='zoning' and other.roster==4 then\n"..body..source:sub(zfirst)
print('MK2_CURRENT_KANO_KITANA_PHYSICAL_POLICY true_cpu=4 cloned_original_reactive_body=1 timing_changes=0 writes=0 assistance=none')
local adapted,count=source:gsub('screen:snapshot%(', '_campaign_emit(')]=])
assert(load(adapted,'@'..path..'::original_full_Kano_inputs_with_Kitana_reactive_priority','t',_ENV))()
