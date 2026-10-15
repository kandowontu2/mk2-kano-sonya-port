-- Natural CPU knife/ring selection, owned child life and actual native cleanup.
local selection=dofile('mk2ks_cold_p2_selection.lua')
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local high=manager.machine.ioport.ports[':IN0'].fields
local frame,serial,complete=0,0,nil
local taps,entries,children,bound={}, {}, {}, {}
local slots={{actor=0x01060220,main=0x01060260,id=0x01060280,state=0x010601f0,hp=0x010602f0},
    {actor=0x01060df0,main=0x01060e30,id=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function sample(slot)
    local a,m=p:read_u32(slot.actor),p:read_u32(slot.main);if not valid(a)or not valid(m)then return end
    return {actor=a,main=m,owner=p:read_u32(m+0xc0),id=p:read_u16(a+0x1f0),roster=p:read_u16(slot.id),state=p:read_u16(slot.state),hp=p:read_u16(slot.hp),
        action=p:read_u16(m+0x1f0),pose=p:read_u32(a+0x1d0),list=p:read_u32(a+0x1a0),xraw=p:read_u32(a+0x80),yraw=p:read_u32(a+0xa0),x=p:read_i16(a+0x90),y=p:read_i16(a+0xb0),floor=p:read_i16(m+0x200),
        vx=p:read_u32(a+0x40),vy=p:read_u32(a+0x60),gravity=p:read_u32(a+0x20),flags=p:read_u16(m+0x210),body=p:read_u16(a+0x160),trail=p:read_u32(m+0x190)}
end
local function live()
    local a,v=sample(slots[1]),sample(slots[2])
    if selection.first_live()and p:read_u16(0x010601d0)==2 and a and v and a.state==0 and v.state==1 and a.id==a.roster and v.id==v.roster and(a.id==17 or a.id==18)then return a,v end
end
local function log(tag,s)print(string.format('MK2_CPU_SHOT_%s frame=%d serial=%d %s cpu_slot=1 human_slot=2 writes=0 assistance=none',tag,frame,serial,s))end
local function part(a,prefix)
    local t={}
    for _,k in ipairs({'actor','main','owner','pose','list','xraw','yraw','vx','vy','gravity','flags','body','trail'})do t[#t+1]=string.format('%s%s=%08X',prefix,k,a[k])end
    for _,k in ipairs({'id','roster','state','hp','action','x','y','floor'})do t[#t+1]=string.format('%s%s=%d',prefix,k,a[k])end
    return table.concat(t,' ')
end
local function pair(tag,a,v,extra)
    log(tag,part(a,'')..' '..part(v,'v')..string.format(' mode=%d stage=%d schedule=%08X ',p:read_u16(0x010601d0),p:read_u16(0x01061b30),p:read_u32(0x01061b10))..(extra or''))
end
local function bind(a,side)
    for _,kind in ipairs({'action','flags','body'})do
        local at=kind=='body'and a.actor+0x160 or kind=='flags'and a.main+0x210 or a.main+0x1f0
        if not bound[at]then
            bound[at]=true
            taps[#taps+1]=p:install_write_tap(at,at+15,'actual shot state/lock store',function(offset,data,mask)
                local current=sample(slots[side]);if offset~=at or mask~=0xffff or not current or current.actor~=a.actor or current.main~=a.main or p:read_u16(0x010601d0)~=2 then return end
                log('STORE',string.format('slot=%d kind=%s at=%08X before=%04X after=%04X pc=%08X a8=%08X a13=%08X ',side,kind,at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value)..part(current,''))
            end)
        end
    end
end
for _,address in ipairs({0xffffb000,0xffffb400,0xfffc3800,0xfffc4800,0xff8a5900,0xfffbc000,0xfffbc200,0xff8a5c20,0xff861350,0xff861500,0xff83ed80})do
    taps[#taps+1]=p:install_read_tap(address,address+15,'actual shot body/AI flow',function(at)
        if at~=address or cpu.PC.value~=address+16 then return end
        local a,v=live();if not a or cpu.A8.value~=a.actor or cpu.A13.value~=a.main then return end
        if address==0xffffb000 or address==0xffffb400 then
            serial=serial+1;entries[serial]={start=frame,actor=a.actor,main=a.main,id=a.id}
            pair('ENTRY',a,v,string.format('entry=%08X pc=%08X',address,cpu.PC.value))
        end
        pair('FLOW',a,v,string.format('entry=%08X pc=%08X a8=%08X a13=%08X a0=%08X a1=%08X',address,cpu.PC.value,cpu.A8.value,cpu.A13.value,cpu.A0.value,cpu.A1.value))
        local e=entries[serial]
        if e and e.actor==a.actor and e.main==a.main and address==0xff861500 and not e.ready then
            e.ready=frame;pair('HANDOFF',a,v,string.format('entry=%08X pc=%08X',address,cpu.PC.value))
        end
    end)
end
for _,address in ipairs({0xfffc6000,0xfffc7000})do
    taps[#taps+1]=p:install_read_tap(address,address+15,'actual owned shot child',function(at)
        if at~=address or cpu.PC.value~=address+16 then return end
        local a,v=live();local obj,m=cpu.A8.value,cpu.A13.value
        if not a or not valid(obj)or not valid(m)or p:read_u32(m+0x230)~=a.actor then return end
        local e=entries[serial];if not e or e.actor~=a.actor then return end
        children[obj]={main=m,serial=serial,owner=a.actor};e.child=obj;e.childmain=m
        log('CHILD',string.format('entry=%08X pc=%08X actor=%08X main=%08X owner=%08X id=%d',address,cpu.PC.value,obj,m,p:read_u32(m+0x230),p:read_u16(obj+0x1f0)))
    end)
end
taps[#taps+1]=p:install_read_tap(0xff838790,0xff83879f,'actual shot group renderer',function(at)
    if at~=0xff838790 or cpu.PC.value~=0xff8387a0 then return end
    local a,v=live();if not a then return end
    local obj,m=cpu.A8.value,cpu.A13.value;local child=children[obj]
    if(obj~=a.actor or m~=a.main)and(not child or child.main~=m)then return end
    log('GROUP',string.format('actor=%08X main=%08X id=%d child=%d group=%08X pc=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X',obj,m,p:read_u16(obj+0x1f0),child and 1 or 0,cpu.A0.value,cpu.PC.value,p:read_u32(obj+0x80),p:read_u32(obj+0xa0),p:read_u32(obj+0x40),p:read_u32(obj+0x60)))
end)
taps[#taps+1]=p:install_read_tap(0xff8b6820,0xff8b682f,'actual shot native retirement',function(at)
    if at~=0xff8b6820 or cpu.PC.value~=0xff8b6830 then return end
    local obj,m=cpu.A8.value,cpu.A13.value;local c=children[obj]
    if c and c.main==m then
        log('RETIRE',string.format('actor=%08X main=%08X owner=%08X child_serial=%d pc=%08X',obj,m,c.owner,c.serial,cpu.PC.value))
        entries[c.serial].retired=frame;children[obj]=nil
    end
end)
for side,slot in ipairs(slots)do
    taps[#taps+1]=p:install_write_tap(slot.hp,slot.hp+15,'actual shot native health',function(at,data,mask)
        local a,v=live();if not a or mask~=0xffff then return end
        log('HEALTH',string.format('slot=%d before=%d after=%d pc=%08X a8=%08X a13=%08X',side,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
    end)
end
emu.register_frame(function()
    frame=selection.frame()
    if frame==1 then
        for _,range in ipairs({{0xffffb000,0xffffb450},{0xfffc3800,0xfffc6000},{0xfffbc000,0xfffbc400}})do
            local words={};for at=range[1],range[2]-16,16 do words[#words+1]=string.format('%04X',p:read_u16(at))end
            log('CODE',string.format('start=%08X stop=%08X words=%s',range[1],range[2],table.concat(words,',')))
        end
    end
    local a,v=live()
    if a then
        bind(a,1);bind(v,2);pair('FIELD',a,v)
        for obj,c in pairs(children)do
            local m=c.main
            log('EFFECT',string.format('actor=%08X main=%08X owner=%08X child_serial=%d id=%d type=%d action=%d pose=%08X list=%08X xraw=%08X yraw=%08X vx=%08X vy=%08X velocity_parameter=%08X',obj,m,p:read_u32(m+0x230),c.serial,p:read_u16(obj+0x1f0),p:read_u16(obj+0xc0),p:read_u16(m+0x1f0),p:read_u32(obj+0x1d0),p:read_u32(obj+0x1a0),p:read_u32(obj+0x80),p:read_u32(obj+0xa0),p:read_u32(obj+0x40),p:read_u32(obj+0x60),p:read_u32(m+0x250)))
        end
        if not complete then
            for n,e in ipairs(entries)do
                if e.ready and e.retired then complete=frame;pair('COMPLETE',a,v,string.format('completed_serial=%d start=%d ready=%d retired=%d',n,e.start,e.ready,e.retired));manager.machine.screens[':screen']:snapshot('cpu_shot_complete.png');break end
            end
        end
        -- Only real human input controls spacing and guarding. CPU decisions,
        -- timers, positions, health, actor IDs and action states are untouched.
        local age=frame-selection.first_live();local gap=math.abs(a.x-v.x)
        local clean=v.y==v.floor and v.vy==0 and v.gravity==0 and v.flags&0x1c==0 and v.body&0x0c==0
        if not complete and(age<85 or gap<180 and clean and a.flags&0x1c==0)then
            high['P2 '..(v.x<a.x and'Left'or'Right')]:set_value(1)
            log('INPUT',string.format('buttons=%s gap=%d',v.x<a.x and'Left'or'Right',gap))
        else high['P2 Block']:set_value(1);log('INPUT',string.format('buttons=Block gap=%d',gap))end
        local e=entries[serial];if e and(frame==e.start+8 or frame==e.start+25 or frame==e.start+50)then manager.machine.screens[':screen']:snapshot('cpu_shot_'..serial..'_'..(frame-e.start)..'.png')end
    end
    if complete and frame>=complete+30 or selection.first_live()and frame>=selection.first_live()+2000 then manager.machine:exit()end
end)
emu.register_stop(function()
    local count=0;for _ in pairs(children)do count=count+1 end
    log('RESULT',string.format('schema=1 entries=%d complete=%d live_children=%d scope=natural_CPU_projectile_diagnostic_not_full_goal',serial,complete or-1,count))
    for _,tap in ipairs(taps)do tap:remove()end
end)
