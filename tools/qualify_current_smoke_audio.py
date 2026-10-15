"""Finite post-secret own name playback/EOF, not heard mix or all impact audio."""
import ast
import copy
import json
import re
import wave
import verify_native_source_sync as sync
sync.verify()
tree=ast.parse((sync.ROOT/'tools/qualify_current_sonya_natural_smoke.py').read_text())
defs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='load']
exec(compile(ast.Module(body=defs,type_ignores=[]),__file__+'::records','exec'))
out=sync.ROOT/'audit_current_smoke_audio_checked';assert not out.exists()
cases=[]
def gate(rows,fighter,length):
    marker='FFFC' if fighter=='kano' else 'FFFB'
    sample='0' if fighter=='kano' else '1'
    cues=[r for r in rows['SMOKE_AUDIO_WORD'] if r['word']==marker]
    assert len(cues)==1
    cue=cues[0];begin=int(cue['frame']);arrival=int(rows['SECRET_RETURN'][0]['frame'])
    assert cue['pc']=='FFFF3DA0' and cue['mode']=='13' and cue['arena']=='8' and cue['mute']=='0'
    channels=[r for r in rows['SMOKE_AUDIO_CHANNEL'] if r['channel']=='0' and int(r['frame'])>=begin]
    active=[r for r in channels if r['sample']==sample and int(r['length'])==length]
    assert len(active)>=4 and all(r['loop']=='0' and r['paused']=='0' for r in active)
    positions=[float(r['pos']) for r in active]
    assert all(0<=v<length for v in positions) and all(a<b for a,b in zip(positions,positions[1:]))
    eof=next(r for r in channels if int(r['frame'])>begin and float(r['pos'])==length and r['sample']=='4294967295')
    assert int(eof['frame'])<arrival
    assert all(float(r['pos'])==length and r['sample']=='4294967295' for r in channels if int(r['frame'])>=int(eof['frame']))
    at_return=[r for r in rows['SMOKE_AUDIO_CHANNEL'] if int(r['frame'])==arrival]
    assert {int(r['channel']) for r in at_return}==set(range(19))
    assert all(r['sample']=='4294967295' and float(r['pos'])>=int(r['length']) for r in at_return)
    return dict(cue=cue,activePositionReads=len(active),actualEOF=eof,all19ChannelsInactiveAtReturn=True)
for fighter,baseline in [('kano','audit_current_kano_smoke_64_cadence'),('sonya','audit_current_sonya_smoke_transition_batched')]:
    folder=sync.ROOT/('audit_current_smoke_audio_'+fighter+'_runtime')
    terminal=json.loads((folder/'terminal.json').read_text(encoding='utf-8-sig'))
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/('audit_current_smoke_audio_preparation/'+fighter+'.lua'))
    assert not (folder/'stderr.log').read_text().strip()
    prior=json.loads((sync.ROOT/(baseline+'_checked')/'report.json').read_text())
    assert prior['normalTwoHumanReturnAccepted']
    old=load(sync.ROOT/(baseline+'_runtime')/'run.log');rows=load(folder/'run.log')
    assert {t:g for t,g in rows.items() if not t.startswith('SMOKE_AUDIO_')}==old
    path=sync.ROOT/('samples/mk2ks/'+fighter+'_select.wav')
    with wave.open(str(path),'rb') as wav:length=wav.getnframes();rate=wav.getframerate()
    proof=gate(rows,fighter,length)
    bad=copy.deepcopy(rows)
    next(r for r in bad['SMOKE_AUDIO_CHANNEL'] if r['frame']==proof['actualEOF']['frame'] and r['channel']=='0')['pos']='0.0'
    try:gate(bad,fighter,length)
    except AssertionError:pass
    else:raise AssertionError('Unfinished voice accepted')
    cases.append(dict(fighter=fighter,proof=proof,actualGameplayUnchanged=True,
        unfinishedVoiceFaultRejected=True,samplePath=str(path),sampleSHA256=sync.sha(path),sampleFrames=length,sampleRate=rate,
        terminal=terminal,logSHA256=sync.sha(folder/'run.log')))
out.mkdir()
(out/'report.json').write_text(json.dumps(dict(passedFinitePostSecretNamePlayback=True,cases=cases,
    heardMixAccepted=False,allSecretImpactAudioAccepted=False,activeBattleVoiceCutProven=False,fullPortAccepted=False),indent=2))
print(json.dumps(dict(passed=True,characters=2,scope='actual name playback/EOF and quiet channels at normal return only')))
