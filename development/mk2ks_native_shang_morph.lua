-- Read-only native Shang provenance, never an ID alias or game-memory patch.
local existing=rawget(_G,"MK2_NATIVE_SHANG_OBSERVER")
if existing then return existing end
local p=manager.machine.devices[":maincpu"].spaces.program
local cpu=manager.machine.devices[":maincpu"].state
assert(p:read_u16(0xff86e650)==0xb128 and p:read_u16(0xff86e660)==0x01f0,
    "Original Shang MOVE A9,*A8(1F0h),0 changed")
assert(p:read_u16(0xffa166e0)==0xb008 and p:read_u16(0xffa166f0)==0x01f0,
    "Original Shang MOVE A0,*A8(1F0h),0 changed")
local frame,taps,records=0,{},{}
local observer={}
local function valid(a) return a>=0x01000000 and a<0x01100000 end
local function owned(a)
    local a2=p:read_u32(0x01060df0)
    local r2=p:read_u16(0x01060e50)
    if a~=p:read_u32(0x01060220) or not valid(a2) or (r2~=17 and r2~=18) or
        p:read_u16(a2+0x1f0)~=r2 or p:read_u16(0x010601f0)~=0 or
        p:read_u16(0x01060dc0)~=1 or p:read_u16(0x01060280)~=6 or
        p:read_u16(0x01061b30)~=14 or p:read_u32(0xff8a11f0)~=0xfffa2c00 then return false end
    local schedule=p:read_u32(0x01061b10)
    for order=0,5 do
        if p:read_u32(0xfffa2c00+order*32)==schedule and p:read_u16(schedule+14*16)==6 then return true end
    end
    return false
end
function observer.allowed(a,expected)
    local record=records[a]
    return expected==6 and owned(a) and record and record.id==p:read_u16(a+0x1f0) and
        record.process==p:read_u32(0x01060260) and record.id<=11
end
emu.register_frame(function()
    frame=frame+1
    if frame==1 then print("MK2_NATIVE_SHANG_ROM morph_store=FF86E650:B128,01F0 restore_store=FFA166E0:B008,01F0") end
    local a=p:read_u32(0x01060220)
    if not valid(a) or not owned(a) or taps[a] then return end
    records[a]=nil
    taps[a]=p:install_write_tap(a+0x1f0,a+0x1ff,"original scheduled Shang ID stores",function(at,data,mask)
        if not owned(a) or mask~=0xffff or cpu.A8.value~=a or cpu.A13.value~=p:read_u32(0x01060260) then return end
        local pc,new=cpu.PC.value,data&0xffff
        local morph=pc==0xff86e670 and new<=11 and new==(cpu.A9.value&0xffff)
        local restore=pc==0xffa16700 and new==6 and new==(cpu.A0.value&0xffff)
        if not morph and not restore then records[a]=nil;return end
        records[a]={id=new,process=cpu.A13.value}
        print(string.format("MK2_NATIVE_SHANG_ID frame=%d actor=%08X old=%d new=%d pc=%08X a9=%08X a0=%08X a8=%08X process=%08X mask=%04X kind=%s",
            frame,a,p:read_u16(a+0x1f0),new,pc,cpu.A9.value,cpu.A0.value,cpu.A8.value,cpu.A13.value,mask,morph and "morph" or "restore"))
    end)
end)
rawset(_G,"MK2_NATIVE_SHANG_OBSERVER",observer)
return observer
