-- Current-build stock freeze/lightning regressions. Native controls only.
dofile('mk2ks_blue_palette_test.lua')
local side=assert(tonumber(os.getenv('MK2KS_BLUE_SIDE')))
local victim=assert(os.getenv('MK2KS_BLUE_VICTIM'))
local effect=assert(os.getenv('MK2KS_BLUE_EFFECT'))
local id=assert(({kano=17,sonya=18,cage=2})[victim])
local attack_id=effect=='freeze' and 8 or 7
local p=manager.machine.devices[':maincpu'].spaces.program
local cpu=manager.machine.devices[':maincpu'].state
local slots={{actor=0x01060220,main=0x01060260,roster=0x01060280,state=0x010601f0,hp=0x010602f0},
             {actor=0x01060df0,main=0x01060e30,roster=0x01060e50,state=0x01060dc0,hp=0x01060ec0}}
local fields={}
for _,port in ipairs({':IN0',':IN2'}) do
    for name,field in pairs(manager.machine.ioport.ports[port].fields) do fields[name]=field end
end
local frame,start,actor,main,attacker,attack_main=0,nil,nil,nil,nil,nil
local taps={}
local function valid(a)return a>=0x01000000 and a<0x01100000 end
local function log(tag,text)
    print(string.format('MK2_STOCK_REACTION_%s frame=%d side=%d effect=%s victim=%s %s writes=0 assistance=none',tag,frame,side,effect,victim,text))
end
emu.register_frame(function()
    frame=frame+1
    local own,other=slots[side],slots[3-side]
    if not start then
        local a,m,b,n=p:read_u32(own.actor),p:read_u32(own.main),p:read_u32(other.actor),p:read_u32(other.main)
        if frame>1200 and p:read_u16(0x010601d0)==2 and valid(a) and valid(m) and valid(b) and valid(n) and
            p:read_u16(a+0x1f0)==id and p:read_u16(b+0x1f0)==attack_id then
            start,actor,main,attacker,attack_main=frame,a,m,b,n
            log('MATCH',string.format('actor=%08X main=%08X attacker=%08X attack_main=%08X id=%d attack_id=%d hp1=%d hp2=%d',a,m,b,n,id,attack_id,p:read_u16(slots[1].hp),p:read_u16(slots[2].hp)))
            taps[#taps+1]=p:install_write_tap(own.hp,own.hp+15,'stock projectile health ledger',function(at,data,mask)
                if mask==0xffff and frame-start<=1300 then
                    log('DAMAGE',string.format('actor=%08X main=%08X address=%08X old=%d new=%d pc=%08X a8=%08X a13=%08X',actor,main,at,p:read_u16(at),data&0xffff,cpu.PC.value,cpu.A8.value,cpu.A13.value))
                end
            end)
            taps[#taps+1]=p:install_read_tap(0xff861350,0xff86135f,'stock victim actual ready',function()
                if cpu.PC.value==0xff861360 and cpu.A8.value==actor and cpu.A13.value==main then
                    log('READY',string.format('actor=%08X main=%08X pc=%08X action=%04X',actor,main,cpu.PC.value,p:read_u16(main+0x1f0)))
                end
            end)
        elseif frame>=3000 then log('ERROR','reason=no_actual_selected_match');manager.machine:exit() end
    end
    if not start then return end
    local age=frame-start
    if age>1300 then return end
    local command=nil
    if age>=1140 and age<1156 then command=p:read_i16(actor+0x90)<p:read_i16(attacker+0x90) and 'Right' or 'Left'
    elseif age>=1180 and age<1183 then command='Up'
    elseif age>=1260 and age<1264 then command='High Punch' end
    if command then fields['P'..side..' '..command]:set_value(1);log('INPUT',string.format('age=%d buttons=%s',age,command:gsub(' ','_'))) end
    local bank=p:read_u16(actor+0x140)&0x7f00
    local colors={};for index=0,63 do colors[#colors+1]=string.format('%04X',p:read_u16(0x01800000+(bank+index)*16)&0x7fff)end
    log('FIELD',string.format('age=%d actor=%08X main=%08X published=%08X published_main=%08X attacker=%08X attack_main=%08X mode=%d own_state=%d own_roster=%d id=%d attack_state=%d attack_roster=%d attack_id=%d action=%04X pose=%08X floor=%d x=%d y=%d vx=%08X vy=%08X trail=%08X body=%04X hp=%d attack_hp=%d bank=%04X colors=%s',
        age,actor,main,p:read_u32(own.actor),p:read_u32(own.main),p:read_u32(other.actor),p:read_u32(other.main),p:read_u16(0x010601d0),p:read_u16(own.state),p:read_u16(own.roster),p:read_u16(actor+0x1f0),p:read_u16(other.state),p:read_u16(other.roster),p:read_u16(attacker+0x1f0),p:read_u16(main+0x1f0),p:read_u32(actor+0x1d0),p:read_i16(main+0x200),p:read_i16(actor+0x90),p:read_i16(actor+0xb0),p:read_u32(actor+0x40),p:read_u32(actor+0x60),p:read_u32(main+0x190),p:read_u16(actor+0x160),p:read_u16(own.hp),p:read_u16(other.hp),bank,table.concat(colors,',')))
    if age==1130 or age==1200 or age==1290 then manager.machine.screens[':screen']:snapshot(string.format('stock_reaction_age_%d.png',age))end
    if age==1300 then manager.machine:exit()end
end)
emu.register_stop(function()
    log('RESULT',string.format('match=%d fields=%d scope=input_only_stock_freeze_lightning_and_followup_not_all_stock_projectiles_pixels_or_full_goal',start or -1,start and math.min(frame-start+1,1301) or 0))
    for _,tap in ipairs(taps)do tap:remove()end
end)
