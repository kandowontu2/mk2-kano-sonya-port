"""Same whole earned-admission/continuous scene gate with explicit stock victim."""
import inspect
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_native_tomb_stock_jax_sonya_p2_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_tomb_stock_jax_sonya_p2_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=base.load(folder/'run.log')
code=inspect.getsource(base.gate)
replacements={"r['side']=='1'":"r['side']=='2'","r['winner']=='kano'":"r['winner']=='sonya'",'17,18':'18,11',"action['id']=='17'":"action['id']=='18'","row['id']=='17'":"row['id']=='18'","row['victim_id']=='18'":"row['victim_id']=='11'"}
for old,new in replacements.items():
    assert old in code;code=code.replace(old,new)
context={};exec(compile(code,__file__+'::stock Jax reciprocal gate','exec'),context)
result=context['gate'](rows)
report=dict(passedNativeStockVictimTomb=True,performer=18,side=2,victim=11,scene=result,
            logSHA256=sync.sha(folder/'run.log'),stockVictimPixelsAccepted=False,
            allStockVictimsAccepted=False,fullPortAccepted=False)
out=sync.ROOT/'audit_current_native_tomb_stock_jax_sonya_p2_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
