-- Passive program-read tap, no return value: never changes emulated reads.
do
 local m=manager.machine;local cpu=m.devices[':maincpu'];local p=cpu.spaces.program
 local address=assert(tonumber(os.getenv('KS_NORMAL_STRIKE_PC')))
 local log=assert(io.open('normal_strike_entries.csv','w'))
 log:write('frame,pc,side,actor,action,table,xoffset,yoffset,width,height,flags,x,y,left,right,top,bottom\n')
 local frame,count=0,0
 local function word(a)return p:read_u8(a)|(p:read_u8(a+8)<<8)end
 local function long(a)return word(a)|(word(a+16)<<16)end
 local function signed(a)local v=word(a);return v>=32768 and v-65536 or v end
 local function valid(a)return a>=0x01000000 and a<0x01400000 end
 local tap=p:install_read_tap(address,address+15,'ks_normal_strike_entry',function()
  count=count+1;assert(count<=10000,'Strike-entry tap bound exceeded')
  if word(0x010601d0)~=2 then return end
  local me=cpu.state['A8'].value;local table=cpu.state['A0'].value
  if not valid(me) then return end
  local first,second=long(0x01060220),long(0x01060df0)
  local side=me==first and 1 or (me==second and 2 or 0)
  if side==0 then return end
  local proc=long(side==1 and 0x01060260 or 0x01060e30)
  if not valid(proc) or word(me+0x1f0)~=17 or word(proc+0x1f0)~=0x101 then return end
  local victim=side==1 and second or first
  assert(valid(victim))
  local image=long(victim+0x1a0)
  local left,right,top,bottom=65535,-5000,65535,0
  for index=0,63 do
   local part=image+index*112;assert(valid(part) and valid(part+112))
   if long(part)==0 then break end
   local x=signed(victim+0x90)-signed(part+80);local y=signed(victim+0xb0)-signed(part+96)
   left=math.min(left,x);right=math.max(right,x+word(part+32))
   top=math.min(top,y);bottom=math.max(bottom,y+word(part+48))
  end
  log:write(string.format('%d,%08x,%d,%d,%d,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',
   frame,cpu.state['PC'].value,side,word(me+0x1f0),word(proc+0x1f0),table,
   signed(table),signed(table+16),word(table+32),word(table+48),word(me+0xf0),
   signed(me+0x90),signed(me+0xb0),left,right,top,bottom));log:flush()
 end)
 -- Frame callback retains the tap. Each record is flushed; process exit
 -- closes the file when the primary bounded controller exits earlier.
 emu.register_frame_done(function()
  frame=frame+1;assert(tap)
  if frame==9000 then tap:remove();log:close() end
 end)
end
