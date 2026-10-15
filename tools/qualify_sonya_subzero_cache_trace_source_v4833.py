"""Preserve actual native corruption AND failed trace before corrected probe."""
import ast,hashlib,json,re,subprocess
from pathlib import Path
import qualify_sonya_subzero_cache_trace_source_v4825 as previous
import run_sonya_subzero_cache_trace_ram_v4832 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
LUA=capture.LUA
OUT=ROOT/'audit_v4834_sonya_subzero_cache_trace_source_checked'
TRANSITIVE_LUA=tuple(dict.fromkeys((LUA,*previous.TRANSITIVE_LUA)))

def source_boundary(wrapper=None):
    previous.source_boundary()
    wrapper=(ROOT/LUA).read_text()if wrapper is None else wrapper
    previous.observer_readonly(wrapper)
    need(wrapper==(ROOT/LUA).read_text(),'Exact reviewed corrected readonly observer')
    for token in ('cpu.SP.value','assert(cpu.SP and cpu.A14 and cpu.ST',
        'local ok,line=pcall(function()','busy=false\n if not ok then',"print('LUA ERROR readonly cache observer:",
        "if kind~='group_next' and kind~='descriptor'then print(line)end",'local ring,ring_size,flushed={},1200,false',
        'cpu.PC.value==address+16','p:read_u32(0x01060220)==a','p:read_u16(a+0x1f0)==18',
        'cpu.PC.value~=0xff838860','frame>=bad_frame+2','frame>=108270',
        "dofile('mk2ks_sonya_p1_jax_jump_guard_ram_v4807.lua')"):
        need(token in wrapper,'Actual readonly SP/error/first-input/physical boundary '+token)
    need('cpu.A15'not in wrapper,'Actual CPU has SP, not a named A15 state')
    code=capture.collector_source();ast.parse(code)
    for token in ('audit_v4835_{fighter}_subzero_cache_trace_ram',"MK2KS_CAMPAIGN_SIDE='1'",'human_slot=1,cpu_slot=2',
        "MK2KS_TWO_PLAYER='0'",'raw==guest','rawRasterFilesWritten=0','raw_audio_files_written=0','Never persist encoded raster',
        "images[h['filename']]",'files.update(ROOT/p for p in source.TRANSITIVE_LUA)'):
        need(token in code,'Original complete RAM-only physical collector '+token)
    return dict(passed=True,diagnosticOnly=True,observerReadOnly=True,originalAllPhysicalPoliciesRetained=True,
        traceRecordsRequiredAtRuntime=True,nativeFixAccepted=False,fullPortAcceptance=False)

def main():
    need(not OUT.exists(),'Fresh immutable source preflight')
    prior=json.loads((previous.OUT/'report.json').read_text())
    terminal_path=ROOT/'audit_v4829_sonya_subzero_cache_trace_observed/report.json'
    terminal=json.loads(terminal_path.read_text())
    folder=ROOT/'audit_v4828_sonya_subzero_cache_trace_ram';log=(folder/'run.log').read_text()
    need(prior['passed']and prior['originalSourceFaultsRetained']==27 and len(prior['actualSourceFaultsRejected'])==5,'All32earlier source faults retained')
    need(terminal['passed']and terminal['nativeExit']==0 and terminal['actualStages']==list(range(8)),'Original actual native terminal, no restarted live process')
    need('MK2_SUBZERO_CACHE_TRACE frame='not in log and 'first_bad=-1 records=1' in log and
        'frame=108255 pc=FF838860' in log and 'at=010601F0 data=0510' in log,'Actual empty trace failure and exact native state corruption independently retained')
    cpu=(ROOT/'mame-mkp/src/devices/cpu/tms34010/tms34010.cpp').read_text()
    need('state_add(TMS34010_SP,     "SP",'in cpu and 'for (int regnum = 0; regnum < 15; regnum++)'in cpu,'Actual CPU registered SP and only A0..A14')
    positive=source_boundary();wrapper=(ROOT/LUA).read_text();faults=[]
    for label,bad in (('nonexistent_stack_state',wrapper.replace('cpu.SP.value','cpu.A15.value',1)),
        ('missing_error_signal',wrapper.replace('LUA ERROR readonly cache observer','ignored callback',1)),
        ('lost_first_input',wrapper.replace("then print(line)end","then end",1)),
        ('register_write',wrapper+'cpu.A0.value=0\n'),('state_write',wrapper+'p:write_u16(0x010601F0,1)\n')):
        need(bad!=wrapper,'Nonvacuous observer mutation')
        try:source_boundary(bad)
        except ValueError as error:faults.append(dict(kind=label,rejectedBy=str(error)))
        else:raise ValueError('Observer fault admitted '+label)
        need(source_boundary()==positive,'Restored whole readonly observer')
    pins=dict(prior['inputHashes'])
    for p,h in terminal['inputHashes'].items():
        need(p not in pins or pins[p]==h,'Consistent executed source/terminal pins');pins[p]=h
    for p in (previous.OUT/'report.json',terminal_path,Path(__file__).resolve(),Path(capture.__file__).resolve(),
        ROOT/'tools/inspect_sonya_subzero_cache_trace_v4830.py',*(ROOT/p for p in TRANSITIVE_LUA)):
        pins[str(p.resolve())]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual original native/controller/failure/public byte unchanged')
    report=dict(positive,inputHashes=pins,originalSourceFaultsRetained=32,actualSourceFaultsRejected=faults,
        actual4828TraceRejected=True,actual4828NativeBadWriteReproduced=True,actualNativeBadFrame=108255)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Compression before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)

if __name__=='__main__':main()
