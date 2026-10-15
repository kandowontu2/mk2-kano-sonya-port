"""Full original Ring FIFO/cache/projection and compressed-shadow contracts.

Bind them to the current RAM-only continuous raster, independently decoded
donor art, actual physical timeline and thirty-field recovery/erase tail.
No raw target reconstruction, extra emulator or universal acceptance claim.
"""
import argparse,copy,gzip,inspect,json,re,subprocess,traceback
from collections import defaultdict
from pathlib import Path
import capture_current_cpu_ring_render_v6377 as capture
import verify_native_cpu_ring_render_v2983 as original
import inspect_native_shadow_rows_v635 as shadows
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6380_current_cpu_ring_render_checked'


def observations(text,image):
 groups=defaultdict(list);buffers={}
 for line in text.splitlines():
  digest=re.search(r'\bdata_sha256=([^\s]+)',line)
  parsed=capture.model.parse(re.sub(r'\bdata_sha256=[^\s]+','',line))
  if not parsed:continue
  tag,row=parsed
  if digest:row['actualDataSHA256']=digest[1]
  groups[tag].append(row)
  if tag=='FLOOR_GFX':
   need(digest and 0<=row['first']<row['first']+row['bytes']<=len(image),'Whole hash-bound observed GFX range')
   raw=image[row['first']:row['first']+row['bytes']]
   need(capture.model.digest(raw)==digest[1]and row['key']not in buffers,'Every independently reconstructed GFX fragment matches actual observed bytes')
   buffers[row['key']]={**row,'data':raw.hex()}
 return groups,buffers


def native_gate(groups,records,text,guest,payload,seq,timeline):
 source=inspect.getsource(original.verify)
 first=source.index("    origin=state.one(groups['FLOOR_BEGIN']");last=source.index('    streams=shadow.inspect(CASE)',first)
 block=source[first:last]
 before="(CASE/'input_sources/mk2ks_physical_p2_cpu_continuation_v1997.lua')"
 need(block.count(before)==1,'Only original source file location differs; no source-tree copy')
 block=block.replace(before,"(ROOT/'mk2ks_physical_p2_cpu_continuation_v1997.lua')",1)
 prefix='''def gate(groups,records,log,guest,payload,seq,timeline):
    human=17
    identities=(17,18)
    timeline={**timeline,'lastScene':max(timeline['ownReady'],timeline['retirement'])+30}
    observer=(ROOT/'mk2ks_physical_p2_cpu_ring_display_v2014.lua').read_text()
'''
 suffix='''
    visible=defaultdict(set)
    by_frame={r['frame']:r for r in records}
    for frame,rows in by_draw.items():
        target=by_frame.get(frame+1)
        if target is None:continue
        for q in rows:
            if target['body'][str(q['slot'])]['pixels']>0:visible[q['slot']].add(q['pose'])
    assert set(seq['body'])<=visible[2]and set(seq['impact'])<=visible[3], 'Every original release and seven impact poses actually visible'
    executed={q['pose']for q in queues.values()if q['slot']==3 and q['pose']in seq['flight']}
    assert executed and executed<=visible[3], 'Every actually executed Ring flight phase visible'
    tail=[r for r in records if r['frame']>timeline['retirement']+1]
    assert len(tail)>=30 and all(r['body']['3']['pixels']==0 for r in tail),'Complete actual post-retirement erase tail has no ring pixels'
    return dict(nativeDraws=dict(draws),sourceBoundProjections=projection_checks,bodyCacheParts=len(groups['FLOOR_QUEUE_PART']),
                completeOriginalBodyPoses=len(seq['body']),completeOriginalImpactPoses=len(seq['impact']),
                actualVisibleFlightPoses=len(executed),postRetirementEmptyFields=len(tail),physicalPointersUnchanged=True)
'''
 scope=dict(original.verify.__globals__,CASE=CASE)
 exec(compile(prefix+block+suffix,__file__+'::whole_original_native_ring_inventory_cache_projection_dispatch','exec'),scope)
 return scope['gate'](groups,records,text,guest,payload,seq,timeline)


def shadow_gate(groups,buffers):
 scope=dict(shadows.__dict__,data=lambda folder:(groups,buffers,None,None,None))
 exec(compile(inspect.getsource(shadows.inspect),__file__+'::whole_original_compressed_shadow_rows','exec'),scope)
 result=scope['inspect'](CASE)
 need(result['rowStreamVerified']and not result['failures']and not result['oversized_rows']and
      set(map(tuple,result['identities']))=={(1,17),(2,18)},'All native owned compressed shadows, complete original stepping/copy cadence')
 return result


def main(preflight=False):
 need(not OUT.exists(),'Fresh immutable current Ring qualification')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(meta['passed']and meta['nativeExit']==terminal['exitCode']==0 and terminal['naturalTerminal']and not terminal['observationErrors'],
      'Actual same native process naturally terminal before host acceptance')
 need(not capture.previous.terminal.process_tools.census(),'No live native game, no new replay')
 pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Complete actual capture inputs unchanged')
 guest,build,scene,_,graphics_pins=capture.init_model();pins.update(graphics_pins)
 sequences,pieces=original.art.independent_art(scene.payload,scene.graphics,pins)
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 groups,buffers=observations(text,scene.graphics)
 records=json.loads((CASE/'continuous_scene_records.json').read_text())
 timeline=meta['independentSemantics']['ring']['acceptedRings'][0]
 need([r['frame']for r in records]==list(range(timeline['start']+1,max(timeline['retirement'],timeline['ownReady'])+31)),
      'Every current full screen field, original entry through complete recovery tail')
 positive=native_gate(groups,records,text,guest,scene.payload,sequences['ring'],timeline)
 shadow=shadow_gate(groups,buffers)
 if preflight:
  print(json.dumps(dict(preflightPassed=True,newNativeBoots=0,positive=positive,shadowCopies=shadow['checked_copies'])),flush=True);return
 rejected=[]
 def reject(label,bad,gate):
  need(bad!=groups,'Real actual native observation changed')
  try:gate(bad)
  except(ValueError,AssertionError,KeyError)as error:rejected.append(dict(fault=label,rejectedBy=str(error)))
  else:raise ValueError('Accepted actual Ring record fault '+label)
 check=lambda value:native_gate(value,records,text,guest,scene.payload,sequences['ring'],timeline)
 for label,tag,key,delta in [('floor shifted','FLOOR_QUEUE_TRANSFORM','floor',1),
                           ('camera shifted','FLOOR_QUEUE_TRANSFORM','camera',65536),
                           ('cache body origin shifted','FLOOR_QUEUE_PART','dy',1),
                           ('wrong actual DMA source','FLOOR_DMA','source',1),
                           ('child dispatch owner lost','FLOOR_QUEUE_DISPATCH','actor',1)]:
  bad=copy.deepcopy(groups)
  target=next(r for r in bad[tag]if r.get('slot')==3)if tag=='FLOOR_QUEUE_DISPATCH'else bad[tag][0]
  target[key]+=delta;reject(label,bad,check)
 bad=copy.deepcopy(groups);stale=dict(next(r for r in groups['FLOOR_ALL_QUEUE']if r['actor']==groups['FLOOR_CHILD_SPAWN'][0]['actor']))
 stale.update(frame=timeline['retirement']+5,cursor=0x01000000);bad['FLOOR_ALL_QUEUE'].append(stale)
 reject('ring republished after retirement',bad,check)
 bad=copy.deepcopy(groups);component=bad['SHADOW_COMPONENT'][0]
 row=next(r for r in bad['FLOOR_DMA']if r['event']==component['event']);row['y']+=1
 reject('native floor-shadow copy shifted',bad,lambda value:shadow_gate(value,buffers))
 need(check(groups)==positive and shadow_gate(groups,buffers)==shadow,'Complete native positive restored after every actual fault')
 for path in(CASE/'result.json',CASE/'native_terminal.json',CASE/'run.log.gz',CASE/'continuous_scene_records.json',
             CASE/'buffer_digests.json',Path(__file__),Path(original.__file__),Path(shadows.__file__),ROOT/'audit_v6359_current_cpu_effect_render_checked/report.json'):
  pins[str(path.resolve())]=sha(path)
 result=dict(passed=True,currentCPUFullRingHitRenderShadowAndEraseAccepted=True,candidate=capture.previous.terminal.current.NAME,
             nativeTerminal=terminal,phase=timeline,completeContinuousRender=meta['continuousRender'],
             originalDonorPiecesIndependentlyCompared=pieces,nativeFIFOProjectionArt=positive,
             ownedNativeCompressedShadow=shadow,actualFaultsRejected=rejected,wholeNativePhysicalPhaseAndHealth=meta['independentSemantics'],
             wholeEarlierPhysicalTrajectoryIdentical=meta['wholeEarlierPhysicalTrajectoryIdentical'],inputHashes=pins,
             goalStatus='active',fullPortAcceptance=False,newNativeBoots=0,newBuilds=0,newRawMedia=0,fullAudioAcceptance=False)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact current proof losslessly compressed')
 print(json.dumps(dict(passed=True,fields=meta['continuousRender']['fields'],exactRGBPixels=meta['continuousRender']['exactRGBPixels'],shadowCopies=shadow['checked_copies'],actualFaultsRejected=len(rejected))),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
