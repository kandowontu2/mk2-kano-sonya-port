-- Audit naturally earned fatalities in either physical slot; inputs only.
dofile("mk2ks_finish_range_test.lua")
local side=tonumber(os.getenv('MK2_TRACE_NATIVE_FINISH_SIDE'))
assert(side==1 or side==2)
assert(os.getenv("MK2_TRACE_INPUT_ONLY_APPROACH")=="1")
assert(os.getenv("MK2_TRACE_POSITION_ASSIST")~="1")
assert(os.getenv("MK2_TRACE_LADDER")~="1")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local fighter=assert(os.getenv("MK2_TRACE_NATIVE_FINISH"))
local id=assert(({kano=17,sonya=18})[fighter])
local ids={kung_lao=0,liu_kang=1,cage=2,baraka=3,kitana=4,mileena=5,shang_tsung=6,
 raiden=7,sub_zero=8,reptile=9,scorpion=10,jax=11,kano=17,sonya=18}
local own_field=side==1 and 0x01060220 or 0x01060df0
local victim_field=side==1 and 0x01060df0 or 0x01060220
local own_health=side==1 and 0x010602f0 or 0x01060ec0
local victim_health=side==1 and 0x01060ec0 or 0x010602f0
local victim_id=assert(ids[os.getenv(side==1 and 'MK2KS_P2_FIGHTER' or 'MK2KS_TEST_FIGHTER')])
local frame,damage_events,total_damage,wins,errors=0,0,0,0,0
local writers,taps={},{}
assert(p:read_u16(0xff8366c0)==0x4541 and p:read_u16(0xff8366f0)==0x8026,
    "Original native subtract/store health writer must remain intact")
local function valid(actor) return actor>=0x01000000 and actor<0x01100000 end
taps[1]=p:install_write_tap(victim_health,victim_health+15,"unassisted native victim health writes",function(at,data,mask)
    if at~=victim_health or mask&0xffff~=0xffff or p:read_u16(0x010601d0)~=2 then return end
    local before,after=p:read_u16(at),data&0xffff
    local own,victim=p:read_u32(own_field),p:read_u32(victim_field)
    if before>161 or after>=before or not valid(own) or not valid(victim) or
        p:read_u16(own+0x1f0)~=id or p:read_u16(victim+0x1f0)~=victim_id or
        p:read_u16(0x010601f0)~=1 or p:read_u16(0x01060dc0)~=1 then return end
    damage_events=damage_events+1;total_damage=total_damage+before-after
    if cpu.PC.value~=0xff836700 then errors=errors+1 end
    writers[cpu.PC.value]=true
    print(string.format("MK2_UNASSISTED_DAMAGE frame=%d pc=%08X actor=%08X id=%d health=%d,%d damage=%d",
        frame,cpu.PC.value,victim,p:read_u16(victim+0x1f0),before,after,before-after))
end)
taps[2]=p:install_read_tap(0xfffef800,0xfffef800+19*32-1,"unassisted native round victory",function(at)
    local own=p:read_u32(own_field)
    if (at-0xfffef800)%32==0 and (at-0xfffef800)//32==id and valid(own) and
        p:read_u16(own+0x1f0)==id and p:read_u16(own_health)>0 and p:read_u16(victim_health)==0 and
        p:read_u16(0x010601f0)==1 and p:read_u16(0x01060dc0)==1 then
        wins=wins+1
        print(string.format("MK2_UNASSISTED_WIN frame=%d fighter=%s wins=%d damage=%d",frame,fighter,wins,total_damage))
    end
end)
local hud=side==1 and 0xfffee800 or 0xfffee000
taps[3]=p:install_read_tap(hud,hud+19*64-1,'actual victim native HUD construction',function(at)
 if (at-hud)%64==0 and(at-hud)//64==victim_id and p:read_u16(victim_field+0x60)==victim_id then
  print(string.format('MK2_UNASSISTED_HUD frame=%d victim_slot=%d id=%d entry=%08X pc=%08X',frame,3-side,victim_id,at,cpu.PC.value))
 end
end)
emu.register_frame(function() frame=frame+1;assert(#taps==3) end)
emu.register_stop(function()
    local pcs={}
    for pc in pairs(writers) do pcs[#pcs+1]=string.format("%08X",pc) end
    table.sort(pcs)
    print(string.format("MK2_UNASSISTED_RESULT fighter=%s damage_events=%d total_damage=%d wins=%d errors=%d writers=%s writes=0 assistance=none side=%d scope=native_physical_slot_damage_and_finisher_input",
        fighter,damage_events,total_damage,wins,errors,table.concat(pcs,","),side))
end)
