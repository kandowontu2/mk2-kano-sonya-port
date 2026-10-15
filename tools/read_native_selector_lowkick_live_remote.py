"""Read capture counters on exact existing host; no emulator interaction."""
def send():
    import json,os,socket,struct,sys,traceback
    answer=dict(hostPID=os.getpid(),gameWrites=0,newNativeGames=0)
    try:
        assert os.getpid()==38752
        capture=sys.modules['capture_native_selector_sonya_cpu_lowkick_owners']
        held=capture.NATIVE_HANDLES[capture.KEY]
        assert held['identity']['ProcessId']==49084 and held['identity']['ParentProcessId']==38752
        display=capture.DISPLAY
        audio=capture.AUDIO[capture.KEY]
        answer.update(passed=True,actualNativeIdentity=held['identity'],nativeExit=held['process'].poll(),
            displayCallbacks=len(display['rgbHeaders']),displayBuffers=len(display['buffers']),
            latestDisplayFrame=max((int(h['frame']) for h in display['rgbHeaders'].values()),default=None),
            pcmCallbacks=len(audio['pcmHeaders']),dacCallbacks=len(audio['dacHeaders']))
    except Exception:answer.update(passed=False,error=traceback.format_exc())
    packet=json.dumps(answer).encode();assert len(packet)<10000
    with socket.create_connection(('127.0.0.1',51461),timeout=5) as conn:
        conn.sendall(struct.pack('<I',len(packet))+packet)
send()
