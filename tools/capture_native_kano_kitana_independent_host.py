"""Session-independent SAME full Kano policy with RAM-only raster review.

The earlier tool-owned host/native disappeared without a terminal receipt.
Preserve that partial chronology as incomplete, never an engine failure or
successful campaign. Launch this host with hidden Windows Start-Process.
"""
import argparse
import gzip
import hashlib
import inspect
import io
import json
import os
import secrets
import threading
import traceback
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from PIL import Image
import prepare_native_kano_kitana_reactive_campaign as previous
import native_process_census_v6647 as census

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_kano_kitana_reactive_independent'
SOURCE=ROOT/'audit_native_kano_kitana_reactive_independent_source'
INIT=ROOT/'audit_native_kano_kitana_reactive_independent_initializer'
OLD_INIT=ROOT/'audit_native_kano_kitana_reactive_independent_previous_initializer'
PRESERVED=ROOT/'audit_native_kano_kitana_reactive_interrupted_preserved'
HOST=ROOT/'audit_native_kano_kitana_reactive_independent_host'
RAM={}


def preserve_interruption():
    need(not census.census(),'Previous native is actually absent, never restart after a mere timeout')
    identity_path=previous.OUT/'native_identity.json'
    identity=json.loads(identity_path.read_text())
    need(identity['ProcessId']==176048 and identity['ParentProcessId']==75048 and
         not (previous.OUT/'native_terminal.json').exists()and not (previous.OUT/'result.json').exists(),
         'Exact interrupted producer, genuinely missing terminal/result; no guessed exit or gameplay verdict')
    proof=json.loads((previous.OUT/'guest_memory_proof.json').read_text())
    before=json.loads((previous.OUT/'input_hashes_before.json').read_text())
    need(proof['everyActualByteComparedInRAM']and proof['bytes']==1048576 and
         all(sha(p)==h for p,h in before.items()),'Whole actual guest proof and original input pins unchanged')
    if PRESERVED.exists():
        report=json.loads((PRESERVED/'report.json').read_text())
        need(all(sha(p)==h for p,h in report['inputHashes'].items()),'Original interruption record remains unchanged')
        return report
    PRESERVED.mkdir()
    with gzip.open(PRESERVED/'original_sources.json.gz','wt',encoding='utf-8')as stream:
        json.dump({p:dict(sha256=h,text=Path(p).read_text())for p,h in before.items()
            if Path(p).suffix.lower()in('.py','.lua','.cpp','.h','.cmd')},stream)
    bound=dict(before)
    bound.update({str(p.resolve()):sha(p)for p in previous.OUT.rglob('*')if p.is_file()})
    bound[str(PRESERVED/'original_sources.json.gz')]=sha(PRESERVED/'original_sources.json.gz')
    report=dict(passed=False,preservationPassed=True,interruptedNotQualified=True,
        exactOriginalIdentity=identity,nativeActuallyAbsent=True,toolSessionAlsoMissing=True,
        terminalExitCodeUnknown=True,interruptionCauseUnknown=True,gameplayFailureNotInferred=True,
        originalRAMNoLongerAccessible=True,visualAudioAcceptance=False,fullPortAcceptance=False,
        inputHashes=bound,goalStatus='active',newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0)
    (PRESERVED/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def functions(provider):
    scope=dict(vars(previous),__file__=__file__,OUT=OUT,RAM=RAM)
    exec(compile(inspect.getsource(previous.functions),__file__+'::whole_original_reactive_host_factory','exec'),scope)
    result,host=scope['functions'](provider)
    need(result['OUT']==OUT and result['LUA']==previous.LUA and result['CONTROLLERS']==previous.CONTROLLERS,
         'Identical whole physical controls, only independent host output changed')
    return result,host


def source_guard():
    old=previous.source_guard();saved=preserve_interruption()
    build=json.loads((ROOT/previous.original.repaired.NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    scope,host=functions(SimpleNamespace(GUEST_SHA=build['expected_guest_sha256'],
        EXE_SHA=build['executable_sha256'],PAYLOAD_SHA=build['payload_sha256']))
    report=dict(old,sessionIndependentHostPrepared=True,wholePythonHostCompiled=True,
        fullPhysicalPolicyUnchanged=True,hostSourceSHA256=hashlib.sha256(host.encode()).hexdigest().upper())
    report['inputHashes']=dict(old['inputHashes'])
    for p in (Path(__file__).resolve(),previous.SOURCE/'report.json',PRESERVED/'report.json'):
        report['inputHashes'][str(p)]=sha(p)
    need(saved['preservationPassed']and not saved['passed'],'Actual partial interruption preserved, never campaign credit')
    if SOURCE.exists():need(json.loads((SOURCE/'report.json').read_text())==report,'Independent host preflight stays frozen')
    else:SOURCE.mkdir();(SOURCE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def run():
    scope=dict(vars(previous),__file__=__file__,OUT=OUT,SOURCE=SOURCE,INIT=INIT,OLD_INIT=OLD_INIT,
        RAM=RAM,source_guard=source_guard,functions=functions)
    exec(compile(inspect.getsource(previous.run),__file__+'::whole_current_campaign_in_independent_host','exec'),scope)
    return scope['run']()


def review_server():
    token=secrets.token_hex(32)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/metadata':
                scope=RAM.get('scope',{});raws=scope.get('RAM_RAW',{})
                content=json.dumps(dict(hostPID=os.getpid(),nativeCensus=census.census(),
                    frames=[dict(filename=n,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
                        width=400,height=254)for n,raw in raws.items()],
                    nativeTerminalRecorded=(OUT/'native_terminal.json').exists(),fullPortAcceptance=False)).encode()
                kind='application/json'
            elif self.path.startswith('/frame/'):
                raws=RAM.get('scope',{}).get('RAM_RAW',{})
                try:name=list(raws)[int(self.path.rsplit('/',1)[1])];raw=raws[name]
                except (ValueError,IndexError):self.send_error(404);return
                need(len(raw)==400*254*4,'Actual whole native400x254 raster, no composed proxy image')
                image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')
                output=io.BytesIO();image.save(output,format='PNG');content=output.getvalue();kind='image/png'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',kind)
            self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
        def do_POST(self):
            if self.path!='/release' or self.headers.get('Authorization')!='Bearer '+token:
                self.send_error(403);return
            permission_path=OUT/'ram_release_authorization.json'
            if not permission_path.exists():self.send_error(409);return
            permission=json.loads(permission_path.read_text())
            native_path=OUT/'native_terminal.json'
            if not native_path.exists():self.send_error(409);return
            terminal=json.loads(native_path.read_text())
            need(permission['releaseAuthorized']and permission['exactHostPID']==os.getpid()and
                 permission['nativeTerminalSHA256']==sha(native_path)and
                 all(sha(p)==h for p,h in permission['inputHashes'].items())and
                 not any(q==terminal['identity']for q in census.census()),
                 'Original terminal and completed preservation/review bound before RAM release')
            scope=RAM.get('scope',{});raws=scope.get('RAM_RAW',{});images=scope.get('RAM_IMAGES',{})
            need(set(raws)==set(images),'Original raw/PIL buffer inventory')
            receipt=dict(released=True,hostPID=os.getpid(),rawBuffers=len(raws),pilBuffers=len(images),
                authorizationSHA256=sha(permission_path),nativeTerminalSHA256=sha(native_path),fullPortAcceptance=False)
            raws.clear();images.clear();RAM.clear()
            (OUT/'ram_buffers_released.json').write_text(json.dumps(receipt,indent=2)+'\n')
            self.send_response(200);self.end_headers()
            threading.Thread(target=self.server.shutdown,daemon=True).start()
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    HOST.mkdir(exist_ok=True)
    (HOST/'review_session.json').write_text(json.dumps(dict(hostPID=os.getpid(),port=server.server_port,
        releaseToken=token,source=str(Path(__file__).resolve()),sourceSHA256=sha(__file__)),indent=2)+'\n')
    return server


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-only',action='store_true');args=parser.parse_args()
    if args.source_only:
        source_guard();print(json.dumps(dict(passed=True,sourceOnlyAccepted=True,wholePythonHostCompiled=True,
            physicalPolicyUnchanged=True,newNativeBoots=0,fullPortAcceptance=False)),flush=True)
    else:
        server=review_server()
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:run()
        except Exception as error:
            folder=OUT if OUT.exists()else(INIT if INIT.exists()else SOURCE)
            failure=folder/'current_capture_failure.json'
            if folder.exists()and not failure.exists():
                failure.write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                    fullPortAcceptance=False),indent=2)+'\n')
            print(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc())),flush=True)
        server_thread=next((t for t in threading.enumerate()if t is not threading.current_thread()and t.is_alive()),None)
        if server_thread:server_thread.join()
        server.server_close()
