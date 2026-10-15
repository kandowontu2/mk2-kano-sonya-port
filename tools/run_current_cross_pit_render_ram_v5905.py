"""Current5219 cross Pit: complete original movie/ground/shadow/erase in RAM.

Entire5820 cold transport and3642 continuous raster pipeline retained. The
whole2092 Pit observer,2107native phase/constructor/FIFO contract and2136all31
movie faults replace Tomb-only branches. No build or raw recording copies.
"""
import argparse,gzip,hashlib,inspect,json,os,re,subprocess,traceback
from pathlib import Path
import run_current_held_tomb_render_ram_v5820 as base
import run_current_cross_pit_winner_mix_v5894 as timing
import current_pit_render_model_v5902 as model
import current_pit_scene_contract_v5903 as contract
import current_cross_pit_earned_state_v5893 as native
ROOT,need,sha,current,old=base.ROOT,base.need,base.sha,base.current,base.old
once=timing.once
OBSERVER=ROOT/'mk2ks_current_cross_pit_display_ram_v5904.lua'
scene_contract=contract.scene_contract

def paths(fighter,side):
 need(fighter in ('kano','sonya')and side in (1,2),'Exact native cross character and slot')
 return ROOT/f'audit_v5906_current_cross_pit_{fighter}_p{side}_render_ram',ROOT/f'audit_v5907_current_cross_pit_{fighter}_p{side}_render_checked'

def controls():
 source=(ROOT/'mk2ks_native_pit_display_v2092.lua').read_text()
 changes=(
  ("dofile('mk2ks_native_stage_performer_v806.lua')","dofile('mk2ks_current_cross_tomb_provenance_v5834.lua')"),
  ("local f=assert(io.open(output..'/'..file,'wb'));f:write(raw);f:close()",'MK2KS_TOMB_RAM_SAVE(file,raw)'),
  ('screen:snapshot(file)','MK2KS_TOMB_RAM_PIXELS(file)'),
 )
 for before,after in changes:source=once(source,before,after)
 need(not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)|io\.open|snapshot\(',source),
      'Entire original Pit observer retained passive, only driver and RAM sinks change')
 wrapper=(ROOT/'mk2ks_native_tomb_ram_v3624.lua').read_text()
 need(wrapper.count('assert(count==1)')==3,'Original three driver/sink substitutions')
 for before,after,count in (
  ('mk2ks_native_tomb_display_v2062.lua','mk2ks_native_pit_display_v2092.lua',1),
  ("dofile%('mk2ks_stage_branch_provenance_v1722%.lua'%)","dofile%('mk2ks_native_stage_performer_v806%.lua'%)",1),
  ("dofile('mk2ks_current_stage_provenance_v3595.lua')","dofile('mk2ks_current_cross_tomb_provenance_v5834.lua')",1),
 ):
  need(wrapper.count(before)==count,'Whole3624wrapper declared target count')
  wrapper=wrapper.replace(before,after,count)
 declared=OBSERVER.read_text()
 need(all(s in declared for s in ('mk2ks_native_tomb_ram_v3624.lua',
      'mk2ks_native_pit_display_v2092.lua','mk2ks_current_cross_tomb_provenance_v5834.lua',
      'assert(count==pair[3])',"emu.time()>=890")) and
      not re.search(r':write_|write_u\d+|set_value|clear_value|load_?state|\.value\s*=(?!=)',declared),
      'Passive entire3624 RAM wrapper and failure-only890deadline')
 current.expected()
 proof=json.loads((timing.source.OUT/'report.json').read_text())
 need(proof['passed'] and all(sha(p)==h for p,h in proof['inputHashes'].items()),
      'Whole cold current physical Pit/audio source proof unchanged')
 return hashlib.sha256(source.encode()).hexdigest().upper()

def preflight(guest,payload,image):
 observer=controls()
 for ids in ((17,18),(18,17)):
  need(model.Model(guest,payload,image,ids).ids==ids,'Both real opposite physical tuples')
 rejected=[]
 for ids in ((17,1),(1,17),(18,0),(17,),(17,18,17)):
  try:model.Model(guest,payload,image,ids)
  except ValueError:rejected.append(ids)
  else:raise ValueError('Proxy/invalid physical tuple admitted')
 return dict(observerSHA256=observer,modelSHA256=model.MODEL_SOURCE_SHA256,
             nativeMovieContractSHA256=contract.NATIVE_SOURCE_SHA256,
             actualMovieFaultContractSHA256=contract.FAULT_SOURCE_SHA256,
             earnedContractSHA256=native.CONTRACT_SHA256,rejectedProxyTuples=rejected)

run_source=inspect.getsource(base.run)
run_source=once(run_source,"identity=17 if fighter=='kano'else 18;ids=(identity,identity)",
 "identity=17 if fighter=='kano'else 18;ids=tuple(identity if slot==side else 35-identity for slot in(1,2))")
run_source=once(run_source,'audit_v5786_current_enabled_tomb_winner_mix_checked/report.json',
 'audit_v5899_current_cross_pit_winner_mix_checked/report.json')
run_source=once(run_source,"matrix['actualCurrentBothCharactersBothSidesHeldTombEnabledWinnerMixAccepted']",
 "matrix['actualCurrentBothCharactersBothSidesPitEnabledWinnerMixAccepted']")
start=run_source.index("    branch_reference=case['sourceQualifiedNativeBranch']")
end=run_source.index("    reference=Path(case['capture'])",start)
run_source=run_source[:start]+"    native_reference=case['nativePitPhysicalState']\n    need(native_reference['earned_matches']==7 and native_reference['consecutive_fields']==801,'Actual full seven-match native Pit audio reference')\n"+run_source[end:]
run_source=once(run_source,'image=old.source_graphics(payload,graphics_pins)',
 'image=pit_contract.source_graphics(payload,graphics_pins)')
for before,after in (
 ('mk2ks_native_tomb_display_v2062.lua','mk2ks_native_pit_display_v2092.lua'),
 ('mk2ks_tomb_mirror_driver_ram_v4340.lua','mk2ks_current_cross_tomb_driver_v5833.lua'),
 ('mk2ks_tomb_mirror_provenance_ram_v4341.lua','mk2ks_current_cross_tomb_provenance_v5834.lua'),
 ("MK2KS_STAGE_ARENA='1'","MK2KS_STAGE_ARENA='6'"),
 ('MK2_CURRENT_TOMB_RENDER_DEADLINE','MK2_CURRENT_PIT_RENDER_DEADLINE'),
 ('actualCurrentHeldMirrorNativeTombWholeRenderPaletteShadowEraseAccepted=True',
  'actualCurrentCrossNativePitWholeRenderPaletteShadowEraseAccepted=True'),
 ('nativeScene=contract,nativeBranch=branch,nativeMirrorPaletteSelectors=palettes,',
  "nativeScene=contract,nativePitPhysicalState=contract['nativeState'],nativeCrossPaletteSelectors=palettes,"),
 ('true mirror complete native scene RAM','true cross complete native Pit scene RAM'),
 ('mirror {len(scene.records)} whole fields exact','Pit {len(scene.records)} whole fields exact'),
):run_source=once(run_source,before,after)
start=run_source.index('    branch=branches.branch(text,guest,fighter,side)')
end=run_source.index('    palettes=',start)
run_source=run_source[:start]+"    need(contract['nativeState']==native_reference,'Entire independent physical Pit state matches enabled-audio capture')\n"+run_source[end:]
run_source=once(run_source,"need(palettes=={1:[False],2:[True]},'Normal native mirror selection gives exactly P1normal/P2alternate, no forced flags')",
 "need(palettes=={1:[False],2:[False]},'Actual cross physical bodies retain original normal palettes')")
# Keep module pins and all original collector/terminal/raw-copy checks.
run_source=once(run_source,"    contract=scene_contract(scene,text,guest,payload,fighter,side,reference,ids)",
 "    contract=scene_contract(scene,text,guest,payload,fighter,side,reference,ids)")
scope=dict(vars(base),__file__=__file__,__doc__=__doc__,paths=paths,preflight=preflight,controls=controls,
           scene_contract=scene_contract,model=model,native=native,timing=timing,OBSERVER=OBSERVER,pit_contract=contract)
exec(compile(run_source,__file__+'::entire5820_native_current_Pit_cold_RAM','exec'),scope)
run=scope['run'];run.source=run_source

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 CASE,OUT=paths(args.fighter,args.side)
 try:report=run(args.fighter,args.side)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 need(not OUT.exists(),'Never overwrite current native Pit result');OUT.mkdir()
 need(subprocess.run(['compact.exe','/C','/I','/Q','/S:'+str(OUT)],capture_output=True).returncode==0,'Bounded report text compressed')
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in ('inputHashes','nativeScene','nativePitPhysicalState')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
