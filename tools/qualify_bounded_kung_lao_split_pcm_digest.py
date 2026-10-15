"""Paired full mixed PCM update SHA256/levels; never claim heard or byte retention."""
import copy,json,re
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync

def load(folder):
    baseline=[];pcm=[];masks=[];stops=[]
    with (folder/'run.log').open() as stream:
        for line in stream:
            assert '[LUA ERROR]' not in line
            if line.startswith(('MK2_STOCK_HEAD_V921_','MK2_VOICE_','MK2_FINISHER_AUDIO_')):baseline.append(line.strip())
            r=dict(re.findall(r'(\w+)=([^\s]+)',line))
            if line.startswith('MK2_SPLIT_PCM_DIGEST '):pcm.append(r)
            elif line.startswith('MK2_SPLIT_SAMPLE_MASK '):masks.append(r)
            elif line.startswith('MK2_SPLIT_PCM_STOP '):stops.append(r)
    return baseline,pcm,masks,stops

def gate(on,off,masks,stop,begin,end):
    assert on==off and len(on)>200 and len(stop)==1
    assert stop[0]['raw_media']=='none' and int(stop[0]['frame'])==end
    assert int(stop[0]['updates'])==len(on) and int(stop[0]['bytes'])==sum(int(r['bytes']) for r in on)
    assert int(on[0]['frame'])==begin and end-2<=int(on[-1]['frame'])<end
    assert all(Decimal(b['seconds'])-Decimal(a['seconds'])==Decimal('.02') for a,b in zip(on,on[1:]))
    assert all(r['writes']=='0' and r['assistance']=='none' and int(r['bytes'])>0 and int(r['bytes'])%4==0 and re.fullmatch('[0-9A-F]{64}',r['sha256']) for r in on)
    assert all(0<=int(r['nonzero'])<=int(r['bytes'])//2 and 0<=int(r['peak'])<=32768 and int(r['energy'])>=0 for r in on)
    assert sum(int(r['energy']) for r in on)>0 and max(int(r['peak']) for r in on)>0
    for rows in masks:
        assert {int(r['age']) for r in rows}==set(range(1,299)) and len(rows)==298
        assert all(r['active']=='0000' and r['writes']=='0' and r['assistance']=='none' for r in rows)
    return dict(pairedNativeUpdates=len(on),mixedStereoPCMBytesHashed=sum(int(r['bytes']) for r in on),
        mixedStereoSampleFrames=sum(int(r['bytes'])//4 for r in on),nonzeroSignedSamples=sum(int(r['nonzero']) for r in on),
        peak=max(int(r['peak']) for r in on),importedChannelsIdleFields=298,perUpdateSHA256AndLevelsEqual=True)

def main():
    out=sync.ROOT/'audit_bounded_kung_lao_split_pcm_digest_checked';assert not out.exists();results={}
    proof_path=sync.ROOT/'audit_bounded_kung_lao_split_dcs_delivery_checked/report.json'
    proof=json.loads(proof_path.read_text());assert proof['passed']
    for side in (1,2):
        for fighter in ('sonya','kano'):
            key=f'{fighter}P{side}';base=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_dcs_delivery_runtime'
            assert sync.sha(base/'run.log')==proof['results'][key]['logSha256']
            original,_,_,_=load(base);captures=[];terminals=[];pins={}
            for label in ('samples','nosamples'):
                folder=sync.ROOT/f'audit_bounded_{fighter}_p{side}_kung_lao_split_pcm_{label}_runtime'
                t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
                assert not (folder/'stderr.log').read_text().strip();capture=load(folder)
                assert capture[0]==original;captures.append(capture);terminals.append(t);pins[label]=sync.sha(folder/'run.log')
            action=dict(re.findall(r'(\w+)=([^\s]+)',next(r for r in original if r.startswith('MK2_STOCK_HEAD_V921_ACTION '))))
            terminal=dict(re.findall(r'(\w+)=([^\s]+)',next(r for r in original if r.startswith('MK2_STOCK_HEAD_V921_BOUNDED_TERMINAL '))))
            begin,end=int(action['frame']),int(terminal['frame']);assert end-begin==299
            on,off=captures[0][1],captures[1][1];masks=[c[2] for c in captures];stop=captures[0][3]
            assert captures[1][3]==stop;accepted=gate(on,off,masks,stop,begin,end);faults=[]
            bad=copy.deepcopy(off);bad[0]['sha256']='0'*64
            try:gate(on,bad,masks,stop,begin,end)
            except AssertionError:faults.append('changed_waveform_digest')
            else:raise AssertionError('PCM fault accepted')
            bad=copy.deepcopy(masks);bad[0][0]['active']='0001'
            try:gate(on,off,bad,stop,begin,end)
            except AssertionError:faults.append('phantom_imported_sample')
            else:raise AssertionError('Channel fault accepted')
            results[key]=dict(**accepted,originalControlVoiceAndPacketsUnchanged=True,rejectedFaults=faults,terminals=terminals,logHashes=pins)
    source=sync.ROOT/'mame-mkp/src/frontend/mame/luaengine.cpp';text=source.read_text()
    assert 'sm.sample_count() * 2 * 2' in text and 'sm.samples(ptr);' in text
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        soundAPISourceSHA256=sync.sha(source),luaHashSourceSHA256=sync.sha(sync.ROOT/'tools/bounded_pcm_sha256.lua'),
        deliveryProofSha256=sync.sha(proof_path),cryptographicMixedPCMConsistencyVerified=True,
        retainedRawByteComparisonAccepted=False,stockWholeWaveformParityAccepted=False,heardAudioAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,cases={k:{a:r[a] for a in ('pairedNativeUpdates','mixedStereoPCMBytesHashed','peak')} for k,r in results.items()})))

if __name__=='__main__':main()
