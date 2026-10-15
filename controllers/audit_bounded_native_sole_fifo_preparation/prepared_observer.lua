-- Natural cold P1-human/P2-CPU ladder. Inputs only; CPU choices are never supplied.
for _,name in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
    assert(not os.getenv(name),'Natural pair probe cannot use '..name)
end
-- Physical roles remain explicit: every flag/health slot is the real machine slot.
local cpu_slot,human_slot=2,1
local selection_frame,selection_css,selection_exit,selection_checks,selection_errors=0,nil,nil,0,0
local human=assert(os.getenv('MK2KS_TEST_FIGHTER'))
local human_id=assert(({kano=17,sonya=18,liu_kang=1,cage=2,baraka=3,kitana=4,
    kung_lao=0,mileena=5,shang_tsung=6,raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11})[human])
assert(human=='kano' or human=='sonya','This cold native UI route covers the two added humans')
local native_direction=human=='kano'and'Left'or'Right'
local stock_direction=human=='kano'and'Right'or'Left'
local route={}
for i=1,(human=='sonya'and 4 or 1)do route[#route+1]={native_direction,12+(i-1)*12}end
for _,step in ipairs({{stock_direction,72},{native_direction,96},{stock_direction,120},{native_direction,144},
    {'Down',168},{'Up',192},{native_direction,216}})do route[#route+1]=step end
local boot=tonumber(os.getenv('MK2KS_TEST_BOOT_FRAME')or'604')
assert(boot>=600 and boot<=1500)
local confirm_age=tonumber(os.getenv('MK2KS_CPU_PAIR_CONFIRM_AGE')or'264')
assert(confirm_age>=96 and confirm_age<=370,'Only actual selection confirmation timing')
local continuation=os.getenv('MK2KS_CPU_CONTINUATION_POLICY')or'retreat'
assert(continuation=='retreat' or continuation=='jump_guard' or continuation=='guard_hold' or continuation=='neutral_hold' or continuation=='jump_on_launch','Only real human continuation buttons')
local approach=os.getenv('MK2KS_CPU_PAIR_APPROACH')or'original'
assert(approach=='original' or approach=='guard_wait' or approach=='guard_until_close','Only genuine human input strategies')
local selection_p=manager.machine.devices[':maincpu'].spaces.program
local high,system=manager.machine.ioport.ports[':IN0'].fields,manager.machine.ioport.ports[':IN1'].fields
local selection_inputs={system['Coin 1'],system['1 Player Start'],high['P1 High Punch'],
    high['P1 Left'],high['P1 Right'],high['P1 Up'],high['P1 Down'],high['P1 Block']}
local initial_cpu,first_live=nil,nil
emu.register_frame(function()
    selection_frame=selection_frame+1
    for _,field in ipairs(selection_inputs)do field:clear_value()end
    if selection_frame>=300 and selection_frame<304 then high['P1 High Punch']:set_value(1)end
    local pixels,width=manager.machine.screens[':screen']:pixels()
    local yellow,early=0,0
    if width==400 and #pixels>=400*254*4 then
        for y=0,24,2 do for x=40,360,2 do
            local rgb=string.unpack('<I4',pixels,(y*width+x)*4+1)
            local r,g,b=(rgb>>16)&255,(rgb>>8)&255,rgb&255
            if r>175 and g>140 and b<100 then yellow=yellow+1;if y==4 then early=early+1 end end
        end end
    end
    local css=yellow>=400 and yellow<=430 and early>=10
    if not selection_css and selection_frame>=boot then
        local age=(selection_frame-boot)%300
        if age<4 then system['Coin 1']:set_value(1)end
        if age>=20 and age<24 then system['1 Player Start']:set_value(1)end
    end
    if not selection_css and selection_frame>700 and css then
        selection_css=selection_frame
        print(string.format('MK2_P2CPU_SELECT_CSS frame=%d human=%s slot=1 yellow=%d early=%d writes=0 assistance=none',selection_frame,human,yellow,early))
    end
    if selection_css and not selection_exit then
        local age=selection_frame-selection_css
        for _,step in ipairs(route)do
            local direction,at=step[1],step[2]
            if age>=at and age<at+4 then high['P1 '..direction]:set_value(1)end
        end
        if(age>=54 and age<=70)or(age>=228 and age<=260)then
            selection_checks=selection_checks+1
            if selection_p:read_u16(0x01060280)~=human_id then selection_errors=selection_errors+1 end
        end
        if age>=confirm_age and age<confirm_age+8 then high['P1 High Punch']:set_value(1)end
        if age>confirm_age and not css then
            selection_exit=selection_frame
        end
    end
    if selection_frame%120==0 then
        print(string.format('MK2_P2CPU_BOOT_STATE frame=%d mode=%d states=%d,%d roster=%d,%d stage=%d schedule=%08X writes=0 assistance=none',
            selection_frame,selection_p:read_u16(0x010601d0),selection_p:read_u16(0x010601f0),
            selection_p:read_u16(0x01060dc0),selection_p:read_u16(0x01060280),selection_p:read_u16(0x01060e50),
            selection_p:read_u16(0x01061b30),selection_p:read_u32(0x01061b10)))
    end
    if selection_exit and not first_live and selection_p:read_u16(0x010601d0)==2 and
        selection_p:read_u16(0x010601f0)==1 and selection_p:read_u16(0x01060dc0)==0 then
        first_live=selection_frame;initial_cpu=selection_p:read_u16(0x01060e50)
        print(string.format('MK2_P2CPU_COLD_LIVE frame=%d human=%s human_id=%d cpu_id=%d stage=%d schedule=%08X writes=0 assistance=none',
            first_live,human,human_id,initial_cpu,selection_p:read_u16(0x01061b30),selection_p:read_u32(0x01061b10)))
    end
end)
emu.register_stop(function()
    print(string.format('MK2_P2CPU_SELECT_RESULT human=%s human_id=%d css=%d exit=%d live=%d initial_cpu=%d checks=%d errors=%d writes=0 assistance=none',
        human,human_id,selection_css or -1,selection_exit or -1,first_live or -1,initial_cpu or -1,selection_checks,selection_errors))
end)

-- Bounded scalar-only probe. CPU decisions and all guest state remain native.
assert(human=='kano','This distinct policy is the physical Kano uppercut probe')
local bounded_fields,bounded_presses=0,0
local function bounded_actor(slot)
    local ap=slot==1 and 0x01060220 or 0x01060df0
    local mp=slot==1 and 0x01060260 or 0x01060e30
    local a,m=selection_p:read_u32(ap),selection_p:read_u32(mp)
    if a<0x01000000 or a>=0x01100000 or m<0x01000000 or m>=0x01100000 then return nil end
    return {a=a,m=m,id=selection_p:read_u16(a+0x1f0),
        x=selection_p:read_i16(a+0x90),y=selection_p:read_i16(a+0xb0),
        floor=selection_p:read_i16(m+0x200),action=selection_p:read_u16(m+0x1f0),
        vy=selection_p:read_u32(a+0x60),gravity=selection_p:read_u32(a+0x20),
        flags=selection_p:read_u16(m+0x210),body=selection_p:read_u16(a+0x160),
        hp=selection_p:read_u16(slot==1 and 0x010602f0 or 0x01060ec0)}
end
emu.register_frame(function()
    if not first_live then
        if selection_frame>=2400 then print('MK2_BOUNDED_STOP reason=no_live_pair');manager.machine:exit() end
        return
    end
    local age=selection_frame-first_live
    if age>=120 then print('MK2_BOUNDED_STOP reason=field_limit');manager.machine:exit();return end
    local a,b=bounded_actor(1),bounded_actor(2)
    if not a or not b then return end
    bounded_fields=bounded_fields+1
    local press='none'
    local ordinary=selection_p:read_u16(0x010601d0)==2 and
        selection_p:read_u16(0x010601f0)==1 and selection_p:read_u16(0x01060dc0)==0 and
        a.id==17 and a.hp>0 and b.hp>0 and a.y==a.floor and a.vy==0 and a.gravity==0 and
        (a.flags&0x1c)==0 and (a.body&0xc)==0 and (a.action==0 or a.action==0x0303)
    if false and ordinary then
        if math.abs(a.x-b.x)<120 and age%36<4 then
            high['P1 Down']:set_value(1);high['P1 High Punch']:set_value(1)
            bounded_presses=bounded_presses+1;press='down_highpunch'
        elseif math.abs(a.x-b.x)>50 then
            press=a.x<b.x and 'Right' or 'Left';high['P1 '..press]:set_value(1)
        end
    end
    print(string.format('MK2_BOUNDED_FIELD frame=%d mode=%d p1id=%d p2id=%d hp1=%d hp2=%d action1=%04X action2=%04X x1=%d x2=%d y1=%d floor1=%d press=%s writes=0',
        selection_frame,selection_p:read_u16(0x010601d0),a.id,b.id,a.hp,b.hp,a.action,b.action,a.x,b.x,a.y,a.floor,press))
end)
emu.register_stop(function()
    print(string.format('MK2_BOUNDED_RESULT fields=%d presses=%d writes=0 raw_media=none',bounded_fields,bounded_presses))
end)
-- Read actual saved driver arrays through MAME's read-only item interface.
-- No inferred owner lifetime from intended routes or audible sample numbers.
local owner_frame,owner_serial=0,0
local saved={}
local sizes={actor=4,main=4,health=2,id=2,mode=2}
local names={'actor','main','health','id','mode'}
local function bind()
 local device=assert(manager.machine.devices[':'],'Actual root driver')
 for name,index in pairs(device.items)do
  for _,field in ipairs(names)do
   if name:match('/m_mk2ks_battle_'..field..'$')then
    assert(not saved[field],'Unique actual saved battle field')
    local item=emu.item(index)
    assert(item.size==sizes[field] and item.count==2,'Actual two-player saved field layout')
    saved[field]=item
    print(string.format('MK2_VOICE_OWNER_ITEM field=%s name=%s bytes=%d count=%d writes=0 assistance=none',
     field,name,item.size,item.count))
   end
  end
 end
 for _,field in ipairs(names)do assert(saved[field],'Actual saved field '..field)end
end
local function observe(phase)
 if not saved.actor then return end
 owner_serial=owner_serial+1
 for slot=0,1 do
  print(string.format('MK2_VOICE_OWNER frame=%d seconds=%.12f serial=%d phase=%s slot=%d actor=%08X main=%08X health=%d id=%d mode=%d writes=0 assistance=none',
   owner_frame,emu.time(),owner_serial,phase,slot+1,saved.actor:read(slot),saved.main:read(slot),
   saved.health:read(slot),saved.id:read(slot),saved.mode:read(slot)))
 end
end
emu.register_frame(function()
 owner_frame=owner_frame+1
 if owner_frame==1 then bind()end
 observe('frame')
end)
emu.register_sound_update(function()observe('sound')end)
emu.register_stop(function()observe('stop')end)

local bounded_sound_tap=selection_p:install_write_tap(0x01d01030,0x01d0103f,
    'bounded passive private cue observation',function(at,data,mask)
    local word=data&0xffff
    if at==0x01d01030 and mask==0xffff and word>=0x6b00 and word<=0x6b03 then
        print(string.format('MK2_BOUNDED_CUE frame=%d seconds=%.12f word=%04X writes=0',selection_frame,emu.time(),word))
    end
end)

-- A registered closure retains the actual tap userdata beyond chunk return.
emu.register_stop(function()
    assert(bounded_sound_tap,'Actual passive sound tap retained through stop')
    print('MK2_BOUNDED_TAP_TERMINAL retained=1 writes=0')
end)

local sole_gfx=assert(manager.machine.memory.regions[':gfxrom'])
local function opaque_bounds(source,w,h,command)
    assert(w>0 and w<=200 and h>0 and h<=200)
    local mapped=source
    if source>=0x10000000 and source<0x1a000000 then mapped=source-0x0a000000 end
    assert(mapped>=0 and mapped<0x10000000)
    local bit=mapped
    local bpp=(command>>12)&7;if bpp==0 then bpp=8 end
    local function take(n)
        assert(bit+n<=sole_gfx.size*8,'Complete actual source bits')
        local at=bit//8
        local word=sole_gfx:read_u8(at)|(sole_gfx:read_u8(at+1)<<8)
        local value=(word>>(bit%8))&((1<<n)-1)
        bit=bit+n;return value
    end
    local count,low,high=0,nil,nil
    for y=0,h-1 do
        local pre,post=0,0
        if command&0x80~=0 then
            local header=take(8)
            pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
        end
        assert(pre+post<=w,'Valid native compressed row')
        for x=pre,w-post-1 do
            if take(bpp)~=0 then
                local yy=command&0x20~=0 and -y or y
                count=count+1;low=low and math.min(low,yy) or yy;high=high and math.max(high,yy) or yy
            end
        end
    end
    return count,low or -999,high or -999,bit-mapped
end
emu.register_frame_done(function()
    if not first_live then return end
    local age=selection_frame-first_live
    if age~=8 and age~=16 and age~=24 and age~=32 and age~=80 and age~=96 and age~=112 then return end
    for slot=1,2 do
        local s=assert(bounded_actor(slot))
        local cache=selection_p:read_u32(s.a+0x1a0)
        assert(cache>=0x01000000 and cache<0x01100000)
        local count=0
        for part=0,11 do
            local row=cache+part*112;local source=selection_p:read_u32(row)
            if source==0 then break end
            count=count+1
            local w,h,c=selection_p:read_u16(row+0x20),selection_p:read_u16(row+0x30),selection_p:read_u16(row+0x40)
            local opaque,top,bottom,bits=opaque_bounds(source,w,h,c)
            print(string.format('MK2_BOUNDED_STANCE_PART frame=%d age=%d slot=%d id=%d actor=%08X main=%08X pose=%08X cache=%08X part=%d source=%08X width=%d height=%d command=%04X dx=%d dy=%d opaque=%d top=%d bottom=%d bits=%d y=%d floor=%d action=%04X hp=%d stage_floor=%d writes=0',
                selection_frame,age,slot,s.id,s.a,s.m,selection_p:read_u32(s.a+0x1d0),cache,part,source,w,h,c,
                selection_p:read_i16(row+0x50),selection_p:read_i16(row+0x60),opaque,top,bottom,bits,
                s.y,s.floor,s.action,s.hp,selection_p:read_i16(0x0105ecd0)))
        end
        assert(count>0 and count<12,'Complete terminated actual component list')
    end
end)

local sole_dma_count=0
local sole_dma_tap=selection_p:install_write_tap(0x01a80010,0x01a8001f,
    'bounded actual opaque body DMA',function(at,data,mask)
    if not first_live or at~=0x01a80010 then return end
    local age=selection_frame-first_live
    if age~=8 and age~=16 and age~=24 and age~=32 and age~=80 and age~=96 and age~=112 then return end
    local command=data&0xffff
    if command&15~=2 then return end
    local function reg(n)return selection_p:read_u16(0x01a80000+n*16)end
    local palette=reg(8)&0x7f00;local slot=palette==0x200 and 1 or (palette==0x300 and 2 or nil)
    if not slot then return end
    local s=assert(bounded_actor(slot));local cache=selection_p:read_u32(s.a+0x1a0)
    local source=reg(2)|(reg(3)<<16);local w,h=reg(6)&0x3ff,reg(7)&0x3ff
    local part=nil
    for index=0,11 do
        local row=cache+index*112;local graphic=selection_p:read_u32(row)
        if graphic==0 then break end
        if graphic==source and selection_p:read_u16(row+0x20)==w and selection_p:read_u16(row+0x30)==h then part=index;break end
    end

    if not part then
        local source_part,cw,ch=-1,0,0
        for index=0,11 do
            local row=cache+index*112;local graphic=selection_p:read_u32(row)
            if graphic==0 then break end
            if graphic==source then source_part=index;cw=selection_p:read_u16(row+0x20);ch=selection_p:read_u16(row+0x30);break end
        end
        print(string.format('MK2_BOUNDED_SOLE_UNMATCHED frame=%d age=%d slot=%d id=%d source=%08X width=%d height=%d command=%04X x=%d y=%d cache_source_part=%d cache_width=%d cache_height=%d pc=%08X writes=0',
            selection_frame,age,slot,s.id,source,w,h,command,reg(4)&0x3ff,reg(5)&0x1ff,source_part,cw,ch,
            manager.machine.devices[':maincpu'].state.PC.value))
        return
    end
    local opaque,top,bottom,bits=opaque_bounds(source,w,h,command)
    sole_dma_count=sole_dma_count+1
    print(string.format('MK2_BOUNDED_SOLE_DMA frame=%d age=%d slot=%d id=%d part=%d source=%08X command=%04X palette=%04X width=%d height=%d x=%d y=%d opaque=%d top=%d bottom=%d opaque_bottom_y=%d stage_floor=%d actor_y=%d floor=%d action=%04X pc=%08X writes=0',
        selection_frame,age,slot,s.id,part,source,command,palette,w,h,reg(4)&0x3ff,reg(5)&0x1ff,opaque,top,bottom,
        ((reg(5)&0x1ff)+bottom)&0x1ff,selection_p:read_i16(0x0105ecd0),s.y,s.floor,s.action,
        manager.machine.devices[':maincpu'].state.PC.value))
end)
emu.register_stop(function()
    assert(sole_dma_tap,'Native body DMA tap retained')
    print(string.format('MK2_BOUNDED_SOLE_DMA_TERMINAL copies=%d writes=0',sole_dma_count))
end)

local sole_queue_count=0
local sole_queue_tap=selection_p:install_read_tap(0xff804410,0xff80441f,
    'actual sparse physical body FIFO',function(at)
    local regs=manager.machine.devices[':maincpu'].state
    if not first_live or at~=0xff804410 or regs.PC.value~=0xff804420 then return end
    local age=selection_frame-first_live
    if age~=8 and age~=16 and age~=24 and age~=32 and age~=80 and age~=96 and age~=112 then return end
    for slot=1,2 do
        local s=bounded_actor(slot)
        if s and s.a==regs.A0.value then
            local cache=selection_p:read_u32(s.a+0x1a0);local row=regs.A3.value-112
            assert(row>=cache and row<cache+12*112 and (row-cache)%112==0)
            sole_queue_count=sole_queue_count+1
            print(string.format('MK2_BOUNDED_SOLE_FIFO frame=%d seconds=%.12f slot=%d id=%d actor=%08X main=%08X pose=%08X part=%d source=%08X size=%08X xy=%08X command=%08X palette=%08X pc=%08X writes=0',
                selection_frame,emu.time(),slot,s.id,s.a,s.m,selection_p:read_u32(s.a+0x1d0),(row-cache)//112,
                regs.A11.value,regs.A9.value,regs.A10.value,regs.A12.value,regs.A6.value,regs.PC.value))
        end
    end
end)
emu.register_stop(function()
    assert(sole_queue_tap,'Actual FIFO tap retained')
    print(string.format('MK2_BOUNDED_SOLE_FIFO_TERMINAL entries=%d writes=0',sole_queue_count))
end)
