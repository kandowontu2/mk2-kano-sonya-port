"""Sparse opaque bounds from actual cache/GFX; no pixel dumps or screenshots."""
import prepare_bounded_native_uppercut_retained_tap_probe as old
scope=dict(old.scope)
scope['OUT']=old.prior.ROOT/'audit_bounded_native_stance_bounds_preparation'
tail=scope['TAIL']
assert tail.count('if ordinary then')==1
tail=tail.replace('if ordinary then','if false and ordinary then',1)
assert tail.count('if age>=1800 then')==1
tail=tail.replace('if age>=1800 then','if age>=120 then',1)
tail+=r'''
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
    if age~=8 and age~=16 and age~=24 and age~=32 then return end
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
'''
scope['TAIL']=tail
exec(compile(old.previous.source,__file__,'exec'),scope)
if __name__=='__main__':scope['main']()
