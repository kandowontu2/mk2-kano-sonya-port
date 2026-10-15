"""Current corrected executable P1 full ending/300-attract pixel observation.

Same accepted cold physical campaigns, single native VRAM base and complete
CPU/DMA/shift/IO/source-cycle renderer. Text gzip only; raw buffers RAM-only.
A matching renderer does not prove all original-art/audio/cinematic contexts.
"""
import argparse,gzip,hashlib,inspect,json,re,traceback
from pathlib import Path
import numpy as np
import current_payload_metadata_context_v5229 as current
import run_corrected_p1_campaigns_v5230 as policies
import qualify_p1_ending_deferred_source_v5265 as source
import p1_ending_cpu_cycle_model_v5240 as model
import run_current_tomb_ram_matrix_v3648 as renderer
import qualify_ending_display_latch_source_v4647 as window
ROOT,need,sha=current.ROOT,current.need,current.sha

def collector(fighter):
 ref=policies.kano if fighter=='kano'else policies.sonya
 out=ROOT/f'audit_v5264_{fighter}_current_p1_ending_pixels'
 code=inspect.getsource(ref.capture)
 changes=[
 ("pins=dict(build['input_hashes'])", """pins=dict(build['input_hashes'])
 payload=(candidate/'roms/mk2ks/mk2ks.mdata').read_bytes()
 graphics_pins={};graphics=bytearray(renderer.source_graphics(payload,graphics_pins))
 owned=current.expected_gfx()
 need(len(owned)==18976,'Exact independent current frozen bodies and legs bytes')
 graphics[0x1fa0000:0x1fa0000+11944]=owned[:11944]
 graphics[0x1fa4000:0x1fa4000+7032]=owned[11944:]
 graphics=bytes(graphics);pins.update(graphics_pins)
 preflight=json.loads((source.OUT/'report.json').read_text())
 need(preflight['passed']and all(sha(p)==h for p,h in preflight['inputHashes'].items()),'Before-boot entire physical P1 observer/model qualification')
 pins[str(source.OUT/'report.json')]=sha(source.OUT/'report.json')
 scene=model.Model(guest,payload,graphics,(17 if fighter=='kano'else 18,13))
 ram_transport=model.Transport();scene_errors=[];scene_rgb=[]"""),
 ("if line.startswith('MK2_CAMPAIGN_GUEST_RAM '):", """if line.startswith(('MK2_TOMB_RAM_BUFFER ','MK2_TOMB_RAM_PIXELS ')):
     fields=dict(re.findall(r'(\\w+)=([^\\s]+)',line));encoded=next(process.stdout).strip()
     try:
      if line.startswith('MK2_TOMB_RAM_BUFFER '):
       raw=ram_transport.decode(fields,encoded)
       if fields['file']=='guest_maincpu.bin':need(raw==guest,'Every additional readonly observer guest byte exact in RAM')
       elif not scene_errors:scene.raw[fields['file']]=raw
       log.write('MK2_ENDING_RAM_BUFFER_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+model.digest(raw)+'\\n')
      else:
       need(fields['bytes']=='406400'and fields['width']=='400'and fields['height']=='254'and fields['encoding']=='u32le_numeric_hex'and len(encoded)==812800,'Every full actual native RGB field')
       words=np.frombuffer(bytes.fromhex(encoded),dtype='>u4').reshape(254,400)
       rgb=np.stack([(words>>n)&255 for n in (16,8,0)],axis=2).astype(np.uint8)
       record=dict(file=fields['file'],rgbSHA256=model.digest(rgb.tobytes()));scene_rgb.append(record)
       if not scene_errors:scene.rgb[fields['file']]=rgb
       log.write('MK2_ENDING_RAM_RGB_DIGEST '+line.split(' ',1)[1].strip()+' sha256='+record['rgbSHA256']+'\\n')
     except Exception as error:
      if not scene_errors:
       scene_errors.append(dict(header=line.strip(),error=repr(error),traceback=traceback.format_exc()))
       print(f'{fighter} ending RAM transport error: {error!r}',flush=True)
    elif line.startswith('MK2_CAMPAIGN_GUEST_RAM '):"""),
 ("need('hex='not in line,'Never persist encoded guest/raster/audio')", """need('hex='not in line,'Never persist encoded guest/raster/audio')
     if not scene_errors:
      try:scene.line(line)
      except Exception as error:
       scene_errors.append(dict(line=re.sub(r'\\bdata=[^\\s]+','data=RAM_ONLY',line.strip()),error=repr(error),traceback=traceback.format_exc()))
       print(f'{fighter} ending native model error: {error!r}',flush=True)
     if re.search(r'\\bdata=',line):
      raw=bytes.fromhex(re.search(r'\\bdata=([^\\s]+)',line).group(1))
      line=re.sub(r'\\bdata=[^\\s]+','data_sha256='+model.digest(raw),line)
     if line.startswith('MK2_NAT_CAMPAIGN_FLOOR_SNAP ')and scene.records and len(scene.records)%100==0:
      print(f'{fighter}: {len(scene.records)} complete ending VRAM/RGB fields exact',flush=True)"""),
 ("elapsedSeconds=time.time()-started,rawMediaGuestAudioFilesWritten=0,newBuilds=0", """observedEndingRGBFields=len(scene_rgb),exactContinuousEndingFields=len(scene.records),
  endingModelErrors=scene_errors,endingNativePixelFaults=scene.counterexamples,
  elapsedSeconds=time.time()-started,rawMediaGuestAudioFilesWritten=0,newBuilds=0"""),
 ("return result", """(OUT/'ending_buffer_digests.json').write_text(json.dumps(ram_transport.records,indent=2)+'\\n')
 (OUT/'ending_visible_digests.json').write_text(json.dumps(scene_rgb,indent=2)+'\\n')
 (OUT/'ending_continuous_records.json').write_text(json.dumps(scene.records,indent=2)+'\\n')
 return result,scene,graphics_pins""")]
 for before,after in changes:
  need(code.count(before)==1,'Exactly one complete original capture RAM/model addition '+before)
  code=code.replace(before,after,1)
 scope=dict(vars(ref),__file__=__file__,native=current,OUT=out,LUA=source.LUA,
  CONTROLLERS=ref.CONTROLLERS+source.EXTRA,qualify_payload_metadata_warning=policies.metadata_clean,
  np=np,source=source,renderer=renderer,model=model,current=current,fighter=fighter)
 exec(compile(code,__file__+'::whole_original_current_P1_capture_readonly_ending_RAM','exec'),scope)
 return scope['capture']

def run(fighter):
 actual,scene,graphics_pins=collector(fighter)()
 folder=ROOT/f'audit_v5264_{fighter}_current_p1_ending_pixels'
 with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
 with gzip.open(ROOT/f'audit_v5231_{fighter}_corrected_p1_campaign/run.log.gz','rt')as reader:previous=reader.read()
 def native(t):
  return [s for s in t.splitlines()if not s.startswith(('MK2_NAT_CAMPAIGN_FLOOR_',
   'MK2_NAT_CAMPAIGN_SHADOW_','MK2_NAT_CAMPAIGN_ENDING_DISPLAY_','MK2_ENDING_RAM_','Average speed: '))]
 need(native(text)==native(previous),'Entire actual cold physical/guest/selection/ladder/combat/boss/ending/RGB native chronology unchanged')
 need(actual['passed']and actual['nativeExit']==0 and not actual['endingModelErrors'],
  'Actual complete native terminal and full source-timed pixel model with no ignored errors')
 lo,hi=window.renderer_window(text,fighter)
 rows=lambda tag:[dict(re.findall(r'(\w+)=([^\s]+)',s))for s in text.splitlines()
  if s.startswith('MK2_NAT_CAMPAIGN_'+tag+' ')]
 begin,ko,attract=map(rows,('ENDING_DISPLAY_BEGIN','ENDING_DISPLAY_KO','ENDING_DISPLAY_ATTRACT'))
 need(len(begin)==len(ko)==len(attract)==1 and begin[0]['frame']==str(lo)and
  begin[0]['identity']==str(17 if fighter=='kano'else 18)and begin[0]['winner']=='1'and
  int(begin[0]['final_ko'])==int(ko[0]['frame'])<lo and ko[0]['pc']=='FF836700'and
  int(attract[0]['frame'])==hi-299,'Actual own P1 native final boss winner/collision/ending/attract provenance')
 need([r['frame']for r in scene.records]==list(range(lo,hi+1))and
  len(scene.records)==actual['observedEndingRGBFields']and len(scene.counterexamples)==2 and
  all(r['exactVRAMWords']==512*512 and r['exactRGBPixels']==400*254 and r['actualRasterClocks']>=2
   for r in scene.records),'Every complete ending and300attract field exact, no gaps; actual VRAM/RGB bit faults rejected')
 need(len(scene.groups['FLOOR_BASE'])==1 and not scene.groups['FLOOR_QUEUE']and
  not scene.groups['FLOOR_OWNER']and scene.palette_checks==0 and not scene.events and not scene.rgb,
  'One base only, all actual targets consumed; no floor classification substituted for cinematic semantics')
 pins=dict(actual['inputHashes']);pins.update(graphics_pins)
 for p in folder.rglob('*'):
  if p.is_file():pins[str(p.resolve())]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'All actual source/game/render inputs unchanged after terminal')
 return dict(passed=True,fighter=fighter,physicalSlot=1,candidate=current.NAME,executableSHA256=current.EXE_SHA,
  capture=str(folder),actualColdNativeCampaignExactlyUnchanged=True,endingStart=lo,
  endingAttract=hi-299,lastCompletedRendererField=hi,actualAttractRendererFields=300,
  exactConsecutiveNativeVideoFields=len(scene.records),exactRGBPixels=len(scene.records)*101600,
  exactVRAMWords=len(scene.records)*262144,actualNativePixelFaultsRejected=scene.counterexamples,
  actualSourceTimedRasterClocks=sum(r['actualRasterClocks']for r in scene.records),
  actualDisplayIOStores=scene.records[-1]['actualDisplayIOStoresAtSnapshot'],
  oneInitialBaseOnly=True,comparisonTargetsNeverReanchor=True,
  actualCurrentP1EndingAttractNativeRendererVideoAccepted=True,
  independentStockTransitionChoreographyAccepted=False,completeArtAudioCinematicContextAcceptance=False,
  inputHashes=pins,rawMediaGuestAudioFilesWritten=0,newBuilds=0,publicPlayableChanged=False,fullPortAcceptance=False)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True);args=parser.parse_args()
 out=ROOT/f'audit_v5264_{args.fighter}_current_p1_ending_pixels_checked'
 need(not out.exists(),'Fresh immutable whole P1 ending result')
 try:report=run(args.fighter)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k!='inputHashes'},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
