"""Current3172 earned Tomb whole-scene replay without disk raster/VRAM/PCM.

The original observer's CPU/FIFO/DMA/shift reads remain intact. Only its output
sinks change; the original physical driver omits its two PNG-only calls. The
native RNG outcome is observed, never prescribed. No all-stage/audio claim.
"""
import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import traceback
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
import current_tomb_ram_model_v3629 as model
import run_current_stage_palette_pixels_v3602 as stage
import verify_current_ground_shadow_v1859 as graphics
import inspect_native_shadow_rows_v635 as shadow
from verify_cpu_pair_display_v635_v3 import group
from verify_current_tomb_drop_physics_v3618 import phase_contract

ROOT,need,sha=stage.ROOT,stage.need,stage.sha
OBSERVER=ROOT/'mk2ks_native_tomb_ram_v3624.lua'
OUT=ROOT/'audit_v3635_current_native_tomb_ram_checked'
CASE=ROOT/'audit_v3634_current_kano_tomb_p1_native_ram'


def source_graphics(payload,pins):
    image=bytearray(graphics.graphics(pins))
    for header,magic,wanted_source,wanted_dest in (
        (0x1c0000,b'KFX1',0x1c4000,0x1e04000),(0x1c1000,b'KPI1',0x1e6000,0x1e50000),
        (0x1c2000,b'KPJ1',0x1f4000,0x1e60000),(0x1d0000,b'KBL1',0x1d4000,0x1e08000)):
        need(payload[header:header+4]==magic,'Actual native graphics upload header')
        source,count,dest=struct.unpack_from('<III',payload,header+4)
        need((source,dest)==(wanted_source,wanted_dest)and count>0 and
             source+count<=len(payload)and dest+count<=len(image), 'Complete original upload range')
        image[dest:dest+count]=payload[source:source+count]
    return bytes(image)


def controls():
    stage.controls()
    source=(ROOT/'mk2ks_native_tomb_display_v2062.lua').read_text()
    need(source.count("dofile('mk2ks_stage_branch_provenance_v1722.lua')")==1 and
         source.count("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()")==1 and
         source.count('screen:snapshot(file)')==1, 'Exactly three original observer substitutions')
    executed=source.replace("dofile('mk2ks_stage_branch_provenance_v1722.lua')",
                            "dofile('mk2ks_current_stage_provenance_v3595.lua')")
    executed=executed.replace("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",
                              'MK2KS_TOMB_RAM_SAVE(file,raw)').replace('screen:snapshot(file)',
                              'MK2KS_TOMB_RAM_PIXELS(file)')
    need(not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)|io\.open|snapshot\(',executed),
         'Original complete read-only observer, only sinks changed')
    wrapper=OBSERVER.read_text()
    need(wrapper.count('assert(count==1)')==3 and
         not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',wrapper),
         'RAM wrapper never changes gameplay/registers/controls')
    return hashlib.sha256(executed.encode()).hexdigest().upper()


def protocol_control():
    transport=model.Transport()
    samples=[(stage.REFERENCE/'display_base.bin').read_bytes(),
             (stage.REFERENCE/'display_pre_8173.bin').read_bytes()]
    encode=lambda raw: np.frombuffer(raw,dtype='<u4').astype('>u4').tobytes().hex().upper()
    prior=None
    for i,raw in enumerate(samples):
        row=dict(file=f'display_pre_{i}.bin',family='pre',bytes=str(len(raw)),prior=str(int(prior is not None)),
                 blocks='',block_bytes='64',encoding='u32le_numeric_hex_delta')
        blocks=[f'{first//64}:{encode(raw[first:first+64])}' for first in range(0,len(raw),64)
                if prior is None or raw[first:first+64]!=prior[first:first+64]]
        row['blocks']=str(len(blocks)); encoded=','.join(blocks)
        need(transport.decode(row,encoded)==raw,'Actual native whole transport round-trip, no byte tolerance')
        prior=raw
    faults=[]
    row=dict(file='display_pre_2.bin',family='pre',bytes=str(len(prior)),prior='1',blocks='1',
             block_bytes='64',encoding='u32le_numeric_hex_delta')
    for label,encoded in [('duplicate block','0:'+encode(prior[:64])+',0:'+encode(prior[:64])),
                          ('out of range',str(len(prior)//64)+':'+encode(prior[:64])),
                          ('omitted word','0:'+encode(prior[:60]))]:
        changed=dict(row);changed['blocks']=str(len(encoded.split(',')))
        try: copy.deepcopy(transport).decode(changed,encoded)
        except ValueError as error: faults.append(dict(kind=label,rejectedBy=str(error)))
        else: raise ValueError('Invalid native transport accepted')
    return dict(actualNativeWholeRoundTrips=2,logicalBytes=sum(map(len,samples)),faults=faults)


def positive_control():
    old=json.loads(stage.OLD_REPORT.read_text())
    need(old['passed']and sha(stage.REFERENCE/'run.log')==old['inputHashes'][str(stage.REFERENCE/'run.log')],
         'Retained source-qualified original control log')
    _,guest,_,_,_=stage.inventory.current.expected_current()
    payload=(ROOT/'diagnostic_v1836_ball_register_boundary/roms/mk2ks/mk2ks.mdata').read_bytes()
    pins={};scene=model.Model(guest,payload,source_graphics(payload,pins))
    for line in (stage.REFERENCE/'run.log').open(encoding='utf-8-sig'):
        parsed=model.parse(line)
        if parsed:
            kind,row=parsed
            if kind in ('FLOOR_BASE','FLOOR_SHIFT_DATA','FLOOR_PRE_FRAME','FLOOR_LATCH','FLOOR_HELD'):
                file=stage.REFERENCE/row['file']
                need(sha(file)==old['inputHashes'][str(file)],'Source-bound existing raw control')
                scene.raw[row['file']]=file.read_bytes()
            if kind=='FLOOR_DISPLAY':
                file=stage.REFERENCE/row['palette_file']
                need(sha(file)==old['inputHashes'][str(file)],'Source-bound existing palette control')
                scene.raw[row['palette_file']]=file.read_bytes()
            if kind=='FLOOR_SNAP':
                file=stage.REFERENCE/'snap'/row['file']
                need(sha(file)==old['inputHashes'][str(file)],'Source-bound existing raster control')
                scene.rgb[row['file']]=np.asarray(Image.open(file).convert('RGB'))
        scene.line(line)
        if len(scene.records)==3:break
    need(len(scene.records)==3 and scene.pre_count==4 and scene.flip_count==3
         and scene.loads==scene.fills and scene.transfers>0 and scene.palette_checks>0,
         'Three actual continuous original fields, native shifts/palettes/shadows/visible scanouts')
    return dict(passed=True,retainedBuildOnly=True,frames=3,exactRGBPixels=3*400*254,
                initialBaseCount=1,exactPreBuffers=scene.pre_count,exactFlips=scene.flip_count,
                nativeShiftTransfers=scene.transfers,paletteChecks=scene.palette_checks,
                rejectedActualPixelTargetFaults=scene.counterexamples,
                transport=protocol_control(),noNewRuntimeOrDiskRasterCopies=True)


def scene_contract(scene,log,guest,payload):
    groups=scene.groups
    need(len(groups['FLOOR_BEGIN'])==len(groups['FLOOR_RESULT'])==len(groups['FLOOR_RETIRED'])==1,
         'One actual earned native Tomb action and actor retirement')
    begin,result,retired=(groups[key][0]for key in ('FLOOR_BEGIN','FLOOR_RESULT','FLOOR_RETIRED'))
    origin,end=begin['origin'],retired['frame']
    need((begin['id'],begin['entry'])==(17,0xff8bdfe0)and
         result['origin']==origin and result['retired']==end and
         [r['frame']for r in scene.records]==list(range(origin+1,end+31))and
         result['snapshots']==len(scene.records)>500 and
         (retired['mode'],retired['p1'],retired['p2'],retired['victim_health'])==(3,0,0,0),
         'Complete true Kano native action through retirement plus30, no held/drop normalization')
    physical=('MK2_STAGE_BOOT ','MK2_STAGE_INPUT ','MK2_STAGE_DAMAGE ','MK2_STAGE_MATCH ',
              'MK2_STAGE_SELECT ','MK2_STAGE_SELECT_ID ','MK2_STAGE_WINDOW ','MK2_STAGE_COMMAND ','MK2_STAGE_RESULT ')
    old=(stage.REFERENCE/'run.log').read_text(encoding='utf-8-sig')
    need([line for line in log.splitlines()if line.startswith(physical)]==
         [line for line in old.splitlines()if line.startswith(physical)],
         'All original physical controls/earned damage/select/window/command/terminal records')
    original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
    for first,last in ((0xff804040,0xff804470),(0xff8eaf00,0xff8eb490),(0xff876650,0xff876b40),
                       (0xff80e980,0xff80ecf0),(0xff82b800,0xff82bca0)):
        lo,hi=(first-0xff800000)//8,(last-0xff800000)//8
        need(guest[lo:hi]==original[lo:hi],'Unchanged original projection/Tomb/RNG/fall/teardown code')
    states=groups['FLOOR_STATE'];first=states[0]
    actors={s:first[f'p{s}']for s in(1,2)}; mains={s:first[f'main{s}']for s in(1,2)}
    need([r['frame']for r in states]==list(range(origin,end+31)), 'Complete native scene states')
    anchors={17:134,18:135}
    for row in states:
        need(all(row[f'main{s}']==mains[s]and row[f'roster{s}']==(16+s)for s in(1,2)),
             'Actual true IDs/main schedulers remain native, no proxies')
        need(all(row[f'p{s}']==actors[s]for s in(1,2))if row['frame']<end else
             row['p1']==row['p2']==0 and row['mode']==3, 'Native physical actor lifetime')
    for row in groups['FLOOR_BODY']:
        s=row['slot']
        need(row['actor']==row['owner']==actors[s]and row['main']==mains[s]and
             row['id']==row['roster']==16+s and row['floor']==220-anchors[row['id']]
             and row['frame']<end,'Own actual body/main/floor until native retirement')
    branches=[dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()
              if line.startswith('MK2_STAGE_PROVENANCE_BRANCH ')]
    entries=('FF8EB0D0','FF8EB150','FF80EC20','FF8EB1A0','FF8EB1B0','FF8EB200','FF8EB290','FF876650','FF8EB3C0','FF8EB400')
    branches=[r for r in branches if int(r['frame'])>=origin and r['entry']in entries]
    value=int(branches[3]['a0'],16);branch=int(branches[0]['frame']);dropped=value<50
    need([r['entry']for r in branches]==list(entries[:4])+(
         list(entries[4:9])if dropped else [entries[9]]) and branches[2]['a0']=='00000032'
         and 0<=value<1000 and all(r['io0']=='FFFFFFFF'and r['a8']==r['actor']==f'{actors[2]:08X}'
         and r['a13']==r['main']==f'{mains[2]:08X}'for r in branches),
         'Actual original unpressed-control RNG branch, not prescribed old outcome')
    callbacks={int(r['frame']):r for r in
        [dict(re.findall(r'(\w+)=([^\s]+)',line))for line in log.splitlines()
         if line.startswith('MK2_STAGE_PROVENANCE_FIELD ')]if origin<int(r['frame'])<=end}
    if dropped: motion=phase_contract(callbacks,branch,85)
    else:
        held=[r for f,r in callbacks.items()if f>branch]
        need(held and all((int(r['y']),int(r['vy'],16),int(r['gravity'],16),int(r['action'],16))==
             (-174,0,0,0x503)for r in held),'Complete actual original held ceiling branch')
        motion=dict(ceiling=-174,heldCallbacks=len(held))
    queues={(q['frame'],q['cursor']):q for q in groups['FLOOR_QUEUE']}
    inventory={(q['frame'],q['cursor']):q for q in groups['FLOOR_ALL_QUEUE']}
    transforms={(t['frame'],t['cursor']):t for t in groups['FLOOR_QUEUE_TRANSFORM']}
    need(len(queues)==len(groups['FLOOR_QUEUE'])and len(inventory)==len(groups['FLOOR_ALL_QUEUE'])>len(queues)
         and set(transforms)==set(queues),'Complete actual body/all native FIFO publications and transforms')
    parts=defaultdict(list);published=defaultdict(list)
    for p in groups['FLOOR_QUEUE_PART']:parts[p['frame'],p['cursor']].append(p)
    for key,q in inventory.items():
        if q['actor'] in actors.values():need(key in queues,'No hidden physical body publication')
    signed= model.erase.short
    for key,q in queues.items():
        s=q['slot'];need(s in(1,2)and q['actor']==q['owner']==q['parent']==actors[s]
             and q['main']==mains[s]and q['id']==q['roster']==16+s and q['kind']==0
             and q['multipart']==1 and q['frame']<end,'True physical FIFO owner')
        need(key in inventory and all(q[k]==inventory[key][k]for k in
             ('actor','source','pose','cache','id','body','facing','bank','pc')), 'Actual native queue inventory agrees')
        composition=group(q,payload,guest)
        need(len(composition)==len(parts[key])and all(all(p[k]==v for k,v in expected.items())
             for p,expected in zip(parts[key],composition)),'Every published original-art composite source/offset/flip')
        need(q['row']==q['cache']+112*q['part']and q['pc']==0xff804420,'Original component cache iterator')
        t=transforms[key];part=composition[q['part']]
        need(all(t[k]==q[k]for k in('slot','actor','main'))and
             t['world']==((q['y']&65535)<<16)|(q['x']&65535)and
             t['floor']==q['floor']==t['stageY']-anchors[q['id']], 'Actual world/camera/ground anchor')
        x,y=signed(t['world']),signed(t['world']>>16)
        if not t['a7']&1:x-=signed(t['camera']);y-=signed(t['camera']>>16)
        x-=part['dx'];y-=part['dy'];command=q['command']>>16
        if command&16:x+=part['width']-1
        if command&32:y+=part['height']-1
        x+=signed(t['display']);y+=signed(t['display']>>16)
        need((q['xy']&1023,q['xy']>>16&511)==(x&1023,y&511),'Exact native camera/cache/flip projection')
        published[q['cursor']].append(q)
    dmas={r['event']:r for r in groups['FLOOR_DMA']};regs={r['event']:r for r in groups['FLOOR_DMA_REGS']}
    dispatch={r['event']:r for r in groups['FLOOR_QUEUE_DISPATCH']}
    need(set(regs)==set(dmas)and len(dispatch)==len(groups['FLOOR_QUEUE_DISPATCH']), 'Complete native DMA cursor inventory')
    draws=defaultdict(int);poses=defaultdict(set)
    for event,d in dmas.items():
        candidates=[q for q in published[regs[event]['b14']+192]if q['frame']<=d['frame']]
        q=max(candidates,key=lambda r:r['frame'])if candidates else None
        owned=bool(q and d['command']&15==2 and q['source']==d['source'])
        need((event in dispatch)==owned and d['slot']==(q['slot']if owned else 0),
             'Every actual FIFO dispatch classified by cursor, never palette bank')
        if not owned:continue
        actual=dispatch[event];part=group(q,payload,guest)[q['part']]
        need(queues[actual['queue_frame'],actual['cursor']]==q and
             all(actual[k]==q[k]for k in('actor','main','slot'))and d['source']==part['source']and
             (d['width'],d['height'])==(part['width'],part['height'])and d['command']==part['command']|0x8002
             and (q['xy']&1023,q['xy']>>16&511,q['bank']&0x7f00)==(d['x'],d['y'],d['palette']),
             'Native dispatched body source/size/command/position/palette unchanged')
        draws[q['slot']]+=1;poses[q['slot']].add(q['pose'])
    shadow.data=lambda _: (groups,scene.buffers,None,None,scene.owners)
    shadows=shadow.inspect(None)
    need(shadows['rowStreamVerified']and not shadows['failures']and not shadows['oversized_rows']and
         set(map(tuple,shadows['identities']))=={(1,17),(2,18)},'All actual owned compressed native shadow rows')
    need(scene.pre_count==len(groups['FLOOR_PRE_FRAME'])and
         scene.flip_count==len(groups['FLOOR_LATCH'])and scene.loads==scene.fills>0 and
         scene.palette_checks>len(scene.records)and all(draws[s]>100 for s in(1,2))and
         not scene.events and not scene.raw and not scene.rgb,'No omitted target/shift/field/palette/body data')
    return dict(origin=origin,retired=end,actualNativeRandomValue=value,nativeDrop=dropped,nativeMotion=motion,
                sourceBoundProjections=len(queues),nativeShadowCopies=shadows['checked_copies'],
                sourceGraphicsStreams=len(scene.buffers),ownedBodyDispatches=dict(draws),
                visiblePoseInventory={s:sorted(v)for s,v in poses.items()})


def run():
    need(not CASE.exists()and not OUT.exists(),'Fresh immutable RAM native scene')
    controls_sha=controls(); positive=positive_control()
    print('Positive control: three source-perfect native fields, one continuous base, transport exact',flush=True)
    guest,_,payload,_,_=stage.inventory.current.expected_current(); pins={}
    image=source_graphics(payload,pins);candidate=ROOT/stage.NAME
    build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    files={Path(p)for p in build['input_hashes']}|{OBSERVER,Path(__file__).resolve(),Path(model.__file__),
        candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
        ROOT/'mk2ks_native_tomb_display_v2062.lua',ROOT/'mk2ks_current_stage_ram_driver_v3594.lua',
        ROOT/'mk2ks_current_stage_provenance_v3595.lua',ROOT/'mk2ks_native_stage_performer_v806.lua',
        ROOT/'mk2ks_stage_branch_provenance_v1722.lua',stage.OLD_REPORT,stage.REFERENCE/'run.log',
        ROOT/'audit_v3623_current_tomb_drop_full_scope_checkpoint/checkpoint.json'}
    for module in list(sys.modules.values()):
        file=getattr(module,'__file__',None)
        if file and Path(file).resolve().is_relative_to(ROOT/'tools'):files.add(Path(file).resolve())
    files.update(Path(p)for p in pins)
    for directory in ('roms/mk2ks','samples/mk2ks','artwork'):files.update((ROOT/directory).glob('*'))
    before={str(p.resolve()):sha(p)for p in files if p.is_file()}
    need(all(before[str(Path(p).resolve())]==value for p,value in build['input_hashes'].items())and
         sha(candidate/'mkport_candidate.exe')==build['executable_sha256']and
         sha(candidate/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256']and
         (candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()==payload,'Current executable/payload and full actual compiled manifest')
    CASE.mkdir();result=subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(CASE)],capture_output=True,text=True)
    need(result.returncode==0,'Small diagnostic leaf inherits NTFS lossless compression')
    (CASE/'input_hashes_before.json').write_text(json.dumps(before,indent=2)+'\n')
    for file in (OBSERVER,Path(__file__).resolve(),Path(model.__file__)):
        target=CASE/'input_sources'/file.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(file,target);need(sha(target)==sha(file),'Exact executed diagnostic source snapshot')
    scene=model.Model(guest,payload,image);transport=model.Transport();errors=[];rgb_records=[]
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_STAGE_SIDE='1',MK2KS_STAGE_WINNER='kano',MK2KS_STAGE_ARENA='1',
               MK2KS_STAGE_CASE='positive',MK2KS_STAGE_OUT=str(CASE))
    cmd=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),
        '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat',
        '-inipath',str(CASE),'-video','none','-sound','none','-samplerate','48000','-noautoframeskip','-frameskip','0',
        '-nothrottle','-str','900','-snapsize','400x254','-cfg_directory',str(CASE/'cfg'),
        '-nvram_directory',str(CASE/'nvram'),'-snapshot_directory',str(CASE/'snap'),'-autoboot_script',str(OBSERVER)]
    ram_guest=None
    with (CASE/'stderr.log').open('wb')as stderr,subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=stderr)as process:
        print(f'Current full native Tomb RAM replay PID={process.pid}; original physical inputs',flush=True)
        with (CASE/'run.log').open('w',encoding='utf-8')as log:
            for binary in iter(process.stdout.readline,b''):
                if binary.startswith((b'MK2_TOMB_RAM_BUFFER ',b'MK2_TOMB_RAM_PIXELS ')):
                    header=binary.decode('ascii').strip();row=dict(re.findall(r'(\w+)=([^\s]+)',header))
                    encoded=process.stdout.readline().decode('ascii').strip()
                    try:
                        if binary.startswith(b'MK2_TOMB_RAM_BUFFER '):
                            raw=transport.decode(row,encoded)
                            if row['file']=='guest_maincpu.bin':
                                need(raw==guest,'Complete actual initialized current guest in RAM');ram_guest=model.digest(raw)
                            elif not errors:scene.raw[row['file']]=raw
                            log.write('MK2_TOMB_RAM_BUFFER_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(raw)+'\n')
                        else:
                            need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and
                                 row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,
                                 'Complete exact native RGB transfer')
                            words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
                            rgb=np.stack([(words>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
                            rgb_records.append(dict(file=row['file'],rgbSHA256=model.digest(rgb.tobytes())))
                            if not errors:scene.rgb[row['file']]=rgb
                            log.write('MK2_TOMB_RAM_PIXELS_CHECKED '+header.split(' ',1)[1]+' sha256='+model.digest(rgb.tobytes())+'\n')
                    except Exception as error:
                        if not errors:errors.append(dict(header=header,error=repr(error),traceback=traceback.format_exc()))
                else:
                    need(not re.match(b'^[A-F0-9]{1000}',binary),'No raw RAM raster/VRAM written to logs')
                    line=binary.decode('utf-8');log.write(line)
                    if not errors:
                        try:scene.line(line)
                        except Exception as error:errors.append(dict(line=line.rstrip(),error=repr(error),traceback=traceback.format_exc()))
                    if len(scene.records)and len(scene.records)%100==0 and line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP '):
                        print(f'Current: {len(scene.records)} whole fields exact; {scene.transfers} original erase transfers',flush=True)
        code=process.wait()
    log=(CASE/'run.log').read_text();stderr=(CASE/'stderr.log').read_text()
    terminal=dict(captureCompleted=True,exit_code=code,candidate=stage.NAME,guest_writes=0,assistance='none',
                  cheats_enabled=False,input_hashes=before,ramGuestSHA256=ram_guest,
                  observedRGBFields=len(rgb_records),modelExactFields=len(scene.records),modelErrors=errors,
                  executable_sha256=build['executable_sha256'],payload_sha256=build['payload_sha256'],
                  rawImageAudioVRAMPlayableCopiesWritten=0,diagnosticGuestDumps=1,fullPortAcceptance=False)
    (CASE/'result.json').write_text(json.dumps(terminal,indent=2)+'\n')
    (CASE/'buffer_digests.json').write_text(json.dumps(transport.records,indent=2)+'\n')
    (CASE/'visible_digests.json').write_text(json.dumps(rgb_records,indent=2)+'\n')
    (CASE/'continuous_scene_records.json').write_text(json.dumps(scene.records,indent=2)+'\n')
    need(code==0 and not errors and ram_guest==model.digest(guest)and
         (CASE/'guest_maincpu.bin').read_bytes()==guest and not re.search(
         r'LUA ERROR|Lua error|stack traceback|Fatal error|WRONG CHECKSUMS|might not run correctly',log+stderr,re.I),
         'Actual current terminal, whole guest and unweakened continuous native scene model')
    contract=scene_contract(scene,log,guest,payload)
    for file,wanted in before.items():need(sha(file)==wanted,'Actual executed relevant input unchanged')
    pins.update(before)
    for file in CASE.rglob('*'):
        if file.is_file():pins[str(file)]=sha(file)
    return dict(passed=True,candidate=stage.NAME,currentActualEarnedKanoP1TombWholeSceneRenderShadowEraseAccepted=True,
        nativeScene=contract,sampledFrames=len(scene.records),exactRGBPixels=len(scene.records)*400*254,
        continuousExactPreBuffers=scene.pre_count,continuousExactFlips=scene.flip_count,
        continuouslyExactHeldScanouts=len(scene.records)-scene.flip_count,oneInitialBaseOnly=True,
        laterTargetVRAMNeverUsedAsAnchors=True,nativeShiftLoads=scene.loads,nativeShiftFills=scene.fills,
        nativeShiftTransfers=scene.transfers,directNativeShiftStores=scene.direct,
        exactCPUWrites=scene.cpu_count,fullPhysicalPaletteChecks=scene.palette_checks,
        finalVisibleShadowPixels=sum(r['shadowPixels']for r in scene.records),
        rejectedActualPixelTargetFaults=scene.counterexamples,retainedOriginalPositiveControl=positive,
        executedOriginalObserverWithOnlySinksReplacedSHA256=controls_sha,
        observerIndependentGameplayEquivalenceAccepted=False,allVictimMirrorBranchAudioAcceptance=False,
        stageAudioFidelityAccepted=False,publicReleaseChanged=False,fullPortAcceptance=False,
        rawImageAudioVRAMPlayableCopiesWritten=0,inputHashes=pins,scope=__doc__)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--positive-control',action='store_true');args=parser.parse_args()
    if args.positive_control:
        print(json.dumps(positive_control(),indent=2));raise SystemExit(0)
    need(not OUT.exists(),'Never overwrite executed evidence')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    OUT.mkdir();file=OUT/'report.json';file.write_text(json.dumps(report,indent=2)+'\n')
    wanted=sha(file);result=subprocess.run(['compact.exe','/C','/I','/Q',str(file)],capture_output=True,text=True)
    need(result.returncode==0 and sha(file)==wanted,'Lossless compact bounded result')
    print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','retainedOriginalPositiveControl')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)


