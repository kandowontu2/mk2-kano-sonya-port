"""Actual native bio name-cue dispatch and bounded channel completion."""
import json,re,wave
import verify_native_source_sync as sync
import qualify_bounded_current_attract_bios as bios

def main():
    source_sync=sync.verify()
    out=sync.ROOT/'audit_bounded_current_bio_cues_checked';assert not out.exists()
    folder=sync.ROOT/'audit_bounded_current_bio_cues_runtime'
    terminal=json.loads((folder/'terminal.json').read_text())
    lua=sync.ROOT/'audit_bounded_current_bio_cues_preparation/attract.lua'
    assert terminal['exitCode']==0 and terminal['limitReason'] is None and terminal['observerSha256']==sync.sha(lua)
    assert terminal['peakWorkingSetBytes']<=320*1024*1024 and terminal['elapsedSeconds']<=90 and terminal['logBytes']<=10*1024*1024
    assert not (folder/'stderr.log').read_text().strip() and not any(p.suffix.lower() in ('.png','.bin','.wav') for p in folder.rglob('*'))
    text=(folder/'run.log').read_text();assert 'LUA ERROR' not in text
    lines=[l for l in text.splitlines() if l.startswith('MK2_LIGHT_ATTRACT_')]
    rows=[(l.split()[0].removeprefix('MK2_LIGHT_ATTRACT_'),dict(re.findall(r'(\w+)=([^\s]+)',l))) for l in lines]
    bio_proof=bios.gate(rows)
    cues=[r for t,r in rows if t=='NAME_CUE' and r['pc']=='FFFB77C0']
    assert len(cues)==2 and [r['word'] for r in cues]==['FFFC','FFFB']
    packet=[r for t,r in rows if t=='NAME_CUE' and r['pc'] in ('FFA13C90','FFA13D60')]
    assert len(packet)==1 and packet[0]['counter']=='11'
    results={}
    for r,ident,name in zip(cues,(17,18),('kano','sonya')):
        assert r['counter']==str(ident) and r['mode']=='1' and r['mute']=='0'
        start=int(r['frame']);assert bio_proof[str(ident)]['frame']<start<bio_proof[str(ident)]['frame']+60
        wave_path=sync.ROOT/f'samples/mk2ks/{name}_select.wav'
        with wave.open(str(wave_path),'rb') as clip:length=clip.getnframes()
        trace=[x for t,x in rows if t=='VOICE_CHANNEL' and start<int(x['frame'])<=start+120]
        assert [int(x['frame']) for x in trace]==list(range(start+1,start+121))
        assert all(int(x['length'])==length and x['loop']==x['paused']=='0' for x in trace)
        positions=[float(x['pos']) for x in trace]
        assert positions==sorted(positions) and 0<=positions[0]<length and positions[-1]>=length
        end=next(i for i,p in enumerate(positions) if p>=length)
        assert end<100 and all(p==positions[end] for p in positions[end:])
        assert all(x['sample']=='4294967295' for x in trace[end:])
        results[name]=dict(nativeCue=r['word'],frame=start,fullObservedChannelFields=120,
            clipFrames=length,completionAge=end+1,waveSHA256=sync.sha(wave_path),nonLoopingCompletion=True)
    report=dict(passed=True,sourceSync=source_sync,terminal=terminal,bios=bio_proof,nameCues=results,
        nativePacketMarkerExcluded=True,logSHA256=sync.sha(folder/'run.log'),
        firstColdSourceNumNotUsedAsPlaybackFlag=True,
        heardAudioQualityAccepted=False,fullPortAcceptance=False,
        scope='Natural Kano/Sonya bio name markers under native sound-enabled gate, actual channel0 non-looping clip-length/position advancement and completion through120fields. Stock source_num may stay-1 on first start because it tests previous source_len before assignment; advancing position establishes playback activity. No PCM capture, heard quality or muted-branch/priority/all audio acceptance.')
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,nativeBioNameCuesCompleted=2,heardAudioQualityAccepted=False)))

if __name__=='__main__':main()
