"""Whole qualified native DAC/resampler/ROM model for earned Tomb windows.

Only the old 685-callback duration is replaced by the independently checked
complete actual Tomb window. No waveform fitting, gain changes or trimming.
"""
import inspect
import current_ending_audio_model_v5733 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
predict_waveform=original.predict_waveform
expected_region=original.expected_region
rom_models=original.rom_models


def dac_models(callbacks):
 need(isinstance(callbacks,int)and 800<callbacks<1200,'Full original1100field earned Tomb window')
 code=inspect.getsource(original.original_dac.dac_gate)
 before='len(chunks)==len(headers)==len(pcm_headers)==685'
 need(code.count(before)==1,'Only exact whole DAC callback duration adapter')
 code=code.replace(before,'len(chunks)==len(headers)==len(pcm_headers)==callbacks',1)
 scope=dict(vars(original.original_dac),__file__=__file__,callbacks=callbacks)
 exec(compile(code,__file__+'::entire_original_DAC_Tomb_window','exec'),scope)
 exec(compile(inspect.getsource(original.original_dac.dac_faults),__file__+'::entire_actual_DAC_faults','exec'),scope)
 need(scope['dac_faults'].__globals__['dac_gate']is scope['dac_gate'],'Actual faults bind full-window gate')
 return scope['dac_gate'],scope['dac_faults']
