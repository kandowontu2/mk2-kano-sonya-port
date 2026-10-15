"""Earned native stock-victim Pit, sample lifetime and bounded reviewed images."""
import inspect
import json
import qualify_current_native_pit_case as base
import verify_native_source_sync as sync
sync.verify()
folder=sync.ROOT/'audit_current_native_pit_stock_jax_sonya_p2_runtime'
terminal=json.loads((folder/'terminal.json').read_text())
assert terminal['exitCode']==0 and terminal['limitReason'] is None
assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_pit_stock_jax_sonya_p2_preparation/stage.lua')
assert not (folder/'stderr.log').read_text().strip()
rows=base.load(folder/'run.log')
code=inspect.getsource(base.gate)
for old,new in {"r['side']=='1'":"r['side']=='2'","r['winner']=='kano'":"r['winner']=='sonya'",'17,18':'18,11',"action['id']=='17'":"action['id']=='18'","row['id']=='17'":"row['id']=='18'","row['victim_id']=='18'":"row['victim_id']=='11'"}.items():
    assert old in code;code=code.replace(old,new)
context={};exec(compile(code,__file__+'::stock Jax Pit gate','exec'),context)
proof=context['gate'](rows);assert proof['completeSceneFollowthrough']
channels=rows['AUDIO_CHANNEL'];assert [int(r['age']) for r in channels]==list(range(801))
assert all(r['loop']==r['paused']==r['mute']=='0' for r in channels)
cue=[r for r in rows['AUDIO_WORD'] if r['word']=='FFFD']
assert len(cue)==1 and cue[0]['pc']=='FFFB7140' and cue[0]['mute']=='0'
active=[r for r in channels if r['sample']=='3'];assert active
ages=[int(r['age']) for r in active]
assert ages==list(range(ages[0],ages[-1]+1)) and ages[0]==int(cue[0]['age'])
pos=[float(r['pos']) for r in active]
assert all(r['length']=='32000' for r in active) and pos==sorted(pos) and pos[0]<320 and pos[-1]<32000 and pos[-1]-pos[0]>30000
done=channels[ages[-1]+1];assert done['sample']=='4294967295' and float(done['pos'])>=32000
images=sorted(folder.rglob('*.png'));assert len(images)==2
assert {p.name for p in images}=={'stock_pit_15.png','stock_pit_120.png'}
size=sum(p.stat().st_size for p in images);assert size<=120*1024
assert [r['age'] for r in rows['VISUAL_SAVED']]==['15','120']
report=dict(passedNativeStockVictimPit=True,performer=18,side=2,victim=11,scene=proof,
            winnerCue=cue[0],sampleCompletionAge=int(done['age']),
            reviewedImages=[dict(path=str(p),SHA256=sync.sha(p)) for p in images],imageBytes=size,
            finiteImagesReviewed=True,heardAudioMixAccepted=False,allStockVictimsAccepted=False,
            logSHA256=sync.sha(folder/'run.log'),fullPortAccepted=False)
out=sync.ROOT/'audit_current_native_pit_stock_jax_sonya_p2_checked'
assert not out.exists();out.mkdir()
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v for k,v in report.items() if k not in ('reviewedImages',)},indent=2))
