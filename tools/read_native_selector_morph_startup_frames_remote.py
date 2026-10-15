"""Return individual whole-digest-bound morph rasters without image files."""
def send():
    import base64, hashlib, io, json, os, socket, struct, sys, traceback
    import numpy as np
    from PIL import Image
    connection = socket.create_connection(('127.0.0.1',51438), timeout=5)
    def receive(n):
        data = bytearray()
        while len(data) < n:
            part = connection.recv(n-len(data))
            if not part: raise ValueError('Incomplete original reader request')
            data.extend(part)
        return bytes(data)
    answer = dict(hostPID=os.getpid(), readOnly=True, newNativeBoots=0,
        gameWrites=0, persistentRawFiles=0)
    try:
        size = struct.unpack('<I', receive(4))[0]; assert 0 < size < 2048
        request = json.loads(receive(size))
        assert os.getpid() == 38752 and request['profile'] == 'startup' and request['case'] == 'ball_p1'
        root = sys.modules['capture_native_selector_morph_startup_return']
        c = root.CASES['ball',1]
        receipt = json.loads((root.ROOT/'audit_native_selector_morph_startup_return_ball_p1_checked/report.json').read_text())
        identity = c['terminal']['actualWindowsIdentity']
        assert receipt['passed'] and c['report']['passed'] and c['process'].poll() == c['terminal']['nativeExit'] == 0
        assert identity == receipt['actualNativeIdentity'] and (identity['ProcessId'],identity['ParentProcessId'],identity['createdUnix']) == (46572,38752,1791761737.394802)
        answer['actualNativeIdentity'] = identity
        answer['availableFrames'] = [r['header'] for r in c['rgbFrames']]
        selected = request['indices']; assert 0 < len(selected) <= 6
        assert all(isinstance(n,int) and 0 <= n < len(c['rgbFrames']) for n in selected)
        answer['selectedFrames'] = []
        for index in selected:
            r = c['rgbFrames'][index]; raw, head = r['pixels'], r['header']
            assert len(raw) == 406400 and head['width'] == '400' and head['height'] == '254'
            assert hashlib.sha256(raw).hexdigest().upper() == head['sha256']
            packed = np.frombuffer(raw, np.uint8).reshape(254,400,4)
            assert np.all(packed[:,:,3] == 255)
            rgb = np.ascontiguousarray(packed[:,:,:3][:,:,::-1])
            png = io.BytesIO(); Image.fromarray(rgb).save(png, format='PNG')
            answer['selectedFrames'].append(dict(index=index, header=head,
                SHA256=head['sha256'], nativeRGBSHA256=hashlib.sha256(rgb.tobytes()).hexdigest().upper(),
                actualReconstructedAlpha=255, pngBase64=base64.b64encode(png.getvalue()).decode()))
        answer['passed'] = True
    except Exception:
        answer.update(passed=False, error=traceback.format_exc())
    packet = json.dumps(answer).encode(); assert len(packet) < 5000000
    with connection: connection.sendall(struct.pack('<I',len(packet))+packet)


send()
