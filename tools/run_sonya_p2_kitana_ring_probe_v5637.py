"""Fresh bounded Kitana strategy comparison, not duplicate/restarted full campaign."""
import inspect,json,re,traceback
import run_current_sonya_p2_campaign_v5628 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v5638_sonya_p2_kitana_ring_probe'
LUA='mk2ks_sonya_p2_kitana_ring_probe_v5636.lua'
CONTROLLERS=[LUA,*original.CONTROLLERS]
native=original.native
qualify_payload_metadata_warning=original.qualify_payload_metadata_warning

def capture():
 original.source_boundary()
 source=original.capture_source()
 before="'-nothrottle','-str','18100'";after="'-nothrottle','-str','900'"
 need(source.count(before)==1,'Bounded900emulated-second diagnostic fallback, not long campaign restart')
 source=source.replace(before,after,1)
 text='\n'.join((ROOT/n).read_text()for n in CONTROLLERS)
 need(not re.search(r'write_u\d+|:write_|load_?state|\.value\s*=(?!=)|return\s+data',text),
  'All transitive physical strategy/read observers only, no guest assistance')
 scope=dict(vars(original.original),__file__=__file__,native=native,OUT=OUT,LUA=LUA,CONTROLLERS=CONTROLLERS,
  qualify_payload_metadata_warning=qualify_payload_metadata_warning)
 exec(compile(source,__file__+'::whole_current_host_bounded_probe','exec'),scope)
 return scope['capture']()

if __name__=='__main__':
 try:capture()
 except Exception as error:
  report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
  if OUT.exists():(OUT/'capture_failure.json').write_text(json.dumps(report,indent=2)+'\n')
  print(json.dumps(report,indent=2),flush=True);raise
