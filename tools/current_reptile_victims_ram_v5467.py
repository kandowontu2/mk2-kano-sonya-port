"""Current real Reptile victims, original physical/FIFO/floor contract in RAM.

Rebuild selected source-PNG encoding independently in RAM, with the original
alpha/scaling/quantization rules. Not a new asset, game build, proxy, guest
write, savestate, raw-media dump or universal art/audio/arena acceptance.
"""
import concurrent.futures, datetime, inspect, json, os, re, struct, subprocess, textwrap, traceback
from pathlib import Path
import numpy as np
from PIL import Image
import current_payload_metadata_context_v5229 as current
import verify_native_death_grounding_v990 as original
import build_native_death_art_v900 as assets

ROOT, need, sha = current.ROOT, current.need, current.sha
PARENT = ROOT / 'audit_v5466_current_primary_audio_qualified_progress/progress.json'
BASE = ROOT / 'audit_v5468_current_reptile_victims_ram'
OUT = ROOT / 'audit_v5469_current_reptile_victims_progress'
LUA = ROOT / 'mk2ks_current_reptile_ram_v5467.lua'
COMPLETED = []


def save(p,v):
    p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')


def digest(raw):
    return assets.sha(raw).upper()


def independent_art(guest,payload,pins):
    donor_path = ROOT / 'mk3/mk3-maincpu.bin'
    donor = donor_path.read_bytes()
    need(digest(donor) == assets.DONOR_SHA.upper(), 'Original independently owned MK3 palette ROM')
    pins[str(donor_path)] = sha(donor_path)
    parts = {}
    for filename,wanted in assets.ASSETS.items():
        p = ROOT / 'art_native_death_v893' / filename
        need(sha(p) == wanted.upper(), 'Exact original selected native-death source PNG')
        pins[str(p)] = sha(p)
        parts[filename] = assets.components(p)
    first,last,sonya = parts['kano-bodies-first-five.png'],parts['kano-bodies-last-two.png'],parts['sonya-bodies.png']
    need((len(first),len(last),len(sonya)) == (6,2,7), 'Original isolated native-death components')
    bodies = dict(kano=first[:5]+last,sonya=sonya)
    factors = dict(kano=[110/first[0][1].height]*5+[130/last[1][1].width]*2,
                   sonya=[105/sonya[0][1].height]*5+[125/sonya[6][1].width]*2)
    pixel_at,descriptor_at = assets.PIXELS,assets.DESCRIPTORS
    result = dict(fighters={})
    for fighter_index,fighter in enumerate(('kano','sonya')):
        heads = parts[fighter+'-heads.png']
        need(len(heads) == 7, 'Original seven separate owned head components')
        normal = assets.palettes.palette(donor,(0x92bbc,0x92cf2)[fighter_index])
        records = []
        for kind,source_parts,scales in (('body',bodies[fighter],factors[fighter]),('head',heads,[27/heads[0][1].height]*7)):
            for pose,(part,factor) in enumerate(zip(source_parts,scales)):
                box,image,area = part
                size = (round(image.width*factor),round(image.height*factor))
                indices = assets.palettes.quantize(image.resize(size,Image.Resampling.LANCZOS),normal)
                raw = indices.tobytes()
                packed = assets.codec.pack_indices(raw)
                need(assets.unpack(packed,len(raw)) == raw and max(raw) < 64 and any(raw), 'Whole independent native6bpp pixel roundtrip')
                descriptor = 0xff800000+(assets.ROM_DESCRIPTORS+descriptor_at-assets.DESCRIPTORS)*8
                width,height = size
                left,top = (assets.LEFTS[pose],assets.BOTTOMS[fighter]-height) if kind=='body' else (-(width//2),-(height//2))
                graphic = (assets.GFX+pixel_at-assets.PIXELS)*8
                palette = (0xfffed000,0xfffed800)[fighter_index]
                encoded = struct.pack('<4hIHIH',width,height,-left,-top,graphic,0x6000,palette,0)
                need(len(encoded) == 20 and payload[descriptor_at:descriptor_at+20] == encoded and
                     guest[(descriptor-0xff800000)//8:(descriptor-0xff800000)//8+20] == encoded,
                     'Entire current descriptor independently source-PNG/donor-palette encoded')
                need(payload[pixel_at:pixel_at+len(packed)] == packed, 'Every actual current packed native-death pixel independently source-exact')
                if kind=='body':
                    at = assets.offset(assets.GROUPS[fighter][pose])
                    need(struct.unpack_from('<2I',payload,at) == (descriptor,0), 'Own exact headless body group, no Liu substitute')
                else:
                    at = assets.offset(assets.STREAMS[fighter][1])+pose*4
                    need(struct.unpack_from('<I',payload,at)[0] == descriptor, 'Own exact detached-head stream, no Liu substitute')
                records.append(dict(kind=kind,pose=pose,size=list(size),descriptor=f'{descriptor:08X}',graphics=f'{graphic:08X}',
                                    indices_sha256=digest(raw),packed_bytes=len(packed)))
                padding = (-(pixel_at+len(packed))) & 3
                pixel_at += len(packed)+padding
                descriptor_at += 20
        result['fighters'][fighter] = dict(frames=records)
    count = pixel_at-assets.PIXELS
    need(count == 49228 and descriptor_at-assets.DESCRIPTORS == 560, 'Complete original28-frame native-death allocation')
    result['pixel_bytes'] = count
    return result,payload[assets.PIXELS:pixel_at]


def physical_contract():
    source = inspect.getsource(original.verify)
    first = "  name=result['player'];side=result['victim_slot'];identity=17 if name=='kano'else 18"
    last = ' need(len(summaries)==4'
    need(source.count(first) == source.count(last) == 1, 'Whole original990 native physical/art contract boundaries')
    body = textwrap.dedent(source[source.index(first):source.index(last)])
    edits = {
      'if len(actions)!=1 or len(heads)!=1 or len(wraps)!=1:continue':
      "if len(actions)!=1 or len(heads)!=1 or len(wraps)!=1:raise ValueError('Invalid single-context native chronology')",
      "original_case=case.replace('audit_v988_','audit_v904_',1)\nprevious_text=(ROOT/original_case/'run.log').read_text(encoding='utf-8-sig')\nneed(rows==records(previous_text),case+': unchanged genuine input/state/fatality replay after read-only camera instrumentation')":
      "need(result['entireOriginal887PhysicalControllerRetained'],case+': whole original controller retained; historical media/replay not substituted')",
      "pictures=directory/'snap'\nfor age in range(0,301,10):\n path=pictures/f'reptile_victim_{start}_{age:03d}.png'\n need(path.is_file()and Image.open(path).size==(400,254),case+': actual picture '+str(age))\n previous=ROOT/original_case/'snap'/path.name\n need(previous.is_file()and path.read_bytes()==previous.read_bytes(),case+': unchanged actual rendered snapshot after read-only camera instrumentation')\n if check_files and path.is_file():pins[str(path)]=digest(path)":
      "need(list(images)==[f'reptile_victim_{start}_{age:03d}.png'for age in range(0,301,10)]and all(image.shape==(254,400,3)for image in images.values()),case+': all31 actual full displayed native rasters transported in RAM')",
      "payload=(ROOT/'diagnostic_v958_owned_cage_torso_grounding/roms/mk2ks/mk2ks.mdata').read_bytes()":
      "# Actual current payload is supplied, independently source-PNG-bound.",
      "guest=(directory/'guest_maincpu.bin').read_bytes()": "# Actual whole initialized current guest supplied from RAM.",
      'wanted_guest=gore.expected_guest()': '# Whole current guest expectation independently reconstructed before cold boot.',
      "gfx=(directory/'native_death_gfx.bin').read_bytes()": 'gfx=actual_gfx',
      "encoding=json.loads((ROOT/'audit_v900_native_death_grounding_encoding/report.json').read_text())":
      '# Original selected source images re-encoded independently in RAM, not a restored old media report.',
    }
    for before,after in edits.items():
        need(body.count(before) == 1, 'Exact original transport/version-only adaptation: '+before.splitlines()[0])
        body = body.replace(before,after)
    function = 'def contract(text,result,guest,actual_gfx,encoding,images,wanted_guest,payload):\n    errors=[];pins={};summaries={};check_files=False;case="actual_current_reptile";directory=None\n    def need(ok,label):\n        if not ok:errors.append(label)\n'+textwrap.indent(body,'    ')+"    if errors:raise ValueError(' | '.join(errors))\n    return summaries[case]\n"
    scope = dict(original.__dict__)
    scope.update(EXE=current.EXE_SHA,PAYLOAD=current.PAYLOAD_SHA)
    exec(compile(function,__file__+'.whole_original990_RAM_transport_current_source','exec'),scope)
    return scope['contract'],digest(function.encode())


def faults(log,result,ram,reference,images,guest,payload,contract):
    positive = contract(log,result,ram['guest_maincpu.bin'],ram['native_death_gfx.bin'],reference,images,guest,payload)
    out=[]
    def reject(label,pattern,replacement):
        changed,count = re.subn(pattern,replacement,log,count=1,flags=re.M)
        need(count == 1 and changed != log, 'Effective actual native-record fault: '+label)
        try:contract(changed,result,ram['guest_maincpu.bin'],ram['native_death_gfx.bin'],reference,images,guest,payload)
        except ValueError as error:out.append(dict(label=label,rejectedBy=str(error)))
        else:raise ValueError('Actual native-record counterexample accepted: '+label)
    reject('wrong actual native victim identity',r'ids=9,(17|18)',r'ids=9,1')
    reject('non-native health writer',r'pc=FF836700',r'pc=FF838860')
    reject('missing actual original action',r'^MK2_REPTILE_V879_ACTION .*\n','')
    reject('missing actual original wrap',r'^MK2_REPTILE_V879_WRAP .*\n','')
    reject('unearned actual damage',r'^MK2_REPTILE_V879_HEALTH .*before=161 after=121 pc=FF836700\n','')
    reject('missing genuine Low Punch command',r'^MK2_REPTILE_V879_INPUT .*button=Low_Punch\n','')
    reject('wrong actual victim table row offset',r'(data=)FFF[CD]( mask=FFFF pc=FF8C8AB0)',r'\g<1>0000\2')
    reject('wrong actual native table consumer',r'pc=FF8C8AB0',r'pc=FFA59F10')
    reject('foreign actual victim palette',r'(pointer=)FFFED[08]00',r'\g<1>FFADD0D0')
    reject('Liu head substituted for actual victim',r'(descriptor=)FFFD(5460|5D20)',r'\g<1>FFB4A4B0')
    reject('actual body loses owned floor',r'(^MK2_DEATH_ART_V897_QUEUE .*?y=)(-?\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('foreign actual art owner',r'(^MK2_DEATH_ART_V897_QUEUE .*?owner=)[0-9A-F]+',r'\g<1>01000000')
    reject('actual native FIFO not bound',r'queue_match=1',r'queue_match=0')
    reject('wrong actual DMA dimensions',r'(^MK2_DEATH_ART_V897_DMA .*?width=)(\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('actual collapse floats one raster pixel',r'(^MK2_DEATH_ART_V897_DMA .*? y=)(\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('actual art lingers after continuation',r'(^MK2_DEATH_ART_V897_RESULT .*?last=)\d+',r'\g<1>5197')
    reject('wrong actual native display origin',r'(^MK2_DEATH_ART_V897_QUEUE .*?displayY=)(-?\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('wrong actual native stage floor',r'(^MK2_DEATH_ART_V897_QUEUE .*?stageY=)(-?\d+)',lambda m:m[1]+str(int(m[2])+1))
    reject('actual DMA loses same-frame queue',r'(^MK2_DEATH_ART_V897_QUEUE frame=)\d+',r'\g<1>1')
    reject('wrong actual original wrap age',r'age=187 pc=FF8C9690',r'age=188 pc=FF8C9690')
    reject('boot picture falsely claimed as finisher',r'(^MK2_REPTILE_V879_DISPLAY frame=)\d+',r'\g<1>1')
    need(contract(log,result,ram['guest_maincpu.bin'],ram['native_death_gfx.bin'],reference,images,guest,payload)==positive,
         'Same actual native positive restored after every effective record counterexample')
    return out


def capture(spec,guest,payload,expected_gfx,reference,pins):
    fighter,side=spec
    folder=BASE/f'{fighter}_p{side}'
    need(not folder.exists(),'Fresh immutable current Reptile victim context')
    folder.mkdir(parents=True)
    for name in ('cfg','nvram','snap'):(folder/name).mkdir()
    frozen=dict(pins)
    save(folder/'input_hashes_before.json',frozen)
    build=ROOT/current.NAME
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_PORT_ROOT=str(ROOT),MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_REPTILE_AUDIT_DIR=str(folder))
    command=[str(build/'mkport_candidate.exe'),'mk2ks','-rompath',str(build/'roms')+';'+str(ROOT/'roms'),
      '-samplepath',str(ROOT/'samples'),'-samples','-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),
      '-video','none','-sound','none','-noautoframeskip','-frameskip','0','-nothrottle','-str','95','-snapsize','400x254',
      '-cfg_directory',str(folder/'cfg'),'-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(LUA)]
    ram,images,headers={},{},[]
    with (folder/'stderr.log').open('w',encoding='utf-8')as err:
        proc=subprocess.Popen(command,cwd=folder,env=env,stdout=subprocess.PIPE,stderr=err,text=True,encoding='utf-8',creationflags=subprocess.CREATE_NO_WINDOW)
        save(folder/'process.json',dict(pid=proc.pid,command=command,env={k:v for k,v in env.items()if k.startswith('MK2KS_')}))
        print(f'{fighter} P{side} actual native PID={proc.pid}',flush=True)
        with (folder/'run.log').open('w',encoding='utf-8')as out:
            for line in proc.stdout:
                if line.startswith('MK2_CURRENT_REPTILE_RAM_'):
                    tag=line.split()[0];r=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(r.pop('hex'))
                    need(len(raw)==int(r['bytes']),'Whole actual RAM transport buffer');r['sha256']=digest(raw)
                    if tag.endswith('_DATA'):
                        need(r['filename']not in ram,'Unique actual initialized guest/GFX RAM buffers');ram[r['filename']]=raw
                    else:
                        need(tag.endswith('_RGB')and(r['width'],r['height'],len(raw))==('400','254',406400)and r['filename']not in images,
                             'Actual whole unique400x254 displayed native frame')
                        images[r['filename']]=np.frombuffer(raw,np.uint8).reshape(254,400,4)[:,:,2::-1].copy();headers.append(r)
                    out.write(tag+'_DIGEST '+' '.join(k+'='+str(v)for k,v in r.items())+'\n')
                else:need('hex='not in line,'No raw image/guest/GFX persisted');out.write(line)
            code=proc.wait()
    log=(folder/'run.log').read_text();error=(folder/'stderr.log').read_text()
    need(code==0 and not error and not re.search(r'LUA ERROR|stack traceback|Fatal error|access violation|WRONG CHECKSUMS|might not run correctly',log,re.I),
         'Actual native warning-free terminal0')
    need(ram.get('guest_maincpu.bin')==guest and ram.get('native_death_gfx.bin')==expected_gfx,
         'Entire actual current initialized guest and independently source-PNG encoded death GFX exact')
    result=dict(exit_code=code,candidate=current.NAME,player=fighter,victim_slot=side,winner_slot=3-side,seconds=95,
      executable_sha256=current.EXE_SHA,payload_sha256=current.PAYLOAD_SHA,assistance='none',cheats_enabled=False,
      entireOriginal887PhysicalControllerRetained=True,input_hashes=frozen,nativePID=proc.pid)
    contract,contract_sha=physical_contract()
    state=contract(log,result,ram['guest_maincpu.bin'],ram['native_death_gfx.bin'],reference,images,guest,payload)
    counterexamples=faults(log,result,ram,reference,images,guest,payload,contract)
    final=dict(passed=True,process=result,originalFullPhysicalArtContractSHA256=contract_sha,actualNativeContract=state,
      actualDisplayHeaders=headers,effectiveActualNativeRecordFaults=counterexamples,
      allGuestGraphicsAndDisplayedFramesOnlyInRAM=True,rawGuestRGBPCMOrWAVFilesWritten=0,audioAccepted=False,
      allArenasAndFinishersAccepted=False,fullPortAcceptance=False)
    save(folder/'result.json',final)
    cp=subprocess.run(['compact.exe','/C','/EXE:LZX','/I','/Q',str(folder/'run.log')],capture_output=True,text=True)
    need(cp.returncode==0,'Lossless terminal current Reptile text trace compression')
    COMPLETED.append(final);print(f'{fighter} P{side} whole original native victim/head/body/ground/FIFO/retirement contract and21 actual record faults passed',flush=True)
    return final


def run():
    guest=current.expected();parent=json.loads(PARENT.read_text())
    need(parent['passed']and parent['goalStatus']=='active','Current primary-fatality/audio checkpoint accepted')
    pins=dict(parent['newInputHashes']);pins[str(PARENT)]=sha(PARENT)
    payload_path=ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata';payload=payload_path.read_bytes()
    paths=(LUA,Path(__file__).resolve(),Path(current.__file__).resolve(),Path(original.__file__).resolve(),Path(assets.__file__).resolve(),
      Path(assets.palettes.__file__).resolve(),Path(assets.codec.__file__).resolve(),ROOT/'tools/upgrade_ksui_previews.py',ROOT/'tools/build_mk2ks_mk3.py',
      ROOT/'mk2ks_reptile_victim_v887.lua',ROOT/'mk2ks_reptile_death_grounding_v904.lua')
    for p in paths:pins[str(p)]=sha(p)
    reference,expected_gfx=independent_art(guest,payload,pins)
    physical_contract()
    stock_path=ROOT/'mk2/mk2-maincpu.bin';stock=stock_path.read_bytes();pins[str(stock_path)]=sha(stock_path)
    offset=lambda address:(address-0xff800000)//8
    original_guest=bytearray(stock);struct.pack_into('<I',original_guest,offset(0xff8c8a70),0xfffd4000)
    first,last=offset(0xff8c81f0),offset(0xff8c9900)
    need(guest[first:last]==original_guest[first:last],'Entire original Reptile choreography; only typed own-victim table relocation')
    need(all(sha(p)==h for p,h in pins.items()),'All current/source/public and selected art sources stable before actual native boot')
    first_case=capture(('kano',1),guest,payload,expected_gfx,reference,pins)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
        cases=[first_case]+list(pool.map(lambda spec:capture(spec,guest,payload,expected_gfx,reference,pins),[('kano',2),('sonya',1),('sonya',2)]))
    for p in BASE.rglob('*'):
        if p.is_file():need(p.suffix.lower()not in('.bin','.png','.wav','.rgb'),'No raw native media files');pins[str(p)]=sha(p)
    need(all(sha(p)==h for p,h in pins.items()),'Every actual current/source/public/evidence pin unchanged after complete native matrix')
    return dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),goalStatus='active',remaining=parent['remaining'],
      parentAdditiveJournal=str(PARENT),previousGoalTurnClassification=parent['thisGoalTurnClassification'],
      thisGoalTurnClassification='progress: actual current true-ID Reptile victims both characters/player slots; whole original physical/parser/damage/table/palette/head/body/ground/FIFO/retirement gate, independent selected source-PNG native encoding inRAM and84 effective actual record faults',
      currentReptileBothVictimsBothSlotsNativeStateHeadBodyGroundAndRetirementAccepted=True,cases=cases,independentSourcePNGNativeReference=reference,
      actualDisplayedFrameCallbacks=sum(len(c['actualDisplayHeaders'])for c in cases),effectiveActualNativeRecordFaults=84,
      newNativeBoots=4,newBuilds=0,newDeletedFiles=0,rawGuestRGBPCMOrWAVFilesWritten=0,publicPlayableChanged=False,refreshedReleaseZIP=False,
      allFinisherContextsAccepted=False,allArenasAccepted=False,audioAccepted=False,continuousWholeSceneRasterAccepted=False,
      fullPortAcceptance=False,newInputHashes=pins,nextAction='Qualify actual current native art pixels and scanout ownership separately; continue broader victim/finisher/arena/audio/CPU/secret/cinematic contexts, preserve every original remaining group, then dependency-aware obsolete-folder cleanup and complete applicable combined acceptance before public release promotion.')


if __name__=='__main__':
    need(not OUT.exists(),'Fresh immutable current Reptile victim checkpoint')
    try:report=run()
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completedCases=COMPLETED,goalStatus='active',fullPortAcceptance=False)
    OUT.mkdir();save(OUT/'progress.json',report)
    print(json.dumps({k:v for k,v in report.items()if k not in('cases','completedCases','newInputHashes','remaining','independentSourcePNGNativeReference')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
