"""Repair5695's Python line continuation; preserve its failed original source.

No native verifier/result/acceptance gate or game/controller byte changes.
"""
import json
from pathlib import Path
import run_verified_subzero_sonya_p2_campaign_v5688 as capture
ROOT,need,sha=capture.ROOT,capture.need,capture.sha
original_path=ROOT/'tools/record_sonya_p2_campaign_clear_progress_v5695.py'


def run():
 source=original_path.read_text()
 try:compile(source,str(original_path),'exec')
 except SyntaxError as error:
  need(error.lineno==56 and 'invalid syntax'in str(error),'Exact original unparenthesized Python line-continuation error')
  observed_error=repr(error)
 else:raise ValueError('Original actual recorder failure source must remain unchanged')
 before="native=job['ProcessId']==m['pid']and job['Name']=='mkport_candidate.exe'and\n   0<=job['createdUnix']-m['startedUnix']<30 and m['command'][-1]in job['CommandLine']"
 after="native=(job['ProcessId']==m['pid']and job['Name']=='mkport_candidate.exe'and\n   0<=job['createdUnix']-m['startedUnix']<30 and m['command'][-1]in job['CommandLine'])"
 changes=[(before,after),
  ("OUT=ROOT/'audit_v5696_sonya_p2_campaign_clear_progress'","OUT=ROOT/'audit_v5700_sonya_p2_campaign_clear_bound_progress'"),
  ("m['hostSource']in job['CommandLine']","Path(m['hostSource']).name in job['CommandLine']"),
  (']+[Path(__file__).resolve()]',']+[Path(__file__).resolve(),original_path]'),
  ('consumedWholeVerifierToolSession=21571,',
   'consumedWholeVerifierToolSession=21571,progressRecorderRepair=dict(originalSource=str(original_path),originalSHA256=sha(original_path),observedOriginalSyntaxError=observed_error,nativeEngineFailure=False,allNativeAcceptanceGatesUnchanged=True),')]
 for before,after in changes:
  need(source.count(before)==1,'One whole additive-recorder syntax/provenance repair '+before)
  source=source.replace(before,after,1)
 scope=dict(__name__='record_sonya_p2_campaign_clear_bound',__file__=__file__,
  original_path=original_path,observed_error=observed_error)
 exec(compile(source,__file__+'::whole_additive_recorder_with_valid_line_continuation','exec'),scope)
 return scope['run']()


if __name__=='__main__':run()
