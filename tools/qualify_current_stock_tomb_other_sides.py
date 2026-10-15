"""Whole native earned admission and continuous scene records in both roles."""
import inspect
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
cases=[]
for name,side,fighter,own,victim in (('sonya_p1_kitana',1,'sonya',18,4),('kano_p2_subzero',2,'kano',17,8)):
    folder=sync.ROOT/('audit_current_stock_tomb_'+name+'_runtime')
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_stock_tomb_other_sides_preparation/'+name+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    code=inspect.getsource(base.gate)
    changes={"r['side']=='1'":f"r['side']=='{side}'","r['winner']=='kano'":f"r['winner']=='{fighter}'",'17,18':f'{own},{victim}',"action['id']=='17'":f"action['id']=='{own}'","row['id']=='17'":f"row['id']=='{own}'","row['victim_id']=='18'":f"row['victim_id']=='{victim}'"}
    for old,new in changes.items():assert old in code;code=code.replace(old,new)
    context={};exec(compile(code,__file__+'::'+name,'exec'),context)
    proof=context['gate'](base.load(folder/'run.log'))
    cases.append(dict(case=name,performer=own,side=side,victim=victim,scene=proof,logSHA256=sync.sha(folder/'run.log')))
out=sync.ROOT/'audit_current_stock_tomb_other_sides_checked'
assert not out.exists();out.mkdir()
report=dict(passedFiniteStockTombRoles=True,cases=cases,visualAudioAccepted=False,allStockVictimsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
