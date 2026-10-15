"""Read exact retained continue scanout bytes; no screenshots saved to disk."""
def _send_continue():
    import base64,hashlib,io,json,os,socket,struct,sys,traceback
    from PIL import Image,ImageDraw
    connection=socket.create_connection(('127.0.0.1',51438),timeout=5)
    def receive(n):
        buf=bytearray()
        while len(buf)<n:
            part=connection.recv(n-len(buf))
            if not part:raise ValueError('Incomplete bounded diagnostic request')
            buf.extend(part)
        return bytes(buf)
    answer=dict(hostPID=os.getpid(),readOnly=True,newNativeBoots=0,gameWrites=0,persistentRawFiles=0)
    try:
        size=struct.unpack('<I',receive(4))[0];assert 0<size<2048
        request=json.loads(receive(size));assert request['profile']=='continue'and os.getpid()==40856
        root=sys.modules['__main__'];case=request['case']
        folder,text,images,report=root.RAM_CASES[case];held=root.NATIVE_HANDLES[case]
        assert held['process'].poll()==0 and report['nativeExit']==0
        answer['actualNativeIdentity']=held.get('recoveredIdentity',held.get('identity'))
        assert answer['actualNativeIdentity']is not None
        frames=report['actualFullRGBDigests'];assert 0<len(frames)<200
        answer['availableFrames']=frames
        selected=request['indices'];assert isinstance(selected,list)and len(selected)<=6
        assert all(isinstance(n,int)and 0<=n<len(frames)for n in selected)
        answer['selectedFrames']=[]
        sheet=Image.new('RGB',(800,276*((len(selected)+1)//2)),(24,24,24))if selected else None
        draw=ImageDraw.Draw(sheet)if sheet else None
        for i,index in enumerate(selected):
            row=frames[index];raw=images[row['frame'],row['label']]
            assert len(raw)==406400 and hashlib.sha256(raw).hexdigest().upper()==row['sha256']
            im=Image.frombytes('RGB',(400,254),raw,'raw','BGRX');x=i%2*400;y=i//2*276
            sheet.paste(im,(x,y));draw.text((x+4,y+256),f"{index}: {row['label']} / {row['frame']}",fill=(255,255,255))
            answer['selectedFrames'].append(dict(index=index,header=row,SHA256=row['sha256']))
        if sheet:
            buf=io.BytesIO();sheet.save(buf,format='PNG');answer['pngBase64']=base64.b64encode(buf.getvalue()).decode()
        answer['passed']=True
    except Exception:answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode();assert len(packet)<5000000
    with connection:connection.sendall(struct.pack('<I',len(packet))+packet)

_send_continue()
