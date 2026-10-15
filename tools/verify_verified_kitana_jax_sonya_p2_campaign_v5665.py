"""Retain entire native campaign gate and verified per-field Ring contexts4/11."""
import inspect,json,traceback
import verify_verified_kitana_sonya_p2_campaign_v5644 as previous
import verify_sonya_p2_jax_ring_probe_v5660 as ring
import run_verified_kitana_jax_sonya_p2_campaign_v5663 as capture
ROOT,need,sha=previous.ROOT,previous.need,previous.sha
OUT=ROOT/'audit_v5666_verified_kitana_jax_sonya_p2_campaign_checked'

def whole_run():
 source=inspect.getsource(previous.whole_run)
 before=' for before,after in changes:'
 need(source.count(before)==1,'One whole physical-replay dispatch list')
 addition=" changes.append(('jax=SimpleNamespace(make_replay=p2_factory(jax.make_replay,jax))','jax=SimpleNamespace(make_replay=ring.make_replay)'))\n"
 source=source.replace(before,addition+before,1)
 scope=dict(vars(previous),__file__=__file__,capture=capture,OUT=OUT,ring=ring)
 exec(compile(source,__file__+'::entire_native_and_verified_Kitana_Jax_Ring_gate','exec'),scope)
 report=scope['whole_run']()
 report['jaxNowUsesFaultQualifiedPhysicalRingSpacing']=True
 report['actualJaxRangeFields']=report['actualFullRingSpacingInputReplay']['actualFieldsByNativeStage'].get(4,0)
 need(report['actualJaxRangeFields']>0,'Full actual Jax per-field Ring replay required')
 return report

if __name__=='__main__':
 need((capture.OUT/'result.json').is_file(),'Await actual terminal, never rerun live job')
 need(not OUT.exists(),'Fresh immutable full campaign verdict')
 try:report=whole_run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 OUT.mkdir();(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','case')},indent=2),flush=True)
 if report['passed']:print(json.dumps({k:v for k,v in report['case'].items()if k not in('inputHashes','uppercutAssignmentFrames')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
