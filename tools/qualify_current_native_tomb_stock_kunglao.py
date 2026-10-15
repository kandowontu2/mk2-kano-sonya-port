"""Native stock-victim scene with same earned admission/true-performer gate."""
import inspect
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync

sync.verify()
folder=sync.ROOT/'audit_current_native_tomb_stock_kunglao_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_tomb_stock_kunglao_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=base.load(folder/'run.log')
code=inspect.getsource(base.gate)
assert code.count('17,18')==2 and code.count("row['victim_id']=='18'")==1
code=code.replace('17,18','17,0').replace("row['victim_id']=='18'","row['victim_id']=='0'")
context={};exec(compile(code,__file__+'::stock victim gate','exec'),context)
result=context['gate'](rows)
report=dict(passedNativeStockVictimTomb=True,performer=17,victim=0,scene=result,
            logSHA256=sync.sha(folder/'run.log'),stockVictimPixelsAccepted=False,
            allStockVictimsAccepted=False,fullPortAccepted=False)
out=sync.ROOT/'audit_current_native_tomb_stock_kunglao_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
