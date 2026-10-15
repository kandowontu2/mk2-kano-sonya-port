-- Entire original cold physical mirror controller; only file sinks changed.
local root=assert(os.getenv('MK2KS_PORT_ROOT'))
local f=assert(io.open(root..'/mk2ks_natural_mirror_finish_v1166.lua','rb'))
local source=f:read('*a');f:close()
local function replace_once(before,after)
 local first,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,first-1)..after..source:sub(last+1)
end
replace_once("local function save(file,data)local f=assert(io.open(output..'/'..file,'wb'));f:write(data);f:close()end",
 "local function save(file,data)ram_emit('DATA',data,'filename='..file)end")
replace_once("for _,file in ipairs(pending)do screen:snapshot(file);log('SNAPSHOT','file='..file)end",
 "for _,file in ipairs(pending)do ram_snapshot(file,frame);log('SNAPSHOT','file='..file)end")
local transport=[[
local function ram_emit(tag,raw,fields)
 print('MK2_PRIMARY_RAM_'..tag..' '..fields..' bytes='..#raw..' hex='..
  raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end
local function ram_snapshot(filename,frame)
 local raw=manager.machine.video:snapshot_pixels()
 local width,height=manager.machine.video:snapshot_size()
 assert(width==400 and height==254 and #raw==400*254*4)
 ram_emit('RGB',raw,'frame='..frame..' filename='..filename..' width='..width..' height='..height)
end
]]
assert(load(transport..source,'@entire_original1166_controller_only_RAM_sinks','t',_ENV))()
