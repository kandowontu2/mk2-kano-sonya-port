"""Current true-ID swallowing: whole enabled native DAC/PCM/ROM in RAM.

Original physical native controls and full source-qualified inter-round
refill/stream/disappearance/retirement state, plus every prior current native
event. No proxy, raw media, copied build, waveform fit or state injection.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_subzero_audio_v6213 as original
import checkpoint_current_subzero_audio_v6219 as lifetime
import current_mileena_native_refill_v6085 as health
ROOT,need,sha=original.ROOT,original.need,original.sha
LUA='mk2ks_current_mileena_audio_v6229.lua'
PARENT=ROOT/'audit_v6228_current_stock_finisher_audio_progress/progress.json'

def state(text,fighter,side,guest):
 native=health.gate(health.original.parse(text),fighter,side,guest)
 need(native['passed'],'Entire original native earned/refill/stream/removal/terminal state '+repr(native['errors']))
 def rows(value):return [s.strip()for s in value.splitlines()if s.startswith(('MK2_MILEENA_V3784_','MK2_CACHE_V3823_'))]
 reference=ROOT/f'audit_v6088_current_mileena_{fighter}_p{side}/run.log'
 actual=rows(text);prior=rows(reference.read_text())
 need(actual==prior,'Every existing true-ID current native control/health/task/cache/cleanup event identical')
 return dict(native,nativeStateRows=len(actual),sourceQualifiedCurrentLifecycle=str(reference))

def dac_models(callbacks):
 code=inspect.getsource(original.dac_models)
 need(code.count('1600<callbacks<2100')==1,'Only declared600field callback-duration scope changes')
 code=code.replace('1600<callbacks<2100','500<callbacks<650',1)
 scope=dict(original.dac_models.__globals__)
 exec(compile(code,__file__+'::whole_native_DAC600field_scope','exec'),scope)
 return scope['dac_models'](callbacks)

def run(fighter,side):
 code=inspect.getsource(original.run)
 def replace(before,after):
  nonlocal code
  need(code.count(before)==1,'One entire original RAM collector adaptation')
  code=code.replace(before,after,1)
 replace('audit_v6214_current_subzero_{fighter}_p{side}_native_audio','audit_v6231_current_mileena_{fighter}_p{side}_native_audio')
 replace('gfx=current.expected_gfx()','gfx=b\'\'')
 first=code.index(' files=[ROOT/leaf for leaf in (LUA,');last=code.index(' controller=',first)
 code=code[:first]+" files=[ROOT/leaf for leaf in (LUA,'mk2ks_mileena_earned_fixed_v3824.lua','mk2ks_cache_provenance_mileena_fixed_v3823.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')]\n"+code[last:]
 replace('Path(__file__),Path(current.__file__),Path(model.__file__),',
         'Path(__file__),Path(original.__file__),Path(lifetime.__file__),Path(health.__file__),Path(health.original.__file__),Path(current.__file__),Path(model.__file__),')
 replace("env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',\n            MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')",
         "env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_PROVENANCE_MIN_FRAME='0')")
 replace("'-nosamples'","'-samples'")
 replace("need(seen_guest==2 and seen_gfx==1 and len(raw_proofs)==4,'Whole driver plus audio guest and four native transitions')",
         "need(seen_guest==1 and seen_gfx==0 and len(raw_proofs)==0,'Whole actual native audio guest; no redundant raster transport')")
 first=code.index(" rows=[dict(fields(line),tag=line.split()[0])");last=code.index(' gate,fault,gate_sha=',first)
 code=code[:first]+" native=state(text,fighter,side,guest)\n end=[native]\n imported_channels=lifetime.inactive_channels(text,pcm_headers)\n"+code[last:]
 replace('nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,',
         'nativeDCSWaveformAccepted=True,samplesEnabled=True,importedVictimMixAccepted=False,allEnabledImportedSourcesInactive=True,importedChannelsObserved=imported_channels,nativeEarnedState=native,')
 scope=dict(original.run.__globals__,__file__=__file__,original=original,lifetime=lifetime,health=health,
            LUA=LUA,PARENT=PARENT,state=state,dac_models=dac_models)
 exec(compile(code,__file__+'::whole6213_current_Mileena_source_audio','exec'),scope)
 return scope['run'](fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  folder=ROOT/f'audit_v6231_current_mileena_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():original.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
