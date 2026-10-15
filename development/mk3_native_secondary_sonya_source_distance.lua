-- Original Sonya player2 second-fatality reference, physical inputs only.
local filename='mk3_native_secondary_kano_reference.lua'
local file=assert(io.open(filename,'r'))
local source=file:read('a');file:close()
local swaps={
 ['0x010609b0']='0x01061560',['0x01061560']='0x010609b0',
 ['0x01060a40']='0x010615f0',['0x010615f0']='0x01060a40'
}
source=source:gsub('0x010[%x]+',function(literal)return swaps[literal]or literal end)
local replacements={
 {"local raw,w,h=machine.screens[':screen']:pixels()",
  "local screen=machine.screens[':screen'];local raw=screen:pixels();local w,h=screen.width,screen.height"},
 {"fields={right=high['P1 Right'],left=high['P1 Left'],hk=high['P1 High Kick'],\n          lp=low['P1 Low Punch'],block=high['P1 Block']}",
  "fields={right=high['P2 Right'],left=high['P2 Left'],hk=high['P2 High Kick'],\n          lp=low['P2 Low Punch'],block=high['P2 Block'],up=high['P2 Up'],down=high['P2 Down'],run=low['P2 Run']}"},
 {'if i~=0 or j~=1 then','if i~=1 or j~=0 then'},
 {'if gap>45 then press(forward)','if gap>65 then press(forward)'},
 {"if gap>20 then press(forward)else command=frame;geometry('COMMAND_SPACING')end",
  "if gap<224 then press(x<y and 'left' or 'right')elseif gap>240 then press(forward)else command=frame;geometry('COMMAND_SPACING')end"},
 {'0xff9b5cd0,0xff9b62c0,0xff9b12e0,0xff998750,0xff9987e0,0xff991f70,0xffa5ef10,0xffa5ef50',
  '0xff9ae0b0,0xff9ae5d0,0xff998750,0xff9987e0,0xff991f70,0xff9923b0,0xff993160,0xff9931f0,0xff993760,0xff992090,0xffa5ef10,0xffa5ef50'},
 {'if at==0xff9b5cd0 and not start then','if at==0xff9ae0b0 and not start then'},
 {"local ca=frame-command\n   for _,item in ipairs({{'lp',10},{'block',20},{'block',30},{'hk',40}})do",
  "local ca=frame-command\n   if ca>=6 and ca<45 then press('block')end\n   if ca>=39 and ca<45 then press('run')end\n   for _,at in ipairs({4,14,24,34,44,70})do if ca==at then pending[#pending+1]='command_age_'..ca end end\n   for _,item in ipairs({{'up',10},{'up',20},{x<y and 'left' or 'right',30},{'down',40}})do"},
 {"geometry('FIELD')",
  "geometry('FIELD')\n  for side,actor in ipairs({a,b})do local bank=p:read_u16(actor+0x140)&0x7f00;local colors={}\n   for color=0,63 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01880000+(bank+color)*16))end\n   log('PALETTE_FIELD',string.format('age=%d side=%d actor=%08X bank=%04X colors=%s',frame-start,side,actor,bank,table.concat(colors,',')))end"}
}
for _,pair in ipairs(replacements)do
 local at=assert(source:find(pair[1],1,true))
 assert(not source:find(pair[1],at+#pair[1],true))
 source=source:sub(1,at-1)..pair[2]..source:sub(at+#pair[1])
end
assert(load(source,'@'..filename..'::original_sonya_source_distance'))()
