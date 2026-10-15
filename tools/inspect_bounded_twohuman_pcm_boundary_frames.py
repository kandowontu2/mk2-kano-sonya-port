"""Exact frame digest census with unchanged larger blocks and gameplay."""
import json,re
import verify_native_source_sync as sync
from qualify_bounded_twohuman_hit_pcm import pcm
from qualify_bounded_twohuman_hit_voice_state import load

def main():
    out=sync.ROOT/'audit_bounded_twohuman_pcm_boundary_frames_observed';assert not out.exists()
    captures=[];pins={};terminals=[]
    for label in ('samples','nosamples'):
        folder=sync.ROOT/f'audit_bounded_twohuman_pcm_boundary_frames_{label}_runtime'
        old=sync.ROOT/f'audit_bounded_twohuman_hit_pcm_boundary_{label}_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        assert pcm(folder)==pcm(old) and load(folder)[1]==load(old)[1]
        rows={};blocks=[];oldblocks=[]
        for location,target in ((folder,blocks),(old,oldblocks)):
            with (location/'run.log').open() as stream:
                for line in stream:
                    assert '[LUA ERROR]' not in line
                    if line.startswith('MK2_HSPECIAL_PCM_BOUNDARY '):target.append(line.strip())
                    if location==folder and line.startswith('MK2_HSPECIAL_PCM_STEREO_FRAME '):
                        r=dict(re.findall(r'(\w+)=([^\s]+)',line));n=int(r['stereo_frame'])
                        assert n not in rows and r['seconds']=='25.460000000000' and r['writes']=='0' and r['raw_media']=='none'
                        assert re.fullmatch('[0-9A-F]{64}',r['sha256']);rows[n]=r
        assert blocks==oldblocks and set(rows)==set(range(16))
        captures.append(rows);pins[str(folder/'run.log')]=sync.sha(folder/'run.log');terminals.append(t)
    on,off=captures;different=[n for n in range(16) if on[n]!=off[n]]
    assert different
    report=dict(passed=True,differentStereoFrameIndices=different,
        upperBoundResidualMicroseconds=(max(different)+1)*1000000/48000,
        wholeUpdatesBlocksAndGameplayUnchanged=True,logPins=pins,terminals=terminals,
        sourceSync=sync.verify(),intraUpdateCutoffExplained=False,heardQualityAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,differentStereoFrameIndices=different,upperBoundResidualMicroseconds=report['upperBoundResidualMicroseconds'])))

if __name__=='__main__':main()
