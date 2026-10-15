"""Whole failed diagnosis successor: A9 is the post-read stream address.

Keep the first checker/source/error frozen, every corrupting record, and the
unresolved-caller limitation. No new game run or speculative source patch.
"""
import inspect
import json
from pathlib import Path
import diagnose_native_sonya_shang_cache_failure as previous

ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_native_sonya_shang_cache_failure_postread_diagnosed'


def run():
    failure_path=previous.OUT/'failure.json'
    failure=json.loads(failure_path.read_text())
    need(not failure['passed'] and not failure['diagnosisCompleted'] and
         failure['error']=="ValueError('Original true18 index lands in a composite list; subsequent animation token would be raw bitmap descriptor')",
         'First failed post-read-address assertion retained without relabeling')
    body=inspect.getsource(previous.run)
    def once(before,after):
        nonlocal body
        need(body.count(before)==1,'One complete original diagnostic boundary');body=body.replace(before,after,1)
    once("struct.unpack_from('<I',rom,offset(0xff9d7b70))[0]==0xffbf18b0",
         "struct.unpack_from('<I',rom,offset(0xff9d7b50))[0]==0xffbf1840 and\n         struct.unpack_from('<I',rom,offset(0xff9d7b70))[0]==0")
    once('Original true18 index lands in a composite list; subsequent animation token would be raw bitmap descriptor',
         'Original true18 index lands in a composite list; first animation read would consume raw descriptor and advance A9 by32')
    once('its next raw descriptor at FF9D7B70 agrees with the actual overrun A9',
         'its first raw descriptor FFBF1840 at FF9D7B50 would advance A9 by32 to the actual overrun FF9D7B70')
    once('runtimeRootCauseResolved=False,',
         'runtimeRootCauseResolved=False,firstFailedDiagnosisPreserved=True,actualA9InterpretedAsPostRead=True,')
    once("Path(capture.__file__),stock,disasm,capture.OUT/'run.log.gz'):",
         "Path(capture.__file__),Path(previous_file),failure_path,stock,disasm,capture.OUT/'run.log.gz'):")
    scope=dict(vars(previous),__file__=__file__,OUT=OUT,previous_file=previous.__file__,failure_path=failure_path)
    exec(compile(body,__file__+'::whole_original_postread_address_diagnosis','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
