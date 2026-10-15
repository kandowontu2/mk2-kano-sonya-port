-- Existing renderer observer, read-only ending window and RAM sinks only.
-- Native physical controls are loaded separately by the exact role wrapper.
local h=assert(io.open('mk2ks_native_tomb_ram_v3624.lua','r'))
local ram=h:read('a');h:close()
local sink_end=assert(ram:find("local handle=assert(io.open",1,true))
assert(load(ram:sub(1,sink_end-1),'@original3624_RAM_transport_functions_only','t',_ENV))()
h=assert(io.open('mk2ks_native_tomb_display_v2062.lua','r'))
local source=h:read('a');h:close()
local function once(old,new)
 local at=assert(source:find(old,1,true),'One declared original renderer boundary')
 assert(not source:find(old,at+#old,true),'Unique original renderer boundary')
 source=source:sub(1,at-1)..new..source:sub(at+#old)
end
local function region(first,last,new)
 local a=assert(source:find(first,1,true));local b=assert(source:find(last,a+#first,true))
 assert(not source:find(first,a+#first,true),'Unique declared region start')
 assert(not source:find(last,b+#last,true),'Unique declared region end')
 source=source:sub(1,a-1)..new..source:sub(b)
end
once("dofile('mk2ks_stage_branch_provenance_v1722.lua')",'')
once('local frame,command=0,nil','local frame,command,ending_completed,ending_ko,own_wins,seen_live=0,nil,nil,nil,0,false')
once("local output=assert(os.getenv('MK2KS_STAGE_OUT'))","local output=assert(os.getenv('MK2KS_CAMPAIGN_OUT'))")
once("local side=tonumber(assert(os.getenv('MK2KS_STAGE_SIDE')))","local side=tonumber(assert(os.getenv('MK2KS_CAMPAIGN_SIDE')));assert(side==1)")
once("os.getenv('MK2KS_STAGE_WINNER')","os.getenv('MK2KS_TEST_FIGHTER')")
once('local function window_end()return retired.frame and retired.frame+30 or command and command+1000 end',
 'local function window_end()return ending_completed and ending_completed+300 or command and command+4000 end')
once('f>=command+1','f>=command')
once("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)')
once('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)')
-- Endings are not floor-shadow/body-palette tests. All actor publications,
-- CPU pixels, DMA, actual graphics bytes, shift clears and RGB remain logged.
-- Do not classify cinematic props or native attract fighters as Kano/Sonya.
region('local function actor(n)','-- The original helper allocates A10;',
 'local function actor(n)return nil end\n\n')
region('for _,address in ipairs({action_entry})do','-- Observe actual native sound-port writes;',[[
local winner_entry=0xfffef800+identity*32
taps[#taps+1]=p:install_read_tap(winner_entry,winner_entry+15,'actual own final-stage first winner',function(at,data,mask)
 if at~=winner_entry or cpu.PC.value~=0xff8296b0 or p:read_u16(0x01061b30)~=16 or
  p:read_u16(0x01061b00)~=side or p:read_u16(0x01060280)~=identity or
  p:read_u16(0x01060ec0)~=0 or p:read_u16(0x010602f0)<=0 then return end
 own_wins=own_wins+1
 log('ENDING_DISPLAY_WIN',string.format('entry=%08X value=%04X mask=%04X pc=%08X identity=%d winner=%d',at,data,mask,cpu.PC.value,identity,side))
end)
taps[#taps+1]=p:install_write_tap(0x01060ec0,0x01060ecf,'actual own final-stage final collision KO',function(at,data,mask)
 if ending_ko or at~=0x01060ec0 or data~=0 or mask~=0xffff or p:read_u16(at)<=0 or
  cpu.PC.value~=0xff836700 or not seen_live or own_wins~=1 or p:read_u16(0x01061b30)~=16 or
  p:read_u16(0x01060280)~=identity or p:read_u16(0x010602f0)<=0 then return end
 ending_ko=frame
 log('ENDING_DISPLAY_KO',string.format('at=%08X before=%d after=%d mask=%04X pc=%08X a8=%08X a13=%08X identity=%d',at,p:read_u16(at),data,mask,cpu.PC.value,cpu.A8.value,cpu.A13.value,identity))
end)
emu.register_frame(function()
 local mode=p:read_u16(0x010601d0);local roster=p:read_u16(0x01060280)
 if mode==4 then own_wins=0 end
 if p:read_u16(0x010601f0)==1 and roster==identity and valid(p:read_u32(0x01060220)) and
  p:read_u16(0x010602f0)>0 then seen_live=true end
 if not command and ending_ko and seen_live and own_wins==1 and mode==11 and
  p:read_u16(0x01061b30)==16 and p:read_u16(0x01061b00)==side and roster==identity and
  p:read_u16(0x01060ec0)==0 and p:read_u16(0x010602f0)>0 and
  p:read_u32(0x01060df0)==0 and p:read_u32(0x01060220)==0 then
  command=frame;origin=frame;ensure_base()
  log('ENDING_DISPLAY_BEGIN',string.format('origin=%d identity=%d winner=%d final_ko=%d own_boss_winner_reads=%d',origin,identity,side,ending_ko,own_wins))
 end
 if command and not ending_completed and frame-command>1200 and mode==11 and roster~=identity then
  ending_completed=frame
  log('ENDING_DISPLAY_ATTRACT',string.format('origin=%d age=%d mode=%d roster1=%d roster2=%d',origin,frame-origin,mode,roster,p:read_u16(0x01060e50)))
 end
end)
]])
once('tag,frame,1,identity==17','tag,frame,side,identity==17')
assert(not source:find('io.open',1,true) and not source:find('screen:snapshot',1,true))
assert(load(source,'@entire2062_native_ending_window_RAM_transport_no_actor_classifier_4518','t',_ENV))()
