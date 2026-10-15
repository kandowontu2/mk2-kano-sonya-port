"""Full actual current enabled Friendship mix; preserve native terminal first.

Keep the complete6213 RAM transport/DAC/ROM gates. Only the actual physical
controller, scene scope and source mix model differ. --hold retains RAM after
a model failure for source-derived requalification without a native rerun.
"""
import argparse,code,inspect,json,traceback
from pathlib import Path
import capture_current_subzero_audio_v6213 as prior
import current_friendship_mix_model_v6254 as mix
import qualify_current_friendship_scenes_v6249 as visual
ROOT,need,sha=prior.ROOT,prior.need,prior.sha
LUA='mk2ks_current_friendship_audio_v6253.lua'
PARENT=ROOT/'audit_v6252_current_friendship_scene_progress/progress.json'
CAPTURE_SCOPE=None

def state(text,fighter,side,guest):
 parser=visual.capture.original.audio.audio.scene.previous.parse
 rows=parser(visual.TextPath(text))
 leaf='audit_v6246'if(fighter,side)==('kano',1)else'audit_v6248'
 reference=ROOT/f'{leaf}_current_{fighter}_friendship_scene_p{side}/run.log.gz'
 with prior.gzip.open(reference,'rt')as log:expected=parser(visual.TextPath(log.read()))
 need(rows==expected,'Every current qualified true-ID physical/health/choreography/winner/cleanup event unchanged')
 control=visual.capture.original.audio.audio.scene.check(rows,fighter,side)
 chronology=visual.capture.original.audio.audio.native.runtime(rows,fighter,side,'positive')
 return dict(control,nativeCueChronology=chronology,nativeStateRows=len(rows),sourceQualifiedCurrentScene=str(reference))

def dac_models(callbacks):
 source=inspect.getsource(prior.dac_models)
 need(source.count('1600<callbacks<2100')==1,'Only actual complete Friendship-action duration adapted')
 source=source.replace('1600<callbacks<2100','1300<callbacks<1500',1)
 scope=dict(prior.dac_models.__globals__)
 exec(compile(source,__file__+'::whole_original_DAC_Friendship_scope','exec'),scope)
 return scope['dac_models'](callbacks)

def run(fighter,side):
 global CAPTURE_SCOPE
 source=inspect.getsource(prior.run)
 def replace(before,after):
  nonlocal source
  need(source.count(before)==1,'One full prior collector adaptation '+before[:80])
  source=source.replace(before,after,1)
 replace('audit_v6214_current_subzero_{fighter}_p{side}_native_audio','audit_v6256_current_{fighter}_friendship_audio_p{side}')
 replace('gfx=current.expected_gfx()',"gfx=b''")
 first=source.index(' files=[ROOT/leaf for leaf in (LUA,');last=source.index(' controller=',first)
 source=source[:first]+" files=[ROOT/leaf for leaf in (LUA,'mk2ks_current_friendship_scene_v6244.lua','mk2ks_current_friendship_stream_probe_v3566.lua','mk2ks_current_friendship_stream_audio_v3567.lua','mk2ks_current_friendship_stream_wins_v3568.lua','mk2ks_current_tomb_winner_mix_observer_v5779.lua')]\n"+source[last:]
 replace('Path(__file__),Path(current.__file__),Path(model.__file__),',
         'Path(__file__),Path(prior.__file__),Path(mix.__file__),Path(mix.original.__file__),Path(visual.__file__),Path(current.__file__),Path(model.__file__),')
 replace("env.update(MK2KS_TEST_FIGHTER=fighter,MK2KS_CAMPAIGN_SIDE=str(side),MK2KS_STOCK_KILLER='subzero',\n            MK2KS_STOCK_COMMAND='ffd_hk',MK2KS_STOCK_GAP='168')",
         "env.update(MK2KS_FRIEND_WINNER=fighter,MK2KS_FRIEND_SIDE=str(side),MK2KS_FRIEND_CASE='positive',MK2KS_FRIEND_GAP='160',MK2KS_FRIEND_OBSERVATION='1600')")
 replace("'-nosamples'","'-samples'")
 replace("'-str','130'","'-str','180'")
 replace("('MK2_MAUDIO_GUEST','MK2_EARNED_SUBZERO_GUEST')","('MK2_MAUDIO_GUEST','MK2_CURRENT_FRIEND_GUEST')")
 replace("need(seen_guest==2 and seen_gfx==1 and len(raw_proofs)==4,'Whole driver plus audio guest and four native transitions')",
         "need(seen_guest==2 and seen_gfx==0 and len(raw_proofs)==0,'Whole current physical/audio guest; no redundant RGB transport')")
 first=source.index(" rows=[dict(fields(line),tag=line.split()[0])");last=source.index(' gate,fault,gate_sha=',first)
 source=source[:first]+" native=state(text,fighter,side,guest)\n end=[native]\n"+source[last:]
 replace('waveform=model.predict_waveform(dac_chunks,dac_headers,pcm)',
         "globals()['LAST_CAPTURE']=dict(locals())\n waveform=mix.predict_mix(dac_chunks,dac_headers,pcm,text,fighter,pins)")
 replace('nativeNextCPUMatch=end[0]','nativeFriendshipScene=end[0]')
 replace('nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,',
         'nativeDCSWaveformAccepted=True,samplesEnabled=True,importedFriendshipMixAccepted=True,')
 replace("('passed','fighter','physicalSlot','comparedStereoFrames','nativeDCSWaveformAccepted','samplesEnabled','fullPortAcceptance')",
         "('passed','fighter','physicalSlot','comparedStereoFrames','importedFriendshipMixAccepted','samplesEnabled','fullPortAcceptance')")
 CAPTURE_SCOPE=dict(prior.run.__globals__,__file__=__file__,prior=prior,mix=mix,visual=visual,
                    LUA=LUA,PARENT=PARENT,state=state,dac_models=dac_models)
 exec(compile(source,__file__+'::whole6213_current_complete_Friendship_mix','exec'),CAPTURE_SCOPE)
 return CAPTURE_SCOPE['run'](fighter,side)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);parser.add_argument('--hold',action='store_true');args=parser.parse_args()
 try:run(args.fighter,args.side)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  folder=ROOT/f'audit_v6256_current_{args.fighter}_friendship_audio_p{args.side}'
  if folder.exists():prior.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True)
  if args.hold and CAPTURE_SCOPE and 'LAST_CAPTURE'in CAPTURE_SCOPE:
   code.interact(banner='Native terminal; actual PCM/DAC buffers retained in capture. No native rerun.',
                 local=dict(capture=CAPTURE_SCOPE['LAST_CAPTURE'],module=__import__(__name__),prior=prior,mix=mix))
  raise SystemExit(1)
