"""Entire original native DAC/clock/ROM models, for full ending windows.

The old685-callback Baraka duration is replaced only by the exact observed
window's independently checked50Hz callback count. Native normalization,
ring, channel, gain, resampler, attosecond/cache and real fault gates remain.
"""
import inspect
import current_native_dac_capture_v5593 as original_dac
import current_native_dac_clock_v5596 as original_clock
import current_dcs_rom_source_capture_v5586 as original_rom

ROOT,need,sha=original_dac.ROOT,original_dac.need,original_dac.sha
predict_waveform=original_clock.predict_waveform
expected_region=original_rom.expected_region


def dac_models(expected_callbacks):
 need(isinstance(expected_callbacks,int)and expected_callbacks>2000,
  'Actual full native ending/attract audio window, not the old short finisher duration')
 gate_source=inspect.getsource(original_dac.dac_gate)
 before='len(chunks)==len(headers)==len(pcm_headers)==685'
 need(gate_source.count(before)==1,'Only whole-window callback duration adapter')
 gate_source=gate_source.replace(before,'len(chunks)==len(headers)==len(pcm_headers)==expected_callbacks',1)
 scope=dict(vars(original_dac),__file__=__file__,expected_callbacks=expected_callbacks)
 exec(compile(gate_source,__file__+'::whole_original_DAC_all_native_callbacks','exec'),scope)
 exec(compile(inspect.getsource(original_dac.dac_faults),__file__+'::all_actual_DAC_faults','exec'),scope)
 need(scope['dac_faults'].__globals__['dac_gate']is scope['dac_gate'],
  'Entire actual fault suite bound to full-window gate, no old685 globals')
 return scope['dac_gate'],scope['dac_faults']


def rom_models(expected):
 need(isinstance(expected,bytes)and len(expected)==0xc00000,'Entire independent original sound firmware/data region')
 scope=dict(vars(original_rom),__file__=__file__,EXPECTED=expected)
 for function in (original_rom.region_gate,original_rom.region_faults):
  exec(compile(inspect.getsource(function),__file__+'::whole_original_ROM_RAM_byte_gate','exec'),scope)
 need(scope['region_faults'].__globals__['region_gate']is scope['region_gate']and
  scope['region_gate'].__globals__['EXPECTED']is expected,
  'Actual source reference bound in every complete gate and genuine byte-fault defining namespace')
 return scope['region_gate'],scope['region_faults']
