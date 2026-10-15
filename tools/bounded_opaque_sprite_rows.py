"""Small original-format sprite decoder for standing-sole observations.

Returns opaque bounds, not a screenshot or a graphical-alignment verdict.
"""
def bounds(raw,offset,width,height,command):
    assert 0<width<=200 and 0<height<=200
    assert len(raw)<=50000 and 0<=offset<8
    bit=offset;count=0;xs=[];ys=[]
    bpp=(command>>12)&7 or 8
    def take(n):
        nonlocal bit
        assert bit+n<=len(raw)*8,'Complete observed graphics stream required'
        value=(int.from_bytes(raw[bit//8:bit//8+2],'little')>>(bit%8))&((1<<n)-1)
        bit+=n;return value
    for y in range(height):
        pre=post=0
        if command&0x80:
            header=take(8)
            pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
        assert pre+post<=width
        for x in range(pre,width-post):
            if take(bpp):
                count+=1;xs.append(-x if command&16 else x);ys.append(-y if command&32 else y)
    return dict(opaquePixels=count,left=min(xs) if xs else None,right=max(xs) if xs else None,
        top=min(ys) if ys else None,bottom=max(ys) if ys else None,bitsConsumed=bit-offset)

def self_test():
    # Two six-bit rows; skip headers keep transparent descriptor padding out.
    values=[(0x11,8),(0,6),(3,6),(0x20,8),(2,6),(0,6)]
    value=0;at=3
    for part,n in values:value|=part<<at;at+=n
    raw=value.to_bytes((at+7)//8,'little')
    normal=bounds(raw,3,4,2,0x6080)
    assert normal==dict(opaquePixels=2,left=0,right=2,top=0,bottom=1,bitsConsumed=40)
    flipped=bounds(raw,3,4,2,0x60b0)
    assert flipped['left']==-2 and flipped['right']==0 and flipped['bottom']==0 and flipped['top']==-1
    try:bounds(raw[:1],3,4,2,0x6080)
    except AssertionError:pass
    else:raise AssertionError('Truncated sprite admitted')
    return dict(decoderUnitChecksPassed=True,actualStandingSoleParityAccepted=False)

if __name__=='__main__':
    import json
    print(json.dumps(self_test()))
