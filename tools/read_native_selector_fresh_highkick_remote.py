"""Read-only bounded counters from the exact retained high-kick collector."""
def send():
    import json,os,socket,struct,sys,traceback
    answer=dict(hostPID=os.getpid(),gameWrites=0,newNativeGames=0)
    try:
        assert os.getpid()==5752
        scope=sys.modules['prepare_native_selector_fresh_highkick_owners_bound'].scope
        key=scope['KEY']; held=scope['NATIVE_HANDLES'][key]; audio=scope['AUDIO'][key]
        assert (held['identity']['ProcessId'],held['identity']['ParentProcessId'],held['identity']['createdUnix']) == (3152,5752,1791816393.9003582)
        display=scope['DISPLAY']
        answer.update(passed=True,actualNativeIdentity=held['identity'],nativeExit=held['process'].poll(),
            displayCallbacks=len(display['rgbHeaders']),displayBuffers=len(display['buffers']),
            latestDisplayFrame=max((int(h['frame']) for h in display['rgbHeaders'].values()),default=None),
            pcmCallbacks=len(audio['pcmHeaders']),dacCallbacks=len(audio['dacHeaders']))
    except Exception: answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode(); assert len(packet)<10000
    try:
        with socket.create_connection(('127.0.0.1',51463),timeout=5) as conn:
            conn.sendall(struct.pack('<I',len(packet))+packet)
    except OSError: pass
send()
