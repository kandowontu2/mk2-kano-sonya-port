"""Retained mirror PCM: Square uses .70 route, not channel0's .30 volume.

Keep6400's complete native clocks and6396's entire DAC/float mixer and fault
suite. Only the independently compiled Square-channel gain is corrected.
"""
import inspect,json
from pathlib import Path
import finish_current_cpu_ring_mirror_audio_v6400 as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v6403_current_cpu_ring_mirror_audio_ram_checked'
FAILURE=ROOT/'audit_v6402_preserved_square_gain_failure'


def predict(*args):
 source=inspect.getsource(original.prior.predict)
 before='square_sample[at[valid]]*gain'
 need(source.count(before)==1,'Only channel12 source route changes; whole mixer retained')
 source=source.replace(before,'square_sample[at[valid]]*np.float32(.70)',1)
 scope=dict(original.prior.__dict__)
 exec(compile(source,__file__+'::whole_mixer_with_compiled_channel12_route','exec'),scope)
 return scope['predict'](*args)


def finish(carrier,failed_waveform):
 need(not FAILURE.exists() and not original.OUT.exists(),'Preserve actual failed6400 gain model once')
 need(not failed_waveform['passed'] and failed_waveform['differentChannelSamples']==84536,
      'Actual failed full mirror waveform retained, not a made-up counterexample')
 FAILURE.mkdir()
 original.prior.original.prior.original.save(FAILURE/'waveform.json',failed_waveform)
 original.prior.original.prior.original.save(FAILURE/'failure.json',dict(passed=False,
  error="ValueError('Entire actual full mirror mixed PCM, source-clocked initial Square plus Sonya winner, no trimming/fits')",
  executedChecker=str(Path(original.__file__).resolve()),checkerSHA256=sha(original.__file__),
  originalOutputWasNotCreated=True,noNativeRerun=True))
 source=inspect.getsource(original.finish)
 before=" need(not failure.exists(),'Preserve actual6398 failed video-state check once')\n prior.original.prior.original.save(failure,dict(passed=False,\n  error=\"ValueError('Every original Square video position through finite retained EOF')\",\n  executedChecker=str(Path(boundary.__file__).resolve()),checkerSHA256=sha(boundary.__file__),\n  nativeTerminal=terminal,originalOutputWasNotCreated=True,noNativeRerun=True))"
 after=" need(json.loads(failure.read_text())['error']==\"ValueError('Every original Square video position through finite retained EOF')\",'Original actual failed6398 evidence preserved unchanged')"
 need(source.count(before)==1,'Do not overwrite the executed owner-clock failure')
 source=source.replace(before,after,1)
 source=source.replace(" scope['OUT']=OUT"," scope['OUT']=OUT\n scope['predict']=correct_predict",1)
 source=source.replace("Path(boundary_checker),first_boundary_failure,owner_timer_failure):",
                       "Path(boundary_checker),first_boundary_failure,owner_timer_failure,Path(owner_checker),gain_failure,gain_waveform):",1)
 source=source.replace("              first_boundary_failure=", "              owner_checker=owner_checker,gain_failure=gain_failure,gain_waveform=gain_waveform,first_boundary_failure=",1)
 scope=dict(original.__dict__,OUT=OUT,__file__=__file__,correct_predict=predict,
            owner_checker=original.__file__,gain_failure=FAILURE/'failure.json',gain_waveform=FAILURE/'waveform.json')
 exec(compile(source,__file__+'::whole_terminal_RAM_qualification_correct_channel_gain','exec'),scope)
 return scope['finish'](carrier)
