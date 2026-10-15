"""Exact native forward/return identity phase; retain both checker failures."""
import inspect,json,traceback
from pathlib import Path
import current_morph_publication_semantics_v5421 as original
import current_morph_publication_semantics_v5423 as transport

OUT=original.ROOT/'audit_v5426_current_morph_publication_progress'
FAILED=transport.OUT/'progress.json'

def run():
 failure=json.loads(FAILED.read_text())
 original.need(not failure['passed']and failure['error']=="ValueError('Declared morph component exists only on its actual current own Shang transition pose')",
  'Preserve exact attempted all-Shang-ID assumption failure')
 original.HEX.update({'p1','p2','main1','main2'})
 source=inspect.getsource(original.check)
 before="s==side and a['id']==6 and a['pose']==source_groups[a['source']]and a['pose']in groups[side]"
 after="s==side and a['id']in(6,17 if groups[side][0]==assets.address(assets.GROUPS)else 18)and by[f,s]['roster']==6 and a['pose']==source_groups[a['source']]and a['pose']in groups[side]"
 original.need(source.count(before)==1,'Only incorrect always-ID6 transition assumption changes; all actual pre-state/source/owner/FIFO gates retained')
 ns=dict(original.check.__globals__);exec(compile(source.replace(before,after,1),__file__+'::native_forward_and_return_ID_phase','exec'),ns)
 original.check=ns['check']
 # Qualify actual forward/reverse ID stores and full human lifecycle again;
 # reverse holds legitimately keep the target ID until the original return
 # store. A target ID alone never permits an unowned/wrong/current stale pose.
 for target in('kano','sonya'):
  for side in(1,2):
   path=original.ROOT/'audit_v5404_current_morph_adversity_ram'/f'{target}_p{side}_repeat_morph_added'/'run.log'
   physical=original.physical.verify_log(path.read_text(),target,side,'repeat_morph','added')
   original.need(physical['passed']and physical['originalNativeIDStores']==6 and physical['summary']['completeRepeatedCycles']==3,
    'All real native 512-field target-ID and 12-field return stores independently requalified')
 report=original.run()
 report.update(preservedActualCheckerFailures=[str(transport.FAILED),str(FAILED)],
  checkerCorrectionsOnly=['Four FLOOR_STATE pointers decode native hexadecimal addresses.',
   'Original forward groups retain Shang ID6; original reverse groups retain actual target ID17/18 until genuine native return store. Every ID/roster/actor/pose still must equal independent actual pre-task state, every component must be exact current descriptor, and all dispatch gates unchanged.'],
  actualEntireOriginalPhysicalLifecycleRequalified=True)
 for p in(transport.FAILED,FAILED,Path(transport.__file__),Path(__file__).resolve()):report['newInputHashes'][str(p.resolve())]=original.sha(p)
 return report

if __name__=='__main__':
 original.need(not OUT.exists(),'Fresh current native forward/return semantic checkpoint')
 try:report=run()
 except Exception as error:report=dict(passed=False,error=repr(error),traceback=traceback.format_exc(),goalStatus='active',fullPortAcceptance=False)
 OUT.mkdir();(OUT/'progress.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items()if k not in('cases','newInputHashes','remaining','actualRecordFaultsRejected')},indent=2),flush=True)
 raise SystemExit(0 if report['passed']else 1)
