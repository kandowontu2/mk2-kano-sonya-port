-- Read-only native MKII body, costume palette and ownership observer.
-- Normal inputs and explicit round-health assistance belong to the reused
-- harness. This observer never writes game state or substitutes a character.
dofile("mk2ks_kano_winner_hold_test.lua")
local p=manager.machine.devices[":maincpu"].spaces.program
local side=tonumber(os.getenv("MK2_TRACE_NATIVE_FINISH_SIDE") or "1")
local own_pointer=side==1 and 0x01060220 or 0x01060df0
local other_pointer=side==1 and 0x01060df0 or 0x01060220
local rows={
    {0xff91a150,0xff91e1a0,0xff91e220,0xff91e320,0xff91e420,0xff91e4a0},
    {0xff926010,0xff92b890,0xff92b930,0xff92bab0,0xff92bbb0,0xff92bc70},
    {0xff934b50,0xff93a410,0xff93a470,0xff93a550,0xff93a6b0,0xff93a750},
    {0xff941cf0,0xff947390,0xff947410,0xff947530,0xff947690,0xff947750},
    {0xff94da00,0xff958330,0xff958390,0xff958470,0xff958570,0xff958610},
    {0xff94da00,0xff958330,0xff958390,0xff958470,0xff958570,0xff958610},
    {0xff960080,0xff9663d0,0xff966430,0xff966510,0xff966610,0xff966690},
    {0xff96e5d0,0xff975010,0xff975070,0xff975150,0xff975270,0xff975310},
    {0xff97fad0,0xff989570,0xff9895d0,0xff9896b0,0xff9897b0,0xff989830},
    {0xff97fad0,0xff989570,0xff9895d0,0xff9896b0,0xff9897b0,0xff989830},
    {0xff97fad0,0xff989570,0xff9895d0,0xff9896b0,0xff9897b0,0xff989830},
    {0xff991950,0xff997980,0xff9979e0,0xff997aa0,0xff997b60,0xff997be0}
}
local palettes={
    {0xffadc3f0,0xff90ed40},{0xffadd0d0,0xff90d0d0},
    {0xffaddd00,0xff90d4e0},{0xff90d8f0,0xffade930},
    {0xffae0020,0xff90e110},{0xff90dd00,0xff90e520},
    {0xffae0c50,0xff90e930},{0xffae4090,0xff90ccc0},
    {0xff90f100,0xff90f510},{0xff90f920,0xff90fd30},
    {0xffae5c00,0xff910140},{0xffae6950,0xff910550}
}
local identity=assert(tonumber(os.getenv("MK2_TRACE_EXPECT_VICTIM_ID") or "",16))
assert(identity>=0 and identity<12,"This observer requires a native stock victim")
local poses=rows[identity+1]
local permitted={}
for _,pose in ipairs(poses) do permitted[pose]=true end
local frame,windup,headless,errors,releases=0,0,0,0,0
local actor,original_bank,body_bank,first_headless,windup_start
local retired,pool_reset,cleared,palette,count,alternate
local original_colors,seen={},{}
local function bank_ref(bank)
    return p:read_u16(0x0105bb30+(bank&0xff)*0x40+0x20)
end
local function valid(ptr) return ptr>=0x01000000 and ptr<0x01100000 end
local reset_tap=p:install_read_tap(0xff80cce0,0xff80ccef,"native stock body palette reset",function(offset)
    if offset==0xff80cce0 and body_bank and not pool_reset then
        pool_reset=frame
        print(string.format("MK2_STOCK_BODY_PALETTE_RESET frame=%d bank=%04X source=%08X refs=%d retired=%s",
            frame,body_bank,p:read_u32(0x0105bb30+(body_bank&0xff)*0x40),bank_ref(body_bank),tostring(retired)))
    end
end)
local ref_tap=p:install_write_tap(0x0105bb30,0x0105ca2f,"native stock body palette lifetime",function(offset,data,mask)
    if body_bank and not cleared and offset==0x0105bb30+(body_bank&0xff)*0x40+0x20 and
       (mask&0xffff)==0xffff and (data&0xffff)==0 then
        releases=releases+1
        cleared=frame
        if not retired or not pool_reset or pool_reset~=frame then errors=errors+1 end
        print(string.format("MK2_STOCK_BODY_PALETTE_CLEAR frame=%d bank=%04X errors=%d",frame,body_bank,errors))
    end
end)
emu.register_frame(function()
    assert(reset_tap and ref_tap) -- retain native tap handles for the whole run
    frame=frame+1
    local own,other=p:read_u32(own_pointer),p:read_u32(other_pointer)
    if actor and other~=actor and not retired then retired=frame end
    if not actor and valid(own) and valid(other) and
       p:read_u16(own+0x1f0)==17 and p:read_u16(other+0x1f0)==identity and
       p:read_u32(own+0x1d0)==0xfe9b2670 and p:read_u32(other+0x1d0)==poses[1] then
        actor=other
        original_bank=p:read_u16(actor+0x140)
        windup_start=frame
        alternate=(p:read_u16(actor+0x160)&0x40)~=0
        palette=palettes[identity+1][alternate and 2 or 1]
        assert(p:read_u32(0xff90c900+identity*64+(alternate and 32 or 0))==palette)
        count=p:read_u16(palette)
        assert(count>0 and count<=256)
        for i=0,63 do original_colors[i]=p:read_u16(0x01800000+((original_bank&0x7f00)+i)*16) end
        print(string.format("MK2_STOCK_BODY_START frame=%d id=%04X alternate=%s palette=%08X count=%d",frame,identity,tostring(alternate),palette,count))
    end
    if not actor or other~=actor or not valid(other) or
       (p:read_u16(0x01061b00)~=3 and p:read_u16(0x01061b00)~=side) then return end
    local pose=p:read_u32(actor+0x1d0)
    if not permitted[pose] then errors=errors+1 return end
    seen[pose]=true
    if p:read_u16(actor+0x1f0)~=identity then errors=errors+1 end
    local bank=p:read_u16(actor+0x140)
    if pose==poses[1] then
        windup=windup+1
        if bank~=original_bank then errors=errors+1 end
        for i=0,63 do
            if p:read_u16(0x01800000+((bank&0x7f00)+i)*16)~=original_colors[i] then errors=errors+1 end
        end
    else
        headless=headless+1
        if not body_bank then
            body_bank=bank
            first_headless=frame
            print(string.format("MK2_STOCK_BODY_PALETTE_TRANSFER frame=%d id=%04X old=%04X new=%04X old_refs=%d new_refs=%d palette=%08X count=%d",
                frame,identity,original_bank,bank,bank_ref(original_bank),bank_ref(bank),palette,count))
        end
        if bank~=body_bank or bank==original_bank or bank_ref(bank)~=1 or
           p:read_u32(0x0105bb30+(bank&0xff)*0x40)~=palette then errors=errors+1 end
        for i=0,count-1 do
            if p:read_u16(0x01800000+((bank&0x7f00)+i)*16)~=p:read_u16(palette+16+i*16) then errors=errors+1 end
        end
    end
    local age=pose==poses[1] and frame-windup_start or frame-(first_headless or frame)
    if age<4 then
        local label=pose==poses[1] and "windup" or "headless"
        manager.machine.screens[":screen"]:snapshot(string.format("stock_body_%s_first_%02d.png",label,age))
        print(string.format("MK2_STOCK_BODY_FIELD frame=%d id=%04X label=%s age=%d bank=%04X pose=%08X errors=%d",frame,identity,label,age,bank,pose,errors))
    end
end)
emu.register_stop(function()
    local phases=0
    for _ in pairs(seen) do phases=phases+1 end
    local source=body_bank and p:read_u32(0x0105bb30+(body_bank&0xff)*0x40) or 0
    local refs=body_bank and bank_ref(body_bank) or -1
    local retained_refs=source==palette and refs or 0
    local passed=windup==59 and headless>=100 and phases==6 and errors==0 and releases==1 and retained_refs==0
    print(string.format("MK2_NATIVE_STOCK_BODY_RESULT pass=%s side=%d id=%04X alternate=%s windup=%d headless=%d phases=%d errors=%d pool_clears=%d retained_refs=%d",
        tostring(passed),side,identity,tostring(alternate),windup,headless,phases,errors,releases,retained_refs))
end)
