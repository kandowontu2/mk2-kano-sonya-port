"""Read current original snapshot from the exact retained native capture host."""
import json
import socket
import struct
import sys
from pathlib import Path
import read_live_shang_drain_frames as transport


def run():
    indices=[int(n) for n in sys.argv[1:]]
    assert 0<len(indices)<=6 and all(0<=n<106 for n in indices)
    pid=38752;host=next(p for p in transport.census_hosts() if p['ProcessId']==pid)
    assert host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766
    assert Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()
    assert host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_special_shadow.py'
    remote=transport.ROOT/'tools/read_native_selector_knife_snapshot_frames_remote.py'
    with socket.socket() as server:
        server.bind(('127.0.0.1',51438));server.listen(1);server.settimeout(20)
        sys.remote_exec(pid,str(remote));conn,_=server.accept()
        with conn:
            conn.settimeout(10);packet=json.dumps(dict(indices=indices)).encode()
            conn.sendall(struct.pack('<I',len(packet))+packet)
            size=struct.unpack('<I',transport.read_exact(conn,4))[0];assert 0<size<5000000
            answer=json.loads(transport.read_exact(conn,size))
    assert answer['passed'] and answer['hostPID']==pid and host in transport.census_hosts()
    assert answer['actualNativeIdentity']['ParentProcessId']==pid
    assert answer['actualNativeIdentity'] not in transport.identity.census()
    answer.update(actualHostIdentity=host,identityRevalidatedBeforeAndAfter=True)
    print(json.dumps(answer),flush=True)


if __name__=='__main__':run()
