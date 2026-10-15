"""All eight physical specials, both slots, twice, on current private build.

Whole original controllers and original semantic/body/shadow gates. No older
game acceptance is transferred. Raw guest/graphics/rasters remain RAM-only.
Finite Prison/Kitana instances; no CPU, blocked/KO, all arenas or release claim.
"""
import code
import copy
import gzip
import hashlib
import inspect
import json
import os
import re
import subprocess
import time
import traceback
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import capture_native_kano_laser_audio as audio
import capture_native_kano_laser_ui as ui
import native_process_census_v6647 as identity
import verify_special_repeat_v5115 as human
import verify_special_shadow_v5141 as shadow
import verify_move_phase_shadow_v5089 as graphics
import run_special_shadow_v5133 as original_transport
import serve_native_current_ui_ram as preview

ROOT,need,sha=audio.ROOT,audio.need,audio.sha
BASE=ROOT/'audit_native_kano_laser_special_shadow_ram'
OUT=ROOT/'audit_native_kano_laser_special_shadow_checked'
MATRIX=ROOT/'audit_native_kano_laser_special_matrix_checked'
INIT=ROOT/'audit_native_kano_laser_special_initializer_source'
GUARD=ROOT/'audit_native_kano_laser_special_shadow_source/report.json'
LUA=ROOT/'mk2ks_native_kano_laser_special_shadow.lua'
RAM_CASES={}
COMPLETED=[]

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def bindings(guest,build):
    native=SimpleNamespace(NAME=audio.NAME,EXE_SHA=build['executable_sha256'],GUEST_SHA=build['expected_guest_sha256'],
                           PAYLOAD_SHA=build['payload_sha256'],expected=lambda:guest)
    scope=dict(vars(human),native=native)
    exec(compile(inspect.getsource(human.check),__file__+'::whole_original_special_semantics','exec'),scope)
    human_check=scope['check']
    scope=dict(vars(shadow),human=SimpleNamespace(SPECS=human.SPECS,check=human_check))
    exec(compile(inspect.getsource(shadow.check),__file__+'::whole_original_every_field_body_shadow_gate','exec'),scope)
    shadow_check=scope['check']
    source=inspect.getsource(original_transport.capture)
    first=source.index('     source,mapped,cmd=');last=source.index("     need(not any(p['stream']==proof['stream']",first)
    body=source[first:last]
    body='\n'.join(line[5:]if line.startswith('     ')else line for line in body.splitlines())
    body='\n'.join('    '+line for line in body.splitlines())
    part_source='def decode_part(f,raw,gfx32):\n'+body+"\n    need(raw==bytes(gfx32[mapped//8:mapped//8+len(raw)]),'Whole actual native stream equals independently interleaved current compiled ROM')\n    return proof\n"
    part_scope=dict(vars(original_transport))
    exec(compile(part_source,__file__+'::whole_original_actual_compressed_stream_decoder','exec'),part_scope)
    return native,human_check,shadow_check,part_scope['decode_part']

def reconstruct(native,pins):
    scope=dict(vars(graphics),native=native)
    exec(compile(inspect.getsource(graphics.reconstruct),__file__+'::whole_actual_compiled_ROM_lane_reconstruction','exec'),scope)
    return scope['reconstruct'](pins)

def channels_gate(text,terminal):
    def rows(tag):return[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith(tag+' ')]
    pools=rows('MK2_SS_FINISH_POOL');channels=rows('MK2_SS_CHANNEL')
    need([int(r['frame'])for r in pools]==list(range(1,terminal+1)) and
         all(r['actor']==r['main']=='00000000' and r['slot']=='0' and r['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0' and
             r['writes']=='0' and r['assistance']=='none'for r in pools),'Every new finisher owner/priority/timer remains clear throughout ordinary specials')
    need([(int(r['frame']),int(r['channel']))for r in channels]==[(f,c)for f in range(1,terminal+1)for c in range(19)] and
         all(r['loop']==r['paused']=='0' and r['writes']=='0' and r['assistance']=='none'for r in channels),'Entire actual nineteen-channel ledger, no looping/paused aliases')
    private=[r for r in channels if int(r['channel'])>=14]
    need(all(r['sample']=='4294967295' and r['length']=='0' and float(r['pos'])==0 for r in private),'All five private finisher sounds remain inactive through special activation/recovery')
    return dict(completeChannelFields=len(channels),completeFinisherPoolFields=len(pools),privateSoundsInactive=True,audioWaveformAcceptance=False)

def load(move,side,finite=False):
    key=f'{move}_p{side}';folder,text,images=RAM_CASES[key]
    rows=defaultdict(list)
    for line in text.splitlines():
        if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
    report=json.loads((folder/'result.json').read_text())
    if finite:
        # Exact original repeated-special observer view. Extra all-field shadow
        # evidence remains independently checked by the complete shadow gate.
        for tag in tuple(rows):
            if tag in('MK2_HPHASE_SHADOW_BEGIN','MK2_HPHASE_PROJECTION','MK2_HPHASE_SHADOW_DMA','MK2_HPHASE_PART_DIGEST'):del rows[tag]
        frames={s['frame']for s in report['actualScenes']}
        entry=human.SPECS[move][1]
        entries={int(r['frame'])for r in rows['MK2_HSPECIAL_EVENT']if int(r['entry'],16)==entry}
        for tag in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):rows[tag]=[r for r in rows[tag]if int(r['frame'])in frames-entries]
    return dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,
                streams=json.loads((folder/'shadow_stream_memory_proofs.json').read_text()))

def capture(move,side,guest,gfx,gfx32,payload,native,check,decode_part,pins):
    key=f'{move}_p{side}';folder=BASE/key;build=ROOT/audio.NAME
    need(not folder.exists() and not identity.census(),'Fresh exact physical leaf, no replay');folder.mkdir(parents=True)
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    env.update(MK2KS_HUMAN_SPECIAL_MOVE=move,MK2KS_HUMAN_SPECIAL_SIDE=str(side),MK2KS_HUMAN_SPECIAL_AIR='0',MK2KS_HUMAN_SPECIAL_VICTIM='kitana')
    command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
             '-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-artpath',str(ROOT/'artwork'),'-samples','-samplerate','48000',
             '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-noautoframeskip','-frameskip','0',
             '-nothrottle','-str','100','-wavwrite','NUL','-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),
             '-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
    images={};scenes=[];streams=[];proofs={};errors=[]
    with(folder/'stderr.log').open('w',encoding='utf-8')as err:
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        try:
            for _ in range(100):
                actual=next((r for r in identity.census()if r['ProcessId']==job.pid),None)
                if actual or job.poll()is not None:break
                time.sleep(.02)
            need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve() and str(folder)in actual['CommandLine'],
                 'Actual native PID/parent/path/birth/full arguments')
        except Exception as error:errors.append(dict(stage='identity',error=repr(error)))
        save(folder/'process.json',dict(pid=job.pid,actualWindowsIdentity=actual,command=command))
        print(f'{move} P{side}: actual current special/shadow PID={job.pid}',flush=True)
        with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
            for line in job.stdout:
                try:
                    if ' hex='in line:
                        tag=line.split()[0];pairs=re.findall(r'(\w+)=([^\s]+)',line);h=dict(pairs);need(len(pairs)==len(h),'Unique raw metadata')
                        raw=bytes.fromhex(h.pop('hex'));need(len(raw)==int(h['bytes']),'Full actual native raw transport')
                        digest=hashlib.sha256(raw).hexdigest().upper()
                        if tag in('MK2_HPHASE_GUEST','MK2_HPHASE_GFX'):
                            kind='guest'if tag.endswith('GUEST')else'gfx';expected=guest if kind=='guest'else gfx
                            need(kind not in proofs and h==dict(frame='1',bytes=str(len(expected))) and raw==expected,'Whole independently reconstructed actual '+kind)
                            proofs[kind]=dict(bytes=len(raw),sha256=digest,everyActualByteComparedInRAM=True)
                        elif tag=='MK2_HPHASE_RGB':
                            need(len(raw)==406400 and h['width']=='400' and h['height']=='254','Complete unscaled native RGB field')
                            frame=int(h['frame']);name=f'ui_{frame:04d}.png';need(name not in images,'Unique original physical frame_done scene')
                            images[name]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy()
                            scenes.append(dict(stage=h['stage'],attempt=int(h['attempt']),frame=frame,width=400,height=254,bytes=len(raw),sha256=digest,rawMediaFilesWritten=0))
                        elif tag=='MK2_HPHASE_PART':
                            proof=decode_part(h,raw,gfx32);need(not any(p['stream']==proof['stream']for p in streams),'Every unique actual static native stream observed once');streams.append(proof)
                        else:raise ValueError('Unknown actual raw block '+tag)
                        log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in h.items())+' sha256='+digest+'\n')
                    else:
                        need('hex='not in line,'No raw media persisted');log.write(line)
                        if re.search(r'_(READY|COMMAND|RECOVERED|FINAL|FAILED|RESULT) ',line):print(line.strip(),flush=True)
                except Exception as error:errors.append(dict(stage='transport',error=repr(error)))
            exitcode=job.wait()
    with gzip.open(folder/'run.log.gz','rt')as f:text=f.read()
    terminal=dict(pid=job.pid,nativeExit=exitcode,actualWindowsIdentity=actual,hostDecodeErrors=errors)
    save(folder/'native_terminal.json',terminal);save(folder/'shadow_stream_memory_proofs.json',streams)
    RAM_CASES[key]=(folder,text,images)
    report=dict(passed=False,nativeExit=exitcode,move=move,side=side,victim='kitana',candidate=native.NAME,
        executableSHA256=native.EXE_SHA,guestSHA256=native.GUEST_SHA,payloadSHA256=native.PAYLOAD_SHA,inputHashes=pins,
        actualScenes=scenes,proofs=proofs,actualUniqueShadowStreams=len(streams),nativeTerminal=terminal,
        canonicalCMDUsed=False,publicPlayableChanged=False,rawGuestGFXRGBPCMOrWAVFilesWritten=0,newBuilds=0,
        fullPortAcceptance=False,fullArtAcceptance=False,fullAudioAcceptance=False)
    try:
        need(exitcode==0 and actual and not errors and len(proofs)==2 and not(folder/'stderr.log').read_text() and
             not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|MK2_HSPECIAL_FAILED|WRONG CHECKSUMS|might not run correctly',text,re.I),
             'Same actual natural native terminal0, complete current inventories and no runtime/host warnings')
        result=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_HSPECIAL_RESULT ')]
        need(len(result)==1 and result[0]['completed']==result[0]['attempt']=='2','Both real physical activation/recovery cycles')
        report.update(passed=True,terminalResult=result[0])
        # The complete unchanged checker reads the current report for metadata.
        # Write once only after its result, using this in-memory metadata view.
        rows=defaultdict(list)
        for line in text.splitlines():
            if line.startswith(('MK2_HSPECIAL_','MK2_HPHASE_')):rows[line.split()[0]].append(dict(re.findall(r'(\w+)=([^\s]+)',line)))
        b=dict(move=move,side=side,folder=folder,report_path=folder/'result.json',report=report,rows=rows,streams=streams)
        report['sourceBoundBodyShadowSemantics']=check(b,guest,payload,gfx32)
        report['passiveSoundChannels']=channels_gate(text,int(result[0]['frame']))
        need(all(sha(p)==h for p,h in pins.items()),'Every actual source/candidate/controller unchanged')
    except Exception as error:report.update(passed=False,error=repr(error),traceback=traceback.format_exc())
    save(folder/'result.json',report);COMPLETED.append(report)
    print(json.dumps(dict(move=move,side=side,passed=report['passed'],nativeExit=exitcode,scenes=len(scenes),error=report.get('error'))),flush=True)
    return report

def shadow_faults(b,guest,payload,gfx32,check):
    source=inspect.getsource(shadow.main)
    first=source.index(' faults=[]');last=source.index(" need(all(sha(p)==h",first)
    block=source[first:last]
    block='\n'.join(line[1:]if line.startswith(' ')else line for line in block.splitlines())
    source='def faults_for_actual_case(b,guest,payload,gfx,case):\n'+'\n'.join('    '+line for line in block.splitlines())+'\n    return faults\n'
    scope=dict(vars(shadow),check=check)
    exec(compile(source,__file__+'::whole_original_eleven_actual_body_shadow_faults','exec'),scope)
    faults=scope['faults_for_actual_case'](b,guest,payload,gfx32,b['report']['sourceBoundBodyShadowSemantics'])
    need(len(faults)==11,'All original actual-field/native-row faults retained')
    return faults

def run():
    need(not BASE.exists() and not OUT.exists() and not MATRIX.exists() and not identity.census(),'Fresh full special/body/shadow matrix, no pending native replay')
    guard=json.loads(GUARD.read_text())
    need(guard['passed'] and guard['actualNativeParserAccepted'] and guard['wholePhysicalSpecialShadowByteIdentical'] and
         not guard['gameplayAccepted'] and guard['totalSampleChannels']==19 and all(sha(p)==h for p,h in guard['inputHashes'].items()),'Actual native parser preserves whole original controller')
    scope=dict(vars(ui),INIT=INIT,__file__=__file__)
    exec(compile(inspect.getsource(ui.expectation),__file__+'::whole_independent_current_guest_initializer','exec'),scope)
    guest,gfx,build=scope['expectation']()
    native,human_check,check,decode_part=bindings(guest,build)
    candidate=ROOT/audio.NAME;payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
    pins=dict(build['input_hashes'])
    for p in(Path(__file__),LUA,GUARD,INIT/'report.json',ROOT/'mk2ks_special_shadow_v5131.lua',Path(audio.__file__),Path(ui.__file__),
             Path(human.__file__),Path(shadow.__file__),Path(graphics.__file__),Path(original_transport.__file__),Path(identity.__file__),
             candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',ROOT/'PLAY_LATEST_KANO_SONYA.cmd'):
        pins[str(p.resolve())]=sha(p)
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for lo,hi in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
        need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],'Entire original native body/shadow kernel unchanged')
    gfx32=reconstruct(native,pins)
    cases=[('ball',1),('ball',2)]+[(m,s)for m in human.SPECS if m!='ball'for s in(1,2)]
    for move,side in cases:
        r=capture(move,side,guest,gfx,gfx32,payload,native,check,decode_part,pins)
        need(r['passed'],'Full current positive control; do not dispatch next case after rejection')
    faults=[]
    for move,side in cases:
        b=load(move,side);values=shadow_faults(b,guest,payload,gfx32,check)
        faults.extend(dict(move=move,side=side,**v)for v in values)
        print(f'{move} P{side}: all eleven original body/shadow faults rejected',flush=True)
    # Entire original 194-fault special matrix, not a smaller fault selection.
    main_scope=dict(vars(human),__file__=__file__,OUT=MATRIX,native=native,check=human_check,load=lambda m,s:load(m,s,finite=True))
    exec(compile(inspect.getsource(human.main),__file__+'::whole_original_194_fault_special_matrix','exec'),main_scope)
    main_scope['main']()
    matrix=json.loads((MATRIX/'report.json').read_text())
    need(matrix['passed'] and matrix['actualCases']==16 and matrix['actualVerifiedSpecialCycles']==32 and
         len(matrix['actualSemanticFaultsRejected'])==194,'All original sixteen cases/32cycles/194 actual-field faults')
    need(not identity.census() and all(sha(p)==h for p,h in pins.items()),'All actual native handles terminal, executed inputs conserved')
    outputs={}
    for folder in(BASE,MATRIX):
        for p in folder.rglob('*'):
            if p.is_file():need(p.suffix.lower()not in('.png','.wav','.bin','.exe','.zip'),'No raw media/build/ROM copies');outputs[str(p.resolve())]=sha(p)
    OUT.mkdir()
    report=dict(passed=True,candidate=native.NAME,actualCases=16,actualVerifiedSpecialCycles=32,cases=COMPLETED,
        actualAddedFighterShadowCopies=sum(r['sourceBoundBodyShadowSemantics']['actualAddedFighterShadowCopies']for r in COMPLETED),
        actualSourceBoundShadowCopies=sum(r['sourceBoundBodyShadowSemantics']['actualSourceBoundShadowCopies']for r in COMPLETED),
        actualContiguousActorFields=sum(r['sourceBoundBodyShadowSemantics']['actualContiguousActorFields']for r in COMPLETED),
        actualFullRGBFields=sum(len(r['actualScenes'])for r in COMPLETED),originalSpecialFaults=194,originalShadowFaults=faults,
        inputHashes=pins,outputHashes=outputs,scope=__doc__,allEightMovesBothSlotsRepeatRecoverVerified=True,
        everyReadyOwnedBodyShadowFieldSourceBound=True,actualSquareContactVerified=False,allArenasVerified=False,
        fullPixelsAccepted=False,fullAudioAcceptance=False,fullPortAcceptance=False,publicPlayableChanged=False,
        newNativeBoots=16,newBuilds=0,newROMCopies=0,newZIPs=0,newRawMedia=0,goalStatus='active')
    save(OUT/'report.json',report)
    print(json.dumps(dict(passed=True,cases=16,cycles=32,specialFaults=194,shadowFaults=len(faults),fullPortAcceptance=False)),flush=True)
    return report

if __name__=='__main__':
    try:accepted=run()
    except Exception as error:
        need(not OUT.exists(),'Never overwrite executed acceptance/failure');OUT.mkdir()
        save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
    server=preview.serve(RAM_CASES)
    code.interact(banner='Same actual sixteen-case special trials terminal; original RGB stays RAM-only.',local=dict(cases=RAM_CASES,server=server,module=__import__(__name__)))
