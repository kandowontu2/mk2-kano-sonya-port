"""Strict classic IPS codec. Per-chip patches; no emulator or ROM execution."""
LIMIT=0x1000000
RESERVED=0x454f46

def apply_patch(source, patch):
    if not patch.startswith(b'PATCH'): raise ValueError('Missing IPS header')
    output=bytearray(source);cursor=5
    def take(size):
        nonlocal cursor
        if cursor+size>len(patch): raise ValueError('Truncated IPS record')
        data=patch[cursor:cursor+size];cursor+=size
        return data
    while True:
        address=take(3)
        if address==b'EOF': break
        offset=int.from_bytes(address,'big')
        size=int.from_bytes(take(2),'big')
        if size: payload=take(size)
        else:
            count=int.from_bytes(take(2),'big')
            if not count: raise ValueError('Empty IPS RLE record')
            payload=take(1)*count
        end=offset+len(payload)
        if end>LIMIT: raise ValueError('IPS record exceeds address limit')
        if end>len(output): output.extend(bytes(end-len(output)))
        output[offset:end]=payload
    remaining=len(patch)-cursor
    if remaining not in (0,3): raise ValueError('Unexpected IPS trailing data')
    if remaining:
        size=int.from_bytes(take(3),'big')
        if size>len(output): output.extend(bytes(size-len(output)))
        else: del output[size:]
    return bytes(output)

def create_patch(source,target):
    if max(len(source),len(target))>=LIMIT: raise ValueError('Classic IPS size limit')
    result=bytearray(b'PATCH');cursor=0
    def equal(at): return at<len(source) and source[at]==target[at]
    def repeated(at):
        end=at+1
        while end<len(target) and end-at<65535 and target[end]==target[at]: end+=1
        return end-at
    while cursor<len(target):
        if equal(cursor): cursor+=1;continue
        start=cursor
        if start==RESERVED:
            # EOF cannot be a record address. Include one already-correct byte.
            start-=1
            size=min(65535,len(target)-start)
            result+=start.to_bytes(3,'big')+size.to_bytes(2,'big')+target[start:start+size]
            cursor=start+size;continue
        run=repeated(start)
        if run>=8:
            result+=start.to_bytes(3,'big')+b'\0\0'+run.to_bytes(2,'big')+target[start:start+1]
            cursor+=run;continue
        cursor+=1
        while cursor<len(target) and cursor-start<65535:
            if equal(cursor):
                end=cursor
                while end<len(target) and end-cursor<8 and equal(end): end+=1
                if end-cursor==8 or end==len(target): break
            if cursor+8<=len(target) and target[cursor:cursor+8]==target[cursor:cursor+1]*8: break
            cursor+=1
        payload=target[start:cursor]
        result+=start.to_bytes(3,'big')+len(payload).to_bytes(2,'big')+payload
    result+=b'EOF'+len(target).to_bytes(3,'big')
    assert apply_patch(source,result)==target
    return bytes(result)
