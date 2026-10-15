"""Keep full6370 proof; derive preceding selection EOF with original arithmetic."""
import argparse,inspect,json,subprocess,traceback,wave
from pathlib import Path
import numpy as np
import verify_current_cpu_blade_knife_audio_v6370 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6373_current_cpu_blade_knife_audio_checked'


def channel_gate(text,waveform,headers):
 path=ROOT/'samples/mk2ks/kano_select.wav'
 with wave.open(str(path),'rb')as clip:
  need((clip.getnchannels(),clip.getsampwidth(),clip.getframerate(),clip.getnframes())==(1,2,16000,18400),
       'Whole original selection source format, not a guessed EOF constant')
  values=np.frombuffer(clip.readframes(clip.getnframes()),dtype='<i2').copy()
 _,positions=original.model.sample_values(values,16000)
 source=inspect.getsource(original.old.channel_gate)
 before='return 0xffffffff,32000,endpoint'
 need(source.count(before)==1,'Only preceding source changes, entire winner clock preserved')
 source=source.replace(before,'return 0xffffffff,18400,selection_endpoint',1)
 scope=dict(original.old.channel_gate.__globals__,selection_endpoint=positions[-1])
 exec(compile(source,__file__+'::whole_original_channel_gate_exact_prior_selection_double_accumulation','exec'),scope)
 return scope['channel_gate'](original.old.inventory(text),headers,dict(waveform=waveform),'kano')


def main(preflight=False):
 source=inspect.getsource(original.main)
 before="waveform['actualMixedRawPCMByteFaultsRejected']"
 need(source.count(before)==1,'Use actual existing source-model raw-fault field name')
 source=source.replace(before,"waveform['actualRawMixedPCMFaultsRejected']",1)
 before='Path(__file__),Path(old.__file__)'
 need(source.count(before)==1,'Pin both preserved executed host checkers')
 source=source.replace(before,'Path(__file__),Path(original.__file__),Path(old.__file__)',1)
 scope=dict(original.__dict__,OUT=OUT,__file__=__file__,original=original,channel_gate=channel_gate)
 exec(compile(source,__file__+'::whole6370_exact_prior_clip_clock_and_fault_field','exec'),scope)
 return scope['main'](preflight)


if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
 try:main(args.preflight)
 except Exception as error:
  failure=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if not args.preflight:OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(failure,indent=2)+'\n')
  print(json.dumps(failure,indent=2),flush=True);raise SystemExit(1)
