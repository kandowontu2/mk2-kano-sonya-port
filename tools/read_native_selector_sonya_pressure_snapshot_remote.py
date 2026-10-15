"""Read actual current images only; no guest inputs or persistent media."""
def send():
    import base64,hashlib,io,json,os,socket,struct,sys,traceback
    import numpy as np
    from PIL import Image,ImageDraw
    conn=socket.create_connection(('127.0.0.1',51439),timeout=5)
    def receive(n):
        result=bytearray()
        while len(result)<n:
            block=conn.recv(n-len(result));assert block
            result.extend(block)
        return bytes(result)
    answer=dict(hostPID=os.getpid(),readOnly=True,newNativeBoots=0,gameWrites=0,persistentRawFiles=0)
    try:
        size=struct.unpack('<I',receive(4))[0];assert 0<size<2048
        frames=json.loads(receive(size));assert os.getpid()==38752
        capture=sys.modules['capture_native_selector_sonya_pressure_snapshot']
        held=capture.NATIVE_HANDLES[capture.KEY]
        receipt=json.loads((capture.ROOT/'audit_native_selector_sonya_pressure_snapshot_schedule_checked/report.json').read_text())
        assert receipt['passed']and held['process'].poll()==receipt['nativeExit']==0
        assert receipt['actualNativeIdentity']==held['identity']
        assert 0<len(frames)<=6 and len(set(frames))==len(frames)and all(isinstance(f,int)and 1818<=f<3618 for f in frames)
        display=capture.DISPLAY;answer['actualNativeIdentity']=held['identity'];answer['selectedFrames']=[]
        sheet=Image.new('RGB',(800,276*((len(frames)+1)//2)),(24,24,24));draw=ImageDraw.Draw(sheet)
        for i,f in enumerate(frames):
            file='display_%d.png'%f;h=display['rgbHeaders'][file];rgb=display['rgb'][file]
            assert rgb.shape==(254,400,3)and rgb.dtype==np.uint8 and h['frame']==str(f)
            raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1];matches=[]
            for alpha in (0,255):
                raw[:,:,3]=alpha
                if hashlib.sha256(raw.tobytes()).hexdigest().upper()==h['sha256']:matches.append(alpha)
            assert len(matches)==1,'Complete original BGRX callback reconstructed, no target substitution'
            x=i%2*400;y=i//2*276;sheet.paste(Image.fromarray(rgb),(x,y))
            draw.text((x+4,y+256),'actual current snapshot %d'%f,fill=(255,255,255))
            answer['selectedFrames'].append(dict(frame=f,header=h,alpha=matches[0],
                nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper()))
        buf=io.BytesIO();sheet.save(buf,format='PNG');answer['pngBase64']=base64.b64encode(buf.getvalue()).decode()
        answer['passed']=True
    except Exception:answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode();assert len(packet)<5000000
    with conn:conn.sendall(struct.pack('<I',len(packet))+packet)


send()
