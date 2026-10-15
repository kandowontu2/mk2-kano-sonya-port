-- Observe original native bulk reset/free membership/reuse, no game writes.
local file=assert(io.open('mk2ks_native_selector_sonya_death_raw_objects.lua','rb'))
local source=file:read('a'):gsub('\r\n','\n');file:close()
local function replace(before,after)
 local at,last=assert(source:find(before,1,true));assert(not source:find(before,last+1,true))
 source=source:sub(1,at-1)..after..source:sub(last+1)
end
replace('assert(valid(a)and a~=subject and not objects[a])',
 'assert(valid(a)and a~=subject and(not objects[a]or objects[a].retired))')
local count=0
source=source:gsub('if not item then return end',function()
 count=count+1;return 'if not item or item.retired then return end'
end)
assert(count==2,'Same original legitimate native-address retirement handling')
replace("for _,entry in ipairs({{0xffa0e060,'first',9},{0xffa0e3b0,'second',10}})do",[[
local drain_sequence=0
local pool_first,pool_stride,pool_count=0x0102d6f0,0x210,0x166
local pool_end=pool_first+pool_stride*pool_count
local function drain_log(tag,value)
 drain_sequence=drain_sequence+1
 print(string.format('MK2_DEATH_DRAIN_%s frame=%d sequence=%d %s writes=0 assistance=none',tag,frame,drain_sequence,value))
end
local function chain(head,free)
 local at=p:read_u32(head);local nodes,seen={},{}
 while at~=0 and(not free or(at~=pool_end and at~=0x00fe0190))do
  assert(valid(at)and not seen[at]and #nodes<1024,'Valid unique native pool/list node')
  if free then assert(at>=pool_first and at<pool_end and(at-pool_first)%pool_stride==0)end
  nodes[#nodes+1]=at;seen[at]=true;at=p:read_u32(at)
 end
 if free then assert(at==pool_end or at==0x00fe0190,'Exact original native pool stop')end
 return nodes,seen,at
end
local function csv(values)
 if #values==0 then return '-'end
 local s={};for _,a in ipairs(values)do s[#s+1]=string.format('%08X',a)end
 return table.concat(s,',')
end
local function drain_snapshot(tag)
 if not next(objects)then return end
 local sets,parts={},{}
 for _,entry in ipairs({{'objects',0x0105d480},{'layer1',0x0105d4a0},{'layer2',0x0105d4c0},{'freeObjects',0x01060130}})do
  local list,seen,stop=chain(entry[2],entry[1]=='freeObjects');sets[entry[1]]=seen
  parts[#parts+1]=string.format('%s=%s %sCount=%d %sStop=%08X',entry[1],csv(list),entry[1],#list,entry[1],stop)
 end
 table.sort(parts)
 drain_log(tag,string.format('mode=%d %s',p:read_u16(0x010601d0),table.concat(parts,' ')))
 for a,item in pairs(objects)do
  local active=(sets.objects[a]or sets.layer1[a]or sets.layer2[a])and 1 or 0
  drain_log('MEMBER',string.format('context=%s kind=%s birth=%d subject=%08X active=%d free=%d bulkReset=%d reused=%d %s',
   tag,item.kind,item.born,item.subject,active,sets.freeObjects[a]and 1 or 0,item.bulkReset or -1,item.reused or -1,object_words(a)))
 end
end
for _,entry in ipairs({{0xffa0e060,'first',9},{0xffa0e3b0,'second',10}})do
]])
replace('emu.register_frame(function()frame=frame+1 end)',[[
for _,entry in ipairs({{0xff83f060,'RESET_ENTER'},{0xff83f200,'RESET_COMPLETE'},{0xff809150,'POOL_POP'}})do
 taps[#taps+1]=p:install_read_tap(entry[1],entry[1]+15,'actual native tracked bulk reset or free-pool pop',function(at,data,mask)
  if at~=entry[1]or cpu.PC.value~=at+16 or not next(objects)then return end
  if entry[2]=='POOL_POP'then
   local a=cpu.A0.value;local item=objects[a]
   if not item or not item.bulkReset or item.reused then return end
   item.reused=frame
   drain_log('REUSE',string.format('kind=%s birth=%d subject=%08X entry=%08X pc=%08X opcode=%04X mask=%04X head=%08X %s %s',
    item.kind,item.born,item.subject,at,cpu.PC.value,data&0xffff,mask&0xffff,p:read_u32(0x01060130),object_words(a),registers()))
   drain_snapshot('REUSE_LISTS')
  else
   drain_log(entry[2],string.format('entry=%08X pc=%08X opcode=%04X mask=%04X freeHead=%08X %s',
    at,cpu.PC.value,data&0xffff,mask&0xffff,p:read_u32(0x01060130),registers()))
   if entry[2]=='RESET_COMPLETE'then
    for _,item in pairs(objects)do if not item.bulkReset then item.bulkReset=frame end end
   end
   drain_snapshot(entry[2]..'_LISTS')
  end
 end)
end
emu.register_frame(function()frame=frame+1 end)
]])
replace(' local label=marks[frame]'," drain_snapshot('FIELD_LISTS')\n local label=marks[frame]")
assert(load(source,'@whole_original_raw_capture_plus_direct_bulk_pool_drain','t',_G))()
