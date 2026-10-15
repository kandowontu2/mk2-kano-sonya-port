"""Exact host/process identity and current volatile collector progress only."""
import json,socket,struct,sys
from pathlib import Path
import read_live_shang_drain_frames as transport
host=next(r for r in transport.census_hosts() if r['ProcessId']==38752)
assert (host['ParentProcessId'],host['createdUnix'])==(40316,1791734919.6266766)
assert Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()
with socket.socket() as server:
    server.bind(('127.0.0.1',51461));server.listen(1);server.settimeout(20)
    sys.remote_exec(38752,str(transport.ROOT/'tools/read_native_selector_lowkick_live_remote.py'))
    conn,_=server.accept()
    with conn:
        conn.settimeout(10)
        size=struct.unpack('<I',transport.read_exact(conn,4))[0];assert 0<size<10000
        answer=json.loads(transport.read_exact(conn,size))
assert answer['passed'] and answer['hostPID']==38752 and host in transport.census_hosts()
native=answer['actualNativeIdentity']
if answer['nativeExit'] is None:assert native in transport.identity.census()
else:assert native not in transport.identity.census()
answer.update(actualHostIdentity=host,identityRevalidatedBeforeAndAfter=True)
print(json.dumps(answer),flush=True)
