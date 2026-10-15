"""Native current selector/transition/names in both slots; no new game build.

Four original input-controller cases, with delayed confirmation solely to see
complete native blinking phases. Independent cfg/NVRAM, original ROM hardlinks,
no persistent raw media. The separate full campaign is never touched/restarted.
"""
import code
import gzip
import hashlib
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
from PIL import Image
import verify_native_shang_drain_anchors_startup as startup

ROOT,NAME= startup.ROOT,startup.NAME
OUT=ROOT/'audit_native_anchor_ui_ram'
INIT=ROOT/'audit_native_anchor_ui_ram_initializer'
LUA=ROOT/'mk2ks_native_anchor_ui_ram.lua'
RAM={}
need,sha,digest=startup.initial.need,startup.initial.sha,startup.initial.digest
FIELDS=re.compile(r'(\w+)=([^\s]+)')

def run():
    need(not OUT.exists() and not INIT.exists(),'Fresh bounded physical UI regression')
    concurrent=json.loads((ROOT/'audit_native_shang_drain_anchors_campaign/native_identity.json').read_text())
    need(startup.initial.identity.census()==[concurrent], 'Exact already-running independent campaign, no unknown native games')
    candidate=ROOT/NAME;meta_path=candidate/'build-info.json'
    meta=json.loads(meta_path.read_text(encoding='utf-8-sig'))
    cold=json.loads((startup.OUT/'report.json').read_text())
    need(cold['passed'] and cold['actualNativeInitializedWindowsAccepted'] and
         sha(candidate/'mkport_candidate.exe')==meta['executable_sha256'],'Actual qualified current executable')
    controllers=[LUA,ROOT/'mk2ks_selector_exit_test.lua',ROOT/'mk2ks_native_shang_morph.lua',startup.initial.LUA]
    for path in controllers:
        need(not re.search(r':write_|write_[ui]\d+|\.value\s*=(?!=)|load_?state|plugin\.cheat|return\s+data',path.read_text()),
             'Every actual loaded controller is physical-input/passive-read only')
    pins={str(p.resolve()):sha(p)for p in (Path(__file__),Path(startup.__file__),meta_path,*controllers)}
    for proof in (cold,):
        for p,h in proof['inputHashes'].items():need(sha(p)==h,'Every frozen original startup input');pins[p]=h
    INIT.mkdir();wanted=startup.expected(INIT)
    need({k:digest(v)for k,v in wanted.items()}==cold['actualWindowHashes'],'All complete independent initialized models')
    OUT.mkdir();RAM.update(wanted=wanted,pins=pins,concurrent=concurrent,cases={})
    for p1,p2,two in (('kano','sonya',True),('sonya','kano',True),('kano','stock',False),('sonya','stock',False)):
        case=f'{p1}_p1_{p2}_p2_'+('two'if two else'ladder')
        folder=OUT/case;folder.mkdir()
        env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
        env.update(MK2KS_TEST_FIGHTER=p1,MK2KS_P2_FIGHTER=p2,MK2KS_TWO_PLAYER='1'if two else'0',
            MK2KS_TEST_CONFIRM='lp',MK2KS_TEST_CONFIRM_AT_AGE='370',MK2KS_TRACE_CURSOR_LONG='1',
            MK2KS_ASSERT_NATIVE_DISPLAY='1',MK2KS_ASSERT_HUD_SHADOW='1',MK2KS_ALLOW_NATURAL_LOSS='1')
        command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
            '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat',
            '-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','65',
            '-snapsize','400x254','-inipath',str(folder),'-cfg_directory',str(folder/'cfg'),
            '-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
            '-autoboot_delay','0','-autoboot_script',str(LUA)]
        captured=dict(images=[],text=[],errors=[],windowProof=False)
        RAM['cases'][case]=captured
        buffers={k:bytearray()for k in wanted}
        with (folder/'stderr.log').open('w',encoding='utf-8')as stderr:
            born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,
                text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
            captured.update(process=job,command=command)
            actual=None
            for _ in range(100):
                actual=next((p for p in startup.initial.identity.census()if p['ProcessId']==job.pid),None)
                if actual or job.poll()is not None:break
                time.sleep(.01)
            need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve() and
                 actual['CommandLine']==subprocess.list2cmdline(command),'Exact new native PID/birth/path/parent/full command')
            captured['identity']=actual
            (folder/'process.json').write_text(json.dumps(actual,indent=2)+'\n')
            print(json.dumps(dict(case=case,nativePID=job.pid,hostPID=os.getpid(),identityVerified=True)),flush=True)
            with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
                for line in job.stdout:
                    try:
                        if line.startswith('MK2_DRAIN_STARTUP '):
                            head,hexdata=line.strip().split(' hex=',1);row=dict(FIELDS.findall(head));raw=bytes.fromhex(hexdata)
                            kind=row['kind'];need(kind in buffers and int(row['offset'])==len(buffers[kind]) and len(raw)==int(row['bytes']),
                                'Every actual initialized chunk contiguous/complete')
                            buffers[kind].extend(raw)
                            log.write(head+' sha256='+digest(raw)+'\n')
                        elif line.startswith('MK2_DRAIN_STARTUP_COMPLETE '):
                            need({k:bytes(v)for k,v in buffers.items()}==wanted,'Actual all three full native initialized windows in THIS case')
                            captured['windowProof']=True;buffers.clear();log.write(line)
                        elif line.startswith('MK2_ANCHOR_UI_FRAME '):
                            head,hexdata=line.strip().split(' hex=',1);row=dict(FIELDS.findall(head));raw=bytes.fromhex(hexdata)
                            need(row['writes']=='0' and row['assistance']=='none' and len(raw)==406400 and len(captured['images'])<80,
                                'Bounded complete native raster, no assistance')
                            image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX')
                            captured['images'].append(dict(header=row,raw=raw,image=image,SHA256=digest(raw)))
                            log.write(head+' sha256='+digest(raw)+'\n')
                        else:
                            log.write(line);captured['text'].append(line)
                    except Exception as error:captured['errors'].append(dict(error=repr(error),tag=line.split()[0]if line.strip()else'empty'))
                exitcode=job.wait()
        need(exitcode==0 and not(folder/'stderr.log').read_text() and captured['windowProof'] and not captured['errors'],
             'Actual native terminal/complete initialization/raster transport clean; not visual acceptance')
        need(not any(p['ProcessId']==job.pid and p['createdUnix']==actual['createdUnix']for p in startup.initial.identity.census()),
             'Exact original case handle terminal; no replacements')
        results=[line.strip()for line in captured['text']if line.startswith(('MK2KS_EXIT_RESULT ','MK2KS_SELECTION_RESULT ',
            'MK2KS_HUD_SHADOW_RESULT ','MK2KS_NATIVE_RESULT ','MK2KS_STABILITY ','MK2KS_DISPLAY_RESULT '))]
        report=dict(passed=True,transportOnly=True,nativeExit=exitcode,case=case,actualNativeIdentity=actual,
            actualInitializedWindowHashes={k:digest(v)for k,v in wanted.items()},nativeControllerResults=results,
            actualNativeRasters=[dict(header=f['header'],SHA256=f['SHA256'])for f in captured['images']],
            visualSelectionAccepted=False,artAccepted=False,audioAccepted=False,fullPortAcceptance=False,
            concurrentCampaignNotMutated=True,newBuilds=0,newROMCopies=0,newRawMediaFiles=0,newZIPs=0)
        (folder/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        captured['report']=report
        print(json.dumps(dict(case=case,nativeExit=exitcode,frames=len(captured['images']),results=results)),flush=True)
        need(concurrent in startup.initial.identity.census(),'Same original independent full campaign remains live')
    need(all(sha(p)==h for p,h in pins.items()),'All inputs unchanged through four native cases')
    (OUT/'input_hashes.json').write_text(json.dumps(pins,indent=2)+'\n')
    print(json.dumps(dict(passed=True,transportOnly=True,cases=4,visualReviewRequired=True,fullPortAcceptance=False)),flush=True)

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';need(not path.exists(),'Preserve original UI failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Native UI cases retained in RAM; inspect exact phases/results before accepting.',local=dict(RAM=RAM))
