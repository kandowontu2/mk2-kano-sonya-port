"""Actual winner sample lifetime, not heard DCS mix or universal priority proof."""
import json
import qualify_current_native_tomb_case as base
import verify_native_source_sync as sync
sync.verify()
proofs=[]
for case,sample,word in (('kunglao','2','FFFE'),('jax_sonya_p2','3','FFFD')):
    folder=sync.ROOT/('audit_current_stock_tomb_audio_'+case+'_runtime')
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_stock_tomb_audio_preparation/'+case+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=base.load(folder/'run.log')
    old=base.load(sync.ROOT/('audit_current_native_tomb_stock_'+case+'_runtime/run.log'))
    for tag in set(rows)|set(old):
        if tag in ('AUDIO_WORD','AUDIO_CHANNEL'):continue
        assert rows.get(tag,[])==old.get(tag,[])
    cues=[r for r in rows['AUDIO_WORD'] if r['word']==word]
    assert len(cues)==1 and cues[0]['mute']=='0'
    channels=rows['AUDIO_CHANNEL']
    assert [int(r['age']) for r in channels]==list(range(801))
    assert all(r['loop']==r['paused']==r['mute']=='0' for r in channels)
    active=[r for r in channels if r['sample']==sample]
    assert active and all(r['length']=='32000' for r in active)
    ages=[int(r['age']) for r in active]
    assert ages==list(range(ages[0],ages[-1]+1))
    assert 0<=ages[0]-int(cues[0]['age'])<=1
    positions=[float(r['pos']) for r in active]
    assert positions==sorted(positions) and positions[0]<320 and positions[-1]<32000
    assert positions[-1]-positions[0]>30000
    done=channels[ages[-1]+1]
    assert done['sample']=='4294967295' and float(done['pos'])>=32000
    proofs.append(dict(case=case,winnerCue=cues[0],sample=int(sample),activeFields=len(active),
                       completionAge=int(done['age']),logSHA256=sync.sha(folder/'run.log')))
out=sync.ROOT/'audit_current_stock_tomb_audio_checked'
assert not out.exists();out.mkdir()
report=dict(passedWinnerCueLifetime=True,cases=proofs,unchangedEarnedControllers=True,
            heardMixAccepted=False,stockVictimDCSVoiceAccepted=False,
            allSoundPriorityContextsAccepted=False,fullPortAccepted=False)
(out/'report.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
