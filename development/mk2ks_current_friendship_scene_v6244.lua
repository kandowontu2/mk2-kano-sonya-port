-- Execute the complete original physical controller, changing only guest
-- export from a disk dump to a read-only stdout transport. Original audio,
-- native winner and actual snapshot-rendering observers remain unchanged.
local function source(path)
 local f=assert(io.open(path,'rb'));local s=f:read('*a');f:close();return s
end
local function replace(s,before,after)
 local first,last=assert(s:find(before,1,true))
 assert(not s:find(before,last+1,true),'One exact observer adaptation')
 return s:sub(1,first-1)..after..s:sub(last+1)
end
local probe=source('mk2ks_current_friendship_stream_probe_v3566.lua')
probe=replace(probe,"  local f=assert(io.open(assert(os.getenv('MK2KS_FRIEND_OUT'))..'/guest_maincpu.bin','wb'));f:write(raw);f:close()",
 "  print('MK2_CURRENT_FRIEND_GUEST bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))")
assert(load(probe,'@whole_original_friendship_physical_controller'))()
for _,item in ipairs({
 {'mk2ks_current_friendship_stream_audio_v3567.lua',"dofile('mk2ks_current_friendship_stream_probe_v3566.lua')"},
 {'mk2ks_current_friendship_stream_wins_v3568.lua',"dofile('mk2ks_current_friendship_stream_audio_v3567.lua')"},
 {'mk2ks_current_friendship_snapshot_pixels_v3573.lua',"dofile('mk2ks_current_friendship_stream_wins_v3568.lua')"}
})do
 assert(load(replace(source(item[1]),item[2],''),'@'..item[1]))()
end
