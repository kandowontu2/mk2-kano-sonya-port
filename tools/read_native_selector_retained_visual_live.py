"""Receive selected actual frames in memory, never write PNGs."""
import json,socket,struct,sys
import read_live_shang_drain_frames as transport
host=next(r for r in transport.census_hosts() if r['ProcessId']==5752)
assert host['ParentProcessId']==19028
with socket.socket() as server:
    server.bind(('127.0.0.1',51464));server.listen(1);server.settimeout(20)
    sys.remote_exec(5752,str(transport.ROOT/'tools/read_native_selector_retained_visual_remote.py'))
    conn,_=server.accept()
    with conn:
        conn.settimeout(10);size=struct.unpack('<I',transport.read_exact(conn,4))[0]
        assert 0<size<1000000
        result=json.loads(transport.read_exact(conn,size))
assert result['passed'] and result['hostPID']==5752 and host in transport.census_hosts()
print(json.dumps(result),flush=True)
