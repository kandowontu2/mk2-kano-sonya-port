"""Read-only MK3 image and composite records for native ROM art import.

No executable relocation, donor code, emulator hooks or driver generation.
Addresses below identify artwork metadata in the user-supplied revision.
"""
import struct

TMS_ROM_BASE=0xff800000
KANO_BLOCK=(0xff823ca0,0xff831b80)
SONYA_BLOCK=(0xff831b80,0xff8408c0)
SONYA_SPECIAL=0xff8323a0

def u16(data,offset):return struct.unpack_from('<H',data,offset)[0]
def u32(data,offset):return struct.unpack_from('<I',data,offset)[0]
def signed(value):return value-0x10000 if value&0x8000 else value

def stock_file(address):
    if not TMS_ROM_BASE<=address<=0xffffffff or address&15:
        raise ValueError(f'Not an aligned MK3 art pointer: {address:08x}')
    return (address-TMS_ROM_BASE)//8

def looks_like_frame(data,offset):
    if offset<0 or offset+14>len(data):return False
    coordinates=[signed(u16(data,offset+index*2)) for index in range(4)]
    if any(value < -0x400 or value > 0x400 for value in coordinates):return False
    source=u32(data,offset+8);control=u16(data,offset+12)
    # Native skip-form and full-copy records both keep low seven bits clear.
    return source<0x0a000000 and not control&0x007f and 3<=((control>>12)&7)<=7

def frame_group(data,address,span_start,span_end):
    if not span_start<=address<span_end or address&15:return None
    offset=stock_file(address);frames=[]
    for _ in range(16):
        if offset+4>len(data):return None
        value=u32(data,offset)
        if value==0:return frames or None
        if not TMS_ROM_BASE<=value<=0xffffffff or value&15:return None
        if not looks_like_frame(data,stock_file(value)):return None
        frames.append(value);offset+=4
    return None

def group_references(data,start_address,end_address,group_start=None,group_end=None):
    start,end=stock_file(start_address),stock_file(end_address)
    assert 0<=start<=end<=len(data)
    group_start=start_address if group_start is None else group_start
    group_end=end_address if group_end is None else group_end
    result=[]
    for offset in range(start,end-3,2):
        value=u32(data,offset)
        group=frame_group(data,value,group_start,group_end)
        if group is not None:
            if result and offset<result[-1][0]+4:continue
            result.append((offset,value,group))
    return result
