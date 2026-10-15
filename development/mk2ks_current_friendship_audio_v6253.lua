-- Same original physical controls; omit only the redundant RGB transport.
local function read(path)
 local f=assert(io.open(path,'rb'));local s=f:read('*a');f:close();return s
end
local function replace(s,before,after)
 local first,last=assert(s:find(before,1,true));assert(not s:find(before,last+1,true))
 return s:sub(1,first-1)..after..s:sub(last+1)
end
local controls=read('mk2ks_current_friendship_scene_v6244.lua')
controls=replace(controls," {'mk2ks_current_friendship_snapshot_pixels_v3573.lua',\"dofile('mk2ks_current_friendship_stream_wins_v3568.lua')\"}\n",'')
assert(load(controls,'@whole_original_Friendship_controls_without_RGB'))()
local identity=assert(({kano=17,sonya=18})[os.getenv('MK2KS_FRIEND_WINNER')])
local side=assert(tonumber(os.getenv('MK2KS_FRIEND_SIDE')))
local entry=0xff800000+(identity==17 and 0xf9a00 or 0xf9c00)*8
local observer=read('mk2ks_current_tomb_winner_mix_observer_v5779.lua')
observer=replace(observer,'local frame,origin,taps,channels=0,nil,{},{}',
 'local frame,origin,taps,channels,friend_window=0,nil,{},{},nil')
observer=replace(observer,'local function active()return origin and frame<=origin+1100 end',
 'local function active()return origin and friend_window and frame<=friend_window+1600 end')
observer=replace(observer,'0xff8bdfe0,0xff8bdfef',string.format('0x%x,0x%x',entry,entry+15))
observer=replace(observer,'at~=0xff8bdfe0',string.format('at~=0x%x',entry))
observer=replace(observer,"os.getenv('MK2KS_STAGE_WINNER')","os.getenv('MK2KS_FRIEND_WINNER')")
observer=replace(observer,' frame=frame+1\n if frame==1 then\n  -- Native',
 string.format([[ frame=frame+1
 if not friend_window and p:read_u16(0x010601d0)==2 and p:read_u16(0x01061b00)==3 then
  local a,m=p:read_u32(0x%x),p:read_u32(0x%x)
  if valid(a)and valid(m)and p:read_u16(a+0x1f0)==%d and p:read_u32(m+0xc0)==a then friend_window=frame end
 end
 if frame==1 then
  -- Native]],side==1 and 0x01060220 or 0x01060df0,side==1 and 0x01060260 or 0x01060e30,identity))
observer=replace(observer,"assert(checks==2 and origin and frame==origin+1101,'Both complete original sound ROM checks and genuine native terminal')",
 "assert(checks==2 and origin and friend_window and frame==friend_window+1601,'Both full original ROM checks and genuine original Friendship terminal')")
assert(load(observer,'@whole_native_Friendship_DAC_PCM_ROM_observer'))()
