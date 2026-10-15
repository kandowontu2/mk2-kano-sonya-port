"""CPython diagnostic callback: READ the existing campaign host RAM only.

No native memory/register/input/process writes, no source changes, no replay,
no clears of original RAM, and no persistent screenshot files. A bounded
localhost connection transports copies of already observed exact native RGB.
"""
def _mk2_drain_send_existing_rasters():
    import base64
    import hashlib
    import io
    import json
    import os
    import socket
    import struct
    import sys
    import traceback

    answer = dict(hostPID=os.getpid(), readOnly=True, newNativeBoots=0,
                  gameWrites=0, physicalInputs=0, persistentRawFiles=0)
    connection=socket.create_connection(('127.0.0.1',51437),timeout=5)
    def receive(count):
        result=bytearray()
        while len(result)<count:
            chunk=connection.recv(count-len(result))
            if not chunk:raise ValueError('Incomplete bounded diagnostic request')
            result.extend(chunk)
        return bytes(result)
    try:
        request_size=struct.unpack('<I',receive(4))[0]
        assert 0<request_size<2048
        request=json.loads(receive(request_size))
        assert isinstance(request,list) and len(request)<=2 and all(isinstance(n,str) for n in request)
        ram = sys.modules['__main__'].RAM
        process, identity = ram['process'], ram['identity']
        assert os.getpid()==30848 and process.pid==31336 and identity['createdUnix']==1791721342.2271461
        assert identity['ParentProcessId']==os.getpid()
        answer['nativeIdentity']=dict(identity)
        answer['nativePoll']=process.poll()
        scope=ram['scope']
        images, raw=scope['RAM_IMAGES'], scope['RAM_RAW']
        names=sorted(images)
        answer['availableNames']=names
        selected=[n for n in names if n in request and (n.startswith('shang_shrink_') or n.startswith('shang_victim_provenance_'))]
        assert len(selected)<=28 and len(images)<=64
        answer['frames']=[]
        for name in selected:
            image=images[name]
            native=raw[name]
            assert image.mode=='RGB' and image.size==(400,254) and len(native)==406400
            # Verify the displayed RGB against the ORIGINAL untouched BGRX buffer.
            rgb=bytes(channel for i in range(0,len(native),4) for channel in (native[i+2],native[i+1],native[i]))
            assert image.tobytes()==rgb
            buf=io.BytesIO();image.save(buf,format='PNG')
            answer['frames'].append(dict(name=name,nativeRGBSHA256=hashlib.sha256(native).hexdigest().upper(),
                                         pngBase64=base64.b64encode(buf.getvalue()).decode()))
        answer['passed']=True
    except Exception:
        answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode()
    assert len(packet)<5000000
    with connection:
        connection.sendall(struct.pack('<I',len(packet))+packet)


_mk2_drain_send_existing_rasters()
