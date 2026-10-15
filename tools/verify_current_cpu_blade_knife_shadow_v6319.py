"""Complete native fighter body/shadow windows around natural CPU blade/knife.

Current actual112 drawing fields, both true Kano actors. Whole native physical
trajectory unchanged from6303/6311. Preserve full original body/shadow model;
only physical-context/identity binding differs. Projectile/trail raster,
whole RGB erasure/pixel replay, audio and broader arenas stay unaccepted.
"""
import copy,datetime,gzip,inspect,json,re,subprocess,traceback
from collections import defaultdict
from pathlib import Path
import current_payload_metadata_context_v5229 as current
import current_kano_cpu_extended_contract_v6291 as physical
import verify_special_shadow_v5141 as body
ROOT,need,sha=current.ROOT,current.need,current.sha
CASE=ROOT/'audit_v6317_current_cpu_blade_knife_shadow_ram'
OUT=ROOT/'audit_v6320_current_cpu_blade_knife_body_shadow_checked'
PARENT=ROOT/'audit_v6311_current_kano_cpu_blade_knife_checked/report.json'
WINDOWS=(('blade',1870,1912,1871),('knife',2441,2509,2442))


def state_gate(b,guest,payload):
 posts=b['rows']['MK2_HPHASE_POST_FIELD'];lo,hi=b['first'],b['last']
 by={(int(r['frame']),int(r['slot'])):r for r in posts}
 need(len(by)==len(posts)==2*(hi-lo+1)and set(by)=={(f,s)for f in range(lo,hi+1)for s in(1,2)},
      'Entire actual both-slot drawing window, including entry/recovery and tail')
 for (frame,slot),r in by.items():
  need(r['writes']=='0'and r['assistance']=='none'and int(r['id'])==int(r['roster'])==17 and
       int(r['state'])==(1 if slot==1 else 0)and int(r['mode'])==(7 if frame==2441 else 2)and int(r['floor'])==82,
       'Actual native identities/roles/source-derived floor, including real round handoff')
  target=b['physicalRound'][frame+1,slot]
  keys=('actor','main','owner','id','action','y','floor','vx','vy','gravity','flags','body','trail','hp','mode')
  need(all(int(r[k],16 if k in body.HEX else 10)==target[k]for k in keys),
       'Every post-draw field agrees with next complete native physical callback')
  actual=b['physicalPair'].get(frame+1)
  if actual:
   prefix='v'if slot==1 else''
   need(all(int(r[k],16 if k in body.HEX else 10)==actual[prefix+k]for k in('actor','main','owner','pose','action','floor','vx','vy','gravity','flags','body','trail')),
        'Draw-complete pose/locks/motion bind to next original live actor observation')
   need(int(r['x'])==actual['vxpos'if slot==1 else'x']and int(r['y'])==actual['vypos'if slot==1 else'y'],
        'Actual post-draw whole-body location bound to next live raw/integer motion records')
 return dict(passed=True,first=lo,last=hi,bothSlotDrawFields=len(posts),actualNativeCPU=17,actualHuman=17,
             completePhysicalMotionDamageCleanupProof=str(PARENT),completePhaseContactProofRetained=True)


def bindings():
 source=inspect.getsource(body.check)
 first=source.index(' # The older physical/ownership/health checker');last=source.index(" fields=rows['MK2_HPHASE_POST_FIELD']",first)
 source=source[:first]+" state=state_gate(b,guest,payload)\n entry_frames={b['entry']}\n"+source[last:]
 before='ids={side:identity,3-side:4}'
 need(source.count(before)==1,'Only real CPU/human identity adaptation');source=source.replace(before,'ids={1:17,2:17}',1)
 scope=dict(body.check.__globals__,state_gate=state_gate)
 exec(compile(source,__file__+'::whole_original_body_shadow_native_CPU_context','exec'),scope)
 return scope['check']


def main():
 need(not OUT.exists(),'Fresh immutable body/shadow qualification')
 report=json.loads((CASE/'result.json').read_text());terminal=json.loads((CASE/'native_terminal.json').read_text())
 need(report['passed']and report['nativeExit']==0 and terminal['exitCode']==0 and terminal['naturalTerminal']and
      not terminal['observationErrors']and report['originalWholePhysicalTrajectoryUnchanged']and
      report['proof']['everyActualByteComparedInRAM']and report['proof']['sha256']==current.GUEST_SHA,
      'Actual current whole-guest RAM proof and naturally terminal same native trajectory')
 parent=json.loads(PARENT.read_text());need(parent['passed']and parent['goalStatus']=='active','Full goal retained')
 pins=dict(report['inputHashes']);need(all(sha(p)==h for p,h in pins.items()),'Every executed input unchanged')
 guest=current.expected();payload=(ROOT/current.NAME/'roms/mk2ks/mk2ks.mdata').read_bytes()
 baseline_path=ROOT/'audit_v5142_special_shadow_ring_p1_checked/report.json';baseline=json.loads(baseline_path.read_text())
 for path in(Path(body.__file__),ROOT/'tools/verify_move_phase_shadow_v5089.py',ROOT/'mk2ks_special_shadow_v5131.lua'):
  need(sha(path)==baseline['inputHashes'][str(path.resolve())],'Full original qualified body/shadow source unchanged');pins[str(path.resolve())]=sha(path)
 gfx=body.reconstruct(pins);added=current.expected_gfx()
 need(len(added)==18976,'Whole actual current appended graphics layout')
 gfx[0x1fa0000:0x1fa0000+11944]=added[:11944];gfx[0x1fa4000:0x1fa4000+7032]=added[11944:]
 old=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
 for lo,hi in((0xff801070,0xff8017b0),(0xff804160,0xff804430)):
  need(guest[(lo-0xff800000)//8:(hi-0xff800000)//8]==old[(lo-0xff800000)//8:(hi-0xff800000)//8],
       'Entire original body/direct-shadow kernels unchanged')
 with gzip.open(CASE/'run.log.gz','rt',encoding='utf-8')as file:text=file.read()
 with gzip.open(ROOT/'audit_v6303_current_kano_cpu_confirm265_ram/run.log.gz','rt',encoding='utf-8')as file:original=file.read()
 prefixes=('MK2_CPU_PAIR_','MK2_P2CPU_','MK2_CPU_ROUND_','MK2_CPU_OVERLAP_','MK2_KNIFE_PAIR_','MK2_CPU_CHOICE_')
 need([s for s in text.splitlines()if s.startswith(prefixes)]==[s for s in original.splitlines()if s.startswith(prefixes)],
      'Every current original physical/AI/RNG/health/state record unchanged under added observers')
 rows=defaultdict(list)
 for line in text.splitlines():
  if line.startswith('MK2_HPHASE_'):
   pairs=re.findall(r'(\w+)=([^\s]+)',line);need(len(pairs)==len(dict(pairs)),'Unique actual drawing protocol fields')
   rows[line.split()[0]].append(dict(pairs))
 streams=json.loads((CASE/'shadow_stream_memory_proofs.json').read_text())
 native_round={(r['frame'],r['slot']):r for r in physical.knife.R.rows(text,'FIELD')}
 native_pair={r['frame']:r for r in physical.original.pair.rows(text,'FIELD')}
 check=bindings();cases=[];rejected=[]
 for move,lo,hi,entry in WINDOWS:
  selected=defaultdict(list,{tag:[r for r in values if lo<=int(r['frame'])<=hi]for tag,values in rows.items()})
  used={f'{r["graphic"]}_{r["width"]}_{r["height"]}_{r["command"]}'for r in selected['MK2_HPHASE_PROJECTION']}
  chosen=[r for r in streams if r['stream']in used];need({r['stream']for r in chosen}==used,'Every actual finite-window source stream retained')
  b=dict(move=move,side=2,first=lo,last=hi,entry=entry,rows=selected,streams=chosen,physicalRound=native_round,physicalPair=native_pair)
  proof=check(b,guest,payload,gfx);cases.append(proof)
  trials=[('entry_body_source','MK2_HPHASE_CANDIDATE','source','00000000'),
   ('shadow_owner','MK2_HPHASE_SHADOW_BEGIN','owner','01000000'),
   ('shadow_eligibility','MK2_HPHASE_SHADOW_BEGIN','body','0002'),
   ('projection_origin','MK2_HPHASE_PROJECTION','dx','999'),
   ('camera','MK2_HPHASE_PROJECTION','b4','00000000'),
   ('floor','MK2_HPHASE_PROJECTION','floor','999'),
   ('shadow_x','MK2_HPHASE_SHADOW_DMA','x','999'),
   ('shadow_pen','MK2_HPHASE_SHADOW_DMA','color','0101'),
   ('shadow_source','MK2_HPHASE_SHADOW_DMA','source','00000001'),
   ('post_actor_proxy','MK2_HPHASE_POST_FIELD','id','1'),
   ('post_pose','MK2_HPHASE_POST_FIELD','pose','00000000')]
  for label,tag,key,value in trials:
   changed=dict(b,rows=copy.deepcopy(selected))
   index=next(i for i,r in enumerate(changed['rows'][tag])if int(r['frame'])==entry)if label=='entry_body_source'else 0
   need(changed['rows'][tag][index][key]!=value,'Actual changed drawing record, never a no-op')
   changed['rows'][tag][index][key]=value
   try:check(changed,guest,payload,gfx)
   except ValueError as error:rejected.append(dict(move=move,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Accepted actual body/shadow fault '+move+':'+label)
  for label in('actual_rom_bytes','packed_row_start'):
   changed=dict(b,streams=copy.deepcopy(chosen))
   if label=='actual_rom_bytes':changed['streams'][0]['sha256']='0'*64
   else:changed['streams'][0]['actualRowStarts'][1]+=1
   try:check(changed,guest,payload,gfx)
   except ValueError as error:rejected.append(dict(move=move,fault=label,rejectedBy=str(error)))
   else:raise ValueError('Accepted actual ROM-stream fault '+move+':'+label)
  need(check(b,guest,payload,gfx)==proof,'Original finite-window positive restored after all real faults')
 for path in(PARENT,baseline_path,Path(__file__),Path(physical.__file__),*(p for p in CASE.rglob('*')if p.is_file())):
  pins[str(path.resolve())]=sha(path)
 need(all(sha(p)==h for p,h in pins.items()),'All source/native/evidence bytes unchanged')
 result=dict(passed=True,candidate=current.NAME,observedUTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             goalStatus='active',parentAdditiveJournal=str(PARENT),remaining=parent['remaining'],cases=cases,
             actualDrawingFields=112,actualBothSlotBodyShadowFields=224,actualSemanticFaultsRejected=rejected,
             currentActualWholePhysicalTrajectoryUnchanged=True,wholeNativeStateHealthAndChoices=report['independentSemantics']['nativeStateHealthAndChoices'],
             fullOriginalBodyShadowModelRetained=True,wholeRGBPixelReplayAccepted=False,bladeEffectRasterAccepted=False,
             knifeEffectRasterAccepted=False,allCPUContextsArenasKOOverlapArtAudioAccepted=False,fullAudioAcceptance=False,
             fullPortAcceptance=False,fullGoalComplete=False,newBuilds=0,newZIPs=0,newRawMedia=0,inputHashes=pins,scope=__doc__,
             previousGoalTurnClassification='progress: complete current CPU blade/blocked-knife motion/contact and21 real faults',
             thisGoalTurnClassification='progress: additional bounded current native body/shadow observations and independent original-kernel qualification',
             nextAction='Remaining independent effect-raster/whole-scene erasure/audio and broader integration; keep full objective active')
 OUT.mkdir();path=OUT/'report.json';path.write_text(json.dumps(result,indent=2)+'\n');digest=sha(path)
 need(subprocess.run(['compact.exe','/C','/EXE:LZX','/F','/I','/Q',str(path)],capture_output=True).returncode==0 and sha(path)==digest,
      'Exact lossless compact qualification report')
 print(json.dumps(dict(passed=True,cases=cases,actualFaultsRejected=len(rejected),newBuilds=0)),flush=True)


if __name__=='__main__':
 try:main()
 except Exception as error:
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
