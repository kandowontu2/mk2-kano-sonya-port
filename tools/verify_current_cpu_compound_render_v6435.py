"""Current CPU leg/Square/ordinary complete body, native shadow and raster.

Keep original whole FIFO/cache/projection and compressed-row stepping gates.
Only nonprojectile compound context differs. No universal arena/audio claim.
"""
import argparse,copy,datetime,gzip,inspect,json,re,struct,subprocess,sys,traceback
from collections import defaultdict
from pathlib import Path
import numpy as np
import capture_current_cpu_compound_render_v6438 as capture
import verify_current_cpu_ring_render_v6379 as ring
import verify_special_shadow_v5141 as body
import inspect_native_shadow_rows_v635 as rows
from verify_move_phase_shadow_v5089 import short,subxy,native_group

ROOT,need,sha=capture.ROOT,capture.need,capture.sha
CASE=capture.FOLDER
OUT=ROOT/'audit_v6436_current_cpu_compound_render_checked'


def strings(text):
 result=defaultdict(list)
 for line in text.splitlines():
  for before,after in [('MK2_NAT_CAMPAIGN_FLOOR_CANDIDATE ','MK2_HPHASE_CANDIDATE'),
                       ('MK2_NAT_CAMPAIGN_FLOOR_QUEUE ','MK2_HPHASE_QUEUE'),
                       ('MK2_HPHASE_SHADOW_BEGIN ','MK2_HPHASE_SHADOW_BEGIN'),
                       ('MK2_HPHASE_PROJECTION ','MK2_HPHASE_PROJECTION'),
                       ('MK2_HPHASE_SHADOW_DMA ','MK2_HPHASE_SHADOW_DMA')]:
   if line.startswith(before):
    fields=re.findall(r'(\w+)=([^\s]+)',line)
    need(len(fields)==len(dict(fields)),'Unique actual shadow/body protocol keys')
    value=dict(fields)
    #2014 prints publication words with8 digits and candidates with4.
    #5141 compares shared fields textually; preserve each actual numeric value.
    if after in('MK2_HPHASE_CANDIDATE','MK2_HPHASE_QUEUE'):
     value={k:(f'{int(v,16):08X}'if k in body.HEX else v)for k,v in value.items()}
    result[after].append(value);break
 return result


def donor_art(groups,payload,image,pins):
 art=ring.original.art;path=ROOT/'mk3/mk3-maincpu.bin';donor=path.read_bytes();pins[str(path)]=sha(path)
 need(pins[str(path)]=='1BC7A53A023F15B20F01398F87E38478A27C670DF27EA320E36125D0957EE651','Exact original MK3 donor program')
 poses=sorted({q['pose']for q in groups['FLOOR_QUEUE']});checked=set();references=0
 def pixels(source,command,w,h,raw):
  first=source//8;count=(source%8+w*h*((command>>12)&7 or 8)+(h*8 if command&128 else 0)+7)//8+8
  need(0<=first<first+count<=len(raw),'Complete independently decoded original sprite range')
  key=f'{source:08X}_{command:04X}_{w}_{h}'
  return art.decoder({key:dict(offset=source,first=first,bytes=count,data=raw[first:first+count].hex())})(source,command,w,h)
 for pose in poses:
  for address,actual in art.source_groups(payload,pose,0xfe800000):
   original=art.read(donor,address+0x1000000,'<4hIHI',0xff800000)
   w,h,x,y,source,command,palette=actual;ew,eh,ex,ey,es,ec,ep=original
   need((w,h,x,y,source,command)==(ew,eh,ex,ey,es+0x10000000,ec),
        'Every complete actual body piece has original donor dimensions, pivot, source and command')
   need(np.array_equal(pixels(source-0x0a000000,command|0x8002,w,h,image),
                       pixels(es,ec|0x8002,ew,eh,image[0xc00000:0x1e00000])),
        'Every independently decoded native body index equals original donor sprite')
   references+=1;checked.add(address)
 return dict(completeObservedBodyPoses=len(poses),originalDonorPieceReferences=references,uniqueOriginalDonorPieces=len(checked),
             allObservedDimensionsPivotsSpriteIndicesExact=True)


def native_gate(groups,records,text,guest,payload,timeline):
 source=inspect.getsource(ring.original.verify)
 first=source.index('    queues={(q[');last=source.index('    streams=shadow.inspect(CASE)',first)
 block=source[first:last]
 first=block.index("    poses=set(seq['intro']");last=block.index('    dmas=',first)
 block=block[:first]+'''    for key,q in inventory.items():
        if q['actor']in actors.values():
            assert key in queues and queues[key]['slot']in(1,2),'Every physical publication independently inventoried'
    assert set(q['slot']for q in queues.values())=={1,2},'Only the two actual native physical bodies'
'''+block[last:]
 before='    assert draws[1]>50 and draws[2]>50 and draws[3]>30'
 need(block.count(before)==1,'Only nonprojectile coverage context differs')
 block=block.replace(before,'    assert draws[1]>50 and draws[2]>50',1)
 prefix='''def gate(groups,records,log,guest,payload,timeline):
    human=17
    first=groups['FLOOR_STATE'][0]
    actors={s:first[f'p{s}']for s in(1,2)}
    mains={s:first[f'main{s}']for s in(1,2)}
    for r in groups['FLOOR_STATE']:
        assert r['mode']==2 and all(r[f'p{s}']==actors[s]and r[f'main{s}']==mains[s]and
            r[f'roster{s}']==(17 if s==1 else 18)and r[f'state{s}']==(1 if s==1 else 0)for s in(1,2))
    assert not groups['FLOOR_POINTER_STORE'],'No physical replacement across compound handoffs'
'''
 suffix='''
    return dict(nativeDraws=dict(draws),sourceBoundProjections=projection_checks,
                bodyCacheParts=len(groups['FLOOR_QUEUE_PART']),physicalPointersUnchanged=True)
'''
 scope=dict(ring.original.verify.__globals__,CASE=CASE)
 exec(compile(prefix+block+suffix,__file__+'::whole_original_body_FIFO_cache_projection','exec'),scope)
 registers={r['event']:r for r in groups['FLOOR_DMA_REGS']};dmas={r['event']:r for r in groups['FLOOR_DMA']}
 need(len(registers)==len(groups['FLOOR_DMA_REGS'])and len(dmas)==len(groups['FLOOR_DMA'])and set(registers)==set(dmas),
      'Every DMA has exactly one independent native register observation')
 for event,d in dmas.items():
  need(all(registers[event][k]==d[k]for k in('frame','source','command')),'All owned/unowned DMA sources and commands bind native registers')
 result=scope['gate'](groups,records,text,guest,payload,timeline)
 physical=capture.compound.square.P.rows(text,'FIELD');by={r['frame']:r for r in physical}
 for r in groups['FLOOR_QUEUE']:
  native=by[r['frame']+1];prefix='v'if r['slot']==1 else''
  need(all(r[k]==native[prefix+k]for k in('actor','main','owner','id','floor')),'Queued native identities and ground bind next complete physical callback')
 #Same original pre-clip gate checks EVERY complete body, including clipped parts.
 raw=strings(text);frames=set(range(timeline['leg']['start']-2,timeline['ordinaryContinuation']['lastObservedTail']+1))
 first=groups['FLOOR_STATE'][0];owners={s:(first[f'p{s}'],first[f'main{s}'])for s in(1,2)}
 parts,published,clipped=body.check_body(dict(rows=raw),guest,payload,frames,owners,{1:17,2:18})
 return {**result,'allNativeDMARegisterBindings':len(dmas),'completeNativeBodyCandidates':parts,
         'completePublishedBodyParts':published,'sourceClippedBodyParts':clipped}


def shadow_gate(groups,buffers,text,guest,payload):
 #Whole original compressed-row decoder checks every actual source/copy cadence.
 scope=dict(rows.__dict__,data=lambda folder:(groups,buffers,None,None,None))
 exec(compile(inspect.getsource(rows.inspect),__file__+'::whole_original_compressed_shadow_rows','exec'),scope)
 stepped=scope['inspect'](CASE)
 need(stepped['rowStreamVerified']and not stepped['failures']and not stepped['oversized_rows']and
      set(map(tuple,stepped['identities']))=={(1,17),(2,18)},'All two-slot native compressed shadow rows exact')
 raw=strings(text);begins=raw['MK2_HPHASE_SHADOW_BEGIN'];projections=raw['MK2_HPHASE_PROJECTION']
 num=body.num;bm={(num(r,'frame'),num(r,'slot')):r for r in begins}
 need(len(bm)==len(begins)and bm and set(bm)=={(r['frame'],s)for r in groups['FLOOR_STATE']for s in(1,2)},
      'One original shadow eligibility call for both actual bodies at every drawing field')
 dm=defaultdict(list);pm=defaultdict(list);copies=0
 components=defaultdict(list);native_dma={r['event']:r for r in groups['FLOOR_DMA']}
 for r in groups['SHADOW_COMPONENT']:components[r['frame'],r['row']].append(r)
 for r in raw['MK2_HPHASE_SHADOW_DMA']:dm[num(r,'frame'),num(r,'cache_row')].append(r)
 physical={r['frame']:r for r in capture.compound.square.P.rows(text,'FIELD')}
 for key,r in bm.items():
  frame,slot=key;n=physical[frame+1];prefix='v'if slot==1 else''
  need(num(r,'id')==(17 if slot==1 else 18)and all(num(r,k)==n[prefix+k]for k in('actor','main','owner')),
       'Actual shadow eligibility executes under true owned native physical Main')
  need((num(r,'pc'),num(r,'value'),num(r,'mask'))==(0xff801080,0xb500,65535),'Original shadow eligibility instruction')
 for r in projections:
  frame,slot=num(r,'frame'),num(r,'slot');begin=bm[frame,slot]
  component=num(r,'component');group=native_group(r,payload,guest);part=group[component]
  need(0<=component<len(group)and num(r,'row')==num(r,'cache')+component*112,
       'Shadow projection belongs to exact complete native cache')
  need(all(r[k]==begin[k]for k in('actor','main','owner','id','pose','cache','body','facing'))and num(r,'body')&16,
       'Every projected component belongs to that actual eligible body')
  need(all(num(r,k)==v for k,v in part.items()),'Shadow source geometry is original pose descriptor with native flips')
  need((num(r,'pc'),num(r,'value'),num(r,'mask'))==(0xff8012c0,0x4e90,65535),'Original native projection instruction')
  need(num(r,'floor')==num(r,'stageY')-(134 if slot==1 else 135),'Native Kano/Sonya floor anchors unchanged')
  camera=num(r,'shadow_camera');b2=num(r,'b2');b4=num(r,'b4');a5=num(r,'a5')
  need(camera==(num(r,'b1')|short(camera)&65535)and b4==subxy(num(r,'world'),camera)and
       b2==((num(r,'stageY')-short(camera>>16)+num(r,'b7'))&65535)<<16,
       'Exact actual native world/camera/ground projection registers')
  gap=(short(b2>>16)-(short(b4>>16)-part['dy']))&65535
  x=(short(b4)-part['dx']+(part['width']-1 if part['command']&16 else 0)+short(a5))&1023
  y=(short(b2>>16)-gap//4+short(a5>>16))&511
  actual=dm[frame,num(r,'row')]
  need(len(actual)==part['height']//4+1,'Whole quarter-height native floor-shadow cadence')
  native=[native_dma[c['event']]for c in components[frame,num(r,'row')]]
  need(len(native)==len(actual)and [num(d,'source')for d in actual]==[d['source']for d in native],
       'Every original shadow source binds independent actual DMA and compressed row observations')
  for i,d in enumerate(actual):
   need(tuple(num(d,k)for k in('x','y','width','height','command','palette','color','mask','pc'))==
        (x,(y+i)&511,part['width'],1,part['command']|0x8008,0,0x0f0f,65535,
         0xff801610 if i==len(actual)-1 else 0xff8015a0),'Every shadow copy reaches source-derived absolute floor geometry and black pen')
  copies+=len(actual);pm[frame,slot].append(component)
 for key,r in bm.items():
  expected=list(range(len(native_group(r,payload,guest))))if num(r,'body')&16 else[]
  need(pm[key]==expected,'Every eligible complete owned body has all shadow components; ineligible bodies have none')
 need(copies==stepped['checked_copies'],'All native projected shadow copies accounted by both independent observations')
 return {**stepped,'scope':'Complete original compressed rows, eligibility and absolute floor geometry for this finite CPU compound',
         'absoluteGeometryCopies':copies,'nativeEligibilityCalls':len(begins),'nativeProjectionCalls':len(projections)}


def main(preflight=False):
 need(not OUT.exists(),'Fresh compound render qualification')
 meta=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(meta['passed']and terminal['naturalTerminal']and terminal['exitCode']==meta['nativeExit']==0 and not terminal['observationErrors'],
      'Same actual native game naturally terminal before host qualification')
 need(meta['wholeEarlierPhysicalTrajectoryIdentical']and not capture.original.original.previous.terminal.process_tools.census(),
      'Whole original physical trajectory identical; no additional native replay')
 pins=dict(meta['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'All executed input sources unchanged')
 guest,_,scene,_,extra=capture.init_model();pins.update(extra)
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as f:text=f.read()
 groups,buffers=ring.observations(text,scene.graphics)
 records=json.loads((CASE/'continuous_scene_records.json').read_text());timeline=meta['independentSemantics']
 need([r['frame']for r in records]==list(range(timeline['leg']['start']-1,timeline['ordinaryContinuation']['lastObservedTail']+1)),
      'Every full native screen through leg/Square/ordinary and complete recovery tail')
 for lo,hi in((0xff801070,0xff8017b0),(0xff804000,0xff804470)):
  original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
  need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==original[(lo-0xff800000)//8:(hi-0xff800000)//8],
       'Entire original body/shadow projection and publication kernels unchanged')
 positive=native_gate(groups,records,text,guest,scene.payload,timeline)
 shadow=shadow_gate(groups,buffers,text,guest,scene.payload)
 donor=donor_art(groups,scene.payload,scene.graphics,pins)
 if preflight:
  print(json.dumps(dict(preflightPassed=True,positive=positive,shadow=shadow,donor=donor)),flush=True);return
 rejected=[]
 check=lambda value:native_gate(value,records,text,guest,scene.payload,timeline)
 for label,tag,key,delta in [('ground anchor shifted','FLOOR_QUEUE_TRANSFORM','floor',1),
                           ('camera shifted','FLOOR_QUEUE_TRANSFORM','camera',65536),
                           ('body source shifted','FLOOR_QUEUE_PART','source',1),
                           ('body offset shifted','FLOOR_QUEUE_PART','dy',1),
                           ('unowned DMA source shifted','FLOOR_DMA','source',1),
                           ('native body hidden by classifier','FLOOR_QUEUE_DISPATCH','actor',1)]:
  bad=copy.deepcopy(groups);bad[tag][0][key]+=delta
  try:check(bad)
  except(ValueError,AssertionError,KeyError)as e:rejected.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Accepted real compound record fault '+label)
 for label,tag,key,value in [('shadow absolute camera','MK2_HPHASE_PROJECTION','b4','00000000'),
                            ('shadow ground','MK2_HPHASE_PROJECTION','floor','999'),
                            ('shadow eligibility','MK2_HPHASE_SHADOW_BEGIN','body','0002'),
                            ('shadow source','MK2_HPHASE_SHADOW_DMA','source','00000001'),
                            ('shadow whole position','MK2_HPHASE_SHADOW_DMA','x','999')]:
  line=next(line for line in text.splitlines()if line.startswith(tag+' '))
  badline=re.sub(r'\b'+key+r'=[^\s]+',key+'='+value,line,count=1);bad=text.replace(line,badline,1)
  need(bad!=text,'Actual changed native shadow record')
  try:shadow_gate(groups,buffers,bad,guest,scene.payload)
  except(ValueError,AssertionError,KeyError)as e:rejected.append(dict(fault=label,rejectedBy=str(e)))
  else:raise ValueError('Accepted real shadow record fault '+label)
 need(check(groups)==positive and shadow_gate(groups,buffers,text,guest,scene.payload)==shadow,'Whole compound positive restored after every real fault')
 for module in tuple(sys.modules.values()):
  path=getattr(module,'__file__',None)
  if path and Path(path).resolve().is_relative_to(ROOT/'tools'):pins[str(Path(path).resolve())]=sha(path)
 for path in CASE.rglob('*'):
  if path.is_file():pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All final current inputs/evidence unchanged')
 result=dict(passed=True,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate=capture.original.original.previous.terminal.current.NAME,
             goalStatus='active',nativeTerminal=terminal,wholePhysicalCompound=timeline,completeContinuousRender=meta['continuousRender'],
             nativeFIFOProjectionArt=positive,ownedNativeFloorShadow=shadow,originalDonorArt=donor,actualFaultsRejected=rejected,inputHashes=pins,
             originalStandaloneLegRejectionPreserved=True,fullAudioAcceptance=False,allArenasAccepted=False,fullPortAcceptance=False,
             newNativeBoots=0,newBuilds=0,newZIPs=0,newRawMedia=0,scope=__doc__)
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');h=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==h,'Exact lossless proof compression')
 print(json.dumps(dict(passed=True,fields=len(records),pixels=meta['continuousRender']['exactRGBPixels'],shadowCopies=shadow['absoluteGeometryCopies'],faultsRejected=len(rejected))),flush=True)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
