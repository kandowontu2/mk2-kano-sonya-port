"""Real two-human native Sub-Zero commands; no health/state/RNG assistance."""
import argparse, hashlib, json, os, re, subprocess, traceback
from pathlib import Path
import run_native_subzero_offset_regression_v4856 as native

ROOT,need,sha=native.ROOT,native.need,native.sha
LUA='mk2ks_earned_subzero_victims_v4870.lua'
NAME=native.NAME

def capture(fighter,side):
    folder=ROOT/f'audit_v4872_subzero_{fighter}_p{side}_earned'
    need(not folder.exists(),'Fresh actual earned case; never restart an executed leaf')
    guest=native.expected()
    build=json.loads((ROOT/NAME/'build-info.json').read_text(encoding='utf-8-sig'))
    pins=dict(build['input_hashes'])
    for path in(ROOT/NAME/'build-info.json',ROOT/NAME/'mkport_candidate.exe',ROOT/NAME/'roms/mk2ks/mk2ks.mdata',
                ROOT/LUA,ROOT/'mk2ks_stock_fatality_v1021.lua',Path(__file__).resolve()):
        pins[str(path.resolve())]=sha(path)
    need(sha(ROOT/NAME/'mkport_candidate.exe')==native.EXE_SHA and all(sha(p)==h for p,h in pins.items()),
         'Exact tested native table-fix binary and every source unchanged')
    text=(ROOT/LUA).read_text()+(ROOT/'mk2ks_stock_fatality_v1021.lua').read_text()
    need(not re.search(r'(?:write_u|write_i|write_direct|write_logical|\.value\s*=(?!=))',text),
         'Physical buttons only; no native guest or register assignment')
    folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Compressed before output')
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',
               MK2KS_STOCK_COMMAND='fdf_hp',MK2KS_STOCK_GAP='168')
    command=[str(ROOT/NAME/'mkport_candidate.exe'),'mk2ks','-rompath',str(ROOT/NAME/'roms')+';'+str(ROOT/'roms'),
        '-samplepath',str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000',
        '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none',
        '-noautoframeskip','-frameskip','0','-nothrottle','-str','130',
        '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
        '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(ROOT/LUA)]
    guest_proof=None
    with (folder/'stderr.log').open('w',encoding='utf-8')as errors, subprocess.Popen(command,cwd=ROOT,env=env,
            stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8',errors='strict')as process:
        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command,environmentPolicy=env['MK2KS_STOCK_COMMAND']),indent=2)+'\n')
        print(f'{fighter} P{side} physical Sub-Zero case started pid={process.pid}',flush=True)
        with (folder/'run.log').open('w',encoding='utf-8')as log:
            for line in process.stdout:
                if line.startswith('MK2_EARNED_SUBZERO_GUEST '):
                    fields=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(fields.pop('hex'))
                    need(guest_proof is None and fields==dict(frame='1',bytes='1048576') and raw==guest,
                         'Every actual cold initialized guest byte independently compared in RAM')
                    guest_proof=dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest().upper(),
                        everyActualByteComparedInRAM=True,executableSHA256=native.EXE_SHA,rawGuestFilesWritten=0)
                    (folder/'guest_memory_proof.json').write_text(json.dumps(guest_proof,indent=2)+'\n')
                    log.write('MK2_EARNED_SUBZERO_GUEST_DIGEST frame=1 bytes=1048576 sha256='+guest_proof['sha256']+'\n')
                else:
                    need('hex='not in line,'Never persist raw guest/encoded media')
                    log.write(line)
                    if re.search(r'_(ACTION|DEEP_TASK|BODY_LOOKUP|UPPERCUT_BEGIN|HOST_EXIT|RESULT) ',line):
                        print(line.strip(),flush=True);log.flush()
        code=process.wait()
    need(all(sha(p)==h for p,h in pins.items()),'Every actual executed source/native input unchanged')
    log=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',line),tag=line.split()[0])for line in log.splitlines()
          if line.startswith('MK2_EARNED_SUBZERO_') and 'GUEST_DIGEST'not in line]
    summary=dict(nativeExit=code,fullGuestComparedInRAM=bool(guest_proof),guestSHA256=guest_proof['sha256']if guest_proof else None,
        actionRows=[r for r in rows if r['tag'].endswith(('DEEP_TASK','BODY_LOOKUP','HOST_EXIT','RESULT'))],
        nativeCacheOverrunObserved='CACHE_OVERWRITE 'in log,rawMediaGuestFilesWritten=0,fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(dict(summary,inputHashes=pins),indent=2)+'\n')
    need(code==0 and guest_proof and not re.search(r'LUA ERROR|stack traceback|fatal error|access violation',log+errors,re.I),
         'Actual successful native transport and callbacks')
    need(any(r['tag'].endswith('DEEP_TASK')for r in rows),'Actual original native0616 victim task required, not ordinary combat')
    need(any(r['tag'].endswith('BODY_LOOKUP')for r in rows),'Actual original native frozen body lookup required')
    need(not summary['nativeCacheOverrunObserved'],'No native group-cache global overwrite')
    summary['passed']=True
    return summary

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));parser.add_argument('--side',required=True,type=int,choices=(1,2));args=parser.parse_args()
    out=ROOT/f'audit_v4873_subzero_{args.fighter}_p{args.side}_earned_observed'
    need(not out.exists(),'Fresh immutable terminal report')
    try:report=capture(args.fighter,args.side)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before report')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
