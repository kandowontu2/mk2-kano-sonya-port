"""Bound exact existing UI-host identity and receive volatile native raster sheet."""
import json,socket,struct,sys
from pathlib import Path
import read_live_shang_drain_frames as transport

def run():
    profile,case,*indices=sys.argv[1:]
    profile_records={'delayed':(27800,29688,1791726178.3294525,'capture_native_anchor_ui_ram.py'),
                     'standard':(12004,16360,1791726301.6143703,'capture_native_anchor_ui_standard_ram.py')}
    pid,parent,birth,script=profile_records[profile]
    host=next(p for p in transport.census_hosts()if p['ProcessId']==pid)
    assert host['ParentProcessId']==parent and host['createdUnix']==birth
    assert Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()
    assert host['CommandLine']=='"'+sys.executable+'" -B tools/'+script
    assert case in ('kano_p1_sonya_p2_two','sonya_p1_kano_p2_two','kano_p1_stock_p2_ladder','sonya_p1_stock_p2_ladder')
    indices=[int(n)for n in indices];assert len(indices)<=6 and all(0<=n<80 for n in indices)
    remote=transport.ROOT/'tools/read_native_anchor_ui_remote.py'
    with socket.socket()as server:
        server.bind(('127.0.0.1',51438));server.listen(1);server.settimeout(20)
        sys.remote_exec(pid,str(remote))
        conn,_=server.accept()
        with conn:
            conn.settimeout(10)
            packet=json.dumps(dict(profile=profile,case=case,indices=indices)).encode()
            conn.sendall(struct.pack('<I',len(packet))+packet)
            size=struct.unpack('<I',transport.read_exact(conn,4))[0];assert 0<size<5000000
            answer=json.loads(transport.read_exact(conn,size))
    assert answer['passed'] and answer['hostPID']==pid and host in transport.census_hosts()
    native=answer['actualNativeIdentity']
    assert native['ParentProcessId']==pid and native not in transport.identity.census()
    answer.update(profile=profile,case=case,actualHostIdentity=host,identityRevalidatedBeforeAndAfter=True)
    print(json.dumps(answer),flush=True)

if __name__=='__main__':run()
