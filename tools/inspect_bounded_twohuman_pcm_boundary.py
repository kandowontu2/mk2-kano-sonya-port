"""Exact block census and unchanged whole-update digests, no audio data."""
import json,re
import verify_native_source_sync as sync
from qualify_bounded_twohuman_hit_pcm import pcm
from qualify_bounded_twohuman_hit_voice_state import load

def main():
    out=sync.ROOT/'audit_bounded_twohuman_pcm_boundary_observed';assert not out.exists()
    captures=[];pins={};terminals=[]
    for label in ('samples','nosamples'):
        folder=sync.ROOT/f'audit_bounded_twohuman_hit_pcm_boundary_{label}_runtime'
        old=sync.ROOT/f'audit_bounded_twohuman_hit_pcm_{label}_runtime'
        terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        assert pcm(folder)==pcm(old) and load(folder)[1]==load(old)[1]
        blocks={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_PCM_BOUNDARY '):
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));key=(r['seconds'],int(r['first_stereo_frame']))
                    assert key not in blocks and r['frames']=='16' and r['writes']=='0' and r['raw_media']=='none'
                    assert re.fullmatch('[0-9A-F]{64}',r['sha256']);blocks[key]=r
        assert set(blocks)=={(time,n) for time in ('25.440000000000','25.460000000000','25.480000000000') for n in range(0,960,16)}
        captures.append(blocks);pins[str(folder/'run.log')]=sync.sha(folder/'run.log');terminals.append(terminal)
    on,off=captures;results={}
    for time in ('25.440000000000','25.460000000000','25.480000000000'):
        different=[n for n in range(0,960,16) if on[time,n]!=off[time,n]]
        results[time]=dict(differentBlockStarts=different,identicalBlocks=60-len(different),blockStereoFrames=16)
    assert results['25.480000000000']['identicalBlocks']==60
    report=dict(passed=True,wholeUpdatesAndPhysicalGameplayUnchanged=True,results=results,
        logPins=pins,terminals=terminals,sourceSync=sync.verify(),intraUpdateCutoffExplained=False,heardQualityAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(results))

if __name__=='__main__':main()
