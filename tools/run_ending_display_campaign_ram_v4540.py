"""New whole natural ending video windows; native controls and build unchanged.

Original4439 full guest/campaign/RGB collector retained. Every ending frame
is continuously checked against the original source-bound native CPU/DMA/
shift renderer. Raw guest/VRAM/RGB remain RAM-only. Not an independent stock
ending/art/cinematic/audio/all-P1/full-port acceptance or a new release.
"""
import argparse,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
import numpy as np
import run_kintaro_pressure_guard_long_campaign_v4439 as original
import qualify_ending_display_source_v4541 as source
import ending_display_ram_model_v4519 as model
import run_current_tomb_ram_matrix_v3648 as renderer
ROOT,need,sha,NAME=original.ROOT,original.need,original.sha,original.NAME

def collector(fighter):
    text=inspect.getsource(original.capture)
    changes=[
      ("need(fighter=='sonya','Actual unfinished Sonya P2 context only')","need(fighter in ('kano','sonya'),'Only actual accepted current P2 policies')"),
      ('source.source_boundary()','source.source_boundary(fighter)'),
      ('audit_v4438_kintaro_pressure_guard_long_source_preflight/report.json',str(source.OUT.relative_to(ROOT))+'/report.json'),
      ("folder=ROOT/f'audit_v4440_{fighter}_kintaro_pressure_guard_long_p2_campaign'","folder=ROOT/f'audit_v4547_{fighter}_p2_ending_display_ram'"),
      ("MK2KS_CAMPAIGN_STRATEGY='guard_punish'","MK2KS_CAMPAIGN_STRATEGY='zoning'if fighter=='kano'else'guard_punish'"),
      ('headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None',
       "headers=[];images={};stream=hashlib.sha256();byte_count=0;guest_sha=None\n    payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()\n    graphics_pins={};graphics=renderer.source_graphics(payload,graphics_pins)\n    need(all(sha(p)==h for p,h in graphics_pins.items()),'All independent source graphics unchanged')\n    scene=model.Model(guest,payload,graphics,(13,17 if fighter=='kano'else 18));transport=model.Transport();scene_errors=[];scene_rgb=[]"),
      ("if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):",'''if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):
                    row=dict(re.findall(r'(\\w+)=([^\\s]+)',line));encoded=next(process.stdout).strip()
                    try:
                        if line.startswith('MK2_TOMB_RAM_BUFFER '):
                            raw=transport.decode(row,encoded)
                            if row['file']=='guest_maincpu.bin':need(raw==guest,'Every additional original observer guest byte exact in RAM')
                            elif not scene_errors:scene.raw[row['file']]=raw
                            log.write('MK2_ENDING_RAM_BUFFER_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+model.digest(raw)+'\\n')
                        else:
                            need(row['bytes']=='406400'and row['width']=='400'and row['height']=='254'and row['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Every complete actual native RGB frame')
                            words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
                            rgb=np.stack([(words>>n)&255 for n in (16,8,0)],axis=2).astype(np.uint8)
                            record=dict(file=row['file'],rgbSHA256=model.digest(rgb.tobytes()));scene_rgb.append(record)
                            if not scene_errors:scene.rgb[row['file']]=rgb
                            log.write('MK2_ENDING_RAM_RGB_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+record['rgbSHA256']+'\\n')
                    except Exception as error:
                        if not scene_errors:
                            scene_errors.append(dict(header=line.strip(),error=repr(error),traceback=traceback.format_exc()))
                            print(f'{fighter} native video transport error: {error!r}',flush=True)
                elif line.startswith('MK2_CAMPAIGN_GUEST_RAM '):'''),
      ("need('hex='not in line,'Never persist encoded raster')",'''need('hex='not in line,'Never persist encoded raster')
                    if not scene_errors:
                        try:scene.line(line)
                        except Exception as error:
                            scene_errors.append(dict(line=re.sub(r'\\bdata=[^\\s]+','data=RAM_ONLY',line.strip()),error=repr(error),traceback=traceback.format_exc()))
                            print(f'{fighter} native video model error: {error!r}',flush=True)
                    if re.search(r'\\bdata=',line):
                        raw=bytes.fromhex(re.search(r'\\bdata=([^\\s]+)',line).group(1))
                        line=re.sub(r'\\bdata=[^\\s]+','data_sha256='+model.digest(raw),line)
                    if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')and len(scene.records)%100==0 and scene.records:
                        print(f'{fighter} ending: {len(scene.records)} complete native RGB/VRAM fields exact',flush=True)'''),
      ('nativeFrameStreamSHA256=stream.hexdigest().upper(),passed=False',
       'nativeFrameStreamSHA256=stream.hexdigest().upper(),observedEndingRGBFields=len(scene_rgb),exactContinuousEndingFields=len(scene.records),endingModelErrors=scene_errors,endingNativePipelineFaults=scene.counterexamples,passed=False'),
      ('return folder,headers,images',
       "(folder/'ending_buffer_digests.json').write_text(json.dumps(transport.records,indent=2)+'\\n')\n    (folder/'ending_visible_digests.json').write_text(json.dumps(scene_rgb,indent=2)+'\\n')\n    (folder/'ending_continuous_records.json').write_text(json.dumps(scene.records,indent=2)+'\\n')\n    need(not scene_errors,'Entire ending native video replay: '+repr(scene_errors[:1]))\n    need(all(sha(p)==h for p,h in graphics_pins.items()),'Every independent graphics input unchanged after native terminal')\n    return folder,headers,images,scene,graphics_pins")]
    before='    need(all(sha(p)==h for p,h in pins.items()),\'Every executed input unchanged\')'
    need(text.count(before)==1,'One actually terminal original input-check boundary')
    text=text.replace(before,"    print(f'{fighter} native video process terminal exit={code}',flush=True)\n"+before,1)
    for before,after in changes:
        need(text.count(before)==1,'Only declared complete collector role/window/RAM sink adaptation: '+before)
        text=text.replace(before,after,1)
    scope=dict(vars(original),__file__=__file__,source=source,LUA=source.LUA[fighter],model=model,renderer=renderer)
    exec(compile(text,__file__+'::entire4439_native_video_RAM_only','exec'),scope)
    return scope['capture']

def rows(text,tag):
    return [dict(re.findall(r'(\w+)=([^\s]+)',line)) for line in text.splitlines()
      if line.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]

def run(fighter):
    folder,headers,images,scene,graphics_pins=collector(fighter)(fighter)
    text=(folder/'run.log').read_text();identity=17 if fighter=='kano'else 18
    reference=ROOT/('audit_v4485_kano_current_p2_campaign_ram' if fighter=='kano'else'audit_v4440_sonya_kintaro_pressure_guard_long_p2_campaign')
    prefixes=('MK2_NAT_CAMPAIGN_','MK2_MILEENA_CAMPAIGN_','MK2_BOSS_KNIFE_','MK2_CAMPAIGN_GUEST_RAM_DIGEST ','MK2_CAMPAIGN_RAM_FRAME_DIGEST ')
    native=lambda t:[line for line in t.splitlines() if line.startswith(prefixes)and not line.startswith(('MK2_NAT_CAMPAIGN_FLOOR_','MK2_NAT_CAMPAIGN_SHADOW_','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_'))]
    need(native(text)==native((reference/'run.log').read_text()),'Every original cold physical/selection/health/move/boss/ending/guest/RGB event exactly unchanged')
    begin=rows(text,'ENDING_DISPLAY_BEGIN');attract=rows(text,'ENDING_DISPLAY_ATTRACT');start=rows(text,'ENDING_START');end=rows(text,'ENDING_COMPLETED');ko=rows(text,'ENDING_DISPLAY_KO')
    need(len(begin)==len(attract)==len(start)==len(end)==len(ko)==1,'One actual final collision/own ending/native attract video window')
    lo,hi=int(start[0]['frame']),int(end[0]['frame'])+300
    need(begin[0]['frame']==start[0]['frame'] and attract[0]['frame']==end[0]['frame']and
      begin[0]['identity']==str(identity)and begin[0]['winner']=='2' and
      int(begin[0]['final_ko'])==int(ko[0]['frame'])<lo and ko[0]['pc']=='FF836700',
      'Same actual source-bound native final KO/own identity/actor-retired ending/attract as qualified whole campaign')
    need([r['frame']for r in scene.records]==list(range(lo,hi+1))and len(scene.records)==len(scene.rgb)+len(json.loads((folder/'ending_visible_digests.json').read_text())),
      'Every ending transition/page/held field and entire native attract plus300, without gaps')
    need(len(scene.counterexamples)==2 and all(r['exactVRAMWords']==512*512 and r['exactRGBPixels']==400*254 for r in scene.records),
      'Every complete native VRAM and visible RGB target exact, actual VRAM/RGB bit faults rejected')
    need(not scene.groups['FLOOR_QUEUE'] and not scene.groups['FLOOR_OWNER'] and scene.palette_checks==0,
      'No floor actor/shadow/own-palette assertion substituted for cinematic/native attract semantics')
    # Existing original-source-qualified early/late page hashes must occur in
    # this continuous stream, not merely in the controller's sparse output.
    references=json.loads((ROOT/('audit_v4490_kano_current_p2_native_ending_pages_checked' if fighter=='kano'else'audit_v4449_sonya_p2_native_ending_pages_checked')/'report.json').read_text())
    byframe={r['frame']:r for r in scene.records}
    need(references['passed']and all(byframe[r['frame']]['rgbSHA256']==r['currentRGBSHA256']for r in references['pages']),
      'All four original-ROM photo/font/shadow/background qualified pages present byte-exact inside complete continuous video')
    pins=dict(graphics_pins)
    for p,h in json.loads((folder/'result.json').read_text())['input_hashes'].items():pins[p]=h
    for p in folder.rglob('*'):
        if p.is_file():pins[str(p)]=sha(p)
    pins[str(reference/'run.log')]=sha(reference/'run.log')
    need(all(sha(p)==h for p,h in pins.items()),'All current actual and independent native source bytes unchanged')
    return dict(passed=True,candidate=NAME,fighter=fighter,physicalSlot=2,identity=identity,
      capture=str(folder),originalColdNativeCampaignExactlyUnchanged=True,endingStart=lo,endingAttract=hi-300,naturalTerminal=hi,
      exactConsecutiveNativeVideoFields=len(scene.records),exactRGBPixels=len(scene.records)*400*254,
      exactVRAMWords=len(scene.records)*512*512,oneInitialBaseOnly=True,comparisonTargetsNeverReanchor=True,
      exactNativeCPUPixelWrites=scene.cpu_count,exactNativePreBuffers=scene.pre_count,exactNativeFlips=scene.flip_count,
      nativeShiftLoads=scene.loads,nativeShiftFills=scene.fills,nativeShiftTransfers=scene.transfers,
      actualNativePixelFaultsRejected=scene.counterexamples,originalQualifiedEarlyLatePagesPresent=True,
      completeCurrentP2EndingAttractNativeRendererVideoAccepted=True,
      independentStockTransitionChoreographyAccepted=False,allEndingArtCinematicsAudioContextsAccepted=False,
      rawImageAudioVRAMROMOrBuildCopiesWritten=0,publicPlayableOrReleaseChanged=False,fullPortAcceptance=False,
      scope=__doc__,inputHashes=pins)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--fighter',required=True,choices=('kano','sonya'));args=parser.parse_args()
    out=ROOT/f'audit_v4548_{args.fighter}_p2_ending_display_checked';need(not out.exists(),'Fresh immutable actual new video result')
    try:report=run(args.fighter)
    except Exception as e:report=dict(passed=False,fighter=args.fighter,error=repr(e),traceback=traceback.format_exc(),fullPortAcceptance=False)
    out.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(out)],capture_output=True).returncode==0,'Compressed result before writes')
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='inputHashes'},indent=2),flush=True)
    raise SystemExit(0 if report['passed']else 1)
