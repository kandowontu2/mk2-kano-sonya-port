"""Save exact passive current anchoring evidence, no native launch or writes."""
import json,socket,struct,sys
from pathlib import Path
import read_live_shang_drain_frames as transport
import verify_native_source_sync as sync
OUT=transport.ROOT/'audit_native_selector_retained_ground_anchors_checked'
assert not OUT.exists()
host=next(r for r in transport.census_hosts() if r['ProcessId']==5752)
assert host['ParentProcessId']==19028
with socket.socket() as server:
    server.bind(('127.0.0.1',51465));server.listen(1);server.settimeout(20)
    sys.remote_exec(5752,str(transport.ROOT/'tools/read_native_selector_ground_anchor_remote.py'))
    conn,_=server.accept()
    with conn:
        conn.settimeout(10);size=struct.unpack('<I',transport.read_exact(conn,4))[0];assert 0<size<10000
        report=json.loads(transport.read_exact(conn,size))
assert host in transport.census_hosts()
pins={}
for p in (Path(__file__),transport.ROOT/'tools/read_native_selector_ground_anchor_remote.py',
          transport.ROOT/'audit_native_selector_fresh_lowkick_controls_checked/report.json',
          transport.ROOT/'mame-mkp/src/mame/midway/midtunit_m.cpp'):
    pins[str(p.resolve())]=sync.sha(p)
report.update(inputHashes=pins,currentSourceSync=sync.verify(),identityRevalidatedBeforeAndAfter=True)
OUT.mkdir();(OUT/('report.json' if report['passed'] else 'failure.json')).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('inputHashes','currentSourceSync','nativeIdentity')}),flush=True)
