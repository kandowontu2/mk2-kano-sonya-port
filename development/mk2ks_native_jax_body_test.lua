-- Read-only rendered-state/ownership observer. The reused harness supplies
-- normal inputs and explicit round-win assistance; this observer writes none.
dofile("mk2ks_kano_winner_hold_test.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
local own_pointer=side==1 and 0x01060220 or 0x01060df0
local other_pointer=side==1 and 0x01060df0 or 0x01060220
local poses={0xff991950,0xff997980,0xff9979e0,0xff997aa0,0xff997b60,0xff997be0}
local permitted={}
for _,pose in ipairs(poses) do permitted[pose]=true end
local frame,windup,headless,errors,releases=0,0,0,0,0
local actor,original_bank,body_bank,first_headless,windup_start
local retired,pool_reset,cleared
local original_colors,seen={},{ }
local function bank_ref(bank)
    return p:read_u16(0x0105bb30+(bank&0xff)*0x40+0x20)
end
local call_taps={}
for _,address in ipairs({0xff80d580,0xff80cad0,0xff80cf60,0xff80cce0,0xff80ce40}) do
    call_taps[#call_taps+1]=p:install_read_tap(address,address+15,"Jax body palette cleanup calls",function(offset)
        if offset==address and actor and os.getenv("MK2_TRACE_JAX_PALETTE_CALLS")=="1" then
            print(string.format("MK2_JAX_BODY_PALETTE_CALL frame=%d at=%08X a0=%08X a8=%08X pose=%08X bank=%04X body=%s",
                frame,address,cpu.A0.value,cpu.A8.value,p:read_u32(actor+0x1d0),p:read_u16(actor+0x140),tostring(body_bank)))
        end
        if offset==address and address==0xff80cce0 and body_bank and not pool_reset then
            pool_reset=frame
            print(string.format("MK2_JAX_BODY_PALETTE_RESET frame=%d bank=%04X source=%08X refs=%d retired=%s",
                frame,body_bank,p:read_u32(0x0105bb30+(body_bank&0xff)*0x40),bank_ref(body_bank),tostring(retired)))
        end
    end)
end
local palette=0xffae6950
local count=p:read_u16(palette)
assert(count>0 and count<=256,"Native headless palette must have a valid header")
local function valid(ptr) return ptr>=0x01000000 and ptr<0x01100000 end
local tap=p:install_write_tap(0x0105bb30,0x0105ca2f,"native Jax palette lifetime",
    function(offset,data,mask)
        if body_bank and not cleared and offset==0x0105bb30+(body_bank&0xff)*0x40+0x20 and
           (mask&0xffff)==0xffff then
            print(string.format("MK2_JAX_BODY_PALETTE_REF frame=%d bank=%04X refs=%d",frame,body_bank,data&0xffff))
            if (data&0xffff)==0 then
                releases=releases+1
                cleared=frame
                if not retired or not pool_reset or pool_reset~=frame then errors=errors+1 end
            end
        end
    end)
emu.register_frame(function()
    assert(tap and #call_taps==5) -- retain native tap handles for the full run
    frame=frame+1
    local own,other=p:read_u32(own_pointer),p:read_u32(other_pointer)
    if actor and other~=actor and not retired then retired=frame end
    if not actor and valid(own) and valid(other) and
       p:read_u16(own+0x1f0)==17 and p:read_u16(other+0x1f0)==11 and
       p:read_u32(own+0x1d0)==0xfe9b2670 and p:read_u32(other+0x1d0)==poses[1] then
        actor=other
        original_bank=p:read_u16(actor+0x140)
        windup_start=frame
        for i=0,count-1 do original_colors[i]=p:read_u16(0x01800000+((original_bank&0x7f00)+i)*16) end
    end
    if not actor or other~=actor or not valid(other) or
       (p:read_u16(0x01061b00)~=3 and p:read_u16(0x01061b00)~=side) then return end
    local pose=p:read_u32(actor+0x1d0)
    if not permitted[pose] then errors=errors+1 return end
    seen[pose]=true
    if p:read_u16(actor+0x1f0)~=11 then errors=errors+1 end
    local bank=p:read_u16(actor+0x140)
    if pose==poses[1] then
        windup=windup+1
        if bank~=original_bank then errors=errors+1 end
        for i=0,count-1 do
            if p:read_u16(0x01800000+((bank&0x7f00)+i)*16)~=original_colors[i] then errors=errors+1 end
        end
    else
        headless=headless+1
        if not body_bank then
            body_bank=bank
            first_headless=frame
            print(string.format("MK2_JAX_BODY_PALETTE_TRANSFER frame=%d old=%04X new=%04X old_refs=%d new_refs=%d native_palette=%08X count=%d",
                frame,original_bank,bank,bank_ref(original_bank),bank_ref(bank),palette,count))
        end
        if bank~=body_bank or bank==original_bank or bank_ref(bank)~=1 then errors=errors+1 end
        for i=0,count-1 do
            if p:read_u16(0x01800000+((bank&0x7f00)+i)*16)~=p:read_u16(palette+16+i*16) then
                errors=errors+1
            end
        end
    end
    local age=pose==poses[1] and frame-windup_start or frame-(first_headless or frame)
    if age<4 then
        local label=pose==poses[1] and "windup" or "headless"
        manager.machine.screens[":screen"]:snapshot(string.format("jax_body_%s_first_%02d.png",label,age))
        print(string.format("MK2_JAX_BODY_FIELD frame=%d label=%s age=%d bank=%04X pose=%08X errors=%d",
            frame,label,age,bank,pose,errors))
    end
end)
emu.register_stop(function()
    local phases=0
    for _ in pairs(seen) do phases=phases+1 end
    local source=body_bank and p:read_u32(0x0105bb30+(body_bank&0xff)*0x40) or 0
    local refs=body_bank and bank_ref(body_bank) or -1
    local retained_refs=source==palette and refs or 0
    local passed=windup==59 and headless>=100 and phases==6 and errors==0 and releases==1 and retained_refs==0
    print(string.format("MK2_NATIVE_JAX_BODY_RESULT pass=%s side=%d windup=%d headless=%d phases=%d errors=%d pool_clears=%d retained_refs=%d final_slot_source=%08X final_slot_refs=%d",
        tostring(passed),side,windup,headless,phases,errors,releases,retained_refs,source,refs))
end)
