"""Whole original exact-target compressor, this finite ball audio evidence."""
import inspect
import compact_current_cpu_compound_audio_v6448 as prior
ROOT=prior.ROOT
OUT=ROOT/'audit_v6464_current_cpu_ball_audio_storage'


def main():
 source=inspect.getsource(prior.main)
 changes={
  'audit_v6447_current_cpu_compound_audio_checked/report.json':'audit_v6462_current_cpu_ball_audio_checked/report.json',
  "dirs=('audit_v6445_current_cpu_compound_audio_ram','audit_v6447_current_cpu_compound_audio_checked')":
  "dirs=('audit_v6460_current_cpu_ball_audio_ram','audit_v6462_current_cpu_ball_audio_checked')",
  'mk2ks_current_cpu_compound_audio_v6442.lua':'mk2ks_current_cpu_ball_audio_v6458.lua',
  "('capture_current_cpu_compound_audio_v6443.py','current_cpu_compound_audio_model_v6444.py',\n                                   'finish_current_cpu_compound_audio_v6446.py',Path(__file__).name)":
  "('capture_current_cpu_ball_audio_v6459.py','finish_current_cpu_ball_audio_v6461.py',Path(__file__).name)",
 }
 for a,b in changes.items():
  prior.need(source.count(a)==1,'Only exact finite evidence targets change '+a)
  source=source.replace(a,b,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT)
 exec(compile(source,__file__+'::whole_exact_compressor_ball_audio_targets','exec'),scope)
 return scope['main']()


if __name__=='__main__':main()
