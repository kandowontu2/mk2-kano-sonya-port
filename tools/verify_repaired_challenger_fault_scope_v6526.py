"""Entire root-cause gate; JSON keys and actual pre-purge input fault scope.

Preserve prior executed qualifier sources. A previous negative test modified a
post-join Block pulse although this root-cause comparison ends before purge;
change only that negative fixture to an actual pre-purge Coin pulse. No native
replay or narrower positive criterion. All full-route gameplay faults remain.
"""
import inspect,json
from pathlib import Path
import verify_repaired_challenger_root_cause_v6520 as prior
import verify_repaired_challenger_serialized_v6524 as serialized

def main():
 source=inspect.getsource(prior.main)
 changes={
  "need(good==r['actualCurrentChallenger'],'Original entire gameplay gate agrees')":
  "need(json.loads(json.dumps(good))==r['actualCurrentChallenger'],'Original entire gameplay gate agrees after exact JSON-key serialization')",
  "('changed input','button=Block','button=Start')":"('changed pre-purge input','button=Coin','button=Start')",
  "pins={str(Path(__file__).resolve()):sha(__file__)};cases=[];faults=[]":
  "pins={str(Path(__file__).resolve()):sha(__file__),str(Path(prior.__file__).resolve()):sha(prior.__file__),str(Path(serialized.__file__).resolve()):sha(serialized.__file__)};cases=[];faults=[]",
  "report=dict(passed=True,candidate=candidate.NAME":
  "report=dict(passed=True,preservedQualifierFailures=[dict(source=str(Path(prior.__file__).resolve()),error=\"ValueError('Original entire gameplay gate agrees')\",cause='Integer Python slot keys versus JSON string slot keys'),dict(source=str(Path(serialized.__file__).resolve()),error='ValueError: False root-cause evidence admitted changed input',cause='Negative fixture changed post-join Block pulse outside pre-purge comparison scope; now changes actual pre-purge Coin pulse')],candidate=candidate.NAME",
 }
 for a,b in changes.items():prior.need(source.count(a)==1,'Exact qualification-boundary/fault-fixture correction '+a);source=source.replace(a,b,1)
 scope=dict(prior.__dict__,prior=prior,serialized=serialized,__file__=__file__,OUT=prior.ROOT/'audit_v6527_repaired_challenger_fault_scope_checked')
 exec(compile(source,__file__+'::whole_original_gate_actual_pre_purge_fault','exec'),scope);scope['main']()

if __name__=='__main__':main()
