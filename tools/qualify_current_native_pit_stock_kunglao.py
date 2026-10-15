"""Actual stock victim earned Pit scene; caps never treated as completed scenes."""
import inspect
import json
import qualify_current_native_pit_case as base
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_native_pit_stock_kunglao_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
complete=terminal['exitCode']==0 and terminal['limitReason'] is None
assert complete or (terminal['exitCode']!=0 and terminal['limitReason']=='wall_limit')
assert terminal['elapsedSeconds']<92 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_pit_stock_kunglao_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
code=inspect.getsource(base.gate)
assert code.count('17,18')==1 and code.count("row['victim_id']=='18'")==1
code=code.replace('17,18','17,0').replace("row['victim_id']=='18'","row['victim_id']=='0'")
context={};exec(compile(code,__file__+'::stock victim earned Pit gate','exec'),context)
proof=context['gate'](base.load(folder/'run.log'))
report=dict(passedObservationChecks=True,completedRun=complete,
            currentStockVictimPitSceneAccepted=complete and proof.get('completeSceneFollowthrough',False),
            performer=17,side=1,victim=0,scene=proof,
            logSHA256=sync.sha(folder/'run.log'),visualAudioAccepted=False,
            allStockVictimsAccepted=False,fullPortAccepted=False)
out=sync.ROOT/'audit_current_native_pit_stock_kunglao_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
