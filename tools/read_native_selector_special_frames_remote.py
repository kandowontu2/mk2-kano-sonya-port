"""Render only source-digest-bound original terminal special RGB in RAM."""
def _send_special():
    import base64,hashlib,io,json,os,socket,struct,sys,traceback
    from PIL import Image,ImageDraw
    import numpy as np
    connection=socket.create_connection(('127.0.0.1',51438),timeout=5)
    def receive(n):
        buf=bytearray()
        while len(buf)<n:
            part=connection.recv(n-len(buf))
            if not part:raise ValueError('Incomplete bounded request')
            buf.extend(part)
        return bytes(buf)
    answer=dict(hostPID=os.getpid(),readOnly=True,newNativeBoots=0,gameWrites=0,persistentRawFiles=0)
    try:
        size=struct.unpack('<I',receive(4))[0];assert 0<size<2048
        request=json.loads(receive(size));assert os.getpid()==38752
        profile=request['profile'];assert profile in('special','air')
        root=sys.modules['__main__']if profile=='special'else sys.modules['capture_native_selector_square_contact_retained']
        cases=root.RAM_CASES if profile=='special'else root.CONTACT_CASES
        handles=root.NATIVE_HANDLES if profile=='special'else root.CONTACT_HANDLES
        case=request['case'];folder,text,images=cases[case];held=handles[case]
        report=json.loads((folder/'result.json').read_text())
        assert held['process'].poll()==0 and report['nativeExit']==0 and report['passed']
        answer['actualNativeIdentity']=held['identity'];frames=report['actualScenes']
        answer['availableFrames']=frames;selected=request['indices'];assert len(selected)<=6
        assert all(isinstance(n,int)and 0<=n<len(frames)for n in selected)
        answer['selectedFrames']=[]
        sheet=Image.new('RGB',(800,276*((len(selected)+1)//2)),(24,24,24))if selected else None
        draw=ImageDraw.Draw(sheet)if sheet else None
        for i,index in enumerate(selected):
            row=frames[index];rgb=images[f"ui_{row['frame']:04d}.png"]
            assert rgb.shape==(254,400,3)and rgb.dtype==np.uint8
            raw=np.empty((254,400,4),np.uint8);raw[:,:,:3]=rgb[:,:,::-1]
            alphas=[]
            for alpha in(0,255):
                raw[:,:,3]=alpha
                if hashlib.sha256(raw.tobytes()).hexdigest().upper()==row['sha256']:alphas.append(alpha)
            assert len(alphas)==1,'Every original RGB pixel reconstructs exact whole captured BGRX digest'
            x=i%2*400;y=i//2*276;sheet.paste(Image.fromarray(rgb),(x,y))
            draw.text((x+4,y+256),f"{index}: {row['stage']} / {row['frame']}",fill=(255,255,255))
            answer['selectedFrames'].append(dict(index=index,header=row,SHA256=row['sha256'],
                nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),actualReconstructedAlpha=alphas[0]))
        if sheet:
            buf=io.BytesIO();sheet.save(buf,format='PNG');answer['pngBase64']=base64.b64encode(buf.getvalue()).decode()
        answer['passed']=True
    except Exception:answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode();assert len(packet)<5000000
    with connection:connection.sendall(struct.pack('<I',len(packet))+packet)

_send_special()
