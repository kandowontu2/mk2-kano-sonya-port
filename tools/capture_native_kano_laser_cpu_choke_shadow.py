"""Current natural CPU Kano choke mirror/cross, whole original physical/body/shadow/health gates.

Finite physical CPU slot2/human slot1, startup and ordinary follow-up. No
other CPU moves/slots, full PCM, all arenas, KO or complete port acceptance.
"""
import code
import copy
import gzip
import inspect
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
from types import SimpleNamespace
import capture_native_kano_laser_special_shadow as base
import verify_current_cpu_choke_shadow_v5331 as cpu_body
import verify_current_cpu_terminal_health_shadow_v5335 as health

ROOT,need,sha=base.ROOT,base.need,base.sha
BASE=ROOT/'audit_native_kano_laser_cpu_choke_shadow_ram'
OUT=ROOT/'audit_native_kano_laser_cpu_choke_shadow_checked'
INIT=ROOT/'audit_native_kano_laser_cpu_choke_initializer_source'
GUARD=ROOT/'audit_native_kano_laser_cpu_choke_shadow_source'
LUA=ROOT/'mk2ks_native_kano_laser_cpu_choke_shadow.lua'
RAM_CASES={}


def replace_once(source,before,after):
    need(source.count(before)==1,'Exact whole original adapter boundary '+before[:80])
    return source.replace(before,after,1)


def qualify():
    need(not GUARD.exists() and not base.identity.census(),'Fresh native compiler diagnostic')
    GUARD.mkdir()
    candidate=ROOT/base.audio.NAME
    paths=[Path(__file__),LUA,ROOT/'mk2ks_native_kano_laser_cpu_choke_parse.lua',
           ROOT/'mk2ks_native_kano_laser_special_shadow.lua',ROOT/'mk2ks_cpu_choke_shadow_v5328.lua',
           ROOT/'mk2ks_cpu_recovery_probe_v1438.lua',ROOT/'mk2ks_special_shadow_v5131.lua',
           candidate/'mkport_candidate.exe',candidate/'build-info.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd']
    pins={str(p.resolve()):sha(p)for p in paths}
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    env['MK2KS_TEST_FIGHTER']='kano'
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
             '-samplepath',str(candidate/'samples')+';'+str(ROOT/'samples'),'-skip_gameinfo','-nocheat','-video','none',
             '-sound','none','-nothrottle','-str','4','-autoboot_delay','0','-autoboot_script',str(paths[2]),
             '-inipath',str(GUARD),'-cfg_directory',str(GUARD/'cfg'),'-nvram_directory',str(GUARD/'nvram')]
    born=time.time()
    job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
    actual=None
    for _ in range(100):
        actual=next((r for r in base.identity.census()if r['ProcessId']==job.pid),None)
        if actual or job.poll()is not None:break
        time.sleep(.02)
    raw,err=job.communicate()
    base.save(GUARD/'native_terminal.json',dict(pid=job.pid,nativeExit=job.returncode,actualWindowsIdentity=actual,stderr=err.decode(errors='replace')))
    with gzip.open(GUARD/'native_stdout.log.gz','wb')as f:f.write(raw)
    need(job.returncode==0 and not err and actual and actual['ParentProcessId']==os.getpid()and actual['createdUnix']>=born-1 and
         Path(actual['ExecutablePath']).resolve()==(candidate/'mkport_candidate.exe').resolve(),'Actual native compiler terminal and identity')
    rows=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in raw.decode().splitlines()if line.startswith('MK2_CS_PARSE_SOURCE ')]
    expanded={r['kind']:bytes.fromhex(r['hex']).decode()for r in rows}
    need(len(rows)==len(expanded)==4 and all(len(expanded[r['kind']].encode())==int(r['bytes'])for r in rows)and
         b'MK2_CS_PARSE_RESULT gameplay_callbacks_executed=0 guest_writes=0'in raw,'Entire actual expansions, callbacks unexecuted')
    original=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()
    need(original.count("manager.machine.screens[':screen']:snapshot")==6 and
         expanded['physical']==original.replace("manager.machine.screens[':screen']:snapshot",'snapshot_ram'),
         'Entire actual original physical controller byte-identical except six RAM media sinks')
    need(expanded['wrapper']==(ROOT/'mk2ks_cpu_choke_shadow_v5328.lua').read_text(),'Whole original CPU wrapper byte-identical')
    passive=(ROOT/'mk2ks_native_kano_laser_special_shadow.lua').read_text().split('-- Passive current nineteen-channel/private-finisher-pool observer only.',1)[1]
    need(expanded['channels']=='-- Passive current nineteen-channel/private-finisher-pool observer only.'+passive,'Entire original nineteen-channel observer')
    need(all(not re.search(r':write_|write_[ui]\d+|load_?state|\.value\s*=(?!=)',s)for s in expanded.values()),'No guest/item/register/state writes')
    need(all(sha(p)==h for p,h in pins.items()),'Native-compiled source inputs conserved')
    value=dict(passed=True,actualNativeParserAccepted=True,wholePhysicalCPUUnchangedExceptSixSinks=True,
               gameplayAccepted=False,inputHashes=pins,nativeExit=0,actualWindowsIdentity=actual,
               fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newRawMedia=0,goalStatus='active')
    base.save(GUARD/'report.json',value)
    print('Whole original physical CPU/body/shadow/current19-channel sources compiled by actual native parser',flush=True)
    return value


def bindings(human):
    # Retrieve the entire already-qualified pre-exit complete-health checker,
    # not the historical run/report function or its historical failure premises.
    whole_health=health.bindings().__globals__['verify_log'].__globals__['whole_health']
    def physical(text,player,guest):
        result=cpu_body.cpu.verify_log(text,player,guest)
        result['wholeNativeHealthHistory']=whole_health(text,guest)
        return result
    scoped_cpu=SimpleNamespace(original=cpu_body.cpu.original,verify_log=physical)
    scope=dict(vars(cpu_body),cpu=scoped_cpu)
    exec(compile(inspect.getsource(cpu_body.bindings),__file__+'::whole_original_CPU_body_shadow_factory','exec'),scope)
    _,original_check=scope['bindings'](human)
    def check(b,guest,payload,gfx32):
        b=dict(b,human=human,cpuLog=b['cpuLog'])
        return original_check(b,guest,payload,gfx32)
    return check


def run():
    need(not BASE.exists() and not OUT.exists() and not base.identity.census(),'Fresh actual CPU cases')
    guard=qualify()
    scope=dict(vars(base.ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(base.ui.expectation),__file__+'::whole_independent_current_guest','exec'),scope)
    guest,gfx,build=scope['expectation']()
    native,_,_,decode=base.bindings(guest,build)
    candidate=ROOT/base.audio.NAME
    payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins=dict(build['input_hashes']);pins.update(guard['inputHashes'])
    for p in(Path(base.__file__),Path(cpu_body.__file__),Path(health.__file__),Path(cpu_body.cpu.__file__),
             Path(cpu_body.cpu.original.__file__),Path(base.shadow.__file__),Path(base.human.__file__),
             Path(base.graphics.__file__),Path(base.original_transport.__file__),Path(base.audio.__file__),Path(base.ui.__file__),
             GUARD/'report.json',INIT/'report.json',candidate/'roms/mk2ks/mk2ks.mdata'):
        pins[str(p.resolve())]=sha(p)
    gfx32=base.reconstruct(native,pins)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],'Whole original native body/shadow kernels')
    source=inspect.getsource(base.capture)
    source=replace_once(source,
        "env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')",
        "env.update(MK2KS_TEST_FIGHTER=human,MK2KS_TEST_BOOT_FRAME='605'if human=='kano'else'606',MK2KS_CPU_PAIR_APPROACH='guard_until_close',MK2KS_CPU_PAIR_CONFIRM_AGE='264')")
    source=replace_once(source,"line.startswith('MK2_HSPECIAL_RESULT ')","line.startswith('MK2_CPU_PAIR_RESULT ')")
    source=replace_once(source,"need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')",
                        "need(len(result)==1 and int(result[0]['complete'])>0 and int(result[0]['follow_regain'])>0,'Actual complete native pair and subsequent ordinary recovery')")
    source=replace_once(source,"b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)",
                        "b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams,human=human,cpuLog=text)")
    source=replace_once(source,"key=f'{move}_p{side}'", "key=f'choke_cpu_kano_human_{human}'")
    source=replace_once(source,"victim='kitana'", "victim=human")
    reports=[]
    for human in('kano','sonya'):
        scope=dict(vars(base),BASE=BASE,LUA=LUA,RAM_CASES=RAM_CASES,COMPLETED=[],human=human)
        exec(compile(source,__file__+'::whole_current_native_capture_CPU_original_controls','exec'),scope)
        r=scope['capture']('choke',2,guest,gfx,gfx32,payload,native,bindings(human),decode,pins)
        reports.append(r)
        need(r['passed'],'Do not dispatch next actual case after positive gate failure')
    need(not base.identity.census() and all(sha(p)==h for p,h in pins.items()),'Actual native terminals and immutable inputs')
    outputs={str(p.resolve()):sha(p)for p in BASE.rglob('*')if p.is_file()}
    need(all(Path(p).suffix.lower()not in('.png','.wav','.bin','.exe','.zip')for p in outputs),'No raw media or duplicate build')
    OUT.mkdir()
    base.save(OUT/'report.json',dict(passed=True,candidate=native.NAME,cases=reports,inputHashes=pins,outputHashes=outputs,
        actualPhysicalCPUChokeCases=2,everyReadyOwnedBodyShadowFieldSourceBound=True,wholeNativeHealthHistoryVerified=True,
        actualCPUChoicesPrescribed=False,physicalHumanSlot=1,physicalCPUSlot=2,checkerFaultTestsPending=True,
        fullVisualTimelineAccepted=False,allCPUContextsAccepted=False,allArenasAccepted=False,fullAudioAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newBuilds=0,newROMCopies=0,newRawMedia=0,newZIPs=0,goalStatus='active',scope=__doc__))
    print(json.dumps(dict(passed=True,actualCPUChokeCases=2,checkerFaultTestsPending=True,fullPortAcceptance=False)),flush=True)


if __name__=='__main__':
    try:run()
    except Exception as error:
        need(not OUT.exists(),'Preserve executed failure')
        OUT.mkdir();base.save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
                                                 fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=base.preview.serve(RAM_CASES)
    code.interact(banner='Same actual CPU trials retained in RAM; no terminal replay.',
                  local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
