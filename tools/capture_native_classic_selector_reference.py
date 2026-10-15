"""Unmodified stock MK2 driver/whole original program; original physical selector."""
import code,gzip,json,os,re,subprocess,time,traceback
from pathlib import Path
from PIL import Image
import native_process_census_v6647 as census
import verify_native_selector_layers_startup as current

ROOT=current.ROOT
OUT=ROOT/'audit_native_classic_selector_reference'
LUA=ROOT/'mk2_native_classic_selector_reference.lua'
RAM={}
need,sha,digest=current.initial.need,current.initial.sha,current.initial.digest
FIELDS=re.compile(r'(\w+)=([^\s]+)')

def run():
    need(not OUT.exists() and not census.census(),'One fresh original stock reference, other native games terminal')
    candidate=ROOT/current.NAME
    cold=json.loads((current.OUT/'report.json').read_text())
    need(cold['passed'] and sha(candidate/'mkport_candidate.exe')==cold['actualCompiledExecutableSHA256'],'Actual qualified executable, unmodified mk2 driver requested')
    stock=ROOT/'mk2/mk2-maincpu.bin';wanted=stock.read_bytes()
    need(len(wanted)==0x100000 and digest(wanted)=='45B3285496DB555EFAF4A3608A4F59845DD47A82E4A0593607E0592F47B36F23','Entire original stock game program')
    paths=[Path(__file__),LUA,ROOT/'mk2ks_native_anchor_ui_ram.lua',ROOT/'mk2ks_selector_exit_test.lua',stock,candidate/'mkport_candidate.exe',ROOT/'roms/mk2.zip']
    for p in paths[:4]:need(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)|plugin\.cheat',p.read_text()),'Actual loaded inputs and passive observers only')
    pins={str(p.resolve()):sha(p)for p in paths};OUT.mkdir()
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    env.update(MK2KS_TEST_FIGHTER='liu_kang',MK2KS_P2_FIGHTER='stock',MK2KS_TWO_PLAYER='0',MK2KS_TEST_CONFIRM='lp',MK2KS_TEST_CONFIRM_AT_AGE='96',MK2KS_TRACE_CURSOR_LONG='1',MK2KS_ALLOW_NATURAL_LOSS='1')
    command=[str(candidate/'mkport_candidate.exe'),'mk2','-rompath',str(ROOT/'roms'),'-skip_gameinfo','-nocheat','-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','65','-snapsize','400x254','-inipath',str(OUT),'-cfg_directory',str(OUT/'cfg'),'-nvram_directory',str(OUT/'nvram'),'-snapshot_directory',str(OUT/'snap'),'-autoboot_delay','0','-autoboot_script',str(LUA)]
    with (OUT/'stderr.log').open('w',encoding='utf-8')as stderr:
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
        RAM.update(process=job,command=command,pins=pins,images=[],text=[],errors=[])
        actual=None
        for _ in range(100):
            actual=next((p for p in census.census()if p['ProcessId']==job.pid),None)
            if actual or job.poll()is not None:break
            time.sleep(.01)
        need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and actual['CommandLine']==subprocess.list2cmdline(command) and Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),'Exact original stock native PID/birth/path/parent/full command')
        RAM['identity']=actual;(OUT/'process.json').write_text(json.dumps(actual,indent=2)+'\n')
        print(json.dumps(dict(stockNativePID=job.pid,hostPID=os.getpid(),driver='mk2',identityVerified=True)),flush=True)
        high=bytearray();complete=False
        with gzip.open(OUT/'run.log.gz','wt',encoding='utf-8')as log:
            for line in job.stdout:
                try:
                    if line.startswith('MK2_CLASSIC_STARTUP '):
                        head,hexdata=line.strip().split(' hex=',1);row=dict(FIELDS.findall(head));raw=bytes.fromhex(hexdata)
                        need(int(row['offset'])==len(high) and len(raw)==int(row['bytes'])==4096 and row['writes']=='0' and row['assistance']=='none','Whole stock native program contiguous chunks')
                        high.extend(raw);log.write(head+' sha256='+digest(raw)+'\n')
                    elif line.startswith('MK2_CLASSIC_STARTUP_COMPLETE '):
                        need(not complete and bytes(high)==wanted,'THIS actual game uses EVERY byte of original unmodified MK2 program')
                        complete=True;high.clear();log.write(line)
                    elif line.startswith('MK2_ANCHOR_UI_FRAME '):
                        head,hexdata=line.strip().split(' hex=',1);row=dict(FIELDS.findall(head));raw=bytes.fromhex(hexdata)
                        need(len(raw)==406400 and row['writes']=='0' and row['assistance']=='none' and len(RAM['images'])<80,'Bounded actual original stock native scanout')
                        RAM['images'].append(dict(header=row,raw=raw,image=Image.frombytes('RGB',(400,254),raw,'raw','BGRX'),SHA256=digest(raw)))
                        log.write(head+' sha256='+digest(raw)+'\n')
                    else:log.write(line);RAM['text'].append(line)
                except Exception as error:RAM['errors'].append(dict(error=repr(error),tag=line.split()[0]if line.strip()else'empty'))
            exitcode=job.wait()
    need(exitcode==0 and complete and not RAM['errors'] and not(OUT/'stderr.log').read_text() and actual not in census.census(),'Actual original native terminal, exact unmodified program and complete raster transport')
    results=[l.strip()for l in RAM['text']if l.startswith(('MK2KS_EXIT_RESULT ','MK2KS_STABILITY ','MK2KS_SELECTION_RESULT '))]
    need(all(sha(p)==h for p,h in pins.items()),'Every original stock reference source/ROM unchanged')
    report=dict(passed=True,transportOnly=True,nativeExit=exitcode,driver='mk2',actualUnmodifiedFullStockProgramSHA256=digest(wanted),actualNativeIdentity=actual,nativeControllerResults=results,
        actualNativeRasters=[dict(header=f['header'],SHA256=f['SHA256'])for f in RAM['images']],inputHashes=pins,
        visualReferenceAccepted=False,artAccepted=False,audioAccepted=False,fullPortAcceptance=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,publicPlayableChanged=False)
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');RAM['report']=report
    print(json.dumps(dict(passed=True,transportOnly=True,nativeExit=exitcode,frames=len(RAM['images']),results=results)),flush=True)

if __name__=='__main__':
    try:run()
    except Exception as error:
        failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
        if OUT.exists():
            path=OUT/'failure.json';need(not path.exists(),'Preserve original stock reference failure')
            path.write_text(json.dumps(failure,indent=2)+'\n')
        print(json.dumps(failure,indent=2),flush=True)
    code.interact(banner='Original unmodified MK2 reference handle and native rasters retained.',local=dict(RAM=RAM))
