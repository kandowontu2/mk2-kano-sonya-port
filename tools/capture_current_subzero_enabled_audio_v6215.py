"""Same complete6213 audio test with the real release samples option enabled.

The stock Sub-Zero wins this earned-victim sequence. Verify every imported
channel inactive, rather than presume a disabled-sample test covers release.
"""
import argparse,inspect,json,traceback
from pathlib import Path
import capture_current_subzero_audio_v6213 as original
ROOT,need,sha=original.ROOT,original.need,original.sha

def adapted_run():
 code=inspect.getsource(original.run)
 def replace(before,after):
  nonlocal code
  need(code.count(before)==1,'One complete original collector adaptation')
  code=code.replace(before,after,1)
 replace('audit_v6214_current_subzero_','audit_v6216_current_subzero_')
 replace("'-nosamples'","'-samples'")
 replace("Path(__file__),Path(current.__file__),Path(model.__file__),",
         "Path(__file__),Path(original.__file__),Path(current.__file__),Path(model.__file__),")
 replace(" waveform=model.predict_waveform(dac_chunks,dac_headers,pcm)",
 """ channels=[fields(line)for line in text.splitlines()if line.startswith('MK2_TOMB_MIX_CHANNEL ')]
 need(len(channels)==14*len(pcm_headers),'All14 real enabled imported channels at every sound callback')
 for index,header in enumerate(pcm_headers):
  group=channels[index*14:(index+1)*14]
  need([r['channel']for r in group]==[str(n)for n in range(14)]and
       all(r['index']==str(index+1)and r['frame']==header['frame']and r['seconds']==header['seconds']and
           r['length']=='0'and r['loop']=='0'and r['paused']=='0'and r['writes']=='0'and r['assistance']=='none'for r in group),
       'Actual enabled imported sources inactive throughout native Sub-Zero winner sequence')
 waveform=model.predict_waveform(dac_chunks,dac_headers,pcm)""")
 replace('nativeDCSWaveformAccepted=True,samplesEnabled=False,importedVictimMixAccepted=False,',
         'nativeDCSWaveformAccepted=True,samplesEnabled=True,importedChannelsObserved=len(channels),allEnabledImportedSourcesInactive=True,importedVictimMixAccepted=False,')
 scope=dict(original.run.__globals__,original=original,__file__=__file__)
 exec(compile(code,__file__+'::whole6213_release_samples_enabled','exec'),scope)
 return scope['run']

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--fighter',choices=('kano','sonya'),required=True)
 parser.add_argument('--side',type=int,choices=(1,2),required=True);args=parser.parse_args()
 try:adapted_run()(args.fighter,args.side)
 except Exception as error:
  folder=ROOT/f'audit_v6216_current_subzero_{args.fighter}_p{args.side}_native_audio'
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if folder.exists():original.save(folder/'failure.json',failure)
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
