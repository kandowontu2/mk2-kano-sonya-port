"""Whole exact-target compressor for current Bicycle and preserved missing-tap run."""
import inspect
import compact_current_cpu_ball_render_v6456 as prior
ROOT=prior.ROOT
OUT=ROOT/'audit_v6475_current_cpu_bicycle_render_storage'


def main():
 source=inspect.getsource(prior.main)
 changes={
  'audit_v6455_current_cpu_ball_render_checked/report.json':'audit_v6473_current_cpu_bicycle_render_checked/report.json',
  "('audit_v6453_current_cpu_ball_render_ram','audit_v6455_current_cpu_ball_render_checked')":
  "('audit_v6467_current_cpu_bicycle_render_ram','audit_v6472_current_cpu_bicycle_bound_ram','audit_v6473_current_cpu_bicycle_render_checked')",
  "files.append(ROOT/'mk2ks_current_cpu_ball_render_v6450.lua')":
  "files.extend(ROOT/n for n in('mk2ks_current_cpu_bicycle_render_ram_v6465.lua','mk2ks_current_cpu_bicycle_render_bound_v6470.lua'))",
  "('current_cpu_ball_context_v6451.py','capture_current_cpu_ball_render_v6452.py',\n                                   'verify_current_cpu_ball_render_v6454.py',Path(__file__).name)":
  "('capture_current_cpu_bicycle_render_v6466.py','verify_current_cpu_bicycle_render_v6468.py','capture_current_cpu_bicycle_bound_v6471.py',Path(__file__).name)",
 }
 for a,b in changes.items():
  prior.need(source.count(a)==1,'Only exact current finite evidence targets differ '+a)
  source=source.replace(a,b,1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT)
 exec(compile(source,__file__+'::whole_exact_compressor_current_Bicycle_evidence','exec'),scope)
 return scope['main']()


if __name__=='__main__':main()
