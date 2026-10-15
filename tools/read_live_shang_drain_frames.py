"""Receive exact existing native rasters from the SAME live Python host.

Uses CPython's supported remote diagnostic hook, never guest assistance.
Output JSON transports images in RAM to the calling tool; no image files.
"""
import inspect
import json
import re
import socket
import struct
import sys
from pathlib import Path

import native_process_census_v6647 as identity

ROOT=Path(__file__).resolve().parents[1]
REMOTE=ROOT/'tools/read_live_shang_drain_frames_remote.py'
OUT=ROOT/'audit_native_shang_owned_drain_campaign'


def read_exact(connection, count):
    data=bytearray()
    while len(data)<count:
        chunk=connection.recv(count-len(data))
        if not chunk:raise ValueError('Incomplete original diagnostic transport; no replay')
        data.extend(chunk)
    return bytes(data)


def census_hosts():
    source=inspect.getsource(identity.census)
    before="entry.szExeFile.lower()=='mkport_candidate.exe'"
    assert source.count(before)==1
    source=source.replace(before,"entry.szExeFile.lower() in ('mkport_candidate.exe','python.exe')")
    scope=dict(vars(identity))
    exec(compile(source,__file__+'::read_only_actual_host_and_child_identity','exec'),scope)
    return scope['census']()


def run():
    request=sys.argv[1:]
    assert len(request)<=2 and all(re.fullmatch(r'shang_(?:shrink_id(?:17|18)_age|victim_provenance_age)\d+\.png',n)for n in request)
    wanted=json.loads((OUT/'native_identity.json').read_text())
    records=census_hosts()
    assert wanted in records and wanted['ProcessId']==31336 and wanted['ParentProcessId']==30848
    host=next(r for r in records if r['ProcessId']==30848)
    assert host['ParentProcessId']==35304 and host['createdUnix']<wanted['createdUnix'] and wanted['createdUnix']-host['createdUnix']<60
    assert Path(host['ExecutablePath']).resolve()==Path(sys.executable).resolve()
    assert host['CommandLine']=='"'+sys.executable+'" -B tools/capture_native_shang_owned_drain_campaign.py'
    text=REMOTE.read_text()
    assert not re.search(r'write_[ui]\d+|:write_|set_value|clear_value|terminate\(|kill\(|load_?state',text)
    assert 'ram.clear' not in text and "open(" not in text
    with socket.socket() as server:
        server.bind(('127.0.0.1',51437));server.listen(1);server.settimeout(20)
        sys.remote_exec(host['ProcessId'],str(REMOTE))
        connection,_=server.accept()
        with connection:
            connection.settimeout(10)
            packet=json.dumps(request).encode()
            connection.sendall(struct.pack('<I',len(packet))+packet)
            size=struct.unpack('<I',read_exact(connection,4))[0]
            assert 0<size<5000000
            answer=json.loads(read_exact(connection,size))
    assert answer['passed'] and answer['hostPID']==host['ProcessId'] and answer['nativeIdentity']==wanted
    assert host in census_hosts() and wanted in identity.census()
    answer['actualHostIdentity']=host
    answer['originalIdentityRevalidatedBeforeAndAfter']=True
    print(json.dumps(answer),flush=True)


if __name__=='__main__':
    run()
