"""One unassisted private Sonya orb test, full guest/RGB retained in RAM.

Transport success does not accept gameplay/art/audio/cleanup. Observe the
same actual native PID to terminal; never restart on a host timeout/error.
"""
import argparse
import code
import gzip
import hashlib
import io
import json
import os
import re
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from PIL import Image

import qualify_native_sonya_orb_worker_lifetime as source
import native_process_census_v6647 as identity

ROOT=source.ROOT
NAME='diagnostic_native_sonya_orb_worker_lifetime'
LUA=ROOT/'mk2ks_native_sonya_orb_worker_wall.lua'
need,sha=source.need,source.sha


def expected(out):
    guard=json.loads((source.OUT/'report.json').read_text())
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    need(guard['passed'] and guard['sourceOnlyAccepted'] and not guard['nativeRuntimeAccepted'] and
         build['expected_guest_sha256']==guard['proposedGuestSHA256'] and
         not build['public_build_promoted'] and not build['native_runtime_accepted'], 'Exact source-only private built candidate')
    for receipt in (guard['inputHashes'],build['input_hashes']):
        need(all(sha(p)==h for p,h in receipt.items()), 'Every actual qualified/compiled input frozen')
    need(sha(ROOT/NAME/'mkport_candidate.exe')==build['executable_sha256'] and
         sha(ROOT/NAME/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256'], 'Actual compiled native executable and immutable payload')
    for leaf in ('restoration.json','cache_retirement.json'):
        need(json.loads((ROOT/NAME/leaf).read_text(encoding='utf-8-sig'))['passed'], 'Native compiler terminal; canonical files restored; generated cache retired')
    need(not (ROOT/'mame-mkp/build/mingw-gcc').exists(), 'No generated compiler cache retained')
    harness=json.loads(gzip.open(source.OUT/'executed_sources.json.gz','rt').read())['actualNewInitializerHarness']
    probe=out/'guest_expectation_probe.exe'
    compiled=subprocess.run([r'C:\Strawberry\c\bin\g++.exe','-std=c++17','-O1','-Wall','-Wextra','-Werror',
                             '-x','c++','-','-o',str(probe)],input=harness,text=True,capture_output=True)
    (out/'expectation_compiler.log').write_text(compiled.stdout+compiled.stderr)
    need(compiled.returncode==0, 'Actual frozen initialized-guest harness compiled warning-free')
    base=source.prior.prior.prior.prior.prior.visual.prior.expected();payload=source.prior.prior.prior.prior.prior.effects.PAYLOAD.read_bytes()
    result=subprocess.run([str(probe)],input=base+payload,capture_output=True)
    (out/'expectation_native_exit.json').write_text(json.dumps(dict(nativeExit=result.returncode,stdoutBytes=len(result.stdout),stderrBytes=len(result.stderr)),indent=2)+'\n')
    need(result.returncode==0 and len(result.stdout)==len(base) and
         hashlib.sha256(result.stdout).hexdigest().upper()==guard['proposedGuestSHA256'], 'Whole expected guest matches independently qualified source model')
    need(probe.parent.resolve()==out.resolve(), 'Exact generated expectation probe only');probe.unlink()
    return result.stdout,build


def serve(capture):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path=='/metadata':
                raw=json.dumps(dict(frames=[f['header'] for f in capture['rgbFrames']],errors=capture['errors'])).encode();kind='application/json'
            elif self.path.startswith('/frame/'):
                try:row=capture['rgbFrames'][int(self.path.rsplit('/',1)[1])]
                except (ValueError,IndexError):self.send_error(404);return
                head=row['header'];im=Image.frombytes('RGB',(int(head['width']),int(head['height'])),row['pixels'],'raw','BGRX')
                stream=io.BytesIO();im.save(stream,format='PNG');raw=stream.getvalue();kind='image/png'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server


def run(side):
    out=ROOT/f'audit_native_sonya_orb_worker_wall_p{side}'
    need(not out.exists() and not identity.census(), 'One fresh exact test; no native game live')
    controller=LUA.read_text()
    need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',controller), 'Physical buttons/passive observers only')
    out.mkdir();guest,build=expected(out)
    candidate=ROOT/NAME
    paths=[Path(__file__),LUA,Path(identity.__file__),Path(source.__file__),source.OUT/'report.json',
           candidate/'build-info.json',candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',
           ROOT/'roms/mk2.zip',ROOT/'roms/mk2ks.zip',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    pins={str(p.resolve()):sha(p) for p in paths}
    env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    env['MK2KS_ORB_SIDE']=str(side)
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
             '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat',
             '-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0','-nothrottle','-str','180',
             '-inipath',str(out),'-cfg_directory',str(out/'cfg'),'-nvram_directory',str(out/'nvram'),
             '-snapshot_directory',str(out/'snap'),'-autoboot_script',str(LUA)]
    capture=dict(rgbFrames=[],errors=[],guestCount=0,folder=out)
    with (out/'stderr.log').open('w',encoding='utf-8') as stderr:
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,text=True,
                                             encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        try:
            for _ in range(100):
                actual=next((item for item in identity.census() if item['ProcessId']==job.pid),None)
                if actual or job.poll()is not None:break
                time.sleep(.02)
            need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(), 'Actual native PID/parent/path/creation identity')
        except Exception as error:capture['errors'].append(dict(error=repr(error),stage='identity'))
        (out/'process.json').write_text(json.dumps(dict(pid=job.pid,command=command,actualWindowsIdentity=actual),indent=2)+'\n')
        print(json.dumps(dict(nativePID=job.pid,actualWindowsIdentity=actual)),flush=True)
        with gzip.open(out/'run.log.gz','wt',encoding='utf-8') as log:
            for line in job.stdout:
                try:
                    if ' hex='in line:
                        tag=line.split()[0];head=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(head.pop('hex'))
                        need(len(raw)==int(head['bytes']), 'Entire actual native declared buffer')
                        head['sha256']=hashlib.sha256(raw).hexdigest().upper()
                        if tag=='MK2_ORB_GUEST':
                            need(raw==guest, 'Every actual compiled initialized guest byte matches source qualification in RAM');capture['guestCount']+=1
                        elif tag=='MK2_ORB_RGB':
                            need(len(raw)==int(head['width'])*int(head['height'])*4, 'Whole actual native raster in RAM')
                            capture['rgbFrames'].append(dict(header=head,pixels=raw))
                        else:raise ValueError('Unexpected raw native block')
                        log.write(tag+'_DIGEST '+' '.join(k+'='+v for k,v in head.items())+'\n')
                    else:
                        log.write(line)
                        if line.startswith(('MK2_ORB_ENTRY ','MK2_ORB_COMMAND_READY ','MK2_ORB_WINNER ','MK2_ORB_STOP ','MK2_ORB_RESULT ','MK2_ORB_OVERRUN ')):
                            print(line.strip(),flush=True);log.flush()
                        if re.search(r'LUA ERROR|stack traceback|fatal error',line,re.I):print(line.strip(),flush=True)
                except Exception as error:capture['errors'].append(dict(error=repr(error),tag=line.split()[0] if line.strip() else 'empty'))
            exitcode=job.wait()
    capture['text']=gzip.open(out/'run.log.gz','rt').read()
    need(not any(item['ProcessId']==job.pid for item in identity.census()), 'Same native game handle actually terminal')
    need(all(sha(p)==h for p,h in pins.items()), 'Actual executed source/ROM/launcher inputs conserved')
    passed=exitcode==0 and capture['guestCount']==1 and not capture['errors'] and not (out/'stderr.log').read_text() and not re.search(r'LUA ERROR|stack traceback|fatal error',capture['text'],re.I)
    report=dict(passed=passed,transportOnlyAccepted=passed,finisherAccepted=False,fullPortAcceptance=False,nativeExit=exitcode,
                actualWindowsIdentity=actual,side=side,candidate=NAME,guestSHA256=build['expected_guest_sha256'],errors=capture['errors'],
                nativeRGBFrames=len(capture['rgbFrames']),wholeGuestMatched=capture['guestCount']==1,inputHashes=pins,
                newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,latestPlayableChanged=False,goalStatus='active')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    with gzip.open(out/'executed_sources.json.gz','wt',encoding='utf-8') as stream:
        json.dump({str(p.resolve()):dict(sha256=pins[str(p.resolve())],text=p.read_text()) for p in paths if p.suffix in ('.py','.lua')},stream)
    print(json.dumps(dict(transportPassed=passed,nativeExit=exitcode,frames=len(capture['rgbFrames']),errors=capture['errors'])),flush=True)
    return capture


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
    capture=run(args.side);server=serve(capture)
    print(json.dumps(dict(ramReviewPort=server.server_port,nativeHandleTerminal=True,frames=len(capture['rgbFrames']))),flush=True)
    code.interact(banner='Same native test is terminal; full real rasters retained in RAM.',local=dict(capture=capture,server=server))
