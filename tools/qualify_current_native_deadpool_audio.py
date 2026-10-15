"""Earned acid winner cue/channel completion; no assertion of heard mix quality."""
import json
import qualify_current_native_deadpool_roles as acid
import verify_native_source_sync as sync
sync.verify()
out=sync.ROOT/'audit_current_native_deadpool_audio_checked'
assert not out.exists()
cases=[]
for fighter,side,cue,sample in [('kano',1,'FFFE',2),('sonya',2,'FFFD',3)]:
 folder=sync.ROOT/f'audit_current_native_deadpool_audio_{fighter}_p{side}_runtime'
 records=acid.rows(folder/'run.log')
 case=acid.check(records,fighter,side)
 baseline=sync.ROOT/f'audit_current_native_deadpool_gate_hold_{fighter}_p{side}_runtime/run.log'
 assert [r for r in records if r[0] not in ('AUDIO_WORD','AUDIO_CHANNEL')]==acid.rows(baseline)
 terminal=json.loads((folder/'terminal.json').read_text())
 assert terminal['exitCode']==0 and terminal['limitReason'] is None
 cues=[r for tag,r in records if tag=='AUDIO_WORD' and r['pc']=='FFFB7140']
 assert len(cues)==1 and cues[0]['word']==cue and cues[0]['mute']=='0'
 channels=[r for tag,r in records if tag=='AUDIO_CHANNEL']
 assert [int(r['age']) for r in channels]==list(range(801))
 start=int(cues[0]['age'])
 playing=[r for r in channels if int(r['age'])>=start and int(r['sample'])==sample]
 assert len(playing)>90 and all(int(r['length'])==32000 and r['loop']=='0' and r['paused']=='0' and r['mute']=='0' for r in playing)
 positions=[float(r['pos']) for r in playing]
 assert all(b>a for a,b in zip(positions,positions[1:]))
 last=int(playing[-1]['age'])
 complete=[r for r in channels if int(r['age'])>last]
 assert complete and all(int(r['sample']) in (-1,4294967295) and float(r['pos'])>=32000 for r in complete)
 case.update(cue=cue,sample=sample,startAge=start,completionAge=last+1,
             scalarBaselineExact=True,logSHA256=sync.sha(folder/'run.log'))
 cases.append(case)
out.mkdir()
(out/'report.json').write_text(json.dumps({'passed':True,'cases':cases,
 'heardMixQualityVerified':False,'allAcidSoundEffectsVerified':False,'fullPortAccepted':False},indent=2))
print('PASS both earned acid winner cues and actual non-looped playback completion')
