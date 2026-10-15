"""RAM-only visual inspection of the exact retained pressure snapshot host."""
import json
import socket
import struct
import sys
from pathlib import Path
import read_live_shang_drain_frames as transport


def run():
    frames=[int(f)for f in sys.argv[1:]]
    assert 0<len(frames)<=6 and len(set(frames))==len(frames)and all(1818<=f<3618 for f in frames)
    host=next(r for r in transport.census_hosts()if r['ProcessId']==38752)
    assert host['ParentProcessId']==40316 and host['createdUnix']==1791734919.6266766
    assert Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()
    assert host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_selector_special_shadow.py'
    remote=transport.ROOT/'tools/read_native_selector_sonya_pressure_snapshot_remote.py'
    with socket.socket()as server:
        server.bind(('127.0.0.1',51439));server.listen(1);server.settimeout(20)
        sys.remote_exec(38752,str(remote));conn,_=server.accept()
        with conn:
            conn.settimeout(10);packet=json.dumps(frames).encode()
            conn.sendall(struct.pack('<I',len(packet))+packet)
            size=struct.unpack('<I',transport.read_exact(conn,4))[0];assert 0<size<5000000
            answer=json.loads(transport.read_exact(conn,size))
    assert answer['passed']and answer['hostPID']==38752 and host in transport.census_hosts()
    assert answer['actualNativeIdentity']['ProcessId']==47004 and answer['actualNativeIdentity']['ParentProcessId']==38752
    assert answer['actualNativeIdentity']not in transport.identity.census()
    answer.update(actualHostIdentity=host,identityRevalidatedBeforeAndAfter=True)
    print(json.dumps(answer),flush=True)


if __name__=='__main__':run()
