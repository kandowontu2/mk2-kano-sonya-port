"""Use actual unchanged native single-frame projection, not multipart offsets.

Original FF804180 jumps past the multipart DX/DY subtraction at FF804290.
Keep full source/cache/palette/camera/flip/DMA and retirement-order gates;
retain6357's incorrect generic-projection rejection. Same641-field capture.
"""
import inspect,json
from pathlib import Path
import verify_current_cpu_effect_render_v6356 as prior
ROOT,need=prior.ROOT,prior.need
OUT=ROOT/'audit_v6359_current_cpu_effect_render_checked'


def source_gate():
 core=prior.prior
 source=inspect.getsource(core.gate)
 changes={
  "1871<=q['frame']<1909":"1872<=q['frame']<=1909",
  "q['frame']>=1909":"q['frame']>1909",
  "x-=e['dx'];y-=e['dy'];cmd=q['command']>>16":"if q['multipart']:x-=e['dx'];y-=e['dy']\n  cmd=q['command']>>16",
 }
 for before,after in changes.items():
  need(source.count(before)==(2 if before.startswith('1871')else 1),'Exact actual original branch/boundary source adaptation')
  source=source.replace(before,after)
 scope=dict(core.gate.__globals__)
 exec(compile(source,__file__+'::whole_original_scene_single_and_multipart_projection','exec'),scope)
 original_gate=scope['gate']
 def gate(g,records,guest,payload,seq,blade_sources):
  original=(ROOT/'mk2/mk2-maincpu.bin').read_bytes()
  lo,hi=((at-0xff800000)//8 for at in(0xff804000,0xff804420))
  need(guest[lo:hi]==original[lo:hi],'Whole original single/multipart native projection/publication code unchanged')
  return original_gate(g,records,guest,payload,seq,blade_sources)
 return gate


def main():
 failure=ROOT/'audit_v6357_current_cpu_effect_render_checked/failure.json'
 need(json.loads(failure.read_text())['error']=="ValueError('Native camera/origin/flip/descriptor projection, no offset substitute')",'Original incorrect multipart-only projection rejection retained')
 source=inspect.getsource(prior.main)
 before="\"for path in(ROOT/'tools/verify_current_cpu_effect_render_v6354.py',"
 need(source.count(before)==1,'Additional source/failed projection pins, no lost original gate')
 source=source.replace(before,"\"for path in(ROOT/'tools/verify_current_cpu_effect_render_v6356.py',ROOT/'audit_v6357_current_cpu_effect_render_checked/failure.json',ROOT/'tools/verify_native_blade_blood_cause_v2813.py',ROOT/'tools/verify_current_cpu_effect_render_v6354.py',",1)
 scope=dict(prior.__dict__,__file__=__file__,OUT=OUT,source_gate=source_gate)
 exec(compile(source,__file__+'::complete_source_projection_retirement_and_transport_gate','exec'),scope)
 scope['main']()


if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  OUT.mkdir(exist_ok=True);(OUT/'failure.json').write_text(json.dumps(dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False),indent=2)+'\n');raise
