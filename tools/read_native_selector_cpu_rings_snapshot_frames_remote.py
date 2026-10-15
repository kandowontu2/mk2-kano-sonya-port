"""Whole original snapshot digest binding; actual displayed RGB kept in RAM."""
def send():
    import base64,hashlib,io,json,os,socket,struct,sys,traceback
    from PIL import Image,ImageDraw
    import numpy as np
    connection=socket.create_connection(('127.0.0.1',51438),timeout=5)
    def receive(n):
        buf=bytearray()
        while len(buf)<n:
            part=connection.recv(n-len(buf));assert part
            buf.extend(part)
        return bytes(buf)
    answer=dict(hostPID=os.getpid(),readOnly=True,newNativeBoots=0,gameWrites=0,persistentRawFiles=0)
    try:
        size=struct.unpack('<I',receive(4))[0];assert 0<size<2048
        request=json.loads(receive(size));assert os.getpid()==38752
        root=sys.modules['capture_native_selector_cpu_rings_snapshot_ram']
        held=root.NATIVE_HANDLES[root.KEY];receipt=json.loads((root.ROOT/'audit_native_selector_cpu_rings_snapshot_transport_checked/report.json').read_text())
        assert receipt['passed'] and held['process'].poll()==receipt['nativeExit']==0
        assert receipt['actualNativeIdentity']==held['identity']
        window=request['window'];assert window in (1,2,3);display=root.DISPLAY[window]
        frames=list(display['rgbHeaders'].values());selected=request['indices'];answer['window']=window
        assert 0<len(selected)<=6 and all(isinstance(n,int) and 0<=n<len(frames) for n in selected)
        answer['actualNativeIdentity']=held['identity'];answer['selectedFrames']=[]
        sheet=Image.new('RGB',(800,276*((len(selected)+1)//2)),(24,24,24));draw=ImageDraw.Draw(sheet)
        for i,index in enumerate(selected):
            header=frames[index];rgb=display['rgb'][header['file']]
            assert rgb.shape==(254,400,3) and rgb.dtype==np.uint8
            raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1];matches=[]
            for alpha in (0,255):
                raw[:,:,3]=alpha
                if hashlib.sha256(raw.tobytes()).hexdigest().upper()==header['sha256']:matches.append(alpha)
            assert len(matches)==1,'All original BGRX pixels reconstruct original whole callback digest'
            x=i%2*400;y=i//2*276;sheet.paste(Image.fromarray(rgb),(x,y))
            draw.text((x+4,y+256),f"{index}: actual current snapshot {header['frame']}",fill=(255,255,255))
            answer['selectedFrames'].append(dict(index=index,header=header,
                nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),alpha=matches[0]))
        buf=io.BytesIO();sheet.save(buf,format='PNG');answer['pngBase64']=base64.b64encode(buf.getvalue()).decode()
        answer['passed']=True
    except Exception:answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode();assert len(packet)<5000000
    with connection:connection.sendall(struct.pack('<I',len(packet))+packet)

send()
