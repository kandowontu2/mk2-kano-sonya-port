"""Whole current Sonya P2 semantics and all actual physical replays retained.

Only Kitana physical replay dispatch changes to the genuinely fault-qualified
Ring policy. Full campaign/boss/ending/attract acceptance remains mandatory.
"""
import inspect,json,traceback
import verify_current_sonya_p2_campaign_v5630 as previous
import run_verified_kitana_sonya_p2_campaign_v5642 as capture
import verify_sonya_p2_kitana_ring_probe_v5639 as ring
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5645_verified_kitana_sonya_p2_campaign_checked'

def whole_run():
 scope=dict(vars(previous),__file__=__file__,capture=capture,OUT=OUT,ring=ring)
 exec(compile(inspect.getsource(previous.matched),__file__+'::whole_current_provenance','exec'),scope)
 source=inspect.getsource(previous.whole_run)
 changes=[('range_replay=original.slot.sonya.spacing.replay','range_replay=ring.make_replay()'),
  ('kitana=SimpleNamespace(make_replay=p2_factory(kitana.make_replay,kitana))',
   'kitana=SimpleNamespace(make_replay=ring.make_replay)')]
 for before,after in changes:
  need(source.count(before)==1,'Single full semantic replay dispatch change '+before)
  source=source.replace(before,after,1)
 exec(compile(source,__file__+'::entire_current_P2_native_and_physical_gate','exec'),scope)
 report=scope['whole_run']()
 report['kitanaNowUsesFaultQualifiedPhysicalRingSpacing']=True
 report['actualKitanaRangeFields']=report['actualFullRingSpacingInputReplay']['actualFieldsByNativeStage'].get(2,0)
 need(report['actualKitanaRangeFields']>0,'Complete actual per-field Kitana Ring replay required')
 return report

if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal; never restart live job')
 need(not OUT.exists(),'Fresh immutable full campaign verdict')
 try:report=whole_run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
