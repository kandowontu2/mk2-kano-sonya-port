"""Four remaining current stock finisher audio consumers; no new art capture.

Preserve the complete6213 RAM collector/source sound models. Observe actual
enabled channels and qualify every existing earned1021 state row against
the matching source-qualified current scene, including native continuation.
"""
import argparse,inspect,json,re,traceback
from pathlib import Path
import capture_current_subzero_audio_v6213 as original
import checkpoint_current_subzero_audio_v6219 as lifetime
ROOT,need,sha=original.ROOT,original.need,original.sha
LUA='mk2ks_current_stock_finisher_audio_v6221.lua'
PARENT=ROOT/'audit_v6220_current_subzero_audio_progress/progress.json'
CONFIG={
 'kitana':dict(killer='kitana',id=4,entry=0xff8cc2d0,command='ffdf_lk_release',gap='64',reference=6114),
 'kung_lao':dict(killer='kung_lao',id=0,entry=0xff8c6040,command='fff_lk',gap='112',reference=6126),
 'jax_clap':dict(killer='jax',id=11,entry=0xff8c7820,command='fff_lp_release',gap='64',reference=6135),
 'jax_arms':dict(killer='jax',id=11,entry=0xff8be240,command='bbbb_lp',gap='96',reference=6142),
}

def state(text,fighter,side,variant,guest):
 config=CONFIG[variant]
 def rows(value):
  return [line.strip()for line in value.splitlines()if line.startswith('MK2_STOCK_HEAD_V921_')]
 reference=ROOT/f'audit_v{config["reference"]}_current_{variant}_{fighter}_p{side}_native_scene_ram/run.log'
 need(reference.exists(),'Existing matching current source-qualified native scene')
 old=rows(reference.read_text());new=rows(text)
 need(old==new and len(new)>200,'All real physical controls/health/commands/tables/completion/continue rows equal full current scene')
 action=[original.fields(line)for line in new if line.startswith('MK2_STOCK_HEAD_V921_ACTION ')]
 result=[original.fields(line)for line in new if line.startswith('MK2_STOCK_HEAD_V921_RESULT ')]
 need(len(action)==len(result)==1 and action[0]['damage']=='322'and result[0]['damage']=='322'and
      result[0]['wins']=='2'and int(result[0]['frame'])==int(action[0]['frame'])+750 and
      int(action[0]['address'],16)==config['entry'],'Actual two earned KOs and whole750field finisher/continuation terminal')
 # Bind the actual entry to one of the true stock actor's original action
 # table rows in the independently reconstructed current whole guest.
 import struct
 entries=[struct.unpack_from('<I',guest,(table-0xff800000)//8+config['id']*4)[0]for table in (0xff8ba210,0xff8ba390)]
 need(config['entry']in entries,'Original stock action table, not forced routine dispatch')
 return dict(nativeStateRows=len(new),sourceQualifiedCurrentScene=str(reference),origin=int(action[0]['frame']),
             nativeCollisionDamage=322,nativeKOs=2,wholePostActionFields=750,terminal=result[0])

def dac_models(callbacks):
 need(600<callbacks<750,'Entire750field native finisher audio window')
 code=inspect.getsource(original.dac_models)
 need(code.count('1600<callbacks<2100')==1,'Only declared callback-duration scope changes')
 code=code.replace('1600<callbacks<2100','600<callbacks<750',1)
 scope=dict(original.dac_models.__globals__)
 exec(compile(code,__file__+'::whole_source_native_DAC_duration','exec'),scope)
 return scope['dac_models'](callbacks)

def run(fighter,side,variant):
 config=CONFIG[variant];code=inspect.getsource(original.run)
 def replace(before,after):
  nonlocal code
  need(code.count(before)==1,'One complete original RAM collector adaptation')
  code=code.replace(before,after,1)
 replace('audit_v6214_current_subzero_{fighter}_p{side}_native_audio','audit_v6223_current_{variant}_{fighter}_p{side}_native_audio')
 replace('gfx=current.expected_gfx()','gfx=b\'\'')
 first=code.index(' files=[ROOT/leaf for leaf in (LUA,');last=code.index(' controller=',first)
 code=code[:first]+" files=[ROOT/leaf for leaf in (LUA,'mk2ks_stock_extended_earned_ram_v3958.lua','mk2ks_stock_fatality_v1021.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')]\n"+code[last:]
 replace('Path(__file__),Path(current.__file__),Path(model.__file__),',
         'Path(__file__),Path(original.__file__),Path(lifetime.__file__),Path(current.__file__),Path(model.__file__),')
 replace("env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',\n            MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')",
         "env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER=config['killer'],MK2KS_STOCK_COMMAND=config['command'],MK2KS_STOCK_GAP=config['gap'],MK2KS_AUDIO_ENTRY=str(config['entry']),MK2KS_AUDIO_KILLER_ID=str(config['id']))")
 replace("'-nosamples'","'-samples'")
 replace("need(seen_guest==2 and seen_gfx==1 and len(raw_proofs)==4,'Whole driver plus audio guest and four native transitions')",
         "need(seen_guest==1 and seen_gfx==0 and len(raw_proofs)==0,'Whole actual native audio guest; no redundant scene transport')")
 first=code.index(" rows=[dict(fields(line),tag=line.split()[0])");last=code.index(' gate,fault,gate_sha=',first)
 code=code[:first]+" native=state(text,fighter,side,variant,guest)\n end=[native['terminal']]\n imported_channels=lifetime.inactive_channels(text,pcm_headers)\n"+code[last:]
 replace('nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,',
         'nativeDCSWaveformAccepted=True,samplesEnabled=True,importedVictimMixAccepted=False,allEnabledImportedSourcesInactive=True,importedChannelsObserved=imported_channels,variant=variant,nativeEarnedState=native,')
 scope=dict(original.run.__globals__,__file__=__file__,original=original,lifetime=lifetime,
            LUA=LUA,PARENT=PARENT,variant=variant,config=config,state=state,dac_models=dac_models)
 exec(compile(code,__file__+'::whole6213_current_stock_finisher','exec'),scope)
 return scope['run'](fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--variant',choices=CONFIG,required=True);args=parser.parse_args()
 try:run(args.fighter,args.side,args.variant)
 except Exception as error:
  folder=ROOT/f'audit_v6223_current_{args.variant}_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():original.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
