"""Same entire6520 gate; normalize integer dictionary keys at JSON boundary.

The first gate successfully rechecked native gameplay then rejected comparing
Python integer slot keys with serialized JSON string keys. Preserve that source;
no native replay or changed gameplay criterion, chronology or fault suite.
"""
import inspect,json
from pathlib import Path
import verify_repaired_challenger_root_cause_v6520 as prior

def main():
 source=inspect.getsource(prior.main)
 before="need(good==r['actualCurrentChallenger'],'Original entire gameplay gate agrees')"
 after="need(json.loads(json.dumps(good))==r['actualCurrentChallenger'],'Original entire gameplay gate agrees after exact JSON-key serialization')"
 prior.need(source.count(before)==1,'Only JSON key representation, full unchanged semantic gate')
 source=source.replace(before,after,1)
 before="pins={str(Path(__file__).resolve()):sha(__file__)};cases=[];faults=[]"
 after="pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__)};cases=[];faults=[]"
 prior.need(source.count(before)==1,'Pin preserved preceding executed qualifier source')
 source=source.replace(before,after,1)
 before="report=dict(passed=True,candidate=candidate.NAME"
 after="report=dict(passed=True,preservedQualifierBoundaryFailure=dict(source=str(Path(prior.__file__).resolve()),error=\"ValueError('Original entire gameplay gate agrees')\",cause='Integer Python slot keys versus JSON string slot keys; no native gameplay rejection or replay'),candidate=candidate.NAME"
 prior.need(source.count(before)==1,'Disclose preserved actual qualification boundary failure')
 source=source.replace(before,after,1)
 scope=dict(prior.__dict__,prior=prior,__file__=__file__,OUT=prior.ROOT/'audit_v6525_repaired_challenger_serialized_checked')
 exec(compile(source,__file__+'::whole_original_gate_json_representation','exec'),scope);scope['main']()

if __name__=='__main__':main()
