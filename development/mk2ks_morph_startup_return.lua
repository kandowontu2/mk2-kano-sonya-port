-- Original real Shang selection/morph/return route plus a late native special.
-- No guest, health, actor, timer or sound writes; capture full screens in RAM.
local function read(name)
 local f=assert(io.open(name,'rb'));local s=f:read('a'):gsub('\r\n','\n');f:close();return s
end
local function change(s,before,after)
 local a,b=assert(s:find(before,1,true));assert(not s:find(before,b+1,true));return s:sub(1,a-1)..after..s:sub(b+1)
end
local side=assert(tonumber(os.getenv('MK2PORT_ACCEPT_SIDE')))
local move=assert(os.getenv('MK2PORT_ACCEPT_MOVE'));assert(move=='ball'or move=='square')
local source=read('mk2ks_morph_adversity_v3215.lua')
source=change(source,"local file=assert(io.open(output..'/guest_maincpu.bin','wb'));file:write(raw);file:close()","print('MK2_HPHASE_GUEST frame=1 bytes=1048576 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))")
source=change(source,'match,actor,main=frame,a,m','match,actor,main=frame,a,m;rawset(_G,\'MK2PORT_NATIVE_AUDIO_READY\',frame)')
source=change(source,'            if attack_due then','            if false and attack_due then')
source=change(source,'        if #command>0 then log(\'INPUT\'',[[        if form_frame and mode==2 and p:read_u16(own+0x1f0)==identity then
            local n=frame-form_frame
            if target=='kano'and n>=400 and n<484 then press('Low Kick')end
            if target=='sonya'then
                if n>=484 and n<487 then press(forward)end
                if n>=489 and n<492 then press(back)end
                if n>=490 and n<493 then press('High Punch')end
            end
        end
        if #command>0 then log('INPUT']])
source=change(source,'if age==2400 then manager.machine:exit() end','if age==2400 then rawset(_G,\'MK2PORT_NATIVE_AUDIO_FINAL\',frame);manager.machine:exit() end')
local snapshot="manager.machine.screens[':screen']:snapshot("
local count=0
while source:find(snapshot,1,true)do
 local a,b=source:find(snapshot,1,true);source=source:sub(1,a-1)..'screen_ram('..source:sub(b+1);count=count+1
end
assert(count==2 and not source:find('guest_maincpu.bin',1,true))
local prefix=[[local function screen_ram(label)
 local raw,w,h=manager.machine.screens[':screen']:pixels();assert(w==400 and h==254 and #raw==406400)
 print(string.format('MK2_HPHASE_RGB frame=%s move=]]..move..[[ side=]]..side..[[ stage=%s width=400 height=254 bytes=%d hex=%s',label:match('(%d+)%.png$'),label,#raw,raw:gsub('.',function(c)return string.format('%02X',c:byte())end)))
end
]]
assert(load(prefix..source,'@whole_native_morph_route_late_startup_return','t',_G))()

-- Whole original passive battle owner/channel/health/mixed PCM/DAC/ROM capture.
local passive=read('mk2ks_launch_interrupt_v6680.lua')
local at=assert(passive:find("local cpu=manager.machine.devices[':maincpu'];local p,regs=cpu.spaces.program,cpu.state",1,true))
passive=passive:sub(at)
passive=change(passive,' if entry then\n  local age=frame-entry',' if false and entry then\n  local age=frame-entry')
passive=change(passive,"local id=assert(({ball=17,square=18,bicycle=18})[os.getenv('MK2PORT_ACCEPT_MOVE')])",'local id=6')
local functions=read('mk2ks_launch_interrupt_v6680.lua')
local first=assert(functions:find('local function read(name)',1,true));local last=assert(functions:find('local getenv=os.getenv',first,true))
functions=functions:sub(first,last-1)..'\nlocal side='..side..';local move='..string.format('%q',move)..';local identity='..(move=='ball'and 17 or 18)..';local delay=1\n'
assert(load(functions..passive,'@whole_native_audio_morph_startup_return','t',_G))()
local physical=read('mk2ks_launch_ko_round.lua');at=assert(physical:find("local p=manager.machine.devices[':maincpu'].spaces.program",1,true))
assert(load(physical:sub(at),'@whole_continuous_native_morph_startup_fields','t',_G))()
local gfx=manager.machine.memory.regions[':gfxrom'];local dumped=false
emu.register_frame(function()
 if dumped then return end;dumped=true
 local bytes={};for i=0,11943 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa0000+i))end
 for i=0,7031 do bytes[#bytes+1]=string.char(gfx:read_u8(0x1fa4000+i))end
 local raw=table.concat(bytes);print('MK2_HPHASE_GFX frame=1 bytes=18976 hex='..raw:gsub('.',function(c)return string.format('%02X',c:byte())end))
end)
