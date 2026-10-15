"""Native Pit winner cue and channel playback/completion, not heard quality."""
import json
import verify_native_source_sync as sync
from qualify_current_native_pit_case import load,gate

def main():
    source=sync.verify();folder=sync.ROOT/'audit_current_native_pit_audio_kano_p1_runtime'
    out=sync.ROOT/'audit_current_native_pit_audio_kano_p1_checked';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text())
    assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert terminal['elapsedSeconds']<=90 and terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['logBytes']<=10*1024*1024
    assert terminal['observerSha256']==sync.sha(sync.ROOT/'audit_current_native_pit_audio_preparation/stage.lua')
    assert not (folder/'stderr.log').read_text().strip()
    assert not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    rows=load(folder/'run.log');proof=gate(rows);assert proof['completeSceneFollowthrough']
    prefix='MK2_STAGE_'
    actual=[l for l in (folder/'run.log').read_text().splitlines() if l.startswith(prefix) and not l.startswith(prefix+'AUDIO_')]
    expected=[l for l in (sync.ROOT/'audit_current_native_pit_longkick_kano_p1_runtime/run.log').read_text().splitlines() if l.startswith(prefix)]
    assert actual==expected
    words=rows['AUDIO_WORD'];cues=[r for r in words if r['pc'] not in ('FFA13C90','FFA13D60')]
    assert len(cues)==1 and cues[0]['word']=='FFFE' and cues[0]['pc']=='FFFB7140' and cues[0]['age']=='247'
    assert all(r['mute']=='0' for r in words)
    channels=rows['AUDIO_CHANNEL'];assert [int(r['age']) for r in channels]==list(range(801))
    assert all(r['loop']==r['paused']==r['mute']=='0' for r in channels)
    active=[r for r in channels if r['sample']=='2'];assert active
    assert int(active[0]['age'])==247 and all(r['length']=='32000' for r in active)
    ages=[int(r['age']) for r in active];assert ages==list(range(ages[0],ages[-1]+1))
    pos=[float(r['pos']) for r in active];assert pos==sorted(pos) and pos[0]<320 and pos[-1]<32000
    completed=channels[ages[-1]+1:]
    assert all(r['sample']=='4294967295' and float(r['pos'])>=32000 for r in completed)
    report=dict(passed=True,sourceSync=source,terminal=terminal,scene=proof,nativeWinnerCue=cues[0],
        actualWinnerPlaybackFields=len(active),winnerCompletionAge=ages[-1]+1,nativePacketWords=len(words)-1,
        completeScalarBaselineUnchanged=True,logSHA256=sync.sha(folder/'run.log'),heardAudioQualityAccepted=False,
        allStageSoundsAccepted=False,fullPortAcceptance=False,
        scope='Earned current KanoP1/SonyaP2 Pit: native unmuted FFFE winner cue, real sample2 advancing channel0 then nonlooping completion,801 continuous scalar audio fields. Other words remain native DCS packets, not proved audible. No PCM/heard mix/all sounds/priority/other roles acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,winnerCompletionAge=ages[-1]+1,heardAudioQualityAccepted=False)))

if __name__=='__main__':main()
