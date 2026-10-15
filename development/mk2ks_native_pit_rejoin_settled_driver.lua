-- Entire earned driver and rejoin policy. Plan ONLY later CSS inputs after
-- native cursor initialization; never trust the previous match's roster word.
local f=assert(io.open('mk2ks_native_tomb_rejoin_driver.lua','rb'))
local source=f:read('a'):gsub('\r\n','\n');f:close()
local function once(old,new)
 local first,last=assert(source:find(old,1,true));assert(not source:find(old,last+1,true))
 source=source:sub(1,first-1)..new..source:sub(last+1)
end
once('if mode==4 and p:read_u16(slots[n].state)==3 then',
 'if mode==4 and p:read_u16(slots[n].state)==3 and p:read_u16(slots[n].roster)<=18 then')
once("join_css[n]={at=frame,path=route(p:read_u16(slots[n].roster),target)}\n     join_log('SELECT','slot='..n..' target='..target..' route='..table.concat(join_css[n].path,','))",
 "join_css[n]={at=frame,path=nil}\n     join_log('SELECT_OPEN','slot='..n..' previous_roster='..p:read_u16(slots[n].roster)..' target='..target)")
once('local css_age=frame-join_css[n].at',
 "local css_age=frame-join_css[n].at\n    if css_age==56 then\n     local cursor=p:read_u16(slots[n].roster)\n     join_css[n].path=route(cursor,target)\n     join_log('SELECT','slot='..n..' start='..cursor..' target='..target..' route='..table.concat(join_css[n].path,','))\n    end")
once('for i,key in ipairs(join_css[n].path)do','for i,key in ipairs(join_css[n].path or{})do')
assert(not source:find(':write_',1,true))
assert(load(source,'@whole_original_earned_driver_only_later_real_initialized_CSS_route','t',_ENV))()
