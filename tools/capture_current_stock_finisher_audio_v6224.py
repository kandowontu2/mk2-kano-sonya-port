"""6222 successor: source-bound exact Kitana entry/controller and stop phase.

Initial6223 capture was native-terminal but its observation origin was wrong;
preserve it. No guest/game edits or restarts after an observation timeout.
"""
import argparse,inspect,json,struct,traceback
from pathlib import Path
import capture_current_stock_finisher_audio_v6222 as prior
import verify_kitana_inflation_earned_state_v3933 as kitana
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
CONFIG={k:dict(v)for k,v in prior.CONFIG.items()}
CONFIG['kitana']['entry']=0xff8cc650
LUA='mk2ks_current_stock_finisher_audio_v6225.lua'

def state(text,fighter,side,variant,guest):
 if variant!='kitana':return prior.state(text,fighter,side,variant,guest)
 folder=ROOT/f'audit_v6114_current_kitana_{fighter}_p{side}_native_scene_ram'
 rows=lambda value:[s.strip()for s in value.splitlines()if s.startswith('MK2_STOCK_HEAD_V921_')]
 actual=rows(text);expected=rows((folder/'run.log').read_text())
 need(actual==expected,'Every original921 native input/health/history/parameter/gore/continuation row equals qualified current Kitana scene')
 proof=kitana.gate(kitana.rows(text),fighter,side,guest)
 return dict(proof,nativeStateRows=len(actual),sourceQualifiedCurrentScene=str(folder/'run.log'),
             terminal=next(prior.original.fields(s)for s in actual if s.startswith('MK2_STOCK_HEAD_V921_RESULT ')))

def run(fighter,side,variant):
 config=CONFIG[variant];guest=prior.original.current.expected()
 entries=[struct.unpack_from('<I',guest,(table-0xff800000)//8+config['id']*4)[0]for table in (0xff8ba210,0xff8ba390)]
 need(config['entry']in entries,'Correct actual source-native action table entry before boot')
 observer=ROOT/('mk2ks_inflation_native_scene_ram_v3919.lua'if variant=='kitana'else
               'mk2ks_split_native_scene_ram_v3965.lua'if variant=='kung_lao'else
               'mk2ks_jax_clap_native_scene_ram_v4019.lua'if variant=='jax_clap'else
               'mk2ks_jax_arms_native_scene_ram_v4073.lua')
 need('local action_entry=0x'+format(config['entry'],'x')in observer.read_text(),'Exact entry agrees with whole current scene observer')
 code=inspect.getsource(prior.run)
 def replace(before,after):
  nonlocal code
  need(code.count(before)==1,'One complete prior observer/collector correction')
  code=code.replace(before,after,1)
 replace('audit_v6223_current_','audit_v6226_current_')
 replace("files=[ROOT/leaf for leaf in (LUA,'mk2ks_stock_extended_earned_ram_v3958.lua','mk2ks_stock_fatality_v1021.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')]",
 "files=[ROOT/leaf for leaf in (LUA,'mk2ks_current_stock_finisher_audio_v6221.lua','mk2ks_stock_extended_earned_ram_v3958.lua','mk2ks_stock_fatality_v1021.lua','mk2ks_stock_earned_ram_v3918.lua','mk2ks_stock_head_victim_v921.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')]")
 replace('Path(original.__file__),Path(lifetime.__file__),Path(current.__file__),Path(model.__file__),',
         'Path(original.__file__),Path(prior.__file__),Path(kitana.__file__),observer,Path(lifetime.__file__),Path(current.__file__),Path(model.__file__),')
 replace('LUA=LUA,PARENT=PARENT,variant=variant,config=config,state=state,dac_models=dac_models)',
         'LUA=LUA,PARENT=PARENT,variant=variant,config=config,state=state,dac_models=dac_models,prior=prior,kitana=kitana,observer=observer)')
 namespace=dict(vars(prior),__file__=__file__,prior=prior,kitana=kitana,observer=observer,
                CONFIG=CONFIG,LUA=LUA,state=state)
 exec(compile(code,__file__+'::whole6222_source_bound_stock_audio','exec'),namespace)
 return namespace['run'](fighter,side,variant)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--variant',choices=CONFIG,required=True);args=parser.parse_args()
 try:run(args.fighter,args.side,args.variant)
 except Exception as error:
  folder=ROOT/f'audit_v6226_current_{args.variant}_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():prior.original.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
