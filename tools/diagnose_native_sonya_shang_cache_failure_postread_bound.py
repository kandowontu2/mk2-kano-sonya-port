"""Whole original diagnosis, with unique report boundary and post-read A9.

Both failed diagnostic attempts remain frozen. Full native corruption and
the missing actual caller witness remain explicit; no speculative fix.
"""
import inspect
import json
from pathlib import Path
import diagnose_native_sonya_shang_cache_failure as original
import diagnose_native_sonya_shang_cache_failure_postread as failed_successor

ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_native_sonya_shang_cache_failure_postread_bound_diagnosed'


def run():
    first_path=original.OUT/'failure.json';second_path=failed_successor.OUT/'failure.json'
    first,second=[json.loads(p.read_text()) for p in (first_path,second_path)]
    need(not first['passed'] and not second['passed'] and not first['diagnosisCompleted'] and
         not second['diagnosisCompleted'] and second['error']=="ValueError('One complete original diagnostic boundary')",
         'Both original checker/source failures retained')
    body=inspect.getsource(original.run)
    def once(before,after):
        nonlocal body
        need(body.count(before)==1,'One uniquely anchored complete original boundary');body=body.replace(before,after,1)
    once("struct.unpack_from('<I',rom,offset(0xff9d7b70))[0]==0xffbf18b0",
         "struct.unpack_from('<I',rom,offset(0xff9d7b50))[0]==0xffbf1840 and\n         struct.unpack_from('<I',rom,offset(0xff9d7b70))[0]==0")
    once('Original true18 index lands in a composite list; subsequent animation token would be raw bitmap descriptor',
         'Original true18 index lands in a composite list; first animation read would consume raw descriptor and advance A9 by32')
    once('its next raw descriptor at FF9D7B70 agrees with the actual overrun A9',
         'its first raw descriptor FFBF1840 at FF9D7B50 would advance A9 by32 to the actual overrun FF9D7B70')
    once('actualLookupCallerWitnessCaptured=False,runtimeRootCauseResolved=False,',
         'actualLookupCallerWitnessCaptured=False,runtimeRootCauseResolved=False,bothFailedDiagnosesPreserved=True,actualA9InterpretedAsPostRead=True,')
    once("Path(capture.__file__),stock,disasm,capture.OUT/'run.log.gz'):",
         "Path(capture.__file__),Path(original_file),Path(second_file),first_path,second_path,stock,disasm,capture.OUT/'run.log.gz'):")
    scope=dict(vars(original),__file__=__file__,OUT=OUT,original_file=original.__file__,
               second_file=failed_successor.__file__,first_path=first_path,second_path=second_path)
    exec(compile(body,__file__+'::whole_original_postread_uniquely_bound_diagnosis','exec'),scope)
    return scope['run']()


if __name__=='__main__':run()
