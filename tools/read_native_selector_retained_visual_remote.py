"""Expose selected actual RGB frames as in-memory PNG, no raw files or edits."""
def send():
    import base64,hashlib,io,json,os,socket,struct,sys,traceback
    answer=dict(hostPID=os.getpid(),gameWrites=0,newGames=0)
    try:
        from PIL import Image
        assert os.getpid()==5752
        prepared=sys.modules['prepare_native_selector_lowkick_after_host_exit_scoped']
        held=prepared.NATIVE_HANDLES[prepared.SCOPE['KEY']]
        assert held['identity']['ProcessId']==21456 and held['process'].poll()==0
        views=[]
        for frame in (1917,1955,2572):
            key='display_%d.png'%frame; rgb=prepared.DISPLAY['rgb'][key]
            assert rgb.shape==(254,400,3)
            output=io.BytesIO(); Image.fromarray(rgb).save(output,format='PNG')
            views.append(dict(frame=frame,rgbSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),
                pngBase64=base64.b64encode(output.getvalue()).decode()))
        answer.update(passed=True,nativeIdentity=held['identity'],views=views)
    except Exception: answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode(); assert len(packet)<1000000
    try:
        with socket.create_connection(('127.0.0.1',51464),timeout=5) as conn:
            conn.sendall(struct.pack('<I',len(packet))+packet)
    except OSError: pass
send()
