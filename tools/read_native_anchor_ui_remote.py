"""Read existing terminal UI-case rasters; compose a diagnostic sheet in RAM."""
def _send_anchor_ui():
    import base64,hashlib,io,json,os,socket,struct,sys,traceback
    from PIL import Image,ImageDraw
    connection=socket.create_connection(('127.0.0.1',51438),timeout=5)
    def receive(n):
        buf=bytearray()
        while len(buf)<n:
            part=connection.recv(n-len(buf))
            if not part:raise ValueError('Incomplete bounded UI diagnostic request')
            buf.extend(part)
        return bytes(buf)
    answer=dict(hostPID=os.getpid(),readOnly=True,newNativeBoots=0,gameWrites=0,persistentRawFiles=0)
    try:
        size=struct.unpack('<I',receive(4))[0];assert 0<size<2048
        request=json.loads(receive(size))
        profile=request['profile'];assert os.getpid()=={'delayed':27800,'standard':12004}[profile]
        ram=sys.modules['__main__'].RAM
        case=request['case'];captured=ram['cases'][case]
        assert captured['process'].poll()==0 and captured['report']['nativeExit']==0
        answer['actualNativeIdentity']=captured['identity']
        frames=captured['images'];assert 0<len(frames)<=80
        answer['availableFrames']=[dict(header=f['header'],SHA256=f['SHA256'])for f in frames]
        selected=request['indices'];assert isinstance(selected,list) and len(selected)<=6
        assert all(isinstance(n,int)and 0<=n<len(frames)for n in selected)
        answer['selectedFrames']=[]
        sheet=Image.new('RGB',(800,276*((len(selected)+1)//2)),(24,24,24))if selected else None
        draw=ImageDraw.Draw(sheet)if sheet else None
        for i,index in enumerate(selected):
            frame=frames[index];raw=frame['raw'];im=frame['image']
            assert len(raw)==406400 and im.size==(400,254)and im.mode=='RGB'
            assert hashlib.sha256(raw).hexdigest().upper()==frame['SHA256']
            assert im.tobytes()==Image.frombytes('RGB',(400,254),raw,'raw','BGRX').tobytes()
            row=frame['header'];x=(i%2)*400;y=(i//2)*276
            sheet.paste(im,(x,y));draw.text((x+4,y+256),f"{index}: {row['label']} / frame {row['frame']}",fill=(255,255,255))
            answer['selectedFrames'].append(dict(index=index,header=row,SHA256=frame['SHA256']))
        if sheet:
            buf=io.BytesIO();sheet.save(buf,format='PNG')
            answer['pngBase64']=base64.b64encode(buf.getvalue()).decode()
        answer['passed']=True
    except Exception:answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode();assert len(packet)<5000000
    with connection:connection.sendall(struct.pack('<I',len(packet))+packet)
_send_anchor_ui()
