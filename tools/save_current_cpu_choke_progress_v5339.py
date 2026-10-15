"""Same complete additive journal, using actual native transport schema key."""
import inspect,json,traceback
from pathlib import Path
import save_current_cpu_choke_progress_v5337 as original
ROOT,need,sha=original.ROOT,original.need,original.sha
OUT=ROOT/'audit_v5340_current_cpu_kano_choke_progress'
def run():
 source=inspect.getsource(original.run)
 before="meta['exit_code']==0"
 need(source.count(before)==1,'Single transport-schema spelling correction')
 source=source.replace(before,"meta['nativeExit']==0",1)
 namespace=dict(original.run.__globals__,__file__=__file__)
 exec(compile(source,__file__+'::complete_original_journal_actual_native_exit_key','exec'),namespace)
 report=namespace['run']()
 failed=original.OUT/'progress.json';failure=json.loads(failed.read_text())
 need(not failure['passed']and failure['error']=="KeyError('exit_code')",'Preserve executed metadata spelling failure')
 for p in(Path(original.__file__),failed):report['newInputHashes'][str(p.resolve())]=sha(p)
 report['preservedJournalSchemaFailure']=str(failed)
 return report
if __name__=='__main__':
 need(not OUT.exists(),'Fresh immutable journal')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active')
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items()if k not in('newInputHashes','captures','remaining')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
