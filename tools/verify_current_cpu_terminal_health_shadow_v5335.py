"""Complete native health ledger with the original source-bound pre-execution exit boundary."""
import argparse,inspect,json,traceback
from pathlib import Path
import verify_current_cpu_choke_health_shadow_v5333 as original
ROOT,need,sha=original.ROOT,original.need,original.sha

def bindings():
 source=inspect.getsource(original.whole_health)
 before=" assert set(posts)=={(f,s)for f in range(first,last+1)for s in(1,2)},'Both complete draw-time physical slots'"
 after=""" terminals=p.rows(log,'RESULT')
 assert len(terminals)==1 and terminals[0]['frame']==last and terminals[0]['follow_regain']>0,'Actual original terminal CPU callback'
 terminal=terminals[0]
 assert last==max(terminal['complete'],terminal['follow_regain'])+30,'Exact original exit instruction deadline'
 source=(ROOT/'mk2ks_cpu_recovery_probe_v1438.lua').read_text()
 assert "local deadline=follow_regain and math.max(complete,follow_regain)+30 or complete+180"in source and "if frame>=deadline then manager.machine:exit()end"in source,'Unchanged actual source exits inside pre-execution frame callback'
 assert set(posts)=={(f,s)for f in range(first,last)for s in(1,2)},'Both complete draw-time slots through last actually completed native field'
 phase=[s for s in log.splitlines()if s.startswith('MK2_HPHASE_RESULT ')]
 assert len(phase)==1 and int(prior.re.search(r'frame=(\\d+)',phase[0])[1])==last,'Actual observer terminal shares exact native exit callback'
 assert not any(r['frame']==last for r in stores),'No guest health execution attributed to unexecuted exit callback'
 terminal_pre=by[last]
 assert terminal_pre['mode']==2 and (terminal_pre['state'],terminal_pre['vstate'])==(0,1),'Actual final pre-execution CPU/human ownership'
"""
 need(source.count(before)==1,'Exact post/terminal boundary substitution');source=source.replace(before,after,1)
 before=' for frame in range(first,last+1):';need(source.count(before)==1,'Exact all actually completed field range')
 source=source.replace(before,' for frame in range(first,last):',1)
 before='everyOrdinaryPairedAndPostRecoveryHealthStoreReplayed=True,'
 after='everyOrdinaryPairedAndPostRecoveryHealthStoreReplayed=True,renderedLast=last-1,unexecutedTerminalPreCallbacks=1,sourceBoundOriginalExitBoundary=True,'
 need(source.count(before)==1,'Explicit actual terminal boundary metadata');source=source.replace(before,after,1)
 namespace=dict(original.whole_health.__globals__)
 exec(compile(source,__file__+'::entire_original_complete_health_replay_exact_native_terminal','exec'),namespace)
 health=namespace['whole_health']
 namespace=dict(original.verify_log.__globals__,whole_health=health)
 exec(compile(inspect.getsource(original.verify_log),__file__+'::entire_original_phase_plus_complete_health','exec'),namespace)
 verify=namespace['verify_log']
 namespace=dict(original.run.__globals__,verify_log=verify,__file__=__file__)
 exec(compile(inspect.getsource(original.run),__file__+'::entire_full_cpu_body_shadow_and_real_faults','exec'),namespace)
 return namespace['run']

def run(human):
 path=ROOT/'audit_v5334_current_cpu_kano_health_shadow_human_kano_checked/report.json'
 failure=json.loads(path.read_text())
 need(not failure['passed']and failure['error']=="AssertionError('Both complete draw-time physical slots')",'Preserve actual unqualified terminal boundary checker failure')
 report=bindings()(human)
 report.update(sourceBoundOriginalPreExecutionExitQualified=True,missingNativeDrawsInvented=False,
  preservedExecutedTerminalBoundaryFailure=str(path),
  terminalBoundary='Exactly one original exit pre-callback follows the final completed draw and native health execution. It must match actual native/observer result and unchanged1438 deadline; no stores or fabricated post/draw allowed there.')
 for p in(Path(original.__file__),path):report['inputHashes'][str(p.resolve())]=sha(p)
 return report

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--human',choices=('kano','sonya'),required=True);a=parser.parse_args()
 out=ROOT/f'audit_v5336_current_cpu_kano_terminal_health_shadow_human_{a.human}_checked';need(not out.exists(),'Fresh immutable source-qualified proof')
 try:report=run(a.human)
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),fullPortAcceptance=False)
 out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('inputHashes','actualSemanticFaultsRejected','actualPhysicalFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
