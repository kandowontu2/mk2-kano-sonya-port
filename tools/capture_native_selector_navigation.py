"""Four physical native walks cover all56 directional edges for BOTH slots.

Fresh cfg/NVRAM per walk; bounded rasters are RAM-only. Full initialized guest,
owned data and reserved graphics are compared byte-for-byte to independent
models before interpreting any navigation. Original process handles are kept.
"""
import code,gzip,json,os,re,subprocess,time,traceback
from pathlib import Path
from PIL import Image
import verify_native_selector_layers_startup as startup
import selector_navigation_contract as contract

ROOT,NAME=startup.ROOT,startup.NAME
OUT=ROOT/'audit_native_selector_navigation'
INIT=ROOT/'audit_native_selector_navigation_initializer'
LUA=ROOT/'mk2ks_native_selector_navigation.lua'
RAM={}
need,sha,digest=startup.initial.need,startup.initial.sha,startup.initial.digest
FIELDS=re.compile(r'(\w+)=([^\s]+)')


def run():
    need(not OUT.exists()and not INIT.exists()and not startup.initial.identity.census(),'Fresh scope; no unknown original native games')
    candidate=ROOT/NAME;meta_path=candidate/'build-info.json'
    meta=json.loads(meta_path.read_text(encoding='utf-8-sig'))
    cold_path=startup.OUT/'report.json';cold=json.loads(cold_path.read_text())
    need(cold['passed']and cold['actualNativeInitializedWindowsAccepted']and sha(candidate/'mkport_candidate.exe')==meta['executable_sha256'],
         'Actual fully initialized qualified private executable')
    restoration=json.loads((candidate/'restoration.json').read_text(encoding='utf-8-sig'))
    need(restoration['passed']and all(sha(p)==h for p,h in restoration['restored_actual_preexisting_files'].items())and
         not(ROOT/'mame-mkp/build/mingw-gcc').exists(),'Actual dirty canonical files restored; generated compiler cache absent')
    paths=(Path(__file__),Path(contract.__file__),Path(startup.__file__),LUA,startup.initial.LUA,meta_path,cold_path,
           candidate/'mkport_candidate.exe',ROOT/'PLAY_LATEST_KANO_SONYA.cmd')
    pins={str(p.resolve()):sha(p)for p in paths}
    for path in (LUA,startup.initial.LUA):
        need(not re.search(r':write_|write_[ui]\d+|\.value\s*=(?!=)|load_?state|plugin\.cheat|return\s+data',path.read_text()),'Actual loaded controllers only physical input/passive reads')
    for p,h in cold['inputHashes'].items():need(sha(p)==h,'Every frozen startup input unchanged');pins[p]=h
    INIT.mkdir();wanted=startup.expected(INIT)
    need({k:digest(v)for k,v in wanted.items()}==cold['actualWindowHashes'],'Independent complete initialized models')
    OUT.mkdir();RAM.update(wanted=wanted,pins=pins,cases={})
    for direction in contract.DIRECTIONS:
        need(not startup.initial.identity.census(),'Previous original native handle actually terminal before next distinct edge walk')
        folder=OUT/direction;folder.mkdir()
        plans={side:contract.plan(start,direction)for side,start in ((1,1),(2,9))}
        need(max(len(p)for p in plans.values())*12+93<800,'Physical walks bounded within normal selection timer')
        (folder/'physical-input-plan.json').write_text(json.dumps(plans,indent=2)+'\n')
        pins[str((folder/'physical-input-plan.json').resolve())]=sha(folder/'physical-input-plan.json')
        env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
        env.update(MK2KS_NAV_DIRECTION=direction,MK2KS_NAV_P1=contract.lua_plan(plans[1]),MK2KS_NAV_P2=contract.lua_plan(plans[2]))
        command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
            '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat','-video','none','-sound','none',
            '-noautoframeskip','-frameskip','0','-nothrottle','-str','65','-snapsize','400x254','-inipath',str(folder),
            '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
            '-autoboot_delay','0','-autoboot_script',str(LUA)]
        captured=dict(plans=plans,images=[],text=[],errors=[],windowProof=False,command=command)
        RAM['cases'][direction]=captured;buffers={k:bytearray()for k in wanted}
        with(folder/'stderr.log').open('w',encoding='utf-8')as stderr:
            born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,
                text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
            captured['process']=job;actual=None
            for _ in range(100):
                actual=next((p for p in startup.initial.identity.census()if p['ProcessId']==job.pid),None)
                if actual or job.poll()is not None:break
                time.sleep(.01)
            need(actual and actual['ParentProcessId']==os.getpid()and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve()and
                 actual['CommandLine']==subprocess.list2cmdline(command),'Exact actual original native process birth/parent/path/full command')
            captured['identity']=actual
            (folder/'process.json').write_text(json.dumps(actual,indent=2)+'\n')
            print(json.dumps(dict(direction=direction,nativePID=job.pid,hostPID=os.getpid(),actualIdentityVerified=True)),flush=True)
            with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
                for line in job.stdout:
                    try:
                        if line.startswith('MK2_DRAIN_STARTUP '):
                            head,hexdata=line.strip().split(' hex=',1);row=dict(FIELDS.findall(head));raw=bytes.fromhex(hexdata);kind=row['kind']
                            need(kind in buffers and int(row['offset'])==len(buffers[kind])and len(raw)==int(row['bytes'])and
                                 int(row['start'],16)==(0x1fb0000 if kind=='graphics'else 0)and row['writes']=='0'and row['assistance']=='none',
                                 'All complete actual initialized chunks')
                            buffers[kind].extend(raw);log.write(head+' sha256='+digest(raw)+'\n')
                        elif line.startswith('MK2_DRAIN_STARTUP_COMPLETE '):
                            need({k:bytes(v)for k,v in buffers.items()}==wanted,'Entire actual guest/owned/newGFX equal independent models in THIS native walk')
                            captured['windowProof']=True;buffers.clear();log.write(line)
                        elif line.startswith('MK2_NAV_FRAME '):
                            head,hexdata=line.strip().split(' hex=',1);row=dict(FIELDS.findall(head));raw=bytes.fromhex(hexdata)
                            need(row['writes']=='0'and row['assistance']=='none'and len(raw)==406400 and len(captured['images'])<40,'Bounded unassisted actual scanout')
                            im=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')
                            captured['images'].append(dict(header=row,raw=raw,image=im,SHA256=digest(raw)))
                            log.write(head+' sha256='+digest(raw)+'\n')
                        else:
                            captured['text'].append(line);log.write(line)
                            if line.startswith(('MK2_NAV_LIVE ','MK2_NAV_RESULT ')):print(line.strip(),flush=True)
                    except Exception as error:captured['errors'].append(dict(error=repr(error),tag=line.split()[0]if line.strip()else'empty'))
                exitcode=job.wait()
        terminal=dict(nativeExit=exitcode,exactNativeAbsent=actual not in startup.initial.identity.census())
        captured['terminal']=terminal;(folder/'terminal.json').write_text(json.dumps(terminal,indent=2)+'\n')
        need(exitcode==0 and terminal['exactNativeAbsent']and not(folder/'stderr.log').read_text()and captured['windowProof']and not captured['errors'],
             'Original native handle clean actual terminal and full passive transport')
        results=[s.strip()for s in captured['text']if s.startswith('MK2_NAV_RESULT ')]
        report=dict(passed=True,transportOnly=True,direction=direction,nativeExit=exitcode,actualNativeIdentity=actual,
            initializedWindowHashes={k:digest(v)for k,v in wanted.items()},nativeResults=results,
            actualNativeRasters=[dict(header=f['header'],SHA256=f['SHA256'])for f in captured['images']],
            fullNavigationAccepted=False,visualAccepted=False,audioAccepted=False,fullPortAcceptance=False,
            newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0,publicPlayableChanged=False)
        captured['report']=report;(folder/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        need(len(results)==1 and 'pass=true 'in results[0],'Original physical-walk predicate; preserve native failures, do not continue blindly')
    need(all(sha(p)==h for p,h in pins.items()),'All frozen inputs and public playable unchanged')
    (OUT/'input_hashes.json').write_text(json.dumps(pins,indent=2)+'\n')
    print(json.dumps(dict(passed=True,transportOnly=True,nativeWalks=4,fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';need(not path.exists(),'Preserve actual original failure');path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Original navigation handles and native rasters retained; no timeout replays.',local=dict(RAM=RAM))
