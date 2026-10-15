-- Preserve the complete original physical controller; replace only disk sinks.
local file=assert(io.open('mk2ks_native_babality_performer_probe_v738.lua','rb'))
local source=file:read('*a');file:close()
assert(not source:find(':write_',1,true))
local function replace_once(before,after)
 local first,last=assert(source:find(before,1,true))
 assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace_once("screen:snapshot('babality_'..age..'.png')","ram_snapshot('babality_'..age..'.png',frame)")
replace_once("screen:snapshot('selection_p'..n..'.png')","ram_snapshot('selection_p'..n..'.png',frame)")
replace_once("screen:snapshot('finish_window.png')","ram_snapshot('finish_window.png',frame)")
replace_once("local f=assert(io.open(assert(os.getenv('MK2KS_BABY_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "ram_emit('GUEST',raw,'frame='..frame)")
local transport=[[
local function ram_emit(tag,raw,fields)
 local hex=raw:gsub('.',function(c)return string.format('%02X',string.byte(c))end)
 print('MK2_BRAM_'..tag..' '..fields..' bytes='..#raw..' hex='..hex)
end
local function ram_snapshot(filename,frame)
 local raw=manager.machine.video:snapshot_pixels()
 local width,height=manager.machine.video:snapshot_size()
 assert(width==400 and height==254 and #raw==width*height*4)
 ram_emit('RGB',raw,'frame='..frame..' filename='..filename..' width='..width..' height='..height)
end
]]
assert(load(transport..source,'@entire_original_babality_controller_RAM_sinks_only','t',_ENV))()
