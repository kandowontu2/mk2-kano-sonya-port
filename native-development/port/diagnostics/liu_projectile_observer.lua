-- Passive Liu projectile geometry. No controls or guest-state writes.
do
 local machine=manager.machine
 local space=machine.devices[':maincpu'].spaces.program
 local head=assert(tonumber(os.getenv('KS_ACTIVE_LIST')))
 local frame=0
 local out=assert(io.open('liu_projectiles.csv','w'))
 out:write('frame,process,object,valid,projectileX,velocityX,ownX,ownAction,enemyAction,ownHP,enemyHP,movingAwayBeyond64\n')
 local function word(address) return space:read_u16(address) end
 local function long(address)
  local value=0
  for i=0,3 do value=value|(space:read_u8(address+i*8)<<(i*8)) end
  return value
 end
 local function signed(value,bits)
  return value<(1<<(bits-1)) and value or value-(1<<bits)
 end
 local function valid(address) return address>=0x01000000 and address<0x01400000 end
 emu.register_frame_done(function()
  frame=frame+1
  if word(0x010601d0)~=2 then return end
  local own,enemy=long(0x01060220),long(0x01060df0)
  if not valid(own) or not valid(enemy) or word(own+0x1f0)~=17 or word(enemy+0x1f0)~=1 then return end
  local ownproc,enemyproc=long(0x01060260),long(0x01060e30)
  assert(valid(ownproc) and valid(enemyproc))
  local ox=signed(word(own+0x90),16)
  local cursor=long(head);local seen={};local count=0;local found=false
  local function record(process,object,good,x,vx)
   local away=good and math.abs(x-ox)>=64 and ((x<ox and vx<0) or (x>ox and vx>0))
   out:write(string.format('%d,%08x,%08x,%d,%d,%d,%d,%d,%d,%d,%d,%d\n',frame,
    process,object,good and 1 or 0,x,vx,ox,word(ownproc+0x1f0),word(enemyproc+0x1f0),
    word(0x010602f0),word(0x01060ec0),away and 1 or 0))
  end
  while cursor~=0 do
   assert(valid(cursor) and not seen[cursor] and count<512,'Invalid active process list')
   seen[cursor]=true;count=count+1
   if word(cursor+0x20)==0x800 then
    found=true
    local object=long(cursor+0xc0) -- MAINEQU.pa8; MKZAP.spawn_proj_proc
    local good=valid(object)
    record(cursor,object,good,good and signed(word(object+0x90),16) or 0,
           good and signed(long(object+0x40),32) or 0) -- DISPEQU.oxvel
   end
   cursor=long(cursor)
  end
  if not found then record(0,0,false,0,0) end
  out:flush()
 end)
end
