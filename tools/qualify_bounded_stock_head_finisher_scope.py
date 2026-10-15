"""Keep scoped victim name separate from STATE's victim actor tuple."""
import copy,json,re
from pathlib import Path
import verify_native_source_sync as sync
import qualify_bounded_stock_head_finisher as original

def main():
    out=sync.ROOT/'audit_bounded_stock_head_finisher_scope_checked';assert not out.exists()
    results={}
    prefix=re.compile(r'^MK2_STOCK_HEAD_V921_(\w+) frame=(\d+) victim=(\w+) side=(\d+) killer=(\w+) writes=(\d+) assistance=(\w+)(?: |$)')
    for fighter,ident in (('sonya',18),('kano',17)):
        folder=sync.ROOT/f'audit_bounded_{fighter}_stock_head_finisher_runtime'
        terminal=json.loads((folder/'terminal.json').read_text())
        assert terminal['exitCode']==0 and terminal['limitReason'] is None
        assert not (folder/'stderr.log').read_text().strip()
        rows=[]
        with (folder/'run.log').open() as stream:
            for line in stream:
                assert '[LUA ERROR]' not in line and len(line)<65536
                if not line.startswith('MK2_STOCK_HEAD_V921_'):continue
                match=prefix.match(line);assert match
                tag,frame,name,side,killer,writes,assistance=match.groups()
                assert (name,side,killer,writes,assistance)==(fighter,'1','baraka','0','none')
                r=dict(re.findall(r'(\w+)=([^\s]+)',line));assert r['frame']==frame
                rows.append((tag,r))
        positive=original.gate(rows,fighter,ident);faults=[]
        for name,key,value in (('wrong_damage','damage','321'),('missing_native_win','wins','1'),('wrong_wrap','wrap','0')):
            bad=copy.deepcopy(rows);next(r for t,r in bad if t=='RESULT')[key]=value
            try:original.gate(bad,fighter,ident)
            except AssertionError:faults.append(name)
            else:raise AssertionError('Fault accepted '+name)
        results[fighter]=dict(**positive,rejectedFaults=faults,terminal=terminal,logSha256=sync.sha(folder/'run.log'))
    report=dict(passed=True,results=results,sourceSync=sync.verify(),checkerSha256=sync.sha(Path(__file__)),
        reusedGateSha256=sync.sha(Path(original.__file__)),fullFinisherArtAccepted=False,
        fullFinisherAudioAccepted=False,allFinishersAccepted=False,fullGoalComplete=False)
    out.mkdir();(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(passed=True,results=results)))

if __name__=='__main__':main()
