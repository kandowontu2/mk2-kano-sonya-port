-- Natural P1-human/P2-CPU ladder. Inputs only; CPU choices are never supplied.
for _,name in ipairs({'MK2KS_DIAGNOSTIC_CPU_ID','MK2KS_DIAGNOSTIC_LADDER_INDEX','MK2KS_DIAGNOSTIC_CPU_HEALTH','MK2KS_DIAGNOSTIC_P1_REGEN','MK2KS_DIAGNOSTIC_ALL_STAGES'})do
    assert(not os.getenv(name),'Natural pair probe cannot use '..name)
end
dofile('mk2ks_cpu_ladder_trace.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local fields=manager.machine.ioport.ports[':IN0'].fields
local frame,cycle,complete=0,0,nil
local taps,cycles={},{}
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
             {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local specs={
    [17]={target='kano',action=0xfff91400,intro=0xfff94000,attack=0xfff94800,release=0xfff93800,pulse=0xfff93400,steps=22,damage=32,state=0x111},
    [18]={target='sonya',action=0xfff80800,intro=0xfff83000,attack=0xfff83800,release=0xfff82200,steps=5,damage=35,state=0x110}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(slot)
    local a,m=p:read_u32(slot.actor),p:read_u32(slot.main)
    if not valid(a) or not valid(m)then return end
    return {actor=a,main=m,id=p:read_u16(a+0x1f0),roster=p:read_u16(slot.id),state=p:read_u16(slot.state),owner=p:read_u32(m+0xc0),
        action=p:read_u16(m+0x1f0),pose=p:read_u32(a+0x1d0),list=p:read_u32(a+0x1a0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
        xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),
        flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),facing=p:read_u16(a+0xf0),trail=p:read_u32(m+0x190),hp=p:read_u16(slot.hp)}
end
local function live()
    local own,v=sample(slots[2]),sample(slots[1])
    if p:read_u16(0x010601d0)==2 and own and v and own.state==0 and v.state==1 and own.roster==own.id and v.roster==v.id and specs[own.id] then return own,v end
end
local function same(c,s,v)return c and c.actor==s.actor and c.main==s.main and c.victim==v.actor and c.vmain==v.main end
local function log(tag,text)print(string.format('MK2_CPU_PAIR_%s frame=%d cycle=%d %s writes=0 assistance=none',tag,frame,cycle,text))end
local function state(tag,s,v)
    local function part(a,prefix)
        local text={}
        for _,key in ipairs({'actor','main','owner','pose','list','xraw','yraw','vx','vy','gravity','flags','body','facing','trail'})do text[#text+1]=string.format('%s%s=%08X',prefix,key,a[key])end
        for _,key in ipairs({'id','roster','state','action','x','y','floor','hp'})do
            local suffix=prefix=='v' and (key=='x' or key=='y')and key..'pos' or key
            text[#text+1]=string.format('%s%s=%d',prefix,suffix,a[key])
        end
        return table.concat(text,' ')
    end
    log(tag,part(s,'')..' '..part(v,'v')..string.format(' mode=%d stage=%d schedule=%08X suppression=%d left=%d right=%d',p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(0x01061b10),p:read_u16(0x010619d0),p:read_i16(0x0105ecf0)+0x3a,p:read_i16(0x0105ed00)+0x15f))
end
local function clean(a)
    local vx=a.vx>=0x80000000 and a.vx-0x100000000 or a.vx
    return a.y==a.floor and a.vy==0 and a.gravity==0 and a.flags&0x1c==0 and a.body&0x0c==0 and a.trail==0 and (vx==0 or a.action==0x303 and math.abs(vx)<=0x30000)
end
local entries={step=0xfff89400,damage=0xff837340,fling=0xff876650,velocity=0xff831bd0,recovery=0xff861350}
for id,spec in pairs(specs)do for _,kind in ipairs({'action','intro','attack','release','pulse'})do if spec[kind]then entries[kind..'_'..id]=spec[kind]end end end
for entry_kind,address in pairs(entries)do
    taps[#taps+1]=p:install_read_tap(address,address+15,'actual native CPU pair '..entry_kind,function(at,data)
        local descriptor=entry_kind:match('^intro_')or entry_kind:match('^attack_')
        if at~=address or(not descriptor and cpu.PC.value~=address+16)or(descriptor and cpu.PC.value<0xff800000)then return end
        local s,v=live();if not s then return end
        local kind=entry_kind:match('^(%a+)');local spec=specs[s.id]
        local requested=tonumber(entry_kind:match('_(%d+)$'));if requested and requested~=s.id then return end
        if kind=='action' then
            if cpu.A8.value~=s.actor or cpu.A13.value~=s.main then return end
            cycle=cycle+1;cycles[cycle]={start=frame,actor=s.actor,main=s.main,victim=v.actor,vmain=v.main,id=s.id,steps=0,damage=0,pulses=0}
            state('ENTRY',s,v)
        end
        local c=cycles[cycle];if not same(c,s,v)or c.closed then return end
        if kind=='intro' or kind=='attack' or kind=='step' or kind=='action'then
            if cpu.A8.value~=s.actor or cpu.A13.value~=s.main then return end
            if kind=='step'then
                if s.action~=spec.state or p:read_u32(cpu.A9.value)==0 then return end
                c.steps=c.steps+1;c.paired=c.paired or frame
                manager.machine.screens[':screen']:snapshot(string.format('cpu_pair_%d_step_%d.png',cycle,c.steps))
            end
        elseif kind=='recovery'then
            if cpu.A8.value==s.actor and cpu.A13.value==s.main then kind='own_ready';c.own_ready=c.own_ready or frame
            elseif cpu.A8.value==v.actor and cpu.A13.value==v.main and c.release then kind='victim_ready';c.victim_ready=c.victim_ready or frame
            else return end
        else
            if not c.paired or cpu.A8.value~=v.actor then return end
            if kind=='release'then c.release=frame
            elseif kind=='pulse'then c.pulses=c.pulses+1
            elseif kind=='damage' and s.id==18 and not c.release then return end
        end
        log('EVENT',string.format('kind=%s entry=%08X pc=%08X actor=%08X main=%08X victim=%08X vmain=%08X a8=%08X a13=%08X a0=%08X a1=%08X a2=%08X a3=%08X a9=%08X a10=%08X group=%08X word=%04X steps=%d',kind,address,cpu.PC.value,s.actor,s.main,v.actor,v.main,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value,cpu.A2.value,cpu.A3.value,cpu.A9.value,cpu.A10.value,kind=='step' and p:read_u32(cpu.A9.value)or 0,descriptor and(data&0xffff)or 0,c.steps))
    end)
end
for side,slot in ipairs(slots)do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'CPU pair health ledger',function(at,data,mask)
        if mask~=0xffff then return end
        local s,v=live();if not s then return end
        local c=cycles[cycle];local before,after=p:read_u16(at),data&0xffff
        log('HEALTH',string.format('slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X',side,before,after,cpu.PC.value,cpu.A8.value,cpu.A13.value))
        if side==1 and same(c,s,v)and c.paired and not c.closed then c.damage=c.damage+before-after end
    end)
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then
        for order=0,5 do
            local roster_table=p:read_u32(0xff8a11f0);local list=p:read_u32(roster_table+order*32);local ids={}
            for n=0,16 do ids[#ids+1]=p:read_u16(list+n*16)end
            log('ROM',string.format('table=%08X order=%d list=%08X ids=%s',roster_table,order,list,table.concat(ids,',')))
        end
    end
    local s,v=live();if not s then return end
    state('FIELD',s,v)
    fields['P1 Left']:set_value(0);fields['P1 Right']:set_value(0)
    local c=cycles[cycle]
    if same(c,s,v) and not c.closed and c.own_ready and c.victim_ready and clean(s)and clean(v)then
        c.closed=true
        if c.steps==specs[s.id].steps and c.damage==specs[s.id].damage and c.release and (s.id~=17 or c.pulses==4)then
            state('COMPLETE',s,v);complete=frame
            manager.machine.screens[':screen']:snapshot('cpu_pair_complete.png')
        else state('INCOMPLETE',s,v)end
    end
    if complete then
        fields['P1 Block']:set_value(1)
        if frame>=complete+30 then manager.machine:exit()end
    elseif not c or c.closed or not c.paired then
        if v.hp>0 and s.hp>0 and clean(v) and math.abs(s.x-v.x)>76 then
            fields['P1 '..(v.x<s.x and 'Right' or 'Left')]:set_value(1)
            log('INPUT',string.format('buttons=%s gap=%d',v.x<s.x and 'Right' or 'Left',math.abs(s.x-v.x)))
        end
    end
end)
emu.register_stop(function()
    log('RESULT',string.format('schema=2 cycles=%d complete=%d scope=natural_CPU_paired_trace_not_all_victims_slots_pixels_audio_or_full_goal',cycle,complete or -1))
    for _,tap in ipairs(taps)do tap:remove()end
end)
