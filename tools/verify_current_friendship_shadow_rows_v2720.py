"""Complete original native shadow row sequence in current Friendship captures.
All observed intermediate row sources/cadence/callers and pose-cache components
are checked, including original signed row scans. Not rendered-scene, complete
child lifecycle, all-victim/arena/finisher or full-port acceptance.
"""
import argparse,copy,json,traceback
from collections import defaultdict
from pathlib import Path
import inspect_current_friendship_full_render_v2705 as diagnostic
from verify_cpu_pair_display_v635_v3 import group
native=diagnostic.native
ROOT=native.ROOT
need=native.need
def rows_checked(groups,image,payload,guest,control,side):
 dmas={row['event']:row for row in groups['FLOOR_DMA']}
 need(len(dmas)==len(groups['FLOOR_DMA']),'Unique actual native DMA event ledger')
 shadow={event for event,row in dmas.items() if row['pc'] in (0xff8015a0,0xff801610)}
 components=groups['SHADOW_COMPONENT']
 need(shadow=={row['event'] for row in components} and len(shadow)==len(components),'Every actual native shadow copy has exactly one physical cache owner')
 families=defaultdict(list)
 for row in components:
  fid=control['actualTrueID'] if row['slot']==side else control['actualVictimID']
  need(row['slot'] in (1,2) and row['id']==fid and row['owner']==row['actor'] and row['row']==row['cache']+112*row['component'],'Actual true owned pose-cache shadow component')
  expected=group(row,payload,guest)[row['component']]
  need((row['first_source'],row['width'],row['height'],row['command'],row['xoff'],row['yoff'])==(expected['source'],expected['width'],expected['height'],expected['command'],expected['dx'],expected['dy']),'All actual shadow cache words match independent original pose descriptors')
  families[row['frame'],row['row']].append(row)
 checked=0;oversized=0
 for key,copies in families.items():
  first=copies[0]
  need(all(all(row[field]==first[field] for field in ('slot','id','actor','main','owner','pose','cache','first_source','width','height','command','xoff','yoff')) for row in copies),'One stable native shadow component during row scan')
  source,command,w,h=(first[k] for k in ('first_source','command','width','height'))
  bit=source-0x0a000000 if 0x10000000<=source<0x1a000000 else source-0xf8000000 if source>=0xf8000000 else source
  origin=bit;starts=[]
  need(((command>>12)&7 or 8)==6 and h>=4 and w>0,'Original six-bit physical shadow scanner context')
  for y in range(h):
   starts.append(source+bit-origin)
   need(0<=bit and bit+8<=len(image)*8,'Original scanner byte header inside full source graphics region')
   header=(int.from_bytes(image[bit//8:bit//8+2],'little')>>(bit%8))&255
   pre=(header&15)<<((command>>8)&3);post=(header>>4)<<((command>>10)&3)
   oversized+=pre+post>w
   bit+=8+6*(w-pre-post)
   need(0<=bit<=len(image)*8,'Original signed source-row advance remains in complete source ROM region')
  indices=list(range(0,4*(h//4),4));indices.append(indices[-1])
  actual=[dmas[row['event']] for row in copies]
  observed=[tuple(row[field] for field in ('source','command','width','height','x','y','palette','color','pc')) for row in actual]
  expected=[(starts[y],command|0x8008,w,1,actual[0]['x'],(actual[0]['y']+i)&511,0,15,0xff801610 if i==len(indices)-1 else 0xff8015a0) for i,y in enumerate(indices)]
  need(observed==expected,'Every actual intermediate source, native copy count, command, relative XY, palette, pen and caller matches original signed scanner')
  checked+=len(actual)
 need(checked>0 and any(row['frame']>=control['action'] for row in components),'Actual native Friendship startup shadow observations, not empty coverage')
 need(not any(row['frame']>=control['action']+10 for row in components),'No extra native shadow commands after original stock startup schedule')
 return dict(components=len(families),checkedCopies=checked,actualOriginalOversizedRows=oversized,firstFrame=min(row['frame'] for row in components),lastFrame=max(row['frame'] for row in components))
def verify(folder):
 meta=json.loads((folder/'result.json').read_text(encoding='utf-8-sig'));fighter,side=meta['winner'],meta['side']
 proof_path=ROOT/f'audit_v2719_current_{fighter}_friendship_lifecycle_render_p{side}_diagnostic/report.json'
 proof=json.loads(proof_path.read_text());need(proof['passed'] and proof['diagnosticCompleted'] and proof['physicalInputAndNativeChronologyUnchanged'] and proof['wholeActualGuestAndPayloadReconstructed'] and proof['allActualGraphicsBuffersROMBound'] and proof['actualConsecutiveScanouts']==1600,'Actual independently bound terminal current render diagnostic')
 pins=native.scene.launch.source_pins()
 for file,wanted in proof['inputHashes'].items():
  need(native.scene.launch.sha(file)==wanted,'Immutable actual render diagnostic dependency '+file)
  need(file not in pins or pins[file]==wanted,'Consistent source/render dependency '+file);pins[file]=wanted
 pins[str(proof_path)]=native.scene.launch.sha(proof_path)
 guest,_,payload=native.scene.current.expected();image=native.graphics.graphics(pins)
 groups,*_=diagnostic.raster.data(folder);control=proof['control'];result=rows_checked(groups,image,payload,guest,control,side)
 first=groups['SHADOW_COMPONENT'][0];event=first['event'];dma_index=next(i for i,row in enumerate(groups['FLOOR_DMA']) if row['event']==event)
 mutations=[('missing_actual_intermediate_copy','drop',None,'Every actual native shadow copy'),('wrong_intermediate_source','source',0,'Every actual intermediate source'),('wrong_intermediate_caller','pc',0xff801590,'Every actual native shadow copy'),('wrong_shadow_pen','color',14,'Every actual intermediate source'),('wrong_shadow_xy','y',(groups['FLOOR_DMA'][dma_index]['y']+1)&511,'Every actual intermediate source'),('wrong_original_cached_source','first_source',0,'All actual shadow cache words')]
 outcomes=[]
 for name,field,value,expected in mutations:
  changed=defaultdict(list,{tag:list(records) for tag,records in groups.items()})
  changed['SHADOW_COMPONENT'][0]=dict(changed['SHADOW_COMPONENT'][0])
  changed['FLOOR_DMA'][dma_index]=dict(changed['FLOOR_DMA'][dma_index])
  if field=='drop':changed['SHADOW_COMPONENT'].pop(0)
  elif field=='first_source':changed['SHADOW_COMPONENT'][0][field]=value
  else:changed['FLOOR_DMA'][dma_index][field]=value
  need(changed!=groups,'Non-vacuous actual row/caller/pen/XY/source counterexample')
  try:rows_checked(changed,image,payload,guest,control,side)
  except ValueError as error:
   need(expected in str(error),'Intended native shadow invariant for '+name+': '+str(error));outcomes.append(dict(name=name,rejectedBy=str(error)))
  else:raise ValueError('Malformed actual intermediate native shadow accepted '+name)
 need(rows_checked(groups,image,payload,guest,control,side)==result,'Final unmodified complete native row-sequence control')
 pins[str(Path(__file__).resolve())]=native.scene.launch.sha(__file__);native.scene.launch.module_pins(pins)
 return dict(passed=True,fighter=fighter,side=side,**result,originalSourcePoseCacheAndAllIntermediateRowsAccepted=True,rejectedSpecificCounterexamples=len(outcomes),outcomes=outcomes,finalUnmodifiedControlPassed=True,gameChanged=False,renderedSceneAccepted=False,absoluteShadowGeometryAccepted=False,childObjectCleanupAccepted=False,fullFinisherAcceptance=False,fullPortAcceptance=False,inputHashes=pins,scope=__doc__)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('folder',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();need(not a.output.exists(),'Immutable complete native row proof')
 try:r=verify(a.folder)
 except Exception as error:r=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 a.output.mkdir();(a.output/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('inputHashes','outcomes')},indent=2),flush=True);raise SystemExit(0 if r['passed'] else 1)
