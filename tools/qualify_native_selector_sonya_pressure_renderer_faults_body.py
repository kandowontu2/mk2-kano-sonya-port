"""Original complete fault suite, first actually classified body DMA context.

Preserve the real opening-frame StopIteration. Snapshot1818 displays the
pre-live1817 pass, without a classified slot2 body command. Use the first
actual command from the same full inventory, never force or invent a draw.
"""
import inspect
import json
from pathlib import Path
from types import FunctionType
import qualify_native_selector_sonya_pressure_renderer_faults as original

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_selector_sonya_pressure_renderer_faults_body_checked'
FAILURE=original.OUT/'failure.json'
need(json.loads(FAILURE.read_text())['error']=='StopIteration()',
     'Actual original opening snapshot lacks an already classified body DMA; failure immutable')
source=inspect.getsource(original.execute)


def once(before,after):
    global source
    need(source.count(before)==1,'One exact original full-suite actual-body-context boundary')
    source=source.replace(before,after,1)


once("    body=next(r for kind,r in reversed(events)if kind=='FLOOR_DMA'and r['slot']==2 and r['command']&15==2 and r['width']and r['height'])",
     "    body_frame,body=next((frame,r)for frame in sorted(CONTEXT['latches'])for kind,r in reversed(window(CONTEXT,frame))if kind=='FLOOR_DMA'and r['slot']==2 and r['command']&15==2 and r['width']and r['height'])\n"
     "    positive[body_frame]=one_pass(folder,CONTEXT,body_frame,display)")
once("reject(label,f,lambda:one_pass(folder,CONTEXT,f,display,{body['event']:mutated}))",
     "reject(label,body_frame,lambda:one_pass(folder,CONTEXT,body_frame,display,{body['event']:mutated}))")
once("Path(__file__),parent.OUT,previous.OUT/'report.json',Path(previous.__file__)",
     "Path(__file__),Path(original.__file__),FAILURE,parent.OUT,previous.OUT/'report.json',Path(previous.__file__)")
once('originalWhole1746PassPositiveRestored=True,',
     'originalWhole1746PassPositiveRestored=True,originalOpeningBodyContextFailurePreserved=True,'
     "actualClassifiedBodyFaultFrame=body_frame,actualClassifiedBodyCommand=dict(body),")
scope=dict(vars(original),OUT=OUT,__file__=__file__,original=original,FAILURE=FAILURE)
exec(compile(source,__file__+'::whole_original_suite_first_real_classified_body','exec'),scope)
execute=scope['execute']
safe_execute=FunctionType(original.safe_execute.__code__,dict(scope,execute=execute),
                          original.safe_execute.__name__,original.safe_execute.__defaults__)
