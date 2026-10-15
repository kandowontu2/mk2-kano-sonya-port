"""Four fresh current-build input-only native floor/shadow regressions.

Whole original 480-field mobility controller, native row scanner/copy PCs,
display latch, independent full VRAM reconstruction, and stock floor control.
All unscaled images, palettes and video buffers stay in RAM. Not all arenas.
"""
import gzip
import hashlib
import inspect
import json
import os
import re
import subprocess
import time
import traceback
from pathlib import Path
import numpy as np
import capture_native_kano_laser_audio as current
import native_process_census_v6647 as identity
import inspect_current_ground_shadow_v811 as ground
import verify_current_ui_ground_v816 as check
import inspect_natural_arena_floor_v602 as decode_source
import verify_native_floor_display_v602 as latch_source

ROOT,need,sha=current.ROOT,current.need,current.sha
BASE=ROOT/'audit_native_kano_laser_ground_ram'
OUT=ROOT/'audit_native_kano_laser_ground_checked'
LUA=ROOT/'mk2ks_native_kano_laser_ground_ram.lua'
GUARD=ROOT/'audit_native_kano_laser_ground_ram_source/report.json'
RAM_CASES={}
COMPLETED=[]

def save(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def model():
    source=inspect.getsource(ground.inspect)
    changes=[('def inspect(folder):','def inspect_ram(log,images,raw_buffers):'),
             ('    folder=Path(folder)\n',''),
             ("    log=(folder/'run.log').read_text(encoding='utf-8-sig')\n",''),
             ("np.asarray(Image.open(folder/'snap'/snap['file']).convert('RGB'))","images[snap['file']]"),
             ("np.fromfile(folder/snap['vram_file'],dtype='<u2')","np.frombuffer(raw_buffers[snap['vram_file']],dtype='<u2')"),
             ("(folder/snap['palette_file']).read_bytes()","raw_buffers[snap['palette_file']]"),
             ("np.fromfile(folder/snap['palette_file'],dtype='<u4')","np.frombuffer(raw_buffers[snap['palette_file']],dtype='<u4')"),
             ("np.fromfile(folder/pre[frame-1]['file'],dtype='<u2')","np.frombuffer(raw_buffers[pre[frame-1]['file']],dtype='<u2')")]
    for old,new in changes:
        need(source.count(old)==1,'Exact whole original ground inspector RAM boundary: '+old);source=source.replace(old,new)
    scope=dict(vars(ground));exec(compile(source,__file__+'::whole_original_ground_inspector_only_RAM_reads','exec'),scope)
    return scope['inspect_ram']

def capture(fighter,side,guest,gfx,pins,inspect_ram):
    key=f'{fighter}_p{side}';folder=BASE/key
    need(not folder.exists() and not identity.census(),'Fresh leaf, no native replay');folder.mkdir(parents=True)
    build=ROOT/current.NAME
    env={k:v for k,v in os.environ.items() if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_|MK2PORT_)',k)}
    env.update(MK2KS_GROUND_FIGHTER=fighter,MK2KS_GROUND_SIDE=str(side),MK2KS_GROUND_BOOT='604',MK2KS_GROUND_OUT=str(folder))
    command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
             '-samplepath',str(build/'samples')+';'+str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),
             '-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000',
             '-noautoframeskip','-frameskip','0','-nothrottle','-str','90','-snapsize','400x254','-wavwrite','NUL',
             '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),
             '-autoboot_script',str(LUA)]
    images={};buffers={};headers=[];ram_lines=[];errors=[];inventories={'MK2_GR_GUEST':0,'MK2_GR_GFX':0};gfx_headers=[]
    with (folder/'stderr.log').open('w',encoding='utf-8')as err:
        born=time.time();job=subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',errors='replace',creationflags=subprocess.CREATE_NO_WINDOW)
        actual=None
        try:
            for _ in range(100):
                actual=next((r for r in identity.census() if r['ProcessId']==job.pid),None)
                if actual or job.poll()is not None:break
                time.sleep(.02)
            need(actual and actual['ParentProcessId']==os.getpid() and actual['createdUnix']>=born-1 and
                 Path(actual['ExecutablePath']).resolve()==(build/'mkport_candidate.exe').resolve() and str(folder)in actual['CommandLine'],
                 'Actual native kernel PID/parent/path/birth/full command')
        except Exception as error:errors.append(dict(stage='identity',error=repr(error)))
        save(folder/'process.json',dict(pid=job.pid,actualWindowsIdentity=actual,command=command))
        print(f'{key} actual ground native PID={job.pid}',flush=True)
        with gzip.open(folder/'run.log.gz','wt',encoding='utf-8')as log:
            for line in job.stdout:
                try:
                    tag=line.split()[0] if line.split() else ''
                    if ' hex=' in line:
                        pairs=re.findall(r'(\w+)=([^\s]+)',line);h=dict(pairs);need(len(pairs)==len(h),'Unique raw metadata')
                        raw=bytes.fromhex(h.pop('hex'));need(len(raw)==int(h['bytes']),'Complete native raw buffer')
                        h['sha256']=hashlib.sha256(raw).hexdigest().upper()
                        if tag in inventories:
                            need(h['frame']=='1' and raw==(guest if tag=='MK2_GR_GUEST' else gfx),'Entire current guest/source GFX independently exact');inventories[tag]+=1
                        elif tag=='MK2_GR_RGB':
                            need(h['width']=='400' and h['height']=='254' and len(raw)==406400 and h['filename']==f"ground_{int(h['frame']):04d}.png",'Full unscaled native displayed field')
                            need(h['filename']not in images,'No duplicate displayed snapshot')
                            images[h['filename']]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy();headers.append(h)
                        elif tag=='MK2_GR_BUFFER':
                            need(h['filename']not in buffers and re.fullmatch(r'(pre|vram|palette)_\d+\.bin',h['filename']),'Unique original bounded video sink')
                            need(len(raw)==(32768*4 if h['filename'].startswith('palette_') else 512*512*2),'Complete native VRAM/palette')
                            buffers[h['filename']]=raw
                        else:raise ValueError('Unknown raw block '+tag)
                        log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in h.items())+'\n')
                    elif tag=='MK2_GROUND_GFX':
                        h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('data'))
                        need(len(raw)==int(h['bytes']),'Whole compressed source stream')
                        h['sha256']=hashlib.sha256(raw).hexdigest().upper();gfx_headers.append(h)
                        ram_lines.append(line)
                        log.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in h.items())+'\n')
                    else:
                        need('hex='not in line and 'data='not in line,'No raw media persisted')
                        log.write(line);ram_lines.append(line)
                        if tag in ('MK2_GROUND_LIVE','MK2_GROUND_READY','MK2_GROUND_RESULT'):print(line.strip(),flush=True)
                except Exception as error:errors.append(dict(stage='decode',error=repr(error)))
            exitcode=job.wait()
    text=''.join(ram_lines)
    terminal=dict(pid=job.pid,nativeExit=exitcode,actualWindowsIdentity=actual,hostDecodeErrors=errors)
    save(folder/'native_terminal.json',terminal)
    carrier=dict(folder=folder,log=text,images=images,buffers=buffers,headers=headers,gfxHeaders=gfx_headers,terminal=terminal)
    RAM_CASES[key]=carrier
    result=dict(passed=False,candidate=current.NAME,fighter=fighter,side=side,nativeTerminal=terminal,inputHashes=pins,fullPortAcceptance=False)
    try:
        need(exitcode==0 and not errors and not (folder/'stderr.log').read_text() and
             not re.search(r'LUA ERROR|stack traceback|fatal error|access violation|INVALID|WRONG CHECKSUMS|might not run correctly',text,re.I),
             'Actual natural native terminal0, no errors or invalid identity')
        need(inventories=={'MK2_GR_GUEST':1,'MK2_GR_GFX':1},'Exactly one full actual guest/GFX startup inventory')
        finish=ground.rows(text,'RESULT');need(len(finish)==1 and finish[0]['terminalAge']==480,'Full original mobility terminal')
        fields=ground.rows(text,'FIELD')
        need(len(fields)==962 and [(r['age'],r['slot']) for r in fields]==[(a,s) for a in range(481)for s in(1,2)],'All true-owned physical mobility fields')
        anchors={17:134,18:135,4:133}
        for r in fields:
            wanted=(17 if fighter=='kano' else 18)if r['slot']==side else 4
            need(r['id']==r['roster']==wanted and r['owner']==r['actor'] and r['state']==1 and r['hp']==161 and
                 r['floor']==r['stageY']-anchors[wanted],'Actual own identity/native floor/stock control/full health')
        snaps=ground.rows(text,'SNAP')
        need([r['file']for r in snaps]==[r['filename']for r in headers] and len(images)==len(snaps)==37,'All original displayed callbacks retained')
        expected_buffers={r['file']for r in ground.rows(text,'PRE')}|{r[k]for r in snaps for k in('vram_file','palette_file')}
        need(set(buffers)==expected_buffers and len(buffers)==111,'All exact pre-DMA, displayed VRAM, palette buffers')
        value=inspect_ram(text,images,buffers);check.check_ground(value,fighter,side)
        pools=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_GR_FINISH_POOL ')]
        last=finish[0]['frame']
        need(len(pools)==last and [int(r['frame'])for r in pools]==list(range(1,last+1)) and
             all(r['actor']==r['main']=='00000000' and r['slot']=='0' and r['slots']=='0000,0;0000,0;0000,0;0000,0;0000,0'for r in pools),
             'Entire private finisher ownership/priority/timer stays clear in ordinary native mobility')
        channels=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in text.splitlines()if line.startswith('MK2_GR_CHANNEL ')]
        need([(int(r['frame']),int(r['channel']))for r in channels]==[(f,c)for f in range(1,last+1)for c in range(19)] and
             all(r['loop']==r['paused']=='0'for r in channels),'Every actual source channel observed, no paused/looping aliases')
        need(all(r['sample']=='4294967295' and r['length']=='0' and float(r['pos'])==0 for r in channels if int(r['channel'])>=14),'All five finisher sounds stay inactive through ordinary ground movement')
        need(all(sha(p)==h for p,h in pins.items()),'Actual source/build/controller preserved')
        result.update(passed=True,presentation=value,ownedIdentityFields=len(fields),displayedNativeRasters=len(images),
                      wholeActualGuestGFXAccepted=True,privateFinisherPoolFields=len(pools),actualChannelFields=len(channels),
                      boundedDeadPoolGroundShadowAcceptance=True,allArenaFloorAcceptance=False,audioWaveformAcceptance=False,newRawMedia=0)
    except Exception as error:result.update(error=repr(error),traceback=traceback.format_exc())
    save(folder/'result.json',result);carrier['result']=result;COMPLETED.append(result)
    print(json.dumps(dict(case=key,passed=result['passed'],rasters=len(images),error=result.get('error'))),flush=True)
    return carrier

def fault_checks(cases):
    """Actual source-row/ownership faults plus separately gated grounding faults."""
    results=[]
    for key,c in cases.items():
        text=c['log'];components=ground.rows(text,'SHADOW_COMPONENT');need(components,'Actual native components')
        buffers={r['key']:r for r in ground.rows(text,'GFX')}
        lines=text.splitlines(keepends=True);at=next(i for i,s in enumerate(lines)if s.startswith('MK2_GROUND_SHADOW_COMPONENT '))
        dma_at=next(i for i,s in enumerate(lines)if s.startswith('MK2_GROUND_DMA ')and f"event={components[0]['event']}"==s.strip().split()[-1])
        mutations=[('missing_component',at,''),
                   ('wrong_row',at,re.sub(r'row=[0-9A-F]+',lambda m:'row='+f"{int(m[0][4:],16)+0x70:08X}",lines[at],count=1)),
                   ('wrong_owner',at,re.sub(r'owner=[0-9A-F]+','owner=00000000',lines[at],count=1)),
                   ('wrong_native_caller',dma_at,re.sub(r'pc=[0-9A-F]+','pc=00000000',lines[dma_at],count=1))]
        for name,index,line in mutations:
            altered=lines.copy();altered[index]=line
            rejected=False
            try:ground.check_shadow_rows(''.join(altered),buffers)
            except (AssertionError,ValueError,KeyError):rejected=True
            need(rejected,'Actual row-stream fault rejects: '+key+'/'+name)
            ground.check_shadow_rows(text,buffers)
            results.append(dict(case=key,fault=name,rejected=True,restoredPositivePassed=True))
        for name in ('shifted_idle_sole','missing_shadow','wrong_floor_body'):
            value=json.loads(json.dumps(c['result']['presentation']))
            # JSON integer slot keys are restored before the original gate.
            for record in value['records']:
                for field in('body','owned_shadow_pixels'):record[field]={int(k):v for k,v in record[field].items()}
            for field in('idle_sole_rows','idle_native_ground_offsets'):value[field]={int(k):v for k,v in value[field].items()}
            if name=='shifted_idle_sole':value['idle_sole_rows'][c['result']['side']]=[y-1 for y in value['idle_sole_rows'][c['result']['side']]]
            elif name=='missing_shadow':value['records'][0]['owned_shadow_pixels'][c['result']['side']]=0
            else:value['records'][0]['body'][c['result']['side']]['mismatches']=1;value['body_mismatches']=1
            rejected=False
            try:check.check_ground(value,c['result']['fighter'],c['result']['side'])
            except ValueError:rejected=True
            need(rejected,'Grounding gate fault rejects: '+key+'/'+name)
            check.check_ground(c['result']['presentation'],c['result']['fighter'],c['result']['side'])
            results.append(dict(case=key,fault=name,rejected=True,restoredPositivePassed=True))
    return results

def run(guest,gfx):
    need(not BASE.exists() and not OUT.exists() and not identity.census(),'Fresh four-case ground run, no native replay')
    source=json.loads(GUARD.read_text())
    need(source['passed'] and source['actualNativeParserAccepted'] and source['wholePhysicalGroundByteIdentical'] and
         not source['gameplayAccepted'] and all(sha(p)==h for p,h in source['inputHashes'].items()),'Whole physical native parser guard')
    initializer=ROOT/'audit_native_kano_laser_ui_initializer_source/report.json';init=json.loads(initializer.read_text())
    need(init['passed'] and not init['nativeGameplayAccepted'] and hashlib.sha256(guest).hexdigest().upper()==init['wholeExpectedGuestSHA256'] and
         hashlib.sha256(gfx).hexdigest().upper()==init['wholeExpectedGFXSHA256'] and all(sha(p)==h for p,h in init['inputHashes'].items()),
         'Same independently source-compiled entire current guest/GFX expectation, not cached game output')
    build=ROOT/current.NAME;metadata=json.loads((build/'build-info.json').read_text())
    pins=dict(metadata['input_hashes'])
    for p in(Path(__file__),LUA,GUARD,initializer,Path(current.__file__),Path(identity.__file__),Path(ground.__file__),
             Path(check.__file__),Path(decode_source.__file__),Path(latch_source.__file__),
             ROOT/'tools/verify_native_idle_feet_v635.py',ROOT/'tools/inspect_ground_presentation.py',
             ROOT/'mk2ks_ground_shadow_v815_probe.lua',build/'mkport_candidate.exe',build/'build-info.json',
             build/'roms/mk2ks/mk2ks.mdata',ROOT/'PLAY_LATEST_KANO_SONYA.cmd'):
        pins[str(p.resolve())]=sha(p)
    need(sha(build/'mkport_candidate.exe')==metadata['executable_sha256'],'Actual current private build')
    inspect_ram=model()
    for fighter,side in(('kano',1),('sonya',1),('kano',2),('sonya',2)):
        c=capture(fighter,side,guest,gfx,pins,inspect_ram)
        need(c['result']['passed'],'Complete original floor/shadow positive, no later dispatch after rejection')
    faults=fault_checks(RAM_CASES)
    need(not identity.census() and all(sha(p)==h for p,h in pins.items()),'All original native handles terminal, inputs conserved')
    for p in BASE.rglob('*'):
        if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.exe','.zip'),'No raw media/build/ROM copies');pins[str(p.resolve())]=sha(p)
    result=dict(passed=True,candidate=current.NAME,cases=COMPLETED,inputHashes=pins,faultChecks=faults,
        nativeGroundShadowCopies=sum(c['presentation']['native_shadow_copies']for c in COMPLETED),
        nativeShadowComponents=sum(c['presentation']['native_shadow_components']for c in COMPLETED),
        actualOwnedIdentityFields=sum(c['ownedIdentityFields']for c in COMPLETED),
        actualDisplayedNativeRasters=sum(c['displayedNativeRasters']for c in COMPLETED),
        boundedBothSlotDeadPoolGroundShadowAcceptance=True,allArenaFloorAcceptance=False,
        allMoveShadowStatesAcceptance=False,fullVisualTimelineAccepted=False,audioWaveformAcceptance=False,
        fullPortAcceptance=False,publicPlayableChanged=False,newNativeBoots=4,newBuilds=0,newROMCopies=0,
        newRawMedia=0,newZIPs=0,goalStatus='active',scope=__doc__)
    OUT.mkdir();save(OUT/'report.json',result)
    print(json.dumps(dict(passed=True,cases=4,nativeShadowCopies=result['nativeGroundShadowCopies'],faultChecks=len(faults))),flush=True)
    return result

def guarded_run(guest,gfx):
    try:return run(guest,gfx)
    except Exception as error:
        need(not OUT.exists(),'Never overwrite executed ground evidence');OUT.mkdir()
        save(OUT/'failure.json',dict(passed=False,error=repr(error),traceback=traceback.format_exc(),
             completedCases=COMPLETED,fullPortAcceptance=False,goalStatus='active'))
        print(json.dumps(dict(passed=False,error=repr(error))),flush=True)
        return None
