"""Focused actual stock-victim corner control; six native frames in RAM only.

These runs are genuinely Kitana4, never relabelled as Kano/Sonya. They inspect
the remaining corner-position/art question, not full stock finisher fidelity.
No whole-scene, original-stock waveform or full-port acceptance is implied.
"""
import hashlib,json,os,re,shutil,subprocess,traceback
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
import run_jax_clap_native_audio_routes_v4059 as current
ROOT,need,sha=current.ROOT,current.need,current.sha
NAME=current.NAME
OUT=ROOT/'audit_v4092_jax_arms_stock_corner_observed'
REVIEW=ROOT/'art_review_jax_arms_stock_corner_v4093'
COMPLETED=[]

def run(side,guest):
    folder=ROOT/f'audit_v4092_jax_arms_stock_kitana_p{side}_corner_ram'
    need(not folder.exists(),'Fresh actual stock control leaf')
    candidate=ROOT/NAME;build=json.loads((candidate/'build-info.json').read_text(encoding='utf-8-sig'))
    lua=ROOT/'mk2ks_jax_arms_stock_corner_ram_v4090.lua';controller=ROOT/'mk2ks_stock_extended_earned_ram_v3958.lua'
    files={Path(p)for p in build['input_hashes']}|{candidate/'mkport_candidate.exe',candidate/'roms/mk2ks/mk2ks.mdata',candidate/'build-info.json',
        lua,controller,ROOT/'mk2ks_stock_fatality_v1021.lua',Path(__file__).resolve(),Path(current.__file__)}
    for leaf in('roms/mk2ks','samples/mk2ks','artwork'):files.update((ROOT/leaf).glob('*'))
    files={p.resolve()for p in files if p.is_file()};pins={str(p):sha(p)for p in files}
    need(sha(candidate/'mkport_candidate.exe')==build['executable_sha256']=='36B306F6A9241C1C977A7B0B1CFAC65884F4ED97963A60A1967138E000E7E982'and
         sha(candidate/'roms/mk2ks/mk2ks.mdata')==build['payload_sha256']=='91F580279F1FC262E6CFE3CBC578FDCF7DC4AC3393B1055156D5FBEBC8998B24'and
         all(pins[str(Path(p).resolve())]==h for p,h in build['input_hashes'].items()),'Exact actual current3836 executable/payload/all compiled inputs')
    folder.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(folder)],capture_output=True).returncode==0,'Capture compressed before writes')
    for p in files:
        if p.suffix in('.py','.lua','.ps1'):
            target=folder/'input_sources'/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);need(sha(target)==pins[str(p)],'Exact original stock control hierarchy snapshot')
    (folder/'input_hashes_before.json').write_text(json.dumps(pins,indent=2)+'\n')
    env={k:v for k,v in os.environ.items()if not re.match(r'^(MK2KS_|MK2_TRACE_|MK2_RANGE_|MK2_P2_)',k)}
    env.update(MK2KS_TEST_FIGHTER='kitana',MK2KS_TEST_BOOT_FRAME='600',MK2KS_TEST_CONFIRM='hp',MK2KS_TEST_CONFIRM_HOLD='8',
        MK2KS_TWO_PLAYER='1',MK2KS_CAMPAIGN_OUT=str(folder),MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0',
        MK2KS_STOCK_KILLER='jax',MK2KS_STOCK_COMMAND='bbbb_lp',MK2KS_STOCK_GAP='96',MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER='kitana',MK2KS_STAGE_OUT=str(folder))
    command=[str(candidate/'mkport_candidate.exe'),'mk2ks','-rompath',str(candidate/'roms')+';'+str(ROOT/'roms'),'-samplepath',str(ROOT/'samples'),'-samples',
        '-artpath',str(ROOT/'artwork'),'-skip_gameinfo','-nocheat','-inipath',str(folder),'-video','none','-sound','none','-samplerate','48000',
        '-noautoframeskip','-frameskip','0','-nothrottle','-str','150','-snapsize','400x254','-cfg_directory',str(folder/'cfg'),
        '-nvram_directory',str(folder/'nvram'),'-snapshot_directory',str(folder/'snap'),'-autoboot_script',str(lua)]
    guest_sha=None;frames=[]
    with(folder/'stderr.log').open('w')as errors,subprocess.Popen(command,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=errors,text=True,encoding='utf-8')as process:
        (folder/'process.json').write_text(json.dumps(dict(pid=process.pid,command=command),indent=2)+'\n');print(f'Actual stock KitanaP{side} corner control pid={process.pid}',flush=True)
        with(folder/'run.log').open('w')as log:
            for line in process.stdout:
                if line.startswith('MK2_ARM_STOCK_GUEST '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'));need(guest_sha is None and len(raw)==1048576 and raw==guest,'Every actual initialized stock-control guest byte compared in RAM')
                    guest_sha=hashlib.sha256(raw).hexdigest().upper();log.write('MK2_ARM_STOCK_GUEST_DIGEST sha256='+guest_sha+'\n')
                elif line.startswith('MK2_ARM_STOCK_RGB '):
                    h=dict(re.findall(r'(\w+)=([^\s]+)',line));raw=bytes.fromhex(h.pop('hex'));need(len(raw)==int(h['bytes'])==406400,'Whole actual native stock RGB')
                    a=np.frombuffer(raw,dtype='<u4').reshape(254,400);rgb=np.stack([(a>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
                    h['rgbSHA256']=hashlib.sha256(rgb.tobytes()).hexdigest().upper();frames.append((h,rgb));log.write('MK2_ARM_STOCK_RGB_DIGEST '+' '.join(f'{k}={v}'for k,v in h.items())+'\n')
                else:
                    need('hex='not in line,'No whole native RGB/guest encoded data on disk');log.write(line)
                    if re.match(r'^MK2_STOCK_HEAD_V921_(ACTION|WRAP|RESULT) ',line):print(line.strip(),flush=True)
        code=process.wait()
    text=(folder/'run.log').read_text();errors=(folder/'stderr.log').read_text()
    need(all(sha(p)==h for p,h in pins.items()),'All actual stock execution inputs unchanged')
    meta=dict(exit_code=code,candidate=NAME,fighter='kitana',actualIdentity=4,side=side,stockReferenceOnly=True,guestSHA256=guest_sha,
        actualNativeRGBFrames=len(frames),rawNativeRGBGuestAudioFilesWritten=0,inputHashes=pins,guestWrites=0,assistance='none',fullPortAcceptance=False)
    (folder/'result.json').write_text(json.dumps(meta,indent=2)+'\n')
    need(code==0 and len(frames)==6 and guest_sha and not re.search(r'LUA ERROR|stack traceback|fatal error|WRONG CHECKSUMS',text+errors,re.I),'Actual terminal stock control with six native frames')
    actions=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_ACTION ')]
    live=[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_FIRST_LIVE ')]
    need(len(actions)==len(live)==1 and live[0]['ids']=='11,4'and actions[0]['variant']=='2'and actions[0]['address']=='FF8BE240'and actions[0]['damage']=='322','Actual original Jax arm-rip and genuine stock Kitana4, never a relabelled own victim')
    atlas=Image.new('RGB',(800,834));draw=ImageDraw.Draw(atlas)
    for index,(h,rgb)in enumerate(frames):
        x,y=(index%2)*400,(index//2)*278;atlas.paste(Image.fromarray(rgb),(x,y+24));draw.text((x+4,y+5),f"Actual stock Kitana4 P{side} age{h['age']} frame{h['frame']}",fill='white')
    image=REVIEW/f'actual-stock-kitana-p{side}-native-corner-review.png';atlas.save(image);pins[str(image)]=sha(image)
    for p in folder.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
    summary=dict(passed=True,fighter='kitana',actualIdentity=4,side=side,stockReferenceOnly=True,capture=str(folder),essentialNativeReview=str(image),
        frames=[h for h,a in frames],actualNativeRGBPixels=609600,inputHashes=pins,allStockFinisherFidelityAccepted=False,fullPortAcceptance=False)
    COMPLETED.append(summary);return summary

if __name__=='__main__':
    need(not OUT.exists()and not REVIEW.exists(),'Fresh actual stock observation/review leaves');REVIEW.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(REVIEW)],capture_output=True).returncode==0,'Review compressed before writes')
    try:
        guest=current.expected();cases=[run(side,guest)for side in(1,2)]
        report=dict(passed=True,cases=cases,actualStockContexts=2,actualAddedCharacterContexts=0,fullPortAcceptance=False,scope=__doc__)
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),completed=COMPLETED,fullPortAcceptance=False)
    OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Stock report compressed before writes')
    (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in('cases','completed')},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
