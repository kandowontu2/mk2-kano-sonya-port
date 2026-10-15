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
    high['P1 Left'],high['P1 Right'],high['P1 Up'],high['P1 Down'],high['P1 Block'],high['P1 High Kick'],manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']}
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
    if age>=1800 then print('MK2_BOUNDED_STOP reason=field_limit');manager.machine:exit();return end
    local a,b=bounded_actor(1),bounded_actor(2)
    if not a or not b then return end
    bounded_fields=bounded_fields+1
    local press='none'
    local ordinary=selection_p:read_u16(0x010601d0)==2 and
        selection_p:read_u16(0x010601f0)==1 and selection_p:read_u16(0x01060dc0)==0 and
        a.id==17 and a.hp>0 and b.hp>0 and a.y==a.floor and a.vy==0 and a.gravity==0 and
        (a.flags&0x1c)==0 and (a.body&0xc)==0 and (a.action==0 or a.action==0x0303)
    if ordinary then
        if ((b.action==0x0207 or b.action==0x0204 or b.action==0x0304) and math.abs(a.x-b.x)<80 and age%8<2) or (math.abs(a.x-b.x)<110 and age%24<4) then
            if b.action==0x0207 or b.action==0x0204 or b.action==0x0304 then
                high['P1 High Kick']:set_value(1);press='highkick'
            else manager.machine.ioport.ports[':IN2'].fields['P1 Low Kick']:set_value(1);press='lowkick' end
            bounded_presses=bounded_presses+1
        elseif math.abs(a.x-b.x)>50 then
            press=a.x<b.x and 'Right' or 'Left';high['P1 '..press]:set_value(1)
        end
    end
    print(string.format('MK2_BOUNDED_PHYSICAL frame=%d in0=%04X in2=%04X flags=%04X body=%04X press=%s writes=0',
        selection_frame,manager.machine.ioport.ports[':IN0']:read(),manager.machine.ioport.ports[':IN2']:read(),a.flags,a.body,press))
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

local counter_health_taps={}
for slot,address in ipairs({0x010602f0,0x01060ec0}) do
    counter_health_taps[slot]=selection_p:install_write_tap(address,address+15,
        'bounded native health provenance '..slot,function(at,data,mask)
        print(string.format('MK2_BOUNDED_HEALTH_WRITE frame=%d seconds=%.12f slot=%d address=%08X before=%d data=%04X mask=%04X pc=%08X writes=0',
            selection_frame,emu.time(),slot,at,selection_p:read_u16(address),data&0xffff,mask&0xffff,
            manager.machine.devices[':maincpu'].state.PC.value))
    end)
end
emu.register_stop(function()
    assert(#counter_health_taps==2,'Both actual health taps retained')
    print('MK2_BOUNDED_HEALTH_TAPS_TERMINAL retained=2 writes=0')
end)

local voice_channels={}
local function bind_voice_channels()
    for name,index in pairs(manager.machine.devices[':mk2ksvoices'].items) do
        local channel,field=name:match('^(%x+)/chan%.(.+)$')
        if channel then
            channel=tonumber(channel,16)
            if channel>=10 and channel<=13 then
                voice_channels[channel]=voice_channels[channel] or {}
                assert(not voice_channels[channel][field],'Unique channel field')
                voice_channels[channel][field]=emu.item(index)
            end
        end
    end
    for channel=10,13 do
        local c=assert(voice_channels[channel])
        for _,field in ipairs({'source_num','source_len','pos','loop','paused'}) do
            assert(c[field],'Actual saved channel field '..field)
        end
    end
end
local function observe_voice_channels(phase)
    if selection_frame<2500 or selection_frame>2700 then return end
    for channel=10,13 do
        local c=voice_channels[channel]
        local pos=string.unpack('<d',c.pos:read_block(0,8))
        print(string.format('MK2_BOUNDED_CHANNEL frame=%d seconds=%.12f phase=%s channel=%d sample=%d length=%d pos=%.8f loop=%d paused=%d writes=0',
            selection_frame,emu.time(),phase,channel,c.source_num:read(0),c.source_len:read(0),pos,c.loop:read(0),c.paused:read(0)))
    end
end
emu.register_frame(function()
    if selection_frame==1 then bind_voice_channels() end
    observe_voice_channels('frame')
end)
emu.register_sound_update(function()observe_voice_channels('sound')end)
emu.register_stop(function()
    assert(voice_channels[10] and voice_channels[13],'Channel observers completed')
    print('MK2_BOUNDED_CHANNEL_TERMINAL channels=4 writes=0 raw_media=none')
end)
-- Constant-memory SHA-256 for transient sound-update strings; no files/media.
local pcm_sha_k={
0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2}
local function pcm_ror(x,n)return ((x>>n)|(x<<(32-n)))&0xffffffff end
local function pcm_sha256(raw)
 local size=#raw
 local padded=raw..'\128'..string.rep('\0',(55-size)%64)..string.pack('>I8',size*8)
 local h={0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19}
 for offset=1,#padded,64 do
  local w={}
  for i=1,16 do w[i]=string.unpack('>I4',padded,offset+(i-1)*4)end
  for i=17,64 do
   local a,b=w[i-15],w[i-2]
   local s0=pcm_ror(a,7)~pcm_ror(a,18)~(a>>3)
   local s1=pcm_ror(b,17)~pcm_ror(b,19)~(b>>10)
   w[i]=(w[i-16]+s0+w[i-7]+s1)&0xffffffff
  end
  local a,b,c,d,e,f,g,j=table.unpack(h)
  for i=1,64 do
   local s1=pcm_ror(e,6)~pcm_ror(e,11)~pcm_ror(e,25)
   local ch=(e&f)~((~e)&g)
   local t1=(j+s1+ch+pcm_sha_k[i]+w[i])&0xffffffff
   local s0=pcm_ror(a,2)~pcm_ror(a,13)~pcm_ror(a,22)
   local maj=(a&b)~(a&c)~(b&c)
   local t2=(s0+maj)&0xffffffff
   j,g,f,e,d,c,b,a=g,f,e,(d+t1)&0xffffffff,c,b,a,(t1+t2)&0xffffffff
  end
  local v={a,b,c,d,e,f,g,j}
  for i=1,8 do h[i]=(h[i]+v[i])&0xffffffff end
 end
 local hex={};for i=1,8 do hex[i]=string.format('%08X',h[i])end
 return table.concat(hex)
end
assert(pcm_sha256('')=='E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855')
assert(pcm_sha256('abc')=='BA7816BF8F01CFEA414140DE5DAE2223B00361A396177A9CB410FF61F20015AD')
assert(pcm_sha256(string.rep('a',1000000))=='CDC76E5C9914FB9281A1C7E284D73E67F1809A48A497200E046D39CCC7112CD0')

local hit_pcm_count=0
emu.register_sound_update(function()
 if selection_frame<2500 or selection_frame>2700 then return end
 local raw=manager.machine.sound:get_samples();assert(#raw>0 and #raw%4==0)
 local energy,peak=0,0
 for offset=1,#raw,2 do
  local value=string.unpack('<i2',raw,offset)
  energy=energy+value*value;peak=math.max(peak,math.abs(value))
 end
 hit_pcm_count=hit_pcm_count+1
 print(string.format('MK2_HIT_PCM frame=%d seconds=%.12f bytes=%d sha256=%s energy=%d peak=%d writes=0 raw_media=none',selection_frame,emu.time(),#raw,pcm_sha256(raw),energy,peak))
end)
emu.register_stop(function()print(string.format('MK2_HIT_PCM_STOP updates=%d writes=0 raw_media=none',hit_pcm_count))end)
