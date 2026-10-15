"""Opposite-slot complete-window convergence and exact boundary inventory."""
import inspect,json,re,copy
from decimal import Decimal
from pathlib import Path
import verify_native_source_sync as sync
import qualify_bounded_twohuman_hit_pcm as previous
import qualify_bounded_twohuman_hit_voice_state as state

def main():
    source=inspect.getsource(previous.gate)
    source=source.replace("if Decimal(a['seconds'])>cleared]","if Decimal(a['seconds'])-Decimal('.02')>=cleared]")
    source=source.replace("<Decimal('.02')","<Decimal('.04')")
    namespace=dict(previous.__dict__);exec(compile(source,__file__+'::complete_windows','exec'),namespace)
    base=sync.ROOT/'audit_bounded_twohuman_p2_hit_voice_runtime'
    proof_path=base/'voice_state_actor_count_check.json';proof=json.loads(proof_path.read_text());assert proof['passed']
    assert sync.sha(base/'run.log')==proof['logSHA256']
    _,original=state.load(base);captures=[];frames=[];pins={};terminals=[]
    for label in ('samples','nosamples'):
        folder=sync.ROOT/f'audit_bounded_twohuman_p2_hit_pcm_{label}_runtime'
        t=json.loads((folder/'terminal.json').read_text());assert t['exitCode']==0 and t['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        assert state.load(folder)[1]==original
        captures.append(previous.pcm(folder));one={}
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line
                if line.startswith('MK2_HSPECIAL_PCM_STEREO_FRAME '):
                    r=dict(re.findall(r'(\w+)=([^\s]+)',line));n=int(r['stereo_frame'])
                    assert n not in one and r['seconds']=='25.460000000000';one[n]=r
        assert set(one)==set(range(16));frames.append(one)
        pins[str(folder/'run.log')]=sync.sha(folder/'run.log');terminals.append(t)
    hit,cleared=Decimal(proof['hitSeconds']),Decimal(proof['firstClearedOwnerSeconds'])
    on,off=captures;accepted=namespace['gate'](on,off,hit,cleared)
    different=[n for n in range(16) if frames[0][n]!=frames[1][n]]
    faults=[];bad=copy.deepcopy(off)
    next(r for r in bad if Decimal(r['seconds'])-Decimal('.02')>=cleared)['sha256']='0'*64
    try:namespace['gate'](on,bad,hit,cleared)
    except AssertionError:faults.append('post_cleanup_difference')
    else:raise AssertionError('Output fault accepted')
    try:namespace['gate'](off,off,hit,cleared)
    except AssertionError:faults.append('absent_positive_contribution')
    else:raise AssertionError('Positive fault accepted')
    out=sync.ROOT/'audit_bounded_twohuman_p2_hit_pcm_checked';assert not out.exists()
    report=dict(passed=True,**accepted,differentBoundaryStereoFrameIndices=different,
        unchangedPhysicalGameplay=True,rejectedFaults=faults,logPins=pins,terminals=terminals,
        sourceSync=sync.verify(),heardQualityAccepted=False,intraUpdateCutoffExplained=False,fullGoalComplete=False,
        checkerSHA256=sync.sha(Path(__file__)),ownerProofSHA256=sync.sha(proof_path))
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,**accepted,differentBoundaryStereoFrameIndices=different)))

if __name__=='__main__':main()
