"""Diagnostic only: locate a failed native cull predicate, no render acceptance."""
import json,re,traceback
from pathlib import Path
from collections import defaultdict
import verify_native_kintaro_launch_cull_v1692 as boss
ROOT=boss.ROOT;OUT=ROOT/'audit_v1697_native_counter_cull_predicate_diagnostic'
if __name__=='__main__':
 assert not OUT.exists()
 guest,_,payload=boss.arena.corrected_source.expected();folder=ROOT/'audit_v1664_current_kano_p1_native_counter'
 context=boss.build_context(folder,guest,payload)
 diagnostic=json.loads((ROOT/'audit_v1661_current_kano_p1_visibility_diagnostic/report.json').read_text())
 records=diagnostic['visibilityFailures'];frames={r['frame']-1 for r in records}|set(range(42376,42381))|set(range(45152,45157))
 groups=defaultdict(list);hex_fields=boss.arena.native.raster.HEX|{'first_source','row'}
 str_fields=boss.arena.native.raster.STR
 with (folder/'run.log').open(encoding='utf-8-sig')as stream:
  for line in stream:
   m=re.match(r'^MK2_NAT_CAMPAIGN_(FLOOR_QUEUE|FLOOR_QUEUE_DISPATCH|SHADOW_COMPONENT) ',line)
   if not m:continue
   r=dict(re.findall(r'(\w+)=([^\s]+)',line))
   if int(r['frame'])not in frames:continue
   for key,v in tuple(r.items()):
    if key not in str_fields:r[key]=int(v,16 if key in hex_fields else 10)
   groups[m[1]].append(r)
 results=[]
 for raw in records:
  record={**raw,'body':{1:raw['body']}}
  try:result=dict(passed=True,proof=boss.prove(context,groups,record,1,17,guest,payload))
  except Exception as e:result=dict(passed=False,frame=record['frame'],error=repr(e),traceback=traceback.format_exc())
  results.append(result)
 OUT.mkdir();report=dict(diagnosticCompleted=True,results=results,fullPortAcceptance=False,renderAccepted=False)
 (OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
