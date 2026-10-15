"""Validate retained full5906RAM renderer and whole native phase-ground successor.

All four native runs exited normally and every live one-base raster check
completed. Preserve the failed5907post-check and its exact source. Requalify
the actual complete movie with5908original-Pit floor phases, never rerun or
reconstruct raw targets. Rebuild only source-native graphics streams in RAM
from unchanged ROM/payload bytes for the original compressed-shadow scanner.
"""
import argparse,collections,gzip,hashlib,inspect,json,re,subprocess,traceback
from pathlib import Path
from types import SimpleNamespace
import run_current_cross_pit_render_ram_v5905 as executed
import current_pit_phase_ground_contract_v5908 as contract
ROOT,need,sha,current,model=executed.ROOT,executed.need,executed.sha,executed.current,executed.model

def load_scene(folder,guest,payload,pins):
 image=contract.source_graphics(payload,pins)
 parser_source=inspect.getsource(model.original.parse)
 needle="{'register','words','reason'}"
 need(parser_source.count(needle)==1,'Exactly one digest transport parser string extension')
 parser_source=parser_source.replace(needle,"{'register','words','reason','data_sha256'}",1)
 scope=dict(vars(model.original));exec(compile(parser_source,__file__+'::whole3642_digest_transport_parser','exec'),scope)
 parse=scope['parse'];groups=collections.defaultdict(list);buffers={};owners=collections.defaultdict(list);cpu_count=0
 with gzip.open(folder/'run.log.gz','rt')as reader:text=reader.read()
 for line in text.splitlines():
  parsed=parse(line)
  if not parsed:continue
  kind,row=parsed
  if kind=='FLOOR_CPU':cpu_count+=1;continue
  groups[kind].append(row)
  if kind=='FLOOR_GFX':
   need('data'not in row and 0<=row['first']<row['first']+row['bytes']<=len(image),
        'Actual observed complete graphics digest, no raw sprite file or substituted range')
   raw=image[row['first']:row['first']+row['bytes']]
   need(hashlib.sha256(raw).hexdigest().upper()==row['data_sha256'] and row['key']not in buffers,
        'Every observed graphics stream digest equals the entire independent source range')
   # This is independent source, not a recovered comparison target.
   buffers[row['key']]=dict(row,data=raw.hex())
  if kind=='FLOOR_OWNER':owners[row['frame'],row['source'],row['slot']].append(row)
 records=json.loads((folder/'continuous_scene_records.json').read_text())
 buffers_json=json.loads((folder/'buffer_digests.json').read_text())
 visible=json.loads((folder/'visible_digests.json').read_text())
 origin=groups['FLOOR_BEGIN'][0]['origin'];end=groups['FLOOR_RETIRED'][0]['frame']
 expected=list(range(origin+1,end+31))
 need([r['frame']for r in records]==expected and all(r['exactVRAMWords']==262144 and
      r['exactRGBPixels']==101600 and set(r['body'])=={'1','2','4'}for r in records),
      'Every actual completed full native VRAM/RGB/cinematic body field retained')
 need(len(visible)==len(records) and all(v['file']==f"display_{r['frame']}.png" and
      v['rgbSHA256']==r['rgbSHA256']for v,r in zip(visible,records)),
      'Every complete live RGB target digest binds its independently modeled full field')
 transported=[]
 for line in text.splitlines():
  if line.startswith('MK2_TOMB_RAM_BUFFER_CHECKED '):
   row=dict(re.findall(r'(\w+)=([^\s]+)',line))
   transported.append(dict(file=row['file'],bytes=int(row['bytes']),changedBlocks=int(row['blocks']),rawSHA256=row['sha256']))
 need(buffers_json==transported and len({r['file']for r in transported})==len(transported),
      'Every actual whole guest/base/pre/shift/VRAM/palette RAM transport digest retained uniquely')
 need(transported[0]['file']=='guest_maincpu.bin' and transported[0]['rawSHA256']==current.GUEST_SHA and
      len(groups['FLOOR_BASE'])==1 and sum(r['file']=='display_base.bin'for r in transported)==1,
      'Entire initialized guest and exactly one native base, never per-frame target anchors')
 files={r['file']for r in transported}
 need(all(r['file']in files for tag in ('FLOOR_BASE','FLOOR_PRE_FRAME','FLOOR_SHIFT_DATA','FLOOR_LATCH','FLOOR_HELD')for r in groups[tag]) and
      all(r['palette_file']in files for r in groups['FLOOR_DISPLAY']),
      'No omitted actual frame, source shift, palette or scanout comparison target')
 need(sum(r['modeledFlip']for r in records)==len(groups['FLOOR_LATCH']) and
      len(records)-sum(r['modeledFlip']for r in records)==len(groups['FLOOR_HELD']),
      'Exact complete flip and held-scanout inventory')
 # The immutable executed whole3642 snapshot method unconditionally executes
 # both actual VRAM/RGB negative checks and restoration on the first field.
 need(model.source==inspect.getsource(model.original.Model).replace(
      "check_owned_body_palette(q,colors,self.guest,self.ids,q['slot'])",'owned_palette(self,q,colors)',1).replace(
      'for n in(1,2)})','for n in(1,2,4)})',1),
      'Entire executed continuous raster and actual first-field negative/restoration gates unchanged')
 scene=SimpleNamespace(groups=groups,buffers=buffers,owners=owners,records=records,
                       pre_count=len(groups['FLOOR_PRE_FRAME']),flip_count=len(groups['FLOOR_LATCH']),
                       loads=len(groups['FLOOR_SHIFT_LOAD']),fills=len(groups['FLOOR_SHIFT_FILL']),
                       retainedLivePipelinePassedBeforeErroneousGroundGate=True,
                       retainedLiveActualPixelFaultGateCompleted=True,allActualTransportDigestsVerified=True)
 return scene,text,cpu_count

def run(fighter,side):
 folder,failed_out=executed.paths(fighter,side)
 meta=json.loads((folder/'result.json').read_text());failed=json.loads((failed_out/'report.json').read_text())
 before=json.loads((folder/'input_hashes_before.json').read_text())
 need(meta['captureCompleted'] and meta['exit_code']==0 and meta['candidate']==current.NAME and
      meta['fighter']==fighter and meta['side']==side and meta['modelErrors']==[] and
      meta['observedRGBFields']==meta['modelExactFields'] and meta['modelExactFields']in(676,677) and
      meta['ramGuestSHA256']==current.GUEST_SHA and meta['executable_sha256']==current.EXE_SHA and
      meta['payload_sha256']==current.PAYLOAD_SHA and meta['guest_writes']==0 and meta['assistance']=='none' and
      not meta['cheats_enabled'] and meta['rawImageAudioVRAMROMCopiesWritten']==0 and meta['input_hashes']==before,
      'Actual terminal and entire unassisted completed live raster pipeline, no failure hidden')
 need(failed['passed']is False and failed['error']=="ValueError('Physical own native ground anchor remains aligned before cinematic retirement')" and
      'current_pit_scene_contract_v5903.py'in failed['traceback'],
      'Preserve exact executed erroneous Tomb-style post-gate; no game/render failure waived')
 pins=dict(before)
 for p,h in pins.items():need(sha(p)==h,'Every actual executed and compiled input remains exact '+p)
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 need(executed.controls()=='4502BD84CE27BD5F8BA4A0D02575D25029C1F69B9982449D3B786201AC09B07A',
      'Executed entire2092 passive observer with only exact driver/RAM sinks substitutions')
 scene,text,cpu_count=load_scene(folder,guest,payload,pins)
 need(not re.search(r'LUA ERROR|Lua error|stack traceback|Fatal error|WRONG CHECKSUMS|might not run correctly|MK2_CURRENT_PIT_RENDER_DEADLINE',text,re.I) and
      (folder/'stderr.log').read_text()=='','No native, deadline or rendering failure')
 matrixpath=ROOT/'audit_v5899_current_cross_pit_winner_mix_checked/report.json';matrix=json.loads(matrixpath.read_text())
 need(matrix['passed'],'Retained independent actual complete audio reference')
 ref=next(c for c in matrix['cases']if c['fighter']==fighter and c['physicalSlot']==side)
 identity=17 if fighter=='kano'else 18;ids=tuple(identity if s==side else 35-identity for s in(1,2))
 proof=contract.scene_contract(scene,text,guest,payload,fighter,side,Path(ref['capture']),ids)
 need(proof['nativeState']==ref['nativePitPhysicalState'] and len(scene.records)==meta['modelExactFields'],
      'Full actual native physical/cinematic proof and exact retained live full-scene fields')
 for p in folder.rglob('*'):
  if not p.is_file():continue
  need(p.suffix.lower()not in('.png','.wav','.bin','.pcm','.rgb','.exe','.zip','.mdata'),
       'No raw recording, playable ROM or build duplicate')
  pins[str(p)]=sha(p)
 for p in (matrixpath,failed_out/'report.json',Path(__file__).resolve(),Path(contract.__file__).resolve()):pins[str(p)]=sha(p)
 need(all(sha(p)==h for p,h in pins.items()),'Every current/compiled/failed/executed/source/result byte preserved')
 return dict(passed=True,fighter=fighter,physicalSlot=side,candidate=current.NAME,capture=str(folder),
  actualCurrentCrossPitCompleteRetainedNativeSceneAccepted=True,nativeScene=proof,
  retainedLiveExactFields=len(scene.records),retainedLiveExactRGBPixels=len(scene.records)*101600,
  retainedLiveExactCPUWrites=cpu_count,retainedLiveActualPixelFaultGateCompleted=True,
  liveRasterSourceSHA256=model.MODEL_SOURCE_SHA256,phaseGroundContractSHA256=contract.CONTRACT_SOURCE_SHA256,
  executedFailedPostGatePreserved=str(failed_out/'report.json'),newNativeBoots=0,newRastersReplayed=0,
  sourceGraphicsReconstructedOnlyInRAM=True,rawTargetsReconstructed=False,
  completeStageVictimAudioAccepted=False,independentStockChoreographyAccepted=False,fullPortAcceptance=False,
  rawGuestRGBPCMFilesWritten=0,newBuilds=0,publicPlayableChanged=False,inputHashes=pins,scope=__doc__)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 OUT=ROOT/f'audit_v5910_current_cross_pit_{args.fighter}_p{args.side}_retained_scene_checked'
 need(not OUT.exists(),'Fresh whole current Pit successor, no failed source/result edits')
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Bounded successor text compressed')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','nativeScene')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
