"""Same early-stop gate on real opposite-slot human context."""
import inspect,json
from pathlib import Path
import verify_native_source_sync as sync
import qualify_bounded_twohuman_hit_voice_state as previous

def main():
    source=inspect.getsource(previous.gate)
    for before,after in {"r['slot']=='1'":"r['slot']=='2'",'01034E90':'010350A0','0106A370':'0106B150',"r['channel']=='11'":"r['channel']=='13'"}.items():
        assert before in source;source=source.replace(before,after)
    namespace=dict(previous.__dict__);exec(compile(source,__file__+'::p2_gate','exec'),namespace)
    folder=sync.ROOT/'audit_bounded_twohuman_p2_hit_voice_runtime'
    out=folder/'voice_state_check.json';assert not out.exists()
    terminal=json.loads((folder/'terminal.json').read_text());assert terminal['exitCode']==0 and terminal['limitReason'] is None
    assert not (folder/'stderr.log').read_text().strip()
    rows,fields=previous.load(folder);assert len(fields)==842
    for tag,r in rows:
        if tag=='MK2_HSPECIAL_FIELD':assert r['id']==r['roster']==('17' if r['slot']=='1' else '18') and r['actor']==r['owner'] and r['state']=='1'
    uppercuts=[r for tag,r in rows if tag=='MK2_HSPECIAL_ACTION_WRITE' and r['value']=='0107']
    assert len(uppercuts)==1 and uppercuts[0]['slot']=='1' and uppercuts[0]['pc']=='FF83C340'
    positive=namespace['gate'](rows,66523)
    report=dict(passed=True,**positive,trueKanoP1SonyaP2ActorFields=842,actualUppercut=uppercuts[0],terminal=terminal,
        sourceSync=sync.verify(),mixedOutputAccepted=False,heardQualityAccepted=False,fullGoalComplete=False,
        logSHA256=sync.sha(folder/'run.log'),checkerSHA256=sync.sha(Path(__file__)))
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(passed=True,**positive)))

if __name__=='__main__':main()
