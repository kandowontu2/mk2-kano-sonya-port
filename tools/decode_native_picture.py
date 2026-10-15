"""Decode original MKII/MK3 picture LZ/Huffman records (no artwork synthesis).

Derived from original MK3 FF929660/FF9298C0/FF92A3B0/FF92A6E0;
the matching original MKII routines are FF903CE0/FF903F40/FF904A30/FF904D60.
"""
import struct
from pathlib import Path
from PIL import Image


class Bits:
    def __init__(self,data,offset): self.data,self.position=data,offset*8
    def read(self,n):
        if self.position+n>len(self.data)*8: raise ValueError('Truncated native picture')
        byte=self.position//8
        word=int.from_bytes(self.data[byte:byte+(self.position%8+n+7)//8],'little')
        value=(word>>(self.position%8))&((1<<n)-1)
        self.position+=n
        return value


def codebook(bits):
    groups=bits.read(8)+1
    lengths=[]
    for _ in range(groups):
        packed=bits.read(8)
        lengths.extend([1+(packed&15)]*(1+(packed>>4)))
    if len(lengths)!=64: raise ValueError('Original native book must contain 64 symbols')
    # Native stable shortest-first selection sort is popped in reverse order.
    prefix,step,previous=0,0,None
    codes={}
    for symbol in reversed(sorted(range(64),key=lambda index:(lengths[index],index))):
        prefix+=step
        length=lengths[symbol]
        if previous!=length: step=1<<(16-length);previous=length
        reverse=int(f'{prefix:016b}'[::-1],2)
        key=(length,reverse&((1<<length)-1))
        if key in codes: raise ValueError('Ambiguous native codebook')
        codes[key]=symbol
    return codes


def symbol(bits,codes):
    prefix=0
    for length in range(1,17):
        prefix|=bits.read(1)<<(length-1)
        if (length,prefix) in codes: return codes[length,prefix]
    raise ValueError('Invalid native Huffman symbol')


def decode(data,offset):
    width,height,frames,count=struct.unpack_from('<4H',data,offset)
    if not (0<width<=1024 and 0<height<=1024 and frames==1 and 0<count<=256):
        raise ValueError('Unsupported native picture header')
    palette=struct.unpack_from(f'<{count}H',data,offset+8)
    bits=Bits(data,offset+8+count*2)
    lengths,distances=codebook(bits),codebook(bits)
    output=bytearray()
    target=width*height
    while len(output)<target:
        if bits.read(1): output.append(bits.read(8))
        else:
            distance=(bits.read(6)|(symbol(bits,distances)<<6))+1
            run=symbol(bits,lengths)
            if run==63: run+=bits.read(8)
            run+=2
            if len(output)+run>target: raise ValueError('Native copy exceeds picture dimensions')
            for _ in range(run):
                previous=len(output)-distance
                output.append(output[previous] if previous>=0 else 0)
    if max(output)>=count: raise ValueError('Native pixel exceeds palette')
    # Native slideshow/backdrop row output runs from the bottom upward.
    top_down=b''.join(output[row*width:(row+1)*width] for row in reversed(range(height)))
    image=Image.frombytes('P',(width,height),top_down)
    rgb=[]
    for word in palette: rgb.extend((((word>>10)&31)*255//31,((word>>5)&31)*255//31,(word&31)*255//31))
    image.putpalette(rgb+[0]*(768-len(rgb)))
    return image,{'width':width,'height':height,'palette_count':count,'stream_end_bit':bits.position,
                  'decoded_pixels':len(output),'source_offset':offset}
