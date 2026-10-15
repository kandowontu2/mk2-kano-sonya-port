"""Whole earned native Pit scene, explicit SonyaP1/stock Kitana identities."""
import inspect,json
import qualify_current_native_pit_case as base
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_stock_pit_sonya_serial_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_stock_pit_other_sides_preparation/sonya_p1_kitana.lua')
assert not (folder/'stderr.log').read_text().strip()
code=inspect.getsource(base.gate)
for old,new in (("r['winner']=='kano'","r['winner']=='sonya'"),('17,18','18,4'),("action['id']=='17'","action['id']=='18'"),("row['id']=='17'","row['id']=='18'"),("row['victim_id']=='18'","row['victim_id']=='4'")):
    assert old in code;code=code.replace(old,new)
context={};exec(compile(code,__file__,'exec'),context)
proof=context['gate'](base.load(folder/'run.log'))
assert proof['nativePitActivated'] and proof['completeSceneFollowthrough']
report=dict(passed=True,performer=18,side=1,victim=4,scene=proof,
 logSHA256=sync.sha(folder/'run.log'),visualAudioAccepted=False,fullPortAccepted=False)
out=sync.ROOT/'audit_current_stock_pit_sonya_serial_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
