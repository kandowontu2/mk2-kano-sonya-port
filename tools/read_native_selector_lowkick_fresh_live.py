"""Verify exact retained host/native identities and read bounded RAM counters."""
import json
import socket
import struct
import sys
from pathlib import Path
import read_live_shang_drain_frames as transport

host = next(r for r in transport.census_hosts() if r['ProcessId'] == 5752)
assert host['ParentProcessId'] == 19028
assert 'recover_native_selector_models_after_host_exit.py' in host['CommandLine']
assert Path(host['ExecutablePath']).resolve() == Path(sys.executable).resolve()
with socket.socket() as server:
    server.bind(('127.0.0.1', 51462))
    server.listen(1)
    server.settimeout(20)
    sys.remote_exec(5752, str(transport.ROOT / 'tools/read_native_selector_lowkick_fresh_live_remote.py'))
    conn, _ = server.accept()
    with conn:
        conn.settimeout(10)
        size = struct.unpack('<I', transport.read_exact(conn, 4))[0]
        assert 0 < size < 10000
        answer = json.loads(transport.read_exact(conn, size))
assert answer['passed'] and answer['hostPID'] == 5752 and host in transport.census_hosts()
native = answer['actualNativeIdentity']
assert native['ProcessId'] == 21456 and native['ParentProcessId'] == 5752
if answer['nativeExit'] is None:
    assert native in transport.identity.census()
else:
    assert native not in transport.identity.census()
answer.update(actualHostIdentity=host, identityRevalidatedBeforeAndAfter=True)
print(json.dumps(answer), flush=True)
