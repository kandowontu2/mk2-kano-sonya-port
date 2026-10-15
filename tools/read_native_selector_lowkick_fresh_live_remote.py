"""Bounded read-only collector counters; no emulator or guest interaction."""
def send():
    import json, os, socket, struct, sys, traceback
    answer = dict(hostPID=os.getpid(), gameWrites=0, newNativeGames=0)
    try:
        assert os.getpid() == 5752
        capture = sys.modules['prepare_native_selector_lowkick_after_host_exit_scoped']
        key = capture.SCOPE['KEY']
        held = capture.NATIVE_HANDLES[key]
        assert held['identity']['ProcessId'] == 21456 and held['identity']['ParentProcessId'] == 5752
        audio = capture.AUDIO[key]
        answer.update(passed=True, actualNativeIdentity=held['identity'], nativeExit=held['process'].poll(),
                      displayCallbacks=len(capture.DISPLAY['rgbHeaders']),
                      displayBuffers=len(capture.DISPLAY['buffers']),
                      latestDisplayFrame=max((int(h['frame']) for h in capture.DISPLAY['rgbHeaders'].values()), default=None),
                      pcmCallbacks=len(audio['pcmHeaders']), dacCallbacks=len(audio['dacHeaders']))
    except Exception:
        answer.update(passed=False, error=traceback.format_exc())
    packet = json.dumps(answer).encode()
    assert len(packet) < 10000
    try:
        with socket.create_connection(('127.0.0.1', 51462), timeout=5) as conn:
            conn.sendall(struct.pack('<I', len(packet)) + packet)
    except OSError:
        # Late delivery after receiver timeout must not disturb the ongoing
        # original capture. The receiver will keep the timeout as unverified.
        pass
send()
