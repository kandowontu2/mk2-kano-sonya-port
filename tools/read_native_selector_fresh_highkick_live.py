"""Original host/process identities before and after passive counter observation."""
import json,socket,struct,sys
from pathlib import Path
import read_live_shang_drain_frames as transport

host=next(r for r in transport.census_hosts() if r['ProcessId']==5752)
assert host['ParentProcessId']==19028 and 'recover_native_selector_models_after_host_exit.py' in host['CommandLine']
assert Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()
with socket.socket() as server:
    server.bind(('127.0.0.1',51463)); server.listen(1); server.settimeout(20)
    sys.remote_exec(5752,str(transport.ROOT/'tools/read_native_selector_fresh_highkick_remote.py'))
    conn,_=server.accept()
    with conn:
        conn.settimeout(10); size=struct.unpack('<I',transport.read_exact(conn,4))[0]
        assert 0<size<10000
        answer=json.loads(transport.read_exact(conn,size))
assert answer['passed'] and answer['hostPID']==5752 and host in transport.census_hosts()
native=answer['actualNativeIdentity']
assert (native['ProcessId'],native['ParentProcessId'],native['createdUnix'])==(3152,5752,1791816393.9003582)
assert (native in transport.identity.census())==(answer['nativeExit'] is None)
answer.update(identityRevalidatedBeforeAndAfter=True)
print(json.dumps(answer),flush=True)
