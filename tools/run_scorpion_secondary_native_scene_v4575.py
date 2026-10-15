"""Fresh missing whole Scorpion-secondary native renderer windows, no guest writes."""
import argparse,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
import run_current_scorpion_secondary_state_v4549 as original
import qualify_scorpion_secondary_scene_source_v4574 as source
import scorpion_secondary_native_scene_model_v4559 as model
ROOT,need,sha,NAME=original.ROOT,original.need,original.sha,original.NAME

def collector():
    text=inspect.getsource(original.capture)
    changes=[
      ('files={Path(p)for p in build',"files={Path(p)for p in preflight['inputHashes']}|{Path(p)for p in build"),
      ("audit_v4552_scorpion_secondary_{fighter}_p{side}_native_state_ram","audit_v4576_scorpion_secondary_{fighter}_p{side}_native_scene_ram"),
      ('MK2KS_REPTILE_AUDIT_DIR=str(folder))',
       'MK2KS_REPTILE_AUDIT_DIR=str(folder),MK2KS_STAGE_OUT=str(folder),MK2KS_STAGE_SIDE=str(side),MK2KS_STAGE_WINNER=fighter)'),
      ('guest_sha=None;rgb=[]',
       "guest_sha=None;rgb=[]\n    model.PALETTES.clear();model.PALETTE_ROUTES.clear();model.QUEUE_ROUTES.clear()\n    graphics_pins={};graphics=model.sources((candidate/'roms/mk2ks/mk2ks.mdata').read_bytes(),graphics_pins)\n    need(all(sha(p)==h for p,h in graphics_pins.items()),'All actual independent graphics sources unchanged')\n    identity={'kano':17,'sonya':18,'kitana':4,'liu_kang':1}[fighter]\n    ids=(identity,10)if side==1 else(10,identity)\n    scene=model.Model(guest,(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes(),graphics,ids);transport=model.Transport();scene_errors=[];visible=[]"),
      ("if line.startswith(('MK2_SSECOND_GUEST ','MK2_SSECOND_RGB ')):",
       """if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):
                    row=dict(re.findall(r'(\\w+)=([^\\s]+)',line));encoded=next(process.stdout).strip()
                    try:
                        if line.startswith('MK2_TOMB_RAM_BUFFER '):
                            raw=transport.decode(row,encoded)
                            if row['file']=='guest_maincpu.bin':need(raw==guest,'Entire actual renderer guest RAM exact')
                            elif not scene_errors:scene.raw[row['file']]=raw
                            log.write('MK2_SCORPION_RAM_BUFFER_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+model.digest(raw)+'\\n')
                        else:
                            need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Whole actual native RGB32 field')
                            words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
                            pixels=np.stack([(words>>n)&255 for n in(16,8,0)],axis=2).astype(np.uint8)
                            visible.append(dict(file=row['file'],rgbSHA256=model.digest(pixels.tobytes())))
                            if not scene_errors:scene.rgb[row['file']]=pixels
                            log.write('MK2_SCORPION_RAM_RGB_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+visible[-1]['rgbSHA256']+'\\n')
                    except Exception as error:
                        if not scene_errors:
                            scene_errors.append(dict(header=line.strip(),error=repr(error),traceback=traceback.format_exc()))
                            print(f'{fighter}P{side} transport error: {error!r}',flush=True)
                elif line.startswith(('MK2_SSECOND_GUEST ','MK2_SSECOND_RGB ')):"""),
      ("need('hex='not in line,'No raw or encoded native media persisted');log.write(line)",
       """need('hex='not in line,'No raw or encoded native media persisted')
                    if not scene_errors:
                        try:model.palette_trace(line,guest);scene.line(line)
                        except Exception as error:
                            scene_errors.append(dict(line=re.sub(r'\\bdata=[^\\s]+','data=RAM_ONLY',line.strip()),error=repr(error),traceback=traceback.format_exc()))
                            print(f'{fighter}P{side} model error: {error!r}',flush=True)
                    if re.search(r'\\bdata=',line):
                        raw=bytes.fromhex(re.search(r'\\bdata=([^\\s]+)',line).group(1));line=re.sub(r'\\bdata=[^\\s]+','data_sha256='+model.digest(raw),line)
                    log.write(line)
                    if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')and scene.records and len(scene.records)%100==0:print(f'{fighter}P{side}: {len(scene.records)} whole native fields exact',flush=True)"""),
      ('rawMediaGuestROMOrBuildFilesWritten=0,assistance=',
       'exactNativeSceneFields=len(scene.records),sceneErrors=scene_errors,nativeRasterFaults=scene.counterexamples,rawMediaGuestROMOrBuildFilesWritten=0,assistance='),
      ('positive=contract(text,fighter,side)',
       """(folder/'native_scene_records.json').write_text(json.dumps(scene.records,indent=2)+'\\n')
    (folder/'native_scene_visible_digests.json').write_text(json.dumps(visible,indent=2)+'\\n')
    (folder/'native_scene_buffer_digests.json').write_text(json.dumps(transport.records,indent=2)+'\\n')
    need(not scene_errors,'Every native scene pipeline field: '+repr(scene_errors[:1]))
    positive=contract(text,fighter,side)
    lo=positive['actualNativeActivation']+1;hi=positive['actualNativeRetirement']+30
    need([r['frame']for r in scene.records]==list(range(lo,hi+1))and len(visible)==len(scene.records),'Every native scene field through real retirement plus30')
    need(len(scene.counterexamples)==2 and scene.palette_checks>0 and model.PALETTES,'Actual whole VRAM/RGB fault rejection and source-qualified own/stock palettes')
    need(scene.groups['FLOOR_QUEUE']and scene.groups['SHADOW_COMPONENT'],'Actual body FIFO and native compressed-shadow components, not metadata-only claims')
    need(all(sha(p)==h for p,h in graphics_pins.items()),'All independent graphics source inputs unchanged after terminal')
    pins.update(graphics_pins)
    positive.update(completeSceneFields=len(scene.records),nativeRasterFaults=scene.counterexamples,sourcePaletteChecks=scene.palette_checks,
      nativeShadowComponents=len(scene.groups['SHADOW_COMPONENT']),nativeCPUWrites=scene.cpu_count,
      nativeShiftTransfers=scene.transfers,completeNativeRendererWindowAccepted=True,
      independentArtAllArenaGroundAudioAcceptance=False)"""),
    ]
    for before,after in changes:
        need(text.count(before)==1,'Only declared unchanged earned-controller/RAM-renderer extension: '+before)
        text=text.replace(before,after,1)
    namespace=dict(vars(original),__file__=__file__,source=source,model=model,np=np)
    exec(compile(text,__file__+'::whole4549_with_continuous_RAM_scene','exec'),namespace)
    return namespace['capture']

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya','kitana','liu_kang'))
    parser.add_argument('--side',required=True,type=int,choices=(1,2));args=parser.parse_args()
    out=ROOT/f'audit_v4577_scorpion_secondary_{args.fighter}_p{args.side}_native_scene_checked'
    need(not out.exists(),'Fresh actual complete native scene output')
    try:report=collector()((args.fighter,args.side))
    except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)

if __name__=='__main__':main()
