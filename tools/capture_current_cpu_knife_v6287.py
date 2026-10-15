"""Normalize historical Windows source-pin keys; retain the prelaunch failure.

Entire previous collector, RAM comparison and unchanged semantic gate retained.
No emulator ran in the failed attempt; this is the first actual cold boot.
"""
import inspect,json
from pathlib import Path
import capture_current_cpu_knife_v6285 as prior
ROOT,need,sha=prior.ROOT,prior.need,prior.sha


def capture():
 failure=ROOT/'audit_v6286_current_native_cpu_knife_ram/failure.json'
 need(json.loads(failure.read_text())['nativeBoots']==0,'Preserve the original unstarted path-key failure')
 source=inspect.getsource(prior.capture)
 before="prior=json.loads(prior_path.read_text())"
 after="prior=json.loads(prior_path.read_text());prior['inputHashes']={str(Path(k).resolve()):v for k,v in prior['inputHashes'].items()}"
 need(source.count(before)==1,'Only normalize legacy equivalent Windows source-pin keys');source=source.replace(before,after,1)
 before='for p in (LUA,Path(__file__).resolve(),'
 need(source.count(before)==1,'Retain original executed collector and prelaunch failure pins')
 source=source.replace(before,'for p in (failure,Path(prior_module.__file__).resolve(),LUA,Path(__file__).resolve(),',1)
 namespace=dict(prior.capture.__globals__,__file__=__file__,failure=failure,prior_module=prior,
                FOLDER=ROOT/'audit_v6288_current_native_cpu_knife_ram')
 exec(compile(source,__file__+'::whole_original_collector_normalized_legacy_pin_keys','exec'),namespace)
 return namespace['capture']()


if __name__=='__main__':capture()
